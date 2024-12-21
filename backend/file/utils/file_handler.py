import os
from common.security.password_encrypt import PasswordEncryptFactory


class FileHandler:
    password_encryptor = PasswordEncryptFactory("AES_256_GCM")

    def __init__(
        self, file_name: str, file_size: int, content_type: str, data: str, user_id: int
    ):
        self.file_name = file_name
        self.file_size = file_size
        self.content_type = content_type
        self.data = data
        self.user_id = user_id

    def get_path(self):
        return os.path.join("uploads", str(self.user_id), self.file_name) + ".vault"

    def save_file(self):
        file_path = self.get_path()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            data = self.password_encryptor.encrypt(self.data)
            file.write(data)

    def read_file(self):
        file_path = self.get_path()
        with open(file_path, "rb") as file:
            data = file.read()
        return self.password_encryptor.decrypt(data)

    def delete_file(self):
        file_path = self.get_path()
        os.remove(file_path)
