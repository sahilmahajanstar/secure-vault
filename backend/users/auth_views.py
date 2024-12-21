from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .utils.otp_verify import OTPVerify

from .utils.user_validator import UserValidator
from common.error.authentication_error import (
    AuthenticationError,
    AuthenticationErrorCodes,
)
from users.utils.token_manager import TokenManager

from .models.repository import Repository
from common.error.validation_error import ValidationError, ValidationErrorCodes
from common.error.exception_handler import ExceptionHandler
from common.security.password_encrypt import PasswordEncryptFactory
from .models.serialize import UserSerializer

from django.contrib.auth import login, logout as django_logout


class AuthViewSet(viewsets.ViewSet):
    repository = Repository()
    serializer_class = UserSerializer

    def get_permissions(self):
        isAuth = IsAuthenticated()
        allowAny = AllowAny()
        permission = {
            "login": [allowAny],
            "logout": [isAuth],
            "refresh": [allowAny],
            "reset_password": [allowAny],
        }
        return permission.get(self.action, [])

    @ExceptionHandler.handle
    @action(detail=False, methods=["post"], authentication_classes=[])
    def login(self, request):
        # TODO:apply rate limit in future to avoid security issue
        # TODOsend email to user if login failed more than 3 times
        data = request.data
        username = data.get("username")
        password = data.get("password")
        otp = data.get("otp")
        if not username or not password:
            raise ValidationError(
                "Username and password are required",
                ValidationErrorCodes.INVALID_CREDENTIALS,
                status.HTTP_400_BAD_REQUEST,
            )

        user = self.repository.user.filter(username=username).first()
        password_encryptor = PasswordEncryptFactory()
        if not user or not password_encryptor.verify(password, user.password):
            raise AuthenticationError(
                "Invalid credentials",
                AuthenticationErrorCodes.INVALID_CREDENTIALS,
                status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            raise ValidationError(
                "Account is inactive",
                ValidationErrorCodes.USER_NOT_FOUND,
                status.HTTP_403_FORBIDDEN,
            )
        otp_verify = OTPVerify(user.email, otp, "login_verification")
        otp_verify.verify_email_otp(otp)
        token_manager = TokenManager(request)
        token = token_manager.sign_token(user)
        login(request, user)
        return Response(
            {"data": {"user": self.serializer_class(user).data, "token": token}},
            status=status.HTTP_200_OK,
        )

    @ExceptionHandler.handle
    @action(detail=False, methods=["post"])
    def logout(self, request):
        token_manager = TokenManager(request)
        django_logout(request)
        token_manager.revoke_token()
        return Response(
            {"data": {"message": "Logout successful"}}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"], authentication_classes=[])
    @ExceptionHandler.handle
    def refresh(self, request):
        """
        Refresh access token using refresh token
        """
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            raise ValidationError(
                "Refresh token is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
        token_manager = TokenManager(request)
        token = token_manager.refresh_token(refresh_token)
        payload = token_manager.verify_token(token["access"])
        user = self.repository.user.filter(id=payload["user_id"]).first()
        data = {"user": self.serializer_class(user).data, "token": token}
        return Response({"data": data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], authentication_classes=[])
    @ExceptionHandler.handle
    def reset_password(self, request):
        """
        Reset user password using email
        """
        email = request.data.get("email")
        new_password = request.data.get("new_password")
        otp = request.data.get("otp")
        # apply rate limit in future to avoid security issue
        if not email:
            raise ValidationError(
                "Email is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
        if not new_password:
            raise ValidationError(
                "New password is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
        user = self.repository.user.filter(email=email).first()
        if not user:
            raise ValidationError(
                "User not found",
                ValidationErrorCodes.USER_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )

        user_validator = UserValidator()
        password_validation = user_validator.validate_password(new_password)
        if (
            not password_validation.get("valid")
            or password_validation.get("strength") == "weak"
        ):
            raise ValidationError(
                "Password is weak",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
        otp_verify = OTPVerify(email, otp, "password_reset")
        otp_verify.verify_email_otp(otp)
        password_encryptor = PasswordEncryptFactory()
        encrypted_password = password_encryptor.encrypt(new_password)
        if password_encryptor.verify(new_password, user.password):
            raise ValidationError(
                "New password cannot be the same as the old password",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
        token_manager = TokenManager(request)
        token_manager.revoke_all_tokens(user)
        self.repository.user.filter(id=user.id).update(password=encrypted_password)
        return Response(
            {"data": {"message": "Password reset successful"}},
            status=status.HTTP_200_OK,
        )
