__author__ = 'shookees'

import time
import http.server
from urllib.parse import parse_qs
from Auth.Authenticator import Authenticator

class CaesarLoginHandler(http.server.BaseHTTPRequestHandler):


    def check_login(self, data):
        validLogin = False
        if "username" in data.keys() and "password" in data.keys():
            validLogin = Authenticator().checkAuthenticity(''.join(data["username"]), ''.join(data["password"]))

        if validLogin:
            code = 200
        else:
            code = 401

        return (code, self.responses[code][0])

    actions = {
        "login": check_login
    }

    def do_POST(self):
        print("POST request received")
        data = self.get_data()
        if "action" in data.keys():
            if ''.join(data["action"]) in self.actions.keys():
                (code, msg) = self.actions[''.join(data["action"])](self, data)
                self.send_response(code, msg)
                self.end_headers()
            else:
                self.send_error(501, self.responses[501][0], self.responses[501][1])
        else:
            self.send_error(400, self.responses[400][0], self.respones[400][1])

    def get_data(self):
        length = int(self.headers["Content-Length"])
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
