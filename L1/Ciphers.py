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
        stulpeliu = int(math.ceil(len(cipher_text) / float(key)))
        uodega = len(cipher_text) % key #nustatomas ilgis
        uodega *= -1 if stulpeliu % 2 == 0 else 1 #nustatoma kryptis
       	ind = 0 #zingsnis, kurio pagalba kopijuojamas tekstas į grupes
       	grupes = [] #grupes, tai atbuliniu zingsniu sudaryta tvorele
       	for i in xrange(0, key):
       		#pridedamas papildomas kiekis (1 daugiau) simbolių, nei įprastai
       		if (uodega > 0 and i <= uodega - 1) or (uodega < 0 and i >= key + uodega):
       			grupes.append(cipher_text[ind: ind + stulpeliu])
       			ind += stulpeliu
       		else:
       			grupes.append(cipher_text[ind: ind + stulpeliu - 1])
       			ind += stulpeliu - 1

       	#gautos grupes, formuojamas tekstas
       	for stulpelis in xrange(0, stulpeliu):
       		iteratorius = xrange(0, key)
       		
       		if stulpelis % 2 == 1:
       			#apverciamas iteratorius
       			iteratorius = reversed(iteratorius)

       		for eilute in iteratorius:
       			if (stulpelis <= len(grupes[eilute]) - 1):
       				plain_text += grupes[eilute][stulpelis]

        return plain_text

    def cryptoanalyze(self, cipher_text):
        raktas = 1
        galimi_atsakymai = {}
        while raktas < len(cipher_text) - 1:
            galimi_atsakymai[raktas] = self.decode(cipher_text, raktas)
            raktas += 1

        return galimi_atsakymai