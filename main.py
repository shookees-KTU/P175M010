#!/usr/bin/env python
# -*- coding: utf-8 -*-

#P aulius Šukys, IFC-1 grupė, P175M010 Taikomoji Kriptografija
# L1

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
            print "line index == letter_index = " + str(line_index)
            cipher_text += plain_text[line_index]
            while letter_index + 2 * key < len(plain_text):
                #Egzistuoja poros, kurių viršūnės susiliečia
                letter_index += 2 * key
                cipher_text += plain_text[letter_index - (line_index + 1)] 
                cipher_text += plain_text[letter_index + line_index]
                


        return cipher_text

    #def decode(self, cipher_text, key):
        

if __name__ == "__main__":
    rf = RailFence()
    key = 4
    cipher = rf.encode("Hippopotamus", key)
    print cipher
    #print rf.decode(cipher, key)
