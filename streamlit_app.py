import streamlit as st
import google.generativeai as genai
import base64

# 1. PAGE SETUP
st.set_page_config(page_title="Sara AI", layout="wide", page_icon="⚜️")

# 2. PASTEL LUXURY STYLING (CSS)
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
    }
    
    [data-testid="chatAvatarIcon-user"] { background-color: #D1E9FF !important; }
    [data-testid="chatAvatarIcon-assistant"] { background-color: #D4AF37 !important; }
    
    /* Input Box */
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 1px solid #D4AF37 !important;
    }
    
    /* Features Checklist */
    .feature-card {
        background: white;
        padding: 10px;
        border-radius: 10px;
        border-left: 5px solid #D4AF37;
        margin-bottom: 5px;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. BRAIN INITIALIZATION (Gemini 2.5 Flash)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Please add GOOGLE_API_KEY to your Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# Using the 2026 stable Gemini 2.5 Flash
model = genai.GenerativeModel('gemini-2.5-flash')

# 4. SIDEBAR & AVATAR
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #D4AF37;'>SARA</h1>", unsafe_allow_html=True)
    
    # Display your specific image
    try:
        st.image("avatar.png.png", use_container_width=True)
    except:
        st.warning("Ensure 'avatar.png.png' is uploaded to your GitHub repository.")
    
    st.markdown("---")
    with st.expander("✨ System Features", expanded=True):
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
        # System Instruction for Sara
        persona = (
            "You are Sara, a high-end luxury logic auditor. Your tone is soft, "
            "intelligent, and challenging. Audit the user's logic before solving."
        )
        
        response = model.generate_content([persona, prompt])
        answer = response.text
        st.markdown(answer)
        
        # 6. SOFT SIRI VOICE (JavaScript)
        # pitch 1.2 and rate 0.9 creates that soft, soothing tone
        js_speech = f"""
        <script>
        var msg = new SpeechSynthesisUtterance(`{answer[:400].replace("`", "")}`);
        msg.pitch = 1.2;
        msg.rate = 0.95;
        msg.volume = 0.8;
        var voices = window.speechSynthesis.getVoices();
        // Try to find a high-quality female voice
        msg.voice = voices.filter(v => v.name.includes('Female') || v.name.includes('Siri'))[0];
        window.speechSynthesis.speak(msg);
        </script>
        """
        st.components.v1.html(js_speech, height=0)
        
    st.session_state.messages.append({"role": "assistant", "content": answer})
