export function haversineDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // km
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;

  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) ** 2;

  return 2 * R * Math.asin(Math.sqrt(a));
}

export function calculateDayDistance(attractions) {
  let total = 0;

  for (let i = 0; i < attractions.length - 1; i++) {
    total += haversineDistance(
      attractions[i].lat,
      attractions[i].lon,
      attractions[i + 1].lat,
      attractions[i + 1].lon
    );
  }

  return total; // km
}

export function estimateTravelTime(distanceKm) {
  const AVG_SPEED = 25; // km/h
  return (distanceKm / AVG_SPEED) * 60; // minutes
}
