from Frontend import Frontend
from key_generator import *


def prototype(input_file, output_file, password):
    print(input_file, output_file, password)
    hash, asymmetric_key, symmetric_key = "abcd", "efgh", "ijkl"
    return hash, asymmetric_key, symmetric_key


frontend = Frontend(encryption_function=encrypt_file, decryption_function=decrypt_file)
