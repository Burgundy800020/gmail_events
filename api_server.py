from datetime import datetime, timedelta
from typing import List
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from structlog import get_logger
logger = get_logger(__name__)
from config import settings
from database import select_events_between
from gpt import Event
from utils import init_services, fetch_events, write_events

@asynccontextmanager
async def lifespan(app: FastAPI):
    gmail_service, openai_client = init_services()
    task = asyncio.create_task(background_polling(gmail_service, openai_client))
    yield
    task.cancel()
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def background_polling(gmail_service, openai_client):
    while True:
        try:
            events = fetch_events(gmail_service, openai_client)
            write_events(events)
            await asyncio.sleep(settings.POLLING_INTERVAL)
        except Exception as e:
            logger.error("main_loop_error", error=str(e))
            await asyncio.sleep(settings.POLLING_INTERVAL)


@app.get("/events", response_model=List[Event])
def get_events():
    now = datetime.now()
    start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end = (now + timedelta(days=7)).replace(hour=23, minute=59, second=59, microsecond=999999)
    return select_events_between(start, end)