__author__ = 'shookees'

#from Auth.Authenticator import AuthDB
#from Ciphers.Caesar import Caesar
from Server.Server import SimpleServer

if __name__ == "__main__":
    host = "localhost"
    port = 8080
    server = SimpleServer(host, port)
