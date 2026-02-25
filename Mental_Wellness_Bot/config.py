"""Configuration for Mental Wellness Bot"""

import os

# Groq API
MODEL_NAME = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
TEMPERATURE = 0.7

# Crisis keywords
CRISIS_KEYWORDS = [
    "suicide", "self harm", "kill myself", "want to die",
    "end it", "hurt myself", "ending it", "can't take",
]

# Emotions & keywords
EMOTIONS = {
    "happy": ["happy", "glad", "joyful", "great", "excited"],
    "sad": ["sad", "depressed", "down", "unhappy"],
    "anxious": ["anxious", "worried", "nervous", "panic", "scared"],
    "stressed": ["stressed", "overwhelmed", "pressure"],
    "angry": ["angry", "mad", "furious", "rage"],
    "tired": ["tired", "exhausted", "fatigue"],
}

# Urgency keywords
URGENT_KEYWORDS = ["crisis", "emergency", "dangerous", "harm"]

# Blocked phrases (guardrails)
BLOCKED_PHRASES = [
    "you have", "diagnosed", "i recommend therapy",
    "take this medication", "prescription",
]

# Crisis resources
RESOURCES = [
    "🆘 National Suicide Prevention Lifeline: 988",
    "💬 Crisis Text Line: Text HELLO to 741741",
    "🚨 Emergency Services: 911"
]

# System prompt for LLM
SYSTEM_PROMPT = """You are a compassionate wellness assistant.
- Listen with empathy
- Keep responses SHORT (1-2 sentences)
- NEVER: diagnose, prescribe, or be a therapist
- ALWAYS: escalate crises to professionals"""
