from common.error.authentication_error import (
    AuthenticationError,
    AuthenticationErrorCodes,
)
from rest_framework import status
from .token_manager import TokenManager
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import BasePermission


class Authentication(JWTAuthentication):
    def authenticate(self, request):
        token_manager = TokenManager(request)
        if not token_manager.get_token() or not token_manager.is_token_valid():
            validation_error = AuthenticationError(
                "Invalid credentials",
                AuthenticationErrorCodes.INVALID_CREDENTIALS,
                status.HTTP_401_UNAUTHORIZED,
            )
            raise validation_error
        token = token_manager.validate_token()
        return self.get_user(token), token


class IsEmailVerified(BasePermission):
    def has_permission(self, request, view):
        return request.user.email_verified


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"
