#!/usr/bin/env python3
"""
Test script to verify city name normalization works correctly.

Demonstrates that city matching is now case-insensitive and handles
punctuation, spaces, and various formatting.
"""

from data_sources import fetch_pois, _normalize_city_name


def print_separator(char='=', length=80):
    print(char * length)


def test_normalization():
    """Test the normalization function directly."""
    print_separator()
    print("TEST 1: CITY NAME NORMALIZATION")
    print_separator()

    test_cases = [
        ("tokyo", "Tokyo"),
        ("TOKYO", "Tokyo"),
        ("Tokyo", "Tokyo"),
        ("tokyo.", "Tokyo"),
        ("tokyo!", "Tokyo"),
        ("  tokyo  ", "Tokyo"),
        ("new york", "New York"),
        ("NEW YORK", "New York"),
        ("New York", "New York"),
        ("new york.", "New York"),
        ("BARCELONA", "Barcelona"),
        ("paris", "Paris"),
    ]

    passed = 0
    for input_city, expected in test_cases:
        result = _normalize_city_name(input_city)
        status = "✓" if result == expected else "✗"
        if result == expected:
            passed += 1
        print(f"{status} '{input_city:15}' -> '{result:15}' (expected: '{expected}')")

    print(f"\nResult: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_poi_fetching():
    """Test that POI fetching works with various city name formats."""
    print("\n")
    print_separator()
    print("TEST 2: POI FETCHING WITH VARIOUS FORMATS")
    print_separator()

    test_cases = [
        ("tokyo.", "Tokyo with period"),
        ("TOKYO", "Tokyo all caps"),
        ("tokyo", "Tokyo lowercase"),
        ("new york", "New York lowercase"),
        ("NEW YORK", "New York all caps"),
        ("New York", "New York title case"),
        ("barcelona", "Barcelona lowercase"),
        ("PARIS", "Paris all caps"),
        ("  london  ", "London with spaces"),
    ]

    passed = 0
    for city_input, description in test_cases:
        pois = fetch_pois(city_input)
        status = "✓" if pois else "✗"
        if pois:
            passed += 1
        print(f"{status} {description:30} -> {len(pois)} POIs")

    print(f"\nResult: {passed}/{len(test_cases)} tests passed")
    return passed == len(test_cases)


def test_original_issue():
    """Test the original reported issue: 'tokyo.' not working."""
    print("\n")
    print_separator()
    print("TEST 3: ORIGINAL REPORTED ISSUE")
    print_separator()

    print("Issue: 'tokyo.' doesn't work")
    print()

    # Test the specific case reported
    pois = fetch_pois("tokyo.")
    if pois:
        print(f"✓ SUCCESS: 'tokyo.' returns {len(pois)} POIs")
        print(f"  First 3 POIs:")
        for poi in pois[:3]:
            print(f"    - {poi['name']} ({poi['area']})")
        return True
    else:
        print("✗ FAILED: 'tokyo.' returns no POIs")
        return False


def test_all_supported_cities():
    """Test all supported cities with various formats."""
    print("\n")
    print_separator()
    print("TEST 4: ALL SUPPORTED CITIES")
    print_separator()

    cities = ["Tokyo", "Barcelona", "Singapore", "Paris", "New York", "London"]
    formats = [
        lambda c: c.lower(),
        lambda c: c.upper(),
        lambda c: c.title(),
        lambda c: c.lower() + ".",
        lambda c: f"  {c}  ",
    ]

    all_passed = True
    for city in cities:
        city_passed = True
        for fmt in formats:
            formatted = fmt(city)
            pois = fetch_pois(formatted)
            if not pois:
                print(f"✗ {city}: '{formatted}' failed")
                city_passed = False
                all_passed = False

        if city_passed:
            print(f"✓ {city}: All formats work")

    return all_passed


def main():
    """Run all tests."""
    print("\n")
    print_separator('=')
    print(" " * 20 + "CITY NAME NORMALIZATION TEST SUITE")
    print_separator('=')
    print()

    results = []

    # Run all tests
    results.append(("Normalization", test_normalization()))
    results.append(("POI Fetching", test_poi_fetching()))
    results.append(("Original Issue", test_original_issue()))
    results.append(("All Cities", test_all_supported_cities()))

    # Summary
    print("\n")
    print_separator('=')
    print("SUMMARY")
    print_separator('=')

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print()
    if passed == total:
        print(f"🎉 ALL TESTS PASSED ({passed}/{total}) 🎉")
        return 0
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed}/{total})")
        return 1


if __name__ == "__main__":
    exit(main())
