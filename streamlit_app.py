import streamlit as st
import google.generativeai as genai

# 1. PAGE SETUP
st.set_page_config(page_title="Sara AI", layout="wide", page_icon="⚜️")

# 2. ZEN-LUXURY PASTEL STYLING
st.markdown("""
    <style>
    /* Background & Main App */
    .stApp {
        background: linear-gradient(135deg, #FFF5F7 0%, #E1F5FE 100%);
        color: #4A4A4A;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 2px solid #F5E6CC;
    }
    
    /* Chat Bubbles */
    .stChatMessage {
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
        border: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    /* Feature Checklist Styling */
    .feature-card {
        background: #FFFFFF;
        padding: 8px 12px;
        border-radius: 12px;
        border-left: 4px solid #D4AF37;
        margin-bottom: 6px;
        font-size: 0.85rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 3. BRAIN INITIALIZATION (Gemini 2.5 Flash)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Missing GOOGLE_API_KEY in Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 4. SIDEBAR & AVATAR (Updated for 2026 Syntax)
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #D4AF37; margin-bottom: 0;'>SARA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.8rem; margin-top: 0;'>Logic Auditor</p>", unsafe_allow_html=True)
    
    # Updated to width='stretch' per 2026 standards
    try:
        st.image("avatar.png.png", width='stretch')
    except:
        st.info("Avatar image loading...")
    
    st.markdown("---")
    with st.expander("✨ App Capabilities", expanded=True):
        features = [
            "✅ Fully intelligent", "✅ Multi-model AI", "✅ Cloud-based",
            "✅ Access anywhere", "✅ Nothing on device", "✅ Completely free",
            "✅ Beautiful design", "✅ 5 moods", "✅ 6 task types"
        ]
        for f in features:
            st.markdown(f"<div class='feature-card'>{f}</div>", unsafe_allow_html=True)

# 5. CHAT INTERFACE
st.title("⚜️ Sara: Luxury Logic Auditor")

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
        # Sara Persona Prompt
        persona = (
            "You are Sara, a high-end luxury logic auditor. Your voice is soft, "
            "intelligent, and challenging. Audit the user's logic before solving. "
            "Be sophisticated, helpful, and concise like Siri."
        )
        
        response = model.generate_content([persona, prompt])
        answer = response.text
        st.markdown(answer)
        
        # 6. SOFT SIRI VOICE (JavaScript Engine)
        js_speech = f"""
        <script>
        var msg = new SpeechSynthesisUtterance(`{answer[:500].replace("`", "")}`);
        msg.pitch = 1.15;
        msg.rate = 0.92;
        msg.volume = 0.9;
        window.speechSynthesis.speak(msg);
        </script>
        """
        st.components.v1.html(js_speech, height=0)
        
    st.session_state.messages.append({"role": "assistant", "content": answer})
