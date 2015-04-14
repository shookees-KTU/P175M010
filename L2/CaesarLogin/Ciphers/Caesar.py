__author__ = 'shookees'
# -*- coding: utf-8 -*-

from . import Cipher

class Caesar(Cipher):
    '''
    Caesar šifro implementacija
    http://en.wikipedia.org/wiki/Caesar_cipher
    Raktas (Key) - pastūmimo nuotolis ir kryptis (teigiama ar negiama)

    Pavyzdys su raktu - +3 (angliška abecėlė):
    L + 3 = O
    A + 3 = D
    B + 3 = E
    A + 3 = D
    S + 3 = V
    '''
    def encode(self, plain_text, key):
        return ''.join([ chr(ord(character) + key) for character in plain_text ])

    def decode(self, cipher_text, key):
        return ''.join([ chr(ord(character) - key) for character in cipher_text])