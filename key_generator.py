import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding


def encrypt_with_public_key(data, public_key):
    # Wczytujemy klucz publiczny
    public_key = serialization.load_pem_public_key(public_key, backend=default_backend())

    # Szyfrujemy dane kluczem publicznym
    encrypted_data = public_key.encrypt(
        data,
        asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_data


def decrypt_with_private_key(encrypted_data, private_key):
    # Wczytujemy klucz prywatny
    private_key = serialization.load_pem_private_key(private_key, password=None, backend=default_backend())

    # Odszyfrowujemy dane kluczem prywatnym
    decrypted_data = private_key.decrypt(
        encrypted_data,
        asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_data


def create_asymmetric_key(password):
    # Obliczamy skrót hasła
    hashed_password = hashlib.sha256(password.encode()).digest()

    # Generujemy klucz prywatny RSA na podstawie skrótu hasła
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
        # Używamy skrótu hasła jako ziarna (seed) do generatora klucza
        private_exponent=int.from_bytes(hashed_password, 'big')
    )

    # Eksportujemy klucz prywatny do formatu PEM
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()  # Bez szyfrowania
    )

    # Eksportujemy klucz publiczny do formatu PEM
    public_key_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key_pem, public_key_pem


def cypher_file(filepath, cyphered_file_path, metadata_file_path, password):
    private_key_pem, public_key_pem = create_asymmetric_key(password)
    key = os.urandom(32)  # 256-bitowy klucz AES
    iv = os.urandom(16)  # 128-bitowy wektor inicjalizacyjny
    encrypt_AES_CBC_file(filepath, cyphered_file_path, key, iv)
    encrypted_key = encrypt_with_public_key(key, public_key_pem)
    encrypted_iv = encrypt_with_public_key(iv, public_key_pem)
    with open(metadata_file_path, 'w') as metadata:
        metadata.write(encrypted_key.decode('utf-8'))
        metadata.write(encrypted_iv.decode('utf-8'))


def encrypt_AES_CBC_file(input_file, output_file, key, iv, chunk_size=8192):
    # Utwórz obiekt AES Cipher w trybie CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Włącz szyfrowanie
    encryptor = cipher.encryptor()

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break

            # Wykonaj dopełnianie (padding) dla tekstu
            padder = padding.PKCS7(128).padder()
            padded_chunk = padder.update(chunk) + padder.finalize()

            # Zaszyfruj blok danych
            encrypted_chunk = encryptor.update(padded_chunk) + encryptor.finalize()

            f_out.write(encrypted_chunk)


def decrypt_AES_CBC_file(input_file, output_file, key, iv, chunk_size=8192):
    # Utwórz obiekt AES Cipher w trybie CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    # Włącz deszyfrowanie
    decryptor = cipher.decryptor()

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break

            # Deszyfruj blok danych
            decrypted_chunk = decryptor.update(chunk) + decryptor.finalize()

            # Usuń dopełnienie (padding)
            unpadder = padding.PKCS7(128).unpadder()
            unpadded_chunk = unpadder.update(decrypted_chunk) + unpadder.finalize()

            f_out.write(unpadded_chunk)


def decypher_file(filepath, cyphered_file_path, metadata_file_path, password):
    private_key_pem, public_key_pem = create_asymmetric_key(password)
    encrypted_key = 0
    encrypted_iv = 0
    with open(metadata_file_path, 'r') as metadata:
        encrypted_key = metadata.readline().rstrip()
        encrypted_iv = metadata.readline().rstrip()
    key = decrypt_with_private_key(encrypted_key, private_key_pem)
    iv = decrypt_with_private_key(encrypted_iv, private_key_pem)
    decrypt_AES_CBC_file(filepath, cyphered_file_path, key, iv)
