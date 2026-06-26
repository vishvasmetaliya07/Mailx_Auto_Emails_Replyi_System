def get_all_unread_emails(service):
    emails = []
    page_token = None

    while True:
        response = service.users().messages().list(
            userId="me",
            labelIds=["INBOX", "UNREAD"],
            maxResults=20,
            pageToken=page_token
        ).execute()

        messages = response.get("messages", [])
        emails.extend(messages)

        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return emails

import socket
socket.create_connection(("imap.gmail.com", 993), timeout=10)
print("Connected")