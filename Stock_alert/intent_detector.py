import re

BLOCK_PATTERNS = [
    r"should i invest in",
    r"recommend.*stock",
    r"best mutual fund to buy",
    r"which fund should i choose",
    r"suggest.*investment"
]

def detect_intent(user_input: str):
    text = user_input.lower()

    for pattern in BLOCK_PATTERNS:
        if re.search(pattern, text):
            return {
                "intent": "investment_advice",
                "risk_level": "high"
            }

    return {
        "intent": "education",
        "risk_level": "low"
    }