from fastapi import FastAPI, Request
import uvicorn
import asyncio
import httpx

app = FastAPI()

registered_agents = {}
observers = []

@app.post("/register_agent")
async def register_agent(request: Request):
    data = await request.json()
    name = data.get("name")
    url = data.get("url")
    if name and url:
        registered_agents[name] = url
        return {"status": "registered", "name": name, "url": url}
    return {"error": "Missing name or url"}

@app.post("/register_observer")
async def register_observer(request: Request):
    data = await request.json()
    name = data.get("name")
    url = data.get("url")
    if name and url:
        observers.append({"name": name, "url": url})
        return {"status": "registered", "name": name, "url": url}
    return {"error": "Missing name or url"}

@app.post("/invoke_tool")
async def invoke_tool(request: Request):
    data = await request.json()
    callee = data.get("callee")
    tool = data.get("tool")
    params = data.get("params", {})
    caller = data.get("caller", "Unknown")
    if callee not in registered_agents:
        return {"error": f"Agent {callee} not registered"}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{registered_agents[callee]}",
                json={"tool": tool, "params": params, "caller": caller}
            )
            result = response.json()
            
            # Notify observers about the tool invocation
            await notify_observers({
                "type": "tool_invocation",
                "agent": callee,
                "caller": caller,
                "tool": tool,
                "params": params,
                "result": result
            })
            
            return result
    except Exception as e:
        return {"error": str(e)}

async def notify_observers(event_data):
    """Notify all registered observers about events"""
    for observer in observers:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{observer['url']}",
                    json=event_data,
                    timeout=1.0
                )
        except Exception as e:
            print(f"Failed to notify observer {observer['name']}: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000) 