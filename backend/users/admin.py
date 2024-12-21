from django.contrib import admin

# Register your models here.
from .models.users import Users
from .models.profile import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "profile_avatar", "created_at", "updated_at")
    list_filter = ("user",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("user", "profile_avatar")}),
        ("Important dates", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
        "email_verified",
        "role",
    )
    list_filter = ("username",)
    search_fields = ("username", "first_name", "last_name", "email")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("username", "password", "email_verified", "role")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Important dates", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "content_type", "codename")
    search_fields = ("name", "codename")
    ordering = ("content_type__app_label", "content_type__model", "codename")
    fieldsets = (
        (None, {"fields": ("content_type",)}),
        ("Code", {"fields": ("codename", "name")}),
    )
