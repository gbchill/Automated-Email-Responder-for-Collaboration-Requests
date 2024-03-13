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

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

# Profile information template
max_profile = {
    "name": "Max Grabel",
    "contact_email": "maxgrabelbusiness@gmail.com",
    "profession": "DJ & Music Creator",
    "bio": "Originally a celebrated Live DJ from Michigan, Max skillfully pivoted to the digital world amidst COVID-19. He rapidly grew a loyal following in the millions on TikTok, Instagram, and YouTube by sharing unique mixes and top song reviews, posting 4-6 times weekly.",
    "interests": ["DJ", "Music Creation"],
    "availability": "Open to new collaborations",
    "statistics": {
        "tiktok_followers": 3.1e6,
        "gender_demographic": "63% Men",
        "engagement_rate": 28.9,
        "weekly_reach": 9.1e6,
    },
    "rates": {
        "flat_rate": {"1_video": 2900, "2_videos": 4700, "3_videos": 6500},
        "additional_platform_rate": 1.5,
        "cpm_rate": {"min": 500, "max": 20000, "1_video": 10, "2_videos": 8, "3_videos": 5},
        "ugc_rate": {"1_video": 2600, "2_videos": 4100, "3_videos": 5600},
        "usage_rights": {"3_months": 550, "6_months": 700, "1_year_plus": 1100},
    },
    "do_not_accept": ["non-paid deals"],
}

# Analyze email content
def analyze_email_content(doc):
    organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    collaboration_mentions = any(word in doc.text.lower() for word in ["collaborate", "partnership", "sponsorship", "affiliate"])
    product_mentions = any(ent.label_ == "PRODUCT" for ent in doc.ents)
    questions = [sent.text for sent in doc.sents if sent.text.endswith('?')]
    tone = TextBlob(doc.text).sentiment.polarity 
    urgency = "urgent" if "urgent" in doc.text.lower() or "asap" in doc.text.lower() or "immediately" in doc.text.lower() else "normal"
    
    return {
        "organizations": organizations,
        "dates": dates,
        "collaboration_mentions": collaboration_mentions,
        "product_mentions": product_mentions,
        "questions": questions,
        "tone": "positive" if tone > 0 else "negative" if tone < 0 else "neutral",
        "urgency": urgency,
    }

# Process email
def process_email(email_text):
    doc = nlp(email_text)
    analyzed_content = analyze_email_content(doc)
    is_paid = any(word in email_text.lower() for word in ["payment", "commission", "paid", "sponsor", "rates", "fee"])

    # Personalized greeting based on the time of day
    greeting = "Good morning" if 5 <= datetime.now().hour < 12 else "Good afternoon" if 12 <= datetime.now().hour < 18 else "Good evening"

    # Start of the response with variability
    responses = [
        f"{greeting},\n\nThank you for reaching out with your proposal.",
        f"{greeting},\n\nThanks for your interest in a collaboration.",
        f"{greeting},\n\nAppreciate your message and the opportunity to collaborate.",
    ]
    response = responses[random.randint(0, len(responses) - 1)]  # Randomly select an opening line
    
    response += f" It's great to hear from {', '.join(analyzed_content['organizations'])}." if analyzed_content['organizations'] else ""
    response += f" I'm intrigued by the proposal for {', '.join(analyzed_content['dates'])}." if analyzed_content['dates'] else ""

    # Personalized body based on email analysis
    if is_paid:
        response += " We're open to discussing paid partnerships."
        if analyzed_content['product_mentions']:
            response += " While I note the product-related discussion, I'm more inclined towards direct collaborations that align with my interests in DJing and music creation."
        if analyzed_content['questions']:
            response += f" Also, you asked: {'; '.join(analyzed_content['questions'])} - let's address these."
        response += f" Max's standard rates are as follows: ${max_profile['rates']['flat_rate']['1_video']} for one video. Detailed rates depend on collaboration specifics."
    else:
        response += " However, we generally don’t proceed with non-paid collaborations as per Max's current policies."

    # Personalized closing based on the tone and urgency
    if analyzed_content['urgency'] == "urgent":
        response += "\n\nI understand the urgency and will get back to you as soon as possible."
    else:
        response += "\n\nLooking forward to your thoughts and more details."

    response += f"\n\nBest regards,\n{max_profile['name']}\n{max_profile['contact_email']}"

    return response

# Authenticate and create Gmail API service
def authenticate_gmail():
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


# Create email message
def create_message(sender, to, message_text):
    # Default subject line - you can change this to anything you like
    subject = "Max Grabel: Response to Your Collaboration Inquiry"  # Change this subject as needed
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


# Send email message
# Send email message
# Modify the send_message function to accept the recipient's email address
def send_message(service, user_id, message, recipient_email):
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        # Decode the email's body for printing
        decoded_message_text = base64.urlsafe_b64decode(message['raw'].encode('ASCII')).decode('utf-8')
        print(f"Email successfully sent to {recipient_email}.")
        print(f"Email details:\n{decoded_message_text}")
        return sent_message
    except HttpError as error:
        print(f'An error occurred while sending the email: {error}')
        return None



# Get label ID
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

# Extract plain text from message parts
def get_plain_text_from_message_parts(parts, base64_url=False):
    plain_text = ""
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                if base64_url:
                    plain_text += base64.urlsafe_b64decode(part['body']['data'].encode("ASCII")).decode("utf-8")
                else:
                    plain_text += part['body']['data']
            elif 'parts' in part:
                plain_text += get_plain_text_from_message_parts(part['parts'], base64_url)
    return plain_text

# Process incoming emails
def process_incoming_emails(service, label_id):
    try:
        response = service.users().messages().list(userId='me', labelIds=[label_id]).execute()
        messages = response.get('messages', [])

        processed_emails = []
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            payload = txt['payload']
            body = ''
            if 'parts' in payload:
                body = get_plain_text_from_message_parts(payload['parts'], base64_url=True)
            elif payload['mimeType'] == 'text/plain':
                body = base64.urlsafe_b64decode(payload['body']['data'].encode("ASCII")).decode("utf-8")

            email_data = {
                'id': msg['id'],
                'subject': next((header['value'] for header in payload['headers'] if header['name'] == 'Subject'), "No Subject"),
                'from': next((header['value'] for header in payload['headers'] if header['name'] == 'From'), "Unknown"),
                'body': body
            }
            processed_emails.append(email_data)

        return processed_emails
    except Exception as e:
        print(f'An error occurred: {e}')
        return []

# Main script logic
# Main script logic
def main():
    service = authenticate_gmail()
    label_id = get_label_id(service, 'AERCR')  # Replace 'AERCR' with your specific label
    if label_id:
        processed_emails = process_incoming_emails(service, label_id)
        for email in processed_emails:
            response_body = process_email(email['body'])  # Use the NLP function to generate response
            # Update the following line to match the new function signature
            message_to_send = create_message(max_profile['contact_email'], email['from'], response_body)
            send_message(service, 'me', message_to_send, email['from'])
    else:
        print("Label not found.")

if __name__ == '__main__':
    main()
