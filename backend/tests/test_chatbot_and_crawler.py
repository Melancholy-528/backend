import io
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.miner.source_catalog import catalog, GovernmentSource, SourceCatalog
from app.miner.crawler import crawl_sources, crawl_source
from app.services.chatbot import chatbot, ChatRequest, ChatMessage
from app.services.ollama_service import ollama_service
from app.schemas.scheme import Scheme


@pytest.fixture(autouse=True, scope="session")
def isolated_schemes_environment(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("schemes_data_chat")
    tmp_schemes = tmp_dir / "schemes.json"
    real_schemes = Path(__file__).resolve().parent.parent / "schemes.json"
    if real_schemes.exists():
        shutil.copyfile(real_schemes, tmp_schemes)
    os.environ["SCHEMES_PATH"] = str(tmp_schemes)
    yield
    os.environ.pop("SCHEMES_PATH", None)


client = TestClient(app)


def test_catalog_default_sources():
    sources = catalog.get_all_sources()
    assert len(sources) >= 12

    # Check MSME filter
    msme_sources = catalog.filter_sources(ministry="MSME")
    assert len(msme_sources) >= 2
    assert any("vishwakarma" in s.id for s in msme_sources)

    # Check category filter
    artisan_sources = catalog.filter_sources(category="Artisan")
    assert len(artisan_sources) >= 1
    assert any("vishwakarma" in s.id for s in artisan_sources)

    # Check state filter
    up_sources = catalog.filter_sources(state="Uttar Pradesh")
    assert len(up_sources) >= 1
    assert up_sources[0].id == "up-yuva-swarojgar"


def test_catalog_add_source():
    new_src = GovernmentSource(
        id="test-portal",
        name="Test Welfare Portal",
        ministry="Ministry of Welfare",
        target_categories=["SC", "ST"],
        portal_url="https://example.gov.in",
        description="Test description for unit testing.",
        tags=["test"],
    )
    catalog.add_source(new_src)
    retrieved = catalog.get_source_by_id("test-portal")
    assert retrieved is not None
    assert retrieved.name == "Test Welfare Portal"


def test_chat_health_endpoint():
    res = client.get("/chat/health")
    assert res.status_code == 200
    data = res.json()
    assert "status" in data
    assert "engine" in data
    assert "total_schemes_indexed" in data
    assert data["total_schemes_indexed"] >= 5


def test_chatbot_context_retrieval():
    sample_schemes = [
        Scheme(
            name="PM Vishwakarma",
            scheme_code="PM-VISHWAKARMA",
            description="Support for artisans with loans up to 3 Lakhs.",
            eligible_categories=["Artisan", "SC", "ST"],
            max_project_cost=300000,
        ),
        Scheme(
            name="Stand-Up India",
            scheme_code="STANDUP-INDIA",
            description="Loans between 10 Lakhs and 1 Crore for SC/ST and women.",
            eligible_categories=["SC", "ST", "Women"],
            max_project_cost=10000000,
        ),
    ]
    matched, ctx_str = chatbot.retrieve_relevant_context(
        query="What is the credit limit for artisan under Vishwakarma?",
        schemes=sample_schemes,
        documents=[],
    )
    assert len(matched) >= 1
    assert matched[0].scheme_code == "PM-VISHWAKARMA"
    assert "PM Vishwakarma" in ctx_str
    assert "₹300,000" in ctx_str


def test_chatbot_rule_based_fallback():
    sample_schemes = [
        Scheme(
            name="PM Vishwakarma",
            scheme_code="PM-VISHWAKARMA",
            ministry="Ministry of MSME",
            description="Artisan welfare support.",
            eligible_categories=["Artisan"],
            max_project_cost=300000,
            subsidy_percentage=15.0,
            benefits=["Toolkit incentive of Rs 15,000"],
            source_url="https://pmvishwakarma.gov.in",
        )
    ]
    fallback_text = chatbot._rule_based_fallback("artisan benefits", sample_schemes)
    assert "PM Vishwakarma" in fallback_text
    assert "Toolkit incentive" in fallback_text
    assert "₹300,000" in fallback_text
    assert "https://pmvishwakarma.gov.in" in fallback_text


def test_chat_endpoint():
    req = {
        "message": "What schemes support SC women entrepreneurs?",
        "history": [],
    }
    res = client.post("/chat", json=req)
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert len(data["reply"]) > 20
    assert "referenced_schemes" in data
    assert "suggested_followups" in data
    assert len(data["suggested_followups"]) > 0


def test_chat_stream_endpoint():
    req = {
        "message": "Briefly tell me about PM SVANidhi loans.",
        "history": [],
    }
    res = client.post("/chat/stream", json=req)
    assert res.status_code == 200
    content = res.text
    assert len(content) > 10


def test_sources_endpoints():
    # GET /miner/sources
    res = client.get("/miner/sources")
    assert res.status_code == 200
    data = res.json()
    assert data["total_sources"] >= 10
    assert "available_ministries" in data
    assert "available_categories" in data

    # Filtered
    res_sc = client.get("/miner/sources?category=SC")
    assert res_sc.status_code == 200
    data_sc = res_sc.json()
    assert data_sc["total_sources"] >= 5

    # POST /miner/sources
    new_src_payload = {
        "id": "my-state-scheme",
        "name": "State Self-Employment Mission",
        "ministry": "State Industries Department",
        "target_categories": ["Women", "OBC"],
        "portal_url": "https://example.state.gov.in",
        "description": "State level startup credit support.",
        "tags": ["state", "startup"],
    }
    res_add = client.post("/miner/sources", json=new_src_payload)
    assert res_add.status_code == 200
    assert res_add.json()["status"] == "success"


def test_crawler_mock_crawl(tmp_path):
    # Mock crawl on a local HTML source to verify crawler pipeline end-to-end
    html_file = tmp_path / "tribal_scheme.html"
    html_file.write_text("""
    <html>
        <head><title>Tribal Artisan Enterprise Grant</title></head>
        <body>
            <h1>Tribal Artisan Enterprise Grant</h1>
            <p>Financial support for Scheduled Tribe craftspeople up to Rs. 5 Lakhs.</p>
            <p>Margin money subsidy of 20%.</p>
        </body>
    </html>
    """)

    test_src = GovernmentSource(
        id="tribal-grant",
        name="Tribal Artisan Enterprise Grant",
        ministry="Ministry of Tribal Affairs",
        target_categories=["ST", "Artisan"],
        portal_url=str(html_file),
        description="Support for ST artisans.",
    )

    out_file = str(tmp_path / "crawled_schemes.json")
    with patch("app.miner.crawler.catalog.get_source_by_id", return_value=test_src):
        result = crawl_sources(
            source_ids=["tribal-grant"],
            follow_pdfs=False,
            output_file=out_file,
        )
        assert result["successful_count"] == 1
        assert Path(out_file).exists()
        saved_scheme = result["successful_schemes"][0]
        assert "Tribal Artisan" in saved_scheme["name"]
        assert "ST" in saved_scheme["categories"]
