#!/usr/bin/env python3
"""
Startup script for Intent-Based Maps Search MVP
"""
import subprocess
import sys
import os
import time
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required keys"""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found!")
        print("Please copy .env.example to .env and add your API keys:")
        print("  cp .env.example .env")
        return False
    
    with open(env_path) as f:
        content = f.read()
        if "your_openai_api_key_here" in content or "your_google_maps_api_key_here" in content:
            print("❌ Please update .env file with your actual API keys!")
            return False
    
    print("✅ Environment file configured")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    try:
        # Start backend in background
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "backend.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
        print("✅ Backend started on http://localhost:8000")
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the Streamlit frontend"""
    print("🎨 Starting Streamlit frontend...")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "frontend/app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")

def main():
    print("🗺️  Intent-Based Maps Search MVP")
    print("=" * 40)
    
    # Check environment
    if not check_env_file():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    try:
        # Start frontend (this will block)
        start_frontend()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        # Clean up backend process
        if backend_process:
            backend_process.terminate()
            backend_process.wait()

if __name__ == "__main__":
    main()
