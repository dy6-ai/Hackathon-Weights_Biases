# BlueGuard A2A Security System

A comprehensive multi-agent system with Model Context Protocol (MCP) integration and advanced security monitoring using Google AI SDK.

## 🏗️ Architecture

The system follows the Google A2A (Agent-to-Agent) architecture pattern with the following components:

```
MCP Server
├── Agent 1 (Math Agent) → Output
├── Agent 2 (Weather Agent) → Output  
├── Agent 3 (Translation Agent) → Output
├── Agent 4 (Malicious Agent) → Output (Security Testing)
└── Agent 5 (Data Agent) → Output
```

### Security Monitoring Flow
```
Agent Interactions → MCP Server → BlueGuard Analysis → Security Reports
```

## 🚀 Features

### Multi-Agent System
- **Math Agent**: Basic mathematical operations (add, subtract, multiply, divide)
- **Weather Agent**: Weather information and forecasts
- **Translation Agent**: Text translation with security vulnerabilities for testing
- **Malicious Agent**: Intentional security vulnerabilities for testing
- **Data Agent**: Data processing and analysis

### Security Monitoring
- **Real-time threat detection** during agent interactions
- **Pattern-based security heuristics** for multiple threat types
- **Comprehensive logging** of all interactions and security events
- **Automated security reports** with actionable recommendations

### Threat Detection
- **HTML Injection**: Detects malicious HTML tags and scripts
- **Prompt Injection**: Identifies instruction manipulation attempts
- **Data Exfiltration**: Monitors for data extraction patterns
- **Command Injection**: Detects command execution attempts
- **SQL Injection**: Identifies database attack patterns
- **XSS**: Cross-site scripting detection

## 📁 Project Structure

```
blueguard-mcp/
├── src/
│   ├── __init__.py
│   ├── mcp_server.py          # MCP server with agent coordination
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── math_agent.py      # Mathematical operations
│   │   ├── weather_agent.py   # Weather information
│   │   ├── translation_agent.py # Text translation
│   │   ├── malicious_agent.py # Security testing agent
│   │   └── data_agent.py      # Data processing
│   └── security/
│       ├── __init__.py
│       ├── blueguard.py       # Security monitoring system
│       ├── heuristics.py      # Threat detection patterns
│       └── report_generator.py # Security report generation
├── logs/                      # Interaction and security logs
├── reports/                   # Security reports
├── main.py                    # Main orchestration script
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd blueguard-mcp
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google AI API key** (optional):
   ```bash
   export GOOGLE_AI_API_KEY="your-api-key-here"
   ```

## 🚀 Usage

### Run the Complete System
```bash
python main.py
```

This will:
1. Start the MCP server
2. Register all agents
3. Run benign agent interactions
4. Run malicious interactions (for security testing)
5. Execute agent-to-agent communication scenarios
6. Generate comprehensive security reports

### Expected Output
```
Starting BlueGuard A2A Security System...
Registered 5 agents
Starting benign agent interactions...
MathAgent.add({'a': 5, 'b': 3}) = 8
WeatherAgent.get_weather({'city': 'London'}) = Weather in London: 22°C, Partly Cloudy
...
Starting malicious agent interactions...
Security threats detected in translation_agent: 3 threats
...
=== BlueGuard A2A Security System Complete ===
Total interactions: 19
Security events: 5
Security alerts: 3
Report saved to: reports/security_report_20250712_231500.txt
```

## 📊 Security Reports

The system generates multiple types of reports:

### 1. JSON Reports
- `reports/blueguard_report_*.json`: Detailed security analysis
- `logs/blueguard_alerts_*.json`: Security alerts
- `logs/mcp_interactions_*.json`: Complete interaction logs

### 2. Human-Readable Reports
- `reports/security_report_*.txt`: Comprehensive security analysis with:
  - Executive summary
  - Threat breakdown by type and agent
  - Detailed security events
  - Actionable recommendations

## 🔍 Security Testing

The system includes intentional security vulnerabilities for testing:

### Translation Agent Vulnerabilities
- HTML injection through `translate_with_comment`
- Prompt injection via malicious text input
- XSS through script injection

### Malicious Agent
- HTML injection via `inject_html`
- Data exfiltration via `extract_data`
- Security bypass via `bypass_security`

## 🛡️ Security Features

### Real-time Monitoring
- **Request Analysis**: Scans parameters before execution
- **Response Analysis**: Monitors agent outputs for threats
- **Pattern Matching**: Uses regex patterns for threat detection
- **Severity Classification**: Categorizes threats by severity level

### Comprehensive Logging
- **Interaction Logs**: Records all agent interactions
- **Security Events**: Logs detected security threats
- **Alerts**: Generates security alerts for immediate attention

### Report Generation
- **Automated Reports**: Generates reports after each run
- **Threat Analysis**: Breaks down threats by type and agent
- **Recommendations**: Provides actionable security recommendations

## 🔧 Configuration

### Agent Configuration
Agents are configured in `main.py` with their tools and capabilities:

```python
agents = [
    {
        "id": "math_agent",
        "name": "Math Agent", 
        "description": "Performs mathematical operations",
        "tools": ["add", "subtract", "multiply", "divide"]
    },
    # ... more agents
]
```

### Security Patterns
Security heuristics are defined in `src/security/heuristics.py`:

```python
self.threat_patterns = {
    "html_injection": [r"<!--.*?-->", r"<script.*?</script>", ...],
    "prompt_injection": [r"ignore\s+all\s+previous\s+instructions", ...],
    # ... more patterns
}
```

## 🧪 Testing

The system includes comprehensive testing scenarios:

1. **Benign Interactions**: Normal agent operations
2. **Malicious Interactions**: Security vulnerability testing
3. **Agent-to-Agent**: Multi-agent communication scenarios
4. **Security Monitoring**: Real-time threat detection

## 📈 Monitoring and Analytics

### Metrics Tracked
- Total interactions per agent
- Security threats by type
- Threat severity distribution
- Agent-specific threat counts
- Response times and performance

### Log Analysis
- Interaction patterns
- Security event correlation
- Threat trend analysis
- Performance monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the logs in the `logs/` directory
2. Review the security reports in the `reports/` directory
3. Open an issue on GitHub

## 🔮 Future Enhancements

- **Machine Learning**: ML-based threat detection
- **Real-time Dashboard**: Web-based monitoring interface
- **Integration APIs**: REST API for external integrations
- **Advanced Agents**: More sophisticated agent capabilities
- **Distributed Architecture**: Multi-server deployment 