#!/usr/bin/env python
# -*- coding: utf-8 -*-

#P aulius Šukys, IFC-1 grupė, P175M010 Taikomoji Kriptografija
# L1
import math


class Cipher:
    def encode(self, plain_text, key):
        raise NotImplementedError("Encoding not implemented")

    def decode(self, cipher_text, key):
        raise NotImplementedError("Decoding not implemented")

class RailFence(Cipher):
    '''
    Rail Fence šifro implementacija
    http://en.wikipedia.org/wiki/Rail_fence_cipher
    Raktas (Key) - eilučių kiekis

    Pavyzdys su raktu - 3:
    LABAS PASAULI

    L P A I
    A S S L
    B A A U

    LPAIASSLBAAU
    '''
    def encode(self, plain_text, key):
        cipher_text = ""
        
        for line_index in xrange(0, key):
            letter_index = 0
            cipher_text += plain_text[line_index]
            while letter_index + 2 * key - (line_index + 1) < len(plain_text):
                #Egzistuoja poros, kurių viršūnės susiliečia
                letter_index += 2 * key
                cipher_text += plain_text[letter_index - (line_index + 1)] 
                if letter_index + line_index >= len(plain_text):
                    break
                cipher_text += plain_text[letter_index + line_index]
                


        return cipher_text

    def decode(self, cipher_text, key):
        #Reikia sužinoti ar yra uodega ir kuriame gale
        #uodega iš viršaus į apačią - teigiama
        #iš apačios į viršų - neigiama
        #
        #pradžioje pradedama nuo viršaus į apačią, nelyginis skaičius
        plain_text = ""
        uodega = len(cipher_text) % key #nustatomas ilgis
        uodega *= 1 if math.ceil(len(cipher_text)/key) % 2 == 0 else -1#nustatoma kryptis
        

        return plain_text


if __name__ == "__main__":
    rf = RailFence()
    key = 4
    cipher = rf.encode("Hippopotamusas", key)
    print cipher
    print rf.decode(cipher, key)
