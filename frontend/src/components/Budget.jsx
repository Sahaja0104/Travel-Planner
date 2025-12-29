import "../App.css";

export default function Budget({ budget, loading }) {
  if (loading) {
    return null; // 👈 DO NOT SHOW ANYTHING
  }
  if (!budget) {
    return <p></p>;
  }

  return (
    <div className="budget-card">
      <h2>Estimated Budget</h2>

      <div className="budget-row">
        <span>🏨 Hotels: ₹{budget.hotel}</span>
      </div>

      <div className="budget-row">
        <span>🍽 Food: ₹{budget.food}</span>
      </div>

      <div className="budget-row">
        <span>🚕 Local Travel: ₹{budget.local_travel}</span>
      </div>

      <div className="budget-row">
        <span>🎟 Activities: ₹{budget.activities}</span>
      </div>

      <hr />

      <div className="budget-total">
        <strong>Estimated Total: ₹{budget.total}</strong>
      </div>
    </div>
  );
}
