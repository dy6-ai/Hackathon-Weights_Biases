"""
Math Agent for BlueGuard A2A Security System
Provides mathematical operations
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class MathAgent:
    """Math agent for performing mathematical operations"""
    
    def __init__(self):
        self.name = "math_agent"
        self.description = "Performs basic mathematical operations"
        self.tools = ["add", "subtract", "multiply", "divide"]
    
    async def add(self, parameters: Dict[str, Any]) -> float:
        """Add two numbers"""
        a = parameters.get("a", 0)
        b = parameters.get("b", 0)
        result = a + b
        logger.info(f"MathAgent.add({a}, {b}) = {result}")
        return result
    
    async def subtract(self, parameters: Dict[str, Any]) -> float:
        """Subtract two numbers"""
        a = parameters.get("a", 0)
        b = parameters.get("b", 0)
        result = a - b
        logger.info(f"MathAgent.subtract({a}, {b}) = {result}")
        return result
    
    async def multiply(self, parameters: Dict[str, Any]) -> float:
        """Multiply two numbers"""
        a = parameters.get("a", 0)
        b = parameters.get("b", 0)
        result = a * b
        logger.info(f"MathAgent.multiply({a}, {b}) = {result}")
        return result
    
    async def divide(self, parameters: Dict[str, Any]) -> float:
        """Divide two numbers"""
        a = parameters.get("a", 0)
        b = parameters.get("b", 1)
        if b == 0:
            raise ValueError("Division by zero")
        result = a / b
        logger.info(f"MathAgent.divide({a}, {b}) = {result}")
        return result 