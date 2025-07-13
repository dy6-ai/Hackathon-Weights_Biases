"""
Mock A2A SDK Implementation
Follows Google A2A SDK pattern for demonstration purposes
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Tool:
    """Mock Tool class following A2A SDK pattern"""
    name: str
    description: str
    parameters: Dict[str, Any]

@dataclass
class ToolCall:
    """Mock ToolCall class following A2A SDK pattern"""
    name: str
    parameters: Dict[str, Any]

class Agent:
    """Mock Agent class following A2A SDK pattern"""
    
    def __init__(self, name: str, description: str, tools: List[Tool]):
        self.name = name
        self.description = description
        self.tools = tools
        logger.info(f"Mock A2A Agent '{name}' initialized with {len(tools)} tools")

class A2AServer:
    """Mock A2A Server class following A2A SDK pattern"""
    
    def __init__(self):
        self.agents = {}
        logger.info("Mock A2A Server initialized")
    
    def register_agent(self, agent: Agent):
        """Register an agent with the A2A server"""
        self.agents[agent.name] = agent
        logger.info(f"Registered mock A2A agent: {agent.name}")
    
    def get_agent(self, name: str) -> Optional[Agent]:
        """Get an agent by name"""
        return self.agents.get(name) 