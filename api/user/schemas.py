from typing import List, Annotated
from uuid import UUID

from pydantic import Field, EmailStr

from ..schemas import PaginationSchema, BaseSchema, InputSchema


class UserSchema(BaseSchema):
    id: UUID
    email: str
    name: str

class UserCreateSchema(InputSchema):
    email: Annotated[str, EmailStr]
    name: Annotated[str, Field(min_length=3, max_length=64)]


class UserPaginationSchema(PaginationSchema):
    results: List[UserSchema]
