# Intent-Based Maps Search MVP

A natural language interface for searching places with intelligent intent parsing and Google Maps integration.

## Features

- Natural language query parsing using OpenAI GPT
- Google Maps API integration (Places, Directions, Maps Embed)
- Midpoint calculation between locations
- Constraint-based filtering
- Simple Streamlit UI

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Get API keys:
- OpenAI API key from https://platform.openai.com/
- Google Maps API key from https://developers.google.com/maps

4. Run the application:
```bash
# Start FastAPI backend
uvicorn backend.main:app --reload

# In another terminal, start Streamlit frontend
streamlit run frontend/app.py
```

## Example Queries

- "Find me a coffee shop halfway between San Francisco and San Jose with parking"
- "Show me quiet restaurants where I can finish a meeting in 45 minutes"
- "Find a vegan restaurant halfway between Palo Alto and Oakland that's open late"
