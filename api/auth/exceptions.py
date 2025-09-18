from httpx import Response

from ..exceptions import ApiException


class LoginException(ApiException):
    def __init__(self, response: Response):
        super().__init__(401, response.json().get("error_description"))