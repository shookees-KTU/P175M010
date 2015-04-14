__author__ = 'shookees'
# -*- coding: utf-8 -*-
import os
import sqlite3 as lite
import datetime
import random
import string

class AuthDB:
    def __init__(self):
        self.conn = None
        self.dbFile = os.path.join(self.getCurrPath(), "auth.db")
        try:
            self.conn = lite.connect(self.dbFile)
            self.cur = self.conn.cursor()
        except lite.Error as e:
            print("AuthDB Error %s:" % e.args[0])

    def close(self):
        if self.conn:
            self.conn.close()

    def getCurrPath(self):
        return os.path.dirname(os.path.realpath(__file__))

    def getUsers(self):
        try:
            self.cur.execute("SELECT username FROM users")
            return self.cur.fetchall()
        except lite.Error as e:
            print("getUsers")
            print(e)
            return []

    def getUserPassword(self, username):
        try:
            self.cur.execute("SELECT password FROM users WHERE username = '" + username + "'")
            return self.cur.fetchone()
        except lite.Error as e:
            print("getUserPassword")
            print(e)
            return None

    def checkUsername(self, username):
        return (username,) in self.getUsers()#tuple todel, kad ta grazina query

    def checkUserPassword(self, username, password):
        if self.checkUsername(username):
            return self.getUserPassword(username) == (password,)
        else:
            return False #the username is not legit

    def createSession(self, username, host):
        expiration = datetime.datetime.now() + datetime.timedelta(minutes=15)
        key = random.randint(1, 1024)#tiesiog skaicius, realiai dalinsis is alfabeto
        token = self.generateToken()
        while self.getSession(token) != None:
            token = self.generateToken()

        query = "INSERT INTO sessions(token, username, host, expiration, key) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(str(token), ''.join(username), str(host),
                                                                      int(expiration.strftime("%s")) * 1000, key)
        try:
            self.cur.execute(query)
        except lite.Error as e:
            print("createSession")
            print(e)
            return None
        finally:
            return token


    def generateToken(self):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(64))

    def getSession(self, token):
        try:
            self.cur.execute("SELECT token FROM sessions")

            if (token,) in self.cur.fetchall():
                self.cur.execute("SELECT token, username, host, expiration, key FROM sessions WHERE token = '{0}'".format(token))
                return self.cur.fetchone()
            else:
                return None
        except lite.Error as e:
            print("getSession")
            print(e)
            return None


