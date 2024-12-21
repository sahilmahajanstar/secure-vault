class ValidationErrorCodes(enumerate):
    USER_NOT_FOUND = "USER_NOT_FOUND"
    PROFILE_ALREADY_EXISTS = "PROFILE_ALREADY_EXISTS"
    INVALID_FILE_EXTENSION = "INVALID_FILE_EXTENSION"
    FILE_SIZE_EXCEEDS_MAX_LIMIT = "FILE_SIZE_EXCEEDS_MAX_LIMIT"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    PROFILE_NOT_FOUND = "PROFILE_NOT_FOUND"
    INVALID_DATA = ("INVALID_DATA",)
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    NOT_FOUND = "NOT_FOUND"


class ValidationError(Exception):
    def __init__(self, message, code: ValidationErrorCodes, status_code):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.errors = []
        super().__init__(self.message)

    def add_error(self, message, field: str):
        self.errors.append({"message": message, "field": field})

    def add_raw_error(self, e: Exception):
        self.errors.append(e)
