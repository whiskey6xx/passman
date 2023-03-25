#!/usr/bin/python

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import secrets


def make_salt():
    salt = secrets.token_hex(16)
    
    salt_bytes = salt.encode("utf-8")

    return salt_bytes

def create_key(master_password, salt):
    # Generate a 256-bit key using PBKDF2 with the master password and salt
    key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), salt, 100000)
    return key



def encrypt(plaintext, key):
    # Create an AES cipher object with the key and IV
    cipher = AES.new(key, AES.MODE_CBC)
    # Pad the plaintext to a multiple of 16 bytes
    padded_plaintext = pad(plaintext.encode(), AES.block_size)
    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)
    # Return the IV and ciphertext concatenated
    return cipher.iv + ciphertext

def decrypt(ciphertext, key):
    # Extract the IV and ciphertext from the input
    iv, ciphertext = ciphertext[:AES.block_size], ciphertext[AES.block_size:]
    # Create an AES cipher object with the key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    # Decrypt the ciphertext and unpad the plaintext
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    # Return the plaintext as a string
    return plaintext.decode()

