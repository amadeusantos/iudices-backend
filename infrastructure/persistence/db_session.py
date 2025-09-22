from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import envSettings

engine = create_engine(envSettings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

def open_db_session() -> Generator[Session]:
    session = None
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
