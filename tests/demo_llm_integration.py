# demo_llm_integration.py
# Comprehensive demonstration of LLM-powered trip planning capabilities

import os
import sys
from typing import List, Dict
from intent import TripIntent
from llm_planner import create_intelligent_itinerary
from llm_config import is_llm_available
from exporters import itinerary_to_markdown
from data_sources import get_supported_cities

def demo_header():
    """Display demo header and system status."""
    print("=" * 70)
    print("🌍 AI-POWERED TRIP PLANNER AGENT - LLM INTEGRATION DEMO 🌍")
    print("=" * 70)
    print()
    
    # Check LLM status
    if is_llm_available():
        print("✅ LLM Status: ENABLED (Claude AI)")
        print("🌟 Capability: Can plan trips to ANY city worldwide!")
    else:
        print("❌ LLM Status: DISABLED (no ANTHROPIC_API_KEY)")
        print("📍 Capability: Limited to static cities only")
        print("💡 Set ANTHROPIC_API_KEY to enable global planning")
    
    print(f"📊 Static Database: {len(get_supported_cities())} cities")
    print(f"🏢 Static Cities: {', '.join(get_supported_cities())}")
    print()

def demo_static_cities():
    """Demonstrate enhanced planning for static cities."""
    print("🏛️  DEMO 1: ENHANCED STATIC CITY PLANNING")
    print("-" * 50)
    print("Testing: Existing cities with AI enhancement")
    print()
    
    test_cases = [
        {
            "name": "Enhanced Tokyo Experience",
            "intent": TripIntent(
                destination="Tokyo",
                days=4,
                preferences=["food", "culture", "art"]
            )
        },
        {
            "name": "Enhanced Barcelona Architecture",
            "intent": TripIntent(
                destination="Barcelona",
                days=3,
                preferences=["architecture", "culture"]
            )
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"📍 Test {i}: {case['name']}")
        print(f"   Request: {case['intent'].days} days in {case['intent'].destination}")
        print(f"   Focus: {', '.join(case['intent'].preferences)}")
        
        try:
            itinerary = create_intelligent_itinerary(case["intent"], use_llm=True)
            print(f"   ✅ Success: {len(itinerary.items)} activities planned")
            print(f"   📅 Day ranges: {len(itinerary.day_ranges)} ranges")
            
            # Show sample activities
            if itinerary.items:
                sample = itinerary.items[0]
                print(f"   🎯 Sample: Day {sample.day}, {sample.time} - {sample.name}")
        
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        print()

def demo_new_cities():
    """Demonstrate AI planning for new cities."""
    print("🌍 DEMO 2: NEW CITY AI PLANNING")
    print("-" * 50)
    print("Testing: Cities not in static database")
    print()
    
    if not is_llm_available():
        print("⚠️  Skipping - LLM not available")
        print("   Set ANTHROPIC_API_KEY to test this feature")
        print()
        return
    
    test_cases = [
        {
            "name": "Prague Architecture Tour",
            "intent": TripIntent(
                destination="Prague",
                days=3,
                preferences=["architecture", "history", "food"]
            )
        },
        {
            "name": "Mumbai Food Adventure",
            "intent": TripIntent(
                destination="Mumbai",
                days=5,
                preferences=["food", "culture", "history"]
            )
        },
        {
            "name": "Reykjavik Nature Experience",
            "intent": TripIntent(
                destination="Reykjavik",
                days=4,
                preferences=["nature", "outdoors", "adventure"]
            )
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"📍 Test {i}: {case['name']}")
        print(f"   Request: {case['intent'].days} days in {case['intent'].destination}")
        print(f"   Focus: {', '.join(case['intent'].preferences)}")
        
        try:
            itinerary = create_intelligent_itinerary(case["intent"], use_llm=True)
            print(f"   ✅ Success: {len(itinerary.items)} activities generated")
            print(f"   📅 Day ranges: {len(itinerary.day_ranges)} ranges")
            
            # Show sample activities
            if itinerary.items:
                sample = itinerary.items[0]
                print(f"   🎯 Sample: Day {sample.day}, {sample.time} - {sample.name}")
                
                # Show activity distribution
                day_counts = {}
                for item in itinerary.items:
                    day_counts[item.day] = day_counts.get(item.day, 0) + 1
                
                print(f"   📊 Distribution: {dict(sorted(day_counts.items()))}")
        
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        print()

def demo_edge_cases():
    """Demonstrate edge cases and fallback behavior."""
    print("🔧 DEMO 3: EDGE CASES & FALLBACK BEHAVIOR")
    print("-" * 50)
    print("Testing: Error handling and fallback mechanisms")
    print()
    
    test_cases = [
        {
            "name": "Very Long Trip",
            "intent": TripIntent(
                destination="Tokyo",
                days=30,
                preferences=["culture"]
            ),
            "description": "Testing long trip handling"
        },
        {
            "name": "Minimal Preferences",
            "intent": TripIntent(
                destination="Paris",
                days=2,
                preferences=[]
            ),
            "description": "Testing with no specific preferences"
        },
        {
            "name": "Single Day Trip",
            "intent": TripIntent(
                destination="Singapore",
                days=1,
                preferences=["family"]
            ),
            "description": "Testing single day planning"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"🧪 Test {i}: {case['name']}")
        print(f"   Scenario: {case['description']}")
        print(f"   Request: {case['intent'].days} days in {case['intent'].destination}")
        
        try:
            itinerary = create_intelligent_itinerary(case["intent"], use_llm=True)
            print(f"   ✅ Success: Generated itinerary")
            print(f"   📊 Activities: {len(itinerary.items)}")
            print(f"   📅 Day ranges: {len(itinerary.day_ranges)}")
            
            # Check coverage
            covered_days = itinerary.get_all_covered_days()
            total_days = set(range(1, case["intent"].days + 1))
            coverage = len(covered_days) / len(total_days) * 100
            print(f"   📈 Coverage: {coverage:.1f}% of days planned")
        
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        print()

def demo_full_itinerary():
    """Show a complete itinerary example."""
    print("📋 DEMO 4: COMPLETE ITINERARY EXAMPLE")
    print("-" * 50)
    
    if not is_llm_available():
        print("⚠️  Using static planning - LLM not available")
    
    # Choose example based on LLM availability
    if is_llm_available():
        intent = TripIntent(
            destination="Prague",
            days=3,
            preferences=["architecture", "food", "culture"]
        )
        print("🏰 Generating AI-powered Prague itinerary...")
    else:
        intent = TripIntent(
            destination="Tokyo",
            days=3,
            preferences=["food", "culture"]
        )
        print("🗾 Generating enhanced Tokyo itinerary...")
    
    print()
    
    try:
        itinerary = create_intelligent_itinerary(intent, use_llm=True)
        markdown = itinerary_to_markdown(itinerary)
        
        print("📄 GENERATED ITINERARY:")
        print("=" * 40)
        print(markdown)
        print("=" * 40)
        
        # Statistics
        print()
        print("📊 ITINERARY STATISTICS:")
        print(f"   🏙️  Destination: {itinerary.destination}")
        print(f"   📅 Total Days: {itinerary.days}")
        print(f"   🎯 Activities: {len(itinerary.items)}")
        print(f"   📝 Day Ranges: {len(itinerary.day_ranges)}")
        
        # Day coverage
        covered_days = itinerary.get_all_covered_days()
        print(f"   ✅ Days Covered: {len(covered_days)}/{itinerary.days}")
        
        # Activity distribution
        if itinerary.items:
            areas = set(item.area for item in itinerary.items)
            tags = set()
            for item in itinerary.items:
                tags.update(item.tags)
            
            print(f"   🗺️  Areas: {len(areas)} different areas")
            print(f"   🏷️  Tags: {len(tags)} activity types")
        
    except Exception as e:
        print(f"❌ Failed to generate itinerary: {e}")

def demo_comparison():
    """Compare static vs LLM planning for the same city."""
    print("⚖️  DEMO 5: STATIC VS LLM COMPARISON")
    print("-" * 50)
    
    if not is_llm_available():
        print("⚠️  Skipping - LLM not available for comparison")
        print()
        return
    
    intent = TripIntent(
        destination="Tokyo",
        days=3,
        preferences=["food", "culture"]
    )
    
    print(f"🔍 Comparing planning approaches for {intent.destination}")
    print(f"   Request: {intent.days} days, {', '.join(intent.preferences)}")
    print()
    
    # Static planning
    print("📊 STATIC PLANNING:")
    try:
        static_itinerary = create_intelligent_itinerary(intent, use_llm=False)
        print(f"   ✅ Activities: {len(static_itinerary.items)}")
        print(f"   📅 Day ranges: {len(static_itinerary.day_ranges)}")
        
        static_areas = set(item.area for item in static_itinerary.items)
        print(f"   🗺️  Areas covered: {len(static_areas)}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print()
    
    # LLM planning
    print("🤖 LLM PLANNING:")
    try:
        llm_itinerary = create_intelligent_itinerary(intent, use_llm=True)
        print(f"   ✅ Activities: {len(llm_itinerary.items)}")
        print(f"   📅 Day ranges: {len(llm_itinerary.day_ranges)}")
        
        llm_areas = set(item.area for item in llm_itinerary.items)
        print(f"   🗺️  Areas covered: {len(llm_areas)}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print()

def interactive_demo():
    """Allow user to test custom inputs."""
    print("🎮 DEMO 6: INTERACTIVE TESTING")
    print("-" * 50)
    print("Enter your own trip requests to test the system!")
    print("(Type 'quit' to exit)")
    print()
    
    while True:
        try:
            city = input("🏙️  Enter city name (or 'quit'): ").strip()
            if city.lower() == 'quit':
                break
            
            if not city:
                print("Please enter a city name.")
                continue
            
            days_input = input("📅 Enter number of days (default 3): ").strip()
            days = int(days_input) if days_input.isdigit() else 3
            
            prefs_input = input("🎯 Enter preferences (comma-separated, optional): ").strip()
            preferences = [p.strip() for p in prefs_input.split(',')] if prefs_input else []
            
            print()
            print(f"🚀 Planning {days}-day trip to {city}...")
            if preferences:
                print(f"   Focus: {', '.join(preferences)}")
            
            intent = TripIntent(
                destination=city,
                days=days,
                preferences=preferences
            )
            
            itinerary = create_intelligent_itinerary(intent, use_llm=True)
            
            print(f"✅ Success! Generated {len(itinerary.items)} activities")
            print(f"📊 Coverage: {len(itinerary.get_all_covered_days())}/{days} days")
            
            show_full = input("📋 Show full itinerary? (y/n): ").strip().lower()
            if show_full == 'y':
                markdown = itinerary_to_markdown(itinerary)
                print()
                print(markdown)
            
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except ValueError:
            print("Please enter a valid number for days.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

def main():
    """Run comprehensive demo."""
    demo_header()
    
    # Run all demos
    demos = [
        ("Enhanced Static Cities", demo_static_cities),
        ("New City AI Planning", demo_new_cities),
        ("Edge Cases & Fallbacks", demo_edge_cases),
        ("Complete Itinerary", demo_full_itinerary),
        ("Static vs LLM Comparison", demo_comparison),
    ]
    
    for title, demo_func in demos:
        try:
            demo_func()
        except KeyboardInterrupt:
            print("\n⏸️  Demo interrupted by user")
            break
        except Exception as e:
            print(f"❌ Demo failed: {e}")
        
        input("Press Enter to continue to next demo...")
        print()
    
    # Interactive demo
    try:
        interactive_demo()
    except KeyboardInterrupt:
        print("\n👋 Demo completed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        # Quick demo - just show capabilities
        demo_header()
        demo_full_itinerary()
    else:
        # Full demo
        main()