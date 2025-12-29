import { useState } from "react";

export default function TripForm({ onPlan }) {
  const [city, setCity] = useState("");
  const [days, setDays] = useState(1);

  const handleSubmit = (e) => {
    e.preventDefault();
    onPlan(city, days);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Plan Your Trip</h2>

      <input
        type="text"
        placeholder="Enter city"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        required
      />

      <input
        type="number"
        min="1"
        value={days}
        onChange={(e) => setDays(e.target.value)}
        required
      />

      <button type="submit">Generate Itinerary</button>
    </form>
  );
}
