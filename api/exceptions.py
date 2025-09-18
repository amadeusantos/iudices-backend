class ApiException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

class TokenInvalidException(ApiException):
    def __init__(self):
        super().__init__(401, "token invalid")