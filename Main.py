import streamlit as st
import uuid
import time
from auto_reply import auto_reply, get_selected_emails
from ollama_with_memory import generate

st.set_page_config(
    page_title="AI Email Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📧 AI Auto Email Reply System")

if "selected_emails" not in st.session_state:
    st.session_state.selected_emails = get_selected_emails()

if "processed_ids" not in st.session_state:
    st.session_state.processed_ids = set()

if "auto_reply_logs" not in st.session_state:
    st.session_state.auto_reply_logs = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

with st.sidebar:
    st.markdown("### 📥 Unread Emails")

    available_emails = [
        email for email in st.session_state.selected_emails
        if email.get("message_id") not in st.session_state.processed_ids
    ]

    select_all = st.checkbox("Select All Emails")

    selected_for_reply = []

    if available_emails:

        for index, email in enumerate(available_emails):
            unique_key = email.get("message_id") or email.get("thread_id") or f"email_{index}"

            checked = select_all or st.checkbox(
                f"{email['sender']} | {email['subject']}",
                key=f"select_{unique_key}"
            )

            if checked:
                selected_for_reply.append(email)

            with st.expander(f"View Email - {email['sender']}"):
                st.markdown(f"**Subject:** {email['subject']}")
                st.write(email["body"])


        reply_mode = st.selectbox(
            "Reply Type",
            ["Reply", "Reply All"],
            key="global_reply_mode"
        )

        for email in selected_for_reply:
            email["reply_mode"] = reply_mode

    else:
        st.caption("No new unread emails")


# end of the sider bar
        

    st.divider()

    if st.button("🚀 Run Auto Reply", use_container_width=True):
        if selected_for_reply:
            with st.spinner("Sending replies..."):
                logs = auto_reply(selected_for_reply)
                st.session_state.auto_reply_logs = logs
                for email in selected_for_reply:
                    st.session_state.processed_ids.add(email.get("message_id"))
            st.success("✅ Auto replies completed")
        else:
            st.warning("⚠ Please select at least one email")

    if st.session_state.auto_reply_logs:
        st.divider()
        st.markdown("### 📄 Auto Reply Logs")
        for log in st.session_state.auto_reply_logs:
            with st.expander(f"📧 {log['sender']}"):
                st.markdown(f"""
                **Sender:** `{log['sender']}`  
                **Intent:** `{log['intent']}`  
                **Mode:** `{log.get('mode','Reply')}`  
                **Status:** ✅ Sent
                """)
                st.code(log["reply"], language="markdown")

    if st.button("🔄 Refresh Emails", use_container_width=True):
        st.session_state.selected_emails = get_selected_emails()
        st.session_state.processed_ids = set()
        st.toast("Emails refreshed")

    if st.button("🧹 Clear Logs", use_container_width=True):
        st.session_state.auto_reply_logs = []
        st.toast("Logs cleared")

    if st.button("🧹 Clear Chat bot ", use_container_width=True):
        st.session_state.messages = []
        st.toast("Chat cleared")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("✍️ Enter here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
      
        placeholder = st.empty()
        rendered = ""
    with st.spinner("🤖 Generating reply..."):
        for token in generate(user_input, st.session_state.session_id):
            loading_placeholder = st.empty()
            for char in token:
                rendered += char
                placeholder.markdown(rendered + "▌")
                if char in ".!?":
                    time.sleep(0.15)
                elif char == ",":
                    time.sleep(0.05)
                elif char == " ":
                    time.sleep(0.02)
                else:
                    time.sleep(0.008)
        placeholder.markdown(rendered)

    st.session_state.messages.append({"role": "assistant", "content": rendered})
