"""
Agent definitions for BlueGuard A2A Security System
"""

from .math_agent import MathAgent
from .weather_agent import WeatherAgent
from .translation_agent import TranslationAgent
from .malicious_agent import MaliciousAgent
from .data_agent import DataAgent

__all__ = [
    "MathAgent",
    "WeatherAgent", 
    "TranslationAgent",
    "MaliciousAgent",
    "DataAgent"
] 