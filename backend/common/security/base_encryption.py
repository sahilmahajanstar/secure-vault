class BaseEncryption:
    def __init__(self, key: str):
        self.key = key

    def encrypt(self, data: str) -> str:
        raise NotImplementedError("Subclasses must implement encrypt method")

    def decrypt(self, encrypted_data: str) -> str:
        raise NotImplementedError("Subclasses must implement decrypt method")
