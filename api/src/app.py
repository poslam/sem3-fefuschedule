import asyncio
from fastapi import BackgroundTasks, Depends, FastAPI
from src.malfunc import event_updater
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.api import api_router
from database.database import get_session


app = FastAPI()

app.include_router(api_router)
