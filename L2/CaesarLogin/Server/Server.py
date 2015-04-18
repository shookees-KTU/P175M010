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
            self.send_response(301)
            self.send_header("Encoding", "utf-8")
            self.send_header("Set-Cookie", 'host="{0}"'.format(cookie["host"].encode("utf-8")))
            self.send_header("Set-Cookie", 'token="{0}"'.format(cookie["token"].encode("utf-8")))
            self.send_header("Location", "/")
            self.end_headers()
        else:
            code = 401
            self.send_error(401, self.responses[401][0], self.responses[401][1])

    def getAuthCookie(self, username):
        host, port = self.client_address
        cipher = Caesar()
        #sausainis identifikacijai
        session = Authenticator().createSession(username, host)
        C = {}
        C["host"] = cipher.encode(session[2], session[4]) # host, key
        C["token"] = session[0] # token ir taip kriptinis
        return C

    actions = {
        "login": check_login
    }

    def do_GET(self):
        print("GET request received")
        print(self.headers)
        if "Cookie" in self.headers:
            cookie = cookies.SimpleCookie(self.headers["Cookie"])
            self.showHelloPage(cookie["token"].value)
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
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        token = token[2:-1] #pašalinamos šiukšlės
        session = Authenticator().adb.getSession(token)
        if session is None:
            self.wfile.write(bytes("<h1>Klaida</h1>", "UTF-8"))
        else:
            self.wfile.write(bytes("<h1>Labas, {0}</h1>".format(session[1]), "UTF-8"))

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
