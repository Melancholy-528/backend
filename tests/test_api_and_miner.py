import io
import os
import shutil
import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from pypdf import PdfWriter

from app.main import app
from app.miner.extractor import extract_html_text, extract_pdf_text, extract_document_links
from app.miner.scheme_extractor import (
    parse_inr_amount,
    extract_categories,
    extract_age_limits,
    extract_income_limit,
    extract_max_project_cost,
    extract_scheme_data,
)
from app.miner.scheme_miner import mine_url
from app.schemas.applicant import Applicant
from app.schemas.scheme import Scheme
from app.services.eligibility import check_eligibility


@pytest.fixture(autouse=True, scope="session")
def isolated_schemes_environment(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("schemes_data")
    tmp_schemes = tmp_dir / "schemes.json"
    real_schemes = Path(__file__).resolve().parent.parent / "schemes.json"
    if real_schemes.exists():
        shutil.copyfile(real_schemes, tmp_schemes)
    os.environ["SCHEMES_PATH"] = str(tmp_schemes)
    yield
    os.environ.pop("SCHEMES_PATH", None)


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "total_schemes_indexed" in data
    assert data["status"] == "online"


def test_get_schemes_and_filter():
    # All schemes
    response = client.get("/schemes")
    assert response.status_code == 200
    schemes = response.json()
    assert len(schemes) >= 5

    # Filter by category
    response = client.get("/schemes?category=SC")
    assert response.status_code == 200
    sc_schemes = response.json()
    assert len(sc_schemes) >= 1
    assert any("NSFDC" in s["name"] or "STANDUP" in s["scheme_code"] for s in sc_schemes)


def test_get_scheme_by_code():
    response = client.get("/schemes/PM-VISHWAKARMA")
    assert response.status_code == 200
    data = response.json()
    assert data["scheme_code"] == "PM-VISHWAKARMA"

    # Non existent
    response_404 = client.get("/schemes/NON-EXISTENT-XYZ")
    assert response_404.status_code == 404


def test_matching_sc_artisan():
    applicant = {
        "category": "SC",
        "occupation": "Artisan",
        "annual_income": 150000,
        "project_cost": 80000,
        "age": 29,
        "gender": "Female",
    }
    response = client.post("/match", json=applicant)
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["total_eligible"] > 0
    matched_names = [m["scheme"] for m in data["matches"]]
    assert any("Vishwakarma" in n for n in matched_names)
    assert any("NSFDC" in n or "Standup" in n for n in matched_names)


def test_matching_ineligible_reasons():
    # Exceeding all reasonable caps
    rich_applicant = {
        "category": "General",
        "annual_income": 50000000,  # 5 Crores
        "project_cost": 800000000,  # 80 Crores
        "age": 85,
        "gender": "Male",
    }
    response = client.post("/match", json=rich_applicant)
    assert response.status_code == 200
    data = response.json()
    # Should have reasons in ineligible list
    assert len(data["ineligible"]) > 0
    first_ineligible = data["ineligible"][0]
    assert len(first_ineligible["reasons"]) > 0


def test_heuristics_parsing():
    assert parse_inr_amount("10 Lakhs") == 1000000
    assert parse_inr_amount("1.5 Crore") == 15000000
    assert parse_inr_amount("50k") == 50000
    assert parse_inr_amount("₹ 25,000") == 25000

    sample_text = "Loan assistance to SC and ST youth aged between 18 and 50 years with annual income up to Rs. 3.00 Lakhs."
    cats = extract_categories(sample_text)
    assert "SC" in cats
    assert "ST" in cats

    min_a, max_a = extract_age_limits(sample_text)
    assert min_a == 18
    assert max_a == 50

    inc = extract_income_limit(sample_text)
    assert inc == 300000


def test_html_extractor():
    html_content = b"""
    <html>
        <head><title>Test Scheme Portal</title></head>
        <body>
            <nav>Menu</nav>
            <h1>Tribal Entrepreneurship Development</h1>
            <p>Target beneficiaries: ST entrepreneurs above 18 years.</p>
            <p>Maximum loan support: Rs. 25 Lakhs at 6% interest subsidy.</p>
            <a href="/guidelines.pdf">Download Guidelines</a>
            <footer>Copyright 2026</footer>
        </body>
    </html>
    """
    text = extract_html_text(html_content)
    assert "Menu" not in text  # nav stripped
    assert "Copyright 2026" not in text  # footer stripped
    assert "Tribal Entrepreneurship Development" in text

    links = extract_document_links(html_content, "https://example.gov.in/scheme")
    assert "https://example.gov.in/guidelines.pdf" in links


def test_mine_local_html_file():
    html_content = """
    <html>
        <head><title>Mukhyamantri Yuva Swarojgar Yojana</title></head>
        <body>
            <h1>Mukhyamantri Yuva Swarojgar Yojana</h1>
            <p>This welfare programme offers collateral-free composite loans up to Rs. 10 Lakhs for OBC and SC youth.</p>
            <p>Applicants must be between 18 and 40 years of age with annual family income below Rs. 2 Lakhs.</p>
            <p>Government offers 25% subsidy on margin money.</p>
        </body>
    </html>
    """
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html_content)
        temp_path = f.name

    try:
        scheme, doc = mine_url(temp_path, follow_pdfs=False)
        assert "Yuva Swarojgar" in scheme.name
        assert "SC" in scheme.eligible_categories
        assert "OBC" in scheme.eligible_categories
        assert scheme.min_age == 18
        assert scheme.max_age == 40
        assert scheme.income_limit == 200000
        assert scheme.max_project_cost == 1000000
        assert scheme.subsidy_percentage == 25.0
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_miner_mine_endpoint():
    html_content = """
    <html>
        <head><title>Artisan Revival Scheme</title></head>
        <body>
            <h1>Artisan Revival Scheme</h1>
            <p>Dedicated funding for traditional Artisans and Craftspeople.</p>
            <p>Maximum credit support of Rs. 3 Lakhs.</p>
        </body>
    </html>
    """
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html_content)
        temp_path = f.name

    try:
        res = client.post("/miner/mine", json={"url": temp_path, "follow_pdfs": False})
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "success"
        assert "Artisan Revival" in data["scheme"]["name"]
        assert "Artisan" in data["scheme"]["eligible_categories"]
    finally:
        Path(temp_path).unlink(missing_ok=True)


SAMPLE_PDF_BYTES = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>
endobj
4 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
5 0 obj
<< /Length 135 >>
stream
BT
/F1 14 Tf
50 700 Td
(Stand-Up India Scheme for SC and ST Entrepreneurs) Tj
0 -30 Td
(Maximum composite loan amount is Rs. 1 Crore with interest subsidy.) Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000234 00000 n 
0000000305 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
490
%%EOF
"""


def test_mine_pdf_file():
    extracted = extract_pdf_text(SAMPLE_PDF_BYTES)
    assert "Stand-Up India" in extracted
    assert "1 Crore" in extracted

    with tempfile.NamedTemporaryFile("wb", suffix=".pdf", delete=False) as f:
        f.write(SAMPLE_PDF_BYTES)
        temp_path = f.name

    try:
        scheme, doc = mine_url(temp_path)
        assert scheme.scheme_code == "STANDUP-INDIA"
        assert "SC" in scheme.eligible_categories
        assert scheme.max_project_cost == 10000000
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_miner_upload_file_endpoint():
    with tempfile.NamedTemporaryFile("wb", suffix=".pdf", delete=False) as f:
        f.write(SAMPLE_PDF_BYTES)
        temp_path = f.name

    try:
        with open(temp_path, "rb") as pf:
            res = client.post(
                "/miner/mine-file",
                files={"file": ("standup_guideline.pdf", pf, "application/pdf")}
            )
            assert res.status_code == 200
            data = res.json()
            assert data["status"] == "success"
            assert "Stand-Up" in data["scheme"]["name"]
            assert data["scheme"]["scheme_code"] == "STANDUP-INDIA"
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_miner_documents_endpoint():
    res = client.get("/miner/documents")
    assert res.status_code == 200
    docs = res.json()
    assert isinstance(docs, list)
    if docs:
        first = docs[0]
        assert "title" in first
        assert "text_preview" in first

