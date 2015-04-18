__author__ = 'shookees'
# -*- coding: utf-8 -*-
from Auth.AuthDB import AuthDB
from Ciphers.Caesar import Caesar


class Authenticator:
    def __init__(self):
        self.adb = AuthDB()

    def checkAuthenticity(self, username, password):
        return self.adb.checkUsername(username) and self.adb.checkUserPassword(username, password)

    def createSession(self, username, host):
        token = self.adb.createSession(username, host)
        return self.adb.getSession(token)

    def checkSession(self, token, host):
        session = self.adb.getSession(token)
        cipher = Caesar()

    def getUserData(self, token):
        pass
