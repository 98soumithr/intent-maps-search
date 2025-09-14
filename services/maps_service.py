import googlemaps
import os
from typing import List, Optional, Dict, Any, Tuple
from .models import PlaceResult, Location


class MapsService:
    def __init__(self):
        self.gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))
    
    async def geocode_location(self, location_name: str) -> Optional[Location]:
        """
        Convert location name to coordinates
        """
        try:
            geocode_result = self.gmaps.geocode(location_name)
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return Location(
                    lat=location['lat'],
                    lng=location['lng'],
                    address=geocode_result[0]['formatted_address']
                )
        except Exception as e:
            print(f"Error geocoding {location_name}: {e}")
        return None
    
    async def calculate_midpoint(self, location1: Location, location2: Location) -> Location:
        """
        Calculate midpoint between two locations
        """
        mid_lat = (location1.lat + location2.lat) / 2
        mid_lng = (location1.lng + location2.lng) / 2
        
        # Reverse geocode to get address
        try:
            reverse_result = self.gmaps.reverse_geocode((mid_lat, mid_lng))
            address = reverse_result[0]['formatted_address'] if reverse_result else "Midpoint Location"
        except:
            address = "Midpoint Location"
        
        return Location(lat=mid_lat, lng=mid_lng, address=address)
    
    async def search_places(self, 
                          place_type: str, 
                          location: Location, 
                          radius: int = 5000,
                          constraints: List[Dict[str, Any]] = None) -> List[PlaceResult]:
        """
        Search for places using Google Places API
        """
        try:
            # Build the search query
            query = place_type
            
            # Add constraints to query if they affect search terms
            if constraints:
                for constraint in constraints:
                    if constraint.get("type") == "quiet" and constraint.get("value"):
                        query += " quiet"
                    elif constraint.get("type") == "open_late" and constraint.get("value"):
                        query += " open late"
            
            # Perform text search
            places_result = self.gmaps.places(
                query=query,
                location=(location.lat, location.lng),
                radius=radius,
                type='establishment'
            )
            
            results = []
            for place in places_result.get('results', [])[:10]:  # Limit to 10 results
                # Get detailed information
                place_details = self._get_place_details(place['place_id'])
                
                # Calculate distance from search location
                distance = self._calculate_distance(
                    location.lat, location.lng,
                    place['geometry']['location']['lat'],
                    place['geometry']['location']['lng']
                )
                
                result = PlaceResult(
                    name=place.get('name', 'Unknown'),
                    place_id=place['place_id'],
                    address=place.get('formatted_address', 'Address not available'),
                    rating=place.get('rating'),
                    price_level=place.get('price_level'),
                    opening_hours=place_details.get('opening_hours', {}),
                    photos=place_details.get('photos', []),
                    distance_from_midpoint=distance,
                    distance_text=self._format_distance(distance),
                    types=place.get('types', [])
                )
                
                # Apply constraints filtering
                if self._meets_constraints(result, constraints or []):
                    results.append(result)
            
            # Sort by rating and distance
            results.sort(key=lambda x: (
                -(x.rating or 0),  # Higher rating first
                x.distance_from_midpoint or float('inf')  # Closer first
            ))
            
            return results[:3]  # Return top 3 results
            
        except Exception as e:
            print(f"Error searching places: {e}")
            return []
    
    def _get_place_details(self, place_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a place
        """
        try:
            details = self.gmaps.place(
                place_id=place_id,
                fields=['opening_hours', 'photos', 'reviews']
            )
            return details.get('result', {})
        except Exception as e:
            print(f"Error getting place details for {place_id}: {e}")
            return {}
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Calculate distance between two points using Haversine formula
        """
        import math
        
        R = 6371000  # Earth's radius in meters
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def _format_distance(self, distance_meters: float) -> str:
        """
        Format distance in a human-readable way
        """
        if distance_meters < 1000:
            return f"{int(distance_meters)}m"
        else:
            return f"{distance_meters/1000:.1f}km"
    
    def _meets_constraints(self, place: PlaceResult, constraints: List[Dict[str, Any]]) -> bool:
        """
        Check if a place meets the specified constraints
        """
        for constraint in constraints:
            constraint_type = constraint.get("type")
            constraint_value = constraint.get("value")
            
            if constraint_type == "rating_min" and place.rating:
                if place.rating < constraint_value:
                    return False
            
            elif constraint_type == "parking" and constraint_value:
                # This is a simplified check - in production you'd analyze place details
                if "parking" not in place.types and "parking" not in place.name.lower():
                    return False
            
            elif constraint_type == "price_range" and place.price_level:
                if place.price_level > constraint_value:
                    return False
        
        return True
    
    def get_directions_url(self, destination_place_id: str, origin: str = None) -> str:
        """
        Generate Google Maps directions URL
        """
        base_url = "https://www.google.com/maps/dir/"
        if origin:
            return f"{base_url}{origin.replace(' ', '+')}/{destination_place_id}"
        else:
            return f"{base_url}{destination_place_id}"
    
    def get_embed_map_url(self, place_id: str) -> str:
        """
        Generate Google Maps embed URL
        """
        return f"https://www.google.com/maps/embed/v1/place?key={os.getenv('GOOGLE_MAPS_API_KEY')}&place_id={place_id}"
