"""Database engine and session management."""

import logging
from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError

from terraseek.config import settings
from terraseek.db.models import Base

logger = logging.getLogger("terraseek.db")

_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is not None:
        return _engine

    db_url = settings.database.url
    # If using localhost PostgreSQL and it is not available, cleanly fall back to SQLite
    if "postgresql" in db_url and "localhost" in db_url:
        try:
            engine = create_engine(
                db_url,
                echo=settings.database.echo,
                pool_pre_ping=True,
                connect_args={"connect_timeout": 1},
            )
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Connected to primary PostgreSQL database.")
            _engine = engine
            return _engine
        except Exception:
            logger.info("PostgreSQL unavailable on localhost; using SQLite development database.")
    elif "postgresql" in db_url:
        try:
            engine = create_engine(db_url, echo=settings.database.echo, pool_pre_ping=True)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            _engine = engine
            return _engine
        except Exception as e:
            logger.warning(f"Could not connect to primary database: {e}")

    fallback_url = settings.database.sqlite_fallback_url
    if fallback_url.startswith("sqlite:///"):
        sqlite_path = fallback_url.replace("sqlite:///", "")
        if sqlite_path and sqlite_path != ":memory:":
            Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)

    engine = create_engine(
        fallback_url,
        echo=settings.database.echo,
        connect_args={"check_same_thread": False} if "sqlite" in fallback_url else {},
    )
    _engine = engine
    return _engine


def get_session_factory():
    global _SessionLocal
    if _SessionLocal is not None:
        return _SessionLocal
    engine = get_engine()
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SessionLocal


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for database sessions."""
    session_factory = get_session_factory()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all database tables."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")
