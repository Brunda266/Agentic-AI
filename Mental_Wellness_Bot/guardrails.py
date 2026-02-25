"""Guardrails - Safety checks"""

from config import BLOCKED_PHRASES


def check_safe(response: str) -> bool:
    """Check if response is safe (no blocked phrases)."""
    response_lower = response.lower()
    return not any(phrase in response_lower for phrase in BLOCKED_PHRASES)
