# from langchain_community.chat_models import ChatOllama
# from langchain_core.prompts import ChatPromptTemplate
# import warnings
# from send_gmail.main import send_gmail

# warnings.filterwarnings("ignore")

# llm = ChatOllama(
#     model="qwen2.5:3b",
#     temperature=0.2
# )

# # # Prompt template
# # prompt = ChatPromptTemplate.from_messages([
# #     ("system", " If the user's Ask To genrate email then genrate emails but if user ask to reply genrator then reply genrate . Write only the reply body. Do not include subject, greeting, or signature."),
# #     ("human", "{email}")
# # ])
# prompt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         "You are an email assistant. "
#         "If the user input looks like an incoming email that needs a response, write a reply, reply generate. "
#         "If the user input is a request to write an email, generate a new email, generate email, create an email. "
#         "Write only the reply in the email body if the user is replying to an email. "
#         "Do not include subject, greeting, or signature."
#     ),
#     ("human", "{email}")
# ])



# # Chain
# chain = prompt | llm

# def chatbot_ollam(email):
#     # Invoke
#     response = chain.invoke({
#         "email": email
#     })

#     # print("AI Reply:\n")
#     return response.content

# # while True:
# #     user=input("user:")
# #     if user.lower() in ["exit","quit"]:
# #         break
# #     elif user.lower in ["send email","send gmail","send mail","to send"]:
# #         send_u=input("Can you send email yes or no")
# #         if send_u.lower() in "yes":
# #             send_gmail()
# #     else:
# #          chatbot_ollam(user)


from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Initialize model once (IMPORTANT)
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0.2,
    streaming=True
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You ONLY write the plain text BODY of an email reply.
You NEVER write anything else.

Forbidden things (never output them):
- subject
- Dear
- Hi
- Hello
- Regards
- Thanks
- signature
- name
- phone
- email
- closing line
- markdown
- explanation

Rules:
1. Read the email carefully.
2. Write ONLY reply paragraphs.
3. Professional & polite.
4. Answer all important points.
5. Raw text only."""
    ),
    ("human", "{email}")
])

chain = prompt | llm


def genrator(email: str):
    """
    Generator function
    Yields tokens one by one
    """
    for chunk in chain.stream({"email": email}):
        yield chunk.content
