import httpx
from fastapi import APIRouter
from fastapi.params import Depends

from api.auth.exceptions import LoginException
from api.auth.schemas import LoginRequest, LoginResponse
from api.authentication import authenticated
from config import envSettings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
def login_via_google(request: LoginRequest) -> LoginResponse:
    response = httpx.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": request.code,
            "client_id": envSettings.GOOGLE_CLIENT_ID,
            "client_secret": envSettings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": envSettings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
    )

    if response.status_code >= httpx.codes.BAD_REQUEST:
        raise LoginException(response)

    return response.json()


@router.get("/authenticated")
def authenticated(user_principal: int = Depends(authenticated)):
    return user_principal
