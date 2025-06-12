from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings
from structlog import get_logger
logger = get_logger(__name__)

Base = declarative_base()

from gpt import Event as gptEvent

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    items_to_bring = Column(JSON, ARRAY(String), nullable=False)

# Initialize database connection
ENGINE = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=ENGINE)
session = Session()
Base.metadata.create_all(ENGINE)

def gpt2sql(event: gptEvent) -> Event:
    return Event(
        name=event.name,
        datetime=event.datetime,
        location=event.location,
        items_to_bring=event.items_to_bring
    )

def create_event(event: gptEvent):
    """
    Creates event in database
    :param event: gpt.Event
    :return: None
    """
    logger.info("creating_event", name=event.name)
    try:
        session.add(gpt2sql(event))
        session.commit()
        logger.info("created_event", name=event.name)
    except Exception as e:
        logger.error("create_event_failed", name=event.name, error=str(e))
        session.rollback()
        raise


