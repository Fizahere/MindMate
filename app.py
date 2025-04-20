import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("api_key")
prompt_ai = os.getenv("prompt_ai")
# Initialize Gemini client with your provided key
client = genai.Client(api_key=api_key)

# Setup chat on first load
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=prompt_ai,
            temperature=0.5,
            max_output_tokens=150,
        )
    )

# Store message history for UI display
if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="MindMate - Mental Health Support", page_icon="🧠")
st.title("🧠 Talk to your Psychologist")

# 🌈 Custom Styling
st.markdown("""
<style>
/* Footer */
.footer {
    text-align: center;
    color: #aaa;
    font-size: 0.85rem;
    # margin-top: 27rem;
}
</style>
""", unsafe_allow_html=True)
st.markdown("_Made with soft code and big hugs 💕_")

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

# ☁️ Footer
# st.markdown('<div class="footer">Made with soft code and big hugs 💕</div>', unsafe_allow_html=True)

# # Optional: Debug history from Gemini backend
# with st.expander("🔍 Full Model History"):
#     for msg in st.session_state.chat.get_history():
#         st.markdown(f"**{msg.role.capitalize()}**: {msg.parts[0].text}")
