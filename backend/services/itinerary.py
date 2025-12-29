from services.osrm import get_road_distance

AVG_SPEED_KMH = 25
AVG_VISIT_TIME_MIN = 45
MAX_DAY_TIME_MIN = 360  # 6 hours

def travel_time_minutes(lat1, lon1, lat2, lon2):
    dist_m = get_road_distance(lat1, lon1, lat2, lon2)
    if not dist_m:
        return 0
    dist_km = dist_m / 1000
    return (dist_km / AVG_SPEED_KMH) * 60

def cluster_places_with_time_limit(places):
    """
    Multi-start clustering:
    - Builds a route
    - Stops when time exceeds daily limit
    - Starts a new cluster automatically
    """
    if not places:
        return []

    unvisited = places[:]
    clusters = []

    while unvisited:
        cluster = []
        total_time = 0

        # start new cluster
        current = unvisited.pop(0)
        cluster.append(current)
        total_time += AVG_VISIT_TIME_MIN

        while unvisited:
            last = cluster[-1]

            # choose nearest next place
            next_place = min(
                unvisited,
                key=lambda p: get_road_distance(
                    last["lat"], last["lon"], p["lat"], p["lon"]
                ) or float("inf")
            )

            travel_time = travel_time_minutes(
                last["lat"], last["lon"],
                next_place["lat"], next_place["lon"]
            )

            projected_time = total_time + travel_time + AVG_VISIT_TIME_MIN

            # ❌ Exceeds daily limit → stop cluster
            if projected_time > MAX_DAY_TIME_MIN:
                break

            # ✅ Add place
            cluster.append(next_place)
            total_time = projected_time
            unvisited.remove(next_place)

        clusters.append(cluster)

    return clusters

def optimize_day_route(places):
    if not places:
        return []

    unvisited = places[:]
    route = [unvisited.pop(0)]

    while unvisited:
        last = route[-1]
        next_place = min(
            unvisited,
            key=lambda p: get_road_distance(
                last["lat"], last["lon"], p["lat"], p["lon"]
            ) or float("inf")
        )
        route.append(next_place)
        unvisited.remove(next_place)

    return route

def distribute_clusters_to_days(clusters, days):
    itinerary_by_day = []

    for i in range(days):
        day_clusters = clusters[i::days]
        day_places = [p for c in day_clusters for p in c]

        itinerary_by_day.append({
            "day": i + 1,
            "attractions": optimize_day_route(day_places)
        })

    return itinerary_by_day
