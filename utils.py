from typing import List

from config import settings
from structlog import get_logger
logger = get_logger(__name__)
from gmail import init_gmail, get_latest_emails, decode_messages
from gpt import init_openai, extract_events, Event
from database import create_event

def init_services():
    """Initialize all required services"""
    if not settings.token:
        raise ValueError("GMAIL_TOKEN_PATH must be set in environment or .env file")

    gmail_service = init_gmail(settings.token)
    openai_client = init_openai()
    return gmail_service, openai_client


def fetch_events(gmail_service, openai_client):
    """Fetch and process events from emails"""
    emails = get_latest_emails(gmail_service)
    messages = decode_messages(emails)
    return extract_events(openai_client, messages)


def write_events(events: List[Event]):
    """Write events to output file and database"""
    for event in events:
        if event.name:
            if settings.output:
                with open(settings.output, 'a') as f:
                    f.write(event.model_dump_json() + '\n')
            create_event(event)

