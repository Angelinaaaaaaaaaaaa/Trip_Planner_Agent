"""
Trip Coordinator Agent - Main Chat Interface
This agent serves as the primary interface for users and coordinates with specialized agents
"""

import os
from typing import Dict, List, Any, Optional
from uagents import Agent, Context, Model
from uagents.contrib.protocols.chat import (
    ChatMessage,
    ChatAcknowledgement,
    TextContent,
    EndSessionContent
)
import json
from dotenv import load_dotenv

# Import utilities
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.claude_integration import get_claude_assistant
from utils.models import TripPreferences, AgentRequest

load_dotenv()

# Agent configuration
AGENT_SEED = os.getenv("AGENT_SEED_PHRASE", "trip_coordinator_seed_phrase_12345")

# Create the Trip Coordinator Agent
trip_coordinator = Agent(
    name="TripCoordinator",
    seed=AGENT_SEED,
    port=8001,
    endpoint=["http://localhost:8001/submit"]
)

# Store conversation context
conversation_contexts: Dict[str, Dict[str, Any]] = {}


class UserQuery(Model):
    """User query model"""
    query: str
    session_id: str
    context: Optional[Dict[str, Any]] = None


@trip_coordinator.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent on startup"""
    ctx.logger.info(f"Trip Coordinator Agent started")
    ctx.logger.info(f"Agent address: {trip_coordinator.address}")


@trip_coordinator.on_message(model=ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handle incoming chat messages using the Chat Protocol
    This is the main entry point for user interactions
    """
    ctx.logger.info(f"Received chat message from {sender}")

    try:
        # Extract message content
        message_text = ""
        for content in msg.contents:
            if isinstance(content, TextContent):
                message_text = content.text
                break

        if not message_text:
            await ctx.send(
                sender,
                ChatMessage(
                    session_id=msg.session_id,
                    contents=[TextContent(text="I didn't receive any message text. Please try again!")]
                )
            )
            return

        # Get or create conversation context
        session_id = msg.session_id
        if session_id not in conversation_contexts:
            conversation_contexts[session_id] = {
                "history": [],
                "preferences": {},
                "trip_plan": None
            }

        context = conversation_contexts[session_id]

        # Add user message to history
        context["history"].append({
            "role": "user",
            "content": message_text
        })

        # Process the message with Claude
        claude = get_claude_assistant()

        # Determine intent and generate response
        response_text = await process_user_message(
            ctx,
            message_text,
            context,
            claude
        )

        # Add assistant response to history
        context["history"].append({
            "role": "assistant",
            "content": response_text
        })

        # Send response
        await ctx.send(
            sender,
            ChatMessage(
                session_id=session_id,
                contents=[TextContent(text=response_text)]
            )
        )

        ctx.logger.info("Response sent successfully")

    except Exception as e:
        ctx.logger.error(f"Error handling chat message: {e}")
        await ctx.send(
            sender,
            ChatMessage(
                session_id=msg.session_id,
                contents=[TextContent(
                    text=f"I apologize, but I encountered an error processing your request. Please try again!"
                )]
            )
        )


async def process_user_message(
    ctx: Context,
    message: str,
    context: Dict[str, Any],
    claude
) -> str:
    """
    Process user message and determine appropriate action
    """

    message_lower = message.lower()

    # Check for specific intents
    if any(keyword in message_lower for keyword in ["recommend", "destination", "where should", "suggest"]):
        return await handle_destination_request(ctx, message, context, claude)

    elif any(keyword in message_lower for keyword in ["itinerary", "plan", "schedule", "day by day"]):
        return await handle_itinerary_request(ctx, message, context, claude)

    elif any(keyword in message_lower for keyword in ["budget", "cost", "price", "expensive", "cheap"]):
        return await handle_budget_request(ctx, message, context, claude)

    elif any(keyword in message_lower for keyword in ["weather", "climate", "temperature", "forecast"]):
        return await handle_weather_request(ctx, message, context, claude)

    elif any(keyword in message_lower for keyword in ["tips", "advice", "culture", "local", "customs"]):
        return await handle_insights_request(ctx, message, context, claude)

    else:
        # General conversation - use Claude for natural response
        conversation_history = context["history"][-10:]  # Last 10 messages
        response = await claude.conversational_response(
            conversation_history,
            message
        )
        return response


async def handle_destination_request(
    ctx: Context,
    message: str,
    context: Dict[str, Any],
    claude
) -> str:
    """Handle destination recommendation requests"""

    # Extract preferences from conversation or ask for them
    if not context.get("preferences"):
        return """I'd love to help you find the perfect destination! To give you the best recommendations, I need to know a bit more about your preferences:

1. What's your approximate budget? (budget-friendly, moderate, or luxury)
2. What are your main interests? (e.g., adventure, culture, food, beaches, history)
3. How many days are you planning to travel?
4. What's your travel style? (relaxed, balanced, or action-packed)
5. Who are you traveling with? (solo, couple, family, friends)
6. Any specific season or month you're considering?

You can tell me all at once or we can go through them one by one!"""

    try:
        # Build preferences dict
        preferences = {
            "budget": context["preferences"].get("budget", "moderate"),
            "interests": context["preferences"].get("interests", []),
            "travel_style": context["preferences"].get("travel_style", "balanced"),
            "duration": context["preferences"].get("duration", 7),
            "season": context["preferences"].get("season", "flexible"),
            "group_size": context["preferences"].get("group_size", "solo"),
            "special_requirements": message
        }

        # Get recommendations from Claude
        recommendations = await claude.generate_destination_recommendations(preferences)

        return f"Based on your preferences, here are my top destination recommendations:\n\n{recommendations}\n\nWould you like me to create a detailed itinerary for any of these destinations?"

    except Exception as e:
        ctx.logger.error(f"Error generating recommendations: {e}")
        return "I encountered an issue generating recommendations. Could you tell me more about what you're looking for in a destination?"


async def handle_itinerary_request(
    ctx: Context,
    message: str,
    context: Dict[str, Any],
    claude
) -> str:
    """Handle itinerary creation requests"""

    destination = context.get("destination")
    duration = context.get("preferences", {}).get("duration", 5)

    if not destination:
        return "I'd be happy to create an itinerary! First, which destination are you interested in? If you haven't chosen yet, I can recommend some destinations based on your preferences."

    try:
        interests = context.get("preferences", {}).get("interests", ["sightseeing"])
        budget = context.get("preferences", {}).get("budget", "moderate")

        itinerary = await claude.create_detailed_itinerary(
            destination=destination,
            duration=duration,
            interests=interests,
            budget=budget,
            additional_context=message
        )

        return f"Here's your personalized {duration}-day itinerary for {destination}:\n\n{itinerary}\n\nWould you like me to adjust anything or provide more details about specific activities?"

    except Exception as e:
        ctx.logger.error(f"Error creating itinerary: {e}")
        return "I had trouble creating the itinerary. Could you provide more details about your destination and preferences?"


async def handle_budget_request(
    ctx: Context,
    message: str,
    context: Dict[str, Any],
    claude
) -> str:
    """Handle budget-related requests"""

    trip_details = context.get("trip_plan")

    if not trip_details:
        return """I can help you plan and optimize your travel budget! To get started, tell me:

1. Where are you planning to go?
2. How many days?
3. What's your total budget?
4. What are your main expense categories? (flights, hotels, food, activities, etc.)

I'll analyze your budget and provide optimization recommendations!"""

    try:
        # This would integrate with actual expense data
        return "Budget analysis feature coming soon! For now, I can provide general budget guidance for your destination."

    except Exception as e:
        ctx.logger.error(f"Error with budget analysis: {e}")
        return "I encountered an issue with the budget analysis. Let me help you with general budget planning instead."


async def handle_weather_request(
    ctx: Context,
    message: str,
    context: Dict[str, Any],
    claude
) -> str:
    """Handle weather information requests"""

    destination = context.get("destination")

    if not destination:
        return "Which destination would you like weather information for?"

    # Weather integration would go here
    return f"Weather service integration for {destination} is being set up. In the meantime, I recommend checking weather.com for up-to-date forecasts. Would you like tips on the best time to visit {destination}?"


async def handle_insights_request(
    ctx: Context,
    message: str,
    context: Dict[str, Any],
    claude
) -> str:
    """Handle local insights and tips requests"""

    destination = context.get("destination")

    if not destination:
        return "Which destination would you like local insights about?"

    try:
        insights = await claude.get_local_insights(destination)
        return f"Here are important local insights for {destination}:\n\n{insights}\n\nDo you have any specific questions about local customs or practical matters?"

    except Exception as e:
        ctx.logger.error(f"Error getting insights: {e}")
        return f"I had trouble fetching specific insights, but I'd be happy to answer any questions you have about {destination}!"


@trip_coordinator.on_message(model=EndSessionContent)
async def handle_end_session(ctx: Context, sender: str, msg: EndSessionContent):
    """Handle session end"""
    session_id = msg.session_id
    if session_id in conversation_contexts:
        del conversation_contexts[session_id]

    ctx.logger.info(f"Session {session_id} ended")


if __name__ == "__main__":
    print("Starting Trip Coordinator Agent...")
    print(f"Agent Address: {trip_coordinator.address}")
    trip_coordinator.run()
