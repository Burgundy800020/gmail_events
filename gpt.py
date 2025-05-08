from openai import OpenAI
import os, json
from pydantic import BaseModel

def init_openai():
    return OpenAI(api_key=os.environ['OPEN_AI'])

class Event(BaseModel):
    name: str
    date: str
    location: str
    items_to_bring: list[str]

PROMPT = ("You will be given an email body. Extract the event information. "
          "If no event or a field is missing, leave it blank"
          )

def get_events(client, messages):
    responses = []
    for message in messages:
        response = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": PROMPT},
                {
                    "role": "user",
                    "content": message
                },
            ],
            response_format=Event
        )
        responses.append(json.loads(response.choices[0].message.content))
    return responses




