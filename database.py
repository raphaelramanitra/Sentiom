from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "sqlite:///./sentiom.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency generator that provides a database session for each request.
    Ensures the session is safely closed automatically after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()