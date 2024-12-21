class TechErrorCodes(enumerate):
    FILE_ENCRYPTION_ERROR = "FILE_ENCRYPTION_ERROR"


class TechError(Exception):
    def __init__(self, message, code: TechErrorCodes, status_code):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)
