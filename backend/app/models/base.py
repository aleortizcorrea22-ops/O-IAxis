"""
Base model with common fields for all entities
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, Boolean
from app.db.database import Base


class BaseModel(Base):
    """Abstract base model with audit fields"""

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
