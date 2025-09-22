from typing import List
from uuid import UUID

from ..schemas import PaginationSchema, BaseSchema


class UserSchema(BaseSchema):
    id: UUID
    email: str
    name: str


class UserPaginationSchema(PaginationSchema):
    results: List[UserSchema]
