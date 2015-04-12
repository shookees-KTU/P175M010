__author__ = 'shookees'

import time
import http.server
from urllib.parse import parse_qs
from Auth.Authenticator import Authenticator

class CaesarLoginHandler(http.server.BaseHTTPRequestHandler):
    actions = {
        "login":
    }

    def check_login(self, username, password):
        return Authenticator().checkAuthenticity(username, password)

    def do_POST(self):
        print("POST request received")
        data = self.get_data()
        #Patirkina ar turi palaikomą veiksmą
        for key in data.keys():
            if key in self.actions:
                actions[key](data)
        else:




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
