import base64

import nacl.secret
import nacl.utils

from src.config import settings

_key = bytes.fromhex(settings.ENCRYPTION_KEY)
_box = nacl.secret.SecretBox(_key)

def encrypt_token(plaintext: str) -> str:

    encrypted = _box.encrypt(plaintext.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_token(ciphertext_b64: str) -> str:

    encrypted = base64.b64decode(ciphertext_b64)
    return _box.decrypt(encrypted).decode()