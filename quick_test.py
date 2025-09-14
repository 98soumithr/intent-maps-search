#!/usr/bin/env python3
"""
Quick test script to verify basic functionality without full imports
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test if environment variables are set"""
    print("🔍 Testing environment configuration...")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    maps_key = os.getenv("GOOGLE_MAPS_API_KEY")
    
    if not openai_key or openai_key == "your_openai_api_key_here":
        print("❌ OpenAI API key not configured")
        print("   Please add your OpenAI API key to .env file")
        return False
    
    if not maps_key or maps_key == "your_google_maps_api_key_here":
        print("❌ Google Maps API key not configured")
        print("   Please add your Google Maps API key to .env file")
        return False
    
    print("✅ Environment variables configured")
    return True

def test_basic_imports():
    """Test basic imports without problematic packages"""
    print("📦 Testing basic imports...")
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import OpenAI: {e}")
        return False
    
    try:
        import googlemaps
        print("✅ Google Maps imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Google Maps: {e}")
        return False
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import FastAPI: {e}")
        return False
    
    return True

def test_project_structure():
    """Test if project files exist"""
    print("📁 Testing project structure...")
    
    required_files = [
        "backend/main.py",
        "frontend/app.py", 
        "services/llm_parser.py",
        "services/maps_service.py",
        "services/models.py",
        "requirements.txt",
        ".env.example"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    return True

def main():
    print("🗺️  Intent-Based Maps Search - Quick Test")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Basic Imports", test_basic_imports),
        ("Project Structure", test_project_structure)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n{test_name} Test:")
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 Basic setup looks good!")
        print("\nNext steps:")
        print("  1. Make sure you have valid API keys in .env")
        print("  2. Try running: python start.py")
        print("  3. Or test with: python demo.py")
    else:
        print("❌ Some issues found. Please fix them before proceeding.")
        print("\nMake sure to:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your OpenAI API key")
        print("  3. Add your Google Maps API key")

if __name__ == "__main__":
    main()
