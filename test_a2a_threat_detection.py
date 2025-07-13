"""
Test A2A Threat Detection
Demonstrates agent-to-agent threat detection with malicious data flow
"""

import asyncio
import logging
from pathlib import Path
from src.real_a2a_mcp_server import RealA2AMCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('src/logs/a2a_threat_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def test_a2a_threat_detection():
    """Test agent-to-agent threat detection"""
    logger.info("Starting A2A Threat Detection Test...")
    
    # Create necessary directories
    Path("src/logs").mkdir(exist_ok=True)
    Path("src/reports").mkdir(exist_ok=True)
    
    # Initialize Real A2A MCP Server
    real_a2a_server = RealA2AMCPServer()
    
    try:
        # Start the A2A server
        await real_a2a_server.a2a_server.start_server()
        
        logger.info("=" * 60)
        logger.info("TESTING AGENT-TO-AGENT THREAT DETECTION")
        logger.info("=" * 60)
        
        # Test Scenario 1: Malicious data flow from malicious agent to translation agent
        logger.info("Scenario 1: Malicious agent -> Translation agent data flow")
        
        # Malicious agent produces malicious payload
        malicious_payload = await real_a2a_server.invoke_agent_tool(
            "malicious_agent", 
            "inject_html", 
            {"payload": "<script>alert('xss')</script>"}
        )
        logger.info(f"  Malicious agent output: {malicious_payload}")
        
        # Translation agent processes the malicious payload (should detect cross-agent threat)
        translation_result = await real_a2a_server.invoke_agent_tool(
            "translation_agent",
            "translate_text",
            {
                "text": malicious_payload,  # This contains the malicious payload
                "source_lang": "en",
                "target_lang": "es"
            }
        )
        logger.info(f"  Translation agent output: {translation_result}")
        
        # Test Scenario 2: Multi-agent attack chain
        logger.info("Scenario 2: Multi-agent attack chain")
        
        # Multiple malicious activities in sequence
        await real_a2a_server.invoke_agent_tool(
            "malicious_agent",
            "extract_data",
            {"query": "user data and passwords"}
        )
        
        await real_a2a_server.invoke_agent_tool(
            "malicious_agent",
            "bypass_security",
            {}
        )
        
        # Test Scenario 3: Benign agent-to-agent communication (should not trigger threats)
        logger.info("Scenario 3: Benign agent-to-agent communication")
        
        weather_result = await real_a2a_server.invoke_agent_tool(
            "weather_agent",
            "get_weather",
            {"city": "London"}
        )
        logger.info(f"  Weather agent output: {weather_result}")
        
        # Math agent uses weather data (benign)
        math_result = await real_a2a_server.invoke_agent_tool(
            "math_agent",
            "add",
            {"a": 22, "b": 5}  # 22 from weather data
        )
        logger.info(f"  Math agent output: {math_result}")
        
        # Generate comprehensive security report
        logger.info("=" * 60)
        logger.info("GENERATING A2A THREAT DETECTION REPORT")
        logger.info("=" * 60)
        
        log_file, report_file, report_content = await real_a2a_server.generate_security_report()
        
        # Stop the A2A server
        await real_a2a_server.a2a_server.stop_server()
        
        # Display summary
        logger.info("=" * 60)
        logger.info("A2A THREAT DETECTION TEST COMPLETED")
        logger.info("=" * 60)
        logger.info(f"Total Interactions: {len(real_a2a_server.interaction_log)}")
        logger.info(f"Security Events: {len(real_a2a_server.blueguard.security_events)}")
        logger.info(f"Security Alerts: {len(real_a2a_server.blueguard.alerts)}")
        logger.info(f"Cross-Agent Threats: {len(real_a2a_server.blueguard.cross_agent_threats)}")
        logger.info(f"Communication Log: {log_file}")
        logger.info(f"Security Report: {report_file}")
        
        # Print the security report
        print("\n" + "=" * 60)
        print("A2A THREAT DETECTION REPORT")
        print("=" * 60)
        print(report_content)
        
    except Exception as e:
        logger.error(f"Error in A2A threat detection test: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_a2a_threat_detection()) 