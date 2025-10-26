#!/usr/bin/env python3
"""
Comprehensive test script to verify all components work correctly.
This script tests all the fixes and identifies any remaining issues.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    print("=" * 70)
    print("TEST 1: Module Imports")
    print("=" * 70)

    tests = []

    # Test data_sources
    try:
        from data_sources import fetch_pois, get_supported_cities, is_city_supported
        print("✓ data_sources imported successfully")
        tests.append(True)
    except Exception as e:
        print(f"✗ data_sources import failed: {e}")
        tests.append(False)

    # Test intent parser
    try:
        from intent import parse_intent, _parse_intent_simple, TripIntent
        print("✓ intent module imported successfully")
        tests.append(True)
    except Exception as e:
        print(f"✗ intent import failed: {e}")
        tests.append(False)

    # Test planner
    try:
        from planner import build_itinerary
        print("✓ planner module imported successfully")
        tests.append(True)
    except Exception as e:
        print(f"✗ planner import failed: {e}")
        tests.append(False)

    # Test exporters
    try:
        from exporters import itinerary_to_markdown, itinerary_to_ics
        print("✓ exporters module imported successfully")
        tests.append(True)
    except Exception as e:
        print(f"✗ exporters import failed: {e}")
        tests.append(False)

    print(f"\nResult: {sum(tests)}/{len(tests)} modules imported successfully")
    return all(tests)


def test_city_validation():
    """Test city validation and normalization."""
    print("\n")
    print("=" * 70)
    print("TEST 2: City Validation & Normalization")
    print("=" * 70)

    from data_sources import is_city_supported, get_supported_cities

    print(f"Supported cities: {', '.join(get_supported_cities())}")
    print()

    test_cases = [
        ('Tokyo', True),
        ('tokyo', True),
        ('TOKYO', True),
        ('tokyo.', True),
        ('new york', True),
        ('NEW YORK', True),
        ('Paris', True),
        ('Unknown City', False),
    ]

    passed = 0
    failed = 0

    for city, expected in test_cases:
        result = is_city_supported(city)
        status = '✓' if result == expected else '✗'
        if result == expected:
            passed += 1
        else:
            failed += 1
        print(f"{status} is_city_supported('{city}') = {result} (expected: {expected})")

    print(f"\nResult: {passed}/{len(test_cases)} tests passed")
    return failed == 0


def test_intent_parsing():
    """Test intent parsing with various formats."""
    print("\n")
    print("=" * 70)
    print("TEST 3: Intent Parsing")
    print("=" * 70)

    from intent import _parse_intent_simple

    test_cases = [
        ('Plan a 3-day trip to Tokyo', 'Tokyo', 3),
        ('Show me Paris highlights', 'Paris', None),
        ('tokyo.', 'Tokyo', None),
        ('TOKYO', 'Tokyo', None),
        ('visit new york', 'New York', None),
    ]

    passed = 0
    failed = 0

    for prompt, expected_city, expected_days in test_cases:
        intent = _parse_intent_simple(prompt)

        city_match = intent.destination and expected_city.lower() in intent.destination.lower()
        days_match = expected_days is None or intent.days == expected_days

        if city_match and days_match:
            status = '✓'
            passed += 1
        else:
            status = '✗'
            failed += 1

        print(f"{status} '{prompt}'")
        print(f"   -> {intent.destination} (expected: {expected_city})")
        if expected_days:
            print(f"   -> {intent.days} days (expected: {expected_days})")

    print(f"\nResult: {passed}/{len(test_cases)} tests passed")
    return failed == 0


def test_end_to_end():
    """Test complete end-to-end flow."""
    print("\n")
    print("=" * 70)
    print("TEST 4: End-to-End Trip Planning")
    print("=" * 70)

    from intent import _parse_intent_simple
    from planner import build_itinerary
    from data_sources import is_city_supported

    test_prompts = [
        'Plan a 3-day trip to Tokyo',
        'Show me Paris highlights for 3 days',
        'visit Barcelona for 2 days',
    ]

    passed = 0
    failed = 0

    for prompt in test_prompts:
        print(f"\nTesting: '{prompt}'")

        try:
            # Parse intent
            intent = _parse_intent_simple(prompt)
            print(f"  ✓ Parsed: {intent.destination}, {intent.days} days")

            # Validate city
            if not intent.destination:
                print(f"  ✗ No destination found")
                failed += 1
                continue

            if not is_city_supported(intent.destination):
                print(f"  ✗ City {intent.destination} not supported")
                failed += 1
                continue

            print(f"  ✓ City {intent.destination} is supported")

            # Set default days if needed
            if not intent.days:
                intent.days = 3

            # Build itinerary
            itinerary = build_itinerary(intent)
            print(f"  ✓ Generated {itinerary.days}-day itinerary with {len(itinerary.items)} activities")

            passed += 1

        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print(f"\nResult: {passed}/{len(test_prompts)} tests passed")
    return failed == 0


def test_web_app_examples():
    """Test all web app example prompts."""
    print("\n")
    print("=" * 70)
    print("TEST 5: Web App Example Prompts")
    print("=" * 70)

    from intent import _parse_intent_simple
    from planner import build_itinerary
    from data_sources import is_city_supported

    examples = [
        ('Plan a 3-day trip to Tokyo for food and culture', 'Tokyo'),
        ('I want to visit Barcelona for 2 days, focus on architecture', 'Barcelona'),
        ('Family trip to Singapore for 4 days, kid-friendly', 'Singapore'),
        ('Show me Paris highlights for 3 days', 'Paris'),
        ('Plan a 5-day trip to New York', 'New York'),
        ('London trip for 3 days, museums and history', 'London'),
    ]

    passed = 0
    failed = 0

    for prompt, expected_city in examples:
        intent = _parse_intent_simple(prompt)

        if intent.destination and expected_city.lower() in intent.destination.lower():
            if is_city_supported(intent.destination):
                status = '✓'
                passed += 1
                print(f"{status} '{prompt[:50]}...' -> {intent.destination}")
            else:
                status = '✗'
                failed += 1
                print(f"{status} '{prompt[:50]}...' -> {intent.destination} (not supported!)")
        else:
            status = '✗'
            failed += 1
            print(f"{status} '{prompt[:50]}...' -> {intent.destination} (expected: {expected_city})")

    print(f"\nResult: {passed}/{len(examples)} tests passed")
    return failed == 0


def main():
    """Run all tests."""
    print("\n")
    print("=" * 70)
    print(" " * 15 + "COMPREHENSIVE SYSTEM TEST")
    print("=" * 70)
    print()

    results = []

    # Run all tests
    results.append(('Module Imports', test_imports()))
    results.append(('City Validation', test_city_validation()))
    results.append(('Intent Parsing', test_intent_parsing()))
    results.append(('End-to-End Flow', test_end_to_end()))
    results.append(('Web App Examples', test_web_app_examples()))

    # Summary
    print("\n")
    print("=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    all_passed = True
    for name, passed in results:
        status = '✓ PASS' if passed else '✗ FAIL'
        print(f"{status}: {name}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print("🎉 ALL TESTS PASSED! System is fully functional.")
        print()
        print("Next steps:")
        print("  1. Install web dependencies: pip install flask flask-cors")
        print("  2. Start the web app: ./start_web_app.sh")
        print("  3. Or run the agent: python agent.py")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED - See details above")
        return 1


if __name__ == '__main__':
    exit(main())
