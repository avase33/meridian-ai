"""Meridian AI � FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.agents   import router as agents_router
from app.api.v1.auth     import router as auth_router
from app.api.v1.insights import router as insights_router
from app.config import settings
from app.database import create_tables

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown lifecycle."""
    logger.info("meridian.startup", environment=settings.environment)
    await create_tables()
    yield
    logger.info("meridian.shutdown")


app = FastAPI(
    title="Meridian AI",
    description=(
        "Enterprise Autonomous Business Intelligence Agent Platform. "
        "Proactive anomaly detection, root-cause analysis, and executive reporting."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

#  Middleware 

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Prometheus metrics 

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

#  Routers 

API_PREFIX = "/api/v1"

app.include_router(auth_router,     prefix=API_PREFIX)
app.include_router(agents_router,   prefix=API_PREFIX)
app.include_router(insights_router, prefix=API_PREFIX)


#  Health check 

@app.get("/health", tags=["system"])
async def health() -> dict:
    return {
        "status": "ok",
        "service": "meridian-ai",
        "version": app.version,
        "environment": settings.environment,
    }


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Meridian AI API. See /docs for the full API reference."}