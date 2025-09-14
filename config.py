"""
Configuration settings for Intent-Based Maps Search MVP
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Server Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", 8501))

# Search Configuration
DEFAULT_SEARCH_RADIUS = 5000  # meters
MAX_RESULTS = 3
DEFAULT_TIMEOUT = 30  # seconds

# LLM Configuration
OPENAI_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 500
TEMPERATURE = 0.1

# Validation
def validate_config():
    """Validate that required configuration is present"""
    errors = []
    
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        errors.append("OpenAI API key not configured")
    
    if not GOOGLE_MAPS_API_KEY or GOOGLE_MAPS_API_KEY == "your_google_maps_api_key_here":
        errors.append("Google Maps API key not configured")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")
    
    return True

# Example queries for testing
EXAMPLE_QUERIES = [
    "Find me a coffee shop halfway between San Francisco and San Jose with parking",
    "Show me quiet restaurants where I can finish a meeting in 45 minutes", 
    "Find a vegan restaurant halfway between Palo Alto and Oakland that's open late",
    "Coffee shops near me with good WiFi",
    "Restaurants in downtown San Francisco with parking and open until 10 PM",
    "Find a bar near Union Square that's open late",
    "Show me cafes in Berkeley with outdoor seating",
    "Find a restaurant halfway between Stanford and San Jose with good ratings"
]

# Supported place types
PLACE_TYPES = [
    "restaurant", "cafe", "coffee shop", "bar", "hotel", 
    "gas station", "parking", "pharmacy", "hospital", "store"
]

# Supported constraints
CONSTRAINT_TYPES = [
    "parking", "quiet", "open_late", "wifi", "rating_min", 
    "time_limit", "price_range", "outdoor_seating"
]
