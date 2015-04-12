__author__ = 'shookees'

class Cipher:
    def encode(self, plain_text, key):
        raise NotImplementedError("Encoding")

    def decode(self, cipher_text, key):
        raise NotImplementedError("Decoding")

    def cryptoanalyze(self, cipher_text):
        raise NotImplementedError("Cryptoanalize")