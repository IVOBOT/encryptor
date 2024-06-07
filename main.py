from Frontend import Frontend
from key_generator import encrypt_file, decrypt_file

Frontend(encryption_function=encrypt_file, decryption_function=decrypt_file)
