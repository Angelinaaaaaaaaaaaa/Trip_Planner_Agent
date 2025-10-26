# test_llm_planner.py
# Test script for LLM-powered trip planning

from intent import TripIntent
from llm_planner import create_intelligent_itinerary
from llm_config import is_llm_available
from exporters import itinerary_to_markdown


def test_llm_planning():
    """Test LLM planning with various scenarios."""
    
    print("🧪 Testing LLM-Powered Trip Planner")
    print("=" * 50)
    
    # Check if LLM is available
    if not is_llm_available():
        print("❌ LLM not available (no ANTHROPIC_API_KEY)")
        print("   Set ANTHROPIC_API_KEY environment variable to test")
        return
    
    print("✅ LLM available - running tests")
    print()
    
    # Test cases
    test_cases = [
        {
            "name": "Prague Short Trip",
            "intent": TripIntent(
                destination="Prague",
                days=3,
                preferences=["architecture", "food", "culture"]
            )
        },
        {
            "name": "Mumbai Long Trip",
            "intent": TripIntent(
                destination="Mumbai",
                days=7,
                preferences=["food", "culture", "history"]
            )
        },
        {
            "name": "Reykjavik Nature Trip",
            "intent": TripIntent(
                destination="Reykjavik",
                days=5,
                preferences=["nature", "outdoors", "adventure"]
            )
        },
        {
            "name": "Dubai Family Trip",
            "intent": TripIntent(
                destination="Dubai",
                days=4,
                preferences=["family", "kids", "shopping"]
            )
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🌍 Test {i}: {test_case['name']}")
        print("-" * 30)
        
        try:
            # Create itinerary
            itinerary = create_intelligent_itinerary(test_case["intent"], use_llm=True)
            
            # Convert to markdown
            markdown = itinerary_to_markdown(itinerary)
            
            # Show summary
            print(f"📍 Destination: {itinerary.destination}")
            print(f"📅 Days: {itinerary.days}")
            print(f"🎯 Activities: {len(itinerary.items)}")
            print(f"📝 Day Ranges: {len(itinerary.day_ranges)}")
            
            # Show first few activities
            print("\n📋 Sample Activities:")
            for j, item in enumerate(itinerary.items[:3]):
                print(f"   Day {item.day}, {item.time}: {item.name} ({item.area})")
            
            if len(itinerary.items) > 3:
                print(f"   ... and {len(itinerary.items) - 3} more")
            
            # Show day ranges if any
            if itinerary.day_ranges:
                print("\n🗓️  Day Ranges:")
                for day_range in itinerary.day_ranges:
                    print(f"   {day_range}")
            
            print("✅ Success!")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        print()
    
    print("🎉 Testing complete!")


def test_specific_city(city: str, days: int = 3, preferences: list = None):
    """Test planning for a specific city."""
    
    if not is_llm_available():
        print("❌ LLM not available (no ANTHROPIC_API_KEY)")
        return
    
    intent = TripIntent(
        destination=city,
        days=days,
        preferences=preferences or ["culture", "food"]
    )
    
    print(f"🌍 Planning {days}-day trip to {city}")
    print(f"🎯 Preferences: {', '.join(intent.preferences)}")
    print()
    
    try:
        itinerary = create_intelligent_itinerary(intent, use_llm=True)
        markdown = itinerary_to_markdown(itinerary)
        
        print("📋 Generated Itinerary:")
        print("=" * 40)
        print(markdown)
        
    except Exception as e:
        print(f"❌ Failed to plan trip: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Test specific city from command line
        city = sys.argv[1]
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        preferences = sys.argv[3:] if len(sys.argv) > 3 else ["culture", "food"]
        
        test_specific_city(city, days, preferences)
    else:
        # Run all tests
        test_llm_planning()