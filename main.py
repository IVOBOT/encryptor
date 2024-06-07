from Frontend import Frontend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


# from key_generator import *

def encrypt_file(password, infile, outfile, chunksize=64*1024):
    salt = os.urandom(16)
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    key = kdf.derive(password.encode())

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)

    outfile.write(salt)
    outfile.write(iv)

    encryptor = cipher.encryptor()
    while True:
        chunk = infile.read(chunksize)
        if len(chunk) == 0:
            break
        elif len(chunk) % 16 != 0:
            chunk += b' ' * (16 - len(chunk) % 16)

        outfile.write(encryptor.update(chunk))

def decrypt_file(password, infile, outfile, chunksize=24*1024):
    salt = infile.read(16)
    iv = infile.read(16)
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    key = kdf.derive(password.encode())

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)

    decryptor = cipher.decryptor()
    while True:
        chunk = infile.read(chunksize)
        if len(chunk) == 0:
            break
        outfile.write(decryptor.update(chunk))

def prototype(input_file, output_file, password):
    print(input_file, output_file, password)
    hash, asymmetric_key, symmetric_key = "abcd", "efgh", "ijkl"
    return hash, asymmetric_key, symmetric_key


frontend = Frontend(encryption_function=encrypt_file, decryption_function=decrypt_file)
