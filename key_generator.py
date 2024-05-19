import hashlib
from ecdsa import SigningKey, SECP256k1


def create_asymetric_key(password: str):
    hashed_password = hashlib.sha256(password.encode()).digest()
    sk = SigningKey.from_string(hashed_password[:32], curve=SECP256k1)
    vk = sk.verifying_key
    return sk, vk
