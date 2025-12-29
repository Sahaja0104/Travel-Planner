import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEOAPIFY_API_KEY")

def get_coordinates(city_name):
    url = "https://api.geoapify.com/v1/geocode/search"
    params = {
        "text": city_name,
        "format": "json",
        "limit": 1,
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = data.get("results")
    if results and len(results) > 0:
        lat = results[0]["lat"]
        lon = results[0]["lon"]
        return lat, lon

    return None, None