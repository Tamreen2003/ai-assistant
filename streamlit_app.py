import streamlit as st
import google.generativeai as genai

# 1. Config & Security
st.set_page_config(page_title="Sara AI", page_icon="⚜️", layout="wide")

# Check if secret exists before configuring
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Missing GOOGLE_API_KEY in Streamlit Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Use 'gemini-1.5-flash' explicitly
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Model Initialization Error: {e}")
    st.stop()

# 2. Luxury UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #D4AF37; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #D4AF37; }
    .stChatMessage { border: 1px solid #D4AF37; border-radius: 10px; background: rgba(212, 175, 55, 0.05); }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar - The 3D Avatar Placeholder
with st.sidebar:
    st.markdown("<h2 style='color: #D4AF37; text-align: center;'>SARA</h2>", unsafe_allow_html=True)
    # This is a high-end avatar placeholder for now
    st.components.v1.iframe("https://readyplayer.me/avatar", height=500)
    st.info("Status: Logic Auditor Online")

# 4. The Challenger Logic
st.title("⚜️ Sara: Luxury Logic Auditor")
st.caption("Dubai Intelligence | 2026 Logic Engine")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("State your proposition..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # The Challenger Prompt
        full_prompt = f"System: You are Sara, a high-end luxury logic auditor. Challenge the user's reasoning if it is weak, then provide a sophisticated, concierge-level solution. Input: {prompt}"
        
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        
        # Voice Trigger (Simple)
        js_speech = f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance(`{response.text[:200]}`));</script>"
        st.components.v1.html(js_speech, height=0)
        
    st.session_state.messages.append({"role": "assistant", "content": response.text})
