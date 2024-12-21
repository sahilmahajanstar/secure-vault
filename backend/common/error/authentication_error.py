from rest_framework_simplejwt.exceptions import AuthenticationFailed


class AuthenticationErrorCodes(enumerate):
    INVALID_CREDENTIALS = ("INVALID_CREDENTIALS",)
    TOKEN_EXPIRED = "TOKEN_EXPIRED"


class AuthenticationError(AuthenticationFailed):
    def __init__(self, message, code: AuthenticationErrorCodes, status_code):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(
            {
                "error": {
                    "message": self.message,
                    "code": self.code,
                }
            }
        )

    def add_raw_error(self, e: Exception):
        self.errors.append(e)
