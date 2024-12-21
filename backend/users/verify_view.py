# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_otp.plugins.otp_email.models import EmailDevice

from .utils.otp_verify import OTPVerify
from vault import settings
from common.error.validation_error import ValidationError, ValidationErrorCodes

from .models.repository import Repository
from common.error.exception_handler import ExceptionHandler
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q


class VerifyViewSet(viewsets.ViewSet):
    repository = Repository()

    def get_permissions(self):
        isAuth = IsAuthenticated()
        allowAny = AllowAny()
        permission = {"email": [allowAny], "verify_otp": [isAuth]}
        return permission.get(self.action, [])

    @action(detail=False, methods=["post"], authentication_classes=[])
    @ExceptionHandler.handle
    def email(self, request):
        # we can apply rate limit here in future
        email = request.data.get("email")
        type = request.data.get("type")
        username = request.data.get("username")
        if not email and not username:
            raise ValidationError(
                "Email or username is required",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )
        user = self.repository.user.filter(
            Q(email=email) | Q(username=username)
        ).first()
        if not user:
            raise ValidationError(
                "User not found",
                ValidationErrorCodes.USER_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )
        try:
            email_device, created = self.repository.email_device.get_or_create(
                user=user, email=user.email, confirmed=False, name=type
            )
            generate_allowed, _ = email_device.generate_is_allowed()
            if not generate_allowed:
                raise ValidationError(
                    "Email verification cooldown period has not expired yet. Next generation allowed within 1 minute",
                    ValidationErrorCodes.INVALID_DATA,
                    status.HTTP_400_BAD_REQUEST,
                )

            message = email_device.generate_challenge()
            return Response(
                {
                    "data": {
                        "message": "Verification email sent successfully",
                        "details": message,
                    }
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            raise ValidationError(
                str(e), ValidationErrorCodes.INVALID_DATA, status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post"])
    @ExceptionHandler.handle
    def validate_email(self, request):
        # we can apply rate limit here in future
        email = request.data.get("email")
        otp = request.data.get("otp")
        type = request.data.get("type")
        if not email or not otp:
            raise ValidationError(
                "Email and OTP are required",
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
        otp_verify = OTPVerify(email, otp, type)
        email_device = otp_verify.verify_email_otp(otp)
        print(email_device.confirmed, "-------", flush=True)
        if (
            type == "email_verification"
            and email_device.confirmed
            and request.user.email == email
        ):
            user.email_verified = True
            user.save()
        return Response(
            {"data": {"verified": True, "message": "Email verified successfully"}},
            status=status.HTTP_200_OK,
        )
