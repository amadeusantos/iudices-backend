from datetime import datetime
from enum import Enum
from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import Field

from infrastructure import DefenseType
from ..schemas import BaseSchema, UserMinimalSchema, PaginationSchema, InputSchema


class UserPosition(Enum):
    AUTHOR = "AUTHOR"
    ADVISOR = "ADVISOR"
    CO_ADVISOR = "CO_ADVISOR"
    JURY = "JURY"


class DefenseSchema(BaseSchema):
    id: UUID
    title: str
    abstract: str
    datetime: datetime
    type: DefenseType
    advisor_id: UUID

    advisor: UserMinimalSchema
    co_advisors: List[UserMinimalSchema]
    authors: List[UserMinimalSchema]
    juries: List[UserMinimalSchema]


class DefenseUpdateSchema(InputSchema):
    title: Annotated[str, Field(min_length=3, max_length=64)]
    abstract: str
    datetime: str
    type: DefenseType
    advisor_id: UUID

    authors: Annotated[List[UUID], Field(min_length=1)]
    co_advisors: Optional[List[UUID]] = []
    juries: Annotated[List[UUID], Field(min_length=1)]

class DefenseCreateSchema(DefenseUpdateSchema):
    pass


class DefensePaginationSchema(PaginationSchema):
    results: List[DefenseSchema]
