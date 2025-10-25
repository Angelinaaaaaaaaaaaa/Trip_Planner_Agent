"""
Weather Service Integration
Provides real-time weather data and forecasts for destinations
"""

import os
import aiohttp
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class WeatherService:
    """
    Integration with weather APIs to provide destination weather information
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"

    async def get_current_weather(self, city: str) -> Dict[str, Any]:
        """
        Get current weather for a destination

        Args:
            city: City name

        Returns:
            Weather data dictionary
        """
        if not self.api_key:
            return self._get_mock_weather(city)

        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/weather"
                params = {
                    "q": city,
                    "appid": self.api_key,
                    "units": "metric"
                }

                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_weather_data(data)
                    else:
                        return self._get_mock_weather(city)
        except Exception as e:
            print(f"Weather API error: {e}")
            return self._get_mock_weather(city)

    async def get_forecast(self, city: str, days: int = 7) -> Dict[str, Any]:
        """
        Get weather forecast for upcoming days

        Args:
            city: City name
            days: Number of days to forecast

        Returns:
            Forecast data dictionary
        """
        if not self.api_key:
            return self._get_mock_forecast(city, days)

        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/forecast"
                params = {
                    "q": city,
                    "appid": self.api_key,
                    "units": "metric",
                    "cnt": days * 8  # 3-hour intervals
                }

                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_forecast_data(data, days)
                    else:
                        return self._get_mock_forecast(city, days)
        except Exception as e:
            print(f"Weather forecast error: {e}")
            return self._get_mock_forecast(city, days)

    def _format_weather_data(self, data: Dict) -> Dict[str, Any]:
        """Format weather API response"""
        return {
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "city": data["name"],
            "country": data["sys"]["country"]
        }

    def _format_forecast_data(self, data: Dict, days: int) -> Dict[str, Any]:
        """Format forecast API response"""
        daily_forecast = []

        for i in range(min(days, len(data["list"]) // 8)):
            day_data = data["list"][i * 8]
            daily_forecast.append({
                "date": day_data["dt_txt"].split()[0],
                "temperature": day_data["main"]["temp"],
                "description": day_data["weather"][0]["description"],
                "humidity": day_data["main"]["humidity"],
                "wind_speed": day_data["wind"]["speed"]
            })

        return {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "forecast": daily_forecast
        }

    def _get_mock_weather(self, city: str) -> Dict[str, Any]:
        """Provide mock weather data when API is unavailable"""
        return {
            "temperature": 22,
            "feels_like": 21,
            "humidity": 65,
            "description": "partly cloudy",
            "wind_speed": 5.2,
            "city": city,
            "country": "XX",
            "note": "Mock data - API key not configured"
        }

    def _get_mock_forecast(self, city: str, days: int) -> Dict[str, Any]:
        """Provide mock forecast data when API is unavailable"""
        today = datetime.now()
        forecast = []

        for i in range(days):
            date = today + timedelta(days=i)
            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "temperature": 20 + (i % 5),
                "description": ["sunny", "cloudy", "partly cloudy"][i % 3],
                "humidity": 60 + (i % 20),
                "wind_speed": 4.0 + (i % 3)
            })

        return {
            "city": city,
            "country": "XX",
            "forecast": forecast,
            "note": "Mock data - API key not configured"
        }


# Singleton instance
_weather_service: Optional[WeatherService] = None


def get_weather_service() -> WeatherService:
    """Get or create singleton WeatherService instance"""
    global _weather_service
    if _weather_service is None:
        _weather_service = WeatherService()
    return _weather_service
