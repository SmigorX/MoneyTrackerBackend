"""SQLAlchemy engine, session factory, and the FastAPI database dependency."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency that yields a database session and closes it afterwards.

    Use with ``Depends(get_db)`` in route handlers to obtain a short-lived
    session that is always cleaned up, even if the request raises an exception.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
