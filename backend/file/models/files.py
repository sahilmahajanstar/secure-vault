import uuid
from django.db import models
from users.models.users import Users


class Files(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, db_column="user_id", related_name="files_user"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    file_url = models.CharField(max_length=500)
    share_type = models.CharField(
        max_length=50,
        choices=[("public", "Public"), ("private", "Private")],
        default="private",
    )
    # parent_id = models.UUIDField(null=True, blank=True)  do this in future to share or store files in folders

    class Meta:
        db_table = "files"
        verbose_name = "file"
        verbose_name_plural = "files"

    def __str__(self):
        return self.name
