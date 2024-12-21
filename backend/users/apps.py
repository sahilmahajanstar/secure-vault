from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    # Optional configurations:
    # verbose_name = 'User Management'
    # label = 'user_app'
