from rest_framework import viewsets, status
from rest_framework.response import Response
from .utils.middleware import IsAdminUser, IsEmailVerified
from common.validation.file_validator import FileValidator
from common.error.validation_error import ValidationError, ValidationErrorCodes
from common.error.exception_handler import ExceptionHandler
from rest_framework.permissions import IsAuthenticated
from .models.repository import Repository

from .models.serialize import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    repository = Repository()
    serializer_class = ProfileSerializer
    http_method_names = ["get", "post"]

    def get_permissions(self):
        isAuth = IsAuthenticated()
        isAdmin = IsAdminUser()
        isEmailVerified = IsEmailVerified()
        permission = {
            "create": [isAuth, isEmailVerified],
            "retrieve": [isAuth, isEmailVerified],
            "list": [isAuth, isAdmin, isEmailVerified],
        }
        return permission.get(self.action, [])

    def get_queryset(self):
        return self.repository.profile

    @ExceptionHandler.handle
    def create(self, request):
        user_id = request.data.get("user_id")
        if str(request.user.id) != user_id:
            raise ValidationError(
                "You are not allowed to create profile for this user",
                ValidationErrorCodes.USER_NOT_FOUND,
                status.HTTP_403_FORBIDDEN,
            )
        user = self.repository.user.filter(id=user_id).first()
        if not user:
            raise ValidationError(
                "User not found",
                ValidationErrorCodes.USER_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )
        profile = self.repository.profile.filter(user_id=user.id).first()
        if profile:
            raise ValidationError(
                "Profile already exists",
                ValidationErrorCodes.PROFILE_ALREADY_EXISTS,
                status.HTTP_409_CONFLICT,
            )
        file_validator = FileValidator(max_size_mb=1)
        file_validator.validate(request.data.get("profile_avatar"))
        profile = self.repository.profile.create(
            user=user, profile_avatar=request.data.get("profile_avatar")
        )
        return Response(
            {"data": {"profile": self.serializer_class(profile).data}},
            status=status.HTTP_201_CREATED,
        )

    @ExceptionHandler.handle
    def retrieve(self, request, *args, **kwargs):
        profile = self.repository.profile.filter(id=kwargs.get("pk")).first()
        if not profile:
            raise ValidationError(
                "Profile not found",
                ValidationErrorCodes.PROFILE_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )
        if request.user.id != profile.user.id:
            raise ValidationError(
                "You are not allowed to access this profile",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_403_FORBIDDEN,
            )
        return Response(
            {"data": {"profile": self.serializer_class(profile).data}},
            status=status.HTTP_200_OK,
        )

    @ExceptionHandler.handle
    def list(self, request, *args, **kwargs):
        query = request.query_params
        offset = int(query.get("offset", 0))
        limit = int(query.get("limit", 10))

        profile_repository = self.repository.profile
        total_count = profile_repository.count()
        profile_repository = profile_repository[offset : offset + limit]
        serializer = self.serializer_class(profile_repository, many=True)

        return Response(
            {
                "data": {
                    "total": total_count,
                    "offset": offset,
                    "limit": limit,
                    "profiles": serializer.data,
                }
            },
            status=status.HTTP_200_OK,
        )
