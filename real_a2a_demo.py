"""
Real A2A Demo for BlueGuard Security System
Demonstrates Real A2A SDK integration with MCP-agent and MCP-A2A workflows
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
        logging.FileHandler('src/logs/real_a2a_demo.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def main():
    """Main function to run the Real A2A BlueGuard Security System"""
    logger.info("Starting Real A2A BlueGuard Security System...")
    
    # Create necessary directories
    Path("src/logs").mkdir(exist_ok=True)
    Path("src/reports").mkdir(exist_ok=True)
    
    # Initialize Real A2A MCP Server
    real_a2a_server = RealA2AMCPServer()
    
    try:
        # Start the A2A server
        await real_a2a_server.a2a_server.start_server()
        
        # Run MCP-agent workflow (direct agent tool calls)
        logger.info("=" * 60)
        logger.info("RUNNING REAL A2A MCP-AGENT WORKFLOW")
        logger.info("=" * 60)
        await real_a2a_server.run_mcp_agent_workflow()
        
        # Run MCP-A2A workflow (agent-to-agent communication)
        logger.info("=" * 60)
        logger.info("RUNNING REAL A2A MCP-A2A WORKFLOW")
        logger.info("=" * 60)
        await real_a2a_server.run_mcp_a2a_workflow()
        
        # Run security testing scenarios
        logger.info("=" * 60)
        logger.info("RUNNING REAL A2A SECURITY TESTING")
        logger.info("=" * 60)
        await real_a2a_server.run_security_testing()
        
        # Generate comprehensive security report
        logger.info("=" * 60)
        logger.info("GENERATING REAL A2A SECURITY REPORT")
        logger.info("=" * 60)
        log_file, report_file, report_content = await real_a2a_server.generate_security_report()
        
        # Stop the A2A server
        await real_a2a_server.a2a_server.stop_server()
        
        # Display summary
        logger.info("=" * 60)
        logger.info("REAL A2A BLUEGUARD SECURITY SYSTEM COMPLETED")
        logger.info("=" * 60)
        logger.info(f"Total Interactions: {len(real_a2a_server.interaction_log)}")
        logger.info(f"Security Events: {len(real_a2a_server.blueguard.security_events)}")
        logger.info(f"Security Alerts: {len(real_a2a_server.blueguard.alerts)}")
        logger.info(f"Communication Log: {log_file}")
        logger.info(f"Security Report: {report_file}")
        
        # Print the security report
        print("\n" + "=" * 60)
        print("REAL A2A SECURITY REPORT")
        print("=" * 60)
        print(report_content)
        
    except Exception as e:
        logger.error(f"Error in Real A2A demo: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 