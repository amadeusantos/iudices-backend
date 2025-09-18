from typing import Annotated, Optional

from cryptography.x509 import load_pem_x509_certificate
import httpx
import jwt
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2
from pydantic import ValidationError

from config import envSettings
from api.exceptions import TokenInvalidException


def authenticated(
    authorization: Annotated[
        Optional[HTTPAuthorizationCredentials], Depends(HTTPBearer())
    ],
):
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
        return user_id
    except (jwt.InvalidTokenError, ValidationError, KeyError) as e:
        print(type(e))
        raise TokenInvalidException()
