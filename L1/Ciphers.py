# -*- coding: utf-8 -*-

# Paulius Šukys, IFC-1 grupė, P175M010 Taikomoji Kriptografija
# L1

import math


class Cipher:
    def encode(self, plain_text, key):
        raise NotImplementedError("Encoding not implemented")

    def decode(self, cipher_text, key):
        raise NotImplementedError("Decoding not implemented")

    def cryptoanalyze(self, cipher_text):
        raise NotImplementedError("Crypto analysis not implemented")

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
        #išimami tarpai
        plain_text = plain_text.replace(" ", "")
        
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
        columns = int(math.ceil(len(cipher_text) / float(key)))
        tail = len(cipher_text) % key #nustatomas ilgis
        tail *= -1 if columns % 2 == 0 else 1 #nustatoma kryptis
        ind = 0 #zingsnis, kurio pagalba kopijuojamas tekstas į grupes
        grupes = [] #grupes, tai atbuliniu zingsniu sudaryta tvorele
        for i in xrange(0, key):
            #pridedamas papildomas kiekis (1 daugiau) simbolių, nei įprastai
            if (tail > 0 and i <= tail - 1) or (tail < 0 and i >= key + tail):
                grupes.append(cipher_text[ind: ind + columns])
                ind += columns
            else:
                grupes.append(cipher_text[ind: ind + columns - 1])
                ind += columns - 1

        #gautos grupes, formuojamas tekstas
        for column in xrange(0, columns):
            iterator = xrange(0, key)
            
            if column % 2 == 1:
                #apverciamas iterator
                iterator = reversed(iterator)

            for eilute in iterator:
                if (column <= len(grupes[eilute]) - 1):
                    plain_text += grupes[eilute][column]

        return plain_text

    def cryptoanalyze(self, cipher_text):
        key = 1
        possible_answers = {}
        while key < len(cipher_text) - 1:
            possible_answers[key] = self.decode(cipher_text, key)
            key += 1

        return possible_answers