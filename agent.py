# agent.py
# Trip Planner Agent for Agentverse using uAgents and Chat Protocol
# Powered by Claude AI for intelligent trip planning

import os
from datetime import datetime
from uuid import uuid4
from typing import Optional
from dotenv import load_dotenv

from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low

# Import Chat Protocol components
try:
    from uagents_core.contrib.protocols.chat import (
        ChatAcknowledgement,
        ChatMessage,
        EndSessionContent,
        StartSessionContent,
        TextContent,
        chat_protocol_spec,
    )
except ImportError:
    # Fallback for older versions
    from uagents.contrib.protocols.chat import (
        ChatAcknowledgement,
        ChatMessage,
        EndSessionContent,
        StartSessionContent,
        TextContent,
        chat_protocol_spec,
    )

from intent import parse_intent
from planner import build_itinerary
from exporters import itinerary_to_markdown, itinerary_to_ics
from data_sources import get_supported_cities, is_city_supported

# Load environment variables
load_dotenv()

# Get configuration from environment
AGENT_SEED = os.getenv("AGENT_SEED", "trip_planner_agent_seed_2024")
AGENT_NAME = os.getenv("AGENT_NAME", "trip_coordinator")
AGENT_PORT = int(os.getenv("AGENT_PORT", "8000"))

# Create the agent instance
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=AGENT_PORT,
)

# Fund agent if needed (for testnet)
fund_agent_if_low(agent.wallet.address())

# Initialize the Chat Protocol
chat_proto = Protocol(spec=chat_protocol_spec)


def make_text_msg(text: str) -> ChatMessage:
    """Helper to wrap plain text into a ChatMessage compatible with the Chat Protocol."""
    content = [TextContent(type="text", text=text)]
    return ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=content)


@chat_proto.on_message(ChatMessage)
async def on_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages from users/agents/ASI:One."""
    ctx.logger.info(f"Received message from {sender}")

    # Always acknowledge receipt
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        )
    )

    # Extract the latest text message in the batch
    user_text: Optional[str] = None
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started with {sender}")
        elif isinstance(item, TextContent):
            user_text = item.text
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended with {sender}")

    if not user_text:
        welcome_msg = (
            "Hi! I'm your AI Trip Planner powered by Claude.\n\n"
            "Tell me about your trip and I'll create a personalized itinerary!\n\n"
            "Example: 'Plan me a 3-day trip to Tokyo for food and culture'\n\n"
            f"I currently support: {', '.join(get_supported_cities())}"
        )
        await ctx.send(sender, make_text_msg(welcome_msg))
        return

    ctx.logger.info(f"Processing request: {user_text}")

    # Parse intent using Claude AI
    intent = parse_intent(user_text)

    if not intent.destination:
        error_msg = (
            "I couldn't identify a destination in your request.\n\n"
            "Please include a city name, for example:\n"
            "- 'Plan a trip to Tokyo'\n"
            "- 'I want to visit Barcelona for 2 days'\n\n"
            f"Supported cities: {', '.join(get_supported_cities())}"
        )
        await ctx.send(sender, make_text_msg(error_msg))
        return

    # Validate that the destination is supported (with normalized matching)
    if not is_city_supported(intent.destination):
        error_msg = (
            f"I found '{intent.destination}' in your request, but I don't have data for that city yet.\n\n"
            f"Supported cities: {', '.join(get_supported_cities())}\n\n"
            "Please try one of these cities!"
        )
        await ctx.send(sender, make_text_msg(error_msg))
        return

    if not intent.days:
        # Default to 3 days if not specified
        intent.days = 3
        ctx.logger.info(f"No duration specified, defaulting to {intent.days} days")

    # Build itinerary
    ctx.logger.info(
        f"Building itinerary for {intent.destination}, "
        f"{intent.days} days, preferences: {intent.preferences}"
    )
    itinerary = build_itinerary(intent)

    # Format as markdown
    md = itinerary_to_markdown(itinerary)

    # Generate calendar file
    ics_path = itinerary_to_ics(itinerary)

    # Build response
    reply = md
    if ics_path:
        reply += f"\n\n---\n📅 **Calendar Export:** I've created `{ics_path}` that you can import into Google Calendar, Apple Calendar, or Outlook!"

    # Send response
    await ctx.send(sender, make_text_msg(reply))
    ctx.logger.info(f"Sent itinerary to {sender}")


@chat_proto.on_message(ChatAcknowledgement)
async def on_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Log acknowledgements for messages this agent has sent."""
    ctx.logger.info(f"ACK from {sender} for message {msg.acknowledged_msg_id}")


# Include the protocol and publish the manifest to Agentverse for discovery
agent.include(chat_proto, publish_manifest=True)


@agent.on_event("startup")
async def startup(ctx: Context):
    """Log agent startup information."""
    ctx.logger.info(f"Trip Planner Agent started!")
    ctx.logger.info(f"Agent name: {agent.name}")
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"Agent port: {AGENT_PORT}")
    ctx.logger.info(f"Chat Protocol enabled and manifest published")
    ctx.logger.info(f"Supported cities: {', '.join(get_supported_cities())}")


if __name__ == "__main__":
    agent.run()
