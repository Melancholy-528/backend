import React, { useState } from "react";
import "../styles/Login.css";
import indiaImage from "../assets/india.jpg";

function SchemeLogo({ small = false }) {
  return (
    <div className={`scheme-logo ${small ? "small" : ""}`}>
      <svg
        viewBox="0 0 64 64"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M20 18C14 18 10 23 10 29C10 35 14 40 20 40H31"
          stroke="white"
          strokeWidth="7"
          strokeLinecap="round"
        />
        <path
          d="M44 46C50 46 54 41 54 35C54 29 50 24 44 24H33"
          stroke="white"
          strokeWidth="7"
          strokeLinecap="round"
        />
        <path
          d="M25 32L39 20"
          stroke="white"
          strokeWidth="7"
          strokeLinecap="round"
        />
        <path
          d="M39 44L25 32"
          stroke="white"
          strokeWidth="7"
          strokeLinecap="round"
        />
      </svg>
    </div>
  );
}

function Login({ onLogin })  {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <main className="login-page">

      <div className="glow glow-one"></div>
      <div className="glow glow-two"></div>

      <div className="login-container">

        {/* ================= LEFT ================= */}

        <section className="hero-section">

          {/* Brand */}
          <div className="brand">
            <SchemeLogo />

            <div className="brand-text">
              <h2>
                SchemeSetu <span>AI</span>
              </h2>

              <p>AI-Driven Scheme Matching</p>
            </div>
          </div>

          {/* Hero */}
          <div className="hero-content">

            <h1>
              Discover.
              <br />

              <span className="purple-text">
                Match.
              </span>

              <br />

              <span className="cyan-text">
                Grow.
              </span>
            </h1>

            <p className="hero-description">
              AI-powered assistance helping marginalized
              entrepreneurs discover government schemes
              that match their needs.
            </p>

          </div>

          {/* India */}
          <div className="india-wrapper">

            <div className="india-glow"></div>

            <img
              src={indiaImage}
              alt="India AI Network"
              className="india-image"
            />

          </div>

          {/* Features */}
          <div className="features">

            {/* AI Matching */}
            <div className="feature-item">

              <div className="feature-icon purple-icon">

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                >
                  <circle
                    cx="12"
                    cy="12"
                    r="8"
                    strokeWidth="1.8"
                  />

                  <circle
                    cx="12"
                    cy="12"
                    r="3"
                    strokeWidth="1.8"
                  />

                  <path
                    d="M12 4V2M12 22v-2M4 12H2M22 12h-2"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                  />

                  <path
                    d="M6.5 6.5l1.5 1.5M16 16l1.5 1.5M17.5 6.5L16 8M8 16l-1.5 1.5"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                  />
                </svg>

              </div>

              <div>
                <h3>AI-Driven Matching</h3>

                <p>
                  Smart algorithms match entrepreneurs
                  with relevant schemes.
                </p>
              </div>

            </div>

            {/* Security */}
            <div className="feature-item">

              <div className="feature-icon blue-icon">

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                >
                  <path
                    d="M12 3l8 3v6c0 5-3.4 8-8 9-4.6-1-8-4-8-9V6l8-3z"
                    strokeWidth="1.8"
                    strokeLinejoin="round"
                  />

                  <path
                    d="M9 12l2 2 4-4"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>

              </div>

              <div>
                <h3>Trusted & Secure</h3>

                <p>
                  Your information is handled securely
                  and responsibly.
                </p>
              </div>

            </div>

            {/* Growth */}
            <div className="feature-item">

              <div className="feature-icon cyan-icon">

                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                >
                  <path
                    d="M4 19l6-6 4 3 6-8"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />

                  <path
                    d="M16 8h4v4"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>

              </div>

              <div>
                <h3>Empower Growth</h3>

                <p>
                  Discover opportunities that support
                  your business journey.
                </p>
              </div>

            </div>

          </div>

          <p className="bottom-text">
            Empowering entrepreneurs.{" "}
            <span>Building a stronger India.</span>
          </p>

        </section>

        {/* ================= RIGHT ================= */}

        <section className="login-section">

          <div className="login-card">

            <SchemeLogo small />

            <h2>Welcome Back </h2>

            <p className="login-subtitle">
              Login to your{" "}
              <span>SchemeSetu AI</span>{" "}
              account
            </p>

            {/* Email */}

            <div className="input-group">

              <label>Email Address</label>

              <div className="input-wrapper">

                <svg
                  className="input-icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                >
                  <rect
                    x="3"
                    y="5"
                    width="18"
                    height="14"
                    rx="2"
                    strokeWidth="1.8"
                  />

                  <path
                    d="M3 7l9 6 9-6"
                    strokeWidth="1.8"
                  />
                </svg>

                <input
                  type="email"
                  placeholder="Enter your email"
                />

              </div>

            </div>

            {/* Password */}

            <div className="input-group">

              <label>Password</label>

              <div className="input-wrapper">

                <input
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Enter your password"
                />

                <button
                  type="button"
                  className="eye-button"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                >

                  {showPassword ? (

                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                    >
                      <path
                        d="M3 3l18 18"
                        strokeWidth="1.8"
                      />

                      <path
                        d="M10.6 10.6a2 2 0 0 0 2.8 2.8"
                        strokeWidth="1.8"
                      />
                    </svg>

                  ) : (

                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                    >
                      <path
                        d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"
                        strokeWidth="1.8"
                      />

                      <circle
                        cx="12"
                        cy="12"
                        r="2.5"
                        strokeWidth="1.8"
                      />
                    </svg>

                  )}

                </button>

              </div>

            </div>

            {/* Forgot */}

            <div className="forgot-password">
              <a href="#">
                Forgot Password?
              </a>
            </div>

            {/* Login */}

           <button className="login-button" onClick={onLogin}>

              <span>
                Login to SchemeSetu AI
              </span>

              <span className="login-arrow">
                →
              </span>

            </button>

            {/* Divider */}

            <div className="divider">

              <span></span>

              <p>or continue with</p>

              <span></span>

            </div>

            {/* Applications */}

            <div className="social-buttons">

              <button className="social-button">

                <span className="google-logo">
                  G
                </span>

                Google

              </button>

              <button className="social-button">

                <svg
                  className="scheme-icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                >
                  <path
                    d="M4 20h16"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                  />

                  <path
                    d="M6 20V10h12v10"
                    strokeWidth="1.8"
                  />

                  <path
                    d="M4 10l8-6 8 6"
                    strokeWidth="1.8"
                    strokeLinejoin="round"
                  />

                  <path
                    d="M9 14h6M9 17h6"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                  />
                </svg>

                <button className="social-button">

  <svg
    className="facebook-icon"
    viewBox="0 0 24 24"
    fill="none"
  >
    <circle
      cx="12"
      cy="12"
      r="10"
      fill="#1877F2"
    />

    <path
      d="M13.5 20V13.5H16L16.5 11H13.5V9.5C13.5 8.7 13.9 8.2 15 8.2H16.5V5.9C16.2 5.8 15.3 5.7 14.3 5.7C12.2 5.7 10.8 7 10.8 9.3V11H8.5V13.5H10.8V20H13.5Z"
      fill="white"
    />
  </svg>

  Facebook

</button>

              </button>

            </div>

            {/* Signup */}

            <p className="signup-text">

              Don't have an account?{" "}

              <a href="#">
                Sign Up
              </a>

            </p>

          </div>

        </section>

      </div>

    </main>
  );
}

export default Login;