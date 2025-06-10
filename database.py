import os

from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, sessionmaker
Base = declarative_base()

from dotenv import load_dotenv
load_dotenv()

from gpt import Event as gptEvent

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    items_to_bring = Column(JSON, ARRAY(String), nullable=False)

print(Base.metadata)

DATABASE_URL = os.environ.get('DATABASE_URL')
ENGINE = create_engine(DATABASE_URL)
Session = sessionmaker(bind=ENGINE)
session = Session()
Base.metadata.create_all(ENGINE)


def gpt2sql(event: gptEvent)->Event:
    return Event(name=event.name, datetime=event.datetime, location=event.location,
                 items_to_bring=event.items_to_bring)


def create_event(event:gptEvent):
    """
    :param event: gpt.Event
    :return: None
    Creates event to database
    """
    session.add(gpt2sql(event))
    session.commit()


