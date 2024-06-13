from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import struct


def encrypt_file(password, infile_path, outfile_path=None, chunksize=64 * 1024):
    # Get filename and convert to bytes
    filename = os.path.basename(infile_path).encode()
    filename_length = len(filename)

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

    # Determine output file path
    if not outfile_path:
        outfile_path = os.path.splitext(infile_path)[0] + '.enc'

    # Open output file
    with open(outfile_path, 'wb') as outfile:
        # Write salt, iv, and filename length
        outfile.write(salt)
        outfile.write(iv)
        outfile.write(struct.pack('<I', filename_length))
        outfile.write(filename)

        encryptor = cipher.encryptor()
        with open(infile_path, 'rb') as infile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.update(chunk))

    return outfile_path


def decrypt_file(password, infile_path, outfile_path=None, chunksize=24 * 1024):
    with open(infile_path, 'rb') as infile:
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

        # Read filename length and filename
        filename_length = struct.unpack('<I', infile.read(4))[0]
        filename = infile.read(filename_length).decode()

        # Determine output file
        if not outfile_path:
            outfile_path = os.path.dirname(infile_path)
            if outfile_path != "":
                outfile_path += "/"
            outfile_path += filename
        else:
            outfile_path += os.path.splitext(filename)[1]

        decryptor = cipher.decryptor()

        with open(outfile_path, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.update(chunk))

    return outfile_path
