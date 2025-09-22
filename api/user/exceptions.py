from ..exceptions import ApiException


class UserEmailAlreadyExistsException(ApiException):
    def __init__(self):
        super().__init__(409, "User email already exists!")
