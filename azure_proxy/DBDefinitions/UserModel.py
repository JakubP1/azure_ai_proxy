from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import String, DateTime, Boolean
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from uuid import uuid4

from .BaseModel import BaseModel

class UserModel(BaseModel):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default_factory=lambda: str(uuid4()))
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(timezone.utc))
    # Entra ID object id (OID) – pro spolehlivý mapping identity
    oid: Mapped[Optional[str]] = mapped_column(String(64), unique=True, index=True, default=None)
    email: Mapped[Optional[str]] = mapped_column(String(320), index=True, default=None)
    display_name: Mapped[Optional[str]] = mapped_column(String(200), default=None)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    # keys: Mapped[list["ApiKey"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    keys = relationship("ApiKeyModel", back_populates="user", cascade="all, delete-orphan")
