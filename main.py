import time
from typing import List

import uvicorn

from config import settings
from structlog import get_logger
logger = get_logger(__name__)
from gmail import init_gmail, get_latest_emails, decode_messages
from gpt import init_openai, extract_events, Event
from api_server import app
from database import create_event

def main():
    logger.info("starting_application", mode=settings.mode)
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

if __name__ == "__main__":
    main()













