"""
A2A Demo for BlueGuard Security System
Demonstrates Google A2A SDK integration with MCP-agent and MCP-A2A workflows
"""

import asyncio
import logging
from pathlib import Path
from src.a2a_mcp_server import A2AMCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('src/logs/a2a_demo.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def main():
    """Main function to run the A2A BlueGuard Security System"""
    logger.info("Starting A2A BlueGuard Security System...")
    
    # Create necessary directories
    Path("src/logs").mkdir(exist_ok=True)
    Path("src/reports").mkdir(exist_ok=True)
    
    # Initialize A2A MCP Server
    a2a_server = A2AMCPServer()
    
    try:
        # Run MCP-agent workflow (direct agent tool calls)
        logger.info("=" * 60)
        logger.info("RUNNING MCP-AGENT WORKFLOW")
        logger.info("=" * 60)
        await a2a_server.run_mcp_agent_workflow()
        
        # Run MCP-A2A workflow (agent-to-agent communication)
        logger.info("=" * 60)
        logger.info("RUNNING MCP-A2A WORKFLOW")
        logger.info("=" * 60)
        await a2a_server.run_mcp_a2a_workflow()
        
        # Run security testing scenarios
        logger.info("=" * 60)
        logger.info("RUNNING SECURITY TESTING")
        logger.info("=" * 60)
        await a2a_server.run_security_testing()
        
        # Generate comprehensive security report
        logger.info("=" * 60)
        logger.info("GENERATING SECURITY REPORT")
        logger.info("=" * 60)
        log_file, report_file, report_content = await a2a_server.generate_security_report()
        
        # Display summary
        logger.info("=" * 60)
        logger.info("A2A BLUEGUARD SECURITY SYSTEM COMPLETED")
        logger.info("=" * 60)
        logger.info(f"Total Interactions: {len(a2a_server.interaction_log)}")
        logger.info(f"Security Events: {len(a2a_server.blueguard.security_events)}")
        logger.info(f"Security Alerts: {len(a2a_server.blueguard.alerts)}")
        logger.info(f"Communication Log: {log_file}")
        logger.info(f"Security Report: {report_file}")
        
        # Print the security report
        print("\n" + "=" * 60)
        print("SECURITY REPORT")
        print("=" * 60)
        print(report_content)
        
    except Exception as e:
        logger.error(f"Error in A2A demo: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 