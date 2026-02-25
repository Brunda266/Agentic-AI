"""Groq API wrapper"""

from groq import Groq
import os
from config import MODEL_NAME, TEMPERATURE, SYSTEM_PROMPT

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None


def generate_response(message: str) -> str | None:
    """
    Generate response using Groq API.
    
    Returns:
        Response text or None if API unavailable
    """
    if not client:
        return None
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=TEMPERATURE
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"API Error: {e}")
        return None
