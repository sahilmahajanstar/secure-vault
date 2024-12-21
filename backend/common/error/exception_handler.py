from functools import wraps
from rest_framework import status
from rest_framework.response import Response


class ExceptionHandler:
    @staticmethod
    def format_response(e: Exception):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if hasattr(e, "status_code"):
            status_code = e.status_code
        return (
            {
                "error": {
                    "message": e.message if hasattr(e, "message") else str(e),
                    "name": e.__class__.__name__,
                    "code": e.code if hasattr(e, "code") else None,
                    "errors": e.errors if hasattr(e, "errors") else None,
                }
            },
            status_code,
        )

    @staticmethod
    def handle(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                return res
            except Exception as e:
                response, status_code = ExceptionHandler.format_response(e)
                return Response(response, status=status_code)

        return wrapper
