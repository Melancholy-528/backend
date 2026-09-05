import mimetypes
import os
from pathlib import Path
from urllib.parse import urlparse
import httpx


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8",
}


def fetch_url(url: str, timeout: int = 30) -> tuple[bytes, str]:
    """
    Fetch a URL (HTML, PDF, or other resources).
    Supports http/https as well as file:// URIs and local file paths.
    Falls back to unverified SSL if government SSL certificate chain fails.
    """
    # 1. Local file support
    if url.startswith("file://") or os.path.isabs(url) or os.path.exists(url):
        clean_path = url.replace("file://", "")
        file_path = Path(clean_path).resolve()
        if file_path.exists() and file_path.is_file():
            content = file_path.read_bytes()
            guess_type, _ = mimetypes.guess_type(str(file_path))
            content_type = guess_type or "application/octet-stream"
            if content.startswith(b"%PDF") or file_path.suffix.lower() == ".pdf":
                content_type = "application/pdf"
            return content, content_type

    # 2. Remote HTTP/HTTPS fetch
    try:
        response = httpx.get(
            url,
            timeout=timeout,
            follow_redirects=True,
            headers=HEADERS,
        )
    except httpx.ConnectError:
        # Many state/central gov portals have expired/misconfigured SSL certs
        response = httpx.get(
            url,
            timeout=timeout,
            follow_redirects=True,
            headers=HEADERS,
            verify=False,
        )

    response.raise_for_status()

    content_type = response.headers.get("content-type", "").lower()
    content = response.content

    # Content-type inference if header is generic or missing
    if content.startswith(b"%PDF"):
        content_type = "application/pdf"
    elif url.lower().split("?")[0].endswith(".pdf"):
        content_type = "application/pdf"

    return content, content_type