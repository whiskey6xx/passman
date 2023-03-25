#!/usr/bin/python

#the cryptman should be able to produce a key from the master password  

#the key should be stored in id 666 and should not be listed

#the key should be used to encrypt inputed credentials

#the key should be used to decrypt the outputed credentials


import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def create_key(master_password, salt=b''):
    """Creates a 256-bit key using PBKDF2 and the master password and salt."""
    # Generate a 256-bit key using PBKDF2 with the master password and salt
    key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), salt, 100000)
    return key
#create and store the key and salt in id 666

def encrypt(plaintext, key):
    """Encrypts the plaintext using AES with the given key."""
    # Create an AES cipher object with the key and IV
    cipher = AES.new(key, AES.MODE_CBC)
    # Pad the plaintext to a multiple of 16 bytes
    padded_plaintext = pad(plaintext.encode(), AES.block_size)
    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)
    # Return the IV and ciphertext concatenated
    return cipher.iv + ciphertext

def decrypt(ciphertext, key):
    """Decrypts the ciphertext using AES with the given key."""
    # Extract the IV and ciphertext from the input
    iv, ciphertext = ciphertext[:AES.block_size], ciphertext[AES.block_size:]
    # Create an AES cipher object with the key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    # Decrypt the ciphertext and unpad the plaintext
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    # Return the plaintext as a string
    return plaintext.decode()


