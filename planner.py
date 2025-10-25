# planner.py
# Intelligent itinerary generation with geographic clustering and time optimization

from typing import List, Dict
from dataclasses import dataclass
from intent import TripIntent
from data_sources import fetch_pois, get_supported_cities


@dataclass
class ItineraryItem:
    """Single item in the trip itinerary."""
    day: int
    time: str
    name: str
    area: str
    tags: List[str]
    url: str


@dataclass
class Itinerary:
    """Complete trip itinerary."""
    destination: str
    days: int
    items: List[ItineraryItem]


# Time slots for activities throughout the day
TIME_SLOTS = [
    ("09:00", 9),   # Morning
    ("12:00", 12),  # Midday
    ("15:00", 15),  # Afternoon
    ("18:00", 18),  # Evening
]


def build_itinerary(intent: TripIntent) -> Itinerary:
    """
    Build a detailed day-by-day itinerary based on user intent.

    Strategy:
    1. Score POIs based on preference matching
    2. Group POIs by geographic area to minimize travel time
    3. Respect opening hours when scheduling
    4. Distribute activities across days with varied time slots
    5. Aim for 3-4 activities per day

    Args:
        intent: Parsed trip intent with destination, days, preferences

    Returns:
        Complete itinerary with scheduled activities
    """
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
            ]
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

    # Build itinerary items
    items: List[ItineraryItem] = []
    area_list = list(by_area.items())
    area_index = 0
    used_poi_names = set()

    for day in range(1, days + 1):
        if area_index >= len(area_list):
            # Cycle back through areas if we have more days than areas
            area_index = 0

        area_name, area_pois = area_list[area_index]
        area_index += 1

        # For each day, try to fill time slots with POIs from the same area
        slots_filled = 0
        for time_label, hour in TIME_SLOTS:
            if slots_filled >= 4:  # Max 4 activities per day
                break

            # Find a POI that:
            # 1. Hasn't been used yet
            # 2. Is open at this time
            # 3. Is from this area
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
                    break

    # If we didn't generate enough items, try to fill in from other areas
    if len(items) < days * 2:  # Aim for at least 2 activities per day
        for day in range(1, days + 1):
            day_items = [item for item in items if item.day == day]
            if len(day_items) < 2:
                # Add more activities from any unused POI
                for poi in ranked_pois:
                    poi_name = poi.get("name", "Unknown")
                    if poi_name not in used_poi_names:
                        items.append(
                            ItineraryItem(
                                day=day,
                                time="14:00",
                                name=poi_name,
                                area=poi.get("area", "Unknown"),
                                tags=poi.get("tags", []),
                                url=poi.get("url", "")
                            )
                        )
                        used_poi_names.add(poi_name)
                        break

    return Itinerary(destination=city, days=days, items=items)
