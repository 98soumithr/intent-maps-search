import random
import math
from typing import List, Optional, Dict, Any
from .models import PlaceResult, Location


class MockMapsService:
    """
    Mock Google Maps service that provides demo data without requiring API keys
    """
    
    def __init__(self):
        # Mock location data for San Francisco Bay Area
        self.mock_locations = {
            "san francisco": Location(lat=37.7749, lng=-122.4194, address="San Francisco, CA"),
            "san jose": Location(lat=37.3382, lng=-121.8863, address="San Jose, CA"),
            "palo alto": Location(lat=37.4419, lng=-122.1430, address="Palo Alto, CA"),
            "oakland": Location(lat=37.8044, lng=-122.2712, address="Oakland, CA"),
            "berkeley": Location(lat=37.8719, lng=-122.2585, address="Berkeley, CA"),
            "stanford": Location(lat=37.4241, lng=-122.1661, address="Stanford, CA"),
            "union square": Location(lat=37.7880, lng=-122.4074, address="Union Square, San Francisco, CA"),
            "downtown": Location(lat=37.7749, lng=-122.4194, address="Downtown San Francisco, CA")
        }
        
        # Mock place data
        self.mock_places = {
            "coffee shop": [
                {"name": "Blue Bottle Coffee", "rating": 4.2, "address": "66 Mint St, San Francisco, CA"},
                {"name": "Philz Coffee", "rating": 4.3, "address": "3101 24th St, San Francisco, CA"},
                {"name": "Ritual Coffee", "rating": 4.1, "address": "1026 Valencia St, San Francisco, CA"},
                {"name": "Sightglass Coffee", "rating": 4.4, "address": "270 7th St, San Francisco, CA"},
                {"name": "Four Barrel Coffee", "rating": 4.0, "address": "375 Valencia St, San Francisco, CA"}
            ],
            "restaurant": [
                {"name": "State Bird Provisions", "rating": 4.5, "address": "1529 Fillmore St, San Francisco, CA"},
                {"name": "Zuni Café", "rating": 4.2, "address": "1658 Market St, San Francisco, CA"},
                {"name": "Foreign Cinema", "rating": 4.3, "address": "2534 Mission St, San Francisco, CA"},
                {"name": "Slanted Door", "rating": 4.4, "address": "1 Ferry Building, San Francisco, CA"},
                {"name": "Gary Danko", "rating": 4.6, "address": "800 North Point St, San Francisco, CA"}
            ],
            "cafe": [
                {"name": "Tartine Bakery", "rating": 4.3, "address": "600 Guerrero St, San Francisco, CA"},
                {"name": "Craftsman and Wolves", "rating": 4.1, "address": "746 Valencia St, San Francisco, CA"},
                {"name": "Jane", "rating": 4.0, "address": "2123 Fillmore St, San Francisco, CA"},
                {"name": "Cafe Flore", "rating": 4.2, "address": "2298 Market St, San Francisco, CA"}
            ],
            "bar": [
                {"name": "The Alembic", "rating": 4.2, "address": "1725 Haight St, San Francisco, CA"},
                {"name": "Smuggler's Cove", "rating": 4.4, "address": "650 Gough St, San Francisco, CA"},
                {"name": "Trick Dog", "rating": 4.3, "address": "3010 20th St, San Francisco, CA"},
                {"name": "Local Edition", "rating": 4.1, "address": "691 Market St, San Francisco, CA"}
            ]
        }
    
    async def geocode_location(self, location_name: str) -> Optional[Location]:
        """Mock geocoding that returns predefined locations"""
        location_key = location_name.lower()
        return self.mock_locations.get(location_key)
    
    async def calculate_midpoint(self, location1: Location, location2: Location) -> Location:
        """Calculate midpoint between two locations"""
        mid_lat = (location1.lat + location2.lat) / 2
        mid_lng = (location1.lng + location2.lng) / 2
        
        return Location(
            lat=mid_lat, 
            lng=mid_lng, 
            address=f"Midpoint between {location1.address} and {location2.address}"
        )
    
    async def search_places(self, 
                          place_type: str, 
                          location: Location, 
                          radius: int = 5000,
                          constraints: List[Dict[str, Any]] = None) -> List[PlaceResult]:
        """Mock place search that returns demo data"""
        
        # Get mock places for the requested type
        places_data = self.mock_places.get(place_type, self.mock_places["restaurant"])
        
        # Filter by constraints if any
        filtered_places = places_data.copy()
        if constraints:
            for constraint in constraints:
                if constraint.get("type") == "rating_min":
                    min_rating = constraint.get("value", 4.0)
                    filtered_places = [p for p in filtered_places if p.get("rating", 0) >= min_rating]
        
        # Select random places (up to 3)
        selected_places = random.sample(filtered_places, min(3, len(filtered_places)))
        
        results = []
        for i, place_data in enumerate(selected_places):
            # Calculate mock distance
            distance = random.randint(100, 2000)  # meters
            
            result = PlaceResult(
                name=place_data["name"],
                place_id=f"mock_place_{i}",
                address=place_data["address"],
                rating=place_data["rating"],
                price_level=random.randint(1, 3),
                opening_hours={"weekday_text": ["Mon-Sun: 7:00 AM - 10:00 PM"]},
                photos=[],
                distance_from_midpoint=distance,
                distance_text=self._format_distance(distance),
                types=[place_type]
            )
            results.append(result)
        
        # Sort by rating
        results.sort(key=lambda x: x.rating or 0, reverse=True)
        
        return results
    
    def _format_distance(self, distance_meters: float) -> str:
        """Format distance in a human-readable way"""
        if distance_meters < 1000:
            return f"{int(distance_meters)}m"
        else:
            return f"{distance_meters/1000:.1f}km"
    
    def get_directions_url(self, destination_place_id: str, origin: str = None) -> str:
        """Generate mock directions URL"""
        return f"https://www.google.com/maps/search/?api=1&query={destination_place_id}"
    
    def get_embed_map_url(self, place_id: str) -> str:
        """Generate mock embed URL"""
        return f"https://www.google.com/maps/embed/v1/place?key=mock&place_id={place_id}"
