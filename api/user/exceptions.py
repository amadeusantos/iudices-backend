from ..exceptions import ApiException


class UserAlreadyExistsException(ApiException):
    def __init__(self):
        super().__init__(409, "User already exists!")
