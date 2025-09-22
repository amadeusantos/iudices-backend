import uuid
from typing import List

from sqlalchemy import Column, UUID, DateTime, func, String, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship

from .enums import DefenseType

Entity = declarative_base()
metadata = Entity.metadata


class EntityBase:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class UserModel(EntityBase, Entity):
    __tablename__ = "users"
    name = Column(String(64), nullable=False)
    picture = Column(String)
    email = Column(String(64), unique=True, nullable=False, index=True)
    google_openid = Column(String(64), unique=True, index=True)


class AuthorsModel(Entity):
    __tablename__ = "authors"

    user_id = Column(ForeignKey("users.id"), nullable=False, primary_key=True)
    defense_id = Column(ForeignKey("defenses.id"), nullable=False, primary_key=True)


class CoAdvisorModel(Entity):
    __tablename__ = "co_advisors"

    user_id = Column(ForeignKey("users.id"), nullable=False, primary_key=True)
    defense_id = Column(ForeignKey("defenses.id"), nullable=False, primary_key=True)


class JuryModel(Entity):
    __tablename__ = "juries"

    user_id = Column(ForeignKey("users.id"), nullable=False, primary_key=True)
    defense_id = Column(ForeignKey("defenses.id"), nullable=False, primary_key=True)


class DefenseModel(EntityBase, Entity):
    __tablename__ = "defenses"

    title = Column(String(64), nullable=False)
    abstract = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    type = Column(Enum(DefenseType), nullable=False)
    advisor_id = Column(ForeignKey("users.id"), nullable=False)

    advisor: Mapped[UserModel] = relationship("UserModel")

    authors: Mapped[List[UserModel]] = relationship(
        "UserModel", secondary="authors", order_by="UserModel.name"
    )
    co_advisors: Mapped[List[UserModel]] = relationship(
        "UserModel", secondary="co_advisors", order_by="UserModel.name"
    )
    juries: Mapped[List[UserModel]] = relationship(
        "UserModel", secondary="juries", order_by="UserModel.name"
    )
