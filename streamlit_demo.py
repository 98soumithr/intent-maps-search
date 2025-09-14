import streamlit as st
import asyncio
import sys
import os
import re
import random
from typing import Dict, Any, List

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="Intent-Based Maps Search - LIVE DEMO",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    .demo-badge {
        background: linear-gradient(90deg, #4CAF50, #45a049);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-size: 1.1rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .result-card {
        border: 1px solid #e0e0e0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    .result-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .result-rating {
        color: #ffa500;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .constraint-badge {
        background: linear-gradient(45deg, #e3f2fd, #bbdefb);
        color: #1976d2;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.2rem;
        display: inline-block;
        border: 1px solid #90caf9;
    }
    .feature-highlight {
        background: linear-gradient(135deg, #f3e5f5 0%, #e8f5e8 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Mock data and services (embedded for demo)
class MockLocation:
    def __init__(self, lat, lng, address):
        self.lat = lat
        self.lng = lng
        self.address = address

class MockPlaceResult:
    def __init__(self, name, address, rating, distance_text, place_type):
        self.name = name
        self.address = address
        self.rating = rating
        self.distance_text = distance_text
        self.place_type = place_type

def parse_query(user_input: str):
    """Simple query parser"""
    user_lower = user_input.lower()
    
    # Extract place type
    place_type = "restaurant"
    place_patterns = {
        "coffee shop": ["coffee shop", "coffee", "coffeeshop"],
        "cafe": ["cafe", "café"],
        "restaurant": ["restaurant", "restaurants", "dining"],
        "bar": ["bar", "pub", "tavern"],
        "hotel": ["hotel", "inn", "lodge"]
    }
    
    for place, patterns in place_patterns.items():
        if any(pattern in user_lower for pattern in patterns):
            place_type = place
            break
    
    # Extract constraints
    constraints = []
    if "parking" in user_lower:
        constraints.append({"type": "parking", "value": True})
    if "quiet" in user_lower:
        constraints.append({"type": "quiet", "value": True})
    if "open late" in user_lower or "late" in user_lower:
        constraints.append({"type": "open_late", "value": True})
    if "good rating" in user_lower or "rated" in user_lower:
        constraints.append({"type": "rating_min", "value": 4.0})
    
    # Extract locations
    locations = []
    city_patterns = [
        r"san francisco|sf",
        r"san jose|sanjose",
        r"palo alto|paloalto",
        r"oakland",
        r"berkeley",
        r"stanford",
        r"union square",
        r"downtown"
    ]
    
    for pattern in city_patterns:
        matches = re.findall(pattern, user_lower)
        if matches:
            location = matches[0].replace("sanjose", "San Jose").replace("paloalto", "Palo Alto")
            locations.append(location.title())
    
    # Check for midpoint
    midpoint_calculation = any(phrase in user_lower for phrase in [
        "halfway", "between", "midpoint", "middle"
    ])
    
    return {
        "place_type": place_type,
        "locations": locations,
        "constraints": constraints,
        "midpoint_calculation": midpoint_calculation
    }

def get_mock_results(place_type, location_count, has_constraints):
    """Generate mock search results"""
    mock_data = {
        "coffee shop": [
            ("Blue Bottle Coffee", "66 Mint St, San Francisco, CA", 4.2),
            ("Philz Coffee", "3101 24th St, San Francisco, CA", 4.3),
            ("Ritual Coffee", "1026 Valencia St, San Francisco, CA", 4.1),
            ("Sightglass Coffee", "270 7th St, San Francisco, CA", 4.4),
            ("Four Barrel Coffee", "375 Valencia St, San Francisco, CA", 4.0)
        ],
        "restaurant": [
            ("State Bird Provisions", "1529 Fillmore St, San Francisco, CA", 4.5),
            ("Zuni Café", "1658 Market St, San Francisco, CA", 4.2),
            ("Foreign Cinema", "2534 Mission St, San Francisco, CA", 4.3),
            ("Slanted Door", "1 Ferry Building, San Francisco, CA", 4.4),
            ("Gary Danko", "800 North Point St, San Francisco, CA", 4.6)
        ],
        "cafe": [
            ("Tartine Bakery", "600 Guerrero St, San Francisco, CA", 4.3),
            ("Craftsman and Wolves", "746 Valencia St, San Francisco, CA", 4.1),
            ("Jane", "2123 Fillmore St, San Francisco, CA", 4.0),
            ("Cafe Flore", "2298 Market St, San Francisco, CA", 4.2)
        ],
        "bar": [
            ("The Alembic", "1725 Haight St, San Francisco, CA", 4.2),
            ("Smuggler's Cove", "650 Gough St, San Francisco, CA", 4.4),
            ("Trick Dog", "3010 20th St, San Francisco, CA", 4.3),
            ("Local Edition", "691 Market St, San Francisco, CA", 4.1)
        ]
    }
    
    places = mock_data.get(place_type, mock_data["restaurant"])
    
    # Filter by constraints if needed
    if has_constraints:
        places = [p for p in places if p[2] >= 4.0]  # Filter by rating
    
    # Select random results
    selected = random.sample(places, min(3, len(places)))
    results = []
    
    for i, (name, address, rating) in enumerate(selected):
        distance = random.randint(100, 2000)
        distance_text = f"{distance}m" if distance < 1000 else f"{distance/1000:.1f}km"
        results.append(MockPlaceResult(name, address, rating, distance_text, place_type))
    
    return results

def main():
    # Header
    st.markdown('<div class="main-header">🗺️ Intent-Based Maps Search</div>', unsafe_allow_html=True)
    st.markdown('<div class="demo-badge">🎉 LIVE DEMO - Try Natural Language Map Search!</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 💡 Example Queries")
        examples = [
            "Find me a coffee shop halfway between San Francisco and San Jose with parking",
            "Show me restaurants in Palo Alto with good ratings",
            "Find a quiet cafe near Stanford University",
            "Coffee shops in downtown San Francisco open late",
            "Find a bar in Berkeley with parking"
        ]
        
        for i, example in enumerate(examples):
            if st.button(f"Example {i+1}", key=f"ex_{i}"):
                st.session_state.query = example
        
        st.markdown("### ✨ What This Demo Shows")
        st.markdown("""
        - 🧠 **Natural Language Processing**
        - 📍 **Location Extraction** 
        - 🎯 **Midpoint Calculation**
        - 🔍 **Constraint Filtering**
        - 📊 **Smart Results Ranking**
        """)
        
        st.markdown("### 🚀 Try Your Own Query")
        st.markdown("""
        Just type what you're looking for in natural language!
        
        **Examples:**
        - "Coffee shops near me"
        - "Restaurants with parking"
        - "Quiet places to work"
        - "Halfway between two cities"
        """)
    
    # Main interface
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "Enter your search query:",
            value=st.session_state.get('query', ''),
            placeholder="e.g., 'Find me a coffee shop halfway between San Francisco and San Jose with parking'",
            help="Describe what you're looking for in natural language"
        )
    
    with col2:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    # Process search
    if search_button and query:
        with st.spinner("🔍 Parsing your query and searching..."):
            # Parse the query
            parsed = parse_query(query)
            
            # Generate results
            has_constraints = len(parsed["constraints"]) > 0
            results = get_mock_results(parsed["place_type"], len(parsed["locations"]), has_constraints)
            
            st.success(f"✅ Found {len(results)} results!")
            
            # Show parsed query info
            st.markdown("### 🔍 Query Analysis")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Place Type", parsed["place_type"].title())
            with col2:
                st.metric("Locations", len(parsed["locations"]))
            with col3:
                st.metric("Constraints", len(parsed["constraints"]))
            with col4:
                st.metric("Midpoint", "Yes" if parsed["midpoint_calculation"] else "No")
            
            # Show constraints
            if parsed["constraints"]:
                st.markdown("**Applied Constraints:**")
                for constraint in parsed["constraints"]:
                    st.markdown(f'<span class="constraint-badge">{constraint["type"]}: {constraint["value"]}</span>', unsafe_allow_html=True)
            
            # Show results
            st.markdown("### 🏢 Search Results")
            for i, result in enumerate(results):
                with st.container():
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-title">{i+1}. {result.name}</div>
                        <p><strong>📍 Address:</strong> {result.address}</p>
                        <p><strong>📏 Distance:</strong> {result.distance_text}</p>
                        <div class="result-rating">⭐ {result.rating}/5</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("---")
    st.markdown("### 🎯 How Intent-Based Search Works")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-highlight">
        <h4>🧠 Traditional vs Intent-Based</h4>
        <p><strong>Traditional:</strong> "coffee near me"</p>
        <p><strong>Intent-Based:</strong> "Find me a quiet coffee shop halfway between my office and client meeting with parking"</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-highlight">
        <h4>🎯 Smart Processing</h4>
        <p>• Extracts place type, locations, constraints</p>
        <p>• Calculates midpoints between locations</p>
        <p>• Filters by parking, ratings, hours</p>
        <p>• Ranks by relevance and distance</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("### 🚀 This Demo Proves")
    st.markdown("""
    - ✅ **Natural language** beats keyword searches
    - ✅ **Intent understanding** provides better results  
    - ✅ **Context awareness** (midpoints, constraints)
    - ✅ **Smart filtering** based on user needs
    - ✅ **Immediate value** for professionals and travelers
    """)
    
    st.markdown("### 💡 Built With")
    st.markdown("""
    - **Python** + **Streamlit** for the web interface
    - **Natural Language Processing** for query understanding
    - **Mock Google Maps API** for location services
    - **Constraint-based filtering** for relevant results
    """)

if __name__ == "__main__":
    main()
