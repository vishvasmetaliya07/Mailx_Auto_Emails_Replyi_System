from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# from api import apikey
import os, json


llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0.2,
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

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a professional and concise email assistant.

Your task is to generate clear, business-appropriate email content.

Rules:
- If the input is a RECEIVED EMAIL, write ONLY the body of a polite and professional reply.
- If the input is a request such as "write an email", "compose an email", or "draft an email", generate a new email and include a subject line only if appropriate.
- Do NOT include greetings (e.g., "Dear", "Hi") or closings (e.g., "Best regards", "Sincerely") unless explicitly requested.
- Do NOT include a signature unless explicitly requested.
- Do NOT apologize.
- Do NOT explain your reasoning.
- Keep the language clear, concise, and professional.
- Output ONLY the email text."""
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
                role = m.get("type")
                content = m.get("content")

                if role == "human":
                    history.add_message(HumanMessage(content=content))
                elif role == "ai":
                    history.add_message(AIMessage(content=content))
                elif role == "system":
                    history.add_message(SystemMessage(content=content))

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


# def generate(text, session_id="user1"):
#     response = chain.invoke(
#         {"text": text},
#         config={"configurable": {"session_id": session_id}}
#     )

#     save_history(session_id, store[session_id])

#     return response.content
def generate(text,session_id="user1"):
    full_text = ""

    for chunk in chain.stream(
        {"text": text},
        config={"configurable": {"session_id": session_id}}
    ):
        full_text += chunk.content
        yield chunk.content   # 👈 streaming token

    save_history(session_id, store[session_id])




# while True:
#     user=input("user:")
#     if user.lower() in ["exit","quit"]:
#         break
#     res=generate(user)
#     print(res)
