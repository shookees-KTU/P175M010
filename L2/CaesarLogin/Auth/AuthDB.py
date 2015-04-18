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
            print(e)
            return []

    def removeSession(self, token):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT token FROM sessions")
            tokens = cur.fetchall()
            if (token,) in tokens:
                cur.execute("DELETE FROM sessions WHERE token = '{0}'".format(token))
                self.conn.commit()
                return cur.fetchone()
            else:
                return None
        except lite.Error as e:
            print(e)
            return None

    def getUserPassword(self, username):
        try:
            self.cur.execute("SELECT password FROM users WHERE username = '" + username + "'")
            return self.cur.fetchone()
        except lite.Error as e:
            print(e)
            return ""

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

        query = "INSERT INTO sessions VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(str(token), int(expiration.strftime("%s")) * 1000, ''.join(username), str(host), key)
        try:
            self.cur.execute(query)
            self.conn.commit()
        except lite.Error as e:
            print(e)
            return ""
        finally:
            return token


    def generateToken(self):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(64))

    def getSession(self, token):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT token FROM sessions")
            tokens = cur.fetchall()
            if (token,) in tokens:
                cur.execute("SELECT token, username, host, expiration, key FROM sessions WHERE token = '{0}'".format(token))
                return cur.fetchone()
            else:
                return None
        except lite.Error as e:
            print(e)
            return None