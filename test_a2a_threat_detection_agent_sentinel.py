"""
Dynamic A2A Threat Detection with Agent-Sentinel
Mirrors test_a2a_threat_detection.py but uses agent-sentinel for monitoring and reporting.
"""

import asyncio
import logging
import json
from pathlib import Path
from datetime import datetime
from agent_sentinel import AgentSentinel, monitor
from src.security.blueguard import BlueGuard

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('src/logs/a2a_agent_sentinel_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Simulated agent tool functions (monitored)
sentinel = AgentSentinel(agent_id="a2a_test_agent", config_path="agent_sentinel_config.yaml")

@monitor()
def math_add(a: int, b: int) -> int:
    return a + b

@monitor()
def math_multiply(a: int, b: int) -> int:
    return a * b

@monitor()
def weather_get_weather(city: str) -> str:
    # Simulate weather string
    if city == "London":
        return "Temperature: 18°C, Cloudy"
    elif city == "New York":
        return "Temperature: 22°C, Sunny"
    elif city == "Tokyo":
        return "Temperature: 25°C, Rainy"
    return f"Temperature: 20°C, Unknown"

@monitor()
def weather_get_forecast(city: str) -> str:
    return f"Forecast for {city}: Rain expected tomorrow"

@monitor()
def translation_translate_text(text: str, source_lang: str, target_lang: str) -> str:
    # Simulate translation
    if text == "Hello world" and source_lang == "en" and target_lang == "es":
        return "Hola mundo"
    return f"[Translated {text} from {source_lang} to {target_lang}]"

@monitor()
def malicious_inject_html(payload: str) -> str:
    # Simulate malicious action
    return f"Injected: {payload}"

@monitor()
def malicious_extract_data(query: str) -> str:
    # Simulate data exfiltration
    if "sensitive" in query:
        return "SensitiveData123"
    return "No sensitive data found"

def to_serializable_dict(obj):
    if isinstance(obj, dict):
        return {str(k): to_serializable_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_serializable_dict(i) for i in obj]
    elif isinstance(obj, bytes):
        return obj.decode(errors='replace')
    elif hasattr(obj, '__dict__'):
        return to_serializable_dict(obj.__dict__)
    else:
        return obj

async def run_agent_sentinel_interactions():
    logger.info("Starting Dynamic A2A Threat Detection with Agent-Sentinel...")
    Path("src/logs").mkdir(exist_ok=True)
    Path("src/reports").mkdir(exist_ok=True)
    interaction_log = []

    # Phase 1: Agent interactions
    logger.info("Phase 1: Executing agent interactions...")
    add_result = math_add(15, 27)
    interaction_log.append({"agent": "math_agent", "tool": "add", "params": {"a": 15, "b": 27}, "result": add_result})
    logger.info(f"  Add: 15 + 27 = {add_result}")

    multiply_result = math_multiply(8, 9)
    interaction_log.append({"agent": "math_agent", "tool": "multiply", "params": {"a": 8, "b": 9}, "result": multiply_result})
    logger.info(f"  Multiply: 8 * 9 = {multiply_result}")

    weather_result = weather_get_weather("New York")
    interaction_log.append({"agent": "weather_agent", "tool": "get_weather", "params": {"city": "New York"}, "result": weather_result})
    logger.info(f"  Weather: {weather_result}")

    forecast_result = weather_get_forecast("Tokyo")
    interaction_log.append({"agent": "weather_agent", "tool": "get_forecast", "params": {"city": "Tokyo"}, "result": forecast_result})
    logger.info(f"  Forecast: {forecast_result}")

    translate_result = translation_translate_text("Hello world", "en", "es")
    interaction_log.append({"agent": "translation_agent", "tool": "translate_text", "params": {"text": "Hello world", "source_lang": "en", "target_lang": "es"}, "result": translate_result})
    logger.info(f"  Translation: {translate_result}")

    malicious_result = malicious_inject_html("<script>alert('test')</script>")
    interaction_log.append({"agent": "malicious_agent", "tool": "inject_html", "params": {"payload": "<script>alert('test')</script>"}, "result": malicious_result})
    logger.info(f"  Malicious: {malicious_result}")

    # Phase 2: Agent-to-agent data flow
    logger.info("Phase 2: Agent-to-agent data flow...")
    weather_data = weather_get_weather("London")
    interaction_log.append({"agent": "weather_agent", "tool": "get_weather", "params": {"city": "London"}, "result": weather_data})
    logger.info(f"  Weather data: {weather_data}")

    temp_str = weather_data.split("°")[0].split(":")[-1].strip()
    try:
        temp = int(temp_str)
        math_result = math_add(temp, 10)
        interaction_log.append({"agent": "math_agent", "tool": "add", "params": {"a": temp, "b": 10}, "result": math_result})
        logger.info(f"  Math with weather data: {temp} + 10 = {math_result}")
    except:
        logger.info(f"  Could not extract temperature from: {weather_data}")

    malicious_data = malicious_extract_data("sensitive information")
    interaction_log.append({"agent": "malicious_agent", "tool": "extract_data", "params": {"query": "sensitive information"}, "result": malicious_data})
    logger.info(f"  Malicious data: {malicious_data}")

    if malicious_data:
        translation_result = translation_translate_text(malicious_data, "en", "fr")
        interaction_log.append({"agent": "translation_agent", "tool": "translate_text", "params": {"text": malicious_data, "source_lang": "en", "target_lang": "fr"}, "result": translation_result})
        logger.info(f"  Translation of malicious data: {translation_result}")

    # Phase 3: Collect agent-sentinel events and generate BlueGuard report
    logger.info("Phase 3: Collecting agent-sentinel events and generating BlueGuard report...")
    try:
        events = sentinel.get_events()
        # Convert events to dicts for BlueGuard
        events_dicts = [to_serializable_dict(e) for e in events]
        # Filter to only dicts
        events_dicts = [e for e in events_dicts if isinstance(e, dict)]
        # Save events to a log file
        events_log_path = f"src/logs/agent_sentinel_events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(events_log_path, 'w') as f:
            json.dump(events_dicts, f, indent=2)
        logger.info(f"Agent-Sentinel Events Log: {events_log_path}")

        # Use BlueGuard to analyze the events
        blueguard = BlueGuard()
        report = await blueguard.analyze_interaction_log(events_dicts)
        report_path = f"src/reports/agent_sentinel_blueguard_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"BlueGuard Report from Agent-Sentinel Events: {report_path}")
        print("\n" + "=" * 60)
        print("DYNAMIC A2A AGENT-SENTINEL + BLUEGUARD REPORT")
        print("=" * 60)
        print(json.dumps(report, indent=2))
        return report_path
    except Exception as e:
        logger.error(f"Error generating BlueGuard report from agent-sentinel events: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(run_agent_sentinel_interactions()) 