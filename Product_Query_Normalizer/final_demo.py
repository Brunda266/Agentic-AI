from normalizer import ProductQueryNormalizer

normalizer = ProductQueryNormalizer()

print('=' * 70)
print('FINAL COMPREHENSIVE DEMO')
print('=' * 70)

test_cases = [
    'Best headphones around 4k for gym',
    'gaming laptop under 100000',
    'i need a good camera',
    'Waterproof earbuds under 5000 for outdoor activities',
]

for i, query in enumerate(test_cases, 1):
    print(f'\n[Test {i}] {query}')
    print('-' * 70)
    
    result = normalizer.normalize(query)
    p = result.parsed_query
    
    price_str = str(p.price_range) if p.price_range else "Not specified"
    contexts = [c.value for c in p.usage_context] if p.usage_context else ["Not specified"]
    features = p.feature_preferences if p.feature_preferences else ["Not specified"]
    
    print(f'  Product Type: {p.product_type.value}')
    print(f'  Price Range: {price_str}')
    print(f'  Usage Context: {contexts}')
    print(f'  Features: {features}')
    print(f'  Confidence: {p.confidence_score:.0%}')
    print(f'  Complete: {"YES" if p.is_complete else "NO"}')
    print(f'  Valid: {"YES" if result.is_valid else "NO"}')
    
    if p.missing_fields:
        print(f'  Missing: {p.missing_fields}')

print('\n' + '=' * 70)
print('SUCCESS: ALL TESTS COMPLETED')
print('=' * 70)
