import json
import os
import re
from typing import List, Optional, Tuple
from urllib.parse import urlparse

import httpx

from app.schemas.scheme import Scheme


KNOWN_SCHEME_CODES = {
    "pmegp": "PMEGP",
    "prime minister employment generation": "PMEGP",
    "mudra": "MUDRA",
    "pradhan mantri mudra": "MUDRA",
    "vishwakarma": "PM-VISHWAKARMA",
    "stand-up india": "STANDUP-INDIA",
    "stand up india": "STANDUP-INDIA",
    "standupindia": "STANDUP-INDIA",
    "nsfdc": "NSFDC",
    "pmsvanidhi": "PM-SVANIDHI",
    "pm svanidhi": "PM-SVANIDHI",
    "svanidhi": "PM-SVANIDHI",
    "pmfme": "PMFME",
    "standupmitra": "STANDUP-INDIA",
    "jansamarth": "JAN-SAMARTH",
}


def clean_title(title: str) -> str:
    """Clean a webpage or document title."""
    title = re.sub(r"\s+", " ", title or "")
    # Remove common site suffixes
    title = re.sub(r"\s*[-|–]\s*(?:Home|Official Website|Govt of India|Government of India).*", "", title, flags=re.I)
    return title.strip() or "Untitled Scheme"


def infer_scheme_code(title: str, url: str) -> str:
    """Infer standard code for well-known schemes or generate from title."""
    text = f"{title} {url}".lower()
    for keyword, code in KNOWN_SCHEME_CODES.items():
        if keyword in text:
            return code

    words = re.findall(r"[A-Za-z0-9]+", title)
    if not words:
        return "SCHEME-UNKNOWN"

    # Stopwords to ignore in scheme codes
    stop_words = {"ABOUT", "THE", "AND", "FOR", "OF", "IN", "TO", "ONLINE", "PORTAL", "SCHEME", "WELCOME"}
    filtered_words = [w.upper() for w in words if w.upper() not in stop_words]
    if not filtered_words:
        filtered_words = [words[0].upper()]

    return "-".join(filtered_words[:4])


def parse_inr_amount(amount_str: str) -> int:
    """Parse Indian Rupee string to integer (handles lakhs, crores, thousands, commas)."""
    cleaned = amount_str.replace(",", "").strip().lower()
    
    crore_match = re.search(r"([\d\.]+)\s*(?:cr|crore|crores)", cleaned)
    if crore_match:
        return int(float(crore_match.group(1)) * 10000000)

    lakh_match = re.search(r"([\d\.]+)\s*(?:lakh|lakhs|lac|lacs)", cleaned)
    if lakh_match:
        return int(float(lakh_match.group(1)) * 100000)

    k_match = re.search(r"([\d\.]+)\s*(?:k|thousand|thousands)", cleaned)
    if k_match:
        return int(float(k_match.group(1)) * 1000)

    num_match = re.search(r"(\d+)", cleaned)
    if num_match:
        return int(num_match.group(1))

    return 0


def extract_categories(text: str) -> List[str]:
    """Extract target demographics and beneficiary categories."""
    categories = []
    
    # Priority checks
    if re.search(r"\b(SC|Scheduled\s+Caste)\b", text, re.I):
        categories.append("SC")
    if re.search(r"\b(ST|Scheduled\s+Tribe)\b", text, re.I):
        categories.append("ST")
    if re.search(r"\b(OBC|Other\s+Backward\s+Classes?)\b", text, re.I):
        categories.append("OBC")
    if re.search(r"\b(Women|Woman|Female)\b", text, re.I):
        categories.append("Women")
    if re.search(r"\b(Artisan|Artisans|Craftsperson|Craftspeople|Vishwakarma|Traditional\s+Trades?)\b", text, re.I):
        categories.append("Artisan")
    if re.search(r"\b(Minority|Minorities|Minority\s+Community)\b", text, re.I):
        categories.append("Minority")
    if re.search(r"\b(Divyang|PwD|Persons?\s+with\s+Disabilit(?:y|ies)|Handicapped)\b", text, re.I):
        categories.append("PwD")
    if re.search(r"\b(EWS|Economically\s+Weaker\s+Sections?)\b", text, re.I):
        categories.append("EWS")
    if re.search(r"\b(Street\s+Vendors?|Hawkers?|Vendors?)\b", text, re.I):
        categories.append("Street Vendor")
    if re.search(r"\b(Safai\s+Karamchari|Sanitation\s+Workers?)\b", text, re.I):
        categories.append("Safai Karamchari")

    if not categories:
        if re.search(r"\b(all\s+citizens?|any\s+citizen|general\s+category|open\s+category|micro\s+enterprise|small\s+business|entrepreneurs?)\b", text, re.I):
            categories.append("General")

    return sorted(list(set(categories)))



def extract_age_limits(text: str) -> Tuple[Optional[int], Optional[int]]:
    """Extract minimum and maximum age requirements."""
    min_age = None
    max_age = None

    # 1. Range patterns: "between 18 and 40 years of age", "aged between 18 and 50 years", "age 18 to 45 years", "18-40 years"
    r1 = re.search(
        r"(?:(?:age|aged)?\s*between\s+|age\s+group\s*(?:of\s*)?)(\d{2})\s*(?:and|to|-)\s*(\d{2})\s*(?:years|yrs)?(?:\s+of\s+age)?",
        text,
        re.I,
    )
    r2 = re.search(
        r"\b(\d{2})\s*(?:to|-)\s*(\d{2})\s*(?:years|yrs)(?:\s+of\s+age)?\b",
        text,
        re.I,
    )
    rm = r1 or r2
    if rm:
        val1, val2 = int(rm.group(1)), int(rm.group(2))
        if 14 <= val1 <= 65 and 18 <= val2 <= 85 and val1 < val2:
            min_age, max_age = val1, val2

    # 2. Minimum age pattern (e.g. minimum age of 18 years, above 18 years, at least 18 years)
    if min_age is None:
        min_match = re.search(
            r"(?:minimum\s+age[^\d]{0,25}?|above\s+|at\s+least\s+|aged?\s+(?:above|over)?\s*)(\d{2})\s*(?:years|yrs)(?:\s+of\s+age)?",
            text,
            re.I,
        )
        if min_match:
            val = int(min_match.group(1))
            if 14 <= val <= 65:
                min_age = val

    # 3. Maximum age pattern (e.g. maximum age of 55 years, not exceeding 50 years, up to 45 years)
    if max_age is None:
        max_match = re.search(
            r"(?:maximum\s+age[^\d]{0,25}?|not\s+exceeding\s+|up\s+to\s+|below\s+)(\d{2})\s*(?:years|yrs)(?:\s+of\s+age)?",
            text,
            re.I,
        )
        if max_match:
            val = int(max_match.group(1))
            if 20 <= val <= 85:
                max_age = val

    return min_age, max_age


def extract_income_limit(text: str) -> Optional[int]:
    """Extract annual family income ceiling in INR."""
    # Look around income, family income, annual income mentions
    pattern = re.compile(
        r"(?:annual\s+income|family\s+income|income\s+limit|income\s+ceiling|income\s+not\s+exceeding)[^\.\n]{0,60}?(?:₹|rs\.?|inr)?\s*([\d\.]+\s*(?:lakh|lakhs|lac|lacs|crore|cr)?|\d[\d,]*)",
        re.I
    )
    for match in pattern.finditer(text):
        val = parse_inr_amount(match.group(1))
        if 30000 <= val <= 2500000:  # Sensible range for scheme income ceilings
            return val

    return None


def extract_max_project_cost(text: str) -> Optional[int]:
    """Extract maximum loan amount or project cost in INR."""
    # Priority to key sections (features, loan size, quantum of assistance)
    key_lines = []
    for line in text.splitlines():
        line_clean = line.strip()
        if any(term in line_clean.lower() for term in [
            "loan size", "quantum of assistance", "composite loan", "project cost",
            "credit support", "enterprise development loan", "max loan", "financial assistance"
        ]):
            key_lines.append(line_clean)

    target_text = " ".join(key_lines) if key_lines else text

    # Search for maximum loan/project cost numbers
    matches = re.findall(
        r"(?:₹|rs\.?|inr)\s*([\d\.]+\s*(?:crore|cr|lakh|lakhs|lac|lacs)?|\d[\d,]*)",
        target_text,
        re.I
    )
    
    candidates = []
    for m in matches:
        val = parse_inr_amount(m)
        # Avoid counting aggregate budget stats (e.g. 53,000 crores disbursed) or small stipends
        if 10000 <= val <= 200000000:
            candidates.append(val)

    if candidates:
        return max(candidates)

    return None


def extract_subsidy(text: str) -> Optional[float]:
    """Extract subsidy percentage or margin money percentage."""
    m = re.search(r"(\d{1,2}(?:\.\d+)?)\s*%\s*(?:subsidy|margin\s+money|interest\s+subvention)", text, re.I)
    if m:
        return float(m.group(1))
    return None


def extract_ministry(text: str) -> Optional[str]:
    """Extract responsible ministry or department."""
    m = re.search(r"(?:Ministry\s+of\s+[A-Za-z\s&,]+|Department\s+of\s+[A-Za-z\s&,]+)", text, re.I)
    if m:
        ministry = m.group(0).strip().rstrip(".,")
        if len(ministry) < 80:
            return ministry
    return None


def extract_benefits(text: str) -> List[str]:
    """Extract key highlight benefits from the scheme text."""
    benefits = []
    # Check for known benefit lines
    benefit_keywords = ["grant", "toolkit", "interest", "collateral free", "training stipend", "subvention", "composite loan"]
    for line in text.splitlines():
        line = line.strip()
        if len(line) > 15 and len(line) < 200:
            if any(kw in line.lower() for kw in benefit_keywords):
                cleaned = re.sub(r"^[0-9\.\-\*\•\)]+\s*", "", line)
                if cleaned and cleaned not in benefits:
                    benefits.append(cleaned)
        if len(benefits) >= 5:
            break
    return benefits


def extract_scheme_with_llm(raw_text: str, title: str, source_url: str) -> Optional[Scheme]:
    """
    Attempt to extract structured Scheme using Gemini API if GEMINI_API_KEY is available.
    Falls back gracefully if unavailable.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        prompt = f"""
        Extract the government scheme's eligibility rules into structured JSON from the text below.
        Return JSON matching this exact structure:
        {{
          "name": "Full official name",
          "scheme_code": "Short code or acronym",
          "ministry": "Ministry/department or null",
          "description": "Short 1-2 sentence overview",
          "eligible_categories": ["SC", "ST", "OBC", "Women", "Artisan", "Minority", "PwD", "General"],
          "min_age": 18,
          "max_age": null,
          "income_limit": 500000,
          "max_project_cost": 1000000,
          "subsidy_percentage": 15.0,
          "benefits": ["benefit 1", "benefit 2"]
        }}

        Scheme Webpage/Document Title: {title}
        Source URL: {source_url}
        Text:
        {raw_text[:12000]}
        """
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }
        res = httpx.post(url, json=payload, timeout=25)
        if res.status_code == 200:
            data = res.json()
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed_json = json.loads(content)
            parsed_json["source_url"] = source_url
            return Scheme(**parsed_json)
    except Exception as e:
        print(f"LLM extraction skipped: {e}")

    return None


def extract_scheme_with_ollama(raw_text: str, title: str, source_url: str) -> Optional[Scheme]:
    """
    Attempt to extract structured Scheme using local Ollama model if available.
    """
    ollama_base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:3b")

    prompt = f"""
    Extract the government scheme's eligibility rules into structured JSON from the text below.
    Return ONLY valid JSON matching this schema:
    {{
      "name": "Full official name",
      "scheme_code": "Short code or acronym",
      "ministry": "Ministry or null",
      "description": "Short 1-2 sentence overview",
      "eligible_categories": ["SC", "ST", "OBC", "Women", "Artisan", "Minority", "PwD", "General"],
      "min_age": 18,
      "max_age": null,
      "income_limit": 500000,
      "max_project_cost": 1000000,
      "subsidy_percentage": 15.0,
      "benefits": ["benefit 1", "benefit 2"]
    }}

    Title: {title}
    URL: {source_url}
    Text:
    {raw_text[:4000]}
    """

    try:
        with httpx.Client(timeout=45.0) as client:
            res = client.post(
                f"{ollama_base}/api/chat",
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "options": {"temperature": 0.1},
                },
            )
            if res.status_code == 200:
                content = res.json().get("message", {}).get("content", "")
                json_match = re.search(r"\{.*\}", content, re.DOTALL)
                if json_match:
                    parsed_json = json.loads(json_match.group(0))
                    parsed_json["source_url"] = source_url
                    return Scheme(**parsed_json)
    except Exception as e:
        print(f"Ollama extraction skipped: {e}")

    return None


def extract_scheme_data(title: str, text: str, source_url: str) -> Scheme:
    """
    Extract structured Scheme object from raw text (HTML/PDF).
    Uses Ollama or cloud LLM if configured, otherwise employs intelligent heuristic extraction.
    """
    # 1. Try local Ollama if explicitly enabled
    if os.getenv("USE_OLLAMA_MINING", "").lower() in ["1", "true", "yes"]:
        ollama_scheme = extract_scheme_with_ollama(raw_text=text, title=title, source_url=source_url)
        if ollama_scheme:
            return ollama_scheme

    # 2. Try Cloud LLM if configured
    llm_scheme = extract_scheme_with_llm(raw_text=text, title=title, source_url=source_url)
    if llm_scheme:
        return llm_scheme

    # 3. Rule & heuristic extraction
    cleaned_name = clean_title(title)
    scheme_code = infer_scheme_code(cleaned_name, source_url)
    categories = extract_categories(text)
    min_age, max_age = extract_age_limits(text)
    income_limit = extract_income_limit(text)
    max_project_cost = extract_max_project_cost(text)
    subsidy_percentage = extract_subsidy(text)
    ministry = extract_ministry(text)
    benefits = extract_benefits(text)

    # Clean description from beginning of text
    lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 40]
    description = lines[0] if lines else f"Government welfare scheme: {cleaned_name}"

    return Scheme(
        name=cleaned_name,
        scheme_code=scheme_code,
        ministry=ministry,
        description=description[:300],
        eligible_categories=categories,
        eligible_category=", ".join(categories) if categories else None,
        min_age=min_age,
        max_age=max_age,
        income_limit=income_limit,
        max_project_cost=max_project_cost,
        subsidy_percentage=subsidy_percentage,
        benefits=benefits,
        source_url=source_url,
    )


def create_document(
    title: str,
    text: str,
    source_url: str
) -> dict:
    """Backward compatibility helper for raw document structure."""
    title = clean_title(title)
    scheme_code = infer_scheme_code(title, source_url)
    return {
        "title": title,
        "scheme_code": scheme_code,
        "text": text,
        "source_url": source_url
    }