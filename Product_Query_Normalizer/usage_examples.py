"""
Complete usage examples and API reference for Product Query Normalizer.

This module demonstrates all ways to use the normalizer system programmatically.
"""

from normalizer import ProductQueryNormalizer
from parser import QueryParser
from ambiguity_detector import AmbiguityDetector
from validator import QueryValidator, InteractiveClarifier


# ============================================================================
# BASIC USAGE: Single-line normalization
# ============================================================================

def basic_usage():
    """Simplest way to normalize a query."""
    normalizer = ProductQueryNormalizer()
    
    result = normalizer.normalize("Best headphones around 4k for gym")
    
    print("Product:", result.parsed_query.product_type.value)
    print("Price:", result.parsed_query.price_range)
    print("Valid:", result.is_valid)


# ============================================================================
# ADVANCED USAGE: Step-by-step control
# ============================================================================

def step_by_step_control():
    """Control each step of the normalization process separately."""
    
    parser = QueryParser()
    detector = AmbiguityDetector()
    validator = QueryValidator()
    clarifier = InteractiveClarifier()
    
    query = "gaming laptop"
    
    # Step 1: Parse the query
    parsed = parser.parse(query)
    print(f"Step 1 - Parsed:")
    print(f"  Product: {parsed.product_type.value}")
    print(f"  Price: {parsed.price_range}")
    print(f"  Complete: {parsed.is_complete}")
    
    # Step 2: Detect ambiguities
    ambiguities = detector.detect_ambiguities(parsed)
    print(f"\nStep 2 - Found {len(ambiguities)} ambiguities:")
    for amb in ambiguities:
        print(f"  • {amb.field_label}: {amb.question}")
    
    # Step 3: Get clarifications from user (simulated)
    user_responses = {
        "price_range": "75000",
        "feature_preferences": "RTX graphics, fast processor",
    }
    
    # Step 4: Apply clarifications
    result = clarifier.clarify_query(parsed, user_responses)
    print(f"\nStep 3 - After clarification:")
    print(f"  Features: {result.parsed_query.feature_preferences}")
    print(f"  Valid: {result.is_valid}")
    
    # Step 5: Validate business rules
    print(f"\nStep 4 - Validation:")
    print(f"  Errors: {result.validation_errors or 'None'}")


# ============================================================================
# DETECTING AMBIGUITIES AND GETTING HELP TEXT
# ============================================================================

def ambiguity_detection_example():
    """Show how to detect and display ambiguities to users."""
    normalizer = ProductQueryNormalizer()
    
    ambiguous_query = "something good"
    
    # Get ambiguities without full normalization
    ambiguities = normalizer.get_ambiguities(ambiguous_query)
    
    print(f"Found {len(ambiguities)} ambiguities in: '{ambiguous_query}'\n")
    
    for i, amb in enumerate(ambiguities, 1):
        print(f"{i}. {amb.field_label}")
        print(f"   Question: {amb.question}")
        if amb.options:
            print(f"   Options: {', '.join(amb.options[:5])}")
            if len(amb.options) > 5:
                print(f"            ... and {len(amb.options) - 5} more")
        print()


# ============================================================================
# DETAILED QUERY SUMMARY
# ============================================================================

def detailed_summary_example():
    """Show detailed summary of parsed query and ambiguities."""
    normalizer = ProductQueryNormalizer()
    
    query = "waterproof earbuds"
    summary = normalizer.get_summary(query)
    print(summary)


# ============================================================================
# BATCH PROCESSING MULTIPLE QUERIES
# ============================================================================

def batch_processing_example():
    """Process multiple queries in batch."""
    normalizer = ProductQueryNormalizer()
    
    queries = [
        "Best headphones around 4k for gym",
        "gaming laptop under 100000",
        "cheap phone",
        "professional camera for streaming",
        "waterproof speakers for beach",
    ]
    
    results = []
    for query in queries:
        result = normalizer.normalize(query)
        results.append({
            "query": query,
            "product": result.parsed_query.product_type.value,
            "price": result.parsed_query.price_range,
            "complete": result.parsed_query.is_complete,
            "valid": result.is_valid,
        })
    
    # Display as table
    print(f"{'Query':<35} {'Product':<12} {'Complete':<10} {'Valid':<8}")
    print("-" * 65)
    for r in results:
        query_short = r["query"][:35]
        product = r["product"]
        complete = "✓" if r["complete"] else "✗"
        valid = "✓" if r["valid"] else "✗"
        print(f"{query_short:<35} {product:<12} {complete:<10} {valid:<8}")


# ============================================================================
# INTERACTIVE USER LOOP SIMULATION
# ============================================================================

def interactive_user_loop_simulation():
    """Simulate an interactive conversation with user."""
    normalizer = ProductQueryNormalizer()
    
    print("=== Product Search Simulator ===\n")
    
    # User enters initial query
    user_query = "laptop for work"
    print(f"User: {user_query}\n")
    
    # System analyzes
    ambiguities = normalizer.get_ambiguities(user_query)
    print(f"System: I found your query a bit vague. Let me ask a few questions.\n")
    
    # Collect responses
    responses = {}
    
    for amb in ambiguities:
        print(f"System: {amb.question}")
        
        if amb.options and len(amb.options) <= 5:
            print(f"Options: {', '.join(amb.options)}")
        
        # Simulate user response
        if amb.field_name == "price_range":
            responses[amb.field_name] = "60000"
            print("User: 60000\n")
        elif amb.field_name == "feature_preferences":
            responses[amb.field_name] = "lightweight, long battery"
            print("User: lightweight, long battery\n")
        else:
            responses[amb.field_name] = amb.options[0] if amb.options else ""
            print(f"User: {responses[amb.field_name]}\n")
    
    # Apply clarifications
    result = normalizer.normalize(user_query, responses)
    
    print("System: Perfect! Here's what I understood:")
    print(f"  • Product: {result.parsed_query.product_type.value}")
    print(f"  • Budget: ₹{result.parsed_query.price_range.min_price:.0f} - "
          f"₹{result.parsed_query.price_range.max_price:.0f}")
    print(f"  • Features: {', '.join(result.parsed_query.feature_preferences)}")
    print(f"  • Status: {'✓ Ready to search' if result.is_valid else '✗ Needs fixing'}")


# ============================================================================
# PARSING WITH CONFIDENCE SCORES
# ============================================================================

def confidence_analysis_example():
    """Analyze confidence scores of parsed fields."""
    parser = QueryParser()
    
    test_queries = [
        "headphones",                          # Very specific
        "headphones for gym",                  # More specific
        "best headphones around 4k",           # Most specific
        "good audio around 4000",              # Less specific
        "something for listening",             # Very vague
    ]
    
    print(f"{'Query':<40} {'Product':<15} {'Confidence':<12}")
    print("-" * 67)
    
    for query in test_queries:
        parsed = parser.parse(query)
        product = parsed.product_type.value
        confidence = f"{parsed.confidence_score:.0%}"
        print(f"{query:<40} {product:<15} {confidence:<12}")


# ============================================================================
# BUDGET VALIDATION AND RECOMMENDATIONS
# ============================================================================

def budget_validation_example():
    """Show budget validation and recommendations."""
    validator = QueryValidator()
    from schemas import ProductTypeEnum, PriceRange
    
    test_cases = [
        (ProductTypeEnum.HEADPHONES, PriceRange(min_price=800, max_price=2000)),
        (ProductTypeEnum.LAPTOP, PriceRange(min_price=800, max_price=2000)),  # Too low
        (ProductTypeEnum.CAMERA, PriceRange(min_price=2000, max_price=500000)), # Reasonable
    ]
    
    for product_type, price_range in test_cases:
        print(f"\n{product_type.value.upper()}")
        print(f"  Budget: ₹{price_range.min_price:.0f} - ₹{price_range.max_price:.0f}")
        
        is_valid, warnings = validator.validate_against_product_type(
            product_type, price_range
        )
        
        print(f"  Valid: {'✓' if is_valid else '✗'}")
        if warnings:
            for warning in warnings:
                print(f"  ⚠️  {warning}")
        
        recommendation = validator.get_budget_recommendation(product_type)
        print(f"  💡 {recommendation}")


# ============================================================================
# WORKING WITH PARSED QUERY OBJECTS
# ============================================================================

def parsed_query_manipulation():
    """Demonstrate working with ParsedQuery objects."""
    parser = QueryParser()
    from schemas import ProductTypeEnum, UsageContextEnum
    
    # Parse a query
    parsed = parser.parse("headphones for gym under 5000")
    
    # Examine properties
    print("ParsedQuery Properties:")
    print(f"  product_type: {parsed.product_type}")
    print(f"  price_range: ₹{parsed.price_range.min_price:.0f}-{parsed.price_range.max_price:.0f}")
    print(f"  usage_context: {[c.value for c in parsed.usage_context]}")
    print(f"  feature_preferences: {parsed.feature_preferences}")
    print(f"  confidence_score: {parsed.confidence_score:.0%}")
    print(f"  is_complete: {parsed.is_complete}")
    print(f"  missing_fields: {parsed.missing_fields}")
    
    # Modify and validate
    print("\nModifying the query...")
    parsed.feature_preferences.append("waterproof")
    print(f"  Updated features: {parsed.feature_preferences}")
    
    # Export as dict/JSON
    print("\nAs JSON:")
    print(parsed.model_dump_json(indent=2))


# ============================================================================
# ERROR HANDLING AND EDGE CASES
# ============================================================================

def error_handling_example():
    """Show how to handle errors and edge cases."""
    normalizer = ProductQueryNormalizer()
    
    test_cases = [
        "",                              # Empty query
        "   ",                          # Whitespace only
        "!@#$%^&*()",                   # Special characters
        None,                           # None value (would raise error)
        "a" * 1000,                     # Very long query
    ]
    
    for query in test_cases:
        try:
            if query is None:
                print(f"Query: None → Skipped (None type)")
                continue
                
            if not query or not query.strip():
                print(f"Query: '{query}' → Empty query skipped")
                continue
            
            result = normalizer.normalize(query)
            print(f"Query: '{query[:50]}...' → {result.parsed_query.product_type.value}")
        except Exception as e:
            print(f"Query: '{str(query)[:50]}' → Error: {type(e).__name__}")


# ============================================================================
# MAIN DEMO
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PRODUCT QUERY NORMALIZER - USAGE EXAMPLES")
    print("=" * 80)
    
    examples = [
        ("Basic Usage", basic_usage),
        ("Step-by-Step Control", step_by_step_control),
        ("Ambiguity Detection", ambiguity_detection_example),
        ("Detailed Summary", detailed_summary_example),
        ("Batch Processing", batch_processing_example),
        ("Interactive Loop Simulation", interactive_user_loop_simulation),
        ("Confidence Analysis", confidence_analysis_example),
        ("Budget Validation", budget_validation_example),
        ("Parsed Query Manipulation", parsed_query_manipulation),
        ("Error Handling", error_handling_example),
    ]
    
    for title, func in examples:
        print(f"\n{'=' * 80}")
        print(f"EXAMPLE: {title}")
        print(f"{'=' * 80}\n")
        try:
            func()
        except Exception as e:
            print(f"Error in {title}: {e}")
        
        input("\nPress Enter to continue...")
