import streamlit as st
import requests

# FastAPI Backend URL
API_URL = "http://127.0.0.1:8000/ask"

# Set page title and layout
st.set_page_config(page_title="DevOps Chatbot", layout="centered")

# Title and description
st.title("🤖 DevOps Chatbot")
st.write("Ask anything about DevOps!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 🚀 User input field
user_input = st.chat_input("Type your question here...")

if user_input:
    # Store user message in session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # API Call
    response = requests.get(API_URL, params={"question": user_input}).json()
    
    # Extract bot response
    bot_response = response.get("response", "Sorry, I didn't understand that.").strip()

    # Store bot response in session state
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.chat_message("assistant").write(bot_response)

    # 🚀 Streamlit automatically refreshes after receiving input, no need for manual rerun
