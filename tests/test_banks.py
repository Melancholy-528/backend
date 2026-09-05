import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.bank_locator import bank_locator

client = TestClient(app)


def test_location_extraction():
    loc1 = bank_locator.extract_location_from_text("SC woman in Varanasi, UP seeking tailoring loan")
    assert loc1["state"] == "Uttar Pradesh"
    assert loc1["district"] == "Varanasi"

    loc2 = bank_locator.extract_location_from_text("Entrepreneur in Pune, Maharashtra")
    assert loc2["state"] == "Maharashtra"
    assert loc2["district"] == "Pune"

    loc3 = bank_locator.extract_location_from_text("Textile startup in Coimbatore, Tamil Nadu")
    assert loc3["state"] == "Tamil Nadu"
    assert loc3["district"] == "Coimbatore"


def test_district_banking_profile():
    # Direct mapped
    profile = bank_locator.get_district_profile("Uttar Pradesh", "Varanasi")
    assert profile.lead_bank == "Union Bank of India"
    assert "Baroda UP Bank" in profile.regional_rural_banks
    assert "Chandpur" in profile.dic_office or "Vikas Bhawan" in profile.dic_office

    # Fallback for unlisted district in known state
    fallback_profile = bank_locator.get_district_profile("Maharashtra", "Satara")
    assert fallback_profile.lead_bank == "Bank of Maharashtra"
    assert "Maharashtra Gramin Bank" in fallback_profile.regional_rural_banks


def test_recommend_banks_standup_india():
    rec = bank_locator.recommend_banks(
        scheme_code="STANDUP-INDIA",
        scheme_name="Stand-Up India Scheme",
        state="Uttar Pradesh",
        district="Varanasi",
    )
    assert rec.lead_bank_name == "Union Bank of India"
    assert any("Baroda UP Bank" in r["bank_name"] for r in rec.regional_rural_banks)
    assert any("Lead District Manager" in n.agency for n in rec.district_nodal_offices)
    assert len(rec.application_steps) >= 3
    assert len(rec.required_documents) >= 5


def test_recommend_banks_pmegp():
    rec = bank_locator.recommend_banks(
        scheme_code="PMEGP",
        scheme_name="Prime Minister's Employment Generation Programme",
        state="Tamil Nadu",
        district="Coimbatore",
    )
    assert rec.lead_bank_name == "Canara Bank"
    assert any("District Industries Centre" in n.agency for n in rec.district_nodal_offices)
    assert any("kviconline" in step for step in rec.application_steps)


def test_get_districts_endpoint():
    res = client.get("/banks/districts")
    assert res.status_code == 200
    data = res.json()
    assert "states" in data
    assert "Uttar Pradesh" in data["states"]
    assert "Varanasi" in data["states"]["Uttar Pradesh"]
    assert "Maharashtra" in data["states"]
    assert "Pune" in data["states"]["Maharashtra"]


def test_get_nearby_banks_endpoint():
    res = client.get("/banks/nearby?scheme_code=STANDUP-INDIA&state=Uttar%20Pradesh&district=Varanasi")
    assert res.status_code == 200
    data = res.json()
    assert data["lead_bank_name"] == "Union Bank of India"
    assert data["district"] == "Varanasi"
    assert len(data["primary_lending_banks"]) >= 1
    assert len(data["district_nodal_offices"]) >= 1


def test_chat_with_location_support():
    # Pass explicit state and district in ChatRequest
    payload = {
        "message": "What loan can I get for a small bakery?",
        "state": "Maharashtra",
        "district": "Pune",
        "history": []
    }
    res = client.post("/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert data.get("nearby_banking_support") is not None
    support = data["nearby_banking_support"]
    assert support["lead_bank_name"] == "Bank of Maharashtra"
    assert support["district"] == "Pune"
