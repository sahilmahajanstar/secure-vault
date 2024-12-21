from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from .users import Users
from .profile import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "role",
            "created_at",
            "updated_at",
            "email_verified",
        )
        read_only_fields = ("groups", "user_permissions")

        extra_kwargs = {
            "password": {"write_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "profile_avatar", "user_id", "user"]
        user = UserSerializer(many=False, read_only=True)
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name")


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("id", "name", "codename")
