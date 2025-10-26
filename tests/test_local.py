#!/usr/bin/env python3
"""
Local test script for Trip Planner Agent
Tests the core functionality without running the full uAgent
"""

from intent import parse_intent
from planner import build_itinerary
from exporters import itinerary_to_markdown, itinerary_to_ics
from data_sources import get_supported_cities

def test_intent_parsing():
    """Test intent parsing with sample requests."""
    print("=" * 60)
    print("TEST 1: Intent Parsing")
    print("=" * 60)

    test_cases = [
        "Plan me a 3-day trip to Tokyo for food and culture",
        "I want to visit Barcelona for 2 days, focus on architecture",
        "Family trip to Singapore, kid-friendly activities"
    ]

    for test_input in test_cases:
        print(f"\nInput: {test_input}")
        intent = parse_intent(test_input)
        print(f"→ Destination: {intent.destination}")
        print(f"→ Days: {intent.days}")
        print(f"→ Preferences: {intent.preferences}")

def test_itinerary_generation():
    """Test itinerary generation."""
    print("\n" + "=" * 60)
    print("TEST 2: Itinerary Generation")
    print("=" * 60)

    # Parse a sample request
    user_input = "Plan a 3-day trip to Tokyo for food and culture"
    print(f"\nRequest: {user_input}\n")

    intent = parse_intent(user_input)
    itinerary = build_itinerary(intent)

    # Convert to markdown
    markdown = itinerary_to_markdown(itinerary)
    print(markdown)

    # Generate calendar file
    print("\n" + "-" * 60)
    ics_path = itinerary_to_ics(itinerary)
    print(f"Calendar file created: {ics_path}")

def test_supported_cities():
    """Test supported cities list."""
    print("\n" + "=" * 60)
    print("TEST 3: Supported Cities")
    print("=" * 60)

    cities = get_supported_cities()
    print(f"\nSupported destinations ({len(cities)}):")
    for city in cities:
        print(f"  • {city}")

def main():
    """Run all tests."""
    print("\n🧪 Trip Planner Agent - Local Testing\n")

    try:
        test_supported_cities()
        test_intent_parsing()
        test_itinerary_generation()

        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Set your ANTHROPIC_API_KEY in .env file")
        print("2. Run: python agent.py")
        print("3. The agent will be available at localhost:8000")

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
