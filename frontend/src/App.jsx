import { useState } from "react";
import Itinerary from "./components/Itinerary";
import Budget from "./components/Budget";
import "./App.css";

function App() {
  const [city, setCity] = useState("");
  const [days, setDays] = useState(1);
  const [itinerary, setItinerary] = useState([]);
  const [loading, setLoading] = useState(false);
  const [budget, setBudget] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  const fetchTrip = async () => {
    setHasSearched(true); // 👈 IMPORTANT
    setLoading(true);
    setItinerary([]);
    setBudget(null);
    try {
      const res = await fetch("http://127.0.0.1:8000/plan-trip", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          destination: city,
          days: Number(days),
        }),
      });

      const data = await res.json();

      console.log("API response:", data);

      if (data.itinerary) {
        setItinerary(data.itinerary);
      }
      if (data.budget) {
        setBudget(data.budget);
      }
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>Travel Planner</h1>
        <div className="entry">
          <input
            placeholder="Enter city"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />

          <input
            placeholder="No.of days"
            type="number"
            min="1"
            value={days}
            onChange={(e) => setDays(e.target.value)}
          />

          <button onClick={fetchTrip} className="planTrip-button">
            Plan Trip
          </button>
        </div>
      </div>
      {loading && <p className="load">Loading...</p>}
      <div className="container">
        {!loading && hasSearched && <Itinerary itinerary={itinerary} />}
        {!loading && hasSearched && <Budget budget={budget} />}
      </div>
    </div>
  );
}

export default App;
