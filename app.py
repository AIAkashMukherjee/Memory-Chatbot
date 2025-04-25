import streamlit as st
from constant import *
from chatbot import ChatBot
import asyncio,os
import threading

if threading.current_thread() is threading.main_thread():
    if not asyncio.get_event_loop().is_running():
        asyncio.set_event_loop(asyncio.new_event_loop())
else:
    asyncio.set_event_loop(asyncio.new_event_loop())

def main():
    st.set_page_config(page_title="Advanced Chatbot", layout="wide")
    st.title("🧠 Memory-Enhanced AI Chatbot: Your Personal Knowledge Assistant")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = None

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        openai_key = st.text_input("OpenAI API Key", type="password")
      

        if st.button("🚀 Initialize Chatbot"):
          
            st.session_state.chatbot = ChatBot(open_ai_api=openai_key if openai_key else None)
            if openai_key:
                
                st.success("✅ Chatbot initialized using OpenAI 🔥")
            else:
                st.success("Chatbot initialized using Groq 🧠 (default)")    

        st.divider()
        st.header("📄 Upload Document")    

        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        if uploaded_file and st.session_state.chatbot:
    # Use the original filename
            original_filename = uploaded_file.name
            with open(original_filename, "wb") as f:
                f.write(uploaded_file.read())
    
    # Upload the document using the original filename
            st.session_state.chatbot.upload_document(original_filename)
    
    # Optionally, remove the file after processing
            os.remove(original_filename)
    
            st.success("✅ Document indexed successfully.")

    
        st.divider()   
        
        if st.button("Clear Memory"):
            if st.session_state.chatbot:
                st.session_state.chatbot.memory_store.clear_memory()
                st.session_state.messages = []
                st.success("Memory cleared!")    


        # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

     # Chat box
    prompt = st.chat_input("Type your message...")

    if prompt:
        if not st.session_state.chatbot:
            st.error("⚠️ Please initialize the chatbot first.")
            return

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)


        with st.chat_message("assistant"):
            response = st.session_state.chatbot.chat(prompt)
        
        # Display response properly
            st.markdown(response)
        
        # Append assistant's response to the chat history
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
