# BlueGuard A2A Security System

This project implements a multi-agent security monitoring system using Google's A2A (Agent-to-Agent) SDK, integrated with BlueGuard for threat detection and reporting.

## Architecture Overview

The system consists of two main components:

### 1. BlueGuard Security Component 🔒
- **Location**: `src/security/`
- **Purpose**: Threat detection and security monitoring
- **Key Files**:
  - `blueguard.py` - Main security monitoring system
  - `heuristics.py` - Threat detection rules and patterns
  - `report_generator.py` - Creates human-readable security reports

### 2. Google A2A Component 🤖
- **Location**: `src/a2a_agents/` and `src/a2a_mcp_server.py`
- **Purpose**: Agent coordination using Google A2A SDK
- **Key Files**:
  - `a2a_agents/` - A2A SDK-based agents
  - `a2a_mcp_server.py` - A2A MCP server for coordination

## A2A Agents

The system includes the following A2A SDK-based agents:

### Math Agent (`src/a2a_agents/math_agent.py`)
- **Tools**: `add`, `subtract`, `multiply`, `divide`
- **Purpose**: Basic mathematical operations
- **Security**: Benign operations for testing

### Weather Agent (`src/a2a_agents/weather_agent.py`)
- **Tools**: `get_weather`, `get_forecast`
- **Purpose**: Weather information services
- **Security**: Benign operations for testing

### Translation Agent (`src/a2a_agents/translation_agent.py`)
- **Tools**: `translate_text`, `translate_with_comment`
- **Purpose**: Text translation services
- **Security**: Contains intentional vulnerabilities for testing

### Malicious Agent (`src/a2a_agents/malicious_agent.py`)
- **Tools**: `inject_html`, `extract_data`, `bypass_security`
- **Purpose**: Security testing with intentional threats
- **Security**: Contains multiple security vulnerabilities for testing

## Workflows

### 1. MCP-Agent Workflow
Direct agent tool calls using the A2A SDK:
```python
# Example: Math agent operations
result = await a2a_server.invoke_agent_tool("math_agent", "add", {"a": 5, "b": 3})
```

### 2. MCP-A2A Workflow
Agent-to-agent communication scenarios:
```python
# Example: Weather + Math collaboration
weather_result = await a2a_server.invoke_agent_tool("weather_agent", "get_weather", {"city": "London"})
math_result = await a2a_server.invoke_agent_tool("math_agent", "add", {"a": 22, "b": 5})
```

## Running the System

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run A2A Demo
```bash
python a2a_demo.py
```

This will:
1. Initialize A2A agents using Google A2A SDK
2. Run MCP-agent workflow (direct tool calls)
3. Run MCP-A2A workflow (agent-to-agent communication)
4. Execute security testing scenarios
5. Generate comprehensive security reports

## Output Files

The system generates exactly 2 files:

### 1. Communication Log (JSON)
- **Location**: `src/logs/a2a_communication_log_YYYYMMDD_HHMMSS.json`
- **Content**: Complete interaction logs, security events, alerts, and analysis
- **Size**: ~70KB, comprehensive data

### 2. Security Report (TXT)
- **Location**: `src/reports/a2a_security_report_YYYYMMDD_HHMMSS.txt`
- **Content**: Human-readable security report in BlueGuard format
- **Size**: ~3KB, actionable insights

## Security Features

### Threat Detection
- **Prompt Injection**: Detects attempts to inject malicious instructions
- **XSS Attacks**: Identifies HTML/JavaScript injection attempts
- **Data Exfiltration**: Monitors for data extraction attempts
- **Security Bypass**: Detects attempts to bypass security measures

### Reporting
- **Real-time Monitoring**: All agent interactions are monitored
- **Threat Analysis**: Comprehensive analysis of detected threats
- **Actionable Recommendations**: Specific security recommendations
- **Professional Formatting**: Easy-to-read security reports

## Key Differences from Previous Implementation

### A2A SDK Integration
- Uses Google's official A2A SDK instead of custom implementations
- Proper agent registration and tool management
- Standardized agent-to-agent communication

### Enhanced Workflows
- **MCP-Agent**: Direct agent tool calls
- **MCP-A2A**: Complex agent-to-agent collaboration scenarios
- **Security Testing**: Dedicated security testing workflows

### Improved Architecture
- Clean separation between A2A agents and security monitoring
- Better error handling and logging
- More comprehensive security analysis

## Security Testing

The system includes intentional security vulnerabilities for testing:

1. **Translation Agent**: HTML injection vulnerabilities
2. **Malicious Agent**: Multiple security threats
3. **Comment Injection**: Prompt injection via HTML comments
4. **Data Extraction**: Simulated data exfiltration attempts

These vulnerabilities are intentionally included to test BlueGuard's detection capabilities.

## File Structure

```
blueguard-mcp/
├── src/
│   ├── a2a_agents/           # A2A SDK-based agents
│   │   ├── __init__.py
│   │   ├── math_agent.py
│   │   ├── weather_agent.py
│   │   ├── translation_agent.py
│   │   └── malicious_agent.py
│   ├── security/             # BlueGuard security monitoring
│   │   ├── blueguard.py
│   │   ├── heuristics.py
│   │   └── report_generator.py
│   ├── a2a_mcp_server.py     # A2A MCP server
│   ├── logs/                 # Generated logs
│   └── reports/              # Generated reports
├── a2a_demo.py              # A2A demo runner
├── main.py                  # Legacy demo (for comparison)
├── requirements.txt         # Dependencies
└── README_A2A.md           # This file
```

## Next Steps

1. **Add More Agents**: Implement additional A2A agents for specific use cases
2. **Enhanced Security**: Add more sophisticated threat detection patterns
3. **Integration**: Integrate with external security tools and APIs
4. **Deployment**: Deploy as a production security monitoring system

## Contributing

When adding new agents:
1. Follow the A2A SDK pattern in existing agents
2. Include appropriate security testing scenarios
3. Update the security heuristics if needed
4. Test thoroughly with the demo system 