"""Agent management endpoints (CRUD + trigger)."""

from typing import Annotated, Any, Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import TokenData, get_current_user
from app.database import get_db

router = APIRouter(prefix="/agents", tags=["agents"])


#  Pydantic schemas 

class AgentConfig(BaseModel):
    data_source:         Dict[str, Any]
    query:               Optional[str]   = None
    schedule:            Optional[str]   = "0 * * * *"     # cron
    alert_threshold_pct: float           = 15.0
    unit:                Optional[str]   = None


class AgentCreate(BaseModel):
    name:        str
    type:        str            = "monitor"
    description: Optional[str] = None
    config:      AgentConfig


class AgentResponse(BaseModel):
    id:          str
    name:        str
    type:        str
    description: Optional[str]
    is_active:   bool
    run_count:   int
    error_count: int

    class Config:
        from_attributes = True


class AgentRunResponse(BaseModel):
    run_id:     str
    agent_id:   str
    status:     str
    message:    str


#  Endpoints 

@router.get("", response_model=List[AgentResponse])
async def list_agents(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    db:           Annotated[AsyncSession, Depends(get_db)],
    is_active:    bool = True,
    limit:        int  = 50,
    offset:       int  = 0,
) -> List[AgentResponse]:
    """List all agents for the caller's organization."""
    # TODO: query Agent model filtered by org_id
    return []


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    payload:      AgentCreate,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    db:           Annotated[AsyncSession, Depends(get_db)],
) -> AgentResponse:
    """Create a new monitoring agent."""
    if current_user.role not in ("admin", "analyst"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
    # TODO: persist to DB
    return AgentResponse(
        id=str(uuid4()),
        name=payload.name,
        type=payload.type,
        description=payload.description,
        is_active=True,
        run_count=0,
        error_count=0,
    )


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id:     str,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    db:           Annotated[AsyncSession, Depends(get_db)],
) -> AgentResponse:
    """Fetch a single agent by ID."""
    # TODO: query DB
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")


@router.post("/{agent_id}/run", response_model=AgentRunResponse)
async def trigger_agent_run(
    agent_id:         str,
    background_tasks: BackgroundTasks,
    current_user:     Annotated[TokenData, Depends(get_current_user)],
    db:               Annotated[AsyncSession, Depends(get_db)],
) -> AgentRunResponse:
    """Manually trigger an agent run (runs asynchronously in background)."""
    run_id = str(uuid4())
    # TODO: background_tasks.add_task(orchestrator.run_monitor_pipeline, ...)
    return AgentRunResponse(
        run_id=run_id,
        agent_id=agent_id,
        status="queued",
        message=f"Run {run_id} queued successfully.",
    )


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id:     str,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    db:           Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Soft-delete an agent (sets is_active=False)."""
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    # TODO: soft delete in DB