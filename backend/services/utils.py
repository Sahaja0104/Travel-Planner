from math import radians, sin, cos, sqrt, atan2

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return 2 * R * atan2(sqrt(a), sqrt(1 - a))

def cluster_center(attractions):
    if not attractions:
        return None, None

    lat = sum(a["lat"] for a in attractions) / len(attractions)
    lon = sum(a["lon"] for a in attractions) / len(attractions)
    return lat, lon
