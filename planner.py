# planner_v2.py
# Intelligent itinerary generation with day range support and guaranteed day counts
# Supports trips up to 1000 days with efficient memory usage

from typing import List, Dict, Union
from dataclasses import dataclass
from intent import TripIntent
from data_sources import fetch_pois, get_supported_cities
from planner_config import get_config, PlannerConfig


@dataclass
class ItineraryItem:
    """Single activity in the trip itinerary."""
    day: int
    time: str
    name: str
    area: str
    tags: List[str]
    url: str


@dataclass
class DayRange:
    """
    Represents a range of days with a common activity or rest period.

    Used for:
    - Multi-day rest periods
    - Free exploration days
    - Buffer days between major activities
    """
    start_day: int
    end_day: int
    description: str
    activity_type: str = "rest"  # "rest", "free_exploration", "buffer"

    @property
    def num_days(self) -> int:
        """Calculate number of days in this range."""
        return self.end_day - self.start_day + 1

    def __repr__(self) -> str:
        if self.start_day == self.end_day:
            return f"Day {self.start_day}: {self.description}"
        return f"Days {self.start_day}–{self.end_day}: {self.description}"


@dataclass
class Itinerary:
    """
    Complete trip itinerary with both specific activities and day ranges.

    Attributes:
        destination: City name
        days: Total number of days in the trip
        items: List of specific activities
        day_ranges: List of multi-day rest/buffer periods
    """
    destination: str
    days: int
    items: List[ItineraryItem]
    day_ranges: List[DayRange] = None

    def __post_init__(self):
        """Initialize day_ranges if not provided."""
        if self.day_ranges is None:
            self.day_ranges = []

    def get_all_covered_days(self) -> set:
        """Get set of all days that have activities or are in ranges."""
        covered = set()

        # Days with specific activities
        for item in self.items:
            covered.add(item.day)

        # Days in ranges
        for day_range in self.day_ranges:
            for day in range(day_range.start_day, day_range.end_day + 1):
                covered.add(day)

        return covered

    def get_uncovered_days(self) -> List[int]:
        """Get list of days not covered by activities or ranges."""
        covered = self.get_all_covered_days()
        all_days = set(range(1, self.days + 1))
        return sorted(all_days - covered)


# Time slots for activities throughout the day
TIME_SLOTS = [
    ("09:00", 9),   # Morning
    ("12:00", 12),  # Midday
    ("15:00", 15),  # Afternoon
    ("18:00", 18),  # Evening
]


def build_itinerary(intent: TripIntent, config: PlannerConfig = None) -> Itinerary:
    """
    Build a detailed day-by-day itinerary based on user intent.

    GUARANTEES:
    - Returns exactly intent.days days (no more, no less)
    - All days from 1 to intent.days are accounted for
    - Handles trips up to 1000 days efficiently
    - Creates day ranges for sparse periods

    Strategy:
    1. Score and rank POIs based on preferences
    2. Allocate POIs to early days (dense activity period)
    3. Create rest/buffer day ranges for remaining days
    4. Ensure every single day is covered

    Args:
        intent: Parsed trip intent with destination, days, preferences
        config: Optional planner configuration (uses default if not provided)

    Returns:
        Complete itinerary with activities and day ranges, covering all days
    """
    if config is None:
        config = get_config()

    city = intent.destination
    days = intent.days or 3
    prefs = set(intent.preferences) if intent.preferences else set()

    # Fetch POIs for this city
    pois = fetch_pois(city, list(prefs))

    if not pois:
        # City not in database - return helpful message
        supported = get_supported_cities()
        return Itinerary(
            destination=city or "Unknown",
            days=days,
            items=[
                ItineraryItem(
                    day=1,
                    time="09:00",
                    name=f"Sorry, I don't have data for {city} yet.",
                    area="",
                    tags=[],
                    url=f"https://maps.google.com/?q={city}" if city else ""
                ),
                ItineraryItem(
                    day=1,
                    time="10:00",
                    name=f"I currently support: {', '.join(supported)}",
                    area="",
                    tags=[],
                    url=""
                )
            ],
            day_ranges=[]
        )

    # Score POIs: preference match (high priority) + opening window length (tiebreaker)
    def score_poi(poi: dict) -> tuple:
        poi_tags = set(poi.get("tags", []))
        preference_match = len(poi_tags & prefs) if prefs else 0
        open_start, open_end = poi.get("open", (9, 18))
        availability_hours = open_end - open_start
        return (preference_match, availability_hours)

    # Sort POIs by score (descending)
    ranked_pois = sorted(pois, key=score_poi, reverse=True)

    # Group POIs by area for geographic clustering
    by_area: Dict[str, List[dict]] = {}
    for poi in ranked_pois:
        area = poi.get("area", "Unknown")
        by_area.setdefault(area, []).append(poi)

    # Determine how many days to generate detailed activities for
    # Be more generous - allow at least 1 activity per day if we have POIs
    if days <= config.dense_activity_days_threshold:
        # For short trips, try to fill as many days as possible with activities
        # Use at least 1 activity per day (not min_activities_per_day)
        max_activity_days = min(
            days,
            config.max_individual_activity_days,
            len(ranked_pois)  # One POI can cover one day minimum
        )
    else:
        # For longer trips, be more conservative
        max_activity_days = min(
            days,
            config.max_individual_activity_days,
            len(ranked_pois) // max(1, config.min_activities_per_day - 1) + 1
        )

    # Build itinerary items for early days (activity-dense period)
    items: List[ItineraryItem] = []
    area_list = list(by_area.items())
    area_index = 0
    used_poi_names = set()

    # Calculate target activities per day to distribute POIs evenly across requested days
    # Use round-robin approach: first give 1 POI to each day, then distribute remainder
    if max_activity_days > 0 and len(ranked_pois) > 0:
        # First pass: 1 POI per day
        base_pois_per_day = min(1, len(ranked_pois) // max_activity_days)
        remaining_pois = len(ranked_pois) - (base_pois_per_day * max_activity_days)

        # Second pass: distribute remainder
        extra_pois_per_day = remaining_pois // max_activity_days if max_activity_days > 0 else 0

        # Calculate per-day allocation for round-robin
        target_activities_per_day = base_pois_per_day + extra_pois_per_day
        target_activities_per_day = max(1, min(config.max_activities_per_day, target_activities_per_day))

        # For short trips with enough POIs, round down to spread more
        if days <= config.dense_activity_days_threshold:
            avg = len(ranked_pois) / max_activity_days
            if 1.0 <= avg < 2.0:
                # Between 1-2 average, start with 1 and add extras later
                target_activities_per_day = 1
            elif avg >= 2.0:
                # 2+ average, allow 2 per day
                target_activities_per_day = min(2, int(avg))
    else:
        target_activities_per_day = config.max_activities_per_day

    for day in range(1, max_activity_days + 1):
        if area_index >= len(area_list):
            # Cycle back through areas if we have more days than areas
            area_index = 0

        area_name, area_pois = area_list[area_index]
        area_index += 1

        # Determine max activities for this day
        # For short/medium trips, distribute POIs evenly
        if days <= config.dense_activity_days_threshold:
            max_activities_today = target_activities_per_day
            # But ensure we try for at least 1 activity per day while POIs remain
            if day <= max_activity_days and len(used_poi_names) < len(ranked_pois):
                max_activities_today = max(1, target_activities_per_day)
        else:
            # For longer trips, taper off over time
            if day <= config.activity_taper_start_day:
                max_activities_today = config.max_activities_per_day
            else:
                taper_factor = (day - config.activity_taper_start_day) / 10
                max_activities_today = max(
                    1,  # At least 1 activity per day
                    config.max_activities_per_day - int(taper_factor)
                )

        # For each day, try to fill time slots with POIs from the same area
        slots_filled = 0

        # For short trips, ensure we put at least 1 POI per day if available
        min_for_today = 1 if (days <= config.dense_activity_days_threshold and
                             len(used_poi_names) < len(ranked_pois)) else 0

        for time_label, hour in TIME_SLOTS:
            # Check if we have POIs left and haven't exceeded max for today
            if len(used_poi_names) >= len(ranked_pois):
                break  # All POIs used
            # Allow at least min_for_today activities before respecting the limit
            if slots_filled >= max_activities_today and slots_filled >= min_for_today:
                break

            # Find a POI that:
            # 1. Hasn't been used yet
            # 2. Is open at this time
            # 3. Is from this area (preferred)
            found = False
            for poi in area_pois:
                poi_name = poi.get("name", "Unknown")
                if poi_name in used_poi_names:
                    continue

                open_start, open_end = poi.get("open", (9, 18))
                if open_start <= hour <= open_end:
                    # This POI works for this time slot!
                    items.append(
                        ItineraryItem(
                            day=day,
                            time=time_label,
                            name=poi_name,
                            area=area_name,
                            tags=poi.get("tags", []),
                            url=poi.get("url", "")
                        )
                    )
                    used_poi_names.add(poi_name)
                    slots_filled += 1
                    found = True
                    break

            # If we didn't find a POI from this area, try any unused POI
            # Be less strict about minimum - if we have POIs left, use them
            if not found and len(used_poi_names) < len(ranked_pois):
                for poi in ranked_pois:
                    poi_name = poi.get("name", "Unknown")
                    if poi_name in used_poi_names:
                        continue

                    open_start, open_end = poi.get("open", (9, 18))
                    if open_start <= hour <= open_end:
                        items.append(
                            ItineraryItem(
                                day=day,
                                time=time_label,
                                name=poi_name,
                                area=poi.get("area", "Unknown"),
                                tags=poi.get("tags", []),
                                url=poi.get("url", "")
                            )
                        )
                        used_poi_names.add(poi_name)
                        slots_filled += 1
                        break

    # Second pass: If we still have unused POIs and days with < 2 activities, add more
    if len(used_poi_names) < len(ranked_pois) and days <= config.dense_activity_days_threshold:
        for day in range(1, max_activity_days + 1):
            if len(used_poi_names) >= len(ranked_pois):
                break  # All POIs now used

            day_items = [item for item in items if item.day == day]
            if len(day_items) < 2:  # Add one more activity to this day
                # Find an unused POI
                for poi in ranked_pois:
                    poi_name = poi.get("name", "Unknown")
                    if poi_name in used_poi_names:
                        continue

                    # Add it to this day
                    # Find a time slot not already used
                    used_times = {item.time for item in day_items}
                    for time_label, hour in TIME_SLOTS:
                        if time_label not in used_times:
                            open_start, open_end = poi.get("open", (9, 18))
                            if open_start <= hour <= open_end:
                                items.append(
                                    ItineraryItem(
                                        day=day,
                                        time=time_label,
                                        name=poi_name,
                                        area=poi.get("area", "Unknown"),
                                        tags=poi.get("tags", []),
                                        url=poi.get("url", "")
                                    )
                                )
                                used_poi_names.add(poi_name)
                                break
                    break  # Move to next day

    # Create day ranges for remaining days
    day_ranges: List[DayRange] = []

    if max_activity_days < days:
        # We have remaining days - create day ranges
        remaining_start = max_activity_days + 1
        remaining_end = days

        # Decide how to describe these days based on trip length
        if days <= config.dense_activity_days_threshold:
            # Short trip - call them "free exploration"
            description = "Free exploration / Rest days"
            activity_type = "free_exploration"
        elif days <= config.auto_range_threshold_days:
            # Medium trip - more relaxed description
            description = "Leisure time / Optional activities"
            activity_type = "buffer"
        else:
            # Long trip - clearly indicate rest period
            description = "Extended rest period / Free time to explore at your own pace"
            activity_type = "rest"

        # Create ranges in reasonable chunks (max 7 days per range for readability)
        current_start = remaining_start
        while current_start <= remaining_end:
            # Create ranges of max 7 days each
            chunk_end = min(current_start + 6, remaining_end)

            # Customize description based on position
            if days > 100:
                # Very long trip - be more specific
                chunk_desc = f"{description} — Week {(current_start - 1) // 7 + 1}"
            else:
                chunk_desc = description

            day_ranges.append(
                DayRange(
                    start_day=current_start,
                    end_day=chunk_end,
                    description=chunk_desc,
                    activity_type=activity_type
                )
            )

            current_start = chunk_end + 1

    # Create the itinerary
    itinerary = Itinerary(
        destination=city,
        days=days,
        items=items,
        day_ranges=day_ranges
    )

    # CRITICAL: Verify we're covering all days
    uncovered = itinerary.get_uncovered_days()
    if uncovered:
        # This should never happen, but if it does, create a catch-all range
        # Group consecutive uncovered days
        ranges_to_add = _group_consecutive_days(uncovered)
        for start, end in ranges_to_add:
            day_ranges.append(
                DayRange(
                    start_day=start,
                    end_day=end,
                    description="Free time / Rest",
                    activity_type="buffer"
                )
            )

    return itinerary


def _group_consecutive_days(days: List[int]) -> List[tuple]:
    """
    Group consecutive days into ranges.

    Args:
        days: Sorted list of day numbers

    Returns:
        List of (start_day, end_day) tuples
    """
    if not days:
        return []

    ranges = []
    start = days[0]
    prev = days[0]

    for day in days[1:]:
        if day == prev + 1:
            # Consecutive
            prev = day
        else:
            # Gap found - close current range
            ranges.append((start, prev))
            start = day
            prev = day

    # Close final range
    ranges.append((start, prev))

    return ranges


# Backward compatibility: keep old function name
def build_itinerary_v1(intent: TripIntent) -> Itinerary:
    """
    Legacy function for backward compatibility.
    Calls the new build_itinerary with default config.
    """
    return build_itinerary(intent)
