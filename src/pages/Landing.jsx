import { useState, useEffect } from "react";
import {
  ChevronLeft,
  ChevronRight,
  GraduationCap,
  Briefcase,
  Wrench,
  Coins,
  ShieldCheck,
  Cpu,
  Building2,
  ArrowRight,
  CheckCircle2,
  Globe,
  User,
  Bookmark,
  Search,
  ExternalLink,
  HelpCircle,
  Phone,
  Mail,
  MapPin,
  LogOut,
  Menu,
  X,
  Star,
  FileText,
  Sparkles,
  Layers,
  Award,
  TrendingUp,
  MessageCircle,
  Send,
} from "lucide-react";
import "../styles/Landing.css";

// Carousel Background Images
import carouselEducation from "../assets/carousel_education.jpg";
import carouselMsme from "../assets/carousel_msme.jpg";
import carouselArtisan from "../assets/carousel_artisan.jpg";

const LANGUAGES = [
  { code: "en", label: "English" },
  { code: "hi", label: "हिंदी (Hindi)" },
  { code: "mr", label: "मराठी (Marathi)" },
  { code: "ta", label: "தமிழ் (Tamil)" },
  { code: "te", label: "తెలుగు (Telugu)" },
  { code: "bn", label: "বাংলা (Bengali)" },
  { code: "gu", label: "ગુજરાતી (Gujarati)" },
  { code: "kn", label: "ಕನ್ನಡ (Kannada)" },
];

const CAROUSEL_SLIDES = [
  {
    id: 1,
    tag: "MINISTRY OF SOCIAL JUSTICE & EMPOWERMENT (MoSJE)",
    title: "Empowering the Scheduled Caste Community with the Right Financial Assistance",
    description:
      "Discover suitable government schemes and educational loans based on your eligibility. Access verified scholarships, concessional term loans, and credit-linked subsidies directly from official portals.",
    image: carouselEducation,
    badgeText: "Concessional Education & Term Loans",
    primaryCta: "Check Eligibility (Scheme Analyzer)",
    secondaryCta: "Explore All Schemes",
    stats: "Up to 100% Scholarship & 4% Concessional Credit",
  },
  {
    id: 2,
    tag: "MINISTRY OF FINANCE & MSME INITIATIVE",
    title: "Catalyzing SC, ST & Women Entrepreneurs with Stand-Up India & PMEGP",
    description:
      "Unlock collateral-free credit from ₹10 Lakhs up to ₹1 Crore. Avail up to 35% margin money capital subsidies and credit guarantee coverage for greenfield manufacturing and services ventures.",
    image: carouselMsme,
    badgeText: "Collateral-Free Capital up to ₹1 Crore",
    primaryCta: "Launch Scheme Analyzer",
    secondaryCta: "Locate Designated Banks",
    stats: "₹10L – ₹1Cr Composite Bank Loans",
  },
  {
    id: 3,
    tag: "PM VISHWAKARMA CENTRAL SECTOR SCHEME",
    title: "Holistic Support for Traditional Artisans & Craftspeople",
    description:
      "Preserving centuries of craftsmanship with ₹3 Lakhs collateral-free credit at 5% interest subvention, ₹15,000 modern toolkit incentives, skill upskilling, and direct market linkages.",
    image: carouselArtisan,
    badgeText: "₹15,000 Toolkit Incentive + 5% Loan",
    primaryCta: "Check Artisan Eligibility",
    secondaryCta: "View Skill Schemes",
    stats: "18 Traditional Trades Supported Across India",
  },
];

const SCHEME_CATALOG = [
  {
    code: "STANDUP-INDIA",
    name: "Stand-Up India Scheme",
    category: "Business",
    target: "SC, ST, Women",
    maxCost: "₹1 Crore",
    subsidy: "15% Margin Money Aid",
    interest: "Base Rate + 3%",
    ministry: "Ministry of Finance / SIDBI",
    description: "Facilitates bank loans between ₹10 Lakhs and ₹1 Crore to at least one SC/ST and one woman borrower per bank branch.",
  },
  {
    code: "PMEGP",
    name: "Prime Minister's Employment Generation Programme (PMEGP)",
    category: "Business",
    target: "SC, ST, OBC, Women, PwD",
    maxCost: "₹50 Lakhs",
    subsidy: "25% to 35% Capital Subsidy",
    interest: "Normal Bank Lending Rate",
    ministry: "Ministry of MSME / KVIC",
    description: "Credit-linked subsidy programme to generate self-employment ventures in manufacturing and services.",
  },
  {
    code: "PM-VISHWAKARMA",
    name: "PM Vishwakarma Scheme",
    category: "Skill Development",
    target: "Artisans, Traditional Crafts",
    maxCost: "₹3 Lakhs (Tranche 1 & 2)",
    subsidy: "8% Interest Subvention + ₹15k Toolkit",
    interest: "Concessional 5% Effective Rate",
    ministry: "Ministry of MSME & MoSJE",
    description: "End-to-end recognition, ID cards, ₹15,000 e-voucher for modern toolkits, and collateral-free enterprise loans.",
  },
  {
    code: "NSFDC-TL",
    name: "NSFDC Term Loan Scheme",
    category: "Financial Assistance",
    target: "Scheduled Castes (SC)",
    maxCost: "₹50 Lakhs",
    subsidy: "SCA Margin Money Assistance",
    interest: "4% to 6% per annum",
    ministry: "Ministry of Social Justice & Empowerment",
    description: "Low-interest project financing through State Channelizing Agencies for income generation ventures of SC beneficiaries.",
  },
  {
    code: "NOS-SC",
    name: "National Overseas Scholarship for SC Candidates",
    category: "Education",
    target: "SC, De-notified Nomadic Tribes",
    maxCost: "Full Tuition + Living Stipend",
    subsidy: "100% Grant Support",
    interest: "Non-repayable Grant",
    ministry: "Ministry of Social Justice & Empowerment",
    description: "Provides financial assistance to selected SC students pursuing Master's or Ph.D. degrees in accredited foreign universities.",
  },
  {
    code: "PM-MUDRA",
    name: "Pradhan Mantri MUDRA Yojana (PMMY)",
    category: "Business",
    target: "Micro Enterprises, All Categories",
    maxCost: "₹20 Lakhs (Tarun Plus)",
    subsidy: "Credit Guarantee Backed (CGFMU)",
    interest: "MBLR Linked Rate",
    ministry: "Ministry of Finance",
    description: "Collateral-free institutional credit to micro/small business enterprises in manufacturing, trading, and services.",
  },
  {
    code: "PM-SVANIDHI",
    name: "PM SVANidhi (Street Vendor's AtmaNirbhar Nidhi)",
    category: "Financial Assistance",
    target: "Street Vendors, Urban Informal",
    maxCost: "₹50,000 (3rd Tranche)",
    subsidy: "7% Interest Subsidy + Cashback",
    interest: "7% Subvention",
    ministry: "Ministry of Housing & Urban Affairs",
    description: "Affordable working capital credit to street vendors to resume their livelihoods post-pandemic, promoting digital transactions.",
  },
  {
    code: "POST-MATRIC-SC",
    name: "Post-Matric Scholarship for SC Students",
    category: "Education",
    target: "SC Students (Income < ₹2.5L)",
    maxCost: "Full Compulsory Non-Refundable Fees",
    subsidy: "Direct Benefit Transfer (DBT)",
    interest: "100% Scholarship",
    ministry: "Ministry of Social Justice & Empowerment",
    description: "Financial assistance to SC students studying at post-matriculation or post-secondary stages to enable them to complete education.",
  },
];

export default function Landing({
  onLogin,
  onRegister,
  onOpenSchemeAnalyzer,
  onOpenBanks,
  onOpenChat,
  user = null,
  onLogout,
}) {
  // Navigation & Language State
  const [currentSlide, setCurrentSlide] = useState(0);
  const [selectedLanguage, setSelectedLanguage] = useState("en");
  const [langDropdownOpen, setLangDropdownOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isPaused, setIsPaused] = useState(false);

  // Authenticated Sidebar State (When user is logged in)
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeTab, setActiveTab] = useState("all-schemes"); // "saved", "all-schemes", "banks"
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");

  // Interactive Trust & How It Works Animation States
  const [activeHowStep, setActiveHowStep] = useState(0);
  const [isHowPaused, setIsHowPaused] = useState(false);
  const [activeTrustCard, setActiveTrustCard] = useState(0);

  // Local saved schemes state (for demo/authenticated layout)
  const [savedSchemes, setSavedSchemes] = useState(["STANDUP-INDIA", "NSFDC-TL", "POST-MATRIC-SC"]);
  const [catalogModalScheme, setCatalogModalScheme] = useState(null);
  const [chatOpen, setChatOpen] = useState(false);
  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState([
    {
      role: "assistant",
      content:
        "Hi! I'm your SC Credit Connect assistant. I can help you find the right loan or education scheme, check eligibility, and locate nearby bank partners.",
    },
    {
      role: "assistant",
      content:
        "Try asking: 'Which scheme is best for a small business?' or 'What documents do I need?'",
    },
  ]);

  // Auto advance carousel every 6 seconds unless paused
  useEffect(() => {
    if (isPaused) return;
    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % CAROUSEL_SLIDES.length);
    }, 6000);
    return () => clearInterval(interval);
  }, [isPaused]);

  // Auto advance how-it-works simulation steps every 4.5 seconds unless paused
  useEffect(() => {
    if (isHowPaused) return;
    const interval = setInterval(() => {
      setActiveHowStep((prev) => (prev + 1) % 3);
    }, 4500);
    return () => clearInterval(interval);
  }, [isHowPaused]);

  const handlePrevSlide = () => {
    setCurrentSlide((prev) => (prev === 0 ? CAROUSEL_SLIDES.length - 1 : prev - 1));
  };

  const handleNextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % CAROUSEL_SLIDES.length);
  };

  const toggleSaveScheme = (code) => {
    setSavedSchemes((prev) =>
      prev.includes(code) ? prev.filter((item) => item !== code) : [...prev, code]
    );
  };

  const filteredSchemes = SCHEME_CATALOG.filter((scheme) => {
    const matchesCat = selectedCategory === "All" || scheme.category === selectedCategory;
    const matchesSearch =
      scheme.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      scheme.code.toLowerCase().includes(searchQuery.toLowerCase()) ||
      scheme.target.toLowerCase().includes(searchQuery.toLowerCase()) ||
      scheme.ministry.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesSearch;
  });

  const savedList = SCHEME_CATALOG.filter((scheme) => savedSchemes.includes(scheme.code));

  const handleChatSubmit = (event) => {
    event.preventDefault();
    const question = chatInput.trim();

    if (!question) return;

    setChatMessages((prev) => [
      ...prev,
      { role: "user", content: question },
      {
        role: "assistant",
        content:
          "Thanks for your question. I can help compare SC-focused loans, scholarships, eligibility, documents, and nearby bank partners. For a detailed answer, open the full AI Chatbot.",
      },
    ]);
    setChatInput("");
  };

  // =========================================================================
  // AUTHENTICATED USER LAYOUT WITH COMPACT VERTICAL SIDEBAR
  // (Displays if user is authenticated OR viewing user dashboard)
  // =========================================================================
  if (user) {
    return (
      <div className="auth-dashboard-layout">
        {/* COMPACT VERTICAL SIDEBAR */}
        <aside className={`auth-sidebar ${sidebarOpen ? "expanded" : "collapsed"}`}>
          <div className="sidebar-brand">
            <div className="brand-emblem">SS</div>
            {sidebarOpen && (
              <div className="brand-info">
                <h3>UdyamSetu AI</h3>
                <span>MoSJE Beneficiary Portal</span>
              </div>
            )}
          </div>

          <div className="sidebar-user-card">
            <div className="user-avatar">
              <User size={20} />
            </div>
            {sidebarOpen && (
              <div className="user-details">
                <strong>{user.full_name || "Beneficiary User"}</strong>
                <span>{user.category || "SC"} Community</span>
              </div>
            )}
          </div>

          <nav className="sidebar-nav">
            <button
              className={`sidebar-nav-item ${activeTab === "saved" ? "active" : ""}`}
              onClick={() => setActiveTab("saved")}
              title="Saved Schemes / Favorites"
            >
              <Bookmark size={18} />
              {sidebarOpen && <span>Saved Schemes ({savedSchemes.length})</span>}
            </button>

            <button
              className={`sidebar-nav-item ${activeTab === "all-schemes" ? "active" : ""}`}
              onClick={() => setActiveTab("all-schemes")}
              title="All Government Schemes"
            >
              <FileText size={18} />
              {sidebarOpen && <span>All Schemes</span>}
            </button>

            <button
              className={`sidebar-nav-item ${activeTab === "banks" ? "active" : ""}`}
              onClick={() => {
                if (onOpenBanks) {
                  onOpenBanks();
                } else {
                  setActiveTab("banks");
                }
              }}
              title="Nearby Banks & Lead District Offices"
            >
              <Building2 size={18} />
              {sidebarOpen && <span>Nearby Banks</span>}
            </button>

            <button
              className="sidebar-nav-item highlight-btn"
              onClick={onOpenSchemeAnalyzer}
              title="Run AI Scheme Analyzer"
            >
              <Cpu size={18} />
              {sidebarOpen && <span>Scheme Analyzer</span>}
            </button>

            {onOpenChat && (
              <button
                className="sidebar-nav-item"
                onClick={onOpenChat}
                title="AI Scheme Advisory Chat"
              >
                <Sparkles size={18} />
                {sidebarOpen && <span>AI Chatbot</span>}
              </button>
            )}
          </nav>

          <div className="sidebar-footer">
            <button
              className="sidebar-nav-item logout-btn"
              onClick={onLogout || onLogin}
              title="Logout"
            >
              <LogOut size={18} />
              {sidebarOpen && <span>Logout</span>}
            </button>
          </div>
        </aside>

        {/* MAIN DASHBOARD CONTENT */}
        <main className="auth-main-content">
          {/* Top Bar */}
          <header className="auth-topbar">
            <div className="topbar-left">
              <button
                className="sidebar-toggle-btn"
                onClick={() => setSidebarOpen(!sidebarOpen)}
                title="Toggle Sidebar"
              >
                <Menu size={20} />
              </button>
              <h2>
                {activeTab === "saved" && "My Saved Schemes / Favorites"}
                {activeTab === "all-schemes" && "All Government Welfare & Enterprise Schemes"}
                {activeTab === "banks" && "Designated Lead District Banks & Nodal Agencies"}
              </h2>
            </div>

            <div className="topbar-right">
              <button className="primary-action-pill" onClick={onOpenSchemeAnalyzer}>
                <Cpu size={16} /> Run Scheme Analyzer
              </button>
              <button
                className="ghost-action-pill"
                onClick={() => {
                  if (onLogout) onLogout();
                }}
              >
                Public Homepage
              </button>
            </div>
          </header>

          {/* TAB: SAVED SCHEMES */}
          {activeTab === "saved" && (
            <div className="dashboard-view-container">
              <div className="section-intro-bar">
                <p>
                  You have bookmarked <strong>{savedList.length} schemes</strong>. Access your DPR
                  requirements, documentation checklists, and application guidelines below.
                </p>
              </div>

              {savedList.length === 0 ? (
                <div className="empty-saved-card">
                  <Bookmark size={40} />
                  <h3>No schemes saved yet</h3>
                  <p>Browse through All Schemes and click the bookmark icon to save them here.</p>
                  <button className="primary-navy-btn" onClick={() => setActiveTab("all-schemes")}>
                    Browse Schemes
                  </button>
                </div>
              ) : (
                <div className="schemes-grid">
                  {savedList.map((scheme) => (
                    <div className="scheme-dashboard-card" key={scheme.code}>
                      <div className="card-top-header">
                        <span className="category-tag">{scheme.category}</span>
                        <button
                          className="bookmark-action active"
                          onClick={() => toggleSaveScheme(scheme.code)}
                          title="Remove from favorites"
                        >
                          <Bookmark size={18} fill="#1E3A8A" />
                        </button>
                      </div>
                      <h3>{scheme.name}</h3>
                      <p className="ministry-tag">{scheme.ministry}</p>
                      <p className="card-desc">{scheme.description}</p>
                      <div className="scheme-metrics">
                        <div>
                          <span>Loan Limit</span>
                          <strong>{scheme.maxCost}</strong>
                        </div>
                        <div>
                          <span>Subsidy Rate</span>
                          <strong>{scheme.subsidy}</strong>
                        </div>
                      </div>
                      <div className="card-actions">
                        <button
                          className="btn-outline-navy"
                          onClick={() => setCatalogModalScheme(scheme)}
                        >
                          View Details
                        </button>
                        <button className="btn-solid-navy" onClick={onOpenSchemeAnalyzer}>
                          Apply & Check Score
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* TAB: ALL SCHEMES */}
          {activeTab === "all-schemes" && (
            <div className="dashboard-view-container">
              {/* Search & Category Filter */}
              <div className="catalog-filter-bar">
                <div className="search-input-wrapper">
                  <Search size={18} />
                  <input
                    type="text"
                    placeholder="Search schemes by name, category, or ministry..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                  {searchQuery && (
                    <button className="clear-search" onClick={() => setSearchQuery("")}>
                      <X size={16} />
                    </button>
                  )}
                </div>

                <div className="category-pills">
                  {["All", "Education", "Business", "Skill Development", "Financial Assistance"].map(
                    (cat) => (
                      <button
                        key={cat}
                        className={`filter-pill ${selectedCategory === cat ? "active" : ""}`}
                        onClick={() => setSelectedCategory(cat)}
                      >
                        {cat}
                      </button>
                    )
                  )}
                </div>
              </div>

              {/* Schemes Grid */}
              <div className="schemes-grid">
                {filteredSchemes.map((scheme) => (
                  <div className="scheme-dashboard-card" key={scheme.code}>
                    <div className="card-top-header">
                      <span className="category-tag">{scheme.category}</span>
                      <button
                        className={`bookmark-action ${savedSchemes.includes(scheme.code) ? "active" : ""
                          }`}
                        onClick={() => toggleSaveScheme(scheme.code)}
                        title={
                          savedSchemes.includes(scheme.code)
                            ? "Remove from favorites"
                            : "Save scheme"
                        }
                      >
                        <Bookmark
                          size={18}
                          fill={savedSchemes.includes(scheme.code) ? "#1E3A8A" : "none"}
                        />
                      </button>
                    </div>
                    <h3>{scheme.name}</h3>
                    <p className="ministry-tag">{scheme.ministry}</p>
                    <p className="card-desc">{scheme.description}</p>
                    <div className="scheme-metrics">
                      <div>
                        <span>Max Assistance</span>
                        <strong>{scheme.maxCost}</strong>
                      </div>
                      <div>
                        <span>Subsidy / Aid</span>
                        <strong>{scheme.subsidy}</strong>
                      </div>
                    </div>
                    <div className="card-actions">
                      <button
                        className="btn-outline-navy"
                        onClick={() => setCatalogModalScheme(scheme)}
                      >
                        View Full Details
                      </button>
                      <button className="btn-solid-navy" onClick={onOpenSchemeAnalyzer}>
                        Analyze Eligibility
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB: NEARBY BANKS */}
          {activeTab === "banks" && (
            <div className="dashboard-view-container">
              <div className="bank-info-card">
                <Building2 size={36} color="#1E3A8A" />
                <div>
                  <h3>Designated Lead District Banks & Nodal Agencies</h3>
                  <p>
                    Every district in India has a designated Lead District Bank (LDB), Regional
                    Rural Bank (RRB), and District Industries Centre (DIC) assigned to sanction
                    welfare loans under MoSJE and MSME convergence.
                  </p>
                  <button
                    className="primary-navy-btn"
                    style={{ marginTop: "1rem" }}
                    onClick={onOpenBanks}
                  >
                    Open District Bank Locator Tool →
                  </button>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    );
  }

  // =========================================================================
  // PRIMARY PUBLIC HOMEPAGE (NAVY BLUE + WHITE THEME)
  // =========================================================================
  return (
    <div className="home-wrapper">
      {/* 1. TOP NAVBAR */}
      <header className="gov-navbar">
        {/* Top Ministry Ribbon */}
        <div className="gov-top-ribbon">
          <div className="ribbon-container">
            <div className="gov-identity">
              <span className="national-emblem-text">भारत सरकार | Government of India</span>
              <span className="separator">•</span>
              <span>Ministry of Social Justice and Empowerment (MoSJE)</span>
            </div>
            <div className="ribbon-right">
              <a href="#contact" className="ribbon-link">
                Helpdesk: 1800-11-2001
              </a>
              <span className="separator">•</span>
              <span className="sih-badge">SIH26092 AI Platform</span>
            </div>
          </div>
        </div>

        {/* Main Navbar */}
        <div className="nav-main-container">
          <div className="nav-brand" onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}>
            <div className="brand-logo-icon">
              <svg viewBox="0 0 40 40" width="36" height="36" fill="none">
                <circle cx="20" cy="20" r="18" stroke="#1E3A8A" strokeWidth="2.5" />
                <path
                  d="M12 20C12 15.58 15.58 12 20 12C24.42 12 28 15.58 28 20C28 24.42 24.42 28 20 28"
                  stroke="#D97706"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                />
                <circle cx="20" cy="20" r="3.5" fill="#1E3A8A" />
                <path d="M20 12V6M20 34V28M12 20H6M34 20H28" stroke="#1E3A8A" strokeWidth="2" strokeLinecap="round" />
              </svg>
            </div>
            <div className="brand-text-block">
              <h1>
                UdyamSetu <span>AI</span>
              </h1>
              <p>AI-Driven Scheme Matching Platform</p>
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <nav className="nav-links-desktop">
            <a href="#home" className="nav-link active">
              Home
            </a>
            <button className="nav-link-btn" onClick={onOpenSchemeAnalyzer}>
              Scheme Analyzer
            </button>
            <a href="#schemes-catalog" className="nav-link">
              All Schemes
            </a>
            <button className="nav-link-btn" onClick={onOpenBanks}>
              Nearby Banks
            </button>
            <a href="#contact" className="nav-link">
              Contact
            </a>
          </nav>

          {/* Right Actions: 8-Language Selector + Login/Register */}
          <div className="nav-actions">
            {/* 8-Language Dropdown */}
            <div className="language-selector-wrapper">
              <button
                className="lang-select-btn"
                onClick={() => setLangDropdownOpen(!langDropdownOpen)}
                aria-label="Select Language"
              >
                <Globe size={16} />
                <span>
                  {LANGUAGES.find((l) => l.code === selectedLanguage)?.label.split(" ")[0] ||
                    "English"}
                </span>
                <span className="arrow-down">▾</span>
              </button>

              {langDropdownOpen && (
                <div className="lang-dropdown-menu">
                  <div className="lang-menu-header">Select Language (8 Languages)</div>
                  {LANGUAGES.map((lang) => (
                    <button
                      key={lang.code}
                      className={`lang-option ${selectedLanguage === lang.code ? "active" : ""}`}
                      onClick={() => {
                        setSelectedLanguage(lang.code);
                        setLangDropdownOpen(false);
                      }}
                    >
                      <span className="lang-code">{lang.code.toUpperCase()}</span>
                      <span className="lang-text">{lang.label}</span>
                      {selectedLanguage === lang.code && <CheckCircle2 size={14} color="#1E3A8A" />}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Auth Buttons */}
            <button className="btn-nav-login" onClick={onLogin}>
              Login
            </button>
            <button className="btn-nav-register" onClick={onRegister || onLogin}>
              Register
            </button>

            {/* Mobile Menu Toggle */}
            <button
              className="mobile-menu-toggle"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label="Toggle Navigation"
            >
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile Dropdown Menu */}
        {mobileMenuOpen && (
          <div className="mobile-nav-panel">
            <a
              href="#home"
              className="mobile-link"
              onClick={() => setMobileMenuOpen(false)}
            >
              Home
            </a>
            <button
              className="mobile-link"
              onClick={() => {
                setMobileMenuOpen(false);
                onOpenSchemeAnalyzer();
              }}
            >
              Scheme Analyzer
            </button>
            <a
              href="#schemes-catalog"
              className="mobile-link"
              onClick={() => setMobileMenuOpen(false)}
            >
              All Schemes
            </a>
            <button
              className="mobile-link"
              onClick={() => {
                setMobileMenuOpen(false);
                onOpenBanks();
              }}
            >
              Nearby Banks
            </button>
            <a
              href="#contact"
              className="mobile-link"
              onClick={() => setMobileMenuOpen(false)}
            >
              Contact
            </a>
            <div className="mobile-auth-row">
              <button className="btn-nav-login" onClick={onLogin}>
                Login
              </button>
              <button className="btn-nav-register" onClick={onRegister || onLogin}>
                Register
              </button>
            </div>
          </div>
        )}
      </header>

      <main id="home">
        {/* =========================================================================
            2. HERO CAROUSEL (FULL-WIDTH WITH LEFT HERO CONTENT, ARROWS, DOTS)
           ========================================================================= */}
        <section
          className="hero-carousel-section"
          onMouseEnter={() => setIsPaused(true)}
          onMouseLeave={() => setIsPaused(false)}
        >
          {CAROUSEL_SLIDES.map((slide, index) => (
            <div
              key={slide.id}
              className={`carousel-slide ${index === currentSlide ? "active" : ""}`}
              style={{ backgroundImage: `url(${slide.image})` }}
            >
              <div className="carousel-navy-overlay"></div>

              <div className="hero-content-container">
                {/* Left Side Hero Content */}
                <div className="hero-text-card">
                  <div className="hero-pill-badge">
                    <Award size={14} />
                    <span>{slide.tag}</span>
                  </div>

                  <h2 className="hero-main-heading">{slide.title}</h2>

                  <p className="hero-subtext">{slide.description}</p>

                  <div className="hero-action-buttons">
                    <button
                      className="btn-hero-primary"
                      onClick={onOpenSchemeAnalyzer}
                    >
                      {slide.primaryCta}
                      <ArrowRight size={18} />
                    </button>

                    <button
                      className="btn-hero-secondary"
                      onClick={() => {
                        if (slide.id === 2 && onOpenBanks) {
                          onOpenBanks();
                        } else {
                          const el = document.getElementById("schemes-catalog");
                          if (el) el.scrollIntoView({ behavior: "smooth" });
                        }
                      }}
                    >
                      {slide.secondaryCta}
                    </button>
                  </div>

                  <div className="hero-slide-stat">
                    <CheckCircle2 size={16} color="#D97706" />
                    <span>{slide.stats}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}

          {/* Carousel Arrows */}
          <button
            className="carousel-arrow prev-arrow"
            onClick={handlePrevSlide}
            aria-label="Previous Slide"
          >
            <ChevronLeft size={28} />
          </button>

          <button
            className="carousel-arrow next-arrow"
            onClick={handleNextSlide}
            aria-label="Next Slide"
          >
            <ChevronRight size={28} />
          </button>

          {/* Slide Indicators (Dots) */}
          <div className="carousel-dots-container">
            {CAROUSEL_SLIDES.map((_, index) => (
              <button
                key={index}
                className={`carousel-dot ${index === currentSlide ? "active" : ""}`}
                onClick={() => setCurrentSlide(index)}
                aria-label={`Go to slide ${index + 1}`}
              ></button>
            ))}
          </div>
        </section>

        {/* =========================================================================
            3. TRUST / ELIGIBILITY — 4 INTERACTIVE ANIMATED FEATURE CARDS
           ========================================================================= */}
        <section className="trust-section">
          <div className="section-header-centered">
            <span className="section-kicker">GOVERNMENT INTEGRATION & TRUST</span>
            <h2>Why Choose UdyamSetu AI Platform?</h2>
            <p>
              Designed for transparency, direct benefit convergence, and financial inclusion for
              Scheduled Castes, traditional artisans, and marginalized entrepreneurs.
            </p>
          </div>

          <div className="trust-grid-container">
            {/* Card 1 */}
            <div
              className={`trust-card animated-card ${activeTrustCard === 0 ? "card-highlighted" : ""}`}
              onMouseEnter={() => setActiveTrustCard(0)}
            >
              <div className="card-accent-line blue-accent"></div>
              <div className="trust-card-top-row">
                <div className="trust-icon-box blue-box">
                  <ShieldCheck size={30} color="#1E3A8A" />
                </div>
                <span className="trust-live-chip">
                  <span className="micro-dot green"></span> Verified Gazette
                </span>
              </div>
              <h3>100% Government Verified</h3>
              <p>
                Strictly indexed from official gazettes and portals of MoSJE, MSME, KVIC, NSFDC,
                NBCFDC, and SIDBI with up-to-date circular guidelines.
              </p>
              <div className="trust-card-bottom-metrics">
                <div className="metric-pill">
                  <strong>99.9%</strong>
                  <span>Official Alignment</span>
                </div>
                <span className="card-highlight-tag">Verified Circulars</span>
              </div>
            </div>

            {/* Card 2 */}
            <div
              className={`trust-card animated-card ${activeTrustCard === 1 ? "card-highlighted" : ""}`}
              onMouseEnter={() => setActiveTrustCard(1)}
            >
              <div className="card-accent-line amber-accent"></div>
              <div className="trust-card-top-row">
                <div className="trust-icon-box amber-box">
                  <Cpu size={30} color="#D97706" />
                </div>
                <span className="trust-live-chip">
                  <span className="micro-dot amber"></span> Neural Engine
                </span>
              </div>
              <h3>AI-Powered Scheme Matching</h3>
              <p>
                Proprietary scoring engine cross-evaluates caste, income ceiling, age limits, and
                project budgets to deliver high-confidence eligibility matches.
              </p>
              <div className="trust-card-bottom-metrics">
                <div className="metric-pill">
                  <strong>&lt; 200ms</strong>
                  <span>Match Speed</span>
                </div>
                <span className="card-highlight-tag">Instant Evaluation</span>
              </div>
            </div>

            {/* Card 3 */}
            <div
              className={`trust-card animated-card ${activeTrustCard === 2 ? "card-highlighted" : ""}`}
              onMouseEnter={() => setActiveTrustCard(2)}
            >
              <div className="card-accent-line green-accent"></div>
              <div className="trust-card-top-row">
                <div className="trust-icon-box green-box">
                  <Coins size={30} color="#059669" />
                </div>
                <span className="trust-live-chip">
                  <span className="micro-dot green"></span> CGTMSE Backed
                </span>
              </div>
              <h3>Collateral-Free & Subsidies</h3>
              <p>
                Discover schemes supported by Central Credit Guarantees (CGTMSE / CGSSI) alongside
                margin money subsidies up to 35% under PMEGP & Stand-Up India.
              </p>
              <div className="trust-card-bottom-metrics">
                <div className="metric-pill">
                  <strong>Up to 35%</strong>
                  <span>Govt Capital Subsidy</span>
                </div>
                <span className="card-highlight-tag">Zero Collateral Up to ₹10L</span>
              </div>
            </div>

            {/* Card 4 */}
            <div
              className={`trust-card animated-card ${activeTrustCard === 3 ? "card-highlighted" : ""}`}
              onMouseEnter={() => setActiveTrustCard(3)}
            >
              <div className="card-accent-line purple-accent"></div>
              <div className="trust-card-top-row">
                <div className="trust-icon-box purple-box">
                  <Building2 size={30} color="#7C3AED" />
                </div>
                <span className="trust-live-chip">
                  <span className="micro-dot purple"></span> 760+ Districts
                </span>
              </div>
              <h3>Lead District Bank Routing</h3>
              <p>
                Directly maps applicant location to designated Lead District Banks (LDBs), Regional
                Rural Banks (RRBs), and District Industries Centres (DICs).
              </p>
              <div className="trust-card-bottom-metrics">
                <div className="metric-pill">
                  <strong>28 States</strong>
                  <span>All-India Network</span>
                </div>
                <span className="card-highlight-tag">Pan-India District Network</span>
              </div>
            </div>
          </div>
        </section>

        {/* =========================================================================
            4. HOW IT WORKS (ANIMATED 3-STEP FLOW & LIVE SIMULATION STAGE)
           ========================================================================= */}
        <section
          className="how-it-works-section"
          id="how-it-works"
          onMouseEnter={() => setIsHowPaused(true)}
          onMouseLeave={() => setIsHowPaused(false)}
        >
          <div className="section-header-centered">
            <span className="section-kicker">INTERACTIVE 3-STEP JOURNEY</span>
            <h2>How UdyamSetu AI Works</h2>
            <p>
              Click any step below to see how your profile transforms into verified government
              welfare credit and bank approvals.
            </p>
          </div>

          {/* Interactive Step Navigation Cards */}
          <div className="steps-flow-container-animated">
            <div className="flow-connecting-rail">
              <div
                className="flow-progress-beam"
                style={{ width: `${(activeHowStep / 2) * 100}%` }}
              ></div>
            </div>

            {/* Step 0 */}
            <div
              className={`step-interactive-card ${activeHowStep === 0 ? "step-active" : ""}`}
              onClick={() => setActiveHowStep(0)}
              role="button"
              tabIndex={0}
            >
              <div className="step-badge-number">
                <span>01</span>
                {activeHowStep === 0 && <span className="step-active-halo"></span>}
              </div>
              <div className="step-icon-wrapper">
                <User size={26} color="#1E3A8A" />
              </div>
              <h3>1. Enter Details</h3>
              <p>
                Provide simple profile information: social category, income, state, and enterprise
                capital needs.
              </p>
              <span className="step-action-pill">
                {activeHowStep === 0 ? "● Simulating Step 1" : "Click to view Step 1"}
              </span>
            </div>

            <div className="step-flow-arrow-animated">
              <ArrowRight size={22} />
            </div>

            {/* Step 1 */}
            <div
              className={`step-interactive-card ${activeHowStep === 1 ? "step-active" : ""}`}
              onClick={() => setActiveHowStep(1)}
              role="button"
              tabIndex={0}
            >
              <div className="step-badge-number">
                <span>02</span>
                {activeHowStep === 1 && <span className="step-active-halo"></span>}
              </div>
              <div className="step-icon-wrapper">
                <Sparkles size={26} color="#D97706" />
              </div>
              <h3>2. Discover Schemes</h3>
              <p>
                Our AI algorithm scores 15+ Central policies, calculating your match rate and
                capital subsidy grants.
              </p>
              <span className="step-action-pill">
                {activeHowStep === 1 ? "● Simulating Step 2" : "Click to view Step 2"}
              </span>
            </div>

            <div className="step-flow-arrow-animated">
              <ArrowRight size={22} />
            </div>

            {/* Step 2 */}
            <div
              className={`step-interactive-card ${activeHowStep === 2 ? "step-active" : ""}`}
              onClick={() => setActiveHowStep(2)}
              role="button"
              tabIndex={0}
            >
              <div className="step-badge-number">
                <span>03</span>
                {activeHowStep === 2 && <span className="step-active-halo"></span>}
              </div>
              <div className="step-icon-wrapper">
                <Building2 size={26} color="#1E3A8A" />
              </div>
              <h3>3. Connect with Partners</h3>
              <p>
                Generate your DPR, check documentation checklists, and approach designated Lead
                Bank branches.
              </p>
              <span className="step-action-pill">
                {activeHowStep === 2 ? "● Simulating Step 3" : "Click to view Step 3"}
              </span>
            </div>
          </div>

          {/* DYNAMIC LIVE SIMULATION SHOWCASE STAGE */}
          <div className="how-simulation-stage">
            <div className="stage-top-bar">
              <div className="stage-indicator">
                <span className="stage-pulse-dot"></span>
                <strong>Live Workflow Simulation</strong>
                <span className="stage-step-tag">
                  Step {activeHowStep + 1} of 3:{" "}
                  {activeHowStep === 0 && "Profile Input & Verification"}
                  {activeHowStep === 1 && "AI Scoring & Subsidy Identification"}
                  {activeHowStep === 2 && "Lead Bank & Nodal Office Routing"}
                </span>
              </div>
              <div className="stage-nav-dots">
                {[0, 1, 2].map((st) => (
                  <button
                    key={st}
                    className={`nav-stage-dot ${activeHowStep === st ? "active" : ""}`}
                    onClick={() => setActiveHowStep(st)}
                    aria-label={`Jump to step ${st + 1}`}
                  ></button>
                ))}
              </div>
            </div>

            {/* STAGE CONTENT: STEP 0 (ENTER DETAILS) */}
            {activeHowStep === 0 && (
              <div className="stage-view-content animated-fade-in">
                <div className="stage-grid-two-col">
                  <div className="sim-profile-card">
                    <div className="sim-card-header">
                      <div className="sim-avatar">RK</div>
                      <div>
                        <h4>Rajesh Kumar</h4>
                        <span>Beneficiary Entrepreneur Profile</span>
                      </div>
                      <span className="sim-verified-tag">✓ Verified Input</span>
                    </div>

                    <div className="sim-details-rows">
                      <div className="sim-detail-cell">
                        <span className="cell-label">Social Category</span>
                        <strong className="cell-val">SC (Scheduled Caste)</strong>
                      </div>
                      <div className="sim-detail-cell">
                        <span className="cell-label">Annual Income</span>
                        <strong className="cell-val">₹2,40,000 / year</strong>
                      </div>
                      <div className="sim-detail-cell">
                        <span className="cell-label">Required Capital</span>
                        <strong className="cell-val highlight-gold">₹15,00,000</strong>
                      </div>
                      <div className="sim-detail-cell">
                        <span className="cell-label">Resident District</span>
                        <strong className="cell-val">Varanasi, Uttar Pradesh</strong>
                      </div>
                    </div>

                    <div className="sim-progress-bar-wrap">
                      <div className="sim-bar-label">
                        <span>Profile Completeness</span>
                        <strong>100% Ready</strong>
                      </div>
                      <div className="sim-bar-track">
                        <div className="sim-bar-fill green-fill" style={{ width: "100%" }}></div>
                      </div>
                    </div>
                  </div>

                  <div className="sim-explanation-card">
                    <div className="sim-expl-icon">
                      <Cpu size={28} color="#1E3A8A" />
                    </div>
                    <h3>AI Matching Algorithm Activation</h3>
                    <p>
                      The system ingests applicant income limits, social target groups, and
                      geographic district mappings without requiring manual circular lookups.
                    </p>
                    <ul className="sim-checklist">
                      <li>✓ Evaluates double poverty line & income ceilings</li>
                      <li>✓ Filters concessional interest rate brackets (4% – 6%)</li>
                      <li>✓ Matches manufacturing vs services capital allowances</li>
                    </ul>
                    <button
                      className="btn-sim-forward"
                      onClick={() => setActiveHowStep(1)}
                    >
                      Simulate Step 2: AI Matching Engine →
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* STAGE CONTENT: STEP 1 (DISCOVER SCHEMES) */}
            {activeHowStep === 1 && (
              <div className="stage-view-content animated-fade-in">
                <div className="stage-grid-two-col">
                  <div className="sim-results-card">
                    <div className="sim-results-header">
                      <div>
                        <h4>AI Match Confidence Engine</h4>
                        <span>Ranked results for SC Entrepreneur in Varanasi</span>
                      </div>
                      <span className="match-time-badge">⚡ 142ms Match Speed</span>
                    </div>

                    <div className="sim-matched-schemes-list">
                      {/* Scheme 1 */}
                      <div className="matched-item-bar top-match">
                        <div className="item-title-row">
                          <strong>Stand-Up India Scheme</strong>
                          <span className="score-badge gold">94% MATCH</span>
                        </div>
                        <p className="item-sub">Composite Loan up to ₹1 Crore (15% Margin Money Grant)</p>
                        <div className="item-progress-track">
                          <div className="item-progress-fill" style={{ width: "94%" }}></div>
                        </div>
                      </div>

                      {/* Scheme 2 */}
                      <div className="matched-item-bar">
                        <div className="item-title-row">
                          <strong>PMEGP (Prime Minister’s Employment Generation)</strong>
                          <span className="score-badge green">91% MATCH</span>
                        </div>
                        <p className="item-sub">35% Capital Subsidy (₹5,25,000 Govt Margin Grant)</p>
                        <div className="item-progress-track">
                          <div className="item-progress-fill green" style={{ width: "91%" }}></div>
                        </div>
                      </div>

                      {/* Scheme 3 */}
                      <div className="matched-item-bar">
                        <div className="item-title-row">
                          <strong>NSFDC Term Loan (National SC Finance Corp)</strong>
                          <span className="score-badge blue">88% MATCH</span>
                        </div>
                        <p className="item-sub">Concessional 5% Interest Rate through State Channelizing Agency</p>
                        <div className="item-progress-track">
                          <div className="item-progress-fill blue" style={{ width: "88%" }}></div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="sim-explanation-card">
                    <div className="sim-expl-icon">
                      <Coins size={28} color="#059669" />
                    </div>
                    <h3>Capital Subsidy Calculation</h3>
                    <p>
                      UdyamSetu AI determines the maximum non-repayable grant you are entitled to,
                      drastically reducing your effective bank loan EMI.
                    </p>
                    <div className="subsidy-callout-box">
                      <span>Calculated Capital Subsidy</span>
                      <strong>₹5,25,000</strong>
                      <small>KVIC Margin Money TDR credited directly to bank</small>
                    </div>
                    <button
                      className="btn-sim-forward"
                      onClick={() => setActiveHowStep(2)}
                    >
                      Simulate Step 3: Bank Routing →
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* STAGE CONTENT: STEP 2 (CONNECT WITH PARTNERS) */}
            {activeHowStep === 2 && (
              <div className="stage-view-content animated-fade-in">
                <div className="stage-grid-two-col">
                  <div className="sim-bank-routing-card">
                    <div className="sim-bank-header">
                      <Building2 size={24} color="#1E3A8A" />
                      <div>
                        <h4>Designated Nodal Network</h4>
                        <span>Mapped for Varanasi District, Uttar Pradesh</span>
                      </div>
                      <span className="routing-ready-badge">Ready for Sanction</span>
                    </div>

                    <div className="bank-branch-details-box">
                      <div className="branch-meta-row">
                        <span className="branch-label">Designated Lead District Bank</span>
                        <strong>Union Bank of India (Varanasi LDM Office)</strong>
                        <p>Specialized MSME & Priority Sector Lending Desk, Sigra Branch</p>
                      </div>

                      <div className="branch-meta-row">
                        <span className="branch-label">Regional Rural Bank (RRB)</span>
                        <strong>Baroda UP Gramin Bank</strong>
                        <p>Designated rural lending arm for priority sector subsidies</p>
                      </div>

                      <div className="branch-meta-row">
                        <span className="branch-label">District Nodal Office</span>
                        <strong>District Industries Centre (DIC), Chandpur</strong>
                        <p>Issues physical verification & KVIC subsidy recommendation</p>
                      </div>
                    </div>
                  </div>

                  <div className="sim-explanation-card">
                    <div className="sim-expl-icon">
                      <ShieldCheck size={28} color="#1E3A8A" />
                    </div>
                    <h3>Complete Bank Appraisal Package</h3>
                    <p>
                      Walk into the branch with an automatically generated Detailed Project Report
                      (DPR), subsidy sanction documents, and CGTMSE guarantee certificate.
                    </p>
                    <div className="ready-checklist">
                      <span>✓ DPR Financial Projections Ready</span>
                      <span>✓ CGTMSE Collateral-Free Certificate</span>
                      <span>✓ Nodal Agency Direct Application Link</span>
                    </div>
                    <div className="sim-final-cta-row">
                      <button
                        className="btn-sim-launch"
                        onClick={onOpenSchemeAnalyzer}
                      >
                        Launch Scheme Analyzer Now →
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="how-cta-center">
            <button className="primary-navy-btn" onClick={onOpenSchemeAnalyzer}>
              Launch Scheme Analyzer Now <ArrowRight size={18} />
            </button>
          </div>
        </section>

        {/* =========================================================================
            5. FEATURED SCHEME CATEGORIES (EDUCATION, BUSINESS, SKILL, FINANCIAL)
           ========================================================================= */}
        <section className="categories-section" id="schemes-catalog">
          <div className="section-header-centered">
            <span className="section-kicker">CURATED BENEFICIARY DOMAINS</span>
            <h2>Explore Schemes by Category</h2>
            <p>
              Browse priority welfare programs structured across education, enterprise, traditional
              crafts, and direct financial subsidies.
            </p>
          </div>

          <div className="categories-grid-container">
            {/* Category 1: Education */}
            <div
              className="category-showcase-card"
              onClick={() => {
                setSelectedCategory("Education");
                const el = document.getElementById("catalog-details");
                if (el) el.scrollIntoView({ behavior: "smooth" });
              }}
            >
              <div className="category-card-top">
                <div className="cat-icon-container education-bg">
                  <GraduationCap size={32} color="#1E3A8A" />
                </div>
                <span className="cat-badge">Scholarships & Loans</span>
              </div>
              <h3>Education</h3>
              <p>
                Post-matric scholarships, Top Class Education for SC students, and 100% funded
                National Overseas Scholarships for prestigious global degrees.
              </p>
              <ul className="cat-scheme-points">
                <li>• National Overseas Scholarship (NOS)</li>
                <li>• Post-Matric SC/ST Scholarships</li>
                <li>• Concessional Higher Education Loans</li>
              </ul>
              <div className="cat-card-action">
                <span>View Education Schemes →</span>
              </div>
            </div>

            {/* Category 2: Business */}
            <div
              className="category-showcase-card"
              onClick={() => {
                setSelectedCategory("Business");
                const el = document.getElementById("catalog-details");
                if (el) el.scrollIntoView({ behavior: "smooth" });
              }}
            >
              <div className="category-card-top">
                <div className="cat-icon-container business-bg">
                  <Briefcase size={32} color="#1E3A8A" />
                </div>
                <span className="cat-badge">₹10L – ₹1 Crore</span>
              </div>
              <h3>Business & MSME</h3>
              <p>
                Greenfield loans under Stand-Up India, credit-linked margin money grants under PMEGP,
                and micro-enterprise loans under PM MUDRA Yojana.
              </p>
              <ul className="cat-scheme-points">
                <li>• Stand-Up India Scheme (₹10L – ₹1Cr)</li>
                <li>• PMEGP (Up to 35% Capital Subsidy)</li>
                <li>• PM MUDRA Yojana (Shishu, Kishore, Tarun)</li>
              </ul>
              <div className="cat-card-action">
                <span>View Business Schemes →</span>
              </div>
            </div>

            {/* Category 3: Skill Development */}
            <div
              className="category-showcase-card"
              onClick={() => {
                setSelectedCategory("Skill Development");
                const el = document.getElementById("catalog-details");
                if (el) el.scrollIntoView({ behavior: "smooth" });
              }}
            >
              <div className="category-card-top">
                <div className="cat-icon-container skill-bg">
                  <Wrench size={32} color="#1E3A8A" />
                </div>
                <span className="cat-badge">Artisans & Crafts</span>
              </div>
              <h3>Skill Development</h3>
              <p>
                PM Vishwakarma comprehensive support with digital ID, ₹15,000 modern toolkit
                incentives, stipend-supported skill training, and 5% interest loans.
              </p>
              <ul className="cat-scheme-points">
                <li>• PM Vishwakarma Scheme (18 Trades)</li>
                <li>• ₹15,000 Free Modern Toolkit Voucher</li>
                <li>• Daily Stipend-Based Advanced Training</li>
              </ul>
              <div className="cat-card-action">
                <span>View Skill Schemes →</span>
              </div>
            </div>

            {/* Category 4: Financial Assistance */}
            <div
              className="category-showcase-card"
              onClick={() => {
                setSelectedCategory("Financial Assistance");
                const el = document.getElementById("catalog-details");
                if (el) el.scrollIntoView({ behavior: "smooth" });
              }}
            >
              <div className="category-card-top">
                <div className="cat-icon-container finance-bg">
                  <Coins size={32} color="#1E3A8A" />
                </div>
                <span className="cat-badge">Concessional Rates</span>
              </div>
              <h3>Financial Assistance</h3>
              <p>
                Direct term loans through National Scheduled Castes Finance Corporation (NSFDC) at
                4% to 6% per annum, SVANidhi vendor loans, and interest subvention.
              </p>
              <ul className="cat-scheme-points">
                <li>• NSFDC Term Loan (4% – 6% Interest)</li>
                <li>• PM SVANidhi Working Capital</li>
                <li>• NBCFDC & NSKFDC Micro-Credit</li>
              </ul>
              <div className="cat-card-action">
                <span>View Financial Aid →</span>
              </div>
            </div>
          </div>

          {/* Interactive Scheme Catalog Preview Table */}
          <div className="catalog-interactive-preview" id="catalog-details">
            <div className="preview-toolbar">
              <div className="preview-title">
                <h3>Structured Schemes Catalog</h3>
                <span>Filter or search below to explore criteria and assistance</span>
              </div>

              <div className="preview-search-box">
                <Search size={16} />
                <input
                  type="text"
                  placeholder="Quick search schemes..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </div>

            <div className="scheme-cards-compact-row">
              {filteredSchemes.slice(0, 6).map((item) => (
                <div className="compact-scheme-card" key={item.code}>
                  <div className="compact-card-header">
                    <span className="tag-pill">{item.category}</span>
                    <span className="cost-pill">{item.maxCost}</span>
                  </div>
                  <h4>{item.name}</h4>
                  <p className="ministry-sub">{item.ministry}</p>
                  <p className="compact-desc">{item.description}</p>
                  <div className="compact-card-footer">
                    <span className="aid-note">{item.subsidy}</span>
                    <button
                      className="btn-details-link"
                      onClick={() => setCatalogModalScheme(item)}
                    >
                      Details & Criteria →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* =========================================================================
            6. SCHEME ANALYZER CTA BANNER
           ========================================================================= */}
        <section className="analyzer-cta-banner">
          <div className="cta-banner-container">
            <div className="cta-banner-left">
              <div className="cta-badge">
                <Cpu size={16} /> AI-Powered Eligibility Engine
              </div>
              <h2>Ready to Discover Which Government Schemes You Qualify For?</h2>
              <p>
                Input your social category, family income, and enterprise capital requirement. Our
                AI Scheme Analyzer instantly generates your match scores, identifies capital
                subsidies, and maps your designated Lead District Bank.
              </p>
              <div className="cta-perks-row">
                <span>✓ 100% Free & Transparent</span>
                <span>✓ Direct MoSJE & MSME Convergence</span>
                <span>✓ Instant DPR Breakdown</span>
              </div>
            </div>

            <div className="cta-banner-right">
              <button className="cta-primary-btn" onClick={onOpenSchemeAnalyzer}>
                Launch Scheme Analyzer <ArrowRight size={20} />
              </button>
              <button className="cta-secondary-btn" onClick={onOpenBanks}>
                Locate Nearby Banks
              </button>
            </div>
          </div>
        </section>
      </main>

      {/* =========================================================================
          7. FOOTER (GOVERNMENT OF INDIA & MoSJE THEMED)
         ========================================================================= */}
      <footer className="gov-footer" id="contact">
        <div className="footer-main-container">
          {/* Col 1: About & Identity */}
          <div className="footer-col brand-col">
            <div className="footer-brand">
              <div className="footer-emblem-icon">SS</div>
              <div>
                <h3>UdyamSetu AI</h3>
                <p>Ministry of Social Justice & Empowerment Initiative</p>
              </div>
            </div>
            <p className="footer-about-text">
              An advanced AI-powered scheme discovery and financial routing platform developed for
              the Smart India Hackathon (SIH26092). Dedicated to uplifting Scheduled Castes,
              traditional artisans, and marginalized entrepreneurs.
            </p>
            <div className="footer-national-tag">
              <span>National Portal of India Convergence</span>
            </div>
          </div>

          {/* Col 2: Quick Links */}
          <div className="footer-col">
            <h4>Quick Links</h4>
            <ul className="footer-link-list">
              <li>
                <a href="#home">Home</a>
              </li>
              <li>
                <button className="link-button" onClick={onOpenSchemeAnalyzer}>
                  Scheme Analyzer
                </button>
              </li>
              <li>
                <a href="#schemes-catalog">All Schemes</a>
              </li>
              <li>
                <button className="link-button" onClick={onOpenBanks}>
                  Nearby Banks
                </button>
              </li>
              <li>
                <button className="link-button" onClick={onLogin}>
                  Beneficiary Login
                </button>
              </li>
            </ul>
          </div>

          {/* Col 3: Government Portals */}
          <div className="footer-col">
            <h4>Official Portals</h4>
            <ul className="footer-link-list">
              <li>
                <a href="https://socialjustice.gov.in" target="_blank" rel="noreferrer">
                  MoSJE Official Portal ↗
                </a>
              </li>
              <li>
                <a href="https://pmvishwakarma.gov.in" target="_blank" rel="noreferrer">
                  PM Vishwakarma Portal ↗
                </a>
              </li>
              <li>
                <a href="https://www.standupmitra.in" target="_blank" rel="noreferrer">
                  Stand-Up Mitra Portal ↗
                </a>
              </li>
              <li>
                <a href="https://kviconline.gov.in" target="_blank" rel="noreferrer">
                  KVIC PMEGP Portal ↗
                </a>
              </li>
              <li>
                <a href="https://nsfdc.nic.in" target="_blank" rel="noreferrer">
                  NSFDC India Portal ↗
                </a>
              </li>
            </ul>
          </div>

          {/* Col 4: Helpdesk & Contact */}
          <div className="footer-col contact-col">
            <h4>National Helpdesk</h4>
            <div className="contact-detail-row">
              <Phone size={18} color="#D97706" />
              <div>
                <strong>Toll-Free Helplines</strong>
                <p>1800-11-2001 (MoSJE Assistance)</p>
                <p>1800-180-6763 (Stand-Up India)</p>
              </div>
            </div>
            <div className="contact-detail-row">
              <Mail size={18} color="#D97706" />
              <div>
                <strong>Email Support</strong>
                <p>support-udyamsetu@gov.in</p>
              </div>
            </div>
            <div className="contact-detail-row">
              <MapPin size={18} color="#D97706" />
              <div>
                <strong>Headquarters</strong>
                <p>Shastri Bhawan, Dr. Rajendra Prasad Road, New Delhi 110001</p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer Bottom Bar */}
        <div className="footer-bottom-bar">
          <div className="footer-bottom-container">
            <p>© 2026 UdyamSetu AI Platform • Smart India Hackathon (SIH26092). All Rights Reserved.</p>
            <div className="footer-bottom-links">
              <span>Security & Privacy</span>
              <span className="separator">•</span>
              <span>Terms of Use</span>
              <span className="separator">•</span>
              <span>National Informatics Standards</span>
            </div>
          </div>
        </div>
      </footer>

      {/* MODAL: SCHEME DETAILS PREVIEW */}
      {catalogModalScheme && (
        <div className="scheme-modal-backdrop" onClick={() => setCatalogModalScheme(null)}>
          <div className="scheme-modal-card" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div>
                <span className="modal-category">{catalogModalScheme.category}</span>
                <h3>{catalogModalScheme.name}</h3>
                <span className="modal-ministry">{catalogModalScheme.ministry}</span>
              </div>
              <button className="modal-close-btn" onClick={() => setCatalogModalScheme(null)}>
                <X size={20} />
              </button>
            </div>

            <div className="modal-body">
              <p className="modal-description">{catalogModalScheme.description}</p>
              <div className="modal-specs-grid">
                <div className="modal-spec-item">
                  <span>Eligible Target Group</span>
                  <strong>{catalogModalScheme.target}</strong>
                </div>
                <div className="modal-spec-item">
                  <span>Maximum Assistance</span>
                  <strong>{catalogModalScheme.maxCost}</strong>
                </div>
                <div className="modal-spec-item">
                  <span>Government Subsidy / Incentive</span>
                  <strong>{catalogModalScheme.subsidy}</strong>
                </div>
                <div className="modal-spec-item">
                  <span>Concessional Interest</span>
                  <strong>{catalogModalScheme.interest}</strong>
                </div>
              </div>
            </div>

            <div className="modal-footer">
              <button
                className="btn-outline-navy"
                onClick={() => {
                  toggleSaveScheme(catalogModalScheme.code);
                }}
              >
                {savedSchemes.includes(catalogModalScheme.code)
                  ? "✓ Saved in Favorites"
                  : "+ Add to Favorites"}
              </button>
              <button
                className="btn-solid-navy"
                onClick={() => {
                  setCatalogModalScheme(null);
                  onOpenSchemeAnalyzer();
                }}
              >
                Check My Eligibility Score →
              </button>
            </div>
          </div>
        </div>
      )}

      <div className={`credit-assistant ${chatOpen ? "is-open" : ""}`}>
        {chatOpen && (
          <section className="credit-assistant-panel" aria-label="SC Credit Assistant">
            <header className="credit-assistant-header">
              <div className="credit-assistant-heading">
                <span className="credit-assistant-avatar"><MessageCircle size={16} /></span>
                <div>
                  <strong>SC Credit Assistant</strong>
                  <span><i /> Online</span>
                </div>
              </div>
              <button
                className="credit-assistant-close"
                type="button"
                onClick={() => setChatOpen(false)}
                aria-label="Close chat"
              >
                <X size={16} />
              </button>
            </header>

            <div className="credit-assistant-messages" aria-live="polite">
              {chatMessages.map((message, index) => (
                <div className={`credit-assistant-message ${message.role}`} key={`${message.role}-${index}`}>
                  {message.role === "assistant" && (
                    <span className="credit-assistant-mini-avatar"><MessageCircle size={13} /></span>
                  )}
                  <p>{message.content}</p>
                </div>
              ))}
            </div>

            <form className="credit-assistant-form" onSubmit={handleChatSubmit}>
              <input
                type="text"
                placeholder="Type your question..."
                value={chatInput}
                onChange={(event) => setChatInput(event.target.value)}
                aria-label="Type your question"
              />
              <button type="submit" aria-label="Send question" disabled={!chatInput.trim()}>
                <Send size={16} />
              </button>
            </form>
          </section>
        )}

        {!chatOpen && (
          <button
            className="credit-assistant-launcher"
            type="button"
            onClick={() => setChatOpen(true)}
            aria-label="Open SC Credit Assistant"
          >
            <MessageCircle size={24} />
            <span className="credit-assistant-pulse" />
          </button>
        )}
      </div>
    </div>
  );
}