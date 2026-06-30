"""User & Organization ORM models."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Organization(Base):
    __tablename__ = "organizations"

    id:         Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name:       Mapped[str] = mapped_column(String(256), nullable=False)
    slug:       Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    plan:       Mapped[str] = mapped_column(String(32), default="starter")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    is_active:  Mapped[bool] = mapped_column(Boolean, default=True)

    users:   Mapped[List["User"]]   = relationship(back_populates="organization", lazy="select")
    agents:  Mapped[List["Agent"]]  = relationship(back_populates="organization", lazy="select")


class User(Base):
    __tablename__ = "users"

    id:          Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id:      Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    email:       Mapped[str] = mapped_column(String(256), unique=True, nullable=False, index=True)
    name:        Mapped[str] = mapped_column(String(256), nullable=False)
    role:        Mapped[str] = mapped_column(String(32), default="viewer")   # admin | analyst | viewer
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    is_active:   Mapped[bool] = mapped_column(Boolean, default=True)
    created_at:  Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    last_login:  Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    organization: Mapped["Organization"] = relationship(back_populates="users")