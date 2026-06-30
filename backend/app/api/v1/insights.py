"""Insight feed and feedback endpoints."""

from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import TokenData, get_current_user
from app.database import get_db

router = APIRouter(prefix="/insights", tags=["insights"])


class InsightResponse(BaseModel):
    id:                 str
    agent_id:           str
    severity:           str
    metric_name:        str
    current_value:      Optional[float]
    deviation_pct:      Optional[float]
    root_cause:         Optional[str]
    briefing_markdown:  Optional[str]
    confidence:         Optional[float]
    created_at:         str
    feedback:           Optional[str]


class FeedbackPayload(BaseModel):
    rating:  str        # "helpful" | "not_helpful"
    comment: Optional[str] = None


@router.get("", response_model=List[InsightResponse])
async def list_insights(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    db:           Annotated[AsyncSession, Depends(get_db)],
    severity:     Optional[str] = None,
    agent_id:     Optional[str] = None,
    limit:        int           = 20,
    offset:       int           = 0,
) -> List[InsightResponse]:
    """Return the insight feed for the caller's organization, newest first."""
    # TODO: query Insight model
    return []


@router.get("/{insight_id}", response_model=InsightResponse)
async def get_insight(
    insight_id:   str,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    db:           Annotated[AsyncSession, Depends(get_db)],
) -> InsightResponse:
    """Fetch a single insight by ID."""
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Insight not found")


@router.post("/{insight_id}/feedback", status_code=status.HTTP_204_NO_CONTENT)
async def submit_feedback(
    insight_id:   str,
    payload:      FeedbackPayload,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    db:           Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """
    Record user feedback on an insight.
    Meridian uses this signal to improve anomaly detection accuracy over time.
    """
    if payload.rating not in ("helpful", "not_helpful"):
        raise HTTPException(status_code=400, detail="rating must be 'helpful' or 'not_helpful'")
    # TODO: update Insight.feedback in DB