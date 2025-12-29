import {
  MapContainer,
  TileLayer,
  Marker,
  Polyline,
  Popup,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect, useState } from "react";
import { getRoadDistance } from "../utils/roadDistance";
import { calculateDayDistance, estimateDayTime } from "../utils/dayStats";
import "../App.css";
export default function Itinerary({ itinerary, loading }) {
  const [showAttractions, setShowAttractions] = useState(true);
  const [showHotels, setShowHotels] = useState(true);
  const [roadDistances, setRoadDistances] = useState({});

  // Fetch road distances whenever itinerary changes
  useEffect(() => {
    async function fetchDistances() {
      const result = {};

      for (let d = 0; d < itinerary.length; d++) {
        const places = itinerary[d].attractions;
        result[d] = [];

        for (let i = 0; i < places.length - 1; i++) {
          const p1 = places[i];
          const p2 = places[i + 1];

          const dist = await getRoadDistance(p1.lat, p1.lon, p2.lat, p2.lon);

          result[d].push(dist);
        }
      }

      setRoadDistances(result);
    }

    if (itinerary && itinerary.length > 0) {
      fetchDistances();
    }
  }, [itinerary]);

  if (loading) {
    return null;
  }

  if (!itinerary || itinerary.length === 0) {
    return <p className="load">Please enter city</p>;
  }

  return (
    <div>
      {itinerary.map((day, dayIndex) => {
        const attractions = day.attractions;

        const center = [attractions[0].lat, attractions[0].lon];

        const routePoints = attractions.map((p) => [p.lat, p.lon]);
        const distance = calculateDayDistance(attractions);
        const time = estimateDayTime(attractions);

        return (
          <div key={dayIndex} className="day-card">
            <h2>Day {day.day}</h2>
            <p className="weather">
              <span className="font-semibold">Weather:</span>{" "}
              {day.weather.description} | Temp: {day.weather.temp || "N/A"}°C
            </p>

            {/* -------- Places list -------- */}
            <p>📍 Places: {attractions.length}</p>
            <button onClick={() => setShowAttractions(!showAttractions)}>
              {showAttractions ? "Hide Attractions" : "Show Attractions"}
            </button>
            {showAttractions && (
              <ul>
                {day.attractions.map((place, idx) => (
                  <li key={idx}>
                    <span className="font-semibold">{place.name}</span> -{" "}
                    {place.address}
                  </li>
                ))}
              </ul>
            )}
            <p>🚗 Approx Distance: {distance} km</p>
            <p>⏱ Estimated Visit Time: {time} mins</p>

            {time > 480 && (
              <p style={{ color: "red" }}>⚠️ Too many places for one day</p>
            )}

            {/* -------- Map -------- */}
            <MapContainer
              center={center}
              zoom={13}
              style={{ height: "300px", width: "100%" }}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="© OpenStreetMap contributors"
              />

              {attractions.map((place, i) => (
                <Marker key={i} position={[place.lat, place.lon]}>
                  <Popup>
                    <b>{place.name}</b>
                  </Popup>
                </Marker>
              ))}

              <Polyline positions={routePoints} />
            </MapContainer>

            {/* -------- Road distances -------- */}
            {roadDistances[dayIndex] && (
              <div className="routes">
                <b>🚘 Road Travel</b>
                {attractions.map((place, i) => {
                  if (i === attractions.length - 1) return null;
                  const dist = roadDistances[dayIndex][i];

                  return (
                    <div key={i} className="route-row">
                      {place.name} → {attractions[i + 1].name} :{" "}
                      <b>{dist ? dist.toFixed(1) : "..."} km</b>
                    </div>
                  );
                })}
              </div>
            )}
            <button onClick={() => setShowHotels(!showHotels)}>
              {showHotels ? "Hide Hotels" : "Show Hotels"}
            </button>
            {showHotels && (
              <ul>
                {day.hotels.map((hotel, idx) => (
                  <li key={idx}>
                    <span className="font-semibold">{hotel.name}</span> -{" "}
                    {hotel.address} - ₹{hotel.price_per_night}
                  </li>
                ))}
              </ul>
            )}
          </div>
        );
      })}
    </div>
  );
}
