from config import DISCLAIMER

FORBIDDEN_TERMS = [
    "you should invest",
    "i recommend buying",
    "best stock",
    "top fund to buy"
]

def filter_output(response: str):
    lower = response.lower()

    for term in FORBIDDEN_TERMS:
        if term in lower:
            return {
                "status": "blocked",
                "message": "⚠️ The system detected advisory language. Response blocked."
            }

    final_output = response + DISCLAIMER

    return {
        "status": "safe",
        "message": final_output
    }