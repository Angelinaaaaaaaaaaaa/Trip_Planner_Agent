# planner_config.py
# Configuration options for itinerary planning and day range merging

from dataclasses import dataclass


@dataclass
class PlannerConfig:
    """
    Configuration for itinerary planning behavior.

    Controls how days are allocated, when to create rest days,
    and how to merge empty days into ranges.
    """

    # Maximum activities per day (typically 3-4)
    max_activities_per_day: int = 4

    # Minimum activities per day before considering it "sparse"
    # Days with fewer activities may be merged into rest ranges
    min_activities_per_day: int = 2

    # After this many days, start being more aggressive about creating rest ranges
    # For trips longer than this, we'll summarize later days
    dense_activity_days_threshold: int = 14

    # For very long trips, merge consecutive empty/sparse days into ranges
    # if there are this many consecutive sparse days
    min_days_to_merge: int = 3

    # Maximum individual activity days to generate before switching to ranges
    # Prevents performance issues with 1000-day trips
    max_individual_activity_days: int = 50

    # Activity density taper: reduce activities per day after this many days
    # Early days are activity-dense, later days become more relaxed
    activity_taper_start_day: int = 7

    # For trips over this length, automatically summarize the tail
    auto_range_threshold_days: int = 30


# Default configuration singleton
DEFAULT_CONFIG = PlannerConfig()


def get_config() -> PlannerConfig:
    """Get the current planner configuration."""
    return DEFAULT_CONFIG


def set_config(config: PlannerConfig):
    """Set a custom planner configuration."""
    global DEFAULT_CONFIG
    DEFAULT_CONFIG = config
