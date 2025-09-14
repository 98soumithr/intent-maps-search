# Intent-Based Maps Search MVP - Setup Guide

## 🚀 Quick Start

### 1. Get API Keys

You'll need two API keys:

**OpenAI API Key:**
1. Go to https://platform.openai.com/
2. Sign up/login and create an API key
3. Make sure you have credits available

**Google Maps API Key:**
1. Go to https://developers.google.com/maps
2. Create a new project or select existing one
3. Enable these APIs:
   - Places API
   - Directions API
   - Maps Embed API
   - Geocoding API
4. Create credentials (API Key)
5. Restrict the key to your APIs (recommended for production)

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual API keys
nano .env
```

Your `.env` file should look like:
```
OPENAI_API_KEY=sk-your-actual-openai-key-here
GOOGLE_MAPS_API_KEY=your-actual-google-maps-key-here
API_HOST=0.0.0.0
API_PORT=8000
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Test Setup

```bash
python test_setup.py
```

This will verify that:
- ✅ Environment variables are configured
- ✅ All dependencies are installed
- ✅ Services can be instantiated

### 5. Run Demo (Optional)

```bash
python demo.py
```

This runs example queries to test the system without the UI.

### 6. Start the Application

```bash
python start.py
```

This will:
- Start the FastAPI backend on http://localhost:8000
- Start the Streamlit frontend on http://localhost:8501
- Open your browser automatically

## 🎯 Example Queries to Try

1. **"Find me a coffee shop halfway between San Francisco and San Jose with parking"**
2. **"Show me quiet restaurants where I can finish a meeting in 45 minutes"**
3. **"Find a vegan restaurant halfway between Palo Alto and Oakland that's open late"**
4. **"Coffee shops near me with good WiFi"**
5. **"Restaurants in downtown San Francisco with parking and open until 10 PM"**

## 🔧 Manual Start (Alternative)

If the startup script doesn't work, you can start components manually:

**Terminal 1 - Backend:**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
streamlit run frontend/app.py --server.port 8501
```

## 🐛 Troubleshooting

### Backend Connection Issues
- Make sure the backend is running on port 8000
- Check if the API keys are correctly set in `.env`
- Verify Google Maps APIs are enabled

### No Results Found
- Try simpler queries first
- Check if locations are spelled correctly
- Ensure Google Maps API has sufficient quota

### LLM Parsing Errors
- Verify OpenAI API key is valid
- Check if you have sufficient OpenAI credits
- Try rephrasing the query

## 📁 Project Structure

```
intent_maps_search/
├── backend/
│   ├── __init__.py
│   └── main.py              # FastAPI backend
├── frontend/
│   └── app.py               # Streamlit UI
├── services/
│   ├── __init__.py
│   ├── models.py            # Data models
│   ├── llm_parser.py        # OpenAI integration
│   └── maps_service.py      # Google Maps integration
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
├── start.py                # Startup script
├── demo.py                 # Demo script
├── test_setup.py           # Setup verification
└── README.md               # Project documentation
```

## 🚀 Next Steps

Once the MVP is working:

1. **Add more constraint types** (WiFi, outdoor seating, etc.)
2. **Implement voice input** using speech recognition
3. **Add review analysis** using LLM to summarize reviews
4. **Save and share searches** with one-click links
5. **Deploy to cloud** (Vercel, Render, or Heroku)

## 💡 Tips

- Start with simple queries to test the system
- The system works best with specific location names
- Use "halfway between" for midpoint calculations
- Add constraints like "with parking" or "quiet" for better filtering
