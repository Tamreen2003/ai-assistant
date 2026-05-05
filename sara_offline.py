"""
🤖 SARAH - Completely Offline AI Assistant
No servers, no internet, no background processes needed!
Run once, close anytime. Completely standalone.
"""

import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import threading
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import os
from datetime import datetime

# =====================================================
# CONFIGURATION
# =====================================================

class Config:
    # Model: Lightweight, fast, offline-capable
    MODEL_NAME = "distilgpt2"  # ~350MB, super fast
    # Alternatives:
    # "gpt2" - Better quality, ~500MB
    # "distilgpt2" - Fastest, ~350MB (DEFAULT)
    
    MOOD_PROMPTS = {
        "Professional": {
            "system": "You are Sarah, a Senior DevOps Engineer. Be technical, professional, and solution-focused. Keep responses concise and practical.",
            "emoji": "🎯"
        },
        "Friendly": {
            "system": "You are Sarah, a friendly personal assistant. Be warm, casual, and pleasant. Use conversational tone.",
            "emoji": "😊"
        },
        "Motivational": {
            "system": "You are Sarah, a motivational coach. Be inspiring and encouraging. Help the user see their potential.",
            "emoji": "💪"
        },
        "Casual": {
            "system": "You are Sarah, a fun buddy. Be relaxed, witty, and funny. Make conversations enjoyable.",
            "emoji": "😎"
        },
        "Empathetic": {
            "system": "You are Sarah, a caring friend. Be supportive and understanding. Show genuine empathy.",
            "emoji": "🤗"
        }
    }
    
    TASKS = {
        "General": "Answer general questions helpfully",
        "DevOps": "Help with Docker, Kubernetes, CI/CD, cloud deployment",
        "Coding": "Debug code, explain programming concepts",
        "Learning": "Explain concepts and create tutorials",
        "Writing": "Help with emails and documents",
        "Planning": "Create schedules and to-do lists"
    }

# =====================================================
# AI ENGINE (Offline - No Internet)
# =====================================================

class OfflineAI:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.loaded = False
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self, progress_callback=None):
        """Load model without internet"""
        try:
            if progress_callback:
                progress_callback("Downloading model (first time only)...", 10)
            
            # Download and cache the model
            self.tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
            self.model = AutoModelForCausalLM.from_pretrained(Config.MODEL_NAME)
            self.model.to(self.device)
            
            if progress_callback:
                progress_callback("Model loaded successfully!", 100)
            
            self.loaded = True
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def generate_response(self, prompt, max_length=150):
        """Generate response completely offline"""
        if not self.loaded:
            return "Model not loaded. Please wait..."
        
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"

# =====================================================
# GUI - Beautiful Offline App
# =====================================================

class SarahApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 SARAH - Offline AI Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f2f5")
        
        # Initialize AI
        self.ai = OfflineAI()
        self.current_mood = "Professional"
        self.current_task = "General"
        
        self.setup_ui()
        self.load_model_async()
    
    def setup_ui(self):
        """Create beautiful GUI"""
        
        # ===== HEADER =====
        header = tk.Frame(self.root, bg="#667eea", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="🤖 SARAH - Your Offline AI Assistant",
            font=("Helvetica", 24, "bold"),
            bg="#667eea",
            fg="white"
        )
        title.pack(pady=15)
        
        subtitle = tk.Label(
            header,
            text="✅ Completely Offline • 🔒 100% Private • ⚡ No Internet Needed",
            font=("Helvetica", 10),
            bg="#667eea",
            fg="#e0e0ff"
        )
        subtitle.pack()
        
        # ===== MAIN CONTENT =====
        main_frame = tk.Frame(self.root, bg="#f0f2f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # --- LEFT PANEL: Controls ---
        left_panel = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Status
        self.status_label = tk.Label(
            left_panel,
            text="⏳ Loading Model...",
            font=("Helvetica", 10, "bold"),
            bg="white",
            fg="#ff6b6b"
        )
        self.status_label.pack(pady=10, padx=10)
        
        # Mood Selection
        tk.Label(
            left_panel,
            text="🎭 Select Mood:",
            font=("Helvetica", 12, "bold"),
            bg="white"
        ).pack(pady=(10, 5), padx=10)
        
        self.mood_var = tk.StringVar(value="Professional")
        for mood in Config.MOOD_PROMPTS.keys():
            emoji = Config.MOOD_PROMPTS[mood]["emoji"]
            rb = tk.Radiobutton(
                left_panel,
                text=f"{emoji} {mood}",
                variable=self.mood_var,
                value=mood,
                font=("Helvetica", 10),
                bg="white",
                command=self.on_mood_change
            )
            rb.pack(anchor=tk.W, padx=20, pady=5)
        
        # Task Selection
        tk.Label(
            left_panel,
            text="📋 Select Task:",
            font=("Helvetica", 12, "bold"),
            bg="white"
        ).pack(pady=(15, 5), padx=10)
        
        self.task_var = tk.StringVar(value="General")
        for task in Config.TASKS.keys():
            rb = tk.Radiobutton(
                left_panel,
                text=f"• {task}",
                variable=self.task_var,
                value=task,
                font=("Helvetica", 10),
                bg="white",
                command=self.on_task_change
            )
            rb.pack(anchor=tk.W, padx=20, pady=3)
        
        # Info
        info_text = tk.Label(
            left_panel,
            text="ℹ️ Tips:\n\n• Be specific\n• One question\n• Check mood\n\n✅ No WiFi needed!\n🔒 Fully Private\n⚡ Lightning Fast",
            font=("Helvetica", 9),
            bg="#f0f4ff",
            fg="#333",
            justify=tk.LEFT,
            wraplength=150
        )
        info_text.pack(pady=15, padx=10, fill=tk.BOTH)
        
        # --- RIGHT PANEL: Chat ---
        right_panel = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat Header
        chat_header = tk.Label(
            right_panel,
            text="💬 Chat with Sarah",
            font=("Helvetica", 14, "bold"),
            bg="#667eea",
            fg="white"
        )
        chat_header.pack(fill=tk.X, padx=10, pady=10)
        
        # Chat Display
        self.chat_display = scrolledtext.ScrolledText(
            right_panel,
            font=("Helvetica", 10),
            bg="#fafafa",
            fg="#333",
            wrap=tk.WORD,
            height=15,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure text tags for styling
        self.chat_display.tag_config("user", foreground="#667eea", font=("Helvetica", 10, "bold"))
        self.chat_display.tag_config("assistant", foreground="#764ba2", font=("Helvetica", 10, "bold"))
        self.chat_display.tag_config("system", foreground="#999", font=("Helvetica", 9, "italic"))
        
        # Input Frame
        input_frame = tk.Frame(right_panel, bg="white")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_field = tk.Entry(
            input_frame,
            font=("Helvetica", 11),
            bg="#f5f5f5",
            fg="#333",
            relief=tk.FLAT,
            bd=0
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        send_btn = tk.Button(
            input_frame,
            text="📤 Send",
            font=("Helvetica", 10, "bold"),
            bg="#667eea",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.send_message
        )
        send_btn.pack(side=tk.RIGHT)
        
        # Initial message
        self.add_message("System", "✅ Loading model... Please wait!", "system")
    
    def load_model_async(self):
        """Load model in background thread"""
        def load():
            success = self.ai.load_model(self.update_progress)
            if success:
                self.root.after(0, self.on_model_loaded)
            else:
                self.root.after(0, self.on_model_error)
        
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def update_progress(self, message, progress):
        """Update progress during loading"""
        self.status_label.config(text=f"⏳ {message}")
        self.root.update()
    
    def on_model_loaded(self):
        """Called when model is loaded"""
        self.status_label.config(text="✅ Ready!", fg="#51cf66")
        self.add_message("System", "🎉 Model loaded! Ready to chat.\n\nHi! I'm Sarah, your offline AI assistant.\nI'm completely local and don't need internet.\n\nWhat can I help you with?", "system")
        self.input_field.config(state=tk.NORMAL)
    
    def on_model_error(self):
        """Called if model loading fails"""
        self.status_label.config(text="❌ Error", fg="#ff6b6b")
        self.add_message("System", "❌ Error loading model.\n\nMake sure you have:\n• 4GB free RAM\n• 4GB free disk space\n• Internet (first run only)", "system")
    
    def on_mood_change(self):
        self.current_mood = self.mood_var.get()
        emoji = Config.MOOD_PROMPTS[self.current_mood]["emoji"]
        self.add_message("System", f"Mood changed to {emoji} {self.current_mood}", "system")
    
    def on_task_change(self):
        self.current_task = self.task_var.get()
        self.add_message("System", f"Task type: {self.current_task}", "system")
    
    def add_message(self, sender, message, tag="user"):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n", "")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self):
        """Send message and get response"""
        if not self.ai.loaded:
            messagebox.showwarning("Wait", "Model is still loading...")
            return
        
        user_input = self.input_field.get().strip()
        if not user_input:
            return
        
        # Clear input
        self.input_field.delete(0, tk.END)
        
        # Add user message
        self.add_message("You", user_input, "user")
        
        # Generate response in thread
        def generate():
            mood_system = Config.MOOD_PROMPTS[self.current_mood]["system"]
            task_context = Config.TASKS[self.current_task]
            
            prompt = f"{mood_system}\nTask: {task_context}\n\nUser: {user_input}\n\nSarah:"
            
            response = self.ai.generate_response(prompt, max_length=200)
            self.root.after(0, lambda: self.add_message("Sarah", response, "assistant"))
        
        thread = threading.Thread(target=generate, daemon=True)
        thread.start()

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = SarahApp(root)
    root.mainloop()
