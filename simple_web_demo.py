#!/usr/bin/env python3
"""
Simple Web Demo - Intent-Based Maps Search
Works without API keys using mock data
"""
import streamlit as st
import asyncio
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.llm_parser import LLMParser
from services.mock_maps_service import MockMapsService

# Page configuration
st.set_page_config(
    page_title="Intent-Based Maps Search - FREE DEMO",
    page_icon="🗺️",
    layout="wide"
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
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    .result-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #f9f9f9;
    }
    .result-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .result-rating {
        color: #ffa500;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_services():
    """Get the parser and maps service"""
    return LLMParser(), MockMapsService()

async def search_places(query: str):
    """Search for places using the mock service"""
    parser, maps_service = get_services()
    
    try:
        # Parse the query
        parsed = await parser.parse_query(query)
        
        # Get locations
        locations = []
        for loc_name in parsed.locations:
            location = await maps_service.geocode_location(loc_name)
            if location:
                locations.append(location)
        
        # Calculate midpoint if needed
        if parsed.midpoint_calculation and len(locations) >= 2:
            midpoint = await maps_service.calculate_midpoint(locations[0], locations[1])
            search_location = midpoint
        elif locations:
            search_location = locations[0]
        else:
            return None, "No valid locations found"
        
        # Search for places
        results = await maps_service.search_places(
            place_type=parsed.place_type,
            location=search_location,
            radius=parsed.radius,
            constraints=parsed.constraints
        )
        
        return results, parsed
        
    except Exception as e:
        return None, f"Error: {str(e)}"

def main():
    # Header
    st.markdown('<div class="main-header">🗺️ Intent-Based Maps Search</div>', unsafe_allow_html=True)
    st.markdown('<div class="demo-badge">🎉 FREE DEMO - No API Keys Required!</div>', unsafe_allow_html=True)
    
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
        
        st.markdown("### ✨ Features Demonstrated")
        st.markdown("""
        - 🧠 **Natural Language Parsing**
        - 📍 **Location Extraction**
        - 🎯 **Midpoint Calculation**
        - 🔍 **Constraint Filtering**
        - 📊 **Results Ranking**
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
        with st.spinner("Searching for places..."):
            # Run the async search
            results, parsed = asyncio.run(search_places(query))
            
            if results is None:
                st.error(f"❌ {parsed}")
            else:
                st.success(f"✅ Found {len(results)} results!")
                
                # Show parsed query info
                st.markdown("### 🔍 Query Analysis")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Place Type", parsed.place_type)
                with col2:
                    st.metric("Locations", len(parsed.locations))
                with col3:
                    st.metric("Constraints", len(parsed.constraints))
                
                # Show results
                st.markdown("### 🏢 Search Results")
                for i, result in enumerate(results):
                    with st.container():
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="result-title">{i+1}. {result.name}</div>
                            <p><strong>Address:</strong> {result.address}</p>
                            <p><strong>Distance:</strong> {result.distance_text}</p>
                            <div class="result-rating">⭐ {result.rating}/5</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show constraints if any
                        if parsed.constraints:
                            st.markdown("**Constraints Applied:**")
                            for constraint in parsed.constraints:
                                st.markdown(f"- {constraint['type']}: {constraint['value']}")
    
    # Footer
    st.markdown("---")
    st.markdown("### 🎯 How It Works")
    st.markdown("""
    1. **Natural Language Input**: Type what you want in plain English
    2. **Smart Parsing**: The system extracts place type, locations, and constraints
    3. **Location Processing**: Converts location names to coordinates
    4. **Midpoint Calculation**: Finds halfway points between locations
    5. **Place Search**: Searches for relevant places with mock data
    6. **Results Display**: Shows top results with ratings and distances
    """)
    
    st.markdown("### 🚀 This Demo Shows")
    st.markdown("""
    - ✅ **Intent-based search** instead of keyword matching
    - ✅ **Natural language processing** with local parsing
    - ✅ **Midpoint calculations** between locations
    - ✅ **Constraint filtering** (parking, ratings, etc.)
    - ✅ **Mock data integration** without API costs
    - ✅ **Modern web interface** with Streamlit
    """)

if __name__ == "__main__":
    main()
