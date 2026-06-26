from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
# from get_all_un_read_mail import get_all_unread_emails

import pickle
# import gmail_classyfiler as gm

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def gmail_authenticate():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service

gmail_authenticate()

import re

def rule_based_email_filter(sender: str, subject: str, body: str):

    text = f"{sender} {subject} {body}".lower()
    sender_blacklist = [
        "noreply",
        "no-reply",
        "newsletter",
        "alerts",
        "updates",
        "notification"
    ]

    if any(word in sender.lower() for word in sender_blacklist):
        return True

    keyword_blacklist = [
        "unsubscribe",
        "view job",
        "manage alerts",
        "read more",
        "privacy policy",
        "terms and conditions",
        "click here",
        "apply now",
        "follow us"
    ]

    if any(keyword in text for keyword in keyword_blacklist):
        return True

    urls = re.findall(r"http[s]?://", body)
    if len(urls) > 3:
        return True

    if len(body.split()) > 500:
        return True

    html_markers = ["<html", "<body", "<a href", "<div", "<table"]
    if any(tag in body.lower() for tag in html_markers):
        return True
    return False

import base64

def get_unread_emails(service):
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=5
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        headers = msg_data["payload"]["headers"]
        subject = sender = ""

        for h in headers:
            if h["name"] == "Subject":
                subject = h["value"]
            if h["name"] == "From":
                sender = h["value"]

        body = ""
        parts = msg_data["payload"].get("parts", [])
        for part in parts:
            if part["mimeType"] == "text/plain":
                body = base64.urlsafe_b64decode(
                    part["body"]["data"]
                ).decode("utf-8")

        emails.append({
            "id": msg["id"],
            "threadId": msg_data["threadId"],
            "from": sender,
            "subject": subject,
            "body": body
        })

    return emails

service = gmail_authenticate()
emails = get_unread_emails(service)


 
def process_emails(email_list):
    user_emails = []
    blocked_emails = []

    for email in email_list:
        sender = email["from"]
        subject = email["subject"]
        body = email["body"]

        if rule_based_email_filter(sender, subject, body):
            blocked_emails.append(email)
        else:
            user_emails.append(email)

    return user_emails, blocked_emails



# allowed_emails, ignored_emails = process_emails(emails)
# print("✅ User Emails (Process Further):", len(allowed_emails))
# for email in allowed_emails:
#     # email["from"]
#     print(email["body"])
 

# def fillter(allowed_emails, ignored_emails ):



#     print("\n🚫 Auto Emails (Ignored):", len(ignored_emails))
#     for email in ignored_emails:
#         print(email["from"])

# 