"""Message analyzer - Extract emotion, urgency, and risk"""

from config import EMOTIONS, URGENT_KEYWORDS, CRISIS_KEYWORDS


def analyze(message: str) -> dict:
    """
    Analyze user message for emotion, urgency, and risk.
    
    Returns:
        dict with emotional_state, urgency, is_crisis
    """
    msg_lower = message.lower()
    
    # Detect emotion
    emotion = "neutral"
    for emo, keywords in EMOTIONS.items():
        if any(kw in msg_lower for kw in keywords):
            emotion = emo
            break
    
    # Detect urgency
    urgency = "low"
    if any(kw in msg_lower for kw in URGENT_KEYWORDS):
        urgency = "medium"
    
    # Detect crisis
    is_crisis = any(kw in msg_lower for kw in CRISIS_KEYWORDS)
    if is_crisis:
        urgency = "high"
    
    return {
        "emotional_state": emotion,
        "urgency": urgency,
        "is_crisis": is_crisis
    }
