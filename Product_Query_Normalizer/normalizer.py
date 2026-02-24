"""
End-to-end normalizer combining parser, detector, and validator.
Main entry point for the Product Query Normalizer system.
"""

from typing import Optional, Dict
from schemas import ParsedQuery, NormalizedResult, ClarificationRequest
from parser import QueryParser
from ambiguity_detector import AmbiguityDetector
from validator import InteractiveClarifier, QueryValidator


class ProductQueryNormalizer:
    """
    Main orchestrator for the Product Query Normalizer system.
    Handles parsing, ambiguity detection, validation, and clarification.
    """

    def __init__(self):
        self.parser = QueryParser()
        self.detector = AmbiguityDetector()
        self.clarifier = InteractiveClarifier()
        self.validator = QueryValidator()

    def normalize(
        self, query: str, user_responses: Optional[Dict[str, str]] = None
    ) -> NormalizedResult:
        """
        Normalize a user query through the complete pipeline.
        
        Parameters:
            query: User's product search query
            user_responses: Optional dict of {field_name: user_answer}
        
        Returns:
            NormalizedResult with parsed, validated, and clarified data
        """
        # Step 1: Parse the query
        parsed = self.parser.parse(query)

        # Step 2: Run clarification (if needed or responses provided)
        if user_responses or self.detector.is_ambiguous(parsed):
            result = self.clarifier.clarify_query(parsed, user_responses)
        else:
            result = self.validator.validate_query(parsed)

        return result

    def get_ambiguities(self, query: str) -> list[ClarificationRequest]:
        """Get ambiguities for a query without full normalization."""
        parsed = self.parser.parse(query)
        return self.detector.detect_ambiguities(parsed)

    def get_summary(self, query: str) -> str:
        """Get a human-readable summary of parsed and ambiguous fields."""
        parsed = self.parser.parse(query)
        summary = f"Query: {query}\n"
        summary += f"Product: {parsed.product_type.value}\n"
        summary += f"Price: {parsed.price_range or 'Not specified'}\n"
        summary += f"Contexts: {[c.value for c in parsed.usage_context] or 'Not specified'}\n"
        summary += f"Features: {parsed.feature_preferences or 'Not specified'}\n"
        summary += f"Confidence: {parsed.confidence_score:.0%}\n\n"
        summary += self.detector.get_ambiguity_summary(parsed)
        return summary


def demo_interactive_scenario():
    """Demonstrate an interactive clarification scenario."""
    normalizer = ProductQueryNormalizer()

    # Scenario 1: Vague query
    print("=" * 70)
    print("SCENARIO 1: Vague Query")
    print("=" * 70)
    query1 = "Best headphones around 4k for gym"
    print(f"\nUser Query: {query1}\n")

    # First pass: Parse and detect ambiguities
    result1 = normalizer.normalize(query1)
    print("Initial Parse Result:")
    print(f"  Product Type: {result1.parsed_query.product_type.value}")
    print(f"  Price Range: {result1.parsed_query.price_range}")
    print(f"  Usage Context: {[c.value for c in result1.parsed_query.usage_context]}")
    print(f"  Features: {result1.parsed_query.feature_preferences}")
    print(f"  Confidence: {result1.parsed_query.confidence_score:.0%}")

    # Detect ambiguities and show clarification questions
    ambiguities = normalizer.get_ambiguities(query1)
    if ambiguities:
        print(f"\nFound {len(ambiguities)} clarification needed:")
        for i, amb in enumerate(ambiguities, 1):
            print(f"  {i}. {amb.question}")
            if amb.options and len(amb.options) <= 5:
                print(f"     Options: {', '.join(amb.options)}")

    # Second pass: With user clarifications
    print("\n" + "-" * 70)
    print("After User Clarification:")
    print("-" * 70)

    user_responses = {
        "feature_preferences": "noise-cancelling, waterproof",
    }

    result1_clarified = normalizer.normalize(query1, user_responses)
    print(f"  Features (updated): {result1_clarified.parsed_query.feature_preferences}")
    print(f"  Valid: {result1_clarified.is_valid}")
    if result1_clarified.validation_errors:
        print(f"  Errors: {result1_clarified.validation_errors}")

    # Scenario 2: Incomplete query
    print("\n" * 2 + "=" * 70)
    print("SCENARIO 2: Incomplete Query")
    print("=" * 70)
    query2 = "gaming laptop"
    print(f"\nUser Query: {query2}\n")

    result2 = normalizer.normalize(query2)
    print("Parse Result:")
    print(f"  Product Type: {result2.parsed_query.product_type.value}")
    print(f"  Price Range: {result2.parsed_query.price_range}")
    print(f"  Complete: {result2.parsed_query.is_complete}")
    print(f"  Missing Fields: {result2.parsed_query.missing_fields}")

    ambiguities2 = normalizer.get_ambiguities(query2)
    print(f"\nClarifications Needed ({len(ambiguities2)}):")
    for amb in ambiguities2:
        print(f"  • {amb.question}")

    # Scenario 3: With budget validation
    print("\n" * 2 + "=" * 70)
    print("SCENARIO 3: Budget Validation")
    print("=" * 70)
    query3 = "cheap phone for office"
    print(f"\nUser Query: {query3}\n")

    result3 = normalizer.normalize(query3)
    print(f"Parsed Product: {result3.parsed_query.product_type.value}")
    print(f"Price Range: {result3.parsed_query.price_range}")
    print(f"Valid: {result3.is_valid}")
    if result3.validation_errors:
        print(f"Validation Errors:")
        for error in result3.validation_errors:
            print(f"  • {error}")

    # Scenario 4: Complete query
    print("\n" * 2 + "=" * 70)
    print("SCENARIO 4: Complete Query")
    print("=" * 70)
    query4 = "Waterproof earbuds under 5000 for outdoor activities"
    print(f"\nUser Query: {query4}\n")

    result4 = normalizer.normalize(query4)
    print(f"Product Type: {result4.parsed_query.product_type.value}")
    print(f"Price Range: {result4.parsed_query.price_range}")
    print(f"Usage Context: {[c.value for c in result4.parsed_query.usage_context]}")
    print(f"Features: {result4.parsed_query.feature_preferences}")
    print(f"Complete: {result4.parsed_query.is_complete}")
    print(f"Valid: {result4.is_valid}")


if __name__ == "__main__":
    demo_interactive_scenario()
