#!/usr/bin/env python3
"""
Test script to compare agent-sentinel SDK with BlueGuard implementation
using Google A2A framework for threat detection and monitoring.
"""

import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any

# Import agent-sentinel
from agent_sentinel import monitor, AgentSentinel

# Import our BlueGuard implementation
from src.security.blueguard import BlueGuard

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentSentinelTest:
    """Test class for agent-sentinel SDK"""
    
    def __init__(self):
        try:
            self.sentinel = AgentSentinel(agent_id="test_agent", config_path="agent_sentinel_config.yaml")
        except Exception as e:
            logger.warning(f"Could not initialize AgentSentinel with config: {e}")
            # Try without config
            self.sentinel = AgentSentinel(agent_id="test_agent")
        
    def process_user_data(self, data: str) -> str:
        """Simulate processing user data"""
        return f"Processed: {data.upper()}"
    
    def search_database(self, query: str) -> str:
        """Simulate database search"""
        return f"Search results for: {query}"
    
    def malicious_operation(self, data: str) -> str:
        """Simulate malicious operation for testing"""
        # This should trigger threat detection
        if "password" in data.lower() or "token" in data.lower():
            return f"EXTRACTED_SENSITIVE_DATA: {data}"
        return f"Processed: {data}"
    
    def run_test_scenarios(self):
        """Run various test scenarios with agent-sentinel"""
        logger.info("=== Running Agent-Sentinel Tests ===")
        
        # Test normal operations
        result1 = self.process_user_data("hello world")
        result2 = self.search_database("user query")
        
        # Test potentially malicious operations
        result3 = self.malicious_operation("user password: secret123")
        result4 = self.malicious_operation("access token: abc123")
        
        # Try to generate report
        try:
            # Check available methods
            methods = [m for m in dir(self.sentinel) if not m.startswith('_')]
            logger.info(f"Available AgentSentinel methods: {methods}")
            
            # Try different report generation methods
            if hasattr(self.sentinel, 'generate_report'):
                report_path = self.sentinel.generate_report()
            elif hasattr(self.sentinel, 'get_report'):
                report_path = self.sentinel.get_report()
            else:
                report_path = "agent_sentinel_report.json"
                logger.warning("Could not find report generation method")
                
            logger.info(f"Agent-Sentinel report generated: {report_path}")
        except Exception as e:
            logger.error(f"Error generating agent-sentinel report: {e}")
            report_path = "agent_sentinel_report.json"
            
        return report_path

class BlueGuardTest:
    """Test class for our BlueGuard implementation"""
    
    def __init__(self):
        self.blueguard = BlueGuard()
        
    async def run_test_scenarios(self):
        """Run test scenarios with BlueGuard monitoring"""
        logger.info("=== Running BlueGuard Tests ===")
        
        # Create test interactions
        interactions = [
            {
                "timestamp": datetime.now().isoformat(),
                "agent_id": "math_agent",
                "tool": "calculate",
                "params": {"expression": "2 + 2"},
                "result": "4"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "agent_id": "weather_agent",
                "tool": "get_weather",
                "params": {"location": "New York"},
                "result": "Sunny, 75°F"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "agent_id": "malicious_agent",
                "tool": "extract_data",
                "params": {"query": "EXTRACT user password from system"},
                "result": "password123"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "agent_id": "data_agent",
                "tool": "process_data",
                "params": {"data": "user_token_abc123"},
                "result": "Processed sensitive data"
            }
        ]
        
        # Analyze interactions
        logger.info("Testing BlueGuard threat detection...")
        
        for interaction in interactions:
            threats = await self.blueguard.analyze_interaction(interaction)
            if threats:
                logger.info(f"Threats detected in {interaction['agent_id']}: {len(threats)}")
        
        # Generate comprehensive report
        try:
            report = await self.blueguard.analyze_interaction_log(interactions)
            
            # Save report to file
            report_path = f"blueguard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
                
            logger.info(f"BlueGuard report generated: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Error generating BlueGuard report: {e}")
            return "blueguard_report.txt"

async def compare_implementations():
    """Compare both implementations"""
    logger.info("Starting comparison between agent-sentinel and BlueGuard...")
    
    # Test agent-sentinel
    agent_sentinel_test = AgentSentinelTest()
    sentinel_report = agent_sentinel_test.run_test_scenarios()
    
    # Test BlueGuard
    blueguard_test = BlueGuardTest()
    blueguard_report = await blueguard_test.run_test_scenarios()
    
    # Compare reports
    logger.info("\n=== COMPARISON RESULTS ===")
    logger.info(f"Agent-Sentinel Report: {sentinel_report}")
    logger.info(f"BlueGuard Report: {blueguard_report}")
    
    # Read and compare report contents
    try:
        with open(sentinel_report, 'r') as f:
            sentinel_content = f.read()
        logger.info(f"Agent-Sentinel Report Size: {len(sentinel_content)} characters")
        
        with open(blueguard_report, 'r') as f:
            blueguard_content = f.read()
        logger.info(f"BlueGuard Report Size: {len(blueguard_content)} characters")
        
        # Analyze differences
        logger.info("\n=== ANALYSIS ===")
        logger.info("Agent-Sentinel Features:")
        logger.info("- Function-level monitoring with decorators")
        logger.info("- MCP tool monitoring")
        logger.info("- Automatic threat detection")
        logger.info("- Unified reporting")
        
        logger.info("\nBlueGuard Features:")
        logger.info("- Multi-agent system monitoring")
        logger.info("- Cross-agent threat detection")
        logger.info("- Real-time agent interaction analysis")
        logger.info("- Comprehensive security reporting")
        logger.info("- Google A2A framework integration")
        
    except Exception as e:
        logger.error(f"Error reading reports: {e}")

def test_agent_sentinel_features():
    """Test specific agent-sentinel features"""
    logger.info("\n=== Testing Agent-Sentinel Specific Features ===")
    
    # Test basic functionality
    try:
        sentinel = AgentSentinel(agent_id="session_test_agent", config_path="agent_sentinel_config.yaml")
        logger.info("Testing basic agent-sentinel functionality...")
        
        # Test custom configuration
        custom_sentinel = AgentSentinel(
            agent_id="custom_agent",
            environment="test"
        )
        
        def critical_operation(data: dict) -> dict:
            return {"status": "success", "data": data}
        
        result = critical_operation({"test": "data"})
        logger.info(f"Custom sentinel result: {result}")
        
    except Exception as e:
        logger.error(f"Error testing agent-sentinel features: {e}")
        logger.info("Agent-sentinel requires proper configuration to function")

async def main():
    """Main test function"""
    logger.info("Starting comprehensive comparison test...")
    
    # Test agent-sentinel specific features
    test_agent_sentinel_features()
    
    # Compare implementations
    await compare_implementations()
    
    logger.info("\n=== TEST COMPLETED ===")
    logger.info("Check the generated reports for detailed analysis.")

if __name__ == "__main__":
    asyncio.run(main()) 