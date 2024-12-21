from rest_framework import serializers

from .file_share_link import FileShareLink
from .files import Files
from .file_metadata import FileMetadata
from .file_permission import FilePermission
from .file_share import FileShare


class FileMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMetadata
        fields = [
            "id",
            "type",
            "is_folder",
            "content_type",
            "created_at",
            "updated_at",
            "size",
            "file_id",
        ]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class FilePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilePermission
        fields = ["id", "share_file_id", "name", "created_at", "updated_at"]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class FileShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileShare
        fields = [
            "id",
            "file",
            "is_deleted",
            "created_at",
            "updated_at",
            "file_id",
            "user_id",
        ]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = [
            "id",
            "name",
            "size",
            "user_id",
            "file_url",
            "is_favorite",
            "share_type",
            "is_deleted",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "file_url": {"write_only": True},
        }


class FileShareLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileShareLink
        fields = ["id", "file_id", "user_id", "expires_at", "created_at", "updated_at"]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }
