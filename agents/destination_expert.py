"""
Destination Expert Agent
Specializes in destination recommendations based on user preferences
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
destination_expert = Agent(
    name="DestinationExpert",
    seed="destination_expert_seed_phrase_67890",
    port=8002,
    endpoint=["http://localhost:8002/submit"]
)


class DestinationRequest(Model):
    """Request for destination recommendations"""
    preferences: Dict[str, Any]
    constraints: Dict[str, Any] = {}


class DestinationResponse(Model):
    """Response with destination recommendations"""
    recommendations: List[Dict[str, Any]]
    reasoning: str


@destination_expert.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent"""
    ctx.logger.info("Destination Expert Agent started")
    ctx.logger.info(f"Agent address: {destination_expert.address}")


@destination_expert.on_message(model=DestinationRequest)
async def handle_destination_request(
    ctx: Context,
    sender: str,
    msg: DestinationRequest
):
    """
    Process destination recommendation requests using Claude's intelligence
    """
    ctx.logger.info(f"Received destination request from {sender}")

    try:
        claude = get_claude_assistant()

        # Generate recommendations using Claude
        recommendations_text = await claude.generate_destination_recommendations(
            msg.preferences
        )

        # Parse and structure the response
        response = DestinationResponse(
            recommendations=[],  # Would parse Claude's response here
            reasoning=recommendations_text
        )

        await ctx.send(sender, response)
        ctx.logger.info("Destination recommendations sent")

    except Exception as e:
        ctx.logger.error(f"Error processing destination request: {e}")


@destination_expert.on_interval(period=300.0)
async def log_status(ctx: Context):
    """Periodic status log"""
    ctx.logger.info("Destination Expert Agent is active and ready")


if __name__ == "__main__":
    print("Starting Destination Expert Agent...")
    print(f"Agent Address: {destination_expert.address}")
    destination_expert.run()
