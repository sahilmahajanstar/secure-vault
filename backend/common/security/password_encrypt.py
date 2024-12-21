# use fernet default for password encryption and decryption which is AES-128
# reason: fernet is a symmetric encryption algorithm that is easy to use and secure and we can change encryption strategy
# later by decrypt and encrypt in new strategy

from decouple import config

from .fernet import FernetEncryption
from .AES_256 import AES_256_GCM


class PasswordEncryptFactory:
    def __init__(self, algorithm="fernet"):
        """Initialize Fernet encryption with an optional key"""
        self.key = config("PASSWORD_ENCRYPT_KEY")
        self._salt = config("PASSWORD_ENCRYPT_SALT")
        self.algorithm = algorithm
        self._client = self.encryption_client()

    def salt(self):
        return self._salt

    def encryption_client(self):
        if self.algorithm == "fernet":
            return FernetEncryption(self.key)
        elif self.algorithm == "AES_256_GCM":
            return AES_256_GCM(self.key)
        return None

    def encrypt(self, data: str):
        """
        Encrypt the input string data
        Args:
            data: String to encrypt
        Returns:
            Encrypted hex
        """
        if not isinstance(data, str):
            raise ValueError("Data must be a string")
        return self._client.encrypt(data)

    def encode(self, data: str, salt: str) -> str:
        return self._client.encrypt(data)

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt the encrypted bytes
        Args:
            encrypted_data: Encrypted bytes to decrypt
        Returns:
            Decrypted string
        """
        return self._client.decrypt(encrypted_data)

    def verify(self, password: str, encrypted_password: str) -> bool:
        return self.decrypt(encrypted_password) == password
