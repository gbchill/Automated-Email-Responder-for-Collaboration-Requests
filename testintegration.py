import base64
import os
import spacy
from textblob import TextBlob
from datetime import datetime
import random
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText

# Define the scope of the application
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    """
    Authenticates the user and creates a Gmail API service.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def create_message(sender, to, subject, message_text):
    """
    Create a message for an email.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    """
    Send an email message.
    """
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def get_label_id(service, label_name):
    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        for label in labels:
            if label['name'].lower() == label_name.lower():
                return label['id']
    except Exception as e:
        print(f'An error occurred: {e}')
    return None

def process_incoming_emails(service, label_id):
    try:
        response = service.users().messages().list(userId='me', labelIds=[label_id]).execute()
        messages = response.get('messages', [])

        processed_emails = []
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            # You might need to parse the body differently depending on the email structure
            body = get_email_body(txt)  # Assuming you have or will create this function to extract the body

            email_data = {
                'id': msg['id'],
                'subject': next((header['value'] for header in txt['payload']['headers'] if header['name'] == 'Subject'), "No Subject"),
                'from': next((header['value'] for header in txt['payload']['headers'] if header['name'] == 'From'), "Unknown"),
                'body': body
            }
            processed_emails.append(email_data)

        return processed_emails
    except Exception as e:
        print(f'An error occurred: {e}')
        return []

def main():
    service = authenticate_gmail()
    label_id = get_label_id(service, 'AERCR')  # Name of your specific label
    if label_id:
        processed_emails = process_incoming_emails(service, label_id)
        for email in processed_emails:
            # Use the email body and subject to generate a response
            response_body = process_email(email['body'])  # Assume process_email generates a response based on the body
            send_message(service, 'me', create_message('your-email@gmail.com', email['from'], 'Re: ' + email['subject'], response_body))
            # Optional: Remove the email from 'AERCR' label after responding (or mark as read)
            service.users().messages().modify(userId='me', id=email['id'], body={'removeLabelIds': ['UNREAD', label_id]}).execute()
    else:
        print("Label not found.")

if __name__ == '__main__':
    main()
