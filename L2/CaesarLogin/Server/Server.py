__author__ = 'shookees'
# -*- coding: utf-8 -*-
import time
import http.server
import os
from Ciphers.Caesar import Caesar
from http import cookies
from urllib.parse import parse_qs
from Auth.Authenticator import Authenticator

class CaesarLoginHandler(http.server.BaseHTTPRequestHandler):


    def check_login(self, data):
        validLogin = False
        if "username" in data.keys() and "password" in data.keys():
            validLogin = Authenticator().checkAuthenticity(''.join(data["username"]), ''.join(data["password"]))

        if validLogin:
            cookie = self.getAuthCookie(data["username"])
            self.send_response(200)
            self.send_header("Set-Cookie", cookie.output().encode("utf-8"))
        else:
            code = 401
            self.send_error(401, self.responses[401][0], self.responses[401][1])

    def getAuthCookie(self, username):
        host, port = self.client_address
        cipher = Caesar()
        #sausainis identifikacijai
        session = Authenticator().createSession(username, host)
        C = cookies.SimpleCookie()
        C["host"] = cipher.encode(session[2], session[4]) # host, key
        C["token"] = cipher.encode(session[0], session[4]) # token, key
        return C

    actions = {
        "login": check_login
    }

    def do_GET(self):
        print("GET request received")
        if "HTTP_COOKIE" in os.environ:
            cookies = os.environ["HTTP_COOKIE"].split('; ')
            c = {}
            for cookie in cookies:
                cookie = cookie.split('=')
                c[cookie[0]] = cookie[1]
            self.showHelloPage(c["token"])
        else:
            if self.path == "/login":
                self.showLoginPage()
            else:
                self.send_error(401, self.responses[401][0], self.responses[401][1])

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

    def showHelloPage(self, token):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<h1>{0}</h1>".format(Authenticator().adb.getSession(token)[1]))

    def showLoginPage(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("<h1>Prašau prisijungti</h1>".encode("utf-8"))
        self.wfile.write(("<form method='POST'>"
                         "Vardas:<br />"
                         "<input type='text' name='username'><br />"
                         "Slaptažodis:<br />"
                         "<input type='password' name='password'><br />"
                         "<input type='submit' name='action' value='login'>"
                         "</form>").encode("utf-8"))
        self.wfile.close()


    def get_data(self):
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
