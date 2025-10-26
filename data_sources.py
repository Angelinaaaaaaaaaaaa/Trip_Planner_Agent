# data_sources.py
# Built-in POI database for popular destinations
# No external APIs required - works immediately!

import re
from typing import List, Dict

# Comprehensive POI database for 6+ popular cities
DESTINATIONS: Dict[str, Dict[str, List[dict]]] = {
    "Tokyo": {
        "pois": [
            {
                "name": "Meiji Shrine",
                "area": "Harajuku",
                "tags": ["culture", "history"],
                "open": (6, 17),
                "url": "https://maps.google.com/?q=Meiji+Shrine+Tokyo"
            },
            {
                "name": "Takeshita Street",
                "area": "Harajuku",
                "tags": ["food", "shopping"],
                "open": (10, 21),
                "url": "https://maps.google.com/?q=Takeshita+Street+Harajuku"
            },
            {
                "name": "Shibuya Crossing",
                "area": "Shibuya",
                "tags": ["culture"],
                "open": (0, 24),
                "url": "https://maps.google.com/?q=Shibuya+Crossing"
            },
            {
                "name": "Ichiran Ramen",
                "area": "Shibuya",
                "tags": ["food"],
                "open": (10, 24),
                "url": "https://maps.google.com/?q=Ichiran+Ramen+Shibuya"
            },
            {
                "name": "Senso-ji Temple",
                "area": "Asakusa",
                "tags": ["culture", "history"],
                "open": (6, 17),
                "url": "https://maps.google.com/?q=Senso-ji+Temple"
            },
            {
                "name": "Ueno Park",
                "area": "Ueno",
                "tags": ["nature"],
                "open": (5, 23),
                "url": "https://maps.google.com/?q=Ueno+Park+Tokyo"
            },
            {
                "name": "Tsukiji Outer Market",
                "area": "Tsukiji",
                "tags": ["food"],
                "open": (7, 14),
                "url": "https://maps.google.com/?q=Tsukiji+Outer+Market"
            },
            {
                "name": "teamLab Planets",
                "area": "Toyosu",
                "tags": ["art", "culture"],
                "open": (10, 20),
                "url": "https://maps.google.com/?q=teamLab+Planets+Tokyo"
            },
            {
                "name": "Tokyo Skytree",
                "area": "Sumida",
                "tags": ["culture", "architecture"],
                "open": (8, 22),
                "url": "https://maps.google.com/?q=Tokyo+Skytree"
            },
            {
                "name": "Akihabara Electric Town",
                "area": "Akihabara",
                "tags": ["shopping", "culture"],
                "open": (10, 20),
                "url": "https://maps.google.com/?q=Akihabara+Electric+Town"
            }
        ]
    },
    "Barcelona": {
        "pois": [
            {
                "name": "Sagrada Família",
                "area": "Eixample",
                "tags": ["architecture", "culture"],
                "open": (9, 19),
                "url": "https://maps.google.com/?q=Sagrada+Familia+Barcelona"
            },
            {
                "name": "Park Güell",
                "area": "Gràcia",
                "tags": ["architecture", "nature"],
                "open": (8, 20),
                "url": "https://maps.google.com/?q=Park+Guell+Barcelona"
            },
            {
                "name": "La Boqueria Market",
                "area": "Ciutat Vella",
                "tags": ["food"],
                "open": (8, 20),
                "url": "https://maps.google.com/?q=La+Boqueria+Market"
            },
            {
                "name": "Barceloneta Beach",
                "area": "Barceloneta",
                "tags": ["beach", "nature"],
                "open": (6, 22),
                "url": "https://maps.google.com/?q=Barceloneta+Beach"
            },
            {
                "name": "Gothic Quarter",
                "area": "Ciutat Vella",
                "tags": ["culture", "history"],
                "open": (0, 24),
                "url": "https://maps.google.com/?q=Gothic+Quarter+Barcelona"
            },
            {
                "name": "Casa Batlló",
                "area": "Eixample",
                "tags": ["architecture", "culture"],
                "open": (9, 21),
                "url": "https://maps.google.com/?q=Casa+Batllo+Barcelona"
            },
            {
                "name": "Camp Nou",
                "area": "Les Corts",
                "tags": ["sports", "culture"],
                "open": (10, 18),
                "url": "https://maps.google.com/?q=Camp+Nou+Barcelona"
            },
            {
                "name": "Montjuïc Castle",
                "area": "Montjuïc",
                "tags": ["history", "culture"],
                "open": (10, 20),
                "url": "https://maps.google.com/?q=Montjuic+Castle"
            }
        ]
    },
    "Singapore": {
        "pois": [
            {
                "name": "Singapore Zoo",
                "area": "Mandai",
                "tags": ["family", "kids", "nature"],
                "open": (8, 18),
                "url": "https://maps.google.com/?q=Singapore+Zoo"
            },
            {
                "name": "S.E.A. Aquarium",
                "area": "Sentosa",
                "tags": ["family", "kids"],
                "open": (10, 19),
                "url": "https://maps.google.com/?q=SEA+Aquarium+Singapore"
            },
            {
                "name": "Gardens by the Bay",
                "area": "Marina",
                "tags": ["nature", "art"],
                "open": (9, 21),
                "url": "https://maps.google.com/?q=Gardens+by+the+Bay"
            },
            {
                "name": "Maxwell Food Centre",
                "area": "Chinatown",
                "tags": ["food"],
                "open": (8, 22),
                "url": "https://maps.google.com/?q=Maxwell+Food+Centre"
            },
            {
                "name": "Marina Bay Sands SkyPark",
                "area": "Marina",
                "tags": ["architecture"],
                "open": (11, 21),
                "url": "https://maps.google.com/?q=Marina+Bay+Sands+SkyPark"
            },
            {
                "name": "Universal Studios",
                "area": "Sentosa",
                "tags": ["family", "kids"],
                "open": (10, 19),
                "url": "https://maps.google.com/?q=Universal+Studios+Singapore"
            },
            {
                "name": "Merlion Park",
                "area": "Marina",
                "tags": ["culture"],
                "open": (0, 24),
                "url": "https://maps.google.com/?q=Merlion+Park+Singapore"
            }
        ]
    },
    "Paris": {
        "pois": [
            {
                "name": "Eiffel Tower",
                "area": "Champ de Mars",
                "tags": ["architecture", "culture"],
                "open": (9, 24),
                "url": "https://maps.google.com/?q=Eiffel+Tower+Paris"
            },
            {
                "name": "Louvre Museum",
                "area": "1st Arrondissement",
                "tags": ["art", "culture", "history"],
                "open": (9, 18),
                "url": "https://maps.google.com/?q=Louvre+Museum"
            },
            {
                "name": "Notre-Dame Cathedral",
                "area": "Île de la Cité",
                "tags": ["architecture", "history"],
                "open": (8, 19),
                "url": "https://maps.google.com/?q=Notre+Dame+Cathedral"
            },
            {
                "name": "Montmartre & Sacré-Cœur",
                "area": "Montmartre",
                "tags": ["culture", "art"],
                "open": (6, 22),
                "url": "https://maps.google.com/?q=Sacre+Coeur+Montmartre"
            },
            {
                "name": "Champs-Élysées",
                "area": "8th Arrondissement",
                "tags": ["shopping", "culture"],
                "open": (0, 24),
                "url": "https://maps.google.com/?q=Champs+Elysees+Paris"
            },
            {
                "name": "Seine River Cruise",
                "area": "Seine",
                "tags": ["culture", "nature"],
                "open": (10, 22),
                "url": "https://maps.google.com/?q=Seine+River+Cruise+Paris"
            },
            {
                "name": "Latin Quarter",
                "area": "5th Arrondissement",
                "tags": ["food", "culture"],
                "open": (0, 24),
                "url": "https://maps.google.com/?q=Latin+Quarter+Paris"
            }
        ]
    },
    "New York": {
        "pois": [
            {
                "name": "Central Park",
                "area": "Manhattan",
                "tags": ["nature"],
                "open": (6, 25),
                "url": "https://maps.google.com/?q=Central+Park+NYC"
            },
            {
                "name": "Times Square",
                "area": "Manhattan",
                "tags": ["culture", "nightlife"],
                "open": (0, 24),
                "url": "https://maps.google.com/?q=Times+Square+NYC"
            },
            {
                "name": "Metropolitan Museum of Art",
                "area": "Manhattan",
                "tags": ["art", "culture"],
                "open": (10, 17),
                "url": "https://maps.google.com/?q=Metropolitan+Museum+of+Art"
            },
            {
                "name": "Statue of Liberty",
                "area": "Liberty Island",
                "tags": ["history", "culture"],
                "open": (9, 17),
                "url": "https://maps.google.com/?q=Statue+of+Liberty"
            },
            {
                "name": "Brooklyn Bridge",
                "area": "Brooklyn",
                "tags": ["architecture", "culture"],
                "open": (0, 24),
                "url": "https://maps.google.com/?q=Brooklyn+Bridge"
            },
            {
                "name": "9/11 Memorial",
                "area": "Manhattan",
                "tags": ["history", "culture"],
                "open": (9, 20),
                "url": "https://maps.google.com/?q=911+Memorial+NYC"
            },
            {
                "name": "Broadway Theatre District",
                "area": "Manhattan",
                "tags": ["culture", "nightlife"],
                "open": (10, 23),
                "url": "https://maps.google.com/?q=Broadway+NYC"
            },
            {
                "name": "Chelsea Market",
                "area": "Manhattan",
                "tags": ["food", "shopping"],
                "open": (7, 21),
                "url": "https://maps.google.com/?q=Chelsea+Market+NYC"
            }
        ]
    },
    "London": {
        "pois": [
            {
                "name": "Tower of London",
                "area": "Tower Hill",
                "tags": ["history", "culture"],
                "open": (9, 17),
                "url": "https://maps.google.com/?q=Tower+of+London"
            },
            {
                "name": "British Museum",
                "area": "Bloomsbury",
                "tags": ["art", "history", "culture"],
                "open": (10, 17),
                "url": "https://maps.google.com/?q=British+Museum"
            },
            {
                "name": "Buckingham Palace",
                "area": "Westminster",
                "tags": ["culture", "history"],
                "open": (9, 19),
                "url": "https://maps.google.com/?q=Buckingham+Palace"
            },
            {
                "name": "Borough Market",
                "area": "Southwark",
                "tags": ["food"],
                "open": (10, 17),
                "url": "https://maps.google.com/?q=Borough+Market+London"
            },
            {
                "name": "London Eye",
                "area": "South Bank",
                "tags": ["architecture", "culture"],
                "open": (10, 20),
                "url": "https://maps.google.com/?q=London+Eye"
            },
            {
                "name": "Covent Garden",
                "area": "West End",
                "tags": ["shopping", "culture"],
                "open": (10, 20),
                "url": "https://maps.google.com/?q=Covent+Garden+London"
            },
            {
                "name": "Hyde Park",
                "area": "Central London",
                "tags": ["nature"],
                "open": (5, 24),
                "url": "https://maps.google.com/?q=Hyde+Park+London"
            }
        ]
    }
}


def _normalize_city_name(city: str) -> str:
    """
    Normalize city name for case-insensitive matching.

    Handles:
    - Case differences (TOKYO, tokyo, Tokyo)
    - Punctuation (tokyo., new york!)
    - Extra whitespace

    Args:
        city: Raw city name from user input

    Returns:
        Normalized city name in Title Case
    """
    if not city:
        return ""

    # Remove punctuation (except spaces and hyphens for multi-word cities)
    city = re.sub(r'[^\w\s-]', '', city)

    # Strip extra whitespace and convert to title case
    city = city.strip().title()

    return city


def fetch_pois(city: str, preferences: List[str] = None) -> List[dict]:
    """
    Fetch POIs for a given city from the built-in database.

    City matching is case-insensitive and handles punctuation.
    Examples: "tokyo", "TOKYO", "Tokyo.", "new york" all work.

    Args:
        city: Destination city name (case-insensitive, punctuation-tolerant)
        preferences: Optional list of preference tags to filter/prioritize

    Returns:
        List of POI dictionaries with name, area, tags, opening hours, and URL
    """
    # Normalize the input city name
    normalized_city = _normalize_city_name(city)

    # Try exact match first (for backward compatibility)
    city_data = DESTINATIONS.get(normalized_city, {})

    # If not found, try case-insensitive search
    if not city_data:
        for dest_city in DESTINATIONS.keys():
            if _normalize_city_name(dest_city) == normalized_city:
                city_data = DESTINATIONS[dest_city]
                break

    pois = city_data.get("pois", [])

    if not pois:
        # Return empty list if city not found
        return []

    return pois


def get_supported_cities() -> List[str]:
    """Return list of cities with built-in POI data."""
    return list(DESTINATIONS.keys())


def is_city_supported(city: str) -> bool:
    """
    Check if a city is supported (case-insensitive, punctuation-tolerant).

    Args:
        city: City name to check

    Returns:
        True if city has POI data, False otherwise
    """
    if not city:
        return False

    # Try to fetch POIs - if we get any, the city is supported
    pois = fetch_pois(city)
    return len(pois) > 0
