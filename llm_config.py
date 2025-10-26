# llm_config.py
# Configuration for LLM-powered trip planning

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMConfig:
    """Configuration for LLM-powered trip planning."""
    
    # API Configuration
    anthropic_api_key: Optional[str] = None
    model_name: str = "claude-3-haiku-20240307"  # Using available model
    
    # Generation Parameters
    max_tokens: int = 4000
    temperature: float = 0.7  # Creative but controlled
    planning_temperature: float = 0.3  # More structured for itinerary planning
    
    # Planning Parameters
    max_pois_per_city: int = 50  # Maximum POIs to generate
    min_pois_per_day: int = 1
    max_pois_per_day: int = 4
    
    # Fallback Behavior
    fallback_to_static: bool = True  # Fall back to static planner if LLM fails
    retry_on_failure: bool = True    # Retry LLM calls once on failure
    
    # Output Settings
    include_reasoning: bool = False  # Include LLM reasoning in output
    debug_mode: bool = False         # Print debug information
    
    def __post_init__(self):
        """Load API key from environment if not provided."""
        if not self.anthropic_api_key:
            self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")


# Default configuration
DEFAULT_LLM_CONFIG = LLMConfig()


def get_llm_config() -> LLMConfig:
    """Get the current LLM configuration."""
    return DEFAULT_LLM_CONFIG


def set_llm_config(config: LLMConfig):
    """Set a custom LLM configuration."""
    global DEFAULT_LLM_CONFIG
    DEFAULT_LLM_CONFIG = config


def is_llm_available() -> bool:
    """Check if LLM functionality is available."""
    # Read directly from environment to avoid stale cached values
    return bool(os.getenv("ANTHROPIC_API_KEY"))