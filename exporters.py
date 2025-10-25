# exporters.py
# Export itinerary to markdown and ICS calendar formats

from typing import List
from datetime import datetime, timedelta
from dateutil.tz import tzlocal
from planner import Itinerary, ItineraryItem


def itinerary_to_markdown(itinerary: Itinerary) -> str:
    """
    Format itinerary as markdown with clickable links.

    Args:
        itinerary: Complete trip itinerary

    Returns:
        Formatted markdown string
    """
    lines = [f"# {itinerary.days}-Day Trip to {itinerary.destination}\n"]

    current_day = 0
    for item in sorted(itinerary.items, key=lambda x: (x.day, x.time)):
        if item.day != current_day:
            lines.append(f"\n## Day {item.day} - {item.area}")
            current_day = item.day

        # Format tags nicely
        tags_str = ", ".join(item.tags) if item.tags else "attraction"

        # Create clickable link if URL available
        if item.url:
            lines.append(f"**{item.time}** - [{item.name}]({item.url}) _{tags_str}_")
        else:
            lines.append(f"**{item.time}** - {item.name} _{tags_str}_")

    return "\n".join(lines)


def itinerary_to_ics(itinerary: Itinerary, start_date: datetime = None) -> str:
    """
    Export itinerary as ICS calendar file that can be imported to Google Calendar,
    Apple Calendar, Outlook, etc.

    Args:
        itinerary: Complete trip itinerary
        start_date: When the trip starts (defaults to tomorrow at 9 AM)

    Returns:
        Path to the created .ics file
    """
    if start_date is None:
        # Default to tomorrow at 9 AM in local timezone
        start_date = datetime.now(tzlocal()) + timedelta(days=1)
        start_date = start_date.replace(hour=9, minute=0, second=0, microsecond=0)

    # Group items by day
    days_dict = {}
    for item in itinerary.items:
        days_dict.setdefault(item.day, []).append(item)

    def format_ics_datetime(dt: datetime) -> str:
        """Format datetime for ICS file."""
        return dt.strftime("%Y%m%dT%H%M%S")

    # Build ICS content
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Trip Planner Agent//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{itinerary.destination} Trip",
        "X-WR-TIMEZONE:UTC",
    ]

    for day_num in range(1, itinerary.days + 1):
        day_items = days_dict.get(day_num, [])
        if not day_items:
            continue

        # Sort items by time
        day_items = sorted(day_items, key=lambda x: x.time)

        for item in day_items:
            # Parse time
            hour, minute = map(int, item.time.split(':'))

            # Calculate event start time
            event_date = start_date + timedelta(days=day_num - 1)
            event_start = event_date.replace(hour=hour, minute=minute)

            # Event lasts 2 hours (adjustable)
            event_end = event_start + timedelta(hours=2)

            # Build description with tags and area
            description = f"Area: {item.area}"
            if item.tags:
                description += f"\\nCategories: {', '.join(item.tags)}"
            if item.url:
                description += f"\\nMap: {item.url}"

            # Create event
            ics_lines.extend([
                "BEGIN:VEVENT",
                f"DTSTART:{format_ics_datetime(event_start)}",
                f"DTEND:{format_ics_datetime(event_end)}",
                f"SUMMARY:{item.name}",
                f"DESCRIPTION:{description}",
                f"LOCATION:{item.area}, {itinerary.destination}",
                f"UID:{itinerary.destination}-day{day_num}-{item.time}@tripplanner",
                "STATUS:CONFIRMED",
                "END:VEVENT",
            ])

    ics_lines.append("END:VCALENDAR")

    # Write to file
    filename = f"trip_{itinerary.destination.lower().replace(' ', '_')}_{itinerary.days}days.ics"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ics_lines))
        return filename
    except Exception as e:
        print(f"Error creating ICS file: {e}")
        return ""
