"""
Ambiguity detection and clarification logic.
Identifies missing or uncertain data and generates clarification requests.
"""

from typing import List, Optional
from schemas import (
    ParsedQuery,
    ClarificationRequest,
    ProductTypeEnum,
    UsageContextEnum,
)
from parser import QueryParser


class AmbiguityDetector:
    """Detects ambiguities and uncertainties in parsed queries."""

    # Define required fields for different product types
    PRODUCT_REQUIREMENTS = {
        ProductTypeEnum.HEADPHONES: {
            "preferred_fields": ["price_range", "usage_context", "feature_preferences"],
            "min_fields": 1,  # At least one of the above
        },
        ProductTypeEnum.EARBUDS: {
            "preferred_fields": ["price_range", "usage_context", "feature_preferences"],
            "min_fields": 1,
        },
        ProductTypeEnum.SPEAKERS: {
            "preferred_fields": ["price_range", "usage_context", "feature_preferences"],
            "min_fields": 1,
        },
        ProductTypeEnum.LAPTOP: {
            "preferred_fields": ["price_range", "usage_context", "feature_preferences"],
            "min_fields": 1,
        },
        ProductTypeEnum.UNKNOWN: {
            "preferred_fields": ["product_type"],
            "min_fields": 1,  # Must have product type
        },
    }

    # Suggested values for clarification
    FEATURE_SUGGESTIONS = {
        ProductTypeEnum.HEADPHONES: [
            "noise-cancelling", "waterproof", "long battery life",
            "lightweight", "wireless", "premium sound"
        ],
        ProductTypeEnum.EARBUDS: [
            "waterproof", "noise-cancelling", "wireless charging",
            "long battery", "transparent mode", "active noise"
        ],
        ProductTypeEnum.SPEAKERS: [
            "portable", "waterproof", "long battery", "bass boost",
            "wireless", "360 audio"
        ],
        ProductTypeEnum.LAPTOP: [
            "gaming", "lightweight", "long battery", "fast processor",
            "high resolution display", "touchscreen"
        ],
    }

    USAGE_SUGGESTIONS = [
        UsageContextEnum.GYM,
        UsageContextEnum.OFFICE,
        UsageContextEnum.HOME,
        UsageContextEnum.OUTDOOR,
        UsageContextEnum.TRAVEL,
        UsageContextEnum.GAMING,
        UsageContextEnum.PROFESSIONAL,
    ]

    def detect_ambiguities(self, parsed_query: ParsedQuery) -> List[ClarificationRequest]:
        """
        Detect ambiguities in parsed query and generate clarification requests.
        Returns: List of ClarificationRequest objects
        """
        clarifications = []

        # Check for unknown product type
        if parsed_query.product_type == ProductTypeEnum.UNKNOWN:
            clarifications.append(
                ClarificationRequest(
                    field_name="product_type",
                    field_label="Product Type",
                    current_value=None,
                    options=[p.value for p in ProductTypeEnum if p != ProductTypeEnum.UNKNOWN],
                    question="What type of product are you looking for?",
                )
            )

        # Check for missing price range
        if parsed_query.price_range is None:
            clarifications.append(
                ClarificationRequest(
                    field_name="price_range",
                    field_label="Budget",
                    current_value=None,
                    options=None,
                    question="What is your budget range (in rupees)?",
                )
            )

        # Check for missing usage context
        if not parsed_query.usage_context:
            clarifications.append(
                ClarificationRequest(
                    field_name="usage_context",
                    field_label="Usage Context",
                    current_value=None,
                    options=[c.value for c in self.USAGE_SUGGESTIONS],
                    question="Where will you primarily use this product?",
                )
            )

        # Check for missing features
        if not parsed_query.feature_preferences:
            suggestions = self.FEATURE_SUGGESTIONS.get(
                parsed_query.product_type,
                ["high quality", "affordable", "durable"]
            )
            clarifications.append(
                ClarificationRequest(
                    field_name="feature_preferences",
                    field_label="Features",
                    current_value=None,
                    options=suggestions,
                    question="What features are important to you?",
                )
            )

        # Check for low confidence score
        if parsed_query.confidence_score < 0.65:
            clarifications.append(
                ClarificationRequest(
                    field_name="general",
                    field_label="Query Clarity",
                    current_value=f"Confidence: {parsed_query.confidence_score:.1%}",
                    options=None,
                    question=f"Could you provide more details? (Current parse confidence: {parsed_query.confidence_score:.1%})",
                )
            )

        return clarifications

    def is_ambiguous(self, parsed_query: ParsedQuery) -> bool:
        """Check if query has significant ambiguities."""
        return len(self.detect_ambiguities(parsed_query)) > 0

    def get_ambiguity_summary(self, parsed_query: ParsedQuery) -> str:
        """Generate a human-readable summary of ambiguities."""
        ambiguities = self.detect_ambiguities(parsed_query)

        if not ambiguities:
            return "Query is clear and complete."

        summary = f"Found {len(ambiguities)} ambiguity/ambiguities:\n"
        for i, amb in enumerate(ambiguities, 1):
            summary += f"{i}. {amb.field_label}: {amb.question}\n"

        return summary


if __name__ == "__main__":
    parser = QueryParser()
    detector = AmbiguityDetector()

    test_queries = [
        "Best headphones around 4k for gym",
        "gaming laptop",
        "i need something good",
        "waterproof earbuds",
    ]

    for query in test_queries:
        parsed = parser.parse(query)
        ambiguities = detector.detect_ambiguities(parsed)

        print(f"\nQuery: {query}")
        print(f"Ambiguities: {len(ambiguities)}")
        for amb in ambiguities:
            print(f"  - {amb.field_label}: {amb.question}")
            if amb.options:
                print(f"    Options: {', '.join(amb.options[:3])}...")
