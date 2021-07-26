# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import os



m = "1"
key = os.urandom(16)
iv =  os.urandom(16)


def enc(m):
    m=str(m)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padtext = pad(m.encode('utf-8'),16,style='pkcs7')
    return cipher.encrypt(padtext)

def dec(c):
    decrypter = AES.new(key, AES.MODE_CBC, iv)
    plaintext = decrypter.decrypt(c)
    plaintext = unpad(plaintext,16,style='pkcs7')
    return plaintext.decode('utf-8')

# print(enc(m))
# print(dec(enc(m)))
# print(type(True), type(False))