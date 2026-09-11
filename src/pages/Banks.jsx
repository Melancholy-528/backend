import { useState } from "react";
import { getNearbyBanks } from "../services/api";
import "../styles/Banks.css";

function Banks() {
  const [formData, setFormData] = useState({
    scheme_code: "",
    state: "",
    district: "",
  });

  const [banks, setBanks] = useState(null);
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
    setBanks(null);

    try {
      const data = await getNearbyBanks(
        formData.scheme_code,
        formData.state,
        formData.district
      );

      setBanks(data);
    } catch (err) {
      console.error(err);
      setError(
        "Unable to find banks. Please check the scheme code, state and backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="banks-page">

      {/* HEADER */}
      <header className="banks-header">
        <div className="banks-brand">
          <div className="banks-logo">SS</div>

          <div>
            <h1>UdyamSetu AI</h1>
            <p>Bank Recommendation</p>
          </div>
        </div>

        <div className="bank-status">
          <span></span>
          Bank Network
        </div>
      </header>

      {/* MAIN */}
      <main className="banks-container">

        {/* INTRO */}
        <section className="banks-intro">
          <div className="intro-icon">🏦</div>

          <h2>Find Nearby Banks</h2>

          <p>
            Get recommended lending banks, Regional Rural Banks and
            district-level support based on your scheme and location.
          </p>
        </section>

        {/* FORM */}
        <section className="bank-form-card">

          <h3>Enter Your Details</h3>

          <p className="bank-form-subtitle">
            Provide your scheme and location information
          </p>

          <form onSubmit={handleSubmit}>

            <div className="bank-form-grid">

              <div className="bank-input-group">
                <label>Scheme Code</label>

                <input
                  type="text"
                  name="scheme_code"
                  placeholder="e.g. STANDUP-INDIA"
                  value={formData.scheme_code}
                  onChange={handleChange}
                  required
                />

                <small>
                  Enter the government scheme code
                </small>
              </div>

              <div className="bank-input-group">
                <label>State</label>

                <input
                  type="text"
                  name="state"
                  placeholder="e.g. Uttar Pradesh"
                  value={formData.state}
                  onChange={handleChange}
                  required
                />

                <small>
                  Enter your state
                </small>
              </div>

              <div className="bank-input-group">
                <label>District</label>

                <input
                  type="text"
                  name="district"
                  placeholder="e.g. Varanasi"
                  value={formData.district}
                  onChange={handleChange}
                />

                <small>
                  Optional
                </small>
              </div>

            </div>

            <button
              type="submit"
              className="find-bank-button"
              disabled={loading}
            >
              {loading
                ? "Finding Banks..."
                : "Find Recommended Banks →"}
            </button>

          </form>
        </section>

        {/* ERROR */}
        {error && (
          <div className="bank-error">
            ⚠️ {error}
          </div>
        )}

        {/* RESULTS */}
        {banks && (
          <section className="bank-results">

            <div className="results-top">
              <div>
                <span className="results-label">
                  BANK RECOMMENDATIONS
                </span>

                <h2>
                  Recommended Banks
                </h2>

                <p>
                  Based on your scheme and location.
                </p>
              </div>

              <div className="location-badge">
                📍 {banks.district}, {banks.state}
              </div>
            </div>


            {/* BASIC INFORMATION */}
            <div className="bank-summary">

              <div className="summary-card">
                <span>Scheme</span>
                <strong>
                  {banks.scheme_name || "Not available"}
                </strong>
              </div>

              <div className="summary-card">
                <span>Scheme Code</span>
                <strong>
                  {banks.scheme_code || formData.scheme_code}
                </strong>
              </div>

              <div className="summary-card">
                <span>Lead Bank</span>
                <strong>
                  {banks.lead_bank_name || "Not available"}
                </strong>
              </div>

            </div>


            {/* LEAD BANK */}
            {banks.lead_bank_name && (
              <div className="lead-bank-card">

                <div className="lead-bank-icon">
                  🏦
                </div>

                <div>
                  <span>DESIGNATED LEAD BANK</span>
                  <h3>{banks.lead_bank_name}</h3>

                  {banks.ldm_office_info && (
                    <p>
                      {banks.ldm_office_info}
                    </p>
                  )}
                </div>

              </div>
            )}


            {/* PRIMARY LENDING BANKS */}
            {banks.primary_lending_banks &&
              banks.primary_lending_banks.length > 0 && (
                <div className="bank-section">

                  <div className="section-heading">
                    <span>🏦</span>

                    <div>
                      <h3>Primary Lending Banks</h3>
                      <p>
                        Participating banks recommended for this scheme.
                      </p>
                    </div>
                  </div>

                  <div className="bank-list">

                    {banks.primary_lending_banks.map(
                      (bank, index) => (
                        <div
                          className="bank-item"
                          key={index}
                        >
                          <div className="bank-number">
                            {index + 1}
                          </div>

                          <div>
                            <strong>
                              {bank.name ||
                                bank.bank_name ||
                                bank.bank ||
                                "Bank"}
                            </strong>

                            {bank.location && (
                              <p>
                                📍 {bank.location}
                              </p>
                            )}
                          </div>
                        </div>
                      )
                    )}

                  </div>
                </div>
              )}


            {/* REGIONAL RURAL BANKS */}
            {banks.regional_rural_banks &&
              banks.regional_rural_banks.length > 0 && (
                <div className="bank-section">

                  <div className="section-heading">
                    <span>🌾</span>

                    <div>
                      <h3>Regional Rural Banks</h3>
                      <p>
                        Rural banking options available in the region.
                      </p>
                    </div>
                  </div>

                  <div className="bank-list">

                    {banks.regional_rural_banks.map(
                      (bank, index) => (
                        <div
                          className="bank-item"
                          key={index}
                        >
                          <div className="bank-number">
                            {index + 1}
                          </div>

                          <div>
                            <strong>
                              {bank.name ||
                                bank.bank_name ||
                                bank.bank ||
                                "Regional Rural Bank"}
                            </strong>

                            {bank.location && (
                              <p>
                                📍 {bank.location}
                              </p>
                            )}
                          </div>
                        </div>
                      )
                    )}

                  </div>
                </div>
              )}


            {/* DISTRICT NODAL OFFICES */}
            {banks.district_nodal_offices &&
              banks.district_nodal_offices.length > 0 && (
                <div className="bank-section">

                  <div className="section-heading">
                    <span>🏛️</span>

                    <div>
                      <h3>District Nodal Offices</h3>
                      <p>
                        District-level agencies supporting scheme applications.
                      </p>
                    </div>
                  </div>

                  <div className="nodal-list">

                    {banks.district_nodal_offices.map(
                      (office, index) => (
                        <div
                          className="nodal-card"
                          key={index}
                        >
                          <h4>
                            {office.agency}
                          </h4>

                          <p>
                            <strong>Location:</strong>{" "}
                            {office.location}
                          </p>

                          <p>
                            <strong>Role:</strong>{" "}
                            {office.role}
                          </p>
                        </div>
                      )
                    )}

                  </div>
                </div>
              )}


            {/* APPLICATION STEPS */}
            {banks.application_steps &&
              banks.application_steps.length > 0 && (
                <div className="bank-section">

                  <div className="section-heading">
                    <span>📝</span>

                    <div>
                      <h3>Application Steps</h3>
                      <p>
                        General steps for applying through the recommended channel.
                      </p>
                    </div>
                  </div>

                  <div className="steps-list">

                    {banks.application_steps.map(
                      (step, index) => (
                        <div
                          className="step-item"
                          key={index}
                        >
                          <div className="step-number">
                            {index + 1}
                          </div>

                          <p>{step}</p>
                        </div>
                      )
                    )}

                  </div>
                </div>
              )}


            {/* REQUIRED DOCUMENTS */}
            {banks.required_documents &&
              banks.required_documents.length > 0 && (
                <div className="bank-section">

                  <div className="section-heading">
                    <span>📄</span>

                    <div>
                      <h3>Required Documents</h3>
                      <p>
                        Keep these documents ready before applying.
                      </p>
                    </div>
                  </div>

                  <ul className="documents-list">

                    {banks.required_documents.map(
                      (document, index) => (
                        <li key={index}>
                          <span>✓</span>
                          {document}
                        </li>
                      )
                    )}

                  </ul>

                </div>
              )}

          </section>
        )}

      </main>
    </div>
  );
}

export default Banks;