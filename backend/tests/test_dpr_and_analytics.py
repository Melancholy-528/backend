import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.dpr_calculator import dpr_calculator, DPRRequest
from app.services.bank_locator import bank_locator

client = TestClient(app)


def test_dpr_pmegp_sc_rural():
    req = DPRRequest(
        project_cost=1000000,
        scheme_code="PMEGP",
        category="SC",
        is_rural=True,
        tenure_years=5,
    )
    res = dpr_calculator.compute_dpr(req)
    assert res.own_contribution_rate_pct == 5.0
    assert res.own_contribution_amount == 50000
    assert res.subsidy_rate_pct == 35.0
    assert res.subsidy_amount == 350000
    assert res.bank_loan_amount == 950000
    assert res.emi_details.monthly_emi > 0
    assert len(res.checklist_for_bank_interview) >= 4


def test_dpr_standup_india():
    req = DPRRequest(
        project_cost=2000000,
        scheme_code="STANDUP-INDIA",
        category="Women",
        is_rural=False,
        tenure_years=7,
    )
    res = dpr_calculator.compute_dpr(req)
    assert res.own_contribution_rate_pct == 15.0
    assert res.own_contribution_amount == 300000
    assert res.bank_loan_amount == 1700000
    assert res.emi_details.tenure_years == 7
    assert res.emi_details.monthly_emi > 0


def test_dpr_endpoint():
    payload = {
        "project_cost": 500000,
        "scheme_code": "MUDRA",
        "category": "OBC",
        "is_rural": True,
        "tenure_years": 3,
    }
    res = client.post("/calculator/dpr", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["scheme_code"] == "MUDRA"
    assert data["total_project_cost"] == 500000
    assert data["own_contribution_amount"] == 50000
    assert data["bank_loan_amount"] == 450000
    assert data["emi_details"]["monthly_emi"] > 0


def test_analytics_summary_endpoint():
    res = client.get("/analytics/summary")
    assert res.status_code == 200
    data = res.json()
    assert "total_schemes_indexed" in data
    assert data["total_schemes_indexed"] > 0
    assert "ministry_distribution" in data
    assert "demographic_coverage" in data
    assert "SC" in data["demographic_coverage"]
    assert "Women" in data["demographic_coverage"]
    assert "financial_overview" in data
    assert data["financial_overview"]["average_loan_cap_inr"] > 0
    assert len(data["policy_recommendations"]) >= 2


def test_cors_preflight():
    res = client.options("/chat", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type",
    })
    assert res.status_code == 200
    assert res.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_hindi_location_extraction_aliases():
    loc = bank_locator.extract_location_from_text("लखनऊ में खिलौना निर्माण व्यवसाय शुरू करना है")
    assert loc["state"] == "Uttar Pradesh"
    assert loc["district"] == "Lucknow"
