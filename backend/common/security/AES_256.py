from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64
from rest_framework import status
from common.error.tech_error import TechError, TechErrorCodes
from .base_encryption import BaseEncryption


class AES_256_GCM(BaseEncryption):
    def __init__(self, key):
        """Initialize with a secret key"""
        self.backend = default_backend()
        # Generate a salt for key derivation
        self.salt = os.urandom(16)
        # Derive a 32-byte key for AES-256
        self.key = self._derive_key(key.encode(), self.salt)

    def _derive_key(self, password, salt):
        """Derive a 32-byte key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 32 bytes for AES-256
            salt=salt,
            iterations=100000,
            backend=self.backend,
        )
        return kdf.derive(password)

    def encrypt(self, plaintext):
        """Encrypt data using AES-256-GCM"""
        try:
            # Generate a random IV (Initialization Vector)
            iv = os.urandom(16)

            # Create cipher
            cipher = Cipher(
                algorithms.AES(self.key), modes.GCM(iv), backend=self.backend
            )

            encryptor = cipher.encryptor()

            # Pad the plaintext
            padded_data = self._pad(plaintext.encode())

            # Encrypt the data
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

            auth_tag = encryptor.tag

            # Combine salt, IV, and ciphertext
            encrypted_data = self.salt + self.key + iv + auth_tag + ciphertext

            # Return base64 encoded string
            return encrypted_data

        except Exception as e:
            raise TechError(
                message="File encryption error",
                code=TechErrorCodes.FILE_ENCRYPTION_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def decrypt(self, encrypted_data):
        """Decrypt data using AES-256-GCM"""
        try:
            # Extract salt, IV, and ciphertext
            salt = encrypted_data[:16]
            key = encrypted_data[16:48]
            iv = encrypted_data[48:64]
            auth_tag = encrypted_data[64:80]
            ciphertext = encrypted_data[80:]

            # Create cipher
            cipher = Cipher(
                algorithms.AES(key), modes.GCM(iv, auth_tag), backend=self.backend
            )

            decryptor = cipher.decryptor()

            # Decrypt the data
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()

            # Remove padding
            plaintext = self._unpad(padded_data)
            return plaintext

        except Exception as e:
            raise TechError(
                message="File decryption error",
                code=TechErrorCodes.FILE_ENCRYPTION_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _pad(self, data):
        """PKCS7 padding"""
        block_size = algorithms.AES.block_size // 8
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def _unpad(self, padded_data):
        """Remove PKCS7 padding"""
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]
