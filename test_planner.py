# test_planner.py
# Comprehensive unit tests for the planner module
# Tests day count guarantees, day ranges, and performance

import time
import unittest
from intent import TripIntent
from planner import build_itinerary, Itinerary, ItineraryItem, DayRange
from planner_config import PlannerConfig
from exporters import itinerary_to_markdown, itinerary_to_ics


class TestPlannerDayCount(unittest.TestCase):
    """Test that planner always returns exactly the requested number of days."""

    def test_short_trip_enough_pois(self):
        """Test 3-day trip to Tokyo (has 10 POIs - more than enough)."""
        intent = TripIntent(destination="Tokyo", days=3, preferences=["food"])
        itinerary = build_itinerary(intent)

        self.assertEqual(itinerary.days, 3)
        covered_days = itinerary.get_all_covered_days()
        self.assertEqual(covered_days, {1, 2, 3})
        self.assertEqual(len(covered_days), 3)

    def test_medium_trip_not_enough_pois(self):
        """Test 5-day trip to New York (has 8 POIs - not quite enough)."""
        intent = TripIntent(destination="New York", days=5, preferences=[])
        itinerary = build_itinerary(intent)

        self.assertEqual(itinerary.days, 5)
        covered_days = itinerary.get_all_covered_days()
        self.assertEqual(covered_days, {1, 2, 3, 4, 5})
        self.assertEqual(len(covered_days), 5)

        # Should have day ranges for uncovered days
        if len(itinerary.items) < 20:  # If not all days have 4 activities
            self.assertGreater(len(itinerary.day_ranges), 0)

    def test_long_trip_sparse_pois(self):
        """Test 20-day trip to London (has 7 POIs - very sparse)."""
        intent = TripIntent(destination="London", days=20, preferences=[])
        itinerary = build_itinerary(intent)

        self.assertEqual(itinerary.days, 20)
        covered_days = itinerary.get_all_covered_days()
        self.assertEqual(len(covered_days), 20)

        # All days from 1-20 must be covered
        for day in range(1, 21):
            self.assertIn(day, covered_days)

        # Should have day ranges
        self.assertGreater(len(itinerary.day_ranges), 0)

    def test_very_long_trip_1000_days(self):
        """Test 1000-day trip - extreme case."""
        intent = TripIntent(destination="Paris", days=1000, preferences=["art"])
        itinerary = build_itinerary(intent)

        self.assertEqual(itinerary.days, 1000)
        covered_days = itinerary.get_all_covered_days()
        self.assertEqual(len(covered_days), 1000)

        # Verify all 1000 days are covered
        for day in range(1, 1001):
            self.assertIn(day, covered_days, f"Day {day} not covered!")

        # Should have many day ranges to avoid generating 1000s of items
        self.assertGreater(len(itinerary.day_ranges), 0)

    def test_single_day_trip(self):
        """Test edge case: 1-day trip."""
        intent = TripIntent(destination="Barcelona", days=1, preferences=[])
        itinerary = build_itinerary(intent)

        self.assertEqual(itinerary.days, 1)
        covered_days = itinerary.get_all_covered_days()
        self.assertEqual(covered_days, {1})


class TestDayRanges(unittest.TestCase):
    """Test day range creation and merging."""

    def test_day_range_properties(self):
        """Test DayRange data class properties."""
        day_range = DayRange(start_day=5, end_day=10, description="Rest period")

        self.assertEqual(day_range.start_day, 5)
        self.assertEqual(day_range.end_day, 10)
        self.assertEqual(day_range.num_days, 6)

    def test_single_day_range(self):
        """Test day range with single day."""
        day_range = DayRange(start_day=5, end_day=5, description="Free day")

        self.assertEqual(day_range.num_days, 1)
        self.assertIn("Day 5", repr(day_range))

    def test_multi_day_range(self):
        """Test day range with multiple days."""
        day_range = DayRange(start_day=10, end_day=15, description="Rest")

        self.assertEqual(day_range.num_days, 6)
        self.assertIn("Days 10–15", repr(day_range))

    def test_long_trip_creates_ranges(self):
        """Test that long trips automatically create day ranges."""
        intent = TripIntent(destination="Singapore", days=50, preferences=[])
        itinerary = build_itinerary(intent)

        # Should have day ranges
        self.assertGreater(len(itinerary.day_ranges), 0)

        # Verify day ranges cover contiguous periods
        for day_range in itinerary.day_ranges:
            self.assertLessEqual(day_range.start_day, day_range.end_day)
            self.assertGreaterEqual(day_range.start_day, 1)
            self.assertLessEqual(day_range.end_day, 50)

    def test_uncovered_days_method(self):
        """Test that uncovered_days method works correctly."""
        # Manually create itinerary with gaps
        itinerary = Itinerary(
            destination="Tokyo",
            days=5,
            items=[
                ItineraryItem(day=1, time="09:00", name="A", area="X", tags=[], url=""),
                ItineraryItem(day=3, time="09:00", name="B", area="X", tags=[], url=""),
            ],
            day_ranges=[]
        )

        uncovered = itinerary.get_uncovered_days()
        self.assertEqual(set(uncovered), {2, 4, 5})


class TestPlannerPerformance(unittest.TestCase):
    """Test that planner performs well with large day counts."""

    def test_1000_day_trip_performance(self):
        """Test that 1000-day trip completes quickly (< 3 seconds)."""
        intent = TripIntent(destination="Tokyo", days=1000, preferences=["culture"])

        start_time = time.time()
        itinerary = build_itinerary(intent)
        end_time = time.time()

        elapsed = end_time - start_time

        # Should complete in under 3 seconds
        self.assertLess(elapsed, 3.0, f"1000-day trip took {elapsed:.2f}s (too slow!)")

        # Should cover all 1000 days
        self.assertEqual(itinerary.days, 1000)
        covered_days = itinerary.get_all_covered_days()
        self.assertEqual(len(covered_days), 1000)

        print(f"✓ 1000-day trip generated in {elapsed:.3f}s")
        print(f"  - {len(itinerary.items)} activities")
        print(f"  - {len(itinerary.day_ranges)} day ranges")

    def test_memory_efficiency(self):
        """Test that very long trips don't create excessive objects."""
        intent = TripIntent(destination="Paris", days=1000, preferences=[])
        itinerary = build_itinerary(intent)

        # Should NOT have 1000 individual ItineraryItems
        # Should use day ranges for efficiency
        self.assertLess(len(itinerary.items), 500,
                       "Too many individual items - should use day ranges!")

        # Should have day ranges
        self.assertGreater(len(itinerary.day_ranges), 0,
                          "Should use day ranges for long trips!")


class TestPlannerConfiguration(unittest.TestCase):
    """Test planner configuration options."""

    def test_custom_config_max_activities(self):
        """Test custom configuration for max activities per day."""
        config = PlannerConfig(
            max_activities_per_day=2,  # Reduce from default 4
            min_activities_per_day=1
        )

        intent = TripIntent(destination="Tokyo", days=3, preferences=[])
        itinerary = build_itinerary(intent, config=config)

        # Check that no day has more than 2 activities
        for day in range(1, 4):
            day_items = [item for item in itinerary.items if item.day == day]
            self.assertLessEqual(len(day_items), 2,
                                f"Day {day} has {len(day_items)} activities (max should be 2)")

    def test_custom_config_auto_range_threshold(self):
        """Test custom threshold for automatic range creation."""
        config = PlannerConfig(
            auto_range_threshold_days=10,  # Create ranges for trips > 10 days
            max_individual_activity_days=8
        )

        intent = TripIntent(destination="Barcelona", days=15, preferences=[])
        itinerary = build_itinerary(intent, config=config)

        # Should have day ranges since 15 > 10
        self.assertGreater(len(itinerary.day_ranges), 0)


class TestExporters(unittest.TestCase):
    """Test markdown and ICS export with day ranges."""

    def test_markdown_export_with_ranges(self):
        """Test markdown export handles day ranges correctly."""
        intent = TripIntent(destination="London", days=10, preferences=[])
        itinerary = build_itinerary(intent)

        markdown = itinerary_to_markdown(itinerary)

        # Should mention all days
        self.assertIn("London", markdown)
        self.assertIn("10-Day", markdown)

        # If there are day ranges, they should be in markdown
        if itinerary.day_ranges:
            for day_range in itinerary.day_ranges:
                if day_range.start_day != day_range.end_day:
                    # Should have range notation
                    self.assertIn("–", markdown)  # En dash for ranges

    def test_ics_export_with_ranges(self):
        """Test ICS export creates all-day events for ranges."""
        intent = TripIntent(destination="Paris", days=20, preferences=[])
        itinerary = build_itinerary(intent)

        ics_path = itinerary_to_ics(itinerary)

        # Should create a file
        self.assertTrue(ics_path)
        self.assertTrue(ics_path.endswith('.ics'))

        # Read the ICS file
        with open(ics_path, 'r') as f:
            ics_content = f.read()

        # Should have VCALENDAR structure
        self.assertIn("BEGIN:VCALENDAR", ics_content)
        self.assertIn("END:VCALENDAR", ics_content)

        # Should have events
        self.assertIn("BEGIN:VEVENT", ics_content)

        # Clean up
        import os
        if os.path.exists(ics_path):
            os.remove(ics_path)

    def test_markdown_readability(self):
        """Test that markdown output is readable and well-formatted."""
        intent = TripIntent(destination="Tokyo", days=5, preferences=["food"])
        itinerary = build_itinerary(intent)

        markdown = itinerary_to_markdown(itinerary)

        # Should have headers
        self.assertIn("# 5-Day Trip to Tokyo", markdown)
        self.assertIn("## Day", markdown)

        # Should have properly formatted activities
        lines = markdown.split('\n')
        activity_lines = [l for l in lines if '**' in l and ' - ' in l]

        # Should have some activities
        self.assertGreater(len(activity_lines), 0)

        # Each activity line should have time and name
        for line in activity_lines:
            self.assertIn('**', line)
            self.assertIn(' - ', line)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def test_unsupported_city(self):
        """Test handling of unsupported city."""
        intent = TripIntent(destination="UnknownCity", days=3, preferences=[])
        itinerary = build_itinerary(intent)

        # Should still return an itinerary
        self.assertEqual(itinerary.destination, "UnknownCity")
        self.assertEqual(itinerary.days, 3)

        # Should have a helpful message
        self.assertTrue(any("don't have data" in item.name for item in itinerary.items))

    def test_zero_days(self):
        """Test handling of zero days."""
        intent = TripIntent(destination="Tokyo", days=0, preferences=[])
        itinerary = build_itinerary(intent)

        # Should default to some reasonable number (handled by intent parsing)
        # The planner should handle this gracefully
        self.assertGreaterEqual(itinerary.days, 0)

    def test_none_preferences(self):
        """Test handling of None preferences."""
        intent = TripIntent(destination="Paris", days=3, preferences=None)
        itinerary = build_itinerary(intent)

        # Should still work
        self.assertEqual(itinerary.days, 3)
        self.assertGreater(len(itinerary.items), 0)

    def test_empty_preferences(self):
        """Test handling of empty preferences list."""
        intent = TripIntent(destination="Barcelona", days=3, preferences=[])
        itinerary = build_itinerary(intent)

        # Should still work
        self.assertEqual(itinerary.days, 3)
        self.assertGreater(len(itinerary.items), 0)


def run_integration_test():
    """
    Integration test covering all major scenarios.

    This test demonstrates:
    1. Short trips with enough POIs
    2. Medium trips with sparse POIs (ranges needed)
    3. Long trips with efficient day ranges
    4. Very long trips (1000 days) with performance validation
    """
    print("\n" + "="*70)
    print("INTEGRATION TEST: Day Count & Range Generation")
    print("="*70)

    test_cases = [
        ("Tokyo", 3, ["food", "culture"], "Short trip, plenty of POIs"),
        ("New York", 5, [], "Medium trip, enough POIs"),
        ("London", 20, ["history"], "Long trip, need ranges"),
        ("Paris", 100, ["art"], "Very long trip, many ranges"),
        ("Singapore", 1000, [], "Extreme: 1000-day trip"),
    ]

    for city, days, prefs, description in test_cases:
        print(f"\nTest: {description}")
        print(f"  Request: {days}-day trip to {city}")

        intent = TripIntent(destination=city, days=days, preferences=prefs)

        start_time = time.time()
        itinerary = build_itinerary(intent)
        elapsed = time.time() - start_time

        # Verify all days covered
        covered_days = itinerary.get_all_covered_days()
        uncovered = itinerary.get_uncovered_days()

        print(f"  Result:")
        print(f"    - Generated in: {elapsed:.3f}s")
        print(f"    - Activities: {len(itinerary.items)}")
        print(f"    - Day ranges: {len(itinerary.day_ranges)}")
        print(f"    - Days covered: {len(covered_days)}/{days}")

        if uncovered:
            print(f"    - ❌ UNCOVERED DAYS: {uncovered}")
        else:
            print(f"    - ✓ All days covered")

        # Performance check for long trips
        if days >= 1000:
            assert elapsed < 3.0, f"1000-day trip took too long: {elapsed:.2f}s"
            print(f"    - ✓ Performance: < 3s")

        # Export test
        markdown = itinerary_to_markdown(itinerary)
        assert len(markdown) > 0, "Markdown export failed"
        print(f"    - ✓ Markdown export works")

        # Verify guarantees
        assert itinerary.days == days, f"Days mismatch: {itinerary.days} != {days}"
        assert len(covered_days) == days, f"Not all days covered: {len(covered_days)} != {days}"
        assert len(uncovered) == 0, f"Uncovered days: {uncovered}"

    print("\n" + "="*70)
    print("✓ INTEGRATION TEST PASSED")
    print("="*70)


if __name__ == "__main__":
    # Run unit tests
    print("Running unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)

    # Run integration test
    run_integration_test()
