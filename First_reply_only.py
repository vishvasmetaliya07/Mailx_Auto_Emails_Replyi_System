import   gmail_collect.gmail as gm
from intent_classified.model.test import predict_intent,preprocess,predict_intents_list
# import gmail_collect.gmail_classyfiler as gm_classy
from Test_lang import genrate
from Templates.use_templates import templates

from send_gmail.main import send_gmail


print("Emails Reading ...")
service = gm.gmail_authenticate()
emails = gm.get_unread_emails(service)
allowed_emails, ignored_emails = gm.process_emails(emails)


text=''' '''
From =''' '''

for email in allowed_emails:
    From+=email.get("from","").strip()
    subject = email.get("subject", "").strip()
    body = email.get("body", "").strip()
    text += f"{subject} {body}\n"   

# for email in allowed_emails:
# text+=f"{email.get('subject','')} {email.get('body','')}\n"


lines=text.split("\n")
lines=[x for x in lines if str(x).strip()]
print(lines)

# text = "where is my salary how long should i wait"
# print(predict_intent(text))


# ['first emails','second emails']
print(lines)
print("Intent finding ...")
value=predict_intents_list(lines)
print(value)
# ['value 1','value 2']

import re

print(value[0])
# print(From)
sendar=re.findall(r'<([^>]+)>',From)
print(sendar)


# if value[0] =="other":
#     print("Genrating...")
#     res=genrate(lines[0])
#     res+="\n\nBest Regards,\nAI Support Team"
#     print(res)
#     print("Sending....")
#     send_gmail(res,sendar[0])
    

# else:
#     print("Template using...")
    
#     resp=templates(value[0])
#     send_gmail(resp,sendar[0])
    

    


