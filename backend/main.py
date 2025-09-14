import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Import our services
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.llm_parser import LLMParser
from services.maps_service import MapsService
from services.mock_maps_service import MockMapsService
from services.models import ParsedQuery, Location

app = FastAPI(title="Intent-Based Maps Search API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services - use mock service for demo
llm_parser = LLMParser()
maps_service = MockMapsService()  # Using mock service for demo


class SearchRequest(BaseModel):
    query: str


class SearchResponse(BaseModel):
    query: str
    parsed_query: ParsedQuery
    results: List[dict]
    midpoint: Optional[dict]
    execution_time: float
    success: bool
    error_message: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Intent-Based Maps Search API is running!"}


@app.post("/search", response_model=SearchResponse)
async def search_places(request: SearchRequest):
    """
    Main search endpoint that processes natural language queries
    """
    start_time = time.time()
    
    try:
        # Parse the natural language query
        parsed_query = await llm_parser.parse_query(request.query)
        
        if not parsed_query.locations:
            raise HTTPException(status_code=400, detail="No locations found in query")
        
        # Geocode all locations
        locations = []
        for location_name in parsed_query.locations:
            location = await maps_service.geocode_location(location_name)
            if location:
                locations.append(location)
            else:
                raise HTTPException(status_code=400, detail=f"Could not find location: {location_name}")
        
        # Calculate midpoint if requested and we have multiple locations
        search_location = None
        midpoint = None
        
        if parsed_query.midpoint_calculation and len(locations) >= 2:
            midpoint = await maps_service.calculate_midpoint(locations[0], locations[1])
            search_location = midpoint
        elif len(locations) == 1:
            search_location = locations[0]
        else:
            # Use first location as search center
            search_location = locations[0]
        
        # Search for places
        results = await maps_service.search_places(
            place_type=parsed_query.place_type,
            location=search_location,
            radius=parsed_query.radius,
            constraints=parsed_query.constraints
        )
        
        execution_time = time.time() - start_time
        
        return SearchResponse(
            query=request.query,
            parsed_query=parsed_query,
            results=[result.dict() for result in results],
            midpoint=midpoint.dict() if midpoint else None,
            execution_time=execution_time,
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        execution_time = time.time() - start_time
        return SearchResponse(
            query=request.query,
            parsed_query=ParsedQuery(place_type="", locations=[], constraints=[], midpoint_calculation=False),
            results=[],
            midpoint=None,
            execution_time=execution_time,
            success=False,
            error_message=str(e)
        )


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "timestamp": time.time()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
