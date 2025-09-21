import uuid

from sqlalchemy import Column, UUID, DateTime, func, String
from sqlalchemy.ext.declarative import declarative_base

Entity = declarative_base()
metadata = Entity.metadata

class EntityBase:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

class UserModel(EntityBase, Entity):
    __tablename__ = "users"
    name = Column(String(64), nullable=False)
    picture = Column(String(64))
    email = Column(String(64), unique=True, nullable=False, index=True)
    google_openid = Column(String(64), unique=True, index=True)