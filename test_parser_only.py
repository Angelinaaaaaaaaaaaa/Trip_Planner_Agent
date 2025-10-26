#!/usr/bin/env python3
"""
Test the intent parser without requiring external dependencies.
This is a standalone test that can run without the anthropic library.
"""

import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TripIntent:
    destination: Optional[str]
    days: Optional[int]
    preferences: List[str]


def parse_intent_simple(text: str) -> TripIntent:
    """
    Simple rule-based intent parsing (copy of the function from intent.py).
    """
    t = text.strip().lower()

    # Extract days
    days = None
    day_match = re.search(r'(\d+)\s*-?\s*days?', t)
    if day_match:
        days = int(day_match.group(1))

    # Extract destination - try multiple patterns
    destination = None

    # Pattern 1: "to [City]"
    dest_match = re.search(r'to\s+(?:visit\s+)?([A-Za-z\s]+?)(?:\s+for|\s+with|\s*[,.]|\s*$)', text, re.IGNORECASE)
    if dest_match:
        dest = dest_match.group(1).strip()
        dest = re.sub(r'[^\w\s]', '', dest)
        destination = ' '.join(word.capitalize() for word in dest.split())

    # Pattern 2: "visit [City]" or "see [City]"
    if not destination:
        dest_match = re.search(r'(?:visit|see|explore)\s+([A-Za-z\s]+?)(?:\s+for|\s+with|\s*[,.]|\s*$)', text, re.IGNORECASE)
        if dest_match:
            dest = dest_match.group(1).strip()
            dest = re.sub(r'[^\w\s]', '', dest)
            destination = ' '.join(word.capitalize() for word in dest.split())

    # Pattern 3: "Show me [City]" - capture only city name, filter out descriptive words
    if not destination:
        dest_match = re.search(r'show\s+me\s+([A-Za-z\s]+?)(?:\s+for|\s+with|\s*[,.]|\s*$)', text, re.IGNORECASE)
        if dest_match:
            dest = dest_match.group(1).strip()
            dest = re.sub(r'[^\w\s]', '', dest)
            # Filter out descriptive words like "highlights", "attractions", etc.
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
            # Filter out common non-city words
            words = dest.lower().split()
            filtered_words = [w for w in words if w not in ['plan', 'show', 'me', 'want', 'need', 'like', 'i', 'a', 'the']]
            if filtered_words:
                destination = ' '.join(word.capitalize() for word in filtered_words)

    # Pattern 5: Fallback - if input is very short (1-3 words), treat as city name
    # This handles bare city names like "Tokyo", "tokyo.", "New York"
    if not destination and len(text.strip().split()) <= 3:
        cleaned = re.sub(r'[^\w\s]', '', text).strip()
        if cleaned:
            destination = ' '.join(word.capitalize() for word in cleaned.split())

    # Extract preferences (simplified - not used in this test)
    preferences = []

    return TripIntent(destination=destination, days=days, preferences=preferences)


def main():
    """Run parser tests."""
    # Test cases: (prompt, expected_city, expected_days)
    test_cases = [
        # Web app examples
        ('Plan a 3-day trip to Tokyo for food and culture', 'Tokyo', 3),
        ('I want to visit Barcelona for 2 days, focus on architecture', 'Barcelona', 2),
        ('Family trip to Singapore for 4 days, kid-friendly', 'Singapore', 4),
        ('Show me Paris highlights for 3 days', 'Paris', 3),
        ('Plan a 5-day trip to New York', 'New York', 5),
        ('London trip for 3 days, museums and history', 'London', 3),
        # Edge cases
        ('tokyo', 'Tokyo', None),
        ('TOKYO', 'Tokyo', None),
        ('tokyo.', 'Tokyo', None),
        ('new york', 'New York', None),
        ('visit Paris', 'Paris', None),
        ('Show me Barcelona attractions', 'Barcelona', None),
    ]

    print('=' * 70)
    print(' ' * 20 + 'INTENT PARSER TEST')
    print('=' * 70)
    print()

    passed = 0
    failed = 0

    for prompt, expected_city, expected_days in test_cases:
        intent = parse_intent_simple(prompt)

        # Check destination
        dest_ok = intent.destination and expected_city.lower() in intent.destination.lower()

        # Check days (if specified)
        days_ok = True
        if expected_days is not None:
            days_ok = intent.days == expected_days

        if dest_ok and days_ok:
            status = '✓'
            passed += 1
        else:
            status = '✗'
            failed += 1

        print(f"{status} \"{prompt}\"")
        print(f"   -> Destination: {intent.destination} (expected: {expected_city})")
        if expected_days:
            print(f"   -> Days: {intent.days} (expected: {expected_days})")
        print()

    print('=' * 70)
    print(f"Results: {passed}/{len(test_cases)} passed, {failed} failed")
    print('=' * 70)

    if failed == 0:
        print('✅ ALL TESTS PASSED!')
        return 0
    else:
        print(f'❌ {failed} TESTS FAILED')
        return 1


if __name__ == '__main__':
    exit(main())
