from cryptography.fernet import Fernet
from .base_encryption import BaseEncryption


class FernetEncryption(BaseEncryption):
    def __init__(self, key: str):
        self.set_key(key)
        self.fernet = Fernet(self.key)

    def set_key(self, key: str):
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        self.key = key

    def encrypt(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        return self.fernet.decrypt(encrypted_data.encode()).decode()
