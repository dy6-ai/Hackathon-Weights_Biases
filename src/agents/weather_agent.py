"""
Weather Agent for BlueGuard A2A Security System
Provides weather information
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class WeatherAgent:
    """Weather agent for providing weather information"""
    
    def __init__(self):
        self.name = "weather_agent"
        self.description = "Provides weather information for cities"
        self.tools = ["get_weather", "get_forecast"]
    
    async def get_weather(self, parameters: Dict[str, Any]) -> str:
        """Get current weather for a city"""
        city = parameters.get("city", "Unknown")
        result = f"Weather in {city}: 22°C, Partly Cloudy"
        logger.info(f"WeatherAgent.get_weather({city}) = {result}")
        return result
    
    async def get_forecast(self, parameters: Dict[str, Any]) -> str:
        """Get weather forecast for a city"""
        city = parameters.get("city", "Unknown")
        result = f"Forecast for {city}: Sunny tomorrow, Rain on Wednesday"
        logger.info(f"WeatherAgent.get_forecast({city}) = {result}")
        return result 