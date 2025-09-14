#!/usr/bin/env python3
"""
Free Demo - Intent-Based Maps Search without API keys
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.llm_parser import LLMParser
from services.mock_maps_service import MockMapsService

async def demo_query(query: str, parser: LLMParser, maps_service: MockMapsService):
    """Demo a single query"""
    print(f"\n🔍 Query: '{query}'")
    print("-" * 60)
    
    try:
        # Parse the query
        parsed = await parser.parse_query(query)
        print(f"✅ Parsed successfully:")
        print(f"   Place Type: {parsed.place_type}")
        print(f"   Locations: {parsed.locations}")
        print(f"   Constraints: {parsed.constraints}")
        print(f"   Midpoint Calculation: {parsed.midpoint_calculation}")
        print(f"   Search Radius: {parsed.radius}m")
        
        # Geocode locations
        if parsed.locations:
            locations = []
            for loc_name in parsed.locations:
                location = await maps_service.geocode_location(loc_name)
                if location:
                    locations.append(location)
                    print(f"   📍 {loc_name}: {location.address}")
                else:
                    print(f"   ❌ Could not find: {loc_name}")
            
            # Calculate midpoint if needed
            if parsed.midpoint_calculation and len(locations) >= 2:
                midpoint = await maps_service.calculate_midpoint(locations[0], locations[1])
                print(f"   📍 Midpoint: {midpoint.address}")
                search_location = midpoint
            elif locations:
                search_location = locations[0]
            else:
                print("   ❌ No valid locations found")
                return
            
            # Search for places
            results = await maps_service.search_places(
                place_type=parsed.place_type,
                location=search_location,
                radius=parsed.radius,
                constraints=parsed.constraints
            )
            
            print(f"   🏢 Found {len(results)} results:")
            for i, result in enumerate(results):
                print(f"      {i+1}. {result.name}")
                print(f"         📍 {result.address}")
                if result.rating:
                    print(f"         ⭐ {result.rating}/5")
                if result.distance_text:
                    print(f"         📏 {result.distance_text}")
                print()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

async def main():
    """Run demo with example queries"""
    print("🗺️  Intent-Based Maps Search - FREE DEMO")
    print("=" * 60)
    print("🎉 This demo works without any API keys!")
    print("   Using improved local parsing and mock data")
    
    # Initialize services
    parser = LLMParser()
    maps_service = MockMapsService()
    
    # Example queries
    demo_queries = [
        "Find me a coffee shop halfway between San Francisco and San Jose with parking",
        "Show me restaurants in Palo Alto with good ratings",
        "Find a quiet cafe near Stanford University",
        "Coffee shops in downtown San Francisco open late",
        "Find a bar in Berkeley with parking"
    ]
    
    print("\nRunning demo queries...")
    
    for query in demo_queries:
        await demo_query(query, parser, maps_service)
        print()
    
    print("🎉 Demo completed!")
    print("\n✨ What this demo shows:")
    print("   ✅ Natural language query parsing")
    print("   ✅ Location extraction and geocoding")
    print("   ✅ Midpoint calculation between locations")
    print("   ✅ Constraint filtering (parking, ratings, etc.)")
    print("   ✅ Place search with mock data")
    print("   ✅ Results ranking and formatting")
    
    print("\n🚀 To run the full web application:")
    print("   1. Fix API keys in .env (optional)")
    print("   2. Run: python start.py")
    print("   3. Open: http://localhost:8501")

if __name__ == "__main__":
    asyncio.run(main())
