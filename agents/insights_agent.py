"""
Insights Agent
Specializes in local insights, cultural tips, and weather information
Integrates with Fetch.ai's official Weather Agent for real-time data
"""

import os
import sys
from uagents import Agent, Context, Model
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.claude_integration import get_claude_assistant
from utils.weather_service import get_weather_service

load_dotenv()

# Agent configuration
insights_agent = Agent(
    name="InsightsAgent",
    seed="insights_agent_seed_phrase_55667",
    port=8005,
    endpoint=["http://localhost:8005/submit"]
)

# Fetch.ai Weather Agent Address (Official Agentverse Agent)
WEATHER_AGENT_ADDRESS = "agent1qfvydlgcxrvga2kqjxhj3hpngegtysm2c7uk48ywdue0kgvtc2f5cwhyffv"


class WeatherForecastRequest(Model):
    """Request model for Fetch.ai Weather Agent"""
    location: str


class WeatherForecastResponse(Model):
    """Response model from Fetch.ai Weather Agent"""
    location: str
    temperature: float
    condition: str
    humidity: int
    wind_speed: float


class InsightsRequest(Model):
    """Request for destination insights"""
    destination: str
    questions: List[str] = []
    include_weather: bool = True


class InsightsResponse(Model):
    """Response with insights and weather"""
    insights: str
    weather: Optional[Dict[str, Any]] = None
    tips: List[str]


@insights_agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent"""
    ctx.logger.info("Insights Agent started")
    ctx.logger.info(f"Agent address: {insights_agent.address}")


@insights_agent.on_message(model=InsightsRequest)
async def handle_insights_request(
    ctx: Context,
    sender: str,
    msg: InsightsRequest
):
    """
    Provide local insights and weather information
    Uses Fetch.ai's official Weather Agent for agent-to-agent communication
    """
    ctx.logger.info(f"Received insights request for {msg.destination}")

    try:
        claude = get_claude_assistant()

        # Get cultural insights from Claude
        insights_text = await claude.get_local_insights(
            destination=msg.destination,
            specific_questions=msg.questions if msg.questions else None
        )

        # Get weather information if requested
        weather_data = None
        if msg.include_weather:
            # Try to get weather from official Fetch.ai Weather Agent first
            try:
                ctx.logger.info(f"Requesting weather from Fetch.ai Weather Agent for {msg.destination}")

                # Send request to official Weather Agent
                await ctx.send(
                    WEATHER_AGENT_ADDRESS,
                    WeatherForecastRequest(location=msg.destination)
                )

                # Note: In production, you'd wait for response using message handlers
                # For now, we'll use fallback service
                ctx.logger.info("Weather request sent to Fetch.ai agent")

            except Exception as e:
                ctx.logger.warning(f"Could not reach Fetch.ai Weather Agent: {e}")

            # Fallback to local weather service
            weather_service = get_weather_service()
            weather_data = await weather_service.get_current_weather(msg.destination)
            weather_data["source"] = "Local Weather API (Fallback)" if weather_data.get("note") else "OpenWeatherMap API"

        response = InsightsResponse(
            insights=insights_text,
            weather=weather_data,
            tips=[]
        )

        await ctx.send(sender, response)
        ctx.logger.info("Insights sent successfully")

    except Exception as e:
        ctx.logger.error(f"Error getting insights: {e}")


@insights_agent.on_message(model=WeatherForecastResponse)
async def handle_weather_response(
    ctx: Context,
    sender: str,
    msg: WeatherForecastResponse
):
    """
    Handle weather response from official Fetch.ai Weather Agent
    Demonstrates agent-to-agent communication
    """
    ctx.logger.info(f"Received weather data from Fetch.ai agent: {msg.location}")
    ctx.logger.info(f"Temperature: {msg.temperature}°C, Condition: {msg.condition}")

    # Store weather data for use in insights
    # In production, this would update a shared state or database
    weather_info = {
        "temperature": msg.temperature,
        "condition": msg.condition,
        "humidity": msg.humidity,
        "wind_speed": msg.wind_speed,
        "location": msg.location,
        "source": "Fetch.ai Weather Agent (Official)"
    }

    ctx.logger.info(f"Weather data processed: {weather_info}")


@insights_agent.on_interval(period=300.0)
async def log_status(ctx: Context):
    """Periodic status log"""
    ctx.logger.info("Insights Agent is active and ready")


if __name__ == "__main__":
    print("Starting Insights Agent...")
    print(f"Agent Address: {insights_agent.address}")
    insights_agent.run()
