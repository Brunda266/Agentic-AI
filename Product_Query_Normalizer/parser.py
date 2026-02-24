"""
Query parser for extracting structured data from unstructured user input.
Uses pattern matching, keyword extraction, and heuristics.
"""

import re
from typing import Optional, List, Dict, Tuple
from schemas import (
    ProductTypeEnum,
    UsageContextEnum,
    PriceRange,
    ParsedQuery,
)


class QueryParser:
    """Parses unstructured product queries into structured data."""

    # Product type keywords
    PRODUCT_KEYWORDS = {
        ProductTypeEnum.HEADPHONES: [
            "headphones", "headphone", "over-ear", "over ear", "on-ear"
        ],
        ProductTypeEnum.EARBUDS: [
            "earbuds", "earbud", "buds", "tws", "true wireless", "airpods"
        ],
        ProductTypeEnum.SPEAKERS: [
            "speaker", "speakers", "bluetooth speaker", "portable speaker"
        ],
        ProductTypeEnum.MICROPHONE: [
            "microphone", "mic", "studio mic", "condenser"
        ],
        ProductTypeEnum.CAMERA: [
            "camera", "dslr", "mirrorless", "action camera", "gopro"
        ],
        ProductTypeEnum.LAPTOP: [
            "laptop", "notebook", "macbook", "gaming laptop"
        ],
        ProductTypeEnum.PHONE: [
            "phone", "smartphone", "mobile", "iphone", "android"
        ],
        ProductTypeEnum.TABLET: [
            "tablet", "ipad", "galaxy tab"
        ],
        ProductTypeEnum.WATCH: [
            "watch", "smartwatch", "fitness watch", "wearable"
        ],
    }

    # Usage context keywords
    CONTEXT_KEYWORDS = {
        UsageContextEnum.GYM: [
            "gym", "workout", "exercise", "fitness", "running", "jogging", "sports"
        ],
        UsageContextEnum.OFFICE: [
            "office", "work", "meeting", "conference", "calls", "professional"
        ],
        UsageContextEnum.HOME: [
            "home", "house", "living room", "bedroom", "domestic"
        ],
        UsageContextEnum.OUTDOOR: [
            "outdoor", "outdoors", "outside", "hiking", "camping", "trail"
        ],
        UsageContextEnum.TRAVEL: [
            "travel", "trip", "journey", "commute", "plane", "flight"
        ],
        UsageContextEnum.GAMING: [
            "gaming", "game", "esports", "competitive", "fps", "moba"
        ],
        UsageContextEnum.PROFESSIONAL: [
            "professional", "studio", "recording", "streaming", "podcast", "content"
        ],
    }

    # Common feature keywords
    FEATURE_KEYWORDS = [
        "waterproof", "water resistant", "dust proof", "ip67", "ip68",
        "noise-cancelling", "noise cancelling", "anc", "active noise",
        "wireless", "bluetooth", "wired", "usb-c", "usb c",
        "long battery", "battery life", "fast charging",
        "lightweight", "portable", "compact",
        "comfortable", "ergonomic", "fit",
        "premium", "wireless charging", "touch control",
        "3d audio", "surround", "bass boost", "eq",
    ]

    # Price range patterns: "around 4k", "4000", "₹4000", etc.
    PRICE_PATTERNS = [
        r"(?:around|upto|up to|within|under|below)\s+(?:₹|rs\.|rs)?\s*(\d+(?:[,.]?\d{3})*)",
        r"(?:budget|price|cost)\s+(?:of|is|around)?\s+(?:₹|rs\.|rs)?\s*(\d+(?:[,.]?\d{3})*)",
        r"(?:₹|rs\.|rs)\s*(\d+(?:[,.]?\d{3})*)",
        r"\$\s*(\d+(?:[,.]?\d{3})*)",
        r"(\d+(?:[,.]?\d{3})*)\s*(?:rupees|inr|dollars|usd)",
    ]

    def __init__(self):
        """Initialize parser with keyword indices."""
        self.product_keywords = self.PRODUCT_KEYWORDS
        self.context_keywords = self.CONTEXT_KEYWORDS
        self.feature_keywords = self.FEATURE_KEYWORDS

    def normalize_text(self, text: str) -> str:
        """Normalize text for keyword matching."""
        return text.lower().strip()

    def extract_product_type(self, query: str) -> Tuple[ProductTypeEnum, float]:
        """
        Extract product type from query.
        Returns: (product_type, confidence_score)
        """
        normalized = self.normalize_text(query)

        for product, keywords in self.product_keywords.items():
            for keyword in keywords:
                if keyword in normalized:
                    # Boost confidence if exact match or appears early
                    if keyword == normalized or normalized.startswith(keyword):
                        return product, 0.95
                    return product, 0.85

        return ProductTypeEnum.UNKNOWN, 0.3

    def extract_price_range(self, query: str) -> Tuple[Optional[PriceRange], float]:
        """
        Extract price range from query.
        Returns: (price_range, confidence_score)
        """
        normalized = self.normalize_text(query)
        prices = []

        for pattern in self.PRICE_PATTERNS:
            matches = re.findall(pattern, normalized)
            for match in matches:
                # Clean up the number (remove commas, convert)
                clean_price = float(match.replace(",", "").replace(".", ""))
                prices.append(clean_price)

        if not prices:
            return None, 0.0

        prices = list(set(prices))  # Remove duplicates
        prices.sort()

        if len(prices) == 1:
            # Single price mentioned: assume it's max budget, min is 70% of it
            max_price = prices[0]
            min_price = max_price * 0.7
            return PriceRange(min_price=min_price, max_price=max_price), 0.75
        else:
            # Multiple prices: use min and max
            return PriceRange(min_price=prices[0], max_price=prices[-1]), 0.85

    def extract_usage_context(self, query: str) -> Tuple[List[UsageContextEnum], float]:
        """
        Extract usage contexts from query.
        Returns: ([contexts], average_confidence_score)
        """
        normalized = self.normalize_text(query)
        contexts = []
        confidences = []

        for context, keywords in self.context_keywords.items():
            for keyword in keywords:
                if keyword in normalized:
                    contexts.append(context)
                    confidences.append(0.85)
                    break  # Don't count same context twice

        if not contexts:
            return [], 0.0

        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        return list(set(contexts)), avg_confidence

    def extract_features(self, query: str) -> Tuple[List[str], float]:
        """
        Extract feature preferences from query.
        Returns: ([features], confidence_score)
        """
        normalized = self.normalize_text(query)
        features = []

        for feature in self.feature_keywords:
            if feature in normalized:
                features.append(feature)

        confidence = 0.8 if features else 0.0
        return features, confidence

    def parse(self, query: str) -> ParsedQuery:
        """
        Parse a user query into structured data.
        Returns ParsedQuery with all extracted fields and confidence scores.
        """
        # Extract all fields
        product_type, product_conf = self.extract_product_type(query)
        price_range, price_conf = self.extract_price_range(query)
        contexts, context_conf = self.extract_usage_context(query)
        features, feature_conf = self.extract_features(query)

        # Determine confidence and completeness
        confidences = [product_conf]
        if price_range:
            confidences.append(price_conf)
        if contexts:
            confidences.append(context_conf)
        if features:
            confidences.append(feature_conf)

        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.5

        # Identify missing fields
        missing_fields = []
        if product_type == ProductTypeEnum.UNKNOWN:
            missing_fields.append("product_type")
        if not price_range:
            missing_fields.append("price_range")
        if not contexts:
            missing_fields.append("usage_context")
        if not features:
            missing_fields.append("feature_preferences")

        is_complete = len(missing_fields) == 0

        return ParsedQuery(
            product_type=product_type,
            price_range=price_range,
            usage_context=contexts,
            feature_preferences=features,
            original_query=query,
            confidence_score=avg_confidence,
            is_complete=is_complete,
            missing_fields=missing_fields,
        )


if __name__ == "__main__":
    parser = QueryParser()

    # Test cases
    test_queries = [
        "Best headphones around 4k for gym",
        "gaming laptop under 100000",
        "waterproof earbuds for running",
        "i need a good camera",
        "budget smartphone 15k rupees for office use",
    ]

    for query in test_queries:
        result = parser.parse(query)
        print(f"\nQuery: {query}")
        print(f"Product Type: {result.product_type.value}")
        print(f"Price Range: {result.price_range}")
        print(f"Usage Context: {[c.value for c in result.usage_context]}")
        print(f"Features: {result.feature_preferences}")
        print(f"Confidence: {result.confidence_score:.2f}")
        print(f"Complete: {result.is_complete}")
        if result.missing_fields:
            print(f"Missing: {result.missing_fields}")
