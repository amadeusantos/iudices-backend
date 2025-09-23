from datetime import datetime
from typing import Optional, List, Annotated
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy import or_, ColumnElement, update
from sqlalchemy.orm import Session

from infrastructure import DefenseModel, open_db_session, UserModel
from .actions import (
    create_authors,
    create_co_advisor,
    create_juries,
    update_authors,
    update_co_advisor,
    update_juries,
)
from .exceptions import DefenseNotFoundException
from .schemas import (
    DefensePaginationSchema,
    DefenseSchema,
    UserPosition,
    DefenseCreateSchema, DefenseUpdateSchema,
)
from ..authentication import authenticated
from ..database import pagination
from ..schemas import UserPrincipal

router = APIRouter(prefix="/defenses", tags=["Defenses"])


def resolver_user_position(
    user_id: UUID, positions: List[UserPosition]
) -> ColumnElement[bool]:
    position_filters = {
        UserPosition.AUTHOR: DefenseModel.authors.has(UserModel.id == user_id),
        UserPosition.ADVISOR: DefenseModel.advisor_id == user_id,
        UserPosition.CO_ADVISOR: DefenseModel.co_advisors.has(UserModel.id == user_id),
        UserPosition.JURY: DefenseModel.juries.has(UserModel.id == user_id),
    }

    return or_(position_filters[position] for position in positions)


def get_by_id(session: Session, id: UUID) -> type[DefenseModel]:
    defense = session.query(DefenseModel).where(DefenseModel.id == id).first()
    if not defense:
        raise DefenseNotFoundException()
    return defense


@router.get("", response_model=DefensePaginationSchema)
def defenses_pagination(
    page: int = 1,
    size: int = 25,
    user_id: Optional[UUID] = None,
    gte_date: Optional[datetime] = None,
    lte_date: Optional[datetime] = None,
    search: Optional[str] = None,
    positions: Optional[List[UserPosition]] = Query(None),
    session: Session = Depends(open_db_session),
    _: UserPrincipal = Depends(authenticated),
):
    query = session.query(DefenseModel)
    filters = []

    if gte_date:
        filters.append(DefenseModel.datetime >= gte_date)

    if lte_date:
        filters.append(DefenseModel.datetime <= lte_date)

    if user_id:
        if positions is None:
            positions = [position for position in UserPosition]
        filters.append(resolver_user_position(user_id, positions))

    if search:
        filters.append(DefenseModel.title.icontains(search))

    order = [DefenseModel.datetime]
    return pagination(query, page, size, filters, order)


@router.get("/{id}", response_model=DefenseSchema)
def get_defense_by_id(
    id: UUID,
    session: Session = Depends(open_db_session),
    _: UserPrincipal = Depends(authenticated),
):
    return get_by_id(session, id)


@router.post("", response_model=DefenseSchema)
def create_defense(
    content: DefenseCreateSchema,
    session: Session = Depends(open_db_session),
    _: UserPrincipal = Depends(authenticated),
):
    defense = DefenseModel(
        **content.model_dump(exclude={"authors", "co_advisors", "juries"})
    )
    session.add(defense)
    session.flush()
    create_authors(session, defense.id, content.authors)
    create_co_advisor(session, defense.id, content.co_advisors)
    create_juries(session, defense.id, content.juries)
    session.commit()

    session.refresh(defense)
    return defense


@router.put("/{id}", response_model=DefenseSchema)
def update_defense(
    id: UUID,
    content: DefenseUpdateSchema,
    session: Session = Depends(open_db_session),
    _: UserPrincipal = Depends(authenticated),
):
    defense = get_by_id(session, id)

    stmt = (
        update(DefenseModel)
        .where(DefenseModel.id == defense.id)
        .values(**content.model_dump(exclude={"authors", "co_advisors", "juries"}))
    )
    session.execute(stmt)

    update_authors(session, id, content.authors)
    update_co_advisor(session, id, content.co_advisors)
    update_juries(session, id, content.juries)
    session.commit()

    session.refresh(defense)
    return defense
