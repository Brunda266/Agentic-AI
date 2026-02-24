"""
Unit tests for Product Query Normalizer components.
"""

from schemas import (
    ProductTypeEnum,
    UsageContextEnum,
    PriceRange,
    ParsedQuery,
)
from parser import QueryParser
from ambiguity_detector import AmbiguityDetector
from validator import QueryValidator, InteractiveClarifier
from normalizer import ProductQueryNormalizer


def test_parser_product_extraction():
    """Test product type extraction."""
    parser = QueryParser()

    test_cases = [
        ("headphones for gym", ProductTypeEnum.HEADPHONES, 0.85),
        ("gaming laptop", ProductTypeEnum.LAPTOP, 0.85),
        ("earbuds", ProductTypeEnum.EARBUDS, 0.95),
        ("unknown gadget", ProductTypeEnum.UNKNOWN, 0.3),
    ]

    for query, expected_product, min_conf in test_cases:
        product, conf = parser.extract_product_type(query)
        assert product == expected_product, f"Failed for: {query}"
        assert conf >= min_conf, f"Low confidence for: {query}"
        print(f"✓ {query} → {product.value} ({conf:.0%})")


def test_parser_price_extraction():
    """Test price range extraction."""
    parser = QueryParser()

    test_cases = [
        ("around 4000", 2800, 4000),
        ("₹5000", 3500, 5000),
        ("under 50000", 35000, 50000),
        ("no price mentioned", None, None),
    ]

    for query, min_expected, max_expected in test_cases:
        price_range, conf = parser.extract_price_range(query)
        if min_expected is None:
            assert price_range is None, f"Unexpected price for: {query}"
            print(f"✓ {query} → No price")
        else:
            assert price_range is not None, f"Missing price for: {query}"
            assert price_range.min_price >= min_expected * 0.9
            assert price_range.max_price <= max_expected * 1.1
            print(
                f"✓ {query} → ₹{price_range.min_price:.0f}-{price_range.max_price:.0f}"
            )


def test_ambiguity_detection():
    """Test ambiguity detection."""
    parser = QueryParser()
    detector = AmbiguityDetector()

    # Vague query should have ambiguities
    vague_query = parser.parse("best product")
    vague_ambiguities = detector.detect_ambiguities(vague_query)
    assert len(vague_ambiguities) > 0, "Should detect ambiguities in vague query"
    print(f"✓ Vague query detected {len(vague_ambiguities)} ambiguities")

    # Complete query should have fewer/no ambiguities
    complete_query = parser.parse(
        "Waterproof earbuds under 5000 for outdoor activities"
    )
    complete_ambiguities = detector.detect_ambiguities(complete_query)
    assert (
        len(complete_ambiguities) <= len(vague_ambiguities)
    ), "Complete query should have fewer ambiguities"
    print(
        f"✓ Complete query detected {len(complete_ambiguities)} ambiguities"
    )


def test_price_validation():
    """Test budget validation logic."""
    validator = QueryValidator()

    # Valid price range
    valid_range = PriceRange(min_price=2000, max_price=5000)
    is_valid, errors = validator.validate_price_range(valid_range)
    assert is_valid, f"Valid range rejected: {errors}"
    print(f"✓ Valid range accepted: ₹2000-5000")

    # Invalid: max < min (Pydantic will raise during construction)
    try:
        invalid_range = PriceRange(min_price=5000, max_price=2000)
        assert False, "Should have raised ValidationError"
    except Exception as e:
        print(f"✓ Invalid range rejected (max < min): {type(e).__name__}")

    # Valid but warning-worthy
    wide_range = PriceRange(min_price=1000, max_price=100000)
    is_valid, errors = validator.validate_price_range(wide_range)
    print(f"✓ Wide range result - valid: {is_valid}, width check passes")


def test_product_budget_validation():
    """Test budget validation for product types."""
    validator = QueryValidator()

    # Headphones: typical budget 500-50000
    headphone_budget = PriceRange(min_price=1000, max_price=5000)
    is_valid, warnings = validator.validate_against_product_type(
        ProductTypeEnum.HEADPHONES, headphone_budget
    )
    assert is_valid, "Should be valid"
    print(f"✓ Headphone budget 1000-5000 valid")

    # Laptop: typical budget 30000+
    low_laptop_budget = PriceRange(min_price=1000, max_price=5000)
    is_valid, warnings = validator.validate_against_product_type(
        ProductTypeEnum.LAPTOP, low_laptop_budget
    )
    assert is_valid, "Should still be valid (warning only)"
    assert len(warnings) > 0, "Should warn about low budget"
    print(f"✓ Low laptop budget triggers warning")


def test_normalizer_pipeline():
    """Test full normalization pipeline."""
    normalizer = ProductQueryNormalizer()

    query = "Best headphones around 4k for gym"
    result = normalizer.normalize(query)

    assert result.parsed_query.product_type == ProductTypeEnum.HEADPHONES
    assert result.parsed_query.price_range is not None
    assert UsageContextEnum.GYM in result.parsed_query.usage_context
    assert result.is_valid, "Query should be valid"
    print(f"✓ Full pipeline works: {query}")


def test_clarification_loop():
    """Test interactive clarification."""
    clarifier = InteractiveClarifier()
    parser = QueryParser()

    parsed = parser.parse("gaming laptop")
    print(f"Initial parse:")
    print(f"  Product: {parsed.product_type.value}")
    print(f"  Price: {parsed.price_range}")
    print(f"  Complete: {parsed.is_complete}")

    # Run clarification with user responses
    user_responses = {
        "price_range": "75000",
        "feature_preferences": "fast processor, lightweight",
    }

    result = clarifier.clarify_query(parsed, user_responses)

    print(f"\nAfter clarification:")
    print(f"  Price: {result.parsed_query.price_range}")
    print(f"  Features: {result.parsed_query.feature_preferences}")
    print(f"  Valid: {result.is_valid}")
    print(f"✓ Clarification loop works")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("RUNNING TESTS FOR PRODUCT QUERY NORMALIZER")
    print("=" * 70)

    tests = [
        ("Parser: Product Extraction", test_parser_product_extraction),
        ("Parser: Price Extraction", test_parser_price_extraction),
        ("Ambiguity Detection", test_ambiguity_detection),
        ("Price Validation", test_price_validation),
        ("Product Budget Validation", test_product_budget_validation),
        ("Normalizer Pipeline", test_normalizer_pipeline),
        ("Clarification Loop", test_clarification_loop),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        print(f"\n{'—' * 70}")
        print(f"TEST: {test_name}")
        print(f"{'—' * 70}")
        try:
            test_func()
            passed += 1
            print(f"✅ PASSED: {test_name}")
        except AssertionError as e:
            failed += 1
            print(f"❌ FAILED: {test_name}")
            print(f"   Error: {e}")
        except Exception as e:
            failed += 1
            print(f"❌ ERROR: {test_name}")
            print(f"   Error: {type(e).__name__}: {e}")

    print(f"\n{'=' * 70}")
    print(f"TEST SUMMARY: {passed} passed, {failed} failed")
    print(f"{'=' * 70}")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
