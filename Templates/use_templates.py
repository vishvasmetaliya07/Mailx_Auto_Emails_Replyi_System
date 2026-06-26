TEMPLATES = {
    "complaint":
        """We’re sorry for the inconvenience you’ve experienced. 
        Your concern has been noted, and our team is reviewing it carefully. 
        We will update you as soon as possible.""",

    "service_issue":
        """Thank you for bringing this to our attention.
          We are currently looking into the service issue 
          and will keep you informed of any updates.""",

    "connectivity_issue":
        "We understand the connectivity problem you are facing. Our technical team is investigating the issue to restore normal service at the earliest.",

    "it_support":
        "Thank you for reporting the technical issue. Our IT support team has been notified and is working to resolve the problem.",

    "leave_request":
        """Your leave request has been received.\nIt is currently under review, and you will be informed once a decision has been made.""",

    "salary_query":
        """We have received your salary-related query and are verifying the details.\nOur payroll team will get back to you shortly.""",

    "account_issue":
        "We understand you are experiencing account access issues. Our support team is reviewing the matter and will assist you as soon as possible.",

    "support_request":
        "Thank you for reaching out. Our support team has received your request and will assist you shortly.",

    "general_question":
        "Thank you for your message. We have noted your question and will provide the relevant information soon.",

    "personal_advice":
        "Thank you for sharing your concern. While we review your message, we’ll do our best to provide helpful guidance shortly.",

    "general_query":
        "Thank you for checking in. We are reviewing your request and will share an update as soon as possible.",

    "positive_feedback":
        "Thank you for your kind feedback. We truly appreciate your support and are glad to hear about your positive experience."
}



def templates(intent):
    if intent in TEMPLATES:
        mail=TEMPLATES[intent]
        mail +="\nBest Regards,\nSupport Team"
        print(mail)
        
    else:
        print("Please AI Throgh Genrate Them")
    return mail


# templates("account_issue","Hello my salary was creadited at half of month")

        
    