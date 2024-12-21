import os
from rest_framework import status
from common.error.validation_error import ValidationError, ValidationErrorCodes
from django.core.files.uploadedfile import InMemoryUploadedFile


class FileValidator:
    VALID_CONTENT_TYPES = {
        "application/pdf": [".pdf"],
        "text/plain": [".txt"],
        "image/jpeg": [".jpg", ".jpeg"],
        "image/png": [".png"],
        "image/gif": [".gif"],
        "image/webp": [".webp"],
        "audio/mpeg": [".mp3"],
        "audio/wav": [".wav"],
        "audio/ogg": [".ogg"],
        "video/mp4": [".mp4"],
        "video/avi": [".avi"],
        "video/mov": [".mov"],
    }

    def __init__(self, max_size_mb: int):
        self.MAX_SIZE_MB = max_size_mb

    def get_file_extension(self, file: str):
        return os.path.splitext(file.name)[1].lower()

    def validate(self, file: InMemoryUploadedFile):
        if file.size > self.MAX_SIZE_MB * 1024 * 1024:
            raise ValidationError(
                "File size exceeds the maximum limit",
                ValidationErrorCodes.FILE_SIZE_EXCEEDS_MAX_LIMIT,
                status.HTTP_400_BAD_REQUEST,
            )

        content_type = file.content_type
        if content_type not in self.VALID_CONTENT_TYPES:
            raise ValidationError(
                "Invalid file type",
                ValidationErrorCodes.INVALID_FILE_TYPE,
                status.HTTP_400_BAD_REQUEST,
            )
        ext = self.get_file_extension(file.name)
        if ext not in self.VALID_CONTENT_TYPES[content_type]:
            raise ValidationError(
                "File extension does not match its content",
                ValidationErrorCodes.INVALID_FILE_EXTENSION,
                status.HTTP_400_BAD_REQUEST,
            )
