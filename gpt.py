from datetime import datetime
from typing import List

from openai import OpenAI
from pydantic import BaseModel
from config import settings
from structlog import get_logger
logger = get_logger(__name__)

def init_openai():
    return OpenAI(api_key=settings.OPENAI_API_KEY)

class Event(BaseModel):
    name: str
    datetime: datetime
    location: str
    items_to_bring: list[str]

PROMPT = ("You will be given an email body. Extract the event information. "
          "If no event or a field is missing, leave it blank. "
          f"Today's date is {datetime.now().strftime('%A, %B %d, %Y')} "
          f"and the current time is {datetime.now().strftime('%I:%M %p')}."
          )

def get_events(client: OpenAI, messages) -> List[Event]:
    responses = []
    for message in messages:
        try:
            response = client.responses.parse(
                model=settings.GPT_MODEL,
                input=[
                    {"role": "system", "content": PROMPT},
                    {"role": "user", "content": message},
                ],
                text_format=Event
            )
            responses.append(response.output_parsed)
        except Exception as e:
            logger.error("event_extraction_failed", error=str(e), message=message[:100])
            continue
    return responses




