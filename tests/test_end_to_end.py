#!/usr/bin/env python3
"""
End-to-end test to verify the complete system works correctly.
Tests intent parsing, city validation, and itinerary generation.
"""

from intent import parse_intent, _parse_intent_simple
from planner import build_itinerary
from data_sources import is_city_supported, get_supported_cities


def test_web_app_examples():
    """Test all the example prompts from the web app."""
    examples = [
        {
            'title': 'Cultural Tokyo',
            'prompt': 'Plan a 3-day trip to Tokyo for food and culture',
            'expected_city': 'Tokyo',
            'expected_days': 3,
        },
        {
            'title': 'Architecture in Barcelona',
            'prompt': 'I want to visit Barcelona for 2 days, focus on architecture',
            'expected_city': 'Barcelona',
            'expected_days': 2,
        },
        {
            'title': 'Family Singapore',
            'prompt': 'Family trip to Singapore for 4 days, kid-friendly',
            'expected_city': 'Singapore',
            'expected_days': 4,
        },
        {
            'title': 'Paris Highlights',
            'prompt': 'Show me Paris highlights for 3 days',
            'expected_city': 'Paris',
            'expected_days': 3,
        },
        {
            'title': 'New York Adventure',
            'prompt': 'Plan a 5-day trip to New York',
            'expected_city': 'New York',
            'expected_days': 5,
        },
        {
            'title': 'London Culture',
            'prompt': 'London trip for 3 days, museums and history',
            'expected_city': 'London',
            'expected_days': 3,
        },
    ]

    print('=' * 70)
    print('TEST 1: Web App Example Prompts')
    print('=' * 70)

    passed = 0
    failed = 0

    for example in examples:
        print(f"\nTesting: {example['title']}")
        print(f"Prompt: \"{example['prompt']}\"")

        # Use fallback parser since we may not have Anthropic API key
        intent = _parse_intent_simple(example['prompt'])

        # Check destination
        if not intent.destination:
            print(f"  ✗ FAILED: No destination parsed")
            failed += 1
            continue

        if intent.destination != example['expected_city']:
            print(f"  ✗ FAILED: Expected {example['expected_city']}, got {intent.destination}")
            failed += 1
            continue

        # Check if supported
        if not is_city_supported(intent.destination):
            print(f"  ✗ FAILED: City {intent.destination} not supported")
            failed += 1
            continue

        # Check days
        days = intent.days if intent.days else 3  # Default to 3
        if days != example['expected_days']:
            print(f"  ⚠ WARNING: Expected {example['expected_days']} days, got {days}")

        # Try to build itinerary
        try:
            itinerary = build_itinerary(intent)
            print(f"  ✓ SUCCESS: Generated {itinerary.days}-day itinerary with {len(itinerary.items)} activities")
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: Error building itinerary: {e}")
            failed += 1

    print(f"\n{'-' * 70}")
    print(f"Results: {passed}/{len(examples)} passed")
    return failed == 0


def test_edge_cases():
    """Test edge cases and various input formats."""
    test_cases = [
        ('tokyo', 'Tokyo'),
        ('TOKYO', 'Tokyo'),
        ('tokyo.', 'Tokyo'),
        ('new york', 'New York'),
        ('NEW YORK', 'New York'),
        ('visit Paris', 'Paris'),
        ('Show me Barcelona attractions', 'Barcelona'),
    ]

    print('\n')
    print('=' * 70)
    print('TEST 2: Edge Cases & Various Formats')
    print('=' * 70)

    passed = 0
    failed = 0

    for prompt, expected_city in test_cases:
        print(f"\nTesting: \"{prompt}\"")
        intent = _parse_intent_simple(prompt)

        if not intent.destination:
            print(f"  ✗ FAILED: No destination parsed")
            failed += 1
            continue

        if expected_city.lower() not in intent.destination.lower():
            print(f"  ✗ FAILED: Expected {expected_city}, got {intent.destination}")
            failed += 1
            continue

        if not is_city_supported(intent.destination):
            print(f"  ✗ FAILED: City {intent.destination} not supported")
            failed += 1
            continue

        print(f"  ✓ SUCCESS: Parsed as {intent.destination} (supported)")
        passed += 1

    print(f"\n{'-' * 70}")
    print(f"Results: {passed}/{len(test_cases)} passed")
    return failed == 0


def test_city_normalization():
    """Test city name normalization."""
    print('\n')
    print('=' * 70)
    print('TEST 3: City Name Normalization')
    print('=' * 70)

    test_cases = [
        'Tokyo',
        'tokyo',
        'TOKYO',
        'tokyo.',
        'new york',
        'NEW YORK',
        'Barcelona',
        'Paris',
        'London',
        'Singapore',
    ]

    passed = 0
    failed = 0

    for city in test_cases:
        supported = is_city_supported(city)
        status = '✓' if supported else '✗'
        print(f"{status} '{city:20}' -> {'Supported' if supported else 'Not supported'}")
        if supported:
            passed += 1
        else:
            failed += 1

    print(f"\n{'-' * 70}")
    print(f"Results: {passed}/{len(test_cases)} passed")
    return failed == 0


def main():
    """Run all tests."""
    print('\n')
    print('=' * 70)
    print(' ' * 20 + 'END-TO-END TEST SUITE')
    print('=' * 70)
    print()
    print(f"Supported cities: {', '.join(get_supported_cities())}")
    print()

    results = []
    results.append(('Web App Examples', test_web_app_examples()))
    results.append(('Edge Cases', test_edge_cases()))
    results.append(('City Normalization', test_city_normalization()))

    # Summary
    print('\n')
    print('=' * 70)
    print('FINAL SUMMARY')
    print('=' * 70)

    all_passed = True
    for name, passed in results:
        status = '✓ PASS' if passed else '✗ FAIL'
        print(f"{status}: {name}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print('🎉 ALL TESTS PASSED! System is fully functional.')
        return 0
    else:
        print('⚠️  SOME TESTS FAILED')
        return 1


if __name__ == '__main__':
    exit(main())
