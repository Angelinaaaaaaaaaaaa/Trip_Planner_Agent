"""
Claude API Integration for Intelligent Trip Planning
Provides advanced reasoning capabilities for the Trip Planner Agent
"""

import os
from typing import Optional, Dict, Any, List
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class ClaudeAssistant:
    """
    Wrapper for Claude API providing specialized trip planning intelligence
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"  # Latest Claude model

    async def generate_destination_recommendations(
        self,
        preferences: Dict[str, Any]
    ) -> str:
        """
        Generate personalized destination recommendations based on user preferences

        Args:
            preferences: Dict containing budget, interests, travel_style, season, etc.

        Returns:
            Structured recommendations with reasoning
        """

        prompt = f"""You are an expert travel advisor. Based on the following preferences, recommend 3-5 ideal destinations with detailed reasoning.

User Preferences:
- Budget: {preferences.get('budget', 'Not specified')}
- Interests: {preferences.get('interests', 'Not specified')}
- Travel Style: {preferences.get('travel_style', 'Not specified')}
- Duration: {preferences.get('duration', 'Not specified')} days
- Season/Month: {preferences.get('season', 'Not specified')}
- Group Size: {preferences.get('group_size', 'Solo')}
- Special Requirements: {preferences.get('special_requirements', 'None')}

For each destination, provide:
1. Destination name and country
2. Why it matches their preferences (2-3 sentences)
3. Best time to visit
4. Estimated daily budget
5. Top 3 must-do activities
6. Unique selling point

Format your response as a structured JSON-like text that's easy to parse."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text

    async def create_detailed_itinerary(
        self,
        destination: str,
        duration: int,
        interests: List[str],
        budget: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Create a detailed day-by-day itinerary using Claude's reasoning

        Args:
            destination: The chosen destination
            duration: Trip duration in days
            interests: List of user interests
            budget: Budget level (budget/moderate/luxury)
            additional_context: Any additional requirements

        Returns:
            Detailed day-by-day itinerary
        """

        prompt = f"""Create a detailed {duration}-day itinerary for {destination}.

Trip Details:
- Duration: {duration} days
- Interests: {', '.join(interests)}
- Budget Level: {budget}
{f"- Additional Requirements: {additional_context}" if additional_context else ""}

For each day, provide:
1. Day number and theme
2. Morning activities (with timing)
3. Afternoon activities (with timing)
4. Evening activities (with timing)
5. Recommended restaurants/cafes
6. Estimated daily cost
7. Travel tips and logistics
8. Weather considerations

Make sure to:
- Balance activities with rest time
- Consider travel time between locations
- Include local experiences and hidden gems
- Suggest backup options for bad weather
- Provide practical tips (tickets, reservations, etc.)

Format the itinerary in a clear, easy-to-read structure."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text

    async def optimize_budget(
        self,
        trip_details: Dict[str, Any],
        current_budget: float,
        expenses: List[Dict[str, Any]]
    ) -> str:
        """
        Analyze and optimize trip budget using Claude's analytical capabilities

        Args:
            trip_details: Overall trip information
            current_budget: Total available budget
            expenses: List of planned expenses

        Returns:
            Budget analysis and optimization recommendations
        """

        expenses_text = "\n".join([
            f"- {exp.get('category')}: ${exp.get('amount')} ({exp.get('description')})"
            for exp in expenses
        ])

        prompt = f"""Analyze this trip budget and provide optimization recommendations.

Trip: {trip_details.get('destination')} for {trip_details.get('duration')} days
Total Budget: ${current_budget}

Planned Expenses:
{expenses_text}

Please provide:
1. Budget breakdown analysis (percentages by category)
2. Areas where money can be saved without sacrificing experience
3. Potential hidden costs to consider
4. Recommended budget reallocation
5. Tips for getting best value
6. Risk assessment (is budget realistic?)

Be specific with dollar amounts and actionable recommendations."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text

    async def get_local_insights(
        self,
        destination: str,
        specific_questions: Optional[List[str]] = None
    ) -> str:
        """
        Get cultural insights, local tips, and practical advice

        Args:
            destination: The destination
            specific_questions: Optional list of specific questions

        Returns:
            Cultural insights and practical tips
        """

        questions_text = ""
        if specific_questions:
            questions_text = "\n\nSpecific Questions:\n" + "\n".join(
                f"- {q}" for q in specific_questions
            )

        prompt = f"""Provide comprehensive local insights for travelers visiting {destination}.

Include:
1. Cultural etiquette and dos/don'ts
2. Local customs and traditions to be aware of
3. Safety tips and precautions
4. Transportation guide (best ways to get around)
5. Language basics and useful phrases
6. Tipping customs
7. Best local foods to try
8. Money and payment tips
9. SIM card and internet access
10. Emergency contacts and important information
{questions_text}

Provide practical, actionable advice that helps travelers have a smooth and respectful experience."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text

    async def conversational_response(
        self,
        conversation_history: List[Dict[str, str]],
        user_message: str
    ) -> str:
        """
        Generate natural conversational response for the chat interface

        Args:
            conversation_history: Previous messages
            user_message: Current user message

        Returns:
            Natural language response
        """

        system_prompt = """You are a friendly, knowledgeable AI travel assistant helping users plan their dream trips.

Your personality:
- Enthusiastic about travel and helping people explore the world
- Practical and detail-oriented
- Culturally aware and respectful
- Proactive in asking clarifying questions
- Honest about limitations

When helping users:
- Ask clarifying questions to understand their needs
- Provide specific, actionable recommendations
- Consider budget, time, and personal preferences
- Offer alternatives and backup plans
- Share insider tips and hidden gems

Keep responses conversational, helpful, and engaging."""

        messages = [{"role": msg["role"], "content": msg["content"]}
                   for msg in conversation_history]
        messages.append({"role": "user", "content": user_message})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        )

        return response.content[0].text


# Singleton instance
_claude_assistant: Optional[ClaudeAssistant] = None


def get_claude_assistant() -> ClaudeAssistant:
    """Get or create singleton ClaudeAssistant instance"""
    global _claude_assistant
    if _claude_assistant is None:
        _claude_assistant = ClaudeAssistant()
    return _claude_assistant
