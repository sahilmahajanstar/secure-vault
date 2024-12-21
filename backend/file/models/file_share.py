import uuid
from django.db import models
from .files import Files
from users.models.users import Users


class FileShare(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(Files, on_delete=models.CASCADE, related_name="share_file")
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="share_file_user"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "file_share"
        verbose_name = "file_share"
        verbose_name_plural = "file_shares"

    def __str__(self):
        return str(self.id)
