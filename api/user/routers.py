from typing import Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from infrastructure import UserModel, open_db_session
from .schemas import UserPaginationSchema
from .validations import validate_email
from ..authentication import authenticated
from ..database import pagination
from ..schemas import UserPrincipal

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=UserPaginationSchema)
def users_pagination(
    page: int = 1,
    size: int = 25,
    search: Optional[str] = None,
    session: Session = Depends(open_db_session),
    _: UserPrincipal = Depends(authenticated),
):
    query = session.query(UserModel)
    filters = []

    if search:
        filters.append(
            or_(UserModel.name.istartswith(search), UserModel.name.istartswith(search))
        )

    order = [UserModel.name]
    return pagination(query, page, size, filters, order)


@router.post("/check-email", status_code=204)
def check_email(
    email: str,
    exclude_id: Optional[UUID] = None,
    session: Session = Depends(open_db_session),
    _: UserPrincipal = Depends(authenticated),
):
    validate_email(session, email, exclude_id)
    return
