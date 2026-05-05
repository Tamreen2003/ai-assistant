import os
import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Sarah - AI Assistant", layout="wide")

# Initialize
@st.cache_resource
def get_client():
    return InferenceClient(
        "HuggingFaceH4/zephyr-7b-beta",
        token=st.secrets.get("HF_TOKEN", "")
    )

client = get_client()

# Moods
MOOD_PROMPTS = {
    "Professional": "You are Sarah, a Senior DevOps Engineer. Be technical, professional, and solution-focused.",
    "Friendly": "You are Sarah, a friendly assistant. Be warm, casual, and pleasant.",
    "Motivational": "You are Sarah, a motivational coach. Be inspiring and encouraging.",
    "Casual": "You are Sarah, a fun buddy. Be relaxed, witty, and funny.",
    "Empathetic": "You are Sarah, a caring friend. Be supportive and understanding."
}

TASKS = {
    "DevOps": "Help with Docker, Kubernetes, CI/CD",
    "Coding": "Debug code, explain concepts",
    "Learning": "Explain concepts, tutorials",
    "Writing": "Help with emails, documents",
    "Planning": "Create schedules, to-do lists",
    "Problem Solving": "Troubleshoot issues"
}

# UI
st.title("🤖 Sarah - Your Free AI Assistant")
st.markdown("---")

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("🎭 Mood")
    mood = st.radio("Select mood:", list(MOOD_PROMPTS.keys()))
    
    st.subheader("📋 Task")
    task = st.radio("Select task:", ["General"] + list(TASKS.keys()))

with col2:
    st.subheader("💬 Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Input
    if user_input := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        # Generate response
        system_prompt = MOOD_PROMPTS[mood]
        if task != "General":
            system_prompt += f"\n\nYou are helping with: {TASKS[task]}"
        
        messages = [{"role": "system", "content": system_prompt}]
        for msg in st.session_state.messages[:-1]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        try:
            with st.chat_message("assistant"):
                response = ""
                placeholder = st.empty()
                
                for message in client.chat_completion(
                    messages,
                    max_tokens=1024,
                    stream=True
                ):
                    if message.choices[0].delta.content:
                        response += message.choices[0].delta.content
                        placeholder.write(response)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
        
        except Exception as e:
            st.error(f"Error: {str(e)}\n\nMake sure HF_TOKEN is set in secrets!")
