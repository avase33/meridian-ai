"""Insight ORM model â€” stores generated briefings and user feedback."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Insight(Base):
    __tablename__ = "insights"

    id:               Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id:         Mapped[str] = mapped_column(ForeignKey("agents.id"), nullable=False, index=True)
    run_id:           Mapped[str] = mapped_column(String, nullable=False, index=True)
    severity:         Mapped[str] = mapped_column(String(16), default="medium")   # critical|high|medium|low
    metric_name:      Mapped[str] = mapped_column(String(256), nullable=False)
    current_value:    Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    baseline_mean:    Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    deviation_pct:    Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    zscore:           Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    root_cause:       Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    briefing_markdown: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recommended_actions: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    confidence:       Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    feedback:         Mapped[Optional[str]] = mapped_column(String(16), nullable=True)  # helpful|not_helpful
    created_at:       Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    resolved_at:      Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    agent: Mapped["Agent"] = relationship(back_populates="insights")