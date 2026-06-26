import re
import gmail_collect.gmail as gm
from intent_classified.model.test import predict_intents_list
from Test_lang import genrate
from Templates.use_templates import templates
from send_gmail.main import send_gmail


def extract_email(from_field: str):
    match = re.search(r'<([^>]+)>', from_field)
    return match.group(1) if match else None


def get_selected_emails():
    """Fetch unread and allowed emails only (NO reply here)."""

    service = gm.gmail_authenticate()
    emails = gm.get_unread_emails(service)
    allowed_emails, _ = gm.process_emails(emails)

    email_data = []

    for email in allowed_emails:
        sender = extract_email(email.get("from", ""))
        subject = email.get("subject", "").strip()
        body = email.get("body", "").strip()

        if sender and (subject or body):
            combined_text = f"{subject} {body}".strip()

            email_data.append({
                "sender": sender,
                "subject": subject,
                "body": body,
                "text": combined_text,
                "thread_id": email.get("threadId"),
                "message_id": email.get("id"),
                "cc": email.get("cc", "")
            })

    return email_data

def auto_reply(email_data):
    log = []

    for email in email_data:
        sender = email["sender"]
        thread_id = email["thread_id"]
        reply_mode = email.get("reply_mode", "Reply")

        intent = predict_intents_list([email["text"]])[0]

        if intent == "other":
            reply = genrate(email["text"])
        else:
            reply = templates(intent)

        if "Best Regards" not in reply:
            reply += "\n\nBest Regards,\nAI Support Team"

        send_gmail(reply, sender, thread_id=thread_id)

        log.append({
            "sender": sender,
            "intent": intent,
            "reply":reply,
            "mode": reply_mode,
            "status": "sent"
        })

    return log

