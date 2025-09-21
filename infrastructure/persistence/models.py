import uuid

from sqlalchemy import Column, UUID, DateTime, func, String
from sqlalchemy.ext.declarative import declarative_base

Entity = declarative_base()
metadata = Entity.metadata

class EntityBase:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UserModel(EntityBase, Entity):
    __tablename__ = "users"
    name = Column(String(255))
    picture = Column(String(255))
    email = Column(String(255), unique=True, nullable=False, index=True)
    google_openid = Column(String(255), unique=True, index=True)