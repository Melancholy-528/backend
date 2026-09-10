import "../styles/Landing.css";

function Landing({ onLogin, onRegister }) {
  return (
    <div className="landing-page">

      {/* ================= NAVBAR ================= */}
      <header className="landing-navbar">
        <div className="landing-nav-inner">

          <div className="landing-brand">
            <div className="brand-mark">S</div>

            <div>
              <h2>SchemeSetu <span>AI</span></h2>
              <p>Enterprise & Scheme Intelligence</p>
            </div>
          </div>

          <nav className="landing-nav-links">
            <a href="#home">Home</a>
            <a href="#schemes">Schemes</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#features">Features</a>
            <a href="#about">About</a>
          </nav>

          <div className="landing-nav-actions">
            <button className="nav-login" onClick={onLogin}>
              Login
            </button>

            <button className="nav-register" onClick={onRegister}>
              Get Started
            </button>
          </div>

        </div>
      </header>


      {/* ================= HERO ================= */}
      <main>

        <section className="hero-section" id="home">

          <div className="hero-background-grid"></div>

          <div className="hero-content">

            <div className="hero-badge">
              <span className="badge-dot"></span>
              AI-Powered Government Scheme Intelligence
            </div>

            <h1>
              Discover the right
              <br />

              <span className="hero-gradient-text">
                opportunities for your enterprise.
              </span>
            </h1>

            <p className="hero-description">
              SchemeSetu AI helps entrepreneurs discover government schemes,
              understand eligibility, access financial support and connect
              with the right banking ecosystem — all from one platform.
            </p>

            <div className="hero-buttons">

              <button
                className="primary-hero-button"
                onClick={onRegister}
              >
                Find Schemes for Me
                <span>→</span>
              </button>

              <a
                href="#how-it-works"
                className="secondary-hero-button"
              >
                Explore How It Works
              </a>

            </div>

            <div className="hero-trust">

              <div className="trust-item">
                <strong>AI</strong>
                <span>Powered Matching</span>
              </div>

              <div className="trust-divider"></div>

              <div className="trust-item">
                <strong>360°</strong>
                <span>Enterprise Support</span>
              </div>

              <div className="trust-divider"></div>

              <div className="trust-item">
                <strong>1</strong>
                <span>Unified Platform</span>
              </div>

            </div>

          </div>


          {/* HERO VISUAL */}
          <div className="hero-visual">

            <div className="dashboard-glow"></div>

            <div className="floating-card floating-card-one">
              <div className="floating-icon">🎯</div>
              <div>
                <strong>12 Schemes</strong>
                <span>Matched for you</span>
              </div>
            </div>

            <div className="hero-dashboard">

              <div className="mini-dashboard-header">
                <div className="mini-brand">
                  <span className="mini-brand-icon">S</span>
                  SchemeSetu AI
                </div>

                <div className="mini-user">
                  <span></span>
                  Profile
                </div>
              </div>

              <div className="mini-dashboard-body">

                <div className="mini-welcome">
                  <span>Good morning 👋</span>
                  <h3>Find the right scheme for your enterprise.</h3>
                </div>

                <div className="mini-stat-row">

                  <div className="mini-stat">
                    <span>Matched Schemes</span>
                    <strong>12</strong>
                    <small>AI recommendations</small>
                  </div>

                  <div className="mini-stat">
                    <span>Banking Options</span>
                    <strong>05</strong>
                    <small>Available lenders</small>
                  </div>

                </div>

                <div className="mini-section-title">
                  Recommended for you
                </div>

                <div className="mini-scheme-card">

                  <div className="scheme-card-icon">
                    ₹
                  </div>

                  <div className="scheme-card-content">
                    <strong>Enterprise Support Scheme</strong>
                    <span>Eligible based on your profile</span>

                    <div className="scheme-progress">
                      <div></div>
                    </div>
                  </div>

                  <div className="match-score">
                    <strong>94%</strong>
                    <span>Match</span>
                  </div>

                </div>

                <div className="mini-scheme-card second">

                  <div className="scheme-card-icon">
                    🏦
                  </div>

                  <div className="scheme-card-content">
                    <strong>Credit Linked Support</strong>
                    <span>Banking assistance available</span>
                  </div>

                  <div className="match-score">
                    <strong>89%</strong>
                    <span>Match</span>
                  </div>

                </div>

              </div>

            </div>

            <div className="floating-card floating-card-two">

              <div className="ai-orbit">
                ✦
              </div>

              <div>
                <strong>AI Advisor</strong>
                <span>Always ready to help</span>
              </div>

            </div>

          </div>

        </section>


        {/* ================= BENEFICIARIES ================= */}
        <section className="beneficiary-section">

          <div className="section-container">

            <div className="section-label">
              INCLUSIVE BY DESIGN
            </div>

            <h2>
              Built for entrepreneurs across
              <span> communities & sectors.</span>
            </h2>

            <p className="section-description">
              SchemeSetu brings relevant government support closer to the
              people and enterprises that need it most.
            </p>

            <div className="beneficiary-grid">

              <div className="beneficiary-card">
                <div>SC</div>
                <span>Scheduled Castes</span>
              </div>

              <div className="beneficiary-card">
                <div>ST</div>
                <span>Scheduled Tribes</span>
              </div>

              <div className="beneficiary-card">
                <div>OBC</div>
                <span>Other Backward Classes</span>
              </div>

              <div className="beneficiary-card">
                <div>W</div>
                <span>Women Entrepreneurs</span>
              </div>

              <div className="beneficiary-card">
                <div>M</div>
                <span>Minority Communities</span>
              </div>

              <div className="beneficiary-card">
                <div>A</div>
                <span>Artisans & Craftspeople</span>
              </div>

              <div className="beneficiary-card">
                <div>P</div>
                <span>Persons with Disabilities</span>
              </div>

            </div>

          </div>

        </section>


        {/* ================= HOW IT WORKS ================= */}
        <section
          className="how-section"
          id="how-it-works"
        >

          <div className="section-container">

            <div className="section-label">
              SIMPLE. INTELLIGENT. CONNECTED.
            </div>

            <h2>
              From profile to
              <span> opportunity.</span>
            </h2>

            <p className="section-description">
              One simple journey from discovering a scheme to understanding
              eligibility and getting connected with financial support.
            </p>


            <div className="steps-grid">

              <div className="step-card">

                <div className="step-number">01</div>

                <div className="step-icon">
                  👤
                </div>

                <h3>Create Your Profile</h3>

                <p>
                  Tell us about your background, enterprise, location,
                  income and project requirements.
                </p>

              </div>


              <div className="step-connector"></div>


              <div className="step-card">

                <div className="step-number">02</div>

                <div className="step-icon">
                  🎯
                </div>

                <h3>Get AI Matches</h3>

                <p>
                  Our intelligent matching engine identifies schemes
                  relevant to your profile and project.
                </p>

              </div>


              <div className="step-connector"></div>


              <div className="step-card">

                <div className="step-number">03</div>

                <div className="step-icon">
                  🤖
                </div>

                <h3>Understand Your Options</h3>

                <p>
                  Ask the AI advisor about eligibility, benefits,
                  documents and application procedures.
                </p>

              </div>


              <div className="step-connector"></div>


              <div className="step-card">

                <div className="step-number">04</div>

                <div className="step-icon">
                  🏦
                </div>

                <h3>Connect With Support</h3>

                <p>
                  Discover lending banks, rural banks and district
                  support offices connected to your scheme.
                </p>

              </div>

            </div>

          </div>

        </section>


        {/* ================= FEATURES ================= */}
        <section
          className="features-section"
          id="features"
        >

          <div className="section-container">

            <div className="section-label">
              ONE PLATFORM
            </div>

            <h2>
              Everything you need to move
              <span> from idea to action.</span>
            </h2>

            <div className="features-grid">

              <div className="feature-card large-feature">

                <div className="feature-top">
                  <div className="feature-icon blue">
                    🎯
                  </div>

                  <span className="feature-arrow">↗</span>
                </div>

                <h3>AI Scheme Matching</h3>

                <p>
                  Get personalized government scheme recommendations
                  based on your profile, eligibility and enterprise needs.
                </p>

                <div className="feature-tags">
                  <span>Eligibility</span>
                  <span>Benefits</span>
                  <span>Subsidy</span>
                </div>

              </div>


              <div className="feature-card">

                <div className="feature-top">
                  <div className="feature-icon purple">
                    🤖
                  </div>

                  <span className="feature-arrow">↗</span>
                </div>

                <h3>AI Advisor</h3>

                <p>
                  Get instant guidance about schemes, applications
                  and enterprise support.
                </p>

              </div>


              <div className="feature-card">

                <div className="feature-top">
                  <div className="feature-icon green">
                    🏦
                  </div>

                  <span className="feature-arrow">↗</span>
                </div>

                <h3>Banking Support</h3>

                <p>
                  Find relevant lending banks, RRBs and district
                  nodal support offices.
                </p>

              </div>


              <div className="feature-card">

                <div className="feature-top">
                  <div className="feature-icon orange">
                    ₹
                  </div>

                  <span className="feature-arrow">↗</span>
                </div>

                <h3>DPR Calculator</h3>

                <p>
                  Structure your enterprise requirements and generate
                  useful project information.
                </p>

              </div>


              <div className="feature-card">

                <div className="feature-top">
                  <div className="feature-icon pink">
                    📄
                  </div>

                  <span className="feature-arrow">↗</span>
                </div>

                <h3>Document Guidance</h3>

                <p>
                  Know what documents are required before beginning
                  your application.
                </p>

              </div>

            </div>

          </div>

        </section>


        {/* ================= ABOUT ================= */}
        <section
          className="about-section"
          id="about"
        >

          <div className="section-container about-layout">

            <div className="about-content">

              <div className="section-label">
                WHY SCHEMESETU AI
              </div>

              <h2>
                Turning complex scheme
                <span> information into action.</span>
              </h2>

              <p>
                Government support can be difficult to discover,
                understand and navigate. SchemeSetu AI creates a
                single intelligent interface that connects entrepreneurs
                with relevant schemes and the ecosystem around them.
              </p>

              <div className="about-points">

                <div>
                  <span>✓</span>
                  Personalized scheme discovery
                </div>

                <div>
                  <span>✓</span>
                  Eligibility-focused recommendations
                </div>

                <div>
                  <span>✓</span>
                  Banking and enterprise support
                </div>

                <div>
                  <span>✓</span>
                  AI-powered guidance
                </div>

              </div>

            </div>


            <div className="about-visual">

              <div className="about-orb orb-one"></div>
              <div className="about-orb orb-two"></div>

              <div className="about-center-card">

                <div className="about-logo">
                  S
                </div>

                <strong>SchemeSetu</strong>

                <span>AI</span>

                <p>
                  Connecting people,
                  <br />
                  schemes & opportunity.
                </p>

              </div>

            </div>

          </div>

        </section>


        {/* ================= CTA ================= */}
        <section className="cta-section">

          <div className="cta-glow"></div>

          <div className="cta-content">

            <div className="section-label">
              START YOUR JOURNEY
            </div>

            <h2>
              Your next opportunity
              <br />
              could be <span>one match away.</span>
            </h2>

            <p>
              Create your profile and let SchemeSetu AI discover
              relevant government support for your enterprise.
            </p>

            <button
              className="cta-button"
              onClick={onRegister}
            >
              Create Your Free Account
              <span>→</span>
            </button>

          </div>

        </section>

      </main>


      {/* ================= FOOTER ================= */}
      <footer className="landing-footer">

        <div className="footer-main">

          <div className="footer-brand">

            <div className="landing-brand">

              <div className="brand-mark">S</div>

              <div>
                <h2>SchemeSetu <span>AI</span></h2>
                <p>Enterprise & Scheme Intelligence</p>
              </div>

            </div>

            <p>
              Intelligent access to government schemes,
              enterprise support and financial opportunities.
            </p>

          </div>


          <div className="footer-column">

            <h4>Platform</h4>

            <a href="#features">AI Scheme Matching</a>
            <a href="#features">AI Advisor</a>
            <a href="#features">Banking Support</a>
            <a href="#features">DPR Calculator</a>

          </div>


          <div className="footer-column">

            <h4>Explore</h4>

            <a href="#home">Home</a>
            <a href="#schemes">Schemes</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#about">About</a>

          </div>


          <div className="footer-column">

            <h4>Account</h4>

            <button onClick={onLogin}>Login</button>
            <button onClick={onRegister}>Register</button>

          </div>

        </div>


        <div className="footer-bottom">

          <span>
            © 2026 SchemeSetu AI. Built for inclusive enterprise growth.
          </span>

          <span>
            AI • Enterprise • Opportunity
          </span>

        </div>

      </footer>

    </div>
  );
}

export default Landing;