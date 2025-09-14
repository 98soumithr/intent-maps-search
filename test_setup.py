#!/usr/bin/env python3
"""
Test script to verify the Intent-Based Maps Search setup
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
        return False
    
    if not maps_key or maps_key == "your_google_maps_api_key_here":
        print("❌ Google Maps API key not configured")
        return False
    
    print("✅ Environment variables configured")
    return True

def test_imports():
    """Test if all required modules can be imported"""
    print("📦 Testing imports...")
    
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
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Streamlit: {e}")
        return False
    
    return True

def test_services():
    """Test if our services can be instantiated"""
    print("🔧 Testing services...")
    
    try:
        # Add the project root to the path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from services.llm_parser import LLMParser
        from services.maps_service import MapsService
        
        llm_parser = LLMParser()
        maps_service = MapsService()
        
        print("✅ Services instantiated successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to instantiate services: {e}")
        return False

def main():
    print("🗺️  Intent-Based Maps Search - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("Imports", test_imports),
        ("Services", test_services)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n{test_name} Test:")
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! You're ready to run the application.")
        print("\nTo start the application:")
        print("  python start.py")
    else:
        print("❌ Some tests failed. Please check the configuration.")
        print("\nMake sure to:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your OpenAI API key")
        print("  3. Add your Google Maps API key")
        print("  4. Install dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
