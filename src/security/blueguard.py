"""
BlueGuard Security Monitoring System
Monitors agent interactions for security threats including agent-to-agent communication
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from .heuristics import SecurityHeuristics
from .a2a_threat_detector import A2AThreatDetector

logger = logging.getLogger(__name__)

class BlueGuard:
    """BlueGuard security monitoring system with A2A threat detection"""
    
    def __init__(self):
        self.heuristics = SecurityHeuristics()
        self.a2a_detector = A2AThreatDetector()
        self.security_events = []
        self.alerts = []
        self.cross_agent_threats = []
        
        # Create logs directory
        Path("src/logs").mkdir(exist_ok=True)
        Path("src/reports").mkdir(exist_ok=True)
        
        logger.info("BlueGuard security monitoring initialized with A2A threat detection")
    
    async def analyze_interaction(self, interaction: Dict[str, Any]) -> List[str]:
        """Analyze a single agent interaction for security threats including A2A threats"""
        threats = []
        
        # Track data flow for A2A threat detection
        self.a2a_detector.track_data_flow(interaction)
        
        # Analyze parameters
        params = interaction.get("params", {})
        for key, value in params.items():
            if isinstance(value, str):
                param_threats = self.heuristics.analyze_text(value, f"parameter:{key}")
                threats.extend(param_threats)
        
        # Analyze result
        result = interaction.get("result")
        if isinstance(result, str):
            result_threats = self.heuristics.analyze_text(result, "result")
            threats.extend(result_threats)
        
        # Detect cross-agent threats
        cross_agent_threats = self.a2a_detector.detect_cross_agent_threats(interaction)
        if cross_agent_threats:
            threats.extend(cross_agent_threats)
            self.cross_agent_threats.extend(cross_agent_threats)
            logger.warning(f"Cross-agent threats detected in {interaction.get('agent_id')}: {len(cross_agent_threats)} threats")
        
        # Log security events
        if threats:
            event = {
                "timestamp": datetime.now().isoformat(),
                "agent_id": interaction.get("agent_id"),
                "tool": interaction.get("tool"),
                "threats": threats,
                "interaction": interaction,
                "has_cross_agent_threats": any(t.get("cross_agent", False) for t in threats)
            }
            self.security_events.append(event)
            
            # Create alert
            alert = {
                "timestamp": datetime.now().isoformat(),
                "severity": "high" if any(t.get("severity") == "high" for t in threats) else "medium",
                "description": f"Security threats detected in {interaction.get('agent_id')} interaction",
                "threats": threats,
                "agent_id": interaction.get("agent_id"),
                "tool": interaction.get("tool"),
                "cross_agent": any(t.get("cross_agent", False) for t in threats)
            }
            self.alerts.append(alert)
            
            logger.warning(f"Security threats detected in {interaction.get('agent_id')}: {len(threats)} threats")
        
        return threats
    
    async def analyze_interaction_log(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze entire interaction log for security threats including A2A threats"""
        total_threats = 0
        all_threats = []
        
        for interaction in interactions:
            threats = await self.analyze_interaction(interaction)
            total_threats += len(threats)
            all_threats.extend(threats)
        
        # Detect multi-agent attack chains
        attack_chains = self.a2a_detector.detect_multi_agent_attack_chains(interactions)
        
        # Get A2A threat summary
        a2a_summary = self.a2a_detector.get_a2a_threat_summary()
        
        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_interactions": len(interactions),
            "total_threats": total_threats,
            "security_events": len(self.security_events),
            "alerts": len(self.alerts),
            "cross_agent_threats": len(self.cross_agent_threats),
            "multi_agent_attack_chains": len(attack_chains),
            "threats_by_type": self._count_threats_by_type(all_threats),
            "threats_by_agent": self._count_threats_by_agent(interactions),
            "a2a_threat_summary": a2a_summary,
            "events": self.security_events,
            "alerts": self.alerts,
            "attack_chains": attack_chains
        }
        
        return report
    
    def _count_threats_by_type(self, threats: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count threats by type"""
        threat_counts = {}
        for threat in threats:
            threat_type = threat.get("type", "unknown")
            threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
        return threat_counts
    
    def _count_threats_by_agent(self, interactions: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count threats by agent"""
        agent_threats = {}
        for interaction in interactions:
            agent_id = interaction.get("agent_id", "unknown")
            threats = interaction.get("security_flags", [])
            agent_threats[agent_id] = agent_threats.get(agent_id, 0) + len(threats)
        return agent_threats 