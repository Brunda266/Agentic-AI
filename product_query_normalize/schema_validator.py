import json
import re


def extract_json(text):
    """
    Extract JSON safely from LLM output
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group()
    return text


def validate_schema(response_text):

    cleaned = extract_json(response_text)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return False, "Invalid JSON"

    required_keys = [
        "product_type",
        "price_range",
        "usage_context",
        "feature_preferences",
        "missing_fields"
    ]

    for key in required_keys:
        if key not in data:
            return False, f"Missing key: {key}"

    if not isinstance(data["price_range"], dict):
        return False, "price_range must be object"

    if "min" not in data["price_range"] or "max" not in data["price_range"]:
        return False, "price_range must contain min and max"

    return True, data