import io
import json
import sys
from pathlib import Path
from typing import Tuple, List, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from pypdf import PdfReader

from app.miner.fetcher import fetch_url
from app.miner.extractor import extract_html_text, extract_pdf_text, extract_document_links
from app.miner.scheme_extractor import extract_scheme_data, create_document
from app.schemas.scheme import Scheme


def extract_page_title(html: bytes) -> str:
    """Extract clean title from HTML."""
    try:
        soup = BeautifulSoup(html, "lxml")
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
            if title:
                return title
        h1 = soup.find("h1")
        if h1 and h1.get_text():
            return h1.get_text().strip()
    except Exception:
        pass
    return "Untitled Government Scheme"


def extract_pdf_title(pdf_bytes: bytes, url: str) -> str:
    """Extract title from PDF metadata, header line, or filename."""
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        if reader.metadata and reader.metadata.title:
            t = reader.metadata.title.strip()
            if len(t) > 3 and not t.lower().endswith(".pdf"):
                return t

        if reader.pages:
            first_text = reader.pages[0].extract_text()
            if first_text:
                for line in first_text.splitlines():
                    clean_line = line.strip()
                    if 4 < len(clean_line) < 80 and not clean_line.isdigit():
                        return clean_line
    except Exception:
        pass

    # Fallback to URL path filename
    filename = url.split("?")[0].rstrip("/").split("/")[-1]
    name = filename.replace(".pdf", "").replace("-", " ").replace("_", " ")
    return name.title() or "Government Scheme Document"


def mine_url(url: str, follow_pdfs: bool = True) -> Tuple[Scheme, dict]:
    """
    Mine a government scheme URL (HTML or PDF).
    If an HTML page contains guideline PDF links, optionally fetches them to enrich scheme details.
    Returns:
        (Scheme, raw_document_dict)
    """
    print(f"Fetching: {url}")
    content, content_type = fetch_url(url)
    print(f"Content type: {content_type} ({len(content)} bytes)")

    # 1. Direct PDF processing
    if "application/pdf" in content_type or url.lower().split("?")[0].endswith(".pdf"):
        print("  -> Detected PDF document. Extracting PDF text...")
        text = extract_pdf_text(content)
        title = extract_pdf_title(content, url)
        scheme = extract_scheme_data(title=title, text=text, source_url=url)
        document = create_document(title=title, text=text, source_url=url)
        return scheme, document

    # 2. HTML Webpage processing
    elif "text/html" in content_type or "xml" in content_type:
        text = extract_html_text(content)
        title = extract_page_title(content)

        # Discover attached guideline PDFs
        if follow_pdfs:
            pdf_links = extract_document_links(content, base_url=url)
            guideline_links = [
                link for link in pdf_links
                if any(kw in link.lower() for kw in ["guideline", "scheme", "circular", "manual", "eligibility"])
            ]

            # If no keyword-specific guidelines found, consider the first 2 PDFs
            targets = guideline_links[:2] if guideline_links else pdf_links[:1]

            for pdf_url in targets:
                try:
                    print(f"  -> Discovered guideline PDF: {pdf_url}")
                    pdf_bytes, pdf_ct = fetch_url(pdf_url, timeout=20)
                    if "pdf" in pdf_ct or pdf_bytes.startswith(b"%PDF"):
                        pdf_extracted = extract_pdf_text(pdf_bytes)
                        if pdf_extracted and len(pdf_extracted) > 100:
                            print(f"     Extracted {len(pdf_extracted)} chars from guideline PDF")
                            text = text + "\n\n--- Linked Guideline Document ---\n" + pdf_extracted
                except Exception as e:
                    print(f"     Could not fetch guideline PDF {pdf_url}: {e}")

        scheme = extract_scheme_data(title=title, text=text, source_url=url)
        document = create_document(title=title, text=text, source_url=url)
        return scheme, document

    else:
        # Fallback text decoding for plain text/other files
        try:
            text = content.decode("utf-8", errors="ignore")
            title = url.split("/")[-1]
            scheme = extract_scheme_data(title=title, text=text, source_url=url)
            document = create_document(title=title, text=text, source_url=url)
            return scheme, document
        except Exception:
            raise ValueError(f"Unsupported content type: {content_type}")


def save_mined_data(schemes: List[Scheme], documents: List[dict], filename: str = "schemes.json"):
    """
    Save or merge mined schemes and documents into JSON file.
    """
    filepath = Path(filename)
    existing_schemes = {}
    existing_docs = {}

    if filepath.exists():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                for s in data.get("schemes", []):
                    key = s.get("scheme_code") or s.get("name")
                    existing_schemes[key] = s
                for d in data.get("documents", []):
                    key = d.get("scheme_code") or d.get("title")
                    existing_docs[key] = d
        except Exception as e:
            print(f"Notice: Could not parse existing {filename} ({e}), creating fresh.")

    # Merge/upsert newly mined items
    for s in schemes:
        dumped = s.model_dump()
        key = dumped.get("scheme_code") or dumped.get("name")
        existing_schemes[key] = dumped

    for d in documents:
        key = d.get("scheme_code") or d.get("title")
        existing_docs[key] = d

    final_payload = {
        "schemes": list(existing_schemes.values()),
        "documents": list(existing_docs.values())
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(final_payload, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(final_payload['schemes'])} structured schemes to {filename}")


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  python -m app.miner.scheme_miner <URL or PDF_URL> [URL ...]\n\n"
            "Examples:\n"
            "  python -m app.miner.scheme_miner https://pmvishwakarma.gov.in\n"
            "  python -m app.miner.scheme_miner https://example.com/guidelines.pdf"
        )
        return

    urls = sys.argv[1:]
    schemes = []
    documents = []

    for url in urls:
        try:
            scheme, doc = mine_url(url)
            schemes.append(scheme)
            documents.append(doc)

            print(f"  Scheme Name: {scheme.name}")
            print(f"  Code:        {scheme.scheme_code}")
            print(f"  Categories:  {scheme.eligible_categories}")
            print(f"  Max Cost:    {scheme.max_project_cost}")
            print(f"  Income Limit:{scheme.income_limit}")
            print(f"  Min Age:     {scheme.min_age}")
            print(f"  Subsidy:     {scheme.subsidy_percentage}%")
            print(f"  Extracted text size: {len(doc['text'])} characters\n")

        except Exception as e:
            print(f"ERROR processing {url}: {e}\n")

    if schemes:
        save_mined_data(schemes, documents, "schemes.json")


if __name__ == "__main__":
    main()