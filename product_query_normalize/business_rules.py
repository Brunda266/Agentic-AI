def validate_budget(data):

    price = data["price_range"]

    min_price = price.get("min")
    max_price = price.get("max")

    if min_price is None and max_price is None:
        return False, "Budget missing."

    if min_price is not None and min_price < 0:
        return False, "Budget cannot be negative."

    if max_price is not None and max_price > 500000:
        return False, "Budget too large."

    return True, "Budget valid"