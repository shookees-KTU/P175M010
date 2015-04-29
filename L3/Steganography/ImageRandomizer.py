__author__ = 'shookees'

import requests
import os
from PIL import Image
def createRandomImage(num):
    try:

        img = Image.open("/home/shookees/Documents/KTU/Bakalauras 2011-2015/4 kursas/2 pusmetis/[P175M010] Taikomoji kriptografija/Laboratoriniai/L3/base.png")
        img.save("/tmp/" + str(num), "PNG")
        return True  # del viso pikto pasitikriname ar tikrai grazina
    except requests.exceptions.RequestException:
        return False