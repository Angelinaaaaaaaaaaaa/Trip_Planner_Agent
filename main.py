"""
Main orchestration script for Trip Planner Agent System
Runs all specialized agents together
"""

import asyncio
import subprocess
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_agent(agent_file: str):
    """Run a single agent in a subprocess"""
    return subprocess.Popen(
        [sys.executable, agent_file],
        cwd=project_root
    )


async def main():
    """Start all agents"""
    print("=" * 60)
    print("🌍 Trip Planner Agent System")
    print("=" * 60)
    print()
    print("Starting multi-agent system...")
    print()

    # Define all agent scripts
    agent_files = [
        "agents/trip_coordinator.py",
        "agents/destination_expert.py",
        "agents/itinerary_planner.py",
        "agents/budget_optimizer.py",
        "agents/insights_agent.py"
    ]

    processes = []

    try:
        # Start each agent
        for agent_file in agent_files:
            agent_path = project_root / agent_file
            if agent_path.exists():
                print(f"✓ Starting {agent_file}...")
                process = run_agent(str(agent_path))
                processes.append(process)
                await asyncio.sleep(2)  # Stagger startup
            else:
                print(f"✗ Agent file not found: {agent_file}")

        print()
        print("=" * 60)
        print("✓ All agents started successfully!")
        print("=" * 60)
        print()
        print("Agent Information:")
        print("-" * 60)
        print("Trip Coordinator:    http://localhost:8001 (Main Interface)")
        print("Destination Expert:  http://localhost:8002")
        print("Itinerary Planner:   http://localhost:8003")
        print("Budget Optimizer:    http://localhost:8004")
        print("Insights Agent:      http://localhost:8005")
        print("-" * 60)
        print()
        print("Press Ctrl+C to stop all agents")
        print()

        # Keep running until interrupted
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n\nStopping all agents...")
        for process in processes:
            process.terminate()
        print("✓ All agents stopped")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        for process in processes:
            process.terminate()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown complete")
