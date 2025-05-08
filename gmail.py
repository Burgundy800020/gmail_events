from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def init_gmail(token_path):
    creds = Credentials.from_authorized_user_file(token_path,
                                                  ['https://www.googleapis.com/auth/gmail.readonly'])

    # Build the Gmail service
    return build('gmail', 'v1', credentials=creds)


def get_latest_emails(service):
    # List unread messages
    results = (service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=10).
               execute())
    message_ids = results.get('messages', [])

    messages = []
    if not message_ids:
        return []

    for message in message_ids:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        messages.append(msg)

    return messages


import base64
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

