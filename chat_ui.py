import streamlit as st
import requests

st.set_page_config(page_title="Multi-Agentic Chatbot", layout="centered")

st.title("Multi-Agentic Conversational AI System")
st.markdown("This chatbot integrates LLM (Mixtral via Together AI), RAG-based context retrieval, and CRM memory.")

# Sidebar input for user ID
user_id = st.sidebar.text_input("User ID", value="swetha123", help="Enter your unique user identifier")

# Initialize session history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input field
message = st.text_input("Your message", key="input")

# On send
if st.button("Send"):
    if not message.strip():
        st.warning("Please enter a message.")
    else:
        st.session_state.chat_history.append(("You", message))
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"user_id": user_id, "message": message}
            )
            data = response.json()
            reply = data.get("response", "No response from model.")
            st.session_state.chat_history.append(("Bot", reply))
        except Exception as e:
            st.error(f"Failed to contact backend: {e}")

# Display chat history
st.divider()
for sender, text in reversed(st.session_state.chat_history):
    st.markdown(f"**{sender}:** {text}")
