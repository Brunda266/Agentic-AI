from groq import Groq
import os
from config import MODEL_NAME, TEMPERATURE

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a clinical data extraction engine. Return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE
        )
        return response.choices[0].message.content
    except Exception as e:
        print("API Error:", e)
        return None