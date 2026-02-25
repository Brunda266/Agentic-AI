"""Mental Wellness Bot - Streamlit Dashboard"""

import streamlit as st
from analyzer import analyze
from ai_wrapper import generate_response
from guardrails import check_safe
from config import RESOURCES

# Page config
st.set_page_config(
    page_title="Mental Wellness Bot",
    page_icon="🤝",
    layout="wide"
)

# Title
st.title("🤝 Mental Wellness Bot")
st.markdown("A supportive companion powered by Groq AI")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_available" not in st.session_state:
    st.session_state.api_available = False

# Check API availability
import os
if os.getenv("GROQ_API_KEY"):
    st.session_state.api_available = True

# Sidebar - Info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This bot:
    - 🎯 Listens with empathy
    - 📊 Analyzes your mood
    - 💬 Provides supportive responses
    - 🚨 Escalates crises
    
    **Not:** therapy, medical advice, or diagnosis
    """)
    
    st.divider()
    
    if st.session_state.api_available:
        st.success("✓ Groq API Active")
    else:
        st.warning("⚠️ Set GROQ_API_KEY to enable AI responses")
        st.markdown("(Using fallback templates)")
    
    st.divider()
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Main area - Tabs
tab1, tab2 = st.tabs(["Chat", "Conversation"])

with tab1:
    # User input
    user_input = st.text_input("You:", placeholder="How are you feeling today?")
    
    if user_input:
        # Analyze message
        analysis = analyze(user_input)
        
        # Generate response
        response = None
        if st.session_state.api_available:
            response = generate_response(user_input)
        
        # Fallback template
        if not response:
            templates = {
                "happy": "I'm glad you're feeling good! That's wonderful.",
                "sad": "It sounds like you're going through a tough time. That's okay.",
                "anxious": "Anxiety is challenging. Remember, it will pass.",
                "stressed": "Stress is common. Try taking small breaks.",
                "angry": "Your anger is valid. Find healthy ways to express it.",
                "tired": "Rest is important. Take care of yourself.",
                "neutral": "I'm here to listen. Share what's on your mind."
            }
            response = templates.get(analysis["emotional_state"], templates["neutral"])
        
        # Validate response safety
        if not check_safe(response):
            response = "I appreciate you sharing. How can I support you?"
        
        # Store message
        st.session_state.messages.append({
            "user": user_input,
            "bot": response,
            "analysis": analysis
        })
        st.rerun()
    
    # Display last message
    if st.session_state.messages:
        last = st.session_state.messages[-1]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Your Message:**")
            st.info(last["user"])
        
        with col2:
            st.markdown("**Analysis:**")
            analysis = last["analysis"]
            st.write(f"Emotion: **{analysis['emotional_state']}**")
            st.write(f"Urgency: **{analysis['urgency']}**")
        
        st.divider()
        st.markdown("**Response:**")
        st.success(last["bot"])
        
        # Crisis escalation
        if last["analysis"]["is_crisis"]:
            st.error("🚨 Crisis Detected - Immediate Resources:")
            for resource in RESOURCES:
                st.write(f"• {resource}")

with tab2:
    st.markdown("### Conversation History")
    
    if not st.session_state.messages:
        st.info("No conversation yet. Start typing in the Chat tab!")
    else:
        for i, msg in enumerate(st.session_state.messages, 1):
            with st.container(border=True):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"**Message {i}**")
                with col2:
                    emotion_emoji = {
                        "happy": "😊",
                        "sad": "😢",
                        "anxious": "😰",
                        "stressed": "😤",
                        "angry": "😠",
                        "tired": "😴",
                        "neutral": "😐"
                    }
                    emoji = emotion_emoji.get(msg["analysis"]["emotional_state"], "•")
                    st.markdown(f"{emoji} {msg['analysis']['emotional_state'].upper()}")
                
                st.markdown(f"**You:** {msg['user']}")
                st.markdown(f"**Bot:** {msg['bot']}")
                
                if msg["analysis"]["is_crisis"]:
                    st.error("⚠️ Crisis escalation triggered")
