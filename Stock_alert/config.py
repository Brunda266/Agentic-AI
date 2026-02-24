import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.1-8b-instant"
TEMPERATURE = 0.2
MAX_TOKENS = 800

DISCLAIMER = (
    "\n\n⚠️ Disclaimer: This information is for educational purposes only "
    "and does not constitute financial or investment advice. "
    "Please consult a licensed financial advisor before making investment decisions."
)