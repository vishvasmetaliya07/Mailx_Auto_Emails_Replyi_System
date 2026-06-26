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
