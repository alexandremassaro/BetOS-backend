from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import create_db_and_tables

# from typing import Union


@asynccontextmanager
async def lifespan(app: FastAPI):
    "Application lifespan manager"
    # Startup: Create database tables
    create_db_and_tables()
    yield


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")
