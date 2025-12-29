import { haversineDistance } from "./distance";

export function calculateDayDistance(attractions) {
  if (!attractions || attractions.length < 2) return 0;

  let total = 0;
  for (let i = 0; i < attractions.length - 1; i++) {
    total += haversineDistance(
      attractions[i].lat,
      attractions[i].lon,
      attractions[i + 1].lat,
      attractions[i + 1].lon
    );
  }

  return total.toFixed(1); // km
}

export function estimateDayTime(attractions) {
  const VISIT_TIME = 90; // minutes per place
  return attractions.length * VISIT_TIME;
}
