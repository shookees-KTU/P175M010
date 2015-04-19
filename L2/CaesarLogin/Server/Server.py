__author__ = 'shookees'
# -*- coding: utf-8 -*-
import time
import http.server
import html
from Ciphers.Caesar import Caesar
from http import cookies
from urllib.parse import urlparse, parse_qs
from Auth.Authenticator import Authenticator

class CaesarLoginHandler(http.server.BaseHTTPRequestHandler):

    def logout(self, session, params):
        #paprasčiausiai sugadinamas sausainis ir ištrinama iš db
        Authenticator().adb.removeSession(session[0])
        self.send_response(301)
        self.send_header("Encoding", "utf-8")
        self.send_header("Set-Cookie", 'host=""')
        self.send_header("Set-Cookie", 'token=""')
        self.send_header("Set-Cookie", 'key=""')
        self.send_header("Location", "/")
        self.end_headers()

    def check_login(self, data, params=None):
        validLogin = False
        if "username" in data.keys() and "password" in data.keys():
            validLogin = Authenticator().checkAuthenticity(''.join(data["username"]), ''.join(data["password"]))

        if validLogin:
            cookie = self.getAuthCookie(data["username"])
            self.send_response(301)
            self.send_header("Encoding", "utf-8")
            self.send_header("Set-Cookie", 'host="{0}"'.format(cookie["host"].encode("utf-8")))
            self.send_header("Set-Cookie", 'token="{0}"'.format(cookie["token"].encode("utf-8")))
            self.send_header("Set-Cookie", 'key="{0}"'.format(cookie["key"]))
            self.send_header("Location", "/")
            self.end_headers()
        else:
            code = 401
            self.send_error   (401, self.responses[401][0], self.responses[401][1])

    def getAuthCookie(self, username):
        host, port = self.client_address
        cipher = Caesar()
        #sausainis identifikacijai
        session = Authenticator().createSession(username, host)
        C = {}
        C["host"] = cipher.encode(session[2], session[4]) # host, key
        C["token"] = session[0] # token ir taip kriptinis
        C["key"] = session[4]
        return C

    def parseRequest(self, data, params=None):
        if "Cookie" in self.headers:
            #autentifikuojama
            cookie = cookies.SimpleCookie(self.headers["Cookie"])
            if len(cookie["token"].value) > 3:
                session = Authenticator().adb.getSession(cookie["token"].value[2: -1])
                if session is not None:
                    authenticated = True
        if authenticated:
            key = session[4]%26
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            print(data)
            if data["query"]:
                query = html.unescape(data["query"])[0]
                if query == Caesar().encode("labas", key):
                    self.wfile.write(bytes(html.escape(Caesar().encode("Nu labas", key)), "UTF-8"))
                else:
                    self.wfile.write(bytes(html.escape(Caesar().encode("Nežinau šitos komandos", key)), "UTF-8"))
            else:
                self.wfile.write(bytes(html.escape(Caesar().encode("ERROR", key)), "UTF-8"))

    actions = {
        "login": check_login,
        "logout": logout,
        "request": parseRequest
    }

    def do_GET(self):
        print("GET request received")
        authenticated = False
        session = None
        if "Cookie" in self.headers:
            #autentifikuojama
            cookie = cookies.SimpleCookie(self.headers["Cookie"])
            if len(cookie["token"].value) > 3:
                session = Authenticator().adb.getSession(cookie["token"].value[2: -1])
                if session is not None:
                    authenticated = True
        if authenticated:
            self.showPage(session, self.path)
        else:
            self.showLoginPage()

    def do_POST(self):
        print("POST request received")
        data = self.get_data()
        if "action" in data.keys():
            if ''.join(data["action"]) in self.actions.keys():
                self.actions[''.join(data["action"])](self, data)
            else:
                self.send_error(501, self.responses[501][0], self.responses[501][1])
        else:
            self.send_error(400, self.responses[400][0], self.responses[400][1])

    def showPage(self, session, path):
        params = parse_qs(urlparse(path).query)
        data = self.get_data()
        if "action" in params.keys():
            self.actions[''.join(params["action"])](self, session, params)
        elif path == "/":
            self.showHelloPage(session)

    def showHelloPage(self, session):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("<h1>Labas, {0}</h1>\n".format(session[1]), "UTF-8"))
        self.wfile.write(bytes("<a href='?action=logout'>Atsijungti</a>\n", "UTF-8"))
        self.wfile.write(bytes("<form name='f1'>\n<p>Tekstas: <input name='word' type='text'>\n", "UTF-8"))
        self.wfile.write(bytes("<input value='Siųsti' type='button' onclick='Javascript:xmlhttpPost(\"\")'></p>\n", "UTF-8"))
        self.wfile.write(bytes("<div id='result'></div>\n</form>\n", "UTF-8"))
        with open("js/server.js", "r") as file:
            self.wfile.write(bytes("<script type='text/javascript'>\n{0}\n</script>".format(file.read()), "UTF-8"))

    def showLoginPage(self):
        content = bytes("<h1>Prašau prisijungti</h1>"
                   "<form method='POST'>"
                   "Vardas:<br />"
                   "<input type='text' name='username'><br />"
                   "Slaptažodis:<br />"
                   "<input type='password' name='password'><br />"
                   "<input type='submit' name='action' value='login'>"
                   "</form>", "UTF-8")
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content)


    def get_data(self):
        data = None
        if self.headers["Content-Length"]:
            length = int(self.headers.get("Content-Length"))
            data = parse_qs(self.rfile.read(length).decode("utf-8"))
        return data

class SimpleServer:
    def __init__(self, host, port):
        self.port = port
        self.host = host
        self.handler = CaesarLoginHandler
        self.start()
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.close()

    def start(self):
        self.httpd = http.server.HTTPServer((self.host, self.port), self.handler)
        print(time.asctime(), "Server starts - %s:%s" % (self.host, self.port))

    def close(self):
        self.httpd.server_close()
        print(time.asctime(), "Server starts - %s:%s" % (self.host, self.port))
