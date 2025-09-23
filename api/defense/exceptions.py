from api.exceptions import ApiException


class DefenseNotFoundException(ApiException):
    def __init__(self):
        super().__init__(404, "Defense not found!")
