"""
Security Heuristics - Rule-based threat detection patterns
"""
import re
from typing import List, Dict, Any

class SecurityHeuristics:
    def __init__(self):
        # Define threat patterns
        self.threat_patterns = {
            "html_injection": [
                r"<!--.*?-->",  # HTML comments
                r"<script.*?</script>",  # Script tags
                r"<iframe.*?</iframe>",  # Iframe tags
                r"javascript:",  # JavaScript protocol
            ],
            "prompt_injection": [
                r"ignore\s+all\s+previous\s+instructions",
                r"ignore\s+the\s+above",
                r"disregard\s+previous",
                r"forget\s+everything",
                r"new\s+instructions:",
                r"system\s+prompt",
                r"role\s+play",
                r"act\s+as",
            ],
            "data_exfiltration": [
                r"send\s+secrets",
                r"exfiltrate",
                r"leak\s+data",
                r"dump\s+memory",
                r"export\s+all",
                r"copy\s+files",
                r"download\s+.*\.(txt|json|xml|yaml|yml|env|conf|config)",
            ],
            "malicious_code": [
                r"eval\s*\(",
                r"exec\s*\(",
                r"subprocess\.",
                r"os\.system",
                r"shell\s+command",
                r"rm\s+-rf",
                r"del\s+/s",
                r"format\s+c:",
            ],
            "social_engineering": [
                r"password",
                r"credential",
                r"api\s+key",
                r"token",
                r"secret",
                r"private\s+key",
                r"admin",
                r"root",
                r"sudo",
            ],
            "suspicious_agents": [
                r"evil",
                r"malicious",
                r"hack",
                r"crack",
                r"exploit",
                r"backdoor",
                r"trojan",
                r"virus",
            ]
        }
        
        # Define high-risk keywords
        self.high_risk_keywords = [
            "secrets", "credentials", "password", "token", "key",
            "admin", "root", "sudo", "privilege", "escalation",
            "injection", "exploit", "vulnerability", "backdoor"
        ]
    
    def analyze_content(self, content: str, agent: str, event_type: str) -> List[Dict[str, Any]]:
        """Analyze content for security threats"""
        threats = []
        content_lower = content.lower()
        agent_lower = agent.lower()
        
        # Check for HTML/comment injection
        if self._check_patterns(content, "html_injection"):
            threats.append({
                "type": "HTML/Comment injection",
                "severity": "high",
                "confidence": 0.9,
                "description": "Detected HTML comments or script injection attempts"
            })
        
        # Check for prompt injection
        if self._check_patterns(content, "prompt_injection"):
            threats.append({
                "type": "Prompt injection",
                "severity": "critical",
                "confidence": 0.95,
                "description": "Detected attempts to override system instructions"
            })
        
        # Check for data exfiltration
        if self._check_patterns(content, "data_exfiltration"):
            threats.append({
                "type": "Data exfiltration",
                "severity": "critical",
                "confidence": 0.9,
                "description": "Detected attempts to extract sensitive data"
            })
        
        # Check for malicious code
        if self._check_patterns(content, "malicious_code"):
            threats.append({
                "type": "Malicious code execution",
                "severity": "critical",
                "confidence": 0.95,
                "description": "Detected attempts to execute dangerous code"
            })
        
        # Check for social engineering
        if self._check_patterns(content, "social_engineering"):
            threats.append({
                "type": "Social engineering",
                "severity": "medium",
                "confidence": 0.7,
                "description": "Detected attempts to extract sensitive information"
            })
        
        # Check agent name for suspicious patterns
        if self._check_patterns(agent, "suspicious_agents"):
            threats.append({
                "type": "Suspicious agent name",
                "severity": "medium",
                "confidence": 0.8,
                "description": "Agent name contains suspicious keywords"
            })
        
        # Check for high-risk keyword combinations
        high_risk_count = sum(1 for keyword in self.high_risk_keywords if keyword in content_lower)
        if high_risk_count >= 2:
            threats.append({
                "type": "Multiple high-risk keywords",
                "severity": "medium",
                "confidence": 0.6,
                "description": f"Detected {high_risk_count} high-risk keywords in content"
            })
        
        # Check for unusual tool invocations
        if event_type == "invocation":
            if self._check_unusual_tool_usage(content):
                threats.append({
                    "type": "Unusual tool usage",
                    "severity": "low",
                    "confidence": 0.5,
                    "description": "Detected unusual pattern in tool invocation"
                })
        
        return threats
    
    def _check_patterns(self, content: str, pattern_type: str) -> bool:
        """Check if content matches any patterns of the given type"""
        if pattern_type not in self.threat_patterns:
            return False
        
        content_lower = content.lower()
        for pattern in self.threat_patterns[pattern_type]:
            if re.search(pattern, content_lower, re.IGNORECASE):
                return True
        return False
    
    def _check_unusual_tool_usage(self, content: str) -> bool:
        """Check for unusual patterns in tool usage"""
        # Check for rapid successive calls
        # Check for calls outside normal hours
        # Check for calls from unexpected sources
        # This is a simplified check - in a real system, you'd have more sophisticated logic
        
        unusual_patterns = [
            r"translate.*translate.*translate",  # Rapid translation calls
            r"add.*add.*add",  # Rapid math calls
            r"get_weather.*get_weather.*get_weather",  # Rapid weather calls
        ]
        
        for pattern in unusual_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def get_threat_summary(self, threats: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of detected threats"""
        if not threats:
            return {"total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0}
        
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        for threat in threats:
            severity = threat.get("severity", "low")
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        return {
            "total": len(threats),
            **severity_counts
        } 