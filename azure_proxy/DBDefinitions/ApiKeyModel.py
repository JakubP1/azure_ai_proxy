from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import String, DateTime, Boolean
from sqlalchemy import ForeignKey, Integer, Index
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from uuid import uuid4

from .BaseModel import BaseModel

class ApiKeyModel(BaseModel):
    __tablename__ = "api_keys"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default_factory=lambda: str(uuid4()))
    
    user_id: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        index=True, 
        default=None, 
        nullable=True
    )

    # uložený pouze hash; prefix pro rychlé hledání kandidátů
    prefix: Mapped[str] = mapped_column(String(32), index=True, default=None)
    key_hash: Mapped[str] = mapped_column(String(128), index=True, default=None)
    name: Mapped[Optional[str]] = mapped_column(String(120), default=None)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=None)
    rate_limit_per_minute: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=None)

    user = relationship("UserModel", back_populates="keys")
    usages = relationship("UsageModel", back_populates="api_key", cascade="all, delete-orphan")

Index("ix_api_keys_active_prefix", ApiKeyModel.prefix, ApiKeyModel.is_active)

