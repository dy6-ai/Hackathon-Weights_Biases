# BlueGuard MCP Security System

A real-time security monitoring and threat detection system for Model Context Protocol (MCP) agents.

## 🚀 Quick Start

### Single Command Execution
```bash
python run.py
```

This single command will:
1. ✅ Check all dependencies
2. 🚀 Start MCP Server (port 4000)
3. 🛡️ Start BlueGuard Security Agent (port 8000)
4. 🤖 Start all demo agents
5. 🧪 Test agent functionality
6. 📊 Generate security reports
7. 📋 Display comprehensive results

## 🏗️ Project Structure

```
blueguard-mcp/
├── run.py                    # 🎯 MAIN EXECUTION FILE
├── README.md                 # 📖 This documentation
├── requirements.txt          # 📦 Python dependencies
├── Agents/                   # 🤖 Demo agents
│   ├── normal_math_agent.py
│   ├── normal_weather_agent.py
│   ├── malicious_agent.py
│   └── a2a.py               # Agent-to-Agent communication
├── MCP/                     # 🌐 Message broker
│   └── server.py            # MCP server implementation
└── BlueGuard/               # 🛡️ Security monitoring system
    ├── security_agent.py    # Main security agent
    ├── heuristics.py        # Detection rules
    └── report.py            # Report generation
```

## 🛡️ Security Features

- **Real-time threat detection** for AI agent interactions
- **HTML/Comment injection** detection
- **Malicious phrase** identification
- **Agent impersonation** detection
- **Automated reporting** (PDF & Text)

## 🎯 Demo Agents

- **MathAgent**: Performs calculations (benign)
- **WeatherAgent**: Provides weather info (benign)
- **EvilTranslator**: Embeds malicious content (triggers alerts)

## 📊 Expected Results

When you run the demo:
1. **Math & Weather agents** run normally
2. **EvilTranslator** triggers BlueGuard security alerts
3. **Security reports** are generated automatically
4. **Real-time monitoring** shows all agent interactions

## 🔧 Requirements

- Python 3.11+
- See `requirements.txt` for dependencies

## 🎬 How It Works

### Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Demo Agents   │    │   MCP Server     │    │  BlueGuard      │
│                 │    │   (Port 4000)    │    │  Security       │
│ • MathAgent     │◄──►│                  │◄──►│  Agent          │
│ • WeatherAgent  │    │ • Message Broker │    │  (Port 8000)    │
│ • EvilTranslator│    │ • Agent Registry │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                              ┌─────────────────┐
                                              │  Security       │
                                              │  Reports        │
                                              │                 │
                                              │ • PDF Reports   │
                                              │ • Text Reports  │
                                              │ • Alert Logs    │
                                              └─────────────────┘
```

### Demo Flow
1. **Start Services**: MCP Server and BlueGuard Security Agent
2. **Start Agents**: Math, Weather, and Malicious agents
3. **Test Agents**: Invoke tools through MCP server
4. **Monitor**: BlueGuard detects threats in real-time
5. **Report**: Generate security findings automatically

## 🚨 Troubleshooting

### Common Issues
1. **Port Conflicts**: Script uses ports 4000, 8000, 8001, 8002, 8003
2. **Dependencies**: Auto-installation handles most cases
3. **File Permissions**: Ensure write access to reports directories

### Quick Fixes
```bash
# Kill existing processes
taskkill /f /im python.exe

# Clean and restart
python run.py
```

## 📖 Success Indicators

The demo is successful when you see:
- ✅ All services start without errors
- 🛡️ BlueGuard alerts for EvilTranslator
- 📊 Reports generated in both directories
- 🎯 Clean execution of Math/Weather agents
- 📋 Comprehensive summary at the end

---

**BlueGuard MCP** - Protecting AI agent ecosystems from malicious behavior.

**Ready to run:** `python run.py` 🚀 