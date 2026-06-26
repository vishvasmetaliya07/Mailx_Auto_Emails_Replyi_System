api_key=""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
# from api import apikey
import os, json


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    openai_api_key=api_key
)


# prompt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         "You are an email assistant. "
#         "If the input is an incoming email, write a reply. "
#         "If the input asks to write a new email, generate it. "
#         "Write only the email body. "
#         "Do not include subject, greeting, or signature."
#     ),
#     ("human", "{email}")
# ])

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a concise and professional email assistant.

Rules:
- If the input looks like a RECEIVED EMAIL (someone wrote to you) → write **only the body** of a polite reply
- If the input is a request like "write an email to...", "compose email...", "draft email..." → write a complete new email (including subject if appropriate)
- Do NOT add greetings ("Dear...", "Hi..."), closings ("Best regards", "Sincerely") or signatures unless the user explicitly asks for them
- Keep language clear, short and business-like
- Never explain your answer — output only the email text"""
    ),
    ("placeholder", "{history}"),
    ("human", "{text}"),
])


base_chain = prompt | llm

# -------------------------
# FILE MEMORY
# -------------------------
MEMORY_DIR = "memory"
os.makedirs(MEMORY_DIR, exist_ok=True)

store = {} 

def load_history(session_id):
    history = ChatMessageHistory()
    file_path = os.path.join(MEMORY_DIR, f"{session_id}.json")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            messages = json.load(f)
            for m in messages:
                history.add_message(m)

    return history


def save_history(session_id, history):
    file_path = os.path.join(MEMORY_DIR, f"{session_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
           [m.model_dump() for m in history.messages],
            f,
            ensure_ascii=False,
            indent=2
        )


def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = load_history(session_id)
    return store[session_id]


chain = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="text",
    history_messages_key="history"

)


def generate(text, session_id="user1"):
    response = chain.invoke(
        {"text": text},
        config={"configurable": {"session_id": session_id}}
    )

    save_history(session_id, store[session_id])

    return response.content




# while True:
#     user=input("user:")
#     if user.lower() in ["exit","quit"]:
#         break
#     res=generate(user)
#     print(res)
    