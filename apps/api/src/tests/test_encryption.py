import base64

import pytest
from nacl.exceptions import CryptoError

from src.services.encryption import decrypt_token, encrypt_token

TOKEN = "up:yeah:test-token-1234567890"


def test_round_trip():
    assert decrypt_token(encrypt_token(TOKEN)) == TOKEN


def test_ciphertext_is_text_and_hides_plaintext():
    ct = encrypt_token(TOKEN)
    assert isinstance(ct, str)
    assert TOKEN not in ct
    assert "up:yeah" not in ct


def test_same_input_gives_different_ciphertext():
    assert encrypt_token(TOKEN) != encrypt_token(TOKEN)


def test_tampered_ciphertext_is_rejected():
    raw = bytearray(base64.b64decode(encrypt_token(TOKEN)))
    raw[-1] ^= 1
    with pytest.raises(CryptoError):
        decrypt_token(base64.b64encode(bytes(raw)).decode())


def test_garbage_is_rejected():
    with pytest.raises(Exception):
        decrypt_token("not-valid-ciphertext")