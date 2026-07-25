# OpenSchoolOS API — database engine and session (Sprint 001).
# Infrastructure layer. Frozen stack: SQLAlchemy 2.x.
# Uses SQLite locally (DATABASE_URL in .env) and PostgreSQL in production.
# No auth in Sprint 1 (tech-stack.md). Synchronous session for simplicity.
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
