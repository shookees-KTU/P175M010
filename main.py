#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Paulius Šukys, IFC-1 grupė, P175M010 Taikomoji Kriptografija
# L1

from Ciphers import RailFence


if __name__ == "__main__":
    rf = RailFence()
    text = "Hippopotamusas"
    key = 4
    print "Neužšifruotas tekstas: " + text
    cipher = rf.encode(text, key)
    print "Užšifruotas tekstas: " + cipher
    deciphered = rf.decode(cipher, key)

    if deciphered == text:
        print "Užšifruoto teksto atšifravimas sėkmingas"
    else:
        print "Užšifruoto teksto atšifravimas nesėkmingas"

    '''cryptoanalyzed = rf.cryptoanalyze(cipher)

    if text in cryptoanalyzed: #bet žodžių atpažinimo sunkiai galima nuspėti kuris žodis teisingas
        print "Kriptoanalizėje yra teisingas variantas" 
    else:
        print "Kriptoanalizėje nėra teisingo varianto"

    print cryptoanalyzed'''