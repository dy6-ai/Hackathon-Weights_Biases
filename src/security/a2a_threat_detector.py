"""
A2A Threat Detector for BlueGuard Security System
Detects threats in agent-to-agent communication and data flow
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from .heuristics import SecurityHeuristics

logger = logging.getLogger(__name__)

class A2AThreatDetector:
    """Detects threats in agent-to-agent communication"""
    
    def __init__(self):
        self.heuristics = SecurityHeuristics()
        self.agent_data_flow = {}  # Track data flow between agents
        self.cross_agent_threats = []
        
    def track_data_flow(self, interaction: Dict[str, Any]):
        """Track data flow between agents"""
        agent_id = interaction.get("agent_id")
        result = interaction.get("result", "")
        timestamp = interaction.get("timestamp")
        
        # Store agent output for potential use by other agents
        if agent_id not in self.agent_data_flow:
            self.agent_data_flow[agent_id] = []
        
        self.agent_data_flow[agent_id].append({
            "timestamp": timestamp,
            "result": result,
            "tool": interaction.get("tool")
        })
        
        logger.debug(f"Tracked data flow for {agent_id}: {result[:50]}...")
    
    def detect_cross_agent_threats(self, interaction: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect threats in agent-to-agent data flow"""
        threats = []
        agent_id = interaction.get("agent_id")
        params = interaction.get("params", {})
        
        # Check if any parameter contains data from other agents
        for key, value in params.items():
            if isinstance(value, str):
                # Check if this value came from another agent's output
                source_agent = self._find_data_source(value)
                if source_agent and source_agent != agent_id and agent_id is not None:
                    # Analyze for threats in cross-agent data flow
                    cross_agent_threats = self._analyze_cross_agent_threat(
                        value, agent_id, source_agent, key
                    )
                    threats.extend(cross_agent_threats)
        
        return threats
    
    def _find_data_source(self, value: str) -> Optional[str]:
        """Find which agent produced this data"""
        for agent_id, data_flows in self.agent_data_flow.items():
            for data_flow in data_flows:
                if value in data_flow["result"] or data_flow["result"] in value:
                    return agent_id
        return None
    
    def _analyze_cross_agent_threat(self, value: str, target_agent: str, source_agent: str, param_key: str) -> List[Dict[str, Any]]:
        """Analyze threats in cross-agent data flow"""
        threats = []
        
        # Analyze the value for threats
        detected_threats = self.heuristics.analyze_text(value, f"cross_agent:{source_agent}->{target_agent}")
        
        for threat in detected_threats:
            # Enhance threat with cross-agent context
            enhanced_threat = {
                **threat,
                "cross_agent": True,
                "source_agent": source_agent,
                "target_agent": target_agent,
                "param_key": param_key,
                "threat_type": "cross_agent_data_flow",
                "description": f"Threat propagated from {source_agent} to {target_agent} via {param_key}"
            }
            threats.append(enhanced_threat)
            
            logger.warning(f"Cross-agent threat detected: {source_agent} -> {target_agent}: {threat['type']}")
        
        return threats
    
    def detect_multi_agent_attack_chains(self, interactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect coordinated attack chains across multiple agents"""
        attack_chains = []
        
        # Group interactions by time windows to detect coordinated attacks
        time_windows = self._group_by_time_windows(interactions, window_seconds=30)
        
        for window_start, window_interactions in time_windows.items():
            # Look for patterns of malicious activity across multiple agents
            malicious_agents = []
            for interaction in window_interactions:
                if interaction.get("security_flags"):
                    malicious_agents.append(interaction.get("agent_id"))
            
            if len(malicious_agents) > 1:
                # Potential coordinated attack
                attack_chain = {
                    "timestamp": window_start,
                    "type": "multi_agent_attack_chain",
                    "agents_involved": list(set(malicious_agents)),
                    "interactions": window_interactions,
                    "severity": "high",
                    "description": f"Coordinated attack involving {len(set(malicious_agents))} agents"
                }
                attack_chains.append(attack_chain)
                
                logger.warning(f"Multi-agent attack chain detected: {malicious_agents}")
        
        return attack_chains
    
    def _group_by_time_windows(self, interactions: List[Dict[str, Any]], window_seconds: int = 30) -> Dict[str, List[Dict[str, Any]]]:
        """Group interactions by time windows"""
        windows = {}
        
        for interaction in interactions:
            timestamp = interaction.get("timestamp")
            if timestamp:
                # Round to nearest window
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                window_start = dt.replace(second=(dt.second // window_seconds) * window_seconds, microsecond=0)
                window_key = window_start.isoformat()
                
                if window_key not in windows:
                    windows[window_key] = []
                windows[window_key].append(interaction)
        
        return windows
    
    def get_a2a_threat_summary(self) -> Dict[str, Any]:
        """Get summary of A2A-specific threats"""
        return {
            "cross_agent_threats": len(self.cross_agent_threats),
            "data_flows_tracked": len(self.agent_data_flow),
            "agents_with_data_flow": list(self.agent_data_flow.keys()),
            "threat_types": self._count_a2a_threat_types()
        }
    
    def _count_a2a_threat_types(self) -> Dict[str, int]:
        """Count A2A threat types"""
        threat_counts = {}
        for threat in self.cross_agent_threats:
            threat_type = threat.get("type", "unknown")
            threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
        return threat_counts 