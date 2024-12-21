from django.contrib import admin


# Register your models here.
from .models.files import Files
from .models.file_share_link import FileShareLink
from .models.file_share import FileShare
from .models.file_permission import FilePermission
from .models.file_metadata import FileMetadata


@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user_id",
        "size",
        "created_at",
        "is_deleted",
        "is_favorite",
        "file_url",
    )
    list_filter = ("is_deleted", "is_favorite")
    search_fields = ("name",)
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(FileShare)
class FileShareAdmin(admin.ModelAdmin):
    list_display = ("file", "user", "created_at")
    search_fields = ("file__name", "user__username")
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(FilePermission)
class FilePermissionAdmin(admin.ModelAdmin):
    list_display = ("share_file", "name", "created_at")
    list_filter = ("name",)
    search_fields = ("share_file__file__name",)
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(FileMetadata)
class FileMetadataAdmin(admin.ModelAdmin):
    list_display = ("file", "type", "is_folder", "content_type", "size")
    list_filter = ("type", "is_folder")
    search_fields = ("file__name", "content_type")
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(FileShareLink)
class FileShareLinkAdmin(admin.ModelAdmin):
    list_display = (
        "file",
        "user",
        "created_at",
        "expires_at",
        "is_deleted",
        "updated_at",
    )
    search_fields = ("file__name", "user__username")
    readonly_fields = ("id", "created_at", "updated_at")
