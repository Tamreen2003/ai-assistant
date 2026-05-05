import streamlit as st
import google.generativeai as genai

# --- 1. SETTINGS ---
st.set_page_config(page_title="SARA AI", layout="wide", page_icon="⚜️")

# Luxury Dubai Styling
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #D4AF37; }
    .stChatMessage { border: 1px solid #D4AF37; border-radius: 15px; background: rgba(212, 175, 55, 0.05); }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE BRAIN ---
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("❌ Key Missing in Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Use the 2026 Stable Model
# Change this to 'gemini-1.5-flash' only if 2.5 is not in your region yet
MODEL_NAME = 'gemini-2.5-flash' 

try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception:
    # Fail-safe: Try the older model name if the new one isn't active
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. THE UI ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>SARA</h1>", unsafe_allow_html=True)
    st.components.v1.iframe("https://readyplayer.me/avatar", height=400)
    st.info("Logic Engine: 2026 v3.1")

st.title("⚜️ Sara: Luxury Logic Auditor")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. THE INTERACTION ---
if prompt := st.chat_input("State your proposition..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Luxury Auditor Instructions
            persona = "You are Sara, a high-end luxury logic auditor. Challenge the user's reasoning with Dubai-style sophistication. Be concise."
            
            response = model.generate_content([persona, prompt])
            st.markdown(response.text)
            
            # Siri-Style Voice (Zero Cost)
            js_speech = f"""
            <script>
            var msg = new SpeechSynthesisUtterance('{response.text[:300].replace("'", "")}');
            window.speechSynthesis.speak(msg);
            </script>
            """
            st.components.v1.html(js_speech, height=0)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.write("Checking available models for you...")
            # This helps us see what models YOU have access to
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            st.write(f"Try one of these names in the code: {available_models}")
