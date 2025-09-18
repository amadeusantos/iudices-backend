from api.schemas import InputSchema, BaseSchema


class LoginRequest(InputSchema):
    code: str

class LoginResponse(BaseSchema):
    id_token: str
    access_token: str
    refresh_token: str | None = None
    expires_in: int
    token_type: str
