import argparse, time
import json
from typing import List

import dotenv
dotenv.load_dotenv()

from gmail import (init_gmail, get_latest_emails,unpack_gmail_message,
                    decode_messages
                   )
from gpt import init_openai, get_events, Event
from database import create_event


parser = argparse.ArgumentParser()
parser.add_argument('-t','--token')
parser.add_argument('-o','--output')
parser.add_argument('-d','--debug', action='store_true')
parser.add_argument('--alltime', action='store_true')
args = parser.parse_args()

gmail_service = init_gmail(args.token)
openai_client = init_openai()

def fetch_events():
    emails = get_latest_emails(gmail_service, alltime=args.alltime)
    messages = decode_messages(emails)
    return get_events(openai_client, messages)

def write_events(events:List[Event]):
    for event in events:
        if event.name:
            if args.output:
                with open(args.output, 'a') as f:
                    f.write(event.model_dump_json()+'\n')
            create_event(event)


FREQ = 60 if not args.debug else 15

while True:
    events = fetch_events()
    write_events(events)
    time.sleep(FREQ)













