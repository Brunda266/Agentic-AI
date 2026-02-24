"""
Validator and business rule enforcement for product queries.
Includes budget validation, schema compliance, and business logic checks.
"""

from typing import List, Tuple, Optional
from schemas import (
    ParsedQuery,
    PriceRange,
    ProductTypeEnum,
    NormalizedResult,
    ClarificationRequest,
)
from ambiguity_detector import AmbiguityDetector


class QueryValidator:
    """Validates parsed queries against business rules."""

    # Business rule: Minimum budget for each product type (in currency units)
    MINIMUM_BUDGET = {
        ProductTypeEnum.HEADPHONES: 500,
        ProductTypeEnum.EARBUDS: 1000,
        ProductTypeEnum.SPEAKERS: 1500,
        ProductTypeEnum.MICROPHONE: 2000,
        ProductTypeEnum.CAMERA: 15000,
        ProductTypeEnum.LAPTOP: 30000,
        ProductTypeEnum.PHONE: 10000,
        ProductTypeEnum.TABLET: 10000,
        ProductTypeEnum.WATCH: 5000,
    }

    # Business rule: Reasonable maximum budget (e.g., don't recommend 100k laptop as "gaming")
    MAXIMUM_BUDGET = {
        ProductTypeEnum.HEADPHONES: 50000,
        ProductTypeEnum.EARBUDS: 30000,
        ProductTypeEnum.SPEAKERS: 100000,
        ProductTypeEnum.MICROPHONE: 50000,
        ProductTypeEnum.CAMERA: 500000,
        ProductTypeEnum.LAPTOP: 500000,
        ProductTypeEnum.PHONE: 150000,
        ProductTypeEnum.TABLET: 100000,
        ProductTypeEnum.WATCH: 50000,
    }

    def validate_price_range(self, price_range: Optional[PriceRange]) -> Tuple[bool, List[str]]:
        """
        Validate price range business rules.
        Returns: (is_valid, error_messages)
        """
        errors = []

        if price_range is None:
            return True, []  # Price range is optional

        # Check numeric validity
        if price_range.min_price < 0 or price_range.max_price < 0:
            errors.append("Price values cannot be negative")
            return False, errors

        if price_range.max_price < price_range.min_price:
            errors.append("Maximum price must be >= minimum price")
            return False, errors

        # Check for reasonable ranges (not too wide)
        if price_range.max_price > 0 and price_range.min_price > 0:
            ratio = price_range.max_price / price_range.min_price
            if ratio > 10:
                errors.append(
                    f"Price range too wide (ratio {ratio:.1f}x). "
                    "Consider narrowing your budget for better recommendations."
                )

        return len(errors) == 0, errors

    def validate_against_product_type(
        self, product_type: ProductTypeEnum, price_range: Optional[PriceRange]
    ) -> Tuple[bool, List[str]]:
        """
        Validate price range is reasonable for product type.
        Returns: (is_valid, warnings)
        """
        warnings = []

        if price_range is None or product_type == ProductTypeEnum.UNKNOWN:
            return True, warnings

        min_budget = self.MINIMUM_BUDGET.get(product_type, 500)
        max_budget = self.MAXIMUM_BUDGET.get(product_type, 500000)

        if price_range.max_price < min_budget:
            warnings.append(
                f"Budget may be too low for {product_type.value}. "
                f"Minimum recommended: ₹{min_budget}"
            )

        if price_range.min_price > max_budget:
            warnings.append(
                f"Budget seems very high for {product_type.value}. "
                f"Maximum typical: ₹{max_budget}"
            )

        return True, warnings  # Warnings don't invalidate the query

    def validate_query(self, parsed_query: ParsedQuery) -> NormalizedResult:
        """
        Perform full validation on parsed query.
        Returns: NormalizedResult with validation status and errors.
        """
        is_valid = True
        errors = []

        # Validate price range
        price_valid, price_errors = self.validate_price_range(parsed_query.price_range)
        if not price_valid:
            is_valid = False
            errors.extend(price_errors)

        # Validate price against product type
        _, price_warnings = self.validate_against_product_type(
            parsed_query.product_type, parsed_query.price_range
        )

        # Create normalized result
        result = NormalizedResult(
            parsed_query=parsed_query,
            is_valid=is_valid,
            validation_errors=errors,
            clarifications_made=[],
        )

        return result

    def get_budget_recommendation(
        self, product_type: ProductTypeEnum
    ) -> str:
        """Get recommended budget range for a product type."""
        min_budget = self.MINIMUM_BUDGET.get(product_type, 1000)
        max_budget = self.MAXIMUM_BUDGET.get(product_type, 100000)

        return f"Recommended budget for {product_type.value}: ₹{min_budget} - ₹{max_budget}"


class InteractiveClarifier:
    """Manages interactive clarification loop with user."""

    def __init__(self):
        self.detector = AmbiguityDetector()
        self.validator = QueryValidator()

    def clarify_query(
        self, parsed_query: ParsedQuery, user_responses: Optional[dict] = None
    ) -> NormalizedResult:
        """
        Run clarification loop (simulated or interactive).
        
        Args:
            parsed_query: Initial parsed query
            user_responses: Dict mapping field names to user-provided values
        
        Returns: NormalizedResult with all clarifications applied
        """
        user_responses = user_responses or {}
        clarifications_made = []

        # Get ambiguities
        ambiguities = self.detector.detect_ambiguities(parsed_query)

        # Apply user responses to parsed query
        for ambiguity in ambiguities:
            if ambiguity.field_name in user_responses:
                response = user_responses[ambiguity.field_name]
                parsed_query = self._apply_response(parsed_query, ambiguity, response)
                clarifications_made.append(ambiguity)

        # Validate the clarified query
        validation_result = self.validator.validate_query(parsed_query)
        validation_result.clarifications_made = clarifications_made

        return validation_result

    def _apply_response(
        self, query: ParsedQuery, ambiguity: ClarificationRequest, response: str
    ) -> ParsedQuery:
        """Apply user response to update parsed query."""
        field_name = ambiguity.field_name

        if field_name == "product_type":
            try:
                query.product_type = ProductTypeEnum(response)
            except ValueError:
                pass  # Keep original if invalid

        elif field_name == "price_range":
            try:
                # Parse response as numeric value
                value = float(response.replace(",", ""))
                query.price_range = PriceRange(
                    min_price=value * 0.7,
                    max_price=value
                )
            except (ValueError, TypeError):
                pass  # Keep original if invalid

        elif field_name == "usage_context":
            from schemas import UsageContextEnum
            if response in [c.value for c in UsageContextEnum]:
                query.usage_context = [UsageContextEnum(response)]

        elif field_name == "feature_preferences":
            # Accept comma-separated features
            if isinstance(response, str):
                features = [f.strip() for f in response.split(",")]
                query.feature_preferences = features

        return query


if __name__ == "__main__":
    from parser import QueryParser

    parser = QueryParser()
    validator = QueryValidator()
    clarifier = InteractiveClarifier()

    # Test validation
    query = parser.parse("Best headphones around 4k for gym")
    print(f"Original Query: {query.original_query}")
    print(f"Product: {query.product_type.value}")
    print(f"Price: {query.price_range}")
    print()

    # Validate
    result = validator.validate_query(query)
    print(f"Valid: {result.is_valid}")
    if result.validation_errors:
        print(f"Errors: {result.validation_errors}")
    print()

    # Test clarification loop
    print("Testing clarification loop...")
    user_responses = {
        "product_type": "headphones",
        "price_range": "5000",
        "usage_context": "gym",
        "feature_preferences": "noise-cancelling, waterproof",
    }

    clarified = clarifier.clarify_query(query, user_responses)
    print(f"Clarifications Made: {len(clarified.clarifications_made)}")
    print(f"Final Query Valid: {clarified.is_valid}")
    print(f"Final Product: {clarified.parsed_query.product_type.value}")
    print(f"Final Features: {clarified.parsed_query.feature_preferences}")
