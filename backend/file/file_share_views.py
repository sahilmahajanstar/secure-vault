# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.models.serialize import UserSerializer
from .utils.file_handler import FileHandler
from common.error.validation_error import ValidationError, ValidationErrorCodes

from .models.repository import Repository
from .models.files import Files
from common.error.exception_handler import ExceptionHandler
from .models.serialize import (
    FileMetadataSerializer,
    FilePermissionSerializer,
    FileSerializer,
    FileShareSerializer,
)
from rest_framework.permissions import AllowAny
from users.utils.middleware import IsEmailVerified
from rest_framework import viewsets
from django.db import transaction
from rest_framework.decorators import action
from django.db.models import Q


class FileShareViewSet(viewsets.ModelViewSet):
    repository = Repository()
    serializer_class = FileShareSerializer
    permission_serializer_class = FilePermissionSerializer
    user_serializer_class = UserSerializer
    file_serializer_class = FileSerializer
    file_metadata_serializer_class = FileMetadataSerializer
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return self.repository.files

    def get_permissions(self):
        isAuth = IsAuthenticated()
        isEmailVerified = IsEmailVerified()
        allowAny = AllowAny()
        permission = {
            "create": [isAuth, isEmailVerified],
            "list": [isAuth, isEmailVerified],
            "destroy": [isAuth, isEmailVerified],
            "update_permission": [isAuth, isEmailVerified],
            "search_user": [isAuth, isEmailVerified],
            "file_share_with_you": [isAuth, isEmailVerified],
        }
        return permission.get(self.action, [allowAny])

    @ExceptionHandler.handle
    def create(self, request):
        file_id = request.data.get("file_id")
        share_type = request.data.get("share_type")
        users = request.data.get("users", [])
        if not file_id:
            raise ValidationError(
                "File ID is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
        if share_type not in ["private", "public"]:
            raise ValidationError(
                "Invalid share type",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )

        file_share_list = []
        with transaction.atomic():
            file = (
                self.repository.files.select_for_update(nowait=False)
                .filter(id=file_id, user=request.user, is_deleted=False)
                .first()
            )
            if not file:
                raise ValidationError(
                    "File not found",
                    ValidationErrorCodes.NOT_FOUND,
                    status.HTTP_404_NOT_FOUND,
                )
            if not request.user.is_admin() and file.user_id != request.user.id:
                raise ValidationError(
                    "Do not have permission to share this file",
                    ValidationErrorCodes.INVALID_DATA,
                    status.HTTP_403_FORBIDDEN,
                )
            file.share_type = share_type
            file.save()
            for user_to_share in users:
                user = self.repository.user_repository.user.filter(
                    id=user_to_share.get("id")
                ).first()
                if not user:
                    raise ValidationError(
                        "User not found",
                        ValidationErrorCodes.NOT_FOUND,
                        status.HTTP_404_NOT_FOUND,
                    )
                file_share = self.repository.file_share.create(file=file, user=user)
                permission_list = []
                for permission in user_to_share.get("permissions", []):
                    # in future extract available permission from permission main table
                    if permission.get("name") not in ["view", "download"]:
                        raise ValidationError(
                            "Invalid permission",
                            ValidationErrorCodes.INVALID_DATA,
                            status.HTTP_400_BAD_REQUEST,
                        )
                    list = self.repository.file_permission.create(
                        share_file=file_share, name=permission.get("name")
                    )
                    permission_list.append(list)
                data = self.serializer_class(file_share).data
                data["permissions"] = self.permission_serializer_class(
                    permission_list, many=True
                ).data
                file_share_list.append(
                    {"file_share": data, "user": self.user_serializer_class(user).data}
                )

        print(file_share_list, flush=True)
        return Response(
            {
                "data": {
                    "file": self.file_serializer_class(file).data,
                    "file_shares": file_share_list,
                }
            },
            status=status.HTTP_200_OK,
        )

    @ExceptionHandler.handle
    def list(self, request):
        query = request.query_params
        file_id = query.get("file_id", None)
        offset = int(query.get("offset", 0))
        limit = int(query.get("limit", 0))  # diable for now
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
        if not request.user.is_admin() and file.user_id != request.user.id:
            raise ValidationError(
                "Not allowed to access",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_403_FORBIDDEN,
            )
        print(file, flush=True)
        file_shares = (
            self.repository.file_share.select_related("user")
            .filter(file=file, is_deleted=False, user__is_active=True)
            .order_by("-created_at")
        )
        print(file_shares.query, flush=True)
        total_count = file_shares.count()
        if limit > 0:
            file_shares = file_shares[offset : offset + limit]
        file_share_list = []
        for file_share in file_shares:
            permissions = self.repository.file_permission.filter(
                share_file=file_share, is_deleted=False
            ).all()
            user = self.repository.user_repository.user.filter(
                id=file_share.user_id, is_active=True
            ).first()
            data = self.serializer_class(file_share).data
            data["permissions"] = self.permission_serializer_class(
                permissions, many=True
            ).data
            file_share_list.append(
                {"file_share": data, "user": self.user_serializer_class(user).data}
            )

        return Response(
            {
                "data": {
                    "total": total_count,
                    "offset": offset,
                    "limit": limit,
                    "file_shares": file_share_list,
                }
            },
            status=status.HTTP_200_OK,
        )

    @ExceptionHandler.handle
    def destroy(self, request, pk=None):
        file_share_id = pk
        if not file_share_id:
            raise ValidationError(
                "File share ID is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
        file_share = self.repository.file_share.filter(
            id=file_share_id, is_deleted=False
        ).first()
        if not file_share:
            raise ValidationError(
                "File share not found",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )
        file = self.repository.files.filter(
            id=file_share.file_id, is_deleted=False
        ).first()
        if not file:
            raise ValidationError(
                "File not found",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )
        if not request.user.is_admin() and file.user.id != request.user.id:
            raise ValidationError(
                "Do not have permission to delete share file",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_403_FORBIDDEN,
            )
        file_share.is_deleted = True
        file_share.save()
        return Response(
            {"data": {"file_share": self.serializer_class(file_share).data}},
            status=status.HTTP_200_OK,
        )

    @ExceptionHandler.handle
    @action(detail=True, methods=["post"])
    def update_permission(self, request, pk=None):
        file_share_id = pk
        permissions = request.data.get("permission", [])
        if len(permissions) == 0:
            raise ValidationError(
                "Permission is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
        if not file_share_id:
            raise ValidationError(
                "File share ID is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
        data = None
        with transaction.atomic():
            file_share = self.repository.file_share.filter(
                id=file_share_id, user=request.user, is_deleted=False
            ).first()
            if not file_share:
                raise ValidationError(
                    "File share not found",
                    ValidationErrorCodes.NOT_FOUND,
                    status.HTTP_404_NOT_FOUND,
                )
            file = self.repository.files.filter(
                id=file_share.file_id, is_deleted=False
            ).first()
            if not file:
                raise ValidationError(
                    "File not found",
                    ValidationErrorCodes.NOT_FOUND,
                    status.HTTP_404_NOT_FOUND,
                )
            if not request.user.is_admin() and file.user.id != request.user.id:
                raise ValidationError(
                    "Do not have permission to update permission",
                    ValidationErrorCodes.NOT_FOUND,
                    status.HTTP_403_FORBIDDEN,
                )
            permission_list = []
            for permission in permissions:
                if permission.name not in ["view", "download"]:
                    raise ValidationError(
                        "Invalid permission",
                        ValidationErrorCodes.INVALID_DATA,
                        status.HTTP_400_BAD_REQUEST,
                    )
                if permission.type == "add":
                    permission_obj = self.repository.file_permission.create(
                        share_file=file_share, name=permission.name
                    )
                    permission_list.append(permission_obj)
                elif permission.type == "update":
                    permission_obj = self.repository.file_permission.filter(
                        share_file=file_share, name=permission.name, is_deleted=False
                    ).first()
                    if not permission_obj:
                        raise ValidationError(
                            "Permission not found",
                            ValidationErrorCodes.NOT_FOUND,
                            status.HTTP_404_NOT_FOUND,
                        )
                    permission_obj.is_deleted = permission.is_deleted
                    permission_obj.name = permission.name
                    permission_obj.save()
                    if not permission.is_deleted:
                        permission_list.append(permission_obj)
            data = self.serializer_class(file_share).data
            data["permissions"] = self.permission_serializer_class(
                permission_list, many=True
            ).data
        return Response(
            {
                "data": {
                    "file_share": data,
                    "user": self.user_serializer_class(file_share.user).data,
                }
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    @ExceptionHandler.handle
    def search_user(self, request):
        email = request.query_params.get("email", "")
        file_id = request.query_params.get("file_id", "")
        if not email:
            raise ValidationError(
                "Email is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
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
        if not request.user.is_admin() and file.user_id != request.user.id:
            raise ValidationError(
                "Do not have permission to search user",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_403_FORBIDDEN,
            )
        user = self.repository.user_repository.user.raw(
            """
            SELECT * FROM auth_user WHERE auth_user.email LIKE %s AND auth_user.is_active = TRUE AND auth_user.id != %s 
            AND auth_user.id NOT IN (SELECT user_id FROM file_share WHERE is_deleted = FALSE AND file_id = %s) LIMIT 5
        """,
            [
                "%" + email + "%",
                str(request.user.id).replace("-", ""),
                str(file_id).replace("-", ""),
            ],
        )
        users = []
        print(user.query, flush=True)
        for u in user:
            users.append(
                {
                    "id": u.id,
                    "email": u.email,
                    "first_name": u.first_name,
                    "last_name": u.last_name,
                }
            )
        return Response({"data": {"users": users}}, status=status.HTTP_200_OK)

    @ExceptionHandler.handle
    @action(detail=False, methods=["get"])
    def file_share_with_you(self, request):
        current_user = request.user
        offset = int(request.query_params.get("offset", 0))
        limit = int(request.query_params.get("limit", 0))
        # add pagination later
        files = []
        user_query = ""
        if not current_user.is_admin():
            user_query = "AND files.id  IN (SELECT file_id FROM file_share WHERE user_id = '{}' AND is_deleted = FALSE)".format(
                str(current_user.id).replace("-", "")
            )
        files = self.repository.files.raw(
            """
            SELECT *, count(*) over() as row_number FROM files WHERE files.is_deleted = FALSE {user_query} limit {limit} offset {offset}
        """.format(
                user_query=user_query, limit=limit, offset=offset
            )
        )
        file_share_list = []
        total = 0
        for file in files:
            total = file.row_number
            data = self.file_serializer_class(file).data
            user = self.repository.user_repository.user.filter(id=file.user_id).first()
            file_metadata = self.repository.file_metadata.filter(
                file_id=file.id
            ).first()
            data["file_metadata"] = self.file_metadata_serializer_class(
                file_metadata
            ).data
            data["user"] = self.user_serializer_class(user).data
            if not current_user.is_admin():
                file_share = self.repository.file_share.filter(
                    file_id=file.id, user_id=current_user.id, is_deleted=False
                )
                file_share = file_share.first()
                data["user_file_share_info"] = self.serializer_class(file_share).data
                data["user_file_share_info"][
                    "permissions"
                ] = self.permission_serializer_class(
                    self.repository.file_permission.filter(
                        share_file=file_share, is_deleted=False
                    ).all(),
                    many=True,
                ).data
            file_share_list.append(data)
        return Response(
            {
                "data": {
                    "files": file_share_list,
                    "total": total,
                    "offset": offset,
                    "limit": limit,
                }
            },
            status=status.HTTP_200_OK,
        )
