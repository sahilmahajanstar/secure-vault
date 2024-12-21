import uuid
from django.db import models
from .files import Files


class FileMetadata(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.OneToOneField(
        Files, on_delete=models.CASCADE, related_name="file_metadata", unique=True
    )
    type = models.CharField(max_length=1000)
    is_folder = models.BooleanField(default=False)
    content_type = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    size = models.IntegerField()

    class Meta:
        db_table = "file_metadata"
        verbose_name = "file_metadata"
        verbose_name_plural = "file_metadata"

    def __str__(self):
        return self.file.name
