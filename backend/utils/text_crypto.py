"""Cryptographic functions for the backend."""

import base64

from cryptography.fernet import Fernet


def encrypt_string(key: bytes, plaintext: str) -> str:
    """
    Encrypts a string using the given key and returns a Base64-encoded ciphertext.

    Parameters
    ----------
        key (bytes): The encryption key.
        plaintext (str): The string to be encrypted.

    Returns
    -------
        str: The Base64-encoded encrypted string.

    """
    cipher_suite = Fernet(key)
    ciphertext_bytes = cipher_suite.encrypt(plaintext.encode())
    ciphertext_base64 = base64.urlsafe_b64encode(ciphertext_bytes).decode()
    return ciphertext_base64


def decrypt_string(key: bytes, ciphertext_base64: str) -> str:
    """
    Decrypts a Base64-encoded string using the given key.

    Parameters
    ----------
        key (bytes): The encryption key.
        ciphertext_base64 (str): The Base64-encoded encrypted string.

    Returns
    -------
        str: The decrypted string.

    """
    ciphertext_bytes = base64.urlsafe_b64decode(ciphertext_base64.encode())
    cipher_suite = Fernet(key)
    plaintext = cipher_suite.decrypt(ciphertext_bytes).decode()
    return plaintext


def generate_encryption_key() -> str:
    """Generate an encryption key."""
    return Fernet.generate_key().decode()
