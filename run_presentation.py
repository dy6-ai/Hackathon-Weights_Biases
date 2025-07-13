#!/usr/bin/env python3
"""
Run Complete Presentation Workflow

This script runs the complete presentation workflow:
1. A2A Architecture Demo with predefined threats
2. BlueGuard Analysis of generated logs
3. Report generation

Perfect for presentations and demonstrations.
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path

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

def run_command(cmd: str, description: str) -> bool:
    """Run a command and return success status."""
    ColorPrint.print_info(f"Running: {description}")
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            ColorPrint.print_success(f"{description} completed successfully")
            if result.stdout:
                print("Output:")
                print(result.stdout)
            return True
        else:
            ColorPrint.print_error(f"{description} failed")
            if result.stderr:
                print("Error:")
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        ColorPrint.print_error(f"{description} timed out")
        return False
    except Exception as e:
        ColorPrint.print_error(f"{description} error: {e}")
        return False

def check_dependencies():
    """Check if all required files exist."""
    ColorPrint.print_info("Checking dependencies...")
    
    required_files = [
        "presentation_demo.py",
        "blueguard_analyzer.py",
        "src/agent_sentinel/a2a.py",
        "src/agent_sentinel/mcp_server.py",
        "agents/math_agent.py",
        "agents/weather_agent.py",
        "agents/translation_agent.py"
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

def create_directories():
    """Create necessary directories."""
    ColorPrint.print_info("Creating directories...")
    
    directories = ["logs", "reports"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        ColorPrint.print_success(f"Created: {directory}/")

def run_presentation_workflow():
    """Run the complete presentation workflow."""
    ColorPrint.print_header("🎬 Complete Presentation Workflow")
    print("=" * 60)
    print("This workflow will:")
    print("1. 🚀 Start A2A Architecture Demo with predefined threats")
    print("2. 📋 Generate comprehensive logs")
    print("3. 🛡️ Run BlueGuard Analysis on logs")
    print("4. 📊 Generate detailed reports")
    print("=" * 60)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        ColorPrint.print_error("Dependency check failed. Please ensure all files are present.")
        return False
    
    # Step 2: Create directories
    create_directories()
    
    # Step 3: Run A2A Demo
    ColorPrint.print_header("Step 1: Running A2A Architecture Demo")
    print("-" * 40)
    
    demo_success = run_command(
        "python presentation_demo.py",
        "A2A Architecture Demo"
    )
    
    if not demo_success:
        ColorPrint.print_error("A2A Demo failed. Stopping workflow.")
        return False
    
    # Wait a moment for files to be written
    time.sleep(2)
    
    # Step 4: Run BlueGuard Analysis
    ColorPrint.print_header("Step 2: Running BlueGuard Analysis")
    print("-" * 40)
    
    analysis_success = run_command(
        "python blueguard_analyzer.py",
        "BlueGuard Analysis"
    )
    
    if not analysis_success:
        ColorPrint.print_warning("BlueGuard Analysis failed, but continuing...")
    
    # Step 5: Summary
    ColorPrint.print_header("🎉 Presentation Workflow Complete!")
    print("=" * 50)
    
    # Check generated files
    logs_dir = Path("logs")
    reports_dir = Path("reports")
    
    log_files = list(logs_dir.glob("*.log"))
    report_files = list(reports_dir.glob("*.json"))
    markdown_files = list(reports_dir.glob("*.md"))
    
    print(f"📁 Generated Files:")
    print(f"  • Log Files: {len(log_files)}")
    for log_file in log_files:
        print(f"    - {log_file.name}")
    
    print(f"  • JSON Reports: {len(report_files)}")
    for report_file in report_files:
        print(f"    - {report_file.name}")
    
    print(f"  • Markdown Reports: {len(markdown_files)}")
    for md_file in markdown_files:
        print(f"    - {md_file.name}")
    
    print(f"\n📊 Presentation Results:")
    print(f"  ✅ A2A Architecture Demo: {'Completed' if demo_success else 'Failed'}")
    print(f"  ✅ BlueGuard Analysis: {'Completed' if analysis_success else 'Failed'}")
    print(f"  ✅ Log Generation: {'Completed' if log_files else 'Failed'}")
    print(f"  ✅ Report Generation: {'Completed' if report_files or markdown_files else 'Failed'}")
    
    print(f"\n🎯 Key Demonstrations:")
    print(f"  • A2A Protocol with security monitoring")
    print(f"  • Real-time threat detection and blocking")
    print(f"  • Comprehensive logging of all interactions")
    print(f"  • BlueGuard analysis of logs for threat detection")
    print(f"  • Automated report generation")
    
    print(f"\n📋 Next Steps:")
    print(f"  • Review generated reports in reports/ directory")
    print(f"  • Check logs in logs/ directory")
    print(f"  • Customize threat patterns and security rules")
    print(f"  • Scale to production environment")
    
    return True

def main():
    """Main entry point."""
    try:
        success = run_presentation_workflow()
        if success:
            ColorPrint.print_success("Presentation workflow completed successfully!")
            print("\n🎉 Ready for your presentation!")
        else:
            ColorPrint.print_error("Presentation workflow failed.")
            sys.exit(1)
    except KeyboardInterrupt:
        ColorPrint.print_warning("Presentation workflow interrupted by user.")
    except Exception as e:
        ColorPrint.print_error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 