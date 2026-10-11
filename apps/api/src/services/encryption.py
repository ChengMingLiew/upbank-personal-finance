import nacl.secret
import nacl.utils
import base64
from src.config import settings

_key = bytes.fromhex(settings.ENCRYPTION_KEY)
_box = nacl.secret.SecretBox(_key)

def encrypt_token(plaintext: str) -> str:

    encrypted = _box.encrypt(plaintext.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_token(ciphertext_hex: str) -> str:

    encrypted = bytes.fromhex(ciphertext_hex)
    return _box.decrypt(encrypted).decode()