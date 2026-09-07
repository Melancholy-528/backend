import io
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from pypdf import PdfReader


def extract_html_text(html: bytes) -> str:
    soup = BeautifulSoup(html, "lxml")

    # Remove things that aren't useful scheme information
    for element in soup([
        "script",
        "style",
        "noscript",
        "nav",
        "footer",
        "header",
        "svg",
    ]):
        element.decompose()

    text = soup.get_text(
        separator="\n",
        strip=True
    )

    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)

    return "\n".join(lines)


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """
    Extract readable text from PDF bytes using pypdf.
    """
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        extracted_pages = []

        for index, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    extracted_pages.append(page_text.strip())
            except Exception as e:
                # Silently skip single unreadable or encrypted page
                continue

        return "\n\n".join(extracted_pages)
    except Exception as e:
        return f"Error extracting PDF text: {e}"


def extract_document_links(html: bytes, base_url: str) -> list[str]:
    """
    Find document links (PDFs, guidelines, circulars) on an HTML page.
    """
    soup = BeautifulSoup(html, "lxml")
    doc_links = set()

    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href", "").strip()
        if not href or href.startswith("javascript:") or href.startswith("mailto:"):
            continue

        absolute_url = urljoin(base_url, href)
        parsed = urlparse(absolute_url.lower())

        # Check for PDF or document extensions
        if parsed.path.endswith(".pdf") or "download" in parsed.path or "guideline" in parsed.path:
            doc_links.add(absolute_url)

    return sorted(list(doc_links))