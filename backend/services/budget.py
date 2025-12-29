def calculate_budget(days: int, hotels: list):
    """
    Calculate estimated trip budget.
    """

    # ------------------------
    # Hotels
    # ------------------------
    if hotels:
        avg_hotel_price = sum(h["price_per_night"] for h in hotels) / len(hotels)
    else:
        avg_hotel_price = 2500  # fallback per night

    hotel_total = int(avg_hotel_price * days)

    # ------------------------
    # Food (per day per person)
    # ------------------------
    food_per_day = 1200
    food_total = food_per_day * days

    # ------------------------
    # Local travel (per day)
    # ------------------------
    travel_per_day = 1000
    travel_total = travel_per_day * days

    # ------------------------
    # Activities / entry fees
    # ------------------------
    activities_per_day = 700
    activities_total = activities_per_day * days

    # ------------------------
    # Final total
    # ------------------------
    total = hotel_total + food_total + travel_total + activities_total

    return {
        "hotel": hotel_total,
        "food": food_total,
        "local_travel": travel_total,
        "activities": activities_total,
        "total": total
    }
