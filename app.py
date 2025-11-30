import streamlit as st
import os
from google import genai

# --- Configuration & Initialization ---

# 1. Page Setup
st.set_page_config(page_title="The Gemini AI Chatbot", layout="wide")
st.title("🤖 Your Gemini Chatbot")

# 2. API Key Check & Client Initialization
# This code securely retrieves the API key from Streamlit Secrets during deployment
# or from the environment variable during local testing.
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except (AttributeError, KeyError):
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("API Key not found. Please set GEMINI_API_KEY in your environment or Streamlit secrets.")
    st.stop()

# Initialize the Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# System Instruction (Personality)
SYSTEM_INSTRUCTION = (
    "You are a friendly and informative AI assistant. "
    "Your goal is to have a helpful, multi-turn conversation with the user, "
    "and always maintain a positive and curious tone."
)

# 3. Initialize Chat History in Streamlit Session State
# This ensures the chatbot remembers the conversation history.
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model=MODEL_NAME, 
        system_instruction=SYSTEM_INSTRUCTION
    )

# --- Display Conversation ---

# Retrieve and display all past messages
for message in st.session_state.chat.get_history().contents:
    # Map API roles to Streamlit UI roles
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# --- User Input and Response Generation ---

if prompt := st.chat_input("Ask Gemini a question..."):
    # Display the user's message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send message to the Gemini API and stream the response
    with st.chat_message("assistant"):
        # The 'stream=True' setting provides real-time output (better user experience)
        response_stream = st.session_state.chat.send_message(prompt, stream=True)
        # Display the streamed response chunk by chunk
        st.write_stream(response_stream)
