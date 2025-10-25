"""
Run a single Trip Coordinator agent for testing
This is useful for Agentverse deployment and testing
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.trip_coordinator import trip_coordinator

if __name__ == "__main__":
    print("=" * 60)
    print("🌍 Trip Planner Agent - Single Instance")
    print("=" * 60)
    print()
    print(f"Agent Name: {trip_coordinator.name}")
    print(f"Agent Address: {trip_coordinator.address}")
    print(f"Endpoint: http://localhost:8001/submit")
    print()
    print("This agent is ready for Agentverse registration!")
    print("=" * 60)
    print()

    trip_coordinator.run()
