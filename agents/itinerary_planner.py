"""
Itinerary Planner Agent
Specializes in creating detailed day-by-day itineraries
"""

import os
import sys
from uagents import Agent, Context, Model
from typing import Dict, Any, List
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.claude_integration import get_claude_assistant

load_dotenv()

# Agent configuration
itinerary_planner = Agent(
    name="ItineraryPlanner",
    seed="itinerary_planner_seed_phrase_11223",
    port=8003,
    endpoint=["http://localhost:8003/submit"]
)


class ItineraryRequest(Model):
    """Request for itinerary creation"""
    destination: str
    duration: int
    interests: List[str]
    budget: str
    preferences: Dict[str, Any] = {}


class ItineraryResponse(Model):
    """Response with detailed itinerary"""
    itinerary: str
    estimated_cost: float
    highlights: List[str]


@itinerary_planner.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent"""
    ctx.logger.info("Itinerary Planner Agent started")
    ctx.logger.info(f"Agent address: {itinerary_planner.address}")


@itinerary_planner.on_message(model=ItineraryRequest)
async def handle_itinerary_request(
    ctx: Context,
    sender: str,
    msg: ItineraryRequest
):
    """
    Create detailed itineraries using Claude's planning capabilities
    """
    ctx.logger.info(f"Received itinerary request for {msg.destination}")

    try:
        claude = get_claude_assistant()

        # Generate itinerary using Claude
        itinerary_text = await claude.create_detailed_itinerary(
            destination=msg.destination,
            duration=msg.duration,
            interests=msg.interests,
            budget=msg.budget,
            additional_context=str(msg.preferences)
        )

        response = ItineraryResponse(
            itinerary=itinerary_text,
            estimated_cost=0.0,  # Would calculate from itinerary
            highlights=[]
        )

        await ctx.send(sender, response)
        ctx.logger.info("Itinerary sent successfully")

    except Exception as e:
        ctx.logger.error(f"Error creating itinerary: {e}")


@itinerary_planner.on_interval(period=300.0)
async def log_status(ctx: Context):
    """Periodic status log"""
    ctx.logger.info("Itinerary Planner Agent is active and ready")


if __name__ == "__main__":
    print("Starting Itinerary Planner Agent...")
    print(f"Agent Address: {itinerary_planner.address}")
    itinerary_planner.run()
