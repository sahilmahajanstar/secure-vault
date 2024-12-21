from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import action

from .utils.middleware import IsAdminUser, IsEmailVerified

from .utils.user_validator import UserValidator
from common.error.validation_error import ValidationError, ValidationErrorCodes
from common.error.exception_handler import ExceptionHandler
from .models.repository import Repository
from common.security.password_encrypt import PasswordEncryptFactory
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models.serialize import ProfileSerializer, UserSerializer
from .utils.token_manager import TokenManager
from django.contrib.auth import login


class UserViewSet(viewsets.ModelViewSet):
    repository = Repository()
    serializer_class = UserSerializer
    profile_serializer_class = ProfileSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return self.repository.user

    def get_permissions(self):
        isAuth = IsAuthenticated()
        isAdmin = IsAdminUser()
        allowAny = AllowAny()
        isEmailVerified = IsEmailVerified()
        permission = {
            "create_user": [allowAny],
            "user_list": [isAuth, isAdmin, isEmailVerified],
            "user_by_id": [isAuth],
            "profile": [isAuth, isEmailVerified],
            "me": [isAuth],
        }
        return permission.get(self.action, [])

    def get_authenticators(self):
        print(self.request.resolver_match.route, flush=True)
        if (
            self.request.method == "POST"
            and self.request.resolver_match.route == "users/"
        ):
            return []
        return super().get_authenticators()

    @ExceptionHandler.handle
    @action(detail=False, methods=["post"])
    def create_user(self, request):
        data = request.data.copy()
        valdationError = UserValidator.validate(data)
        if len(valdationError.errors) > 0:
            raise valdationError
        user_repository = self.repository.user
        user = user_repository.filter(
            Q(username=data["username"]) | Q(email=data["email"])
        ).count()
        if user > 0:
            raise ValidationError(
                "User already exists with this username or email",
                ValidationErrorCodes.USER_ALREADY_EXISTS,
                status.HTTP_409_CONFLICT,
            )
        data["password"] = PasswordEncryptFactory().encrypt(data["password"])
        # data['phone_number'] = data['country_code'] + data['phone_number']
        # del data['country_code']
        user = user_repository.create(**data)
        tokenManager = TokenManager(request)
        token = tokenManager.sign_token(user)
        login(request, user)
        return Response(
            {"data": {"user": self.serializer_class(user).data, "token": token}},
            status=status.HTTP_201_CREATED,
        )

    @ExceptionHandler.handle
    def user_list(self, request, *args, **kwargs):
        query = request.query_params
        offset = int(query.get("offset", 0))
        limit = int(query.get("limit", 10))

        user_repository = self.repository.user
        total_count = user_repository.count()
        user_repository = user_repository[offset : offset + limit]
        serializer = self.serializer_class(user_repository, many=True)

        return Response(
            {
                "data": {
                    "total": total_count,
                    "offset": offset,
                    "limit": limit,
                    "users": serializer.data,
                }
            },
            status=status.HTTP_200_OK,
        )

    @ExceptionHandler.handle
    def user_by_id(self, request, *args, **kwargs):
        user = self.repository.user.filter(id=kwargs.get("pk")).first()
        # admin can access do later on
        token = request.headers.get("Authorization")
        if request.user.id != user.id:
            raise ValidationError(
                "You are not allowed to access this user",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_403_FORBIDDEN,
            )
        if not user:
            raise ValidationError(
                "User not found",
                ValidationErrorCodes.USER_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"data": {"user": self.serializer_class(user).data}},
            status=status.HTTP_200_OK,
        )

    @ExceptionHandler.handle
    @action(detail=False, methsods=["get"])
    def profile(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        if not user_id:
            raise ValidationError(
                "User id is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
        if user_id != request.user.id:
            raise ValidationError(
                "You are not allowed to access this profile",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_403_FORBIDDEN,
            )
        profile = self.repository.profile.filter(user_id=user_id).first()
        if not profile:
            raise ValidationError(
                "Profile not found",
                ValidationErrorCodes.PROFILE_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"data": {"profile": self.profile_serializer_class(profile).data}},
            status=status.HTTP_200_OK,
        )

    @ExceptionHandler.handle
    @action(detail=False, methods=["get"])
    def me(self, request, *args, **kwargs):
        user = request.user
        profile = self.repository.profile.filter(user_id=user.id).first()
        return Response(
            {
                "data": {
                    "user": self.serializer_class(user).data,
                    "profile": self.profile_serializer_class(profile).data,
                }
            },
            status=status.HTTP_200_OK,
        )
