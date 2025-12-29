import os
import requests
from dotenv import load_dotenv
from services.utils import haversine_km

load_dotenv()
API_KEY = os.getenv("GEOAPIFY_API_KEY")


def estimate_price(hotel_name):
    # simple realistic heuristic
    name = hotel_name.lower() if hotel_name else ""
    if "resort" in name or "luxury" in name:
        return 5000
    if "inn" in name or "lodge" in name:
        return 2000
    return 3000


def get_hotels(lat, lon, attractions, radius_m=3000, limit=10):
    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": "accommodation.hotel",
        "filter": f"circle:{lon},{lat},{radius_m}",
        "limit": limit,
        "apiKey": API_KEY
    }

    res = requests.get(url, params=params, timeout=10)
    data = res.json()

    ranked_hotels = []

    for f in data.get("features", []):
        p = f["properties"]
        h_lat, h_lon = p.get("lat"), p.get("lon")
        name = p.get("name")

        # average distance to attractions
        distances = [
            haversine_km(h_lat, h_lon, a["lat"], a["lon"])
            for a in attractions
        ]
        avg_distance = sum(distances) / len(distances)

        price = estimate_price(name)

        # scoring
        distance_score = max(0, 1 - avg_distance / 10)  # 0–1
        price_score = max(0, 1 - price / 6000)          # 0–1
        quality_score = 0.6                              # placeholder realism

        score = (
            distance_score * 0.6 +
            price_score * 0.25 +
            quality_score * 0.15
        )

        ranked_hotels.append({
            "name": name,
            "address": p.get("formatted"),
            "lat": h_lat,
            "lon": h_lon,
            "avg_distance_km": round(avg_distance, 2),
            "price_per_night": price,
            "score": round(score, 3)
        })

    ranked_hotels.sort(key=lambda x: x["score"], reverse=True)
    return ranked_hotels[:5]
