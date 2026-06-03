"""FastAPI application entry point for the MoneyTracker sync server."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.sync import router as sync_router
from app.db.database import engine
from app.models.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all database tables on startup if they do not already exist."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="MoneyTracker API", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(sync_router)
