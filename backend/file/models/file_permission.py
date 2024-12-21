import uuid
from django.db import models
from users.models.users import Users
from .file_share import FileShare


class FilePermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    share_file = models.ForeignKey(
        FileShare,
        on_delete=models.CASCADE,
        related_name="share_file_id",
        db_column="file_share_id",
    )
    name = models.CharField(
        max_length=255, choices=[("view", "View"), ("download", "Download")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "file_permissions"
        verbose_name = "file_permission"
        verbose_name_plural = "file_permissions"

    def __str__(self):
        return self.name
