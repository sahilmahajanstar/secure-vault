# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_otp.plugins.otp_email.models import EmailDevice

from common.error.validation_error import ValidationError, ValidationErrorCodes

from ..models.users import Users
from ..models.repository import Repository


class OTPVerify:
    repository = Repository()

    def __init__(self, email: str, otp: str, type: str):
        self.email = email
        self.otp = otp
        self.type = type

    def verify_email_otp(self, otp: str):
        email_device = self.repository.email_device.filter(
            email=self.email, confirmed=False, name=self.type
        ).first()
        if not email_device:
            raise ValidationError(
                "No pending verification found for this email",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )

        if not email_device.verify_token(otp):
            raise ValidationError(
                "Invalid OTP",
                ValidationErrorCodes.INVALID_DATA,
                status.HTTP_400_BAD_REQUEST,
            )

        email_device.confirmed = True
        email_device.save()
        return email_device
