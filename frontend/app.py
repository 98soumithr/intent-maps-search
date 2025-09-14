import streamlit as st
import requests
import json
from typing import Dict, List, Optional
import time

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="Intent-Based Maps Search",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
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
    .constraint-badge {
        background-color: #e1f5fe;
        color: #0277bd;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .parsed-query {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def search_places(query: str) -> Optional[Dict]:
    """
    Call the backend API to search for places
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/search",
            json={"query": query},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

def display_result(result: Dict, index: int):
    """
    Display a single search result
    """
    with st.container():
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">{index + 1}. {result['name']}</div>
            <p><strong>Address:</strong> {result['address']}</p>
            <p><strong>Distance:</strong> {result.get('distance_text', 'N/A')}</p>
        """, unsafe_allow_html=True)
        
        # Rating and price level
        col1, col2 = st.columns(2)
        with col1:
            if result.get('rating'):
                st.markdown(f"<div class='result-rating'>⭐ {result['rating']}/5</div>", unsafe_allow_html=True)
        
        with col2:
            if result.get('price_level'):
                price_symbols = "💰" * result['price_level']
                st.markdown(f"**Price:** {price_symbols}")
        
        # Opening hours
        if result.get('opening_hours') and result['opening_hours'].get('weekday_text'):
            with st.expander("Opening Hours"):
                for hours in result['opening_hours']['weekday_text']:
                    st.text(hours)
        
        # Get directions button
        if result.get('place_id'):
            directions_url = f"https://www.google.com/maps/place/?q=place_id:{result['place_id']}"
            st.markdown(f"[Get Directions]({directions_url})")
        
        st.markdown("</div>", unsafe_allow_html=True)

def display_parsed_query(parsed_query: Dict):
    """
    Display the parsed query information
    """
    st.markdown("### 🔍 Query Analysis")
    st.markdown(f"""
    <div class="parsed-query">
        <p><strong>Place Type:</strong> {parsed_query.get('place_type', 'N/A')}</p>
        <p><strong>Locations:</strong> {', '.join(parsed_query.get('locations', []))}</p>
        <p><strong>Midpoint Calculation:</strong> {'Yes' if parsed_query.get('midpoint_calculation') else 'No'}</p>
        <p><strong>Search Radius:</strong> {parsed_query.get('radius', 5000)} meters</p>
    """, unsafe_allow_html=True)
    
    # Display constraints
    constraints = parsed_query.get('constraints', [])
    if constraints:
        st.markdown("**Constraints:**")
        for constraint in constraints:
            constraint_text = f"{constraint.get('type', 'unknown')}: {constraint.get('value', 'N/A')}"
            st.markdown(f"<span class='constraint-badge'>{constraint_text}</span>", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">🗺️ Intent-Based Maps Search</div>', unsafe_allow_html=True)
    st.markdown("### Search for places using natural language queries")
    
    # Sidebar with examples
    with st.sidebar:
        st.markdown("### 💡 Example Queries")
        example_queries = [
            "Find me a coffee shop halfway between San Francisco and San Jose with parking",
            "Show me quiet restaurants where I can finish a meeting in 45 minutes",
            "Find a vegan restaurant halfway between Palo Alto and Oakland that's open late",
            "Coffee shops near me with good WiFi",
            "Restaurants in downtown San Francisco with parking and open until 10 PM"
        ]
        
        for i, example in enumerate(example_queries):
            if st.button(f"Example {i+1}", key=f"example_{i}"):
                st.session_state.query = example
        
        st.markdown("### 🔧 Settings")
        st.markdown("**API Status:**")
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ Backend Connected")
            else:
                st.error("❌ Backend Error")
        except:
            st.error("❌ Backend Offline")
    
    # Main search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Enter your search query:",
            value=st.session_state.get('query', ''),
            placeholder="e.g., 'Find me a coffee shop halfway between San Francisco and San Jose with parking'",
            help="Describe what you're looking for in natural language"
        )
    
    with col2:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    # Perform search
    if search_button and query:
        with st.spinner("Searching for places..."):
            start_time = time.time()
            result = search_places(query)
            
            if result:
                if result.get('success', False):
                    # Display execution time
                    st.success(f"✅ Search completed in {result['execution_time']:.2f} seconds")
                    
                    # Display parsed query
                    display_parsed_query(result.get('parsed_query', {}))
                    
                    # Display midpoint if calculated
                    if result.get('midpoint'):
                        st.markdown("### 📍 Calculated Midpoint")
                        midpoint = result['midpoint']
                        st.info(f"**Location:** {midpoint.get('address', 'N/A')}")
                        st.map({
                            'lat': [midpoint.get('lat')],
                            'lon': [midpoint.get('lng')]
                        })
                    
                    # Display results
                    results = result.get('results', [])
                    if results:
                        st.markdown("### 🏢 Search Results")
                        for i, place_result in enumerate(results):
                            display_result(place_result, i)
                    else:
                        st.warning("No places found matching your criteria. Try adjusting your search.")
                
                else:
                    st.error(f"❌ Search failed: {result.get('error_message', 'Unknown error')}")
    
    # Footer
    st.markdown("---")
    st.markdown("### 📖 How to Use")
    st.markdown("""
    1. **Enter a natural language query** describing what you're looking for
    2. **Include location details** like city names or "near me"
    3. **Add constraints** like "with parking", "quiet", "open late", etc.
    4. **Use "halfway between"** to find places between two locations
    5. **Click Search** to get personalized results
    """)
    
    st.markdown("### 🎯 Supported Features")
    st.markdown("""
    - **Natural Language Processing**: Describe what you want in plain English
    - **Midpoint Calculation**: Find places halfway between two locations
    - **Constraint Filtering**: Filter by parking, ratings, hours, etc.
    - **Real-time Results**: Get instant results with ratings and directions
    """)

if __name__ == "__main__":
    main()
