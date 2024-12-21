import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from ..utils.middleware import IsAdminUser
from common.security.password_encrypt import PasswordEncryptFactory

password_encryptor = PasswordEncryptFactory(algorithm="fernet")


class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # phone_number = models.CharField(max_length=12, unique=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10, choices=[("user", "User"), ("admin", "Admin")], default="user"
    )

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    class Meta:
        db_table = "auth_user"  # Use default table name
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = password_encryptor.encrypt(raw_password)
        print(raw_password, flush=True)
        return self.password

    def check_password(self, raw_password):
        return password_encryptor.verify(raw_password, self.password)

    def is_admin(self):
        return self.role == "admin"
