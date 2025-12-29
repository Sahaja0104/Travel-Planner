from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from services.geocode import get_coordinates
from services.weather import get_weather
from services.attractions import get_attractions
from services.hotels import get_hotels
from services.itinerary import distribute_clusters_to_days
from services.itinerary import cluster_places_with_time_limit
from services.budget import calculate_budget
from services.utils import cluster_center

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripRequest(BaseModel):
    destination: str
    days: int

@app.post("/plan-trip")
def plan_trip(req: TripRequest):
    lat, lon = get_coordinates(req.destination)
    if not lat:
        return {"error": "City not found"}

    # REAL attractions
    attractions = get_attractions(lat, lon, req.days * 5)

    if not attractions:
        return {"error": "No attractions found"}

    # Cluster by ROAD distance
    # clusters = cluster_places(attractions)
    clusters = cluster_places_with_time_limit(attractions)
 
    # Assign clusters to days
    itinerary_by_day = distribute_clusters_to_days(clusters, req.days)

    itinerary = []
    for day_data in itinerary_by_day:
        day_attractions = day_data["attractions"]
        c_lat, c_lon = cluster_center(day_attractions)
        hotels = []
        if c_lat and c_lon:
            hotels = get_hotels(c_lat, c_lon, day_attractions)
        itinerary.append({
            "day": day_data["day"],
            "weather": get_weather(lat, lon),
            "attractions": day_attractions,
            "hotels": hotels
        })

    budget = calculate_budget(req.days, hotels)

    return {
        "destination": req.destination,
        "days": req.days,
        "itinerary": itinerary,
        "budget": budget
    }
