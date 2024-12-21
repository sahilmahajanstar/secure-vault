import uuid
from django.db import models


from .users import Users


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    profile_avatar = models.ImageField(
        upload_to="profile_avatar", null=True, blank=True
    )
    user = models.OneToOneField(
        Users, on_delete=models.CASCADE, related_name="profile_user", unique=True
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        db_table = "profile"
