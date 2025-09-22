import httpx
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.authentication import authenticated
from config import envSettings
from infrastructure import open_db_session, UserModel
from .exceptions import LoginException
from .schemas import LoginRequest, LoginResponse
from api.schemas import UserPrincipal

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token")
def login_via_google(
    request: LoginRequest, session: Session = Depends(open_db_session)
) -> LoginResponse:
    tokens = httpx.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": request.code,
            "client_id": envSettings.GOOGLE_CLIENT_ID,
            "client_secret": envSettings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": envSettings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
    )

    if tokens.status_code >= httpx.codes.BAD_REQUEST:
        raise LoginException(tokens)

    tokens = tokens.json()

    userinfo = httpx.get(
        "https://www.googleapis.com/oauth2/v2/userinfo?alt=json",
        headers={"Authorization": "Bearer " + tokens["access_token"]},
    )

    if userinfo.status_code >= httpx.codes.BAD_REQUEST:
        raise LoginException(userinfo)

    userinfo = userinfo.json()

    user = session.query(UserModel).where(UserModel.email == userinfo["email"]).first()

    if user:
        user.name = userinfo["name"]
        user.email = userinfo["email"]
        user.google_openid = str(userinfo["id"])
        user.picture = userinfo["picture"]
    else:
        user = UserModel(
            name=userinfo["name"],
            email=userinfo["email"],
            google_openid=str(userinfo["id"]),
            picture=userinfo["picture"],
        )

        session.add(user)

    session.commit()

    return tokens


@router.get("/authenticated")
def authenticated(
    user_principal: UserPrincipal = Depends(authenticated),
) -> UserPrincipal:
    return user_principal
