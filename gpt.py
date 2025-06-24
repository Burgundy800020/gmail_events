from datetime import datetime as dt
from typing import List

from openai import OpenAI
from pydantic import BaseModel, Field
from config import settings
from structlog import get_logger
logger = get_logger(__name__)

def init_openai():
    return OpenAI(api_key=settings.OPENAI_API_KEY)

class Event(BaseModel):
    name: str
    datetime: dt
    location: str
    items_to_bring: list[str]


def extract_events(client: OpenAI, messages) -> List[Event]:
    if not messages: return []
    local_time = dt.now().astimezone()
    PROMPT = ("You will be given an email body. Extract the event information. "
              "If no event or a field is missing, leave it blank. "
              f"Today's date is {local_time.strftime('%A, %B %d, %Y')} "
              f"and the current local time is {local_time.strftime('%I:%M %p')}. "
              f"The timezone of my region is {local_time.tzinfo}, so output "
              f"all time-related information in {local_time.tzinfo}. "
              )
    responses = []
    logger.info("Prompting gpt", prompt=PROMPT)
    for message in messages:
        try:
            logger.info("gpt input time", time=dt.now().strftime('%I:%M %p'))
            response = client.responses.parse(
                model=settings.GPT_MODEL,
                input=[
                    {"role": "system", "content": PROMPT},
                    {"role": "user", "content": message},
                ],
                text_format=Event
            )
            extracted_event:Event = response.output_parsed
            logger.info("gpt output time", time=extracted_event.datetime.strftime('%I:%M %p'))
            logger.info("gpt output tz", tz=extracted_event.datetime.tzinfo)
            responses.append(extracted_event)
        except Exception as e:
            logger.error("event_extraction_failed", error=str(e), message=message[:100])
            continue
    return responses




