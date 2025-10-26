# exporters_v2.py
# Export itinerary to markdown and ICS calendar formats
# Now supports day ranges for long trips

from typing import List, Dict
from datetime import datetime, timedelta
from dateutil.tz import tzlocal
from planner import Itinerary, ItineraryItem, DayRange


def itinerary_to_markdown(itinerary: Itinerary) -> str:
    """
    Format itinerary as markdown with clickable links and day ranges.

    Handles both specific activities (ItineraryItem) and day ranges (DayRange).
    Day ranges are displayed as summary blocks.

    Args:
        itinerary: Complete trip itinerary with items and ranges

    Returns:
        Formatted markdown string
    """
    lines = [f"# {itinerary.days}-Day Trip to {itinerary.destination}\n"]

    # Organize content by day
    days_content: Dict[int, List] = {}

    # Add specific activities
    for item in sorted(itinerary.items, key=lambda x: (x.day, x.time)):
        days_content.setdefault(item.day, []).append(item)

    # Add day ranges
    for day_range in sorted(itinerary.day_ranges, key=lambda x: x.start_day):
        # Mark each day in the range
        for day in range(day_range.start_day, day_range.end_day + 1):
            days_content.setdefault(day, []).append(day_range)

    # Render in order
    current_day = 0
    current_range = None

    for day in sorted(days_content.keys()):
        content_list = days_content[day]

        # Check if this day is part of a range
        range_item = next((item for item in content_list if isinstance(item, DayRange)), None)

        if range_item:
            # This day is in a range
            if current_range != range_item:
                # New range started
                if range_item.start_day == range_item.end_day:
                    lines.append(f"\n## Day {range_item.start_day}")
                else:
                    lines.append(f"\n## Days {range_item.start_day}–{range_item.end_day}")

                lines.append(f"_{range_item.description}_")

                # Check if there are also specific activities on these days
                activities = [item for item in content_list if isinstance(item, ItineraryItem)]
                if activities:
                    lines.append("\n**Optional activities:**")
                    for item in sorted(activities, key=lambda x: x.time):
                        tags_str = ", ".join(item.tags) if item.tags else "attraction"
                        if item.url:
                            lines.append(f"- [{item.name}]({item.url}) _{tags_str}_")
                        else:
                            lines.append(f"- {item.name} _{tags_str}_")

                current_range = range_item

        else:
            # Regular day with activities
            if day != current_day:
                activities = [item for item in content_list if isinstance(item, ItineraryItem)]
                if activities:
                    # Get area from first activity
                    area = activities[0].area if activities else "Various"
                    lines.append(f"\n## Day {day} - {area}")

                for item in sorted(activities, key=lambda x: x.time):
                    # Format tags nicely
                    tags_str = ", ".join(item.tags) if item.tags else "attraction"

                    # Create clickable link if URL available
                    if item.url:
                        lines.append(f"**{item.time}** - [{item.name}]({item.url}) _{tags_str}_")
                    else:
                        lines.append(f"**{item.time}** - {item.name} _{tags_str}_")

                current_day = day
                current_range = None

    return "\n".join(lines)


def itinerary_to_ics(itinerary: Itinerary, start_date: datetime = None, output_dir: str = None) -> str:
    """
    Export itinerary as ICS calendar file that can be imported to Google Calendar,
    Apple Calendar, Outlook, etc.

    Handles both specific activities and day ranges. Day ranges are exported as
    all-day events.

    Args:
        itinerary: Complete trip itinerary with items and ranges
        start_date: When the trip starts (defaults to tomorrow at 9 AM)
        output_dir: Directory to save the file (defaults to current directory)

    Returns:
        Path to the created .ics file
    """
    if start_date is None:
        # Default to tomorrow at 9 AM in local timezone
        start_date = datetime.now(tzlocal()) + timedelta(days=1)
        start_date = start_date.replace(hour=9, minute=0, second=0, microsecond=0)

    # Group activities by day
    days_dict: Dict[int, List[ItineraryItem]] = {}
    for item in itinerary.items:
        days_dict.setdefault(item.day, []).append(item)

    def format_ics_datetime(dt: datetime) -> str:
        """Format datetime for ICS file."""
        return dt.strftime("%Y%m%dT%H%M%S")

    def format_ics_date(dt: datetime) -> str:
        """Format date for ICS all-day events."""
        return dt.strftime("%Y%m%d")

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

    # Add specific activities as timed events
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

    # Add day ranges as all-day events
    for day_range in itinerary.day_ranges:
        # Calculate date range
        range_start_date = start_date + timedelta(days=day_range.start_day - 1)
        # ICS all-day events: end date is exclusive, so add 1 extra day
        range_end_date = start_date + timedelta(days=day_range.end_day)

        # Create all-day event for the range
        summary = f"{day_range.description}"
        if day_range.start_day != day_range.end_day:
            num_days = day_range.end_day - day_range.start_day + 1
            summary = f"{day_range.description} ({num_days} days)"

        ics_lines.extend([
            "BEGIN:VEVENT",
            f"DTSTART;VALUE=DATE:{format_ics_date(range_start_date)}",
            f"DTEND;VALUE=DATE:{format_ics_date(range_end_date)}",
            f"SUMMARY:{summary}",
            f"DESCRIPTION:{day_range.description}",
            f"LOCATION:{itinerary.destination}",
            f"UID:{itinerary.destination}-range{day_range.start_day}-{day_range.end_day}@tripplanner",
            "STATUS:CONFIRMED",
            "TRANSP:TRANSPARENT",  # Show as "free" time
            "END:VEVENT",
        ])

    ics_lines.append("END:VCALENDAR")

    # Write to file
    filename = f"trip_{itinerary.destination.lower().replace(' ', '_')}_{itinerary.days}days.ics"

    # Use output_dir if provided, otherwise use current directory
    import os
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
    else:
        filepath = filename

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ics_lines))
        return filepath
    except Exception as e:
        print(f"Error creating ICS file: {e}")
        return ""
