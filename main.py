import argparse, time
import json

import dotenv
from gmail import (init_gmail, get_latest_emails,unpack_gmail_message,
                    decode_messages
                   )
from gpt import init_openai, get_events

dotenv.load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('-t','--token')
parser.add_argument('-o','--output')
parser.add_argument('-d','--debug', action='store_true')
args = parser.parse_args()

gmail_service = init_gmail(args.token)
openai_client = init_openai()

def fetch_events():
    emails = get_latest_emails(gmail_service, debug=args.debug)
    messages = decode_messages(emails)
    return get_events(openai_client, messages)

def write_events(events):
    for event in events:
        if args.debug: print(event.get('datetime'))
        if event.get('name', ''):
            with open(args.output, 'a') as f:
                f.write(json.dumps(event)+'\n')


FREQ = 60 if not args.debug else 15

while True:
    events = fetch_events()
    write_events(events)
    time.sleep(FREQ)













