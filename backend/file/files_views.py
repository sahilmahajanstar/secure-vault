# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .utils.file_handler import FileHandler
from common.error.validation_error import ValidationError, ValidationErrorCodes
from django.contrib.auth.models import AnonymousUser
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
from .utils.file_access import FileAccess
from rest_framework.decorators import action


class FilesViewSet(viewsets.ModelViewSet):
    repository = Repository()
    serializer_class = FileSerializer
    file_metadata_serializer_class = FileMetadataSerializer
    file_share_serializer_class = FileShareSerializer
    file_share_permissions_serializer_class = FilePermissionSerializer
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
            "retrieve": [isAuth, isEmailVerified],
            "retrieve_public": [allowAny],
        }
        return permission.get(self.action, [allowAny])

    def get_authenticators(self):
        print(self.request.resolver_match.route, flush=True)
        if (
            self.request.method == "GET"
            and "public" in self.request.resolver_match.route
        ):
            return []
        return super().get_authenticators()

    @ExceptionHandler.handle
    def create(self, request):
        # max 5 file for now
        files = request.data.get("files", [])
        files_list = []
        if len(files) == 0:
            return ValidationError(
                "No file provided",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
        for file in files:
            file_name = file.get("file_name")
            file_size = file.get("file_size")
            content_type = file.get("content_type")
            share_type = file.get("share_type")
            is_favorite = file.get("is_favorite")
            print(content_type, flush=True)

            file_model = self.repository.files.filter(
                name=file_name, user=request.user, is_deleted=0
            ).first()
            print(content_type, flush=True)

            file_handler = FileHandler(
                file_name, file_size, content_type, file.get("data"), request.user.id
            )
            file_handler.save_file()
            file_obj = None
            file_metadata = None
            type = content_type.split("/")[1]
            # Here, we are executing query one by one for simplicity to avoid complex logic
            # If we want to improve performance, we can use bulk create and bulk update
            if not file_model:
                file_obj = self.repository.files.create(
                    name=file_name,
                    size=file_size,
                    user=request.user,
                    file_url=file_handler.get_path(),
                    is_favorite=is_favorite,
                    share_type=share_type,
                    is_deleted=False,
                )
                file_metadata = self.repository.file_metadata.create(
                    file=file_obj,
                    type=type,
                    content_type=content_type,
                    size=file_size,
                    is_folder=False,
                )
            else:
                file_model.name = file_name
                file_model.size = file_size
                file_model.user = request.user
                file_model.file_url = file_handler.get_path()
                file_model.is_favorite = is_favorite
                file_model.share_type = share_type
                file_model.is_deleted = False
                file_model.save()
                file_obj = file_model
                file_metadata = self.repository.file_metadata.filter(
                    file=file_model
                ).get()
                file_metadata.type = type
                file_metadata.content_type = content_type
                file_metadata.size = file_size
                file_metadata.is_folder = False
                file_metadata.save()
            data = self.serializer_class(file_obj).data
            data["file_metadata"] = self.file_metadata_serializer_class(
                file_metadata
            ).data
            files_list.append(data)

        return Response({"data": {"files": files_list}}, status=status.HTTP_201_CREATED)

    def getFile(self, request, pk=None):
        file_id = pk
        query = request.query_params
        include_file = query.get("include_file")
        include_file_share = query.get("include_file_share", "false")
        if not file_id:
            raise ValidationError(
                "File ID is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
        file = self.repository.files.filter(id=file_id, is_deleted=False).get()
        if not file:
            raise ValidationError(
                "File not found",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )
        file_metadata = self.repository.file_metadata.filter(
            file_id=file.id, is_folder=False
        ).first()
        if not file_metadata:
            raise ValidationError(
                "File metadata not found",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )
        file_access = FileAccess(file, request.user, self.repository)
        if not file_access.check_file_access():
            raise ValidationError(
                "File is private",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_403_FORBIDDEN,
            )
        file_data = None
        user_file_share_info = None
        if include_file == "true":
            file_handler = FileHandler(
                file.name,
                file_metadata.size,
                file_metadata.content_type,
                file.file_url,
                file.user.id,
            )
            file_data = file_handler.read_file()
        if (
            include_file_share == "true"
            and request.user
            and not isinstance(request.user, AnonymousUser)
            and not request.user.is_admin()
        ):
            user_file_share_info = self.repository.file_share.filter(
                file_id=file.id, user_id=request.user.id, is_deleted=False
            ).first()
            if user_file_share_info:
                permissions = self.repository.file_permission.filter(
                    share_file_id=user_file_share_info.id, is_deleted=False
                ).all()
                user_file_share_info = self.file_share_serializer_class(
                    user_file_share_info
                ).data
                user_file_share_info[
                    "permissions"
                ] = self.file_share_permissions_serializer_class(
                    permissions, many=True
                ).data

        data = self.serializer_class(file).data
        data["file_metadata"] = self.file_metadata_serializer_class(file_metadata).data
        data["user_file_share_info"] = user_file_share_info
        return Response(
            {"data": {"file": data, "file_data": file_data}},
            status=status.HTTP_200_OK,
        )

    @ExceptionHandler.handle
    @action(detail=True, methods=["get"])
    def public(self, request, pk=None):
        return self.getFile(request, pk)

    @ExceptionHandler.handle
    def retrieve(self, request, pk=None):
        return self.getFile(request, pk)

    @ExceptionHandler.handle
    def list(self, request):
        query = request.query_params
        offset = int(query.get("offset", 0))
        limit = None
        if query.get("limit"):
            limit = int(query.get("limit"))
        where = {"is_deleted": False}
        # if not request.user.is_admin():
        where["user"] = request.user
        where["is_deleted"] = False
        files = self.repository.files.filter(**where).order_by("-created_at")
        total_count = files.count()
        if limit is not None:
            files = files[offset : offset + limit]
        files_list = []
        for file in files:
            file_metadata = self.repository.file_metadata.filter(file=file).first()
            data = self.serializer_class(file).data
            data["file_metadata"] = self.file_metadata_serializer_class(
                file_metadata
            ).data
            files_list.append(data)

        return Response(
            {
                "data": {
                    "total": total_count,
                    "offset": offset,
                    "limit": limit,
                    "files": files_list,
                }
            },
            status=status.HTTP_200_OK,
        )

    @ExceptionHandler.handle
    def destroy(self, request, pk=None):
        file_id = pk
        if not file_id:
            raise ValidationError(
                "File ID is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )

        # Get file object
        file = self.repository.files.filter(id=file_id, is_deleted=False).first()
        print(file, flush=True)
        if not file:
            raise ValidationError(
                "File not found",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )
        file_metada = self.repository.file_metadata.filter(file=file).first()
        if not file_metada:
            raise ValidationError(
                "File metadata not found",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_403_FORBIDDEN,
            )
        if not request.user.is_admin() and file.user.id != request.user.id:
            raise ValidationError(
                "Do not have permission to delete this file",
                ValidationErrorCodes.NOT_FOUND,
                status.HTTP_403_FORBIDDEN,
            )
        file_handler = FileHandler(
            file.name, file.size, file_metada.content_type, file.file_url, file.user.id
        )
        file.is_deleted = True
        file.save()
        file_handler.delete_file()
        data = self.serializer_class(file).data
        data["file_metadata"] = self.file_metadata_serializer_class(file_metada).data
        return Response({"data": {"file": data}}, status=status.HTTP_200_OK)
