import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
    try:
        res = requests.get(url, params=params).json()
        weather = {
            "temp": res.get("main", {}).get("temp"),
            "description": res.get("weather", [{}])[0].get("description"),
            "icon": res.get("weather", [{}])[0].get("icon")
        }
    except:
        weather = {"temp": None, "description": "N/A", "icon": None}
    return weather
