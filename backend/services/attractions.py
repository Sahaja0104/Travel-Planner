import requests
import os

API_KEY = os.getenv("GEOAPIFY_API_KEY")

def get_attractions(lat, lon, limit):
    url = "https://api.geoapify.com/v2/places"

    params = {
        "categories": "tourism.attraction",
        "filter": f"circle:{lon},{lat},50000",
        "limit": limit,
        "apiKey": API_KEY
    }

    r = requests.get(url, params=params).json()

    attractions = []

    for f in r.get("features", []):
        p = f["properties"]
        attractions.append({
            "name": p.get("name", "Unknown"),
            "category": p.get("categories", []),
            "address": p.get("formatted", ""),
            "lat": p.get("lat"),
            "lon": p.get("lon")
        })

    return attractions
