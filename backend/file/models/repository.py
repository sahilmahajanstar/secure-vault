from .files import Files
from .file_metadata import FileMetadata
from .file_permission import FilePermission
from .file_share import FileShare
from .file_share_link import FileShareLink
from users.models.repository import Repository as UserRepository


class Repository:
    @property
    def files(self):
        return Files.objects.all()

    @property
    def file_metadata(self):
        return FileMetadata.objects.all()

    @property
    def file_permission(self):
        return FilePermission.objects.all()

    @property
    def file_share(self):
        return FileShare.objects.all()

    @property
    def user_repository(self):
        return UserRepository()

    @property
    def file_share_link(self):
        return FileShareLink.objects.all()
