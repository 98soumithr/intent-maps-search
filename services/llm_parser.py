import requests
import json
import os
import re
from typing import Dict, Any, List
from .models import ParsedQuery


class LLMParser:
    def __init__(self):
        # Use Hugging Face free API instead of OpenAI
        self.hf_api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        self.hf_token = os.getenv("HUGGINGFACE_TOKEN", "")  # Optional, works without token too
    
    async def parse_query(self, user_input: str) -> ParsedQuery:
        """
        Parse natural language query into structured data using free LLM or fallback
        """
        # Try free Hugging Face API first
        try:
            return await self._parse_with_hf_api(user_input)
        except Exception as e:
            print(f"HF API failed: {e}")
            # Fallback to improved local parsing
            return self._improved_fallback_parse(user_input)
    
    async def _parse_with_hf_api(self, user_input: str) -> ParsedQuery:
        """Try to use Hugging Face free API"""
        headers = {}
        if self.hf_token:
            headers["Authorization"] = f"Bearer {self.hf_token}"
        
        payload = {
            "inputs": f"Extract place type and locations from: {user_input}",
            "parameters": {"max_length": 100, "temperature": 0.1}
        }
        
        response = requests.post(self.hf_api_url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            # This is a simplified approach - HF API is more complex
            # For demo purposes, fall back to improved parsing
            return self._improved_fallback_parse(user_input)
        else:
            raise Exception(f"HF API error: {response.status_code}")
    
    def _improved_fallback_parse(self, user_input: str) -> ParsedQuery:
        """
        Improved fallback parsing using regex and keyword matching
        """
        user_lower = user_input.lower()
        
        # Extract place types with more comprehensive matching
        place_type = "restaurant"
        place_patterns = {
            "coffee shop": ["coffee shop", "coffee", "coffeeshop"],
            "cafe": ["cafe", "café"],
            "restaurant": ["restaurant", "restaurants", "dining"],
            "bar": ["bar", "pub", "tavern"],
            "hotel": ["hotel", "inn", "lodge"],
            "gas station": ["gas station", "gas", "fuel"],
            "pharmacy": ["pharmacy", "drugstore", "chemist"],
            "hospital": ["hospital", "medical center", "clinic"]
        }
        
        for place, patterns in place_patterns.items():
            if any(pattern in user_lower for pattern in patterns):
                place_type = place
                break
        
        # Extract constraints with more patterns
        constraints = []
        constraint_patterns = {
            "parking": ["parking", "park", "car"],
            "quiet": ["quiet", "silent", "peaceful", "calm"],
            "open_late": ["open late", "late", "until late", "night"],
            "wifi": ["wifi", "wifi", "internet", "wireless"],
            "rating_min": ["good rating", "high rating", "rated", "stars"]
        }
        
        for constraint_type, patterns in constraint_patterns.items():
            if any(pattern in user_lower for pattern in patterns):
                if constraint_type == "rating_min":
                    constraints.append({"type": "rating_min", "value": 4.0})
                else:
                    constraints.append({"type": constraint_type, "value": True})
        
        # Extract locations using regex patterns
        locations = []
        
        # Common city patterns
        city_patterns = [
            r"san francisco|sf",
            r"san jose|sanjose",
            r"palo alto|paloalto",
            r"oakland",
            r"berkeley",
            r"stanford",
            r"union square",
            r"downtown",
            r"mission district",
            r"castro district"
        ]
        
        for pattern in city_patterns:
            matches = re.findall(pattern, user_lower)
            if matches:
                # Clean up the match
                location = matches[0].replace("sanjose", "San Jose").replace("paloalto", "Palo Alto")
                locations.append(location.title())
        
        # Extract radius if mentioned
        radius = 5000  # default
        radius_match = re.search(r"within (\d+)\s*(km|miles?|meters?)", user_lower)
        if radius_match:
            value = int(radius_match.group(1))
            unit = radius_match.group(2)
            if "km" in unit or "mile" in unit:
                radius = value * 1000  # convert to meters
        
        # Determine if midpoint calculation is needed
        midpoint_calculation = any(phrase in user_lower for phrase in [
            "halfway", "between", "midpoint", "middle"
        ])
        
        return ParsedQuery(
            place_type=place_type,
            locations=locations,
            constraints=constraints,
            midpoint_calculation=midpoint_calculation,
            radius=radius
        )
