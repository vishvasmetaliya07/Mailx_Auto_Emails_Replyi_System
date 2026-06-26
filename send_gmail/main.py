# import base64
# from email.message import EmailMessage
# from googleapiclient.discovery import build

# import pickle

# SCOPES=['https://www.googleapis.com/auth/gmail.send']

# with open("token.pickle","rb") as file:
#     creds=pickle.load(file)


# service=build('gmail','v1',credentials=creds)


# def send_gmail(body,to,subject="Auto Emails Reply "):
#     msg=EmailMessage()
#     msg.set_content(body)
#     msg['To']=to
#     msg['From']="me"
#     msg['subject']=subject


#     encode=base64.urlsafe_b64encode(msg.as_bytes()).decode()



#     #send Emails


#     service.users().messages().send(
#         userId='me',
#         body={'raw': encode}
#     ).execute()

#     print("✅ Email sent")

import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

with open("token.pickle", "rb") as file:
    creds = pickle.load(file)

service = build('gmail', 'v1', credentials=creds)


def send_gmail(body, to, subject="Auto Emails Reply", thread_id=None):

    msg = EmailMessage()
    msg.set_content(body)
    msg['To'] = to
    msg['From'] = "me"
    msg['Subject'] = subject

    encoded = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    message = {
        'raw': encoded
    }

    if thread_id:
        message['threadId'] = thread_id

    service.users().messages().send(
        userId='me',
        body=message
    ).execute()

    print("✅ Email sent")
