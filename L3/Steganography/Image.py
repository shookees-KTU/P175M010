# coding=utf-8
__author__ = 'shookees'

# tekstas yra slepiamas mėlynoje spalvoje 0-5 hex rėžiuose

from PIL import Image
import binascii

DELIMITER = "1" * 15 + "0"  #atskyrimui naudojama 15 1 ir 0


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def hex2rgb(hex):
    return tuple(map(ord, hex[1:].decode('hex')))  #pašalinamos grotelės ir tiesiog konvertuojama


def bin2str(binary):
    return binascii.unhexlify('%x' % (int(binary,2)))  #TODO: gražesnis apipavidalinimas


def str2bin(message):
    return bin(int(binascii.hexlify(message), 16))[2:]


def encode(hex, number):
    if int(hex[-1], 16) in range(0, 6):  #žiūri ar paskutinis hexo skaičius yra slepiamos mėlynos spalvos rėžiuose
        return hex[:-1] + number
    else:
        return None


def decode(hex):
    if int(hex[-1]) in range(0, 2):
        return hex[-1]
    else:
        return None


def hide(filename, message):
    '''
    Hides a message text in an image
    :param filename: path to the PNG file
    :param message: message to be hidden in the PNG file
    :return: True if succesfully hidden; else False
    '''
    im = Image.open(filename)  # paveikslėlis, kuris bus steganografuojamas
    bin = list(str2bin(message) + DELIMITER)  # tekstas, kuris bus įsiūtas
    img = im.convert("RGB")  # sutvarkoma, kad būtų nuskaitoma vienodai
    data = img.getdata()
    newData = []
    for pixel in data:
        if len(bin) > 0:
            pixelBin = encode(rgb2hex(pixel[0], pixel[1], pixel[2]), bin.pop(0))  # išimamas pirmas elementas
            if pixelBin == None:
                newData.append(pixel)
            else:
                newData.append(hex2rgb(pixelBin))
        else:
            newData.append(pixel)

    img.putdata(newData)
    img.save(filename)
    return True

def retrieve(filename):
    '''
    Retrieves text from an image
    :param filename:
    :return:
    '''
    img = Image.open(filename)
    bin = b''
    img = img.convert("RGB")
    data = img.getdata()
    for pixel in data:
        num = decode(rgb2hex(pixel[0], pixel[1], pixel[2]))
        if num != None:
            bin += num
            if bin[-16:] == DELIMITER:
                return bin2str(bin[:-16])

    return bin2str(bin)

