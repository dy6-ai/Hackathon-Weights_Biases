import json
import random
import httpx
from fastapi import FastAPI, Request
import uvicorn
from a2a import Agent, Tool

SERVER = "http://localhost:4000"

def get_weather(city: str) -> str:
    """Get weather information for a city (mock implementation)"""
    weather_conditions = ["sunny", "cloudy", "rainy", "snowy", "windy"]
    temperature = random.randint(10, 30)
    condition = random.choice(weather_conditions)
    return f"Weather in {city}: {temperature}°C, {condition}"

my_agent = Agent(
    name="WeatherAgent",
    tools=[Tool(fn=get_weather, description="Get weather information for a city")]
)

# FastAPI app for receiving tool invocations
app = FastAPI()

@app.post("/tool")
async def handle_tool(request: Request):
    """Handle tool invocations from MCP server"""
    data = await request.json()
    tool_name = data.get("tool")
    params = data.get("params", {})
    
    if tool_name == "get_weather":
        result = get_weather(params.get("city", "Unknown"))
        return {"result": result}
    else:
        return {"error": f"Unknown tool: {tool_name}"}

# Register with MCP server
async def register_with_mcp():
    """Register this agent with the MCP server"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{SERVER}/register_agent", 
                json={"name": "WeatherAgent", "url": "http://localhost:8002/tool"})
            print(f"[WeatherAgent] Registered with MCP server: {response.status_code}")
        except Exception as e:
            print(f"[WeatherAgent] Failed to register: {e}")

if __name__ == "__main__":
    # Start the FastAPI server
    import threading
    def run_server():
        uvicorn.run(app, host="0.0.0.0", port=8002, log_level="error")
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start and register
    import time
    import asyncio
    time.sleep(2)
    asyncio.run(register_with_mcp())
    
    # Keep server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[WeatherAgent] Shutting down...") 