# 🧪 Testing Guide - Intent-Based Maps Search MVP

## 🚀 Quick Start Testing

### Step 1: Setup Environment
```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env with your API keys
nano .env  # or use your preferred editor
```

Add your API keys to `.env`:
```
OPENAI_API_KEY=sk-your-actual-openai-key-here
GOOGLE_MAPS_API_KEY=your-actual-google-maps-key-here
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Setup
```bash
python quick_test.py
```

You should see:
```
✅ Environment variables configured
✅ OpenAI imported successfully  
✅ Google Maps imported successfully
✅ FastAPI imported successfully
✅ All required files present
🎉 Basic setup looks good!
```

## 🎯 Testing Methods

### Method 1: Automated Startup (Recommended)
```bash
python start.py
```

This will:
- Start the FastAPI backend on http://localhost:8000
- Start the Streamlit frontend on http://localhost:8501
- Open your browser automatically

### Method 2: Manual Component Testing

**Terminal 1 - Backend:**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
streamlit run frontend/app.py --server.port 8501
```

### Method 3: Command-Line Demo
```bash
python demo.py
```

This runs example queries without the UI for quick testing.

## 🧪 Test Cases to Try

### Basic Functionality Tests

1. **Simple Location Search**
   ```
   "Find restaurants in San Francisco"
   ```

2. **Midpoint Search**
   ```
   "Find a coffee shop halfway between San Francisco and San Jose"
   ```

3. **Constraint Search**
   ```
   "Find restaurants with parking in Palo Alto"
   ```

4. **Complex Query**
   ```
   "Find me a quiet cafe halfway between Stanford and San Jose that's open late"
   ```

### Edge Case Tests

1. **No Results**
   ```
   "Find a unicorn cafe on Mars"
   ```

2. **Invalid Location**
   ```
   "Find restaurants in NonExistentCity"
   ```

3. **Ambiguous Query**
   ```
   "Find food"
   ```

4. **Very Specific**
   ```
   "Find a vegan gluten-free coffee shop with outdoor seating and WiFi halfway between Berkeley and Oakland that's open until midnight"
   ```

## 🔍 Testing Checklist

### ✅ Backend API Tests

**Test 1: Health Check**
```bash
curl http://localhost:8000/health
```
Expected: `{"status": "healthy", "timestamp": 1234567890.123}`

**Test 2: Search Endpoint**
```bash
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "Find restaurants in San Francisco"}'
```
Expected: JSON response with parsed query and results

**Test 3: Error Handling**
```bash
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{"query": ""}'
```
Expected: Error response with helpful message

### ✅ Frontend UI Tests

**Test 1: Page Load**
- Visit http://localhost:8501
- Verify page loads with header "Intent-Based Maps Search"
- Check sidebar shows example queries

**Test 2: Example Queries**
- Click each example query button
- Verify text appears in search box
- Submit query and verify results appear

**Test 3: Custom Query**
- Type: "Find coffee shops in Berkeley"
- Click Search button
- Verify results show with ratings and addresses

**Test 4: Error Handling**
- Type: "Find restaurants on Mars"
- Click Search
- Verify appropriate error message

### ✅ Integration Tests

**Test 1: End-to-End Flow**
1. Open frontend
2. Enter: "Find a restaurant halfway between San Francisco and San Jose with parking"
3. Click Search
4. Verify:
   - Query is parsed correctly
   - Midpoint is calculated
   - Results show restaurants
   - Results include parking information
   - "Get Directions" links work

**Test 2: Performance**
- Time how long searches take
- Target: < 5 seconds for typical queries
- Test with multiple rapid searches

## 🐛 Common Issues & Solutions

### Issue: "OpenAI API key not configured"
**Solution:** Make sure you've added your actual OpenAI API key to `.env`

### Issue: "Google Maps API key not configured"  
**Solution:** Add your Google Maps API key to `.env` and enable required APIs

### Issue: "No results found"
**Solution:** Try simpler queries first, check if locations are spelled correctly

### Issue: Backend connection error
**Solution:** Make sure backend is running on port 8000

### Issue: Streamlit import errors
**Solution:** Try: `pip install --upgrade streamlit numpy pandas`

## 📊 Performance Benchmarks

### Expected Response Times
- **Simple queries**: 2-3 seconds
- **Complex queries with midpoint**: 3-5 seconds
- **Queries with many constraints**: 4-6 seconds

### Success Criteria
- ✅ 80%+ of natural language queries parse correctly
- ✅ < 5 second response time for typical searches
- ✅ Top 3 results are relevant to the query
- ✅ Error handling provides helpful messages

## 🎯 User Acceptance Testing

### Test Scenarios for End Users

**Scenario 1: Professional Meeting**
```
Query: "Find a quiet restaurant halfway between my office in Palo Alto and client in San Jose with parking for a business lunch"
Expected: Results show restaurants between the cities with parking info
```

**Scenario 2: Travel Planning**
```
Query: "Show me coffee shops near Union Square that are open late"
Expected: Results show cafes near Union Square with hours information
```

**Scenario 3: Group Coordination**
```
Query: "Find a place to meet halfway between Berkeley and Stanford that has good WiFi"
Expected: Results show venues between the two locations with WiFi amenities
```

## 🔧 Debugging Tools

### Backend Debugging
```bash
# Check backend logs
uvicorn backend.main:app --reload --log-level debug

# Test API directly
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "test query"}' | jq
```

### Frontend Debugging
```bash
# Run Streamlit in debug mode
streamlit run frontend/app.py --logger.level debug
```

### LLM Debugging
```bash
# Test LLM parser directly
python -c "
import asyncio
import sys, os
sys.path.append('.')
from services.llm_parser import LLMParser
async def test():
    parser = LLMParser()
    result = await parser.parse_query('Find restaurants in SF')
    print(result)
asyncio.run(test())
"
```

## 📈 Success Metrics

### Technical Metrics
- ✅ API response time < 5 seconds
- ✅ Query parsing accuracy > 80%
- ✅ Successful API calls > 95%
- ✅ Error rate < 5%

### User Experience Metrics
- ✅ Users can complete searches without help
- ✅ Results are relevant to the query
- ✅ Interface is intuitive and fast
- ✅ Error messages are helpful

## 🚀 Next Steps After Testing

Once testing is complete:

1. **Document Issues**: Note any bugs or improvements
2. **Performance Tuning**: Optimize slow queries
3. **User Feedback**: Get input from actual users
4. **Feature Enhancements**: Add requested functionality
5. **Deployment**: Deploy to cloud for public access

Happy testing! 🎉
