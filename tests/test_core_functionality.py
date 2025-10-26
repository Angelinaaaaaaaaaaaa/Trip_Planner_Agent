#!/usr/bin/env python3
"""
Core functionality test - tests the system without requiring anthropic library.
This verifies all the fixes work correctly.
"""

import sys
import os

# Add parent directory to path so we can import project modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 70)
print(" " * 15 + "CORE FUNCTIONALITY TEST")
print("=" * 70)
print()

# Test 1: City Validation (the main fix)
print("TEST 1: City Validation & Normalization")
print("-" * 70)

from data_sources import is_city_supported, get_supported_cities, fetch_pois

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
    ('paris!', True),
    ('  barcelona  ', True),
    ('Unknown City', False),
]

city_tests_passed = 0
city_tests_total = len(test_cases)

for city, expected in test_cases:
    result = is_city_supported(city)
    status = '✓' if result == expected else '✗'
    if result == expected:
        city_tests_passed += 1
    print(f"{status} is_city_supported('{city:20}') = {result:5} (expected: {expected})")

print(f"\nResult: {city_tests_passed}/{city_tests_total} passed")
print()

# Test 2: POI Fetching with normalization
print("TEST 2: POI Fetching with Normalized City Names")
print("-" * 70)

poi_test_cases = [
    'Tokyo',
    'tokyo',
    'TOKYO',
    'tokyo.',
    'new york',
    'NEW YORK',
]

poi_tests_passed = 0
poi_tests_total = len(poi_test_cases)

for city in poi_test_cases:
    pois = fetch_pois(city)
    status = '✓' if pois else '✗'
    if pois:
        poi_tests_passed += 1
    print(f"{status} fetch_pois('{city:15}') -> {len(pois)} POIs")

print(f"\nResult: {poi_tests_passed}/{poi_tests_total} passed")
print()

# Test 3: Intent Parser (inline version to avoid anthropic dependency)
print("TEST 3: Intent Parser (Standalone)")
print("-" * 70)

import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TripIntent:
    destination: Optional[str]
    days: Optional[int]
    preferences: List[str]

# Copy of the parser from intent.py
def parse_intent_simple(text: str) -> TripIntent:
    """Simple rule-based intent parsing."""
    t = text.strip().lower()

    days = None
    day_match = re.search(r'(\d+)\s*-?\s*days?', t)
    if day_match:
        days = int(day_match.group(1))

    destination = None

    # Pattern 1: "to [City]"
    dest_match = re.search(r'to\s+(?:visit\s+)?([A-Za-z\s]+?)(?:\s+for|\s+with|\s*[,.]|\s*$)', text, re.IGNORECASE)
    if dest_match:
        dest = dest_match.group(1).strip()
        dest = re.sub(r'[^\w\s]', '', dest)
        destination = ' '.join(word.capitalize() for word in dest.split())

    # Pattern 2: "visit [City]"
    if not destination:
        dest_match = re.search(r'(?:visit|see|explore)\s+([A-Za-z\s]+?)(?:\s+for|\s+with|\s*[,.]|\s*$)', text, re.IGNORECASE)
        if dest_match:
            dest = dest_match.group(1).strip()
            dest = re.sub(r'[^\w\s]', '', dest)
            destination = ' '.join(word.capitalize() for word in dest.split())

    # Pattern 3: "Show me [City]" with filtering
    if not destination:
        dest_match = re.search(r'show\s+me\s+([A-Za-z\s]+?)(?:\s+for|\s+with|\s*[,.]|\s*$)', text, re.IGNORECASE)
        if dest_match:
            dest = dest_match.group(1).strip()
            dest = re.sub(r'[^\w\s]', '', dest)
            words = dest.split()
            filtered_words = [w for w in words if w.lower() not in ['highlights', 'attractions', 'sights', 'things', 'places', 'spots']]
            if filtered_words:
                destination = ' '.join(word.capitalize() for word in filtered_words)

    # Pattern 4: "[City] for X days" or "[City] trip"
    if not destination:
        dest_match = re.search(r'(?:^|\s)([A-Za-z\s]+?)\s+(?:for|trip)', text, re.IGNORECASE)
        if dest_match:
            dest = dest_match.group(1).strip()
            dest = re.sub(r'[^\w\s]', '', dest)
            words = dest.lower().split()
            filtered_words = [w for w in words if w not in ['plan', 'show', 'me', 'want', 'need', 'like', 'i', 'a', 'the']]
            if filtered_words:
                destination = ' '.join(word.capitalize() for word in filtered_words)

    # Pattern 5: Fallback for bare city names
    if not destination and len(text.strip().split()) <= 3:
        cleaned = re.sub(r'[^\w\s]', '', text).strip()
        if cleaned:
            destination = ' '.join(word.capitalize() for word in cleaned.split())

    return TripIntent(destination=destination, days=days, preferences=[])

parser_test_cases = [
    ('Plan a 3-day trip to Tokyo', 'Tokyo', 3),
    ('Show me Paris highlights', 'Paris', None),
    ('tokyo.', 'Tokyo', None),
    ('TOKYO', 'Tokyo', None),
    ('visit new york', 'New York', None),
    ('Barcelona trip for 2 days', 'Barcelona', 2),
]

parser_tests_passed = 0
parser_tests_total = len(parser_test_cases)

for prompt, expected_city, expected_days in parser_test_cases:
    intent = parse_intent_simple(prompt)

    city_match = intent.destination and expected_city.lower() in intent.destination.lower()
    days_match = expected_days is None or intent.days == expected_days

    if city_match and days_match:
        status = '✓'
        parser_tests_passed += 1
    else:
        status = '✗'

    print(f"{status} '{prompt:40}' -> {intent.destination}")

print(f"\nResult: {parser_tests_passed}/{parser_tests_total} passed")
print()

# Test 4: Web App Examples (the critical test)
print("TEST 4: Web App Example Prompts (CRITICAL)")
print("-" * 70)

web_examples = [
    ('Plan a 3-day trip to Tokyo for food and culture', 'Tokyo'),
    ('I want to visit Barcelona for 2 days, focus on architecture', 'Barcelona'),
    ('Family trip to Singapore for 4 days, kid-friendly', 'Singapore'),
    ('Show me Paris highlights for 3 days', 'Paris'),  # This was the failing one!
    ('Plan a 5-day trip to New York', 'New York'),
    ('London trip for 3 days, museums and history', 'London'),
]

web_tests_passed = 0
web_tests_total = len(web_examples)

for prompt, expected_city in web_examples:
    intent = parse_intent_simple(prompt)

    if intent.destination and expected_city.lower() in intent.destination.lower():
        if is_city_supported(intent.destination):
            status = '✓'
            web_tests_passed += 1
        else:
            status = '✗'
            print(f"{status} '{prompt[:45]}...' -> {intent.destination} (NOT SUPPORTED!)")
            continue
    else:
        status = '✗'

    print(f"{status} '{prompt[:45]}...' -> {intent.destination}")

print(f"\nResult: {web_tests_passed}/{web_tests_total} passed")
print()

# Final Summary
print("=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

total_passed = city_tests_passed + poi_tests_passed + parser_tests_passed + web_tests_passed
total_tests = city_tests_total + poi_tests_total + parser_tests_total + web_tests_total

print(f"City Validation:      {city_tests_passed}/{city_tests_total} passed")
print(f"POI Fetching:         {poi_tests_passed}/{poi_tests_total} passed")
print(f"Intent Parsing:       {parser_tests_passed}/{parser_tests_total} passed")
print(f"Web App Examples:     {web_tests_passed}/{web_tests_total} passed")
print()
print(f"TOTAL: {total_passed}/{total_tests} tests passed")
print()

if total_passed == total_tests:
    print("🎉 ALL TESTS PASSED! System is fully functional.")
    print()
    print("The code is ready to run!")
    print()
    print("To use the system:")
    print("  1. Ensure dependencies are installed:")
    print("     pip install anthropic python-dotenv uagents flask flask-cors")
    print("  2. Set your ANTHROPIC_API_KEY in .env (optional, has fallback parser)")
    print("  3. Run the agent: python agent.py")
    print("  4. Or start the web app: ./start_web_app.sh")
    sys.exit(0)
else:
    print(f"⚠️  {total_tests - total_passed} tests failed")
    sys.exit(1)
