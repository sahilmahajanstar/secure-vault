from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from datetime import datetime, timedelta

from .models.serialize import FileShareLinkSerializer
from common.error.exception_handler import ExceptionHandler
from common.error.validation_error import ValidationError, ValidationErrorCodes
from users.utils.middleware import IsEmailVerified
from .models.repository import Repository
import re


class FileShareLinkViewSet(viewsets.ViewSet):
    serializer_class = FileShareLinkSerializer
    repository = Repository()
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return self.repository.file_share_link

    def get_permissions(self):
        isAuth = IsAuthenticated()
        isEmailVerified = IsEmailVerified()
        allowAny = AllowAny()
        permission = {
            "create": [isAuth, isEmailVerified],
            "list": [isAuth, isEmailVerified],
            "destroy": [isAuth, isEmailVerified],
            "retrieve": [allowAny],
        }
        return permission.get(self.action, [allowAny])

    def get_authenticators(self):
        print("files/share/link/" in self.request.resolver_match.route, flush=True)
        if (
            self.request.method == "GET"
            and "files/share/link/" in self.request.resolver_match.route
        ):
            return []
        return super().get_authenticators()

    @ExceptionHandler.handle
    def create(self, request):
        file_id = request.data.get("file_id")
        expires_in_hours = request.data.get("expires_in_hours")

        if not file_id:
            raise ValidationError(
                "File ID is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )

        file = self.repository.files.filter(
            id=file_id, user=request.user, is_deleted=False
        ).first()
        if not file:
            raise ValidationError(
                "File not found",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )

        if not request.user.is_admin() and file.user.id != request.user.id:
            raise ValidationError(
                "Do not have permission to share this file",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_403_FORBIDDEN,
            )

        expires_at = None
        if expires_in_hours:
            expires_at = datetime.now() + timedelta(hours=expires_in_hours)

        file_share_link = self.repository.file_share_link.create(
            file=file, user_id=file.user.id, expires_at=expires_at
        )

        data = self.serializer_class(file_share_link).data

        return Response({"data": {"file_share_link": data}}, status=status.HTTP_200_OK)

    @ExceptionHandler.handle
    def list(self, request, pk=None):
        query = request.query_params
        file_id = pk
        offset = int(query.get("offset", 0))
        limit = int(query.get("limit", 10))

        if not file_id:
            raise ValidationError(
                "File ID is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )

        file = self.repository.files.filter(id=file_id, is_deleted=False).first()

        if not file:
            raise ValidationError(
                "File not found",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )

        if not request.user.is_admin() and file.user.id != request.user.id:
            raise ValidationError(
                "Do not have permission to share this file",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_403_FORBIDDEN,
            )

        share_links = self.repository.file_share_link.filter(
            file=file, is_deleted=False
        ).order_by("-created_at")

        total_count = share_links.count()
        share_links = share_links[offset : offset + limit]

        data = self.serializer_class(share_links, many=True).data

        return Response(
            {
                "data": {
                    "total": total_count,
                    "offset": offset,
                    "limit": limit,
                    "share_links": data,
                }
            },
            status=status.HTTP_200_OK,
        )

    @ExceptionHandler.handle
    def destroy(self, request, pk=None):
        if not pk:
            raise ValidationError(
                "Share link ID is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )

        share_link = self.repository.file_share_link.filter(
            id=pk, is_deleted=False
        ).first()
        if not share_link:
            raise ValidationError(
                "Share link not found",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )

        file = self.repository.files.filter(
            id=share_link.file_id, is_deleted=False
        ).first()
        if not file:
            raise ValidationError(
                "File not found",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )

        if not request.user.is_admin() and file.user.id != request.user.id:
            raise ValidationError(
                "Do not have permission to delete",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_403_FORBIDDEN,
            )

        share_link.is_deleted = True
        share_link.save()

        return Response(
            {"data": {"share_link": self.serializer_class(share_link).data}},
            status=status.HTTP_204_NO_CONTENT,
        )

    @ExceptionHandler.handle
    def retrieve(self, request, pk=None):
        if not pk:
            raise ValidationError(
                "Share link ID is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )

        share_link = self.repository.file_share_link.filter(
            id=pk, is_deleted=False
        ).first()
        if not share_link:
            raise ValidationError(
                "Share link not found",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )

        file = self.repository.files.filter(
            id=share_link.file_id, is_deleted=False
        ).first()
        if not file:
            raise ValidationError(
                "File not found",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )
        if share_link.expires_at and share_link.expires_at < datetime.now(
            share_link.expires_at.tzinfo
        ):
            raise ValidationError(
                "Share link expired",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"data": {"share_link": self.serializer_class(share_link).data}},
            status=status.HTTP_200_OK,
        )
