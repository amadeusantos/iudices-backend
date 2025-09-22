from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from infrastructure import UserModel
from .exceptions import UserAlreadyExistsException


def validate_email(session: Session, email: str, exclude_id: Optional[UUID] = None):
    filters = [UserModel.email == email]

    if exclude_id:
        filters.append(UserModel.id != exclude_id)

    user = session.query(UserModel).where(*filters).first()

    if user:
        raise UserAlreadyExistsException()
