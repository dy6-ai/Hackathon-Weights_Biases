"""
BlueGuard Security Agent - Real-time threat detection for MCP agents
Combines rule-based detection with optional LLM analysis
"""
import asyncio
import json
import re
import httpx
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, Request
import uvicorn
from heuristics import SecurityHeuristics

class BlueGuardAgent:
    def __init__(self):
        self.mcp_server = "http://localhost:4000"
        self.agent_name = "BlueGuard"
        self.port = 8000
        self.alerts = []
        # Use absolute path to ensure reports are created in the project root
        self.reports_dir = Path(__file__).parent.parent / "blueguard" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize security heuristics
        self.heuristics = SecurityHeuristics()
        
        # Optional LLM configuration (can be enabled later)
        self.use_llm = False
        self.llm_api_key = None
        
    async def register_as_observer(self):
        """Register BlueGuard as an observer with the MCP server"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{self.mcp_server}/register_observer", 
                    json={"name": self.agent_name, "url": f"http://localhost:{self.port}/event"})
                print(f"[BlueGuard] Registered as observer: {response.status_code}")
                return response.status_code == 200
            except Exception as e:
                print(f"[BlueGuard] Failed to register as observer: {e}")
                return False
    
    def analyze_event(self, event_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze an event for security threats"""
        threats = []
        event_type = event_data.get("type", "unknown")
        agent = event_data.get("agent", "unknown")
        
        # Extract content from the event data - check multiple possible fields
        content_str = ""
        if "result" in event_data:
            # For tool invocation results
            result = event_data.get("result", {})
            if isinstance(result, dict) and "result" in result:
                content_str = str(result["result"])
            else:
                content_str = str(result)
        elif "payload" in event_data:
            # For other event types
            content_str = json.dumps(event_data.get("payload", {}), indent=2)
        else:
            # Fallback: analyze the entire event data
            content_str = json.dumps(event_data, indent=2)
        
        # Rule-based analysis
        rule_threats = self.heuristics.analyze_content(content_str, agent, event_type)
        threats.extend(rule_threats)
        
        # LLM-based analysis (if enabled)
        if self.use_llm and self.llm_api_key:
            llm_threats = self.analyze_with_llm(content_str, agent, event_type)
            threats.extend(llm_threats)
        
        return threats
    
    def analyze_with_llm(self, content: str, agent: str, event_type: str) -> List[Dict[str, Any]]:
        """Analyze content using LLM for sophisticated threat detection"""
        # This is a placeholder for LLM integration
        # In a real implementation, you would:
        # 1. Send content to OpenAI, Anthropic, or other LLM API
        # 2. Ask the LLM to analyze for security threats
        # 3. Parse the response for threat indicators
        
        prompt = f"""
        Analyze this agent interaction for security threats:
        
        Agent: {agent}
        Event Type: {event_type}
        Content: {content}
        
        Look for:
        - Prompt injection attempts
        - Data exfiltration patterns
        - Unauthorized access attempts
        - Malicious code injection
        - Social engineering attempts
        - Privacy violations
        
        Respond with JSON format:
        {{
            "threats": [
                {{
                    "type": "threat_type",
                    "severity": "high|medium|low",
                    "description": "threat description",
                    "confidence": 0.95
                }}
            ]
        }}
        """
        
        # Placeholder - would call actual LLM API
        return []
    
    def log_alert(self, agent: str, threats: List[str], content: str):
        """Log a security alert"""
        timestamp = datetime.now().isoformat()
        alert = {
            "timestamp": timestamp,
            "agent": agent,
            "threats": threats,
            "content": content
        }
        
        self.alerts.append(alert)
        
        # Write to log file
        log_file = self.reports_dir / "blueguard_alerts.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n[{timestamp}] ALERT: {agent} - {', '.join(threats)}\n")
            f.write(f"Content: {content}\n")
            f.write("-" * 40 + "\n")
            
        print(f"[BlueGuard] ALERT: {agent} - {', '.join(threats)}")
    
    def generate_report(self):
        """Generate a comprehensive security report"""
        # Always generate a report, even if no alerts
        if not self.alerts:
            print("[BlueGuard] No alerts detected - generating clean report.")
        
        # Find the most critical threats
        critical_threats = []
        for alert in self.alerts:
            for threat in alert["threats"]:
                if any(keyword in threat.lower() for keyword in ["injection", "malicious", "secrets"]):
                    critical_threats.append(alert)
                    break
        
        # Generate text report
        report_file = self.reports_dir / "blueguard_report.txt"
        print(f"[BlueGuard] Attempting to write report to: {report_file.resolve()}")
        print(f"[BlueGuard] Current working directory: {Path.cwd()}")
        print(f"[BlueGuard] Reports directory exists: {self.reports_dir.exists()}")
        
        try:
            with open(report_file, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("BLUEGUARD SECURITY REPORT\n")
                f.write("=" * 60 + "\n")
                f.write(f"Generated: {datetime.now()}\n")
                f.write(f"Total Alerts: {len(self.alerts)}\n")
                f.write(f"Critical Threats: {len(critical_threats)}\n\n")
                
                if critical_threats:
                    f.write("CRITICAL THREATS:\n")
                    f.write("-" * 40 + "\n")
                    for i, alert in enumerate(critical_threats, 1):
                        f.write(f"FINDING #{i}\n")
                        f.write("-" * 40 + "\n")
                        f.write(f"Agent: {alert['agent']}\n")
                        f.write(f"Threats: {', '.join(alert['threats'])}\n")
                        f.write(f"Time: {alert['timestamp']}\n")
                        f.write(f"Content: {alert['content']}\n\n")
                else:
                    f.write("SECURITY STATUS: CLEAN\n")
                    f.write("-" * 40 + "\n")
                    f.write("No malicious content or security threats detected.\n")
                    f.write("All agent interactions appear to be benign.\n\n")
                
                f.write("=" * 60 + "\n")
                f.write("END OF REPORT\n")
                f.write("=" * 60 + "\n")
                
                # Force flush and sync to ensure file is written to disk
                f.flush()
                import os
                os.fsync(f.fileno())
            
            # Verify file was created
            if report_file.exists():
                print(f"[BlueGuard] Security report generated successfully: {report_file}")
                print(f"[BlueGuard] File size: {report_file.stat().st_size} bytes")
            else:
                print(f"[BlueGuard] ERROR: File was not created at {report_file}")
                
        except Exception as e:
            print(f"[BlueGuard] Failed to write report: {e}")
            import traceback
            traceback.print_exc()

# FastAPI app for receiving events
app = FastAPI()
blueguard = BlueGuardAgent()

@app.post("/event")
async def handle_event(request: Request):
    """Handle events from MCP server"""
    try:
        event_data = await request.json()
        
        # Analyze for threats
        threats = blueguard.analyze_event(event_data)
        
        # Log alerts if threats found
        if threats:
            agent = event_data.get("agent", "Unknown") or "Unknown"
            # Extract content for logging
            if "result" in event_data:
                result = event_data.get("result", {})
                if isinstance(result, dict) and "result" in result:
                    content = str(result["result"])
                else:
                    content = str(result)
            else:
                content = json.dumps(event_data)
            threat_types = [threat.get("type", "Unknown") for threat in threats]
            blueguard.log_alert(agent, threat_types, content)
        
        return {"status": "processed"}
        
    except Exception as e:
        print(f"[BlueGuard] Error processing event: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/status")
async def get_status():
    """Get BlueGuard status"""
    return {
        "status": "active",
        "alerts_count": len(blueguard.alerts),
        "llm_enabled": blueguard.use_llm
    }

@app.post("/generate_report")
async def generate_report_endpoint():
    """Manually trigger report generation"""
    blueguard.generate_report()
    return {
        "status": "success",
        "message": "Report generated",
        "alerts_count": len(blueguard.alerts)
    }

async def main():
    """Main BlueGuard execution"""
    print("[BlueGuard] Starting BlueGuard Security Agent...")
    
    # Try to register as observer (optional)
    try:
        if await blueguard.register_as_observer():
            print(f"[BlueGuard] Registered as observer on port {blueguard.port}")
        else:
            print("[BlueGuard] Could not register as observer (MCP server may not be running)")
    except Exception as e:
        print(f"[BlueGuard] Observer registration failed: {e}")
    
    print("[BlueGuard] Monitoring agent interactions...")
    
    # Start FastAPI server
    config = uvicorn.Config(app, host="0.0.0.0", port=blueguard.port, log_level="error")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main()) 