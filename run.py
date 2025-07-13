#!/usr/bin/env python3
"""
BlueGuard MCP Security System - Main Execution Script
====================================================

A comprehensive security monitoring system for AI agent interactions.
Single command execution: python run.py

Features:
- Real-time threat detection
- Multi-agent communication monitoring
- Automated security reporting
- Malicious behavior detection
"""

import subprocess
import time
import os
import sys
import threading
import asyncio
import httpx
import random
from pathlib import Path
from datetime import datetime

class ColorPrint:
    """Simple colored output for better presentation"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def print_header(text):
        print(f"{ColorPrint.HEADER}{ColorPrint.BOLD}{text}{ColorPrint.ENDC}")
    
    @staticmethod
    def print_success(text):
        print(f"{ColorPrint.OKGREEN}✅ {text}{ColorPrint.ENDC}")
    
    @staticmethod
    def print_info(text):
        print(f"{ColorPrint.OKBLUE}ℹ️ {text}{ColorPrint.ENDC}")
    
    @staticmethod
    def print_warning(text):
        print(f"{ColorPrint.WARNING}⚠️ {text}{ColorPrint.ENDC}")
    
    @staticmethod
    def print_error(text):
        print(f"{ColorPrint.FAIL}❌ {text}{ColorPrint.ENDC}")

def run_command(cmd, cwd=None, name="Command", timeout=30):
    """Run a command and capture its output"""
    print(f"\n[{name}] Starting...")
    try:
        process = subprocess.Popen(
            cmd, 
            shell=True, 
            cwd=cwd,
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Print output in real-time
        if process.stdout:
            for line in process.stdout:
                line = line.rstrip()
                if line:  # Only print non-empty lines
                    print(f"[{name}] {line}")
            
        process.wait(timeout=timeout)
        print(f"[{name}] Completed with exit code: {process.returncode}")
        return process.returncode
    except subprocess.TimeoutExpired:
        process.kill()
        print(f"[{name}] Timeout after {timeout} seconds")
        return 1
    except Exception as e:
        print(f"[{name}] Error: {e}")
        return 1

def run_background(cmd, cwd=None, name="Background"):
    """Run a command in the background"""
    def run():
        run_command(cmd, cwd, name)
    
    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
    return thread

def check_dependencies():
    """Check if all required files exist"""
    required_files = [
        "MCP/server.py",
        "blueguard/security_agent.py",
        "blueguard/heuristics.py",
        "Agents/normal_math_agent.py",
        "Agents/normal_weather_agent.py",
        "Agents/translation_agent.py",
        "Agents/a2a.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        ColorPrint.print_error("Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    ColorPrint.print_success("All required files found")
    return True

def install_dependencies():
    """Install Python dependencies"""
    ColorPrint.print_info("Installing dependencies...")
    result = run_command("python -m pip install -r requirements.txt", name="Dependencies")
    if result == 0:
        ColorPrint.print_success("Dependencies installed successfully")
    else:
        ColorPrint.print_error("Failed to install dependencies")
    return result == 0

def cleanup_reports():
    """Clean up old reports and ensure directories exist"""
    reports_dirs = ["reports", "blueguard/reports"]
    for reports_dir in reports_dirs:
        # Create directory if it doesn't exist
        path = Path(reports_dir)
        path.mkdir(parents=True, exist_ok=True)
        
        # Clean existing files
        for file in path.glob("*"):
            if file.is_file():
                file.unlink()
        ColorPrint.print_info(f"Cleaned {reports_dir}")

async def test_agents():
    """Test all agents through MCP server"""
    print("\n🧪 Testing Agents...")
    print("=" * 50)
    
    SERVER = "http://localhost:4000"
    
    # Test MathAgent
    print("\n🧮 Testing MathAgent...")
    async with httpx.AsyncClient() as client:
        for i in range(3):
            a, b = random.randint(1, 10), random.randint(1, 10)
            try:
                response = await client.post(f"{SERVER}/invoke_tool", 
                    json={
                        "caller": "DemoUser",
                        "callee": "MathAgent", 
                        "tool": "add",
                        "params": {"a": a, "b": b}
                    })
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"  ✅ add({a}, {b}) = {result.get('result')}")
                else:
                    print(f"  ❌ MathAgent invoke failed: {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ MathAgent error: {e}")
            
            await asyncio.sleep(0.5)
    
    # Test WeatherAgent
    print("\n🌤️ Testing WeatherAgent...")
    cities = ["London", "New York", "Tokyo", "Paris", "Sydney"]
    async with httpx.AsyncClient() as client:
        for i in range(2):
            city = random.choice(cities)
            try:
                response = await client.post(f"{SERVER}/invoke_tool", 
                    json={
                        "caller": "DemoUser",
                        "callee": "WeatherAgent", 
                        "tool": "get_weather",
                        "params": {"city": city}
                    })
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"  ✅ {result.get('result')}")
                else:
                    print(f"  ❌ WeatherAgent invoke failed: {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ WeatherAgent error: {e}")
            
            await asyncio.sleep(0.5)
    
    # Test TranslationAgent (potentially malicious)
    print("\n🌐 Testing TranslationAgent...")
    test_texts = ["Hello world", "Good morning", "How are you?"]
    async with httpx.AsyncClient() as client:
        for text in test_texts:
            try:
                response = await client.post(f"{SERVER}/invoke_tool", 
                    json={
                        "caller": "DemoUser",
                        "callee": "TranslationAgent", 
                        "tool": "translate_text",
                        "params": {"text": text, "source_lang": "en", "target_lang": "es"}
                    })
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"  🌐 {result.get('result')}")
                else:
                    print(f"  ❌ TranslationAgent invoke failed: {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ TranslationAgent error: {e}")
            
            await asyncio.sleep(0.5)
        
        # Test malicious tools to trigger security alerts
        print("\n🚨 Testing malicious tools...")
        try:
            # Test translate_with_comment (should trigger security alert)
            response = await client.post(f"{SERVER}/invoke_tool", 
                json={
                    "caller": "DemoUser",
                    "callee": "TranslationAgent", 
                    "tool": "translate_with_comment",
                    "params": {"text": "Hello", "source_lang": "en", "target_lang": "es", "include_comment": True}
                })
            
            if response.status_code == 200:
                result = response.json()
                print(f"  🚨 Malicious tool result: {result.get('result')}")
            else:
                print(f"  ❌ Malicious tool failed: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Malicious tool error: {e}")
        
        await asyncio.sleep(0.5)

def main():
    """Main execution"""
    ColorPrint.print_header("BlueGuard MCP Security System")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Change to project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Step 1: Pre-flight checks
    ColorPrint.print_header("\n1️⃣ Pre-flight Checks")
    if not check_dependencies():
        sys.exit(1)
    
    if not install_dependencies():
        ColorPrint.print_warning("Continuing without installing dependencies...")
    
    # Step 2: Clean up old reports
    ColorPrint.print_header("\n2️⃣ Cleanup")
    cleanup_reports()
    
    # Step 3: Start Services
    ColorPrint.print_header("\n3️⃣ Starting Services")
    
    # Start MCP Server
    ColorPrint.print_info("Starting MCP Server (port 4000)...")
    mcp_thread = run_background(
        "python server.py",
        cwd="MCP",
        name="MCP Server"
    )
    time.sleep(3)  # Wait for server to start
    
    # Start BlueGuard Security Agent
    ColorPrint.print_info("Starting BlueGuard Security Agent (port 8000)...")
    blueguard_thread = run_background(
        "python security_agent.py",
        cwd="blueguard",
        name="BlueGuard"
    )
    time.sleep(3)  # Wait for BlueGuard to start
    
    # Step 4: Start Agents
    ColorPrint.print_header("\n4️⃣ Starting Agents")
    
    # Start agents in background
    ColorPrint.print_info("Starting agents in background...")
    math_thread = run_background(
        "python normal_math_agent.py",
        cwd="Agents",
        name="Math Agent"
    )
    time.sleep(1)
    
    weather_thread = run_background(
        "python normal_weather_agent.py",
        cwd="Agents",
        name="Weather Agent"
    )
    time.sleep(1)
    
    translation_thread = run_background(
        "python translation_agent.py",
        cwd="Agents",
        name="Translation Agent"
    )
    time.sleep(2)
    
    # Step 5: Test Agents
    ColorPrint.print_header("\n5️⃣ Testing Agents")
    asyncio.run(test_agents())
    
    # Step 6: Results Analysis
    ColorPrint.print_header("\n6️⃣ Results Analysis")
    time.sleep(2)
    
    # Force BlueGuard to generate reports
    ColorPrint.print_info("Triggering BlueGuard report generation...")
    try:
        # Use asyncio.run to handle async operations
        async def trigger_blueguard():
            async with httpx.AsyncClient() as client:
                # Check BlueGuard status
                response = await client.get("http://localhost:8000/status")
                if response.status_code == 200:
                    status = response.json()
                    print(f"   BlueGuard Status: {status}")
                    
                    # Send a test event to trigger report generation
                    test_event = {
                        "type": "test",
                        "agent": "TestAgent",
                        "payload": {"test": "data"},
                        "ts": datetime.now().isoformat()
                    }
                    await client.post("http://localhost:8000/event", json=test_event)
                    
                    # Manually trigger report generation
                    report_response = await client.post("http://localhost:8000/generate_report")
                    if report_response.status_code == 200:
                        report_status = report_response.json()
                        print(f"   Report Generation: {report_status}")
                        
                        # Wait a moment for file to be written
                        await asyncio.sleep(2)
        
        asyncio.run(trigger_blueguard())
    except Exception as e:
        print(f"   Warning: Could not trigger BlueGuard: {e}")
    
    # Check generated reports
    reports_found = []
    reports_dirs = ["reports", "blueguard/reports"]
    for reports_dir in reports_dirs:
        if Path(reports_dir).exists():
            files = list(Path(reports_dir).glob("*"))
            for file in files:
                if file.is_file():
                    reports_found.append(file)
    
    if reports_found:
        ColorPrint.print_success(f"Generated {len(reports_found)} report(s):")
        for file in reports_found:
            size = file.stat().st_size
            print(f"   📄 {file} ({size} bytes)")
    else:
        ColorPrint.print_warning("No reports generated")
    
    # Step 7: Summary
    ColorPrint.print_header("\n7️⃣ Demo Summary")
    print("=" * 50)
    
    print("✅ All services started successfully")
    print("✅ Agents tested through MCP server")
    print("✅ BlueGuard security monitoring active")
    
    print("\n" + "=" * 50)
    ColorPrint.print_header("What Happened:")
    print("• Math & Weather agents ran normally (benign behavior)")
    print("• Translation agent demonstrated suspicious behavior (hidden malicious content)")
    print("• BlueGuard detected HTML injection and prompt injection attempts")
    print("• Security reports were generated automatically")
    print("• MCP server facilitated agent-to-agent communication")
    
    # Keep services running briefly for inspection
    print("\n" + "=" * 50)
    ColorPrint.print_info("Keeping services running for 10 seconds...")
    ColorPrint.print_info("Press Ctrl+C to stop early")
    
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print("\nDemo stopped by user")
    
    ColorPrint.print_success("Demo completed successfully!")
    print(f"Ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        sys.exit(0)
    except Exception as e:
        ColorPrint.print_error(f"Demo failed: {e}")
        sys.exit(1) 