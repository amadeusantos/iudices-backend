from typing import Annotated, Optional

from cryptography.x509 import load_pem_x509_certificate
import httpx
import jwt
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2
from pydantic import ValidationError
from sqlalchemy.orm import Session

from api.schemas import UserPrincipal
from config import envSettings
from api.exceptions import TokenInvalidException, UnauthorizedException
from infrastructure import open_db_session, UserModel


def authenticated(
    authorization: Annotated[
        Optional[HTTPAuthorizationCredentials], Depends(HTTPBearer())
    ],
    session: Session = Depends(open_db_session),
) -> UserPrincipal:
    try:
        kid = jwt.get_unverified_header(authorization.credentials)["kid"]
        certificates = httpx.get(envSettings.GOOGLE_CERTIFICATES_URL).json()
        certificate = load_pem_x509_certificate(certificates[kid].encode())
        public_key = certificate.public_key()
        payload = jwt.decode(
            authorization.credentials,
            public_key,
            algorithms=["RS256"],
            audience=envSettings.GOOGLE_CLIENT_ID,
        )
        user_id = payload.get("sub", "")

        user = (
            session.query(
                UserModel.id, UserModel.name, UserModel.email, UserModel.google_openid
            )
            .where(UserModel.google_openid == user_id)
            .first()
        )

        if user is None:
            raise UnauthorizedException()

        id, name, email, google_openid = user
        user_principal = UserPrincipal(
            id=id, name=name, email=email, google_openid=google_openid
        )
        return user_principal
    except (jwt.InvalidTokenError, ValidationError, KeyError):
        raise TokenInvalidException()
