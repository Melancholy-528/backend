import re
from urllib.parse import urljoin


IMPORTANT_TERMS = [
    "scheme",
    "schemes",
    "eligibility",
    "loan",
    "getLoan",
    "api",
    "jan-samarth",
]


def find_scripts(html: str, base_url: str):
    """
    Extract JavaScript file URLs from the page.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "lxml")

    scripts = []

    for script in soup.find_all("script"):
        src = script.get("src")

        if src:
            scripts.append(urljoin(base_url, src))

    return scripts


def find_api_candidates(js_text: str):
    """
    Find strings in JavaScript that look like API endpoints.
    """

    candidates = set()

    # Absolute URLs
    absolute_urls = re.findall(
        r'https?://[A-Za-z0-9._~:/?#\[\]@!$&\'()*+,;=%-]+',
        js_text
    )

    for url in absolute_urls:
        if any(term.lower() in url.lower() for term in IMPORTANT_TERMS):
            candidates.add(url.rstrip('",\''))


    # Relative API paths
    relative_paths = re.findall(
        r'["\']([^"\']*(?:/api/|/scheme|/schemes|/eligibility|/getLoan|/bot/)[^"\']*)["\']',
        js_text,
        flags=re.IGNORECASE
    )

    for path in relative_paths:
        if len(path) < 300:
            candidates.add(path)


    return sorted(candidates)


def find_relevant_snippets(js_text: str, radius=150):
    """
    Find the code surrounding important API-related terms.
    This is useful for discovering the API base URL.
    """

    results = []

    pattern = re.compile(
        r'.{0,' + str(radius) + r'}'
        r'(?:scheme|schemes|eligibility|getLoan|jan-samarth|/api/)'
        r'.{0,' + str(radius) + r'}',
        re.IGNORECASE | re.DOTALL
    )

    for match in pattern.finditer(js_text):
        snippet = match.group(0)

        # Remove huge whitespace
        snippet = re.sub(r'\s+', ' ', snippet).strip()

        if len(snippet) <= radius * 2 + 100:
            results.append(snippet)

    return results