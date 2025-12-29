import requests

OSRM_SERVER = "http://router.project-osrm.org"  # public OSRM server

def get_road_distance(lat1, lon1, lat2, lon2):
    """
    Returns driving distance in meters between two points using OSRM.
    """
    url = f"{OSRM_SERVER}/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
    response = requests.get(url)
    data = response.json()
    
    if "routes" in data and len(data["routes"]) > 0:
        return data["routes"][0]["distance"]
    return None

def build_distance_matrix(places):
    """
    Returns a matrix of road distances between all places.
    """
    matrix = []
    for p1 in places:
        row = []
        for p2 in places:
            if p1 == p2:
                row.append(0)
            else:
                dist = get_road_distance(p1["lat"], p1["lon"], p2["lat"], p2["lon"])
                row.append(dist if dist else float("inf"))
        matrix.append(row)
    return matrix