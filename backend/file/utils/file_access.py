from file.models.files import Files
from users.models.users import Users
from file.models.repository import Repository
from django.contrib.auth.models import AnonymousUser


class FileAccess:
    def __init__(self, file: Files, user: Users, repository: Repository):
        self.file = file
        self.user = user
        self.repository = repository

    def check_file_access(self):
        if self.file.share_type == "public":
            return True
        # for private file check if user has access to the file
        return self.check_file_share()

    def check_file_share(self):
        if isinstance(self.user, AnonymousUser):
            return False
        if self.user.is_admin():
            # admin has access to the file
            return True
        if self.file.user_id == self.user.id:
            # owner has access to the file
            return True
        # check if user has access to the file
        return self.repository.file_share.filter(
            file=self.file, user=self.user, is_deleted=False
        ).exists()
