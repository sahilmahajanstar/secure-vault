import uuid
from django.db import models
from .files import Files
from users.models.users import Users


class FileShareLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(
        Files, on_delete=models.CASCADE, related_name="share_file_link"
    )
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="share_file_link_user"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "file_share_link"
        verbose_name = "file_share_link"
        verbose_name_plural = "file_share_links"

    def __str__(self):
        return str(self.id)
