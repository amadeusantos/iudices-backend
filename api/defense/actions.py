from typing import List
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.orm import Session

from infrastructure import AuthorsModel, CoAdvisorModel, JuryModel


def create_authors(session: Session, defense_id: UUID, authors_id: List[UUID]):
    authors = [
        AuthorsModel(defense_id=defense_id, user_id=author_id)
        for author_id in authors_id
    ]
    session.add_all(authors)


def create_co_advisor(session: Session, defense_id: UUID, co_advisors_id: List[UUID]):
    co_advisors = [
        CoAdvisorModel(defense_id=defense_id, user_id=co_advisor_id)
        for co_advisor_id in co_advisors_id
    ]
    session.add_all(co_advisors)


def create_juries(session: Session, defense_id: UUID, juries_id: List[UUID]):
    juries = [
        JuryModel(defense_id=defense_id, user_id=jury_id) for jury_id in juries_id
    ]
    session.add_all(juries)


def update_authors(session: Session, defense_id: UUID, authors_id: List[UUID]):
    stmt = delete(AuthorsModel).where(AuthorsModel.defense_id == defense_id)
    session.execute(stmt)
    create_authors(session, defense_id, authors_id)


def update_co_advisor(session: Session, defense_id: UUID, co_advisors_id: List[UUID]):
    stmt = delete(CoAdvisorModel).where(CoAdvisorModel.defense_id == defense_id)
    session.execute(stmt)
    create_co_advisor(session, defense_id, co_advisors_id)


def update_juries(session: Session, defense_id: UUID, juries_id: List[UUID]):
    stmt = delete(JuryModel).where(JuryModel.defense_id == defense_id)
    session.execute(stmt)
    create_juries(session, defense_id, juries_id)
