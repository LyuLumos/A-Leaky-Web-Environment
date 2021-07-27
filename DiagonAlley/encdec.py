# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import os
import string
import random


m = "1"
key = ''.join(random.sample(string.ascii_letters + string.digits, 16))
iv =  ''.join(random.sample(string.ascii_letters + string.digits, 16))

key, iv = key.encode('utf-8'), iv.encode('utf-8')
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
# print(dec(enc(1)))
# print(dec(enc("1")))
# print(type(True), type(False))