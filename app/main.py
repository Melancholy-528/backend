import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.schemas.applicant import Applicant
from app.schemas.scheme import Scheme
from app.schemas.user import UserSignUp, UserLogin, UserResponse, UserUpdate, TokenResponse
from app.services.eligibility import check_eligibility
from app.services.ollama_service import ollama_service
from app.services.chatbot import chatbot, ChatRequest, ChatResponse
from app.services.bank_locator import bank_locator, BankRecommendation, DISTRICT_BANK_DATABASE
from app.services.dpr_calculator import dpr_calculator, DPRRequest, DPRResponse
from app.services.auth_service import auth_service, get_current_user
from app.miner.source_catalog import catalog, GovernmentSource
from app.miner.crawler import crawl_sources
from app.miner.scheme_miner import mine_url, save_mined_data

app = FastAPI(
    title="SIH26092 AI-Driven Scheme Matching Engine",
    description="AI-powered government welfare and enterprise scheme matching platform for marginalized entrepreneurs (MoSJE).",
    version="1.0.0",
)

# Enable CORS for frontend integration (React, Vite, Next.js, mobile app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMES_PATH = BASE_DIR / "schemes.json"


def get_schemes_path() -> Path:
    """Return the active path to schemes.json (configurable via SCHEMES_PATH env var)."""
    env_path = os.getenv("SCHEMES_PATH")
    if env_path:
        return Path(env_path)
    return SCHEMES_PATH


def load_schemes_from_file() -> List[Scheme]:
    """Load and parse structured schemes from schemes.json."""
    path = get_schemes_path()
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Scheme(**item) for item in data.get("schemes", [])]
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return []


def load_documents_from_file() -> List[dict]:
    """Load raw mined documents from schemes.json."""
    path = get_schemes_path()
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("documents", [])
    except Exception:
        return []


class MineRequest(BaseModel):
    url: str
    follow_pdfs: bool = True


class CrawlRequest(BaseModel):
    ministry: Optional[str] = None
    category: Optional[str] = None
    tag: Optional[str] = None
    source_ids: Optional[List[str]] = None
    follow_pdfs: bool = True


@app.get("/")
def root():
    schemes = load_schemes_from_file()
    return {
        "title": "SIH26092 - AI-Driven Scheme Matching Platform",
        "ministry": "Ministry of Social Justice and Empowerment (MoSJE)",
        "status": "online",
        "total_schemes_indexed": len(schemes),
        "endpoints": {
            "GET /schemes": "List all structured government schemes (supports filters)",
            "GET /schemes/{scheme_code}": "Get details of a specific scheme",
            "POST /match": "Match an applicant profile against indexed schemes",
            "POST /chat": "AI Scheme Advisory Chatbot powered by local Ollama & RAG",
            "POST /chat/stream": "Real-time streaming AI chatbot responses for frontend UI",
            "GET /chat/health": "Health and model status for Ollama chat service",
            "GET /miner/sources": "List pre-configured and automated government scheme sources",
            "POST /miner/sources": "Add new government source to registry",
            "POST /miner/crawl": "Trigger automated batch crawl across government sources",
            "POST /miner/mine": "Mine structured scheme data directly from any web URL or PDF URL",
            "POST /miner/mine-file": "Upload and mine a PDF or document directly",
            "GET /miner/documents": "View raw extracted document records",
            "GET /banks/nearby": "Recommend designated Lead District Banks, RRBs, and DIC offices for a scheme and location",
            "GET /banks/districts": "List mapped states and districts with Lead Bank profiles",
            "POST /calculator/dpr": "Generate Detailed Project Report (DPR), subsidy breakdown, and EMI schedule for bank loans",
            "GET /analytics/summary": "Ministry policy and demand analytics dashboard",
            "POST /auth/signup": "Register a new beneficiary user account and receive JWT token",
            "POST /auth/login": "Authenticate with email and password and receive JWT token",
            "GET /auth/me": "Get current authenticated user profile",
            "PUT /auth/me": "Update profile details of logged-in user",
            "POST /users/saved-schemes/{code}": "Bookmark a scheme to user dashboard",
            "DELETE /users/saved-schemes/{code}": "Remove a bookmarked scheme from user dashboard",
            "GET /users/saved-schemes": "Get full details of all schemes bookmarked by the user",
        },
    }


@app.get("/schemes", response_model=List[Scheme])
def get_schemes(
    category: Optional[str] = Query(None, description="Filter by applicant category (e.g. SC, ST, OBC, Women, Artisan)"),
    max_project_cost: Optional[int] = Query(None, description="Filter schemes that support at least this project cost"),
    q: Optional[str] = Query(None, description="Keyword search in scheme title or description"),
):
    schemes = load_schemes_from_file()

    if category:
        norm_cat = category.strip().upper()
        schemes = [
            s for s in schemes
            if any(c.strip().upper() == norm_cat or c.strip().upper() in ["ALL", "GENERAL"] for c in s.eligible_categories)
            or (s.eligible_category and norm_cat in s.eligible_category.upper())
        ]

    if max_project_cost:
        schemes = [
            s for s in schemes
            if s.max_project_cost is None or s.max_project_cost >= max_project_cost
        ]

    if q:
        query_lower = q.lower()
        schemes = [
            s for s in schemes
            if query_lower in s.name.lower() or (s.description and query_lower in s.description.lower())
        ]

    return schemes


@app.get("/schemes/{code_or_name}")
def get_scheme_by_code(code_or_name: str):
    schemes = load_schemes_from_file()
    target = code_or_name.strip().lower()

    for s in schemes:
        if (s.scheme_code and s.scheme_code.lower() == target) or s.name.lower() == target:
            return s

    raise HTTPException(status_code=404, detail=f"Scheme '{code_or_name}' not found")


@app.post("/match")
def match(applicant: Applicant):
    schemes = load_schemes_from_file()
    eligible_matches = []
    ineligible_matches = []

    for scheme in schemes:
        result = check_eligibility(applicant, scheme)
        if result["eligible"]:
            eligible_matches.append(result)
        else:
            ineligible_matches.append(result)

    # Sort eligible matches by highest match score first
    eligible_matches.sort(key=lambda x: x["score"], reverse=True)

    return {
        "applicant": applicant.model_dump(),
        "summary": {
            "total_evaluated": len(schemes),
            "total_eligible": len(eligible_matches),
            "total_ineligible": len(ineligible_matches),
        },
        "matches": eligible_matches,
        "ineligible": ineligible_matches,
    }


@app.post("/miner/mine")
def mine_scheme_endpoint(request: MineRequest):
    try:
        scheme, doc = mine_url(request.url, follow_pdfs=request.follow_pdfs)
        save_mined_data([scheme], [doc], filename=str(get_schemes_path()))
        return {
            "status": "success",
            "message": f"Successfully mined and indexed scheme '{scheme.name}'",
            "scheme": scheme,
            "document_preview": {
                "title": doc.get("title"),
                "scheme_code": doc.get("scheme_code"),
                "text_length": len(doc.get("text", "")),
                "source_url": doc.get("source_url"),
            },
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to mine URL: {str(e)}")


@app.post("/miner/mine-file")
def mine_file_endpoint(file: UploadFile = File(...)):
    suffix = Path(file.filename or "temp.pdf").suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        scheme, doc = mine_url(tmp_path, follow_pdfs=False)
        scheme.source_url = file.filename
        doc["source_url"] = file.filename
        save_mined_data([scheme], [doc], filename=str(get_schemes_path()))
        return {
            "status": "success",
            "message": f"Successfully mined and indexed scheme from uploaded file '{file.filename}'",
            "scheme": scheme,
            "document_preview": {
                "title": doc.get("title"),
                "text_length": len(doc.get("text", "")),
                "source_file": file.filename,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to mine uploaded file: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.get("/miner/documents")
def get_mined_documents():
    docs = load_documents_from_file()
    return [
        {
            "title": d.get("title"),
            "scheme_code": d.get("scheme_code"),
            "source_url": d.get("source_url"),
            "text_preview": d.get("text", "")[:300] + "..." if len(d.get("text", "")) > 300 else d.get("text", ""),
            "full_length": len(d.get("text", "")),
        }
        for d in docs
    ]


# ==========================================
# AI Chatbot & RAG Endpoints (Ollama Powered)
# ==========================================

@app.get("/chat/health")
def chat_health():
    """Check health of the Ollama AI chatbot service and loaded model."""
    is_online = ollama_service.is_available()
    models = ollama_service.get_available_models() if is_online else []
    active_model = ollama_service.get_best_model() if is_online else None
    schemes = load_schemes_from_file()
    return {
        "status": "online" if is_online else "offline",
        "engine": "Ollama Local LLM",
        "active_model": active_model,
        "available_models": models,
        "fallback_available": True,
        "total_schemes_indexed": len(schemes),
    }


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Interact with the Scheme Advisor Chatbot.
    Ask any questions about eligibility, documentation, subsidy, or application guidelines.
    """
    schemes = load_schemes_from_file()
    docs = load_documents_from_file()
    return chatbot.answer(request=request, schemes=schemes, documents=docs)


@app.post("/chat/stream")
def chat_stream_endpoint(request: ChatRequest):
    """
    Real-time streaming chatbot endpoint for frontend chat interfaces.
    Streams answer tokens as they are generated by Ollama.
    """
    schemes = load_schemes_from_file()
    docs = load_documents_from_file()
    return StreamingResponse(
        chatbot.stream_answer(request=request, schemes=schemes, documents=docs),
        media_type="text/plain",
    )


# ==========================================
# Automated Source Catalog & Batch Crawler
# ==========================================

@app.get("/miner/sources")
def get_sources_endpoint(
    ministry: Optional[str] = Query(None, description="Filter by ministry name"),
    category: Optional[str] = Query(None, description="Filter by target category (SC, ST, OBC, Women, Artisan)"),
    tag: Optional[str] = Query(None, description="Filter by tag (credit, subsidy, etc.)"),
    state: Optional[str] = Query(None, description="Filter by state name (or empty string for Central)"),
):
    """List all pre-configured and automated government scheme sources in the registry."""
    sources = catalog.filter_sources(ministry=ministry, category=category, tag=tag, state=state)
    return {
        "total_sources": len(sources),
        "available_ministries": catalog.get_unique_ministries(),
        "available_categories": catalog.get_unique_categories(),
        "sources": sources,
    }


@app.post("/miner/sources")
def add_source_endpoint(source: GovernmentSource):
    """Register a new government source into the automated miner catalog."""
    catalog.add_source(source)
    return {
        "status": "success",
        "message": f"Added source '{source.name}' ({source.id}) to catalog",
        "source": source,
    }


@app.post("/miner/crawl")
def crawl_sources_endpoint(request: CrawlRequest):
    """
    Trigger automated batch crawling across government sources.
    Discovers circulars, guideline PDFs, and extracts structured schemes without manual URL entry.
    """
    try:
        result = crawl_sources(
            ministry=request.ministry,
            category=request.category,
            tag=request.tag,
            source_ids=request.source_ids,
            follow_pdfs=request.follow_pdfs,
            output_file=str(get_schemes_path()),
        )
        return {
            "status": "success",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crawl failed: {str(e)}")


# ==========================================
# Nearby Bank Locator & Nodal Routing Endpoints
# ==========================================

@app.get("/banks/districts")
def get_supported_districts():
    """List states and districts with pre-mapped Lead District Banks and Nodal agencies."""
    result = {}
    for st, dists in DISTRICT_BANK_DATABASE.items():
        result[st.title()] = sorted([d.title() for d in dists.keys()])
    return {
        "mapped_states_count": len(result),
        "states": result,
        "all_india_coverage": True,
    }


@app.get("/banks/nearby", response_model=BankRecommendation)
def get_nearby_banks(
    scheme_code: str = Query(..., description="Government scheme code (e.g. STANDUP-INDIA, PMEGP, PM-VISHWAKARMA)"),
    state: str = Query(..., description="Applicant state (e.g. Uttar Pradesh, Maharashtra, Tamil Nadu)"),
    district: Optional[str] = Query(None, description="Applicant district (e.g. Varanasi, Pune, Coimbatore)"),
):
    """
    Recommend designated Lead Banks, Regional Rural Banks (RRBs), participating commercial branches,
    and District Nodal Agencies (DIC, LDM office) based on the scheme and applicant location.
    """
    schemes = load_schemes_from_file()
    scheme_name = scheme_code
    for s in schemes:
        if s.scheme_code and s.scheme_code.upper() == scheme_code.upper():
            scheme_name = s.name
            break

    return bank_locator.recommend_banks(
        scheme_code=scheme_code,
        scheme_name=scheme_name,
        state=state,
        district=district,
    )


# ==========================================
# DPR Calculator & Financial Appraisal Endpoints
# ==========================================

@app.post("/calculator/dpr", response_model=DPRResponse)
def calculate_dpr_endpoint(request: DPRRequest):
    """
    Generate Detailed Project Report (DPR) financial structure, subsidy breakdown,
    own contribution requirements, and monthly EMI schedule for bank submission.
    """
    try:
        return dpr_calculator.compute_dpr(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"DPR calculation error: {str(e)}")


# ==========================================
# Ministry Policy & Demand Analytics Endpoints
# ==========================================

@app.get("/analytics/summary")
def get_analytics_summary():
    """
    Ministry Policy & Scheme Coverage Analytics.
    Provides demographic distributions, financial limits, and policy insight metrics for MoSJE / MSME evaluators.
    """
    schemes = load_schemes_from_file()
    total_schemes = len(schemes)

    # 1. Ministry breakdown
    ministry_counts: Dict[str, int] = {}
    for s in schemes:
        m = s.ministry or "Central / State Initiative"
        ministry_counts[m] = ministry_counts.get(m, 0) + 1

    # 2. Demographic coverage
    target_groups = ["SC", "ST", "OBC", "Women", "Minority", "PwD", "Artisan", "General"]
    demographic_coverage: Dict[str, Dict[str, Any]] = {}
    for tg in target_groups:
        norm_tg = tg.upper()
        matching_count = sum(
            1 for s in schemes
            if any(norm_tg in c.upper() or c.upper() in ["ALL", "GENERAL"] for c in s.eligible_categories)
        )
        pct = round((matching_count / total_schemes * 100), 1) if total_schemes else 0
        demographic_coverage[tg] = {
            "scheme_count": matching_count,
            "coverage_percentage": pct,
        }

    # 3. Financial statistics
    loans = [s.max_project_cost for s in schemes if s.max_project_cost]
    subsidies = [s.subsidy_percentage for s in schemes if s.subsidy_percentage]

    avg_loan = round(sum(loans) / len(loans), 2) if loans else 0
    max_loan = max(loans) if loans else 0
    avg_subsidy = round(sum(subsidies) / len(subsidies), 1) if subsidies else 0

    subsidized_count = sum(1 for s in schemes if s.subsidy_percentage and s.subsidy_percentage > 0)
    income_capped_count = sum(1 for s in schemes if s.income_limit and s.income_limit > 0)

    return {
        "platform": "SIH26092 AI-Driven Scheme Matching Engine",
        "ministry_sponsor": "Ministry of Social Justice and Empowerment (MoSJE)",
        "total_schemes_indexed": total_schemes,
        "ministry_distribution": ministry_counts,
        "demographic_coverage": demographic_coverage,
        "financial_overview": {
            "average_loan_cap_inr": avg_loan,
            "maximum_loan_limit_inr": max_loan,
            "schemes_with_capital_subsidy": subsidized_count,
            "average_subsidy_rate_pct": avg_subsidy,
            "income_means_tested_schemes": income_capped_count,
            "collateral_free_coverage": "100% of MSME schemes under ₹10L covered by CGTMSE/CGFMU/CGSSI guarantees",
        },
        "policy_recommendations": [
            "Stand-Up India and PMEGP offer the highest capital access (up to ₹1 Crore and ₹50 Lakhs) for SC/ST and Women entrepreneurs.",
            "MoSJE channelizing schemes (NSFDC/NBCFDC) provide lowest concessional interest rates (4% to 6%) with state SCA margin money grants.",
            "Artisans and traditional crafts under PM Vishwakarma receive the highest direct interest subvention (8%) alongside ₹15,000 modern toolkit vouchers.",
        ],
    }


# ==========================================
# User Authentication & Dashboard Endpoints
# ==========================================

@app.post("/auth/signup", response_model=TokenResponse)
def signup_endpoint(request: UserSignUp):
    """Register a new beneficiary/entrepreneur user account and return JWT access token."""
    return auth_service.signup(request)


@app.post("/auth/login", response_model=TokenResponse)
def login_endpoint(request: UserLogin):
    """Authenticate user with email and password and return JWT access token."""
    return auth_service.login(request)


@app.get("/auth/me", response_model=UserResponse)
def get_me_endpoint(current_user: UserResponse = Depends(get_current_user)):
    """Retrieve profile of the currently logged-in user."""
    return current_user


@app.put("/auth/me", response_model=UserResponse)
def update_me_endpoint(request: UserUpdate, current_user: UserResponse = Depends(get_current_user)):
    """Update profile of the currently logged-in user."""
    return auth_service.update_profile(current_user.id, request)


@app.post("/users/saved-schemes/{scheme_code}")
def save_scheme_endpoint(scheme_code: str, current_user: UserResponse = Depends(get_current_user)):
    """Bookmark a scheme code to user's saved list."""
    updated = auth_service.toggle_saved_scheme(current_user.id, scheme_code, save=True)
    return {
        "status": "success",
        "message": f"Scheme {scheme_code} bookmarked",
        "saved_schemes": updated,
    }


@app.delete("/users/saved-schemes/{scheme_code}")
def unsave_scheme_endpoint(scheme_code: str, current_user: UserResponse = Depends(get_current_user)):
    """Remove a bookmarked scheme code from user's saved list."""
    updated = auth_service.toggle_saved_scheme(current_user.id, scheme_code, save=False)
    return {
        "status": "success",
        "message": f"Scheme {scheme_code} removed",
        "saved_schemes": updated,
    }


@app.get("/users/saved-schemes", response_model=List[Scheme])
def get_saved_schemes_endpoint(current_user: UserResponse = Depends(get_current_user)):
    """Retrieve full details of all schemes bookmarked by the logged-in user."""
    schemes = load_schemes_from_file()
    saved_set = {s.upper() for s in current_user.saved_schemes}
    return [s for s in schemes if s.scheme_code and s.scheme_code.upper() in saved_set]