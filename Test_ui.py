import streamlit as st
import subprocess
# from chatbot import chatbot_generate
from Test_ollama import genrator

st.set_page_config(
    page_title="AI Email Auto Reply",
    layout="wide"
)


st.title("📧 AI Email Auto Reply System")
st.caption("Automatic + Chatbot-based email replies")


st.subheader("🔄 Auto Reply (Unread Emails)")

if st.button("🚀 Auto Reply Now"):
    with st.spinner("Replying to unread emails..."):
        subprocess.run(["python", "auto_reply.py"])
    st.success("✅ Replies sent successfully!")

st.divider()


st.subheader("🤖 Email Reply Chatbot")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input(
    "Type email message here...",
    placeholder="Example: Where is my salary?"
)
import time

if st.button("Generate Reply"):
    if user_input.strip():

        st.session_state.chat.append(("You", user_input))

        placeholder = st.empty()
        full_reply = ""

        for token in genrator(user_input):
            for char in token:
                full_reply += char
                placeholder.markdown(f"🤖 **Bot:** {full_reply}")

                # ⏱️ Human-like delay tuning
                if char in [".", ",", "!", "?"]:
                    time.sleep(0.12)   # pause at punctuation
                elif char == " ":
                    time.sleep(0.03)   # tiny pause at space
                else:
                    time.sleep(0.015)  # normal typing speed

        st.session_state.chat.append(("Bot", full_reply))



for sender, msg in st.session_state.chat:
    if sender == "You":
        st.markdown(f"🧑 **You:** {msg}")
    else:
        st.markdown(f"🤖 **Bot:** {msg}")

# import streamlit as st
# import subprocess
# import uuid
# from auto_reply import auto_reply
# from ollama_with_memory import generate
# # from Test_lang import genrate

# st.set_page_config(page_title="AI Email Assistant", layout="wide")

# st.title("📧 AI Email Assistant")
# st.caption("ChatGPT-like Email Reply Generator")


# st.subheader("🔄 Auto Reply (Unread Emails)")

# if st.button("🚀 Auto Reply Now"):
#     with st.spinner("Replying to unread emails..."):
#          auto_reply()
#     st.success("✅ Replies sent successfully!")

# st.divider()

# # ---------------- ChatGPT-like Chatbot ----------------
# st.subheader("Emails Chatbot")
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "session_id" not in st.session_state:
#     st.session_state.session_id = str(uuid.uuid4())

# # Show chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])


# user_input = st.chat_input("Paste or type an email here...")

# if user_input:
 
#     st.session_state.messages.append({
#         "role": "user",
#         "content": user_input
#     })
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # Generate bot reply
#     with st.chat_message("assistant"):
#         with st.spinner("Generating reply..."):
#             bot_reply = generate(user_input, st.session_state.session_id)
#             st.markdown(bot_reply)

#     # Save assistant message
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": bot_reply
#     })
