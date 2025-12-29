// src/api.js
export async function planTrip(destination, days) {
  const response = await fetch("http://127.0.0.1:8000/plan-trip", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ destination, days }),
  });

  if (!response.ok) {
    throw new Error("Failed to plan trip");
  }

  return response.json();
}
