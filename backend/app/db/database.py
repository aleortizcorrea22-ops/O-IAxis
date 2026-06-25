"""
Database configuration and session management for O-IAxis
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Database URL configuration
DATABASE_URL = settings.DATABASE_URL or "sqlite:///./oiaxis.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
