import base64
import time
START_STAMP =  time.time_ns() // 1_000_000
import sys
DEBUG = '-d' in sys.argv

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def init_gmail(token_path):
    creds = Credentials.from_authorized_user_file(token_path,
                                                  ['https://www.googleapis.com/auth/gmail.readonly'])

    # Build the Gmail service
    return build('gmail', 'v1', credentials=creds)


def get_latest_emails(service, alltime=False):
    """
    Returns a list of email messages dating later than START_STAMP
    :param service: the gmail service object
    :param start_date: the date to start getting emails from, in epochs ms
    :return: list of messages (gmail message schema)

    Updates START_STAMP after
    """
    # List unread messages ids
    results = (service.users().messages().list(userId='me', maxResults=10).
               execute())
    message_ids = results.get('messages', [])

    messages = []
    if not message_ids:
        return []

    # get the actual messages from ids
    global START_STAMP
    flag = False
    for message in message_ids:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        internalDate = msg.get('internalDate', '')
        if internalDate:
            if int(internalDate) >= START_STAMP or alltime:
                if DEBUG: print("get_latest_emails: found msg")
                flag=True
                messages.append(msg)
    if flag: START_STAMP = time.time_ns() // 1_000_000
    return messages


def decode_base64url(data):
    # Base64url might miss padding, so fix it
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)

    decoded_bytes = base64.urlsafe_b64decode(data)
    return decoded_bytes.decode('utf-8')  # assume it's UTF-8 text inside

#message: gmail users.messages.get response
def unpack_gmail_message(message):
    payload = message['payload']
    #mime types: text/plain, text/html
    if payload['mimeType'] == 'text/plain' and (res := payload['body'].get('data','')):
        return res
    if 'parts' not in payload: return ''
    for part in payload['parts']:
        if part['mimeType'] == 'text/plain' and (res := part['body'].get('data','')):
            return res
    return ''

def decode_messages(messages):
    decoded_messages = []
    for message in messages:
        decoded_messages.append(decode_base64url(unpack_gmail_message(message)))
    return decoded_messages

