__author__ = 'shookees'

import os
import sys
import sqlite3 as lite

class AuthDB:
    def __init__(self):
        self.conn = None
        self.dbFile = self.getCurrPath() + "auth.db"
        print(self.dbFile)
        try:
            self.conn = lite.connect(self.dbFile)
            self.cur = self.conn.cursor()
        except lite.Error as e:
            print("AuthDB Error %s:" % e.args[0])
        finally:
            self.close()

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

    def getUserPassword(self, username):
        try:
            self.cur.execute("SELECT password FROM users WHERE username = %s" % username)
            return self.cur.fetchone()
        except lite.Error as e:
            print(e)
            return None

    def checkUsername(self, username):
        return username in self.getUsers()

    def checkUserPassword(self, username, password):
        if (self.checkUsername(username)):
            return self.getUserPassword(username) == password
        else:
            return False #the username is not legit
