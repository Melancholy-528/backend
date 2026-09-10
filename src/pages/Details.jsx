import { useState } from "react";
import { matchSchemes } from "../services/api";
import "../styles/Details.css";

function Details({ onOpenChat, onOpenBanks })  {
  const [formData, setFormData] = useState({
    category: "",
    annual_income: "",
    project_cost: "",
    age: "",
    gender: "",
    occupation: "",
    state: "",
    district: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await matchSchemes({
        ...formData,
        annual_income: Number(formData.annual_income),
        project_cost: Number(formData.project_cost),
        age: Number(formData.age),
      });

      setResult(data);
    } catch (err) {
      setError("Unable to fetch schemes. Please check your backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="details-page">

      <div className="details-header">
        <div>
          <h1>Find Your Schemes</h1>
          <p>
            Enter your details and UdyamSetu AI will find suitable
            government schemes for you.
          </p>
        </div>

        <div className="scheme-logo">
          <span>SS</span>
          <div>
            <strong>UdyamSetu</strong>
            <small>AI</small>
          </div>
        </div>
      </div>

      <div className="details-container">

        <div className="form-card">
          <h2>Your Details</h2>
          <p className="form-subtitle">
            Fill in the information below
          </p>

          <form onSubmit={handleSubmit}>

            <div className="form-grid">

              <div className="input-group">
                <label>Category</label>
                <select
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select Category</option>
                  <option value="SC">SC</option>
                  <option value="ST">ST</option>
                  <option value="OBC">OBC</option>
                  <option value="Women">Women</option>
                  <option value="Minority">Minority</option>
                  <option value="Artisan">Artisan</option>
                  <option value="PwD">PwD</option>
                </select>
              </div>

              <div className="input-group">
                <label>Age</label>
                <input
                  name="age"
                  type="number"
                  placeholder="Enter your age"
                  value={formData.age}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="input-group">
                <label>Annual Income</label>
                <input
                  name="annual_income"
                  type="number"
                  placeholder="₹ Annual income"
                  value={formData.annual_income}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="input-group">
                <label>Project Cost</label>
                <input
                  name="project_cost"
                  type="number"
                  placeholder="₹ Project cost"
                  value={formData.project_cost}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="input-group">
                <label>Gender</label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div className="input-group">
                <label>Occupation</label>
                <input
                  name="occupation"
                  type="text"
                  placeholder="e.g. Farmer, Artisan"
                  value={formData.occupation}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="input-group">
                <label>State</label>
                <input
                  name="state"
                  type="text"
                  placeholder="Enter your state"
                  value={formData.state}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="input-group">
                <label>District</label>
                <input
                  name="district"
                  type="text"
                  placeholder="Enter your district"
                  value={formData.district}
                  onChange={handleChange}
                  required
                />
              </div>

            </div>

            <button
              className="find-button"
              type="submit"
              disabled={loading}
            >
              {loading ? "Finding Schemes..." : "Find Suitable Schemes →"}
            </button>

          </form>
        </div>

        {error && (
          <div className="error-box">
            {error}
          </div>
        )}

       {result && (
  <div className="results-card">
    <div className="results-heading">
      <div>
        <span className="results-label">AI MATCHING RESULTS</span>
        <h2>Schemes You May Be Eligible For</h2>
        <p>
          Based on the information you provided, UdyamSetu AI
          found these relevant schemes.
        </p>
      </div>

      <div className="match-badge">
        ✓ AI Matched
      </div>
    </div>

    <div className="scheme-cards">
      {(Array.isArray(result) ? result : result.matches || result.schemes || []).map(
        (scheme, index) => (
          <div className="scheme-card" key={index}>

            <div className="scheme-card-top">
              <div className="scheme-icon">
                {index + 1}
              </div>
              <button
  className="chat-navigation-button"
  onClick={onOpenChat}
>
  💬 Ask UdyamSetu AI
</button>
<button
  className="chat-navigation-button"
  onClick={onOpenBanks}
>
  🏦 Find Nearby Banks
</button>

              <div className="scheme-title">
                <h3>
                  {scheme.name || scheme.scheme_name || "Government Scheme"}
                </h3>

                {scheme.scheme_code && (
                  <span>
                    Scheme Code: {scheme.scheme_code}
                  </span>
                )}
              </div>
            </div>

            {scheme.description && (
              <p className="scheme-description">
                {scheme.description}
              </p>
            )}

            <div className="scheme-info">

              {scheme.subsidy_percentage !== undefined && (
                <div className="info-box">
                  <span>Subsidy</span>
                  <strong>
                    {scheme.subsidy_percentage}%
                  </strong>
                </div>
              )}

              {scheme.max_project_cost !== undefined && (
                <div className="info-box">
                  <span>Max Project Cost</span>
                  <strong>
                    ₹{Number(scheme.max_project_cost).toLocaleString("en-IN")}
                  </strong>
                </div>
              )}

              {scheme.income_limit !== undefined && (
                <div className="info-box">
                  <span>Income Limit</span>
                  <strong>
                    ₹{Number(scheme.income_limit).toLocaleString("en-IN")}
                  </strong>
                </div>
              )}

            </div>

            {scheme.benefits && scheme.benefits.length > 0 && (
              <div className="benefits-section">
                <h4>Key Benefits</h4>

                <ul>
                  {scheme.benefits.map((benefit, i) => (
                    <li key={i}>
                      <span>✓</span>
                      {benefit}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="scheme-card-bottom">

              {scheme.min_age || scheme.max_age ? (
                <span className="eligibility">
                  Age: {scheme.min_age || 0}
                  {scheme.max_age
                    ? ` – ${scheme.max_age}`
                    : "+"}
                </span>
              ) : (
                <span className="eligibility">
                  Eligibility matched
                </span>
              )}

              {scheme.source_url && (
                <a
                  href={scheme.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="apply-button"
                >
                  View Scheme →
                </a>
              )}

            </div>

          </div>
        )
      )}
    </div>
  </div>
)}
      </div>
    </div>
  );
}

export default Details;