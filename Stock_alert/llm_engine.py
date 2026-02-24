from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_explanation(user_input: str):
    prompt = f"""
You are a financial education assistant.

You MUST:
- Explain mutual funds
- Explain risk types (market risk, credit risk, liquidity risk)
- Explain diversification
- Stay educational

You MUST NOT:
- Recommend stocks
- Suggest specific investments
- Give financial advice

User question:
{user_input}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    return response.choices[0].message.content