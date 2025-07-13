"""
Weather Agent using Mock A2A SDK
Provides weather information through A2A framework
"""

from src.a2a_sdk_mock import Agent, Tool, ToolCall
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class WeatherAgent(Agent):
    """Weather agent for providing weather information using A2A SDK"""
    
    def __init__(self):
        super().__init__(
            name="weather_agent",
            description="Provides weather information for cities",
            tools=[
                Tool(
                    name="get_weather",
                    description="Get current weather for a city",
                    parameters={
                        "type": "object",
                        "properties": {
                            "city": {"type": "string", "description": "City name"}
                        },
                        "required": ["city"]
                    }
                ),
                Tool(
                    name="get_forecast",
                    description="Get weather forecast for a city",
                    parameters={
                        "type": "object",
                        "properties": {
                            "city": {"type": "string", "description": "City name"}
                        },
                        "required": ["city"]
                    }
                )
            ]
        )
    
    async def get_weather(self, tool_call: ToolCall) -> str:
        """Get current weather for a city"""
        city = tool_call.parameters.get("city", "Unknown")
        result = f"Weather in {city}: 22°C, Partly Cloudy"
        logger.info(f"WeatherAgent.get_weather({city}) = {result}")
        return result
    
    async def get_forecast(self, tool_call: ToolCall) -> str:
        """Get weather forecast for a city"""
        city = tool_call.parameters.get("city", "Unknown")
        result = f"Forecast for {city}: Sunny tomorrow, Rain on Wednesday"
        logger.info(f"WeatherAgent.get_forecast({city}) = {result}")
        return result 