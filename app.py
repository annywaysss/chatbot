import streamlit as st
from nlp_utils import extract_keywords, extract_entities, extract_user_details
from pathway_genai import get_pathway_console_output
from memory import update_memory, get_user_memory
import json
import os

st.set_page_config(page_title=" AI Financial chatbot")
st.title("AI-Powered Financial Support Chatbot")
st.write("Ask me anything related to finance,banking or investments!")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("you:", placeholder="type your financial query here...")

USER_ID = 1  

if st.button("Ask") and user_input.strip():
    keywords = extract_keywords(user_input)
    entities = extract_entities(user_input)
    user_details = extract_user_details( user_input,USER_ID)

    for key, value in user_details.items():
        update_memory(user_id=1, key=key, value=value)
    
    memory = get_user_memory(USER_ID)
    
   
    bot_reply = get_pathway_console_output(1,user_input)
    
    st.session_state.history.append({
        "user": user_input,
        "bot": bot_reply,
        "keywords": keywords,
        "entities": entities,
        "memory_snapshot": memory
    })

if st.session_state.history:
    st.markdown("### 🗨 Conversation")
    for msg in st.session_state.history:
        st.markdown(f"**You:** {msg['user']}")
        st.markdown(f"**Bot:** {msg['bot']}")
        if msg["keywords"]:
            st.markdown(f"🔍 Keywords: {', '.join(msg['keywords'])}")
        if msg["entities"]:
            st.markdown(f"🏷 Entities: {msg['entities']}")
        if msg["memory_snapshot"]:
            st.markdown(f"💾 Memory: {msg['memory_snapshot']}")
        st.markdown("---")


if st.button("Save Conversation"):
    with open("chat_history.json", "w") as f:
        json.dump(st.session_state.history, f, indent=2)
    st.success("✅ Chat history saved successfully!")
if os.path.exists("chat_history.json"):
    with open("chat_history.json", "r") as f:
        chat_data = f.read()
    st.download_button(
        label="Download Chat History",
        data=chat_data,
        file_name="chat_history.json",
        mime="application/json"
    )


if os.path.exists("user_memory.json"):
    with open("user_memory.json", "r") as f:
        memory_data = f.read()
    st.download_button(
        label="Download User Memory",
        data=memory_data,
        file_name="user_memory.json",
        mime="application/json"
    )
if st.button("Reset Chat"):
    st.session_state.history = []
    st.stop()
