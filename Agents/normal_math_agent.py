import json
import httpx
from fastapi import FastAPI, Request
import uvicorn
from a2a import Agent, Tool

SERVER = "http://localhost:4000"

def add(a: int, b: int) -> int:
    """Add two integers"""
    return a + b

my_agent = Agent(
    name="MathAgent",
    tools=[Tool(fn=add, description="Add two integers")]
)

# FastAPI app for receiving tool invocations
app = FastAPI()

@app.post("/tool")
async def handle_tool(request: Request):
    """Handle tool invocations from MCP server"""
    data = await request.json()
    tool_name = data.get("tool")
    params = data.get("params", {})
    
    if tool_name == "add":
        result = add(params.get("a", 0), params.get("b", 0))
        return {"result": result}
    else:
        return {"error": f"Unknown tool: {tool_name}"}

# Register with MCP server
async def register_with_mcp():
    """Register this agent with the MCP server"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{SERVER}/register_agent", 
                json={"name": "MathAgent", "url": "http://localhost:8001/tool"})
            print(f"[MathAgent] Registered with MCP server: {response.status_code}")
        except Exception as e:
            print(f"[MathAgent] Failed to register: {e}")

if __name__ == "__main__":
    # Start the FastAPI server
    import threading
    def run_server():
        uvicorn.run(app, host="0.0.0.0", port=8001, log_level="error")
    
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
        print("[MathAgent] Shutting down...") 