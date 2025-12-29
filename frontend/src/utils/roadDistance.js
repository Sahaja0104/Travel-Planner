export async function getRoadDistance(lat1, lon1, lat2, lon2) {
  const url = `https://router.project-osrm.org/route/v1/driving/${lon1},${lat1};${lon2},${lat2}?overview=false`;

  try {
    const res = await fetch(url);
    const data = await res.json();

    if (data.routes && data.routes.length > 0) {
      // meters → km
      return data.routes[0].distance / 1000;
    }
  } catch (err) {
    console.error("OSRM error", err);
  }

  return null;
}
