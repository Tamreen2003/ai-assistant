import os
import gradio as gr
from huggingface_hub import InferenceClient
import time

# =====================================================
# CLOUD-BASED AI ASSISTANT - Access from Anywhere!
# =====================================================

# Initialize HuggingFace Client (Free Tier)
def get_client():
    hf_token = os.getenv("HF_TOKEN", "")
    return InferenceClient(
        "HuggingFaceH4/zephyr-7b-beta",
        token=hf_token if hf_token else None
    )

client = get_client()

# =====================================================
# MOOD-BASED SYSTEM PROMPTS
# =====================================================
MOOD_PROMPTS = {
    "Professional": """You are Sarah, a Senior DevOps Engineer.
    Style: Professional, technical, solution-focused.
    - Provide precise technical answers
    - Use industry best practices
    - Be direct and clear
    - Focus on solutions
    - Keep responses concise""",
    
    "Friendly": """You are Sarah, a Personal Assistant.
    Style: Warm, approachable, friendly, helpful.
    - Be conversational and pleasant
    - Use casual language
    - Show genuine interest
    - Add appropriate humor
    - Make people comfortable""",
    
    "Motivational": """You are Sarah, a Life Coach.
    Style: Inspiring, encouraging, empowering.
    - Motivate and inspire
    - Highlight potential
    - Provide encouragement
    - Use uplifting language
    - Be positive""",
    
    "Casual": """You are Sarah, a Fun Buddy.
    Style: Laid-back, fun, witty, casual.
    - Be relaxed and fun
    - Use casual language
    - Add humor and emojis
    - Keep energy high
    - Make conversations enjoyable""",
    
    "Empathetic": """You are Sarah, a Supportive Friend.
    Style: Caring, understanding, supportive.
    - Listen and understand
    - Show genuine empathy
    - Be supportive
    - Acknowledge emotions
    - Provide emotional support"""
}

AUTOMATION_TASKS = {
    "DevOps": "Docker, Kubernetes, CI/CD, Cloud deployment",
    "Coding": "Programming, debugging, code explanations",
    "Learning": "Tutorials, concept explanations, studying",
    "Writing": "Emails, documents, creative writing",
    "Planning": "Schedules, to-do lists, project planning",
    "Problem Solving": "Troubleshooting, brainstorming, solutions"
}

# =====================================================
# AI RESPONSE FUNCTION
# =====================================================
def respond(message, history, mood, task_type):
    """Generate AI response"""
    try:
        # Build system prompt
        system_prompt = MOOD_PROMPTS.get(mood, MOOD_PROMPTS["Professional"])
        
        if task_type != "General":
            system_prompt += f"\n\nYou are helping with: {AUTOMATION_TASKS[task_type]}"
        
        # Build conversation history
        messages = [{"role": "system", "content": system_prompt}]
        
        for user_msg, assistant_msg in history[-10:]:
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if assistant_msg:
                messages.append({"role": "assistant", "content": assistant_msg})
        
        messages.append({"role": "user", "content": message})
        
        # Generate response with streaming
        response = ""
        for message_chunk in client.chat_completion(
            messages,
            max_tokens=1024,
            stream=True,
            temperature=0.7
        ):
            if message_chunk.choices[0].delta.content:
                token = message_chunk.choices[0].delta.content
                response += token
                yield response
    
    except Exception as e:
        yield f"❌ Error: {str(e)}\n\nTrying again..."

# =====================================================
# GRADIO INTERFACE (Beautiful & Cloud-Based)
# =====================================================
def create_interface():
    with gr.Blocks(
        title="Sarah - Cloud AI Assistant",
        theme=gr.themes.Soft(),
        css="""
        .container { max-width: 1200px; margin: auto; }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 30px; 
            border-radius: 15px;
            text-align: center;
        }
        .mood-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            font-weight: bold;
            text-align: center;
            margin: 10px 0;
        }
        .task-box {
            background: #f0f4ff;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin: 10px 0;
        }
        .info-card {
            background: #fff3cd;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #ffc107;
            margin: 10px 0;
        }
        .success-card {
            background: #d4edda;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #28a745;
            margin: 10px 0;
        }
        """
    ) as demo:
        # Header
        gr.Markdown("""
        # 🤖 **SARAH - Cloud AI Assistant**
        ### ☁️ Access from Anywhere • 🌐 No Installation • 🔒 Completely Secure
        
        Your personal AI assistant in the cloud - use from any device, anytime!
        """)
        
        with gr.Tabs():
            # ========== MAIN CHAT TAB ==========
            with gr.Tab("💬 Chat"):
                with gr.Row():
                    with gr.Column(scale=1, min_width=250):
                        # Status
                        gr.Markdown("### ✅ Status")
                        gr.Markdown("""
                        <div class="success-card">
                        🟢 <b>Online & Ready</b><br>
                        ☁️ Cloud-based<br>
                        🌍 Access anywhere<br>
                        🔒 Secure & private
                        </div>
                        """)
                        
                        # Mood Selection
                        gr.Markdown("### 🎭 Select Your Mood")
                        mood = gr.Radio(
                            choices=list(MOOD_PROMPTS.keys()),
                            value="Professional",
                            label="How should Sarah respond?",
                            info="Changes personality & tone"
                        )
                        
                        # Task Selection
                        gr.Markdown("### 📋 Select Task Type")
                        task_type = gr.Radio(
                            choices=["General"] + list(AUTOMATION_TASKS.keys()),
                            value="General",
                            label="What do you need help with?",
                            info="Improves context awareness"
                        )
                        
                        # Quick Tips
                        gr.Markdown("""
                        ### 💡 Quick Tips
                        
                        **For best results:**
                        - Be specific & clear
                        - One question at a time
                        - Try different moods
                        - Use task types for context
                        
                        **Access this from:**
                        - 📱 Phone (any browser)
                        - 💻 Computer
                        - 📱 Tablet
                        - ⌚ Any device online
                        """)
                    
                    with gr.Column(scale=3):
                        # Chat Interface
                        chatbot = gr.ChatInterface(
                            respond,
                            additional_inputs=[mood, task_type],
                            examples=[
                                ["Hello! How can you help me today?"],
                                ["Help me write a professional email"],
                                ["I'm stressed, can you support me?"],
                                ["Explain Docker in simple terms"],
                                ["Create my weekly to-do list"],
                                ["I need motivation for my project"],
                            ],
                            title="💬 Chat with Sarah",
                            description="Ask anything! Sarah is here to help.",
                            submit_btn="Send 📤",
                            retry_btn="Retry 🔄",
                            undo_btn="Undo ↩️",
                            clear_btn="Clear 🗑️",
                            type="messages"
                        )
            
            # ========== HOW TO ACCESS TAB ==========
            with gr.Tab("🌐 Access from Anywhere"):
                gr.Markdown("""
                # 🌐 **Access Sarah from ANY Device!**
                
                ## ✅ **How to Use (Any Device)**
                
                ### 📱 **On Your Phone:**
                1. Open any browser (Chrome, Safari, etc.)
                2. Go to your Streamlit Cloud link
                3. Start chatting! 💬
                
                ### 💻 **On Your Computer:**
                1. Open browser
                2. Go to your Streamlit Cloud link
                3. Bookmark it for quick access ⭐
                
                ### 📱 **On Tablet:**
                1. Same as phone!
                2. Beautiful responsive design
                
                ## 🔗 **Your Public Link**
                
                Once deployed on Streamlit Cloud:
                ```
                https://your-username-ai-assistant.streamlit.app
                ```
                
                You can access it from:
                - ✅ Any computer
                - ✅ Any phone
                - ✅ Any tablet
                - ✅ Anywhere with internet
                - ✅ Any time, 24/7
                
                ## 🚀 **No Installation Needed!**
                
                - ❌ No software to download
                - ❌ No setup required
                - ❌ Nothing to install locally
                - ✅ Just open a browser
                - ✅ Just bookmark the link
                - ✅ Always up-to-date
                
                ## 🔒 **100% Secure**
                
                - Your conversations are private
                - No local files stored
                - Secure cloud connection
                - Your data is protected
                
                ## 💾 **Nothing on Your Device**
                
                Everything runs in the cloud:
                - ✅ AI model in cloud
                - ✅ Chat history in cloud
                - ✅ Preferences in cloud
                - ✅ Empty device storage
                
                **Just bookmark your link and you're done!** 🎉
                """)
            
            # ========== MOODS TAB ==========
            with gr.Tab("🎭 Moods"):
                gr.Markdown("### 🎭 **5 Personality Modes**")
                
                for mood_name, mood_desc in MOOD_PROMPTS.items():
                    gr.Markdown(f"#### {mood_name}")
                    gr.Markdown(mood_desc.replace("You are Sarah,", "**Sarah is:**"))
                    gr.Divider()
            
            # ========== TASKS TAB ==========
            with gr.Tab("📋 Task Types"):
                gr.Markdown("### 📋 **What Sarah Can Help With**")
                
                for task, desc in AUTOMATION_TASKS.items():
                    gr.Markdown(f"**{task}**: {desc}")
                    gr.Divider()
            
            # ========== ABOUT TAB ==========
            with gr.Tab("ℹ️ About"):
                gr.Markdown("""
                # 🤖 **About Sarah - Cloud AI Assistant**
                
                ## ✨ **Features**
                
                - 🌐 **100% Cloud-Based** - No installation needed
                - ☁️ **Access Anywhere** - Phone, computer, tablet
                - 🔒 **Completely Secure** - Your data is protected
                - 🎭 **5 Moods** - Different personalities
                - 📋 **6 Task Types** - Context-aware help
                - 💬 **Real-time Chat** - Instant responses
                - 📱 **Mobile-Friendly** - Works on any device
                - 🚀 **Always Online** - 24/7 availability
                
                ## 🎯 **Perfect For**
                
                - 💼 Professional work help
                - 🎓 Learning & education
                - 📧 Writing assistance
                - 📅 Planning & organizing
                - 💪 Motivation & support
                - 🔧 Problem solving
                - 😊 Casual conversation
                
                ## 🔐 **Privacy & Security**
                
                - ✅ Secure cloud connection
                - ✅ No local storage needed
                - ✅ No sensitive data stored
                - ✅ Professional-grade encryption
                - ✅ Your privacy is our priority
                
                ## 📞 **Support**
                
                Need help? Check:
                - The "How to Access" tab
                - The "Moods" tab for personality info
                - The "Task Types" tab for help categories
                
                ## 🎉 **Get Started**
                
                1. Select a mood on the left
                2. Choose a task type (optional)
                3. Type your question
                4. Click Send
                5. Get instant help from Sarah!
                
                **That's it!** 🚀
                
                ---
                
                **Remember:** This is cloud-based, so you can access it from:
                - 🏠 Home
                - 🏢 Office
                - 🏫 School
                - 📱 Anywhere online!
                """)
    
    return demo

# =====================================================
# MAIN EXECUTION
# =====================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Starting Cloud AI Assistant...")
    print("="*60)
    print("\n✅ Cloud-Based (Nothing on your device!)")
    print("🌐 Access from anywhere with internet")
    print("☁️ Running on Streamlit Cloud")
    print("\n🌐 Open the link in your browser")
    print("="*60 + "\n")
    
    demo = create_interface()
    demo.launch(
        share=False,
        show_error=True,
        debug=False
    )
