"""Agent ORM model."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Agent(Base):
    __tablename__ = "agents"

    id:           Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id:       Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False, index=True)
    name:         Mapped[str] = mapped_column(String(256), nullable=False)
    type:         Mapped[str] = mapped_column(String(32), default="monitor")
    description:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    config:       Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    schedule:     Mapped[Optional[str]] = mapped_column(String(64), nullable=True)  # cron expression
    is_active:    Mapped[bool] = mapped_column(Boolean, default=True)
    created_at:   Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at:   Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    last_run_at:  Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    run_count:    Mapped[int] = mapped_column(default=0)
    error_count:  Mapped[int] = mapped_column(default=0)

    organization: Mapped["Organization"] = relationship(back_populates="agents")
    insights:     Mapped[List["Insight"]] = relationship(back_populates="agent", lazy="select")