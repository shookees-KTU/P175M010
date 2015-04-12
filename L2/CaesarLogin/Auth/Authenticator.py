__author__ = 'shookees'
# -*- coding: utf-8 -*-
from . import adb

class Authenticator:
    def checkAuthenticity(self, username, password):
        return adb.checkUsername(username) and adb.checkUserPassword(username, password)