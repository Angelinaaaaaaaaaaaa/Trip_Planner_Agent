# intent.py
# Claude-powered natural language intent parsing
# Extracts destination, duration, and preferences from user messages

import os
from dataclasses import dataclass
from typing import List, Optional
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class TripIntent:
    """Structured trip planning intent parsed from natural language."""
    destination: Optional[str]
    days: Optional[int]
    preferences: List[str]


# Preference keywords we support
PREFERENCE_KEYWORDS = [
    "food", "culture", "museum", "art", "architecture", "nature", "outdoors",
    "nightlife", "shopping", "family", "kids", "history", "beach", "hiking",
    "sports", "adventure", "relaxation"
]


def parse_intent(text: str) -> TripIntent:
    """
    Parse user's natural language input using Claude AI.

    Extracts:
    - destination: City name
    - days: Trip duration in days
    - preferences: List of interest categories

    Args:
        text: User's natural language request

    Returns:
        TripIntent with parsed information
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        # Fallback to simple rule-based parsing if no API key
        return _parse_intent_simple(text)

    try:
        client = Anthropic(api_key=api_key)

        prompt = f"""Parse this trip planning request and extract structured information.

User request: "{text}"

Extract:
1. Destination city (just the city name, properly capitalized)
2. Number of days for the trip
3. Preferences/interests from this list: {', '.join(PREFERENCE_KEYWORDS)}

Respond in this exact format:
DESTINATION: [city name or NONE]
DAYS: [number or NONE]
PREFERENCES: [comma-separated list or NONE]

Examples:
Request: "Plan me a 3-day trip to Tokyo for food and culture"
DESTINATION: Tokyo
DAYS: 3
PREFERENCES: food, culture

Request: "I want to visit Barcelona for 2 days, focus on architecture"
DESTINATION: Barcelona
DAYS: 2
PREFERENCES: architecture

Request: "Family trip to Singapore, kid-friendly"
DESTINATION: Singapore
DAYS: NONE
PREFERENCES: family, kids

Now parse the user's request."""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse Claude's response
        response_text = message.content[0].text

        destination = None
        days = None
        preferences = []

        for line in response_text.split('\n'):
            line = line.strip()
            if line.startswith('DESTINATION:'):
                dest = line.split(':', 1)[1].strip()
                if dest != 'NONE':
                    destination = dest
            elif line.startswith('DAYS:'):
                days_str = line.split(':', 1)[1].strip()
                if days_str != 'NONE':
                    try:
                        days = int(days_str)
                    except ValueError:
                        pass
            elif line.startswith('PREFERENCES:'):
                prefs_str = line.split(':', 1)[1].strip()
                if prefs_str != 'NONE':
                    preferences = [p.strip() for p in prefs_str.split(',')]

        return TripIntent(destination=destination, days=days, preferences=preferences)

    except Exception as e:
        print(f"Error using Claude for intent parsing: {e}")
        # Fallback to simple parsing
        return _parse_intent_simple(text)


def _parse_intent_simple(text: str) -> TripIntent:
    """
    Simple rule-based intent parsing as fallback.
    Uses pattern matching for common trip planning phrases.
    """
    import re

    t = text.strip().lower()

    # Extract days
    days = None
    # Try patterns like "3-day", "3 days", "three days"
    day_match = re.search(r'(\d+)\s*-?\s*days?', t)
    if day_match:
        days = int(day_match.group(1))

    # Extract destination - try multiple patterns
    destination = None

    # Pattern 1: "to [City]" (most common)
    # Remove common verbs before city name: visit, see, explore, etc.
    dest_match = re.search(r'to\s+(?:visit\s+)?([A-Za-z\s]+?)(?:\s+for|\s+with|\s*[,.]|\s*$)', text, re.IGNORECASE)
    if dest_match:
        dest = dest_match.group(1).strip()
        # Remove punctuation and capitalize properly
        dest = re.sub(r'[^\w\s]', '', dest)
        destination = ' '.join(word.capitalize() for word in dest.split())

    # Pattern 2: "visit [City]" or "see [City]"
    if not destination:
        dest_match = re.search(r'(?:visit|see|explore)\s+([A-Za-z\s]+?)(?:\s+for|\s+with|\s*[,.]|\s*$)', text, re.IGNORECASE)
        if dest_match:
            dest = dest_match.group(1).strip()
            dest = re.sub(r'[^\w\s]', '', dest)
            destination = ' '.join(word.capitalize() for word in dest.split())

    # Pattern 3: "Show me [City]" or "[City] for X days" or "[City] trip"
    if not destination:
        # Try "show me [City]" pattern first
        dest_match = re.search(r'show\s+me\s+([A-Za-z\s]+?)(?:\s+for|\s+with|\s*[,.]|\s*$)', text, re.IGNORECASE)
        if dest_match:
            dest = dest_match.group(1).strip()
            dest = re.sub(r'[^\w\s]', '', dest)
            destination = ' '.join(word.capitalize() for word in dest.split())

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

    # Extract preferences by keyword matching
    preferences = []
    for keyword in PREFERENCE_KEYWORDS:
        if keyword in t:
            preferences.append(keyword)

    return TripIntent(destination=destination, days=days, preferences=preferences)
