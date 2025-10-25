"""
Data models for Trip Planner Agent system
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TripPreferences(BaseModel):
    """User's trip preferences"""
    budget: Optional[str] = Field(None, description="Budget level: budget/moderate/luxury or specific amount")
    interests: List[str] = Field(default_factory=list, description="User interests (e.g., adventure, culture, food)")
    travel_style: Optional[str] = Field(None, description="Travel style: relaxed, moderate, packed")
    duration: Optional[int] = Field(None, description="Trip duration in days")
    season: Optional[str] = Field(None, description="Preferred season or specific month")
    group_size: str = Field("solo", description="Solo, couple, family, group")
    special_requirements: Optional[str] = Field(None, description="Any special requirements or constraints")


class DestinationRecommendation(BaseModel):
    """A destination recommendation"""
    destination: str
    country: str
    reasoning: str
    best_time: str
    daily_budget: str
    top_activities: List[str]
    unique_feature: str


class ItineraryDay(BaseModel):
    """Single day in an itinerary"""
    day_number: int
    theme: str
    morning: str
    afternoon: str
    evening: str
    restaurants: List[str]
    estimated_cost: float
    tips: str


class Itinerary(BaseModel):
    """Complete trip itinerary"""
    destination: str
    duration: int
    days: List[ItineraryDay]
    total_estimated_cost: float
    general_tips: str


class BudgetItem(BaseModel):
    """Budget expense item"""
    category: str
    amount: float
    description: str


class BudgetAnalysis(BaseModel):
    """Budget optimization analysis"""
    total_budget: float
    expenses: List[BudgetItem]
    recommendations: str
    savings_opportunities: List[str]
    risk_assessment: str


class WeatherInfo(BaseModel):
    """Weather information"""
    temperature: float
    description: str
    humidity: int
    forecast: Optional[List[Dict[str, Any]]] = None


class TripPlan(BaseModel):
    """Complete trip plan"""
    destination: str
    duration: int
    preferences: TripPreferences
    itinerary: Optional[Itinerary] = None
    budget_analysis: Optional[BudgetAnalysis] = None
    weather_info: Optional[WeatherInfo] = None
    local_insights: Optional[str] = None
    created_at: str


class ChatMessage(BaseModel):
    """Chat message wrapper for agent communication"""
    message: str
    context: Optional[Dict[str, Any]] = None
    conversation_id: Optional[str] = None


class AgentRequest(BaseModel):
    """Request to a specialized agent"""
    request_type: str
    data: Dict[str, Any]
    sender: str


class AgentResponse(BaseModel):
    """Response from a specialized agent"""
    response_type: str
    data: Dict[str, Any]
    success: bool
    error: Optional[str] = None
