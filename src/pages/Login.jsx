import React, { useState } from "react";
import {
  ShieldCheck,
  Cpu,
  Building2,
  Lock,
  Mail,
  User,
  Eye,
  EyeOff,
  ArrowRight,
  ArrowLeft,
  CheckCircle2,
  Award,
  Phone,
  MapPin,
} from "lucide-react";
import "../styles/Login.css";

export default function Login({ onLogin, onBack }) {
  const [isSignUp, setIsSignUp] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  // Form states
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    phone: "",
    category: "SC",
    state: "Uttar Pradesh",
    district: "Varanasi",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);

    // Simulate login / signup completion
    setTimeout(() => {
      setLoading(false);
      if (onLogin) {
        onLogin({
          full_name: isSignUp ? formData.fullName || "Beneficiary Entrepreneur" : "Rajesh Kumar",
          email: formData.email || "beneficiary@example.com",
          category: formData.category || "SC",
          state: formData.state || "Uttar Pradesh",
          district: formData.district || "Varanasi",
        });
      }
    }, 400);
  };

  const handleDemoLogin = (role = "SC") => {
    if (onLogin) {
      onLogin({
        full_name: role === "SC" ? "Rajesh Kumar" : "Sunita Devi",
        email: role === "SC" ? "rajesh.kumar@beneficiary.gov.in" : "sunita.devi@artisan.gov.in",
        category: role === "SC" ? "SC" : "Artisan",
        state: "Uttar Pradesh",
        district: "Varanasi",
      });
    }
  };

  return (
    <div className="login-page-wrapper">
      {/* Top Government Ribbon */}
      <div className="login-gov-ribbon">
        <div className="login-ribbon-content">
          <div className="ribbon-left">
            <span className="gov-text">भारत सरकार | Government of India</span>
            <span className="dot-sep">•</span>
            <span>Ministry of Social Justice and Empowerment (MoSJE)</span>
          </div>
          <div className="ribbon-right">
            {onBack && (
              <button className="ribbon-back-btn" onClick={onBack}>
                <ArrowLeft size={14} /> Back to Homepage
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="login-split-container">
        {/* =========================================================================
            LEFT COLUMN: THEME PRESENTATION & IMPACT HIGHLIGHTS
           ========================================================================= */}
        <section className="login-brand-panel">
          <div className="brand-panel-inner">
            {/* Logo */}
            <div className="panel-logo-row" onClick={onBack} style={{ cursor: onBack ? "pointer" : "default" }}>
              <div className="brand-emblem-box">SS</div>
              <div>
                <h2>
                  UdyamSetu <span>AI</span>
                </h2>
                <p>MoSJE & MSME Beneficiary Portal</p>
              </div>
            </div>

            {/* Main Heading */}
            <div className="panel-hero-text">
              <div className="hero-trust-badge">
                <Award size={14} /> SIH26092 Central AI Platform
              </div>
              <h1>
                Empowering Marginalized Communities with Direct Scheme Access
              </h1>
              <p className="hero-subline">
                Sign in to discover tailored government subsidies, collateral-free credit
                facilities, educational scholarships, and local Lead District Bank routing.
              </p>
            </div>

            {/* Impact Metric Counters */}
            <div className="panel-stats-grid">
              <div className="panel-stat-item">
                <strong>15+</strong>
                <span>Central & State Schemes</span>
              </div>
              <div className="panel-stat-item">
                <strong>₹1 Crore</strong>
                <span>Max Collateral-Free Loan</span>
              </div>
              <div className="panel-stat-item">
                <strong>Up to 35%</strong>
                <span>Capital Subsidy Aid</span>
              </div>
            </div>

            {/* Trust Highlights */}
            <div className="panel-trust-points">
              <div className="trust-point-item">
                <div className="point-icon-box">
                  <ShieldCheck size={20} color="#1E3A8A" />
                </div>
                <div>
                  <h4>100% Government Verified</h4>
                  <p>Direct integration with MoSJE, MSME, KVIC, NSFDC, and NBCFDC circulars.</p>
                </div>
              </div>

              <div className="trust-point-item">
                <div className="point-icon-box">
                  <Cpu size={20} color="#1E3A8A" />
                </div>
                <div>
                  <h4>AI-Powered Scheme Matching</h4>
                  <p>Automated evaluation of caste, annual income, age, and project budget.</p>
                </div>
              </div>

              <div className="trust-point-item">
                <div className="point-icon-box">
                  <Building2 size={20} color="#1E3A8A" />
                </div>
                <div>
                  <h4>Designated Bank Support</h4>
                  <p>Direct mapping to your Lead District Bank and District Industries Centre (DIC).</p>
                </div>
              </div>
            </div>

            <div className="panel-footer-note">
              <p>
                A Smart India Hackathon initiative for inclusive digital governance and
                financial upliftment.
              </p>
            </div>
          </div>
        </section>

        {/* =========================================================================
            RIGHT COLUMN: LOGIN / REGISTER CARD
           ========================================================================= */}
        <section className="login-form-panel">
          <div className="login-card-box">
            {/* Card Header & Toggle Tabs */}
            <div className="form-card-header">
              <div className="auth-tab-pills">
                <button
                  type="button"
                  className={`auth-tab ${!isSignUp ? "active" : ""}`}
                  onClick={() => setIsSignUp(false)}
                >
                  Sign In
                </button>
                <button
                  type="button"
                  className={`auth-tab ${isSignUp ? "active" : ""}`}
                  onClick={() => setIsSignUp(true)}
                >
                  Create Account
                </button>
              </div>

              <h3>{isSignUp ? "Register as Beneficiary" : "Welcome Back"}</h3>
              <p className="form-instruction">
                {isSignUp
                  ? "Enter your details to create a beneficiary account and save schemes"
                  : "Sign in to access your saved schemes, DPR financial reports, and AI advisor"}
              </p>
            </div>

            {/* Quick Demo Login Option */}
            <div className="demo-login-banner">
              <div className="demo-badge">QUICK DEMO ACCESS</div>
              <p>Skip manual entry for testing and hackathon review:</p>
              <div className="demo-btn-row">
                <button
                  type="button"
                  className="btn-demo-pill"
                  onClick={() => handleDemoLogin("SC")}
                >
                  ⚡ Demo SC Entrepreneur Login
                </button>
                <button
                  type="button"
                  className="btn-demo-pill secondary"
                  onClick={() => handleDemoLogin("Artisan")}
                >
                  🛠️ Demo Artisan Login
                </button>
              </div>
            </div>

            <div className="form-divider">
              <span>or enter credentials</span>
            </div>

            {/* Main Form */}
            <form onSubmit={handleSubmit} className="auth-form-content">
              {isSignUp && (
                <>
                  {/* Full Name */}
                  <div className="form-input-group">
                    <label>Full Name</label>
                    <div className="input-field-box">
                      <User size={18} className="field-icon" />
                      <input
                        type="text"
                        name="fullName"
                        placeholder="e.g. Rajesh Kumar"
                        value={formData.fullName}
                        onChange={handleChange}
                        required={isSignUp}
                      />
                    </div>
                  </div>

                  {/* Category & State Row */}
                  <div className="form-row-two-col">
                    <div className="form-input-group">
                      <label>Target Category</label>
                      <select
                        name="category"
                        value={formData.category}
                        onChange={handleChange}
                        className="select-field"
                      >
                        <option value="SC">SC (Scheduled Caste)</option>
                        <option value="ST">ST (Scheduled Tribe)</option>
                        <option value="OBC">OBC (Backward Class)</option>
                        <option value="Women">Women Entrepreneur</option>
                        <option value="Artisan">Artisan / Vishwakarma</option>
                        <option value="Minority">Minority Community</option>
                        <option value="General">General Category</option>
                      </select>
                    </div>

                    <div className="form-input-group">
                      <label>Resident State</label>
                      <div className="input-field-box">
                        <MapPin size={18} className="field-icon" />
                        <input
                          type="text"
                          name="state"
                          placeholder="e.g. Uttar Pradesh"
                          value={formData.state}
                          onChange={handleChange}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Mobile Number */}
                  <div className="form-input-group">
                    <label>Mobile Number (Optional)</label>
                    <div className="input-field-box">
                      <Phone size={18} className="field-icon" />
                      <input
                        type="tel"
                        name="phone"
                        placeholder="10-digit mobile number"
                        value={formData.phone}
                        onChange={handleChange}
                      />
                    </div>
                  </div>
                </>
              )}

              {/* Email Address */}
              <div className="form-input-group">
                <label>Email Address</label>
                <div className="input-field-box">
                  <Mail size={18} className="field-icon" />
                  <input
                    type="email"
                    name="email"
                    placeholder="name@example.com"
                    value={formData.email}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              {/* Password */}
              <div className="form-input-group">
                <div className="label-with-link">
                  <label>Password</label>
                  {!isSignUp && (
                    <a href="#forgot" className="forgot-link" onClick={(e) => e.preventDefault()}>
                      Forgot Password?
                    </a>
                  )}
                </div>
                <div className="input-field-box">
                  <Lock size={18} className="field-icon" />
                  <input
                    type={showPassword ? "text" : "password"}
                    name="password"
                    placeholder="Enter your password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                  />
                  <button
                    type="button"
                    className="password-toggle-btn"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label="Toggle password visibility"
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                className="btn-auth-submit"
                disabled={loading}
              >
                {loading ? (
                  "Verifying Credentials..."
                ) : isSignUp ? (
                  <>
                    Create Account & Continue <ArrowRight size={18} />
                  </>
                ) : (
                  <>
                    Sign In to UdyamSetu AI <ArrowRight size={18} />
                  </>
                )}
              </button>
            </form>

            {/* Back to Homepage Footer */}
            <div className="form-card-bottom">
              {onBack && (
                <button type="button" className="btn-return-home" onClick={onBack}>
                  <ArrowLeft size={16} /> Return to Homepage
                </button>
              )}
              <p className="card-privacy-notice">
                Official MoSJE Portal • 256-bit SSL Encrypted • Privacy Protected
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}