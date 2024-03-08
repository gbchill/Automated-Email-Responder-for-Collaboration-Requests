
import spacy
from textblob import TextBlob
from datetime import datetime
import random

nlp = spacy.load("en_core_web_sm")

max_profile = {
    "name": "Max Grabel",
    "contact_email": "maxgrabelbusiness@gmail.com",
    "profession": "DJ & Music Creator",
    "bio": "Originally a celebrated Live DJ from Michigan, Max skillfully pivoted to the digital world amidst COVID-19.",
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
        "cpm_rate": {"min": 500, "max": 20000},
        "ugc_rate": {"1_video": 2600, "2_videos": 4100, "3_videos": 5600},
        "usage_rights": {"3_months": 550, "6_months": 700, "1_year_plus": 1100},
    },
    "do_not_accept": ["non-paid deals"],
}

def analyze_email_content(email_text):
    doc = nlp(email_text)
    organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    collaboration_mentions = any(word in doc.text.lower() for word in ["collaborate", "partnership", "sponsorship", "affiliate"])
    product_mentions = any(ent.label_ == "PRODUCT" for ent in doc.ents)
    questions = [sent.text for sent in doc.sents if sent.text.endswith('?')]
    tone = TextBlob(email_text).sentiment.polarity
    urgency = "urgent" if "urgent" in email_text.lower() or "asap" in email_text.lower() or "immediately" in email_text.lower() else "normal"
    
    return {
        "organizations": organizations,
        "dates": dates,
        "collaboration_mentions": collaboration_mentions,
        "product_mentions": product_mentions,
        "questions": questions,
        "tone": "positive" if tone > 0 else "negative" if tone < 0 else "neutral",
        "urgency": urgency,
    }

def process_email(email_text):
    analyzed_content = analyze_email_content(email_text)
    is_paid = any(word in email_text.lower() for word in ["payment", "commission", "paid", "sponsor", "rates", "fee"])
    greeting = "Good morning" if 5 <= datetime.now().hour < 12 else "Good afternoon" if 12 <= datetime.now().hour < 18 else "Good evening"
    responses = [
        "{greeting},\n\nThank you for reaching out with your proposal.",
        "{greeting},\n\nThanks for your interest in a collaboration.",
        "{greeting},\n\nAppreciate your message and the opportunity to collaborate.",
    ]
    response = random.choice(responses).format(greeting=greeting)
    response += f" It's great to hear from {', '.join(analyzed_content['organizations'])}." if analyzed_content['organizations'] else ""
    response += f" I'm intrigued by the proposal for {', '.join(analyzed_content['dates'])}." if analyzed_content['dates'] else ""
    if is_paid:
        response += " We're open to discussing paid partnerships."
        if analyzed_content['product_mentions']:
            response += " While I note the product-related discussion, I'm more inclined towards direct collaborations."
        if analyzed_content['questions']:
            response += f" Also, you asked: {'; '.join(analyzed_content['questions'])} - let's address these."
        response += f" Max's standard rates are as follows: ${max_profile['rates']['flat_rate']['1_video']} for one video."
    else:
        response += " However, we generally don’t proceed with non-paid collaborations as per Max's current policies."
    if analyzed_content['urgency'] == "urgent":
        response += "\n\nI understand the urgency and will get back to you as soon as possible."
    else:
        response += "\n\nLooking forward to your thoughts and more details."
    response += f"\n\nBest regards,\n{max_profile['name']}\n{max_profile['contact_email']}"
    return response
