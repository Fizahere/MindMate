import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("api_key")
# Initialize Gemini client with your provided key
client = genai.Client(api_key=api_key)

# Setup chat on first load
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a psychologist and friendly companion. Design for single personal use. remember user's context and history. If you don't know anything about user just ask for it. Be gentle and supportive. Don't let user know that you are an AI.",
            temperature=0.5,
            max_output_tokens=150,
        )
    )

# Store message history for UI display
if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="Psychologist Chat", page_icon="🧠")
st.title("🧠 Talk to a Psychologist")

st.markdown("_This AI psychologist remembers what you share and supports you gently._")

# Display conversation
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# Input box for user message
user_input = st.chat_input("How are you feeling?")

if user_input:
    # Show user message
    st.session_state.history.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send to Gemini
    response = st.session_state.chat.send_message(user_input)
    bot_reply = response.text

    # Show bot reply
    st.session_state.history.append({"role": "model", "text": bot_reply})
    with st.chat_message("model"):
        st.markdown(bot_reply)

# # Optional: Debug history from Gemini backend
# with st.expander("🔍 Full Model History"):
#     for msg in st.session_state.chat.get_history():
#         st.markdown(f"**{msg.role.capitalize()}**: {msg.parts[0].text}")
