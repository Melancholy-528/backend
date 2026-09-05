"""
District Bank Locator and Scheme-to-Bank Routing Service.
Identifies Lead District Banks (LDB), Regional Rural Banks (RRBs), participating commercial banks,
and District Nodal Agencies (DIC, LDM, SCAs) based on the applicant's State, District, and recommended Scheme.
"""

from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field


class BankBranch(BaseModel):
    bank_name: str
    branch_type: str
    address: str
    services: List[str] = Field(default_factory=list)


class NodalOffice(BaseModel):
    agency: str
    location: str
    role: str


class DistrictBankingProfile(BaseModel):
    state: str
    district: str
    lead_bank: str
    ldm_office: str
    regional_rural_banks: List[str] = Field(default_factory=list)
    prominent_commercial_banks: List[str] = Field(default_factory=list)
    dic_office: str
    sca_office: Optional[str] = None


class BankRecommendation(BaseModel):
    state: str
    district: str
    scheme_name: str
    scheme_code: str
    lead_bank_name: str
    ldm_office_info: str
    primary_lending_banks: List[Dict[str, Any]]
    regional_rural_banks: List[Dict[str, Any]]
    district_nodal_offices: List[NodalOffice]
    application_steps: List[str]
    required_documents: List[str]


# Pre-mapped Lead District Banks and banking networks across key states and districts in India
DISTRICT_BANK_DATABASE: Dict[str, Dict[str, Dict[str, Any]]] = {
    "uttar pradesh": {
        "varanasi": {
            "lead_bank": "Union Bank of India",
            "ldm_office": "Lead District Manager (LDM) Office, Union Bank Bhawan, Sigra / Kachehri, Varanasi",
            "rrbs": ["Baroda UP Bank"],
            "commercial": ["State Bank of India (SMECCC Kachehri)", "Punjab National Bank (Cantonment)", "Bank of Baroda (Bhelupur)", "Canara Bank"],
            "dic_office": "District Industries Centre (DIC), Industrial Estate, Chandpur / Vikas Bhawan, Varanasi",
            "sca_office": "UP Scheduled Castes Finance & Development Corp (UPSCFDC), Vikas Bhawan, Varanasi",
        },
        "lucknow": {
            "lead_bank": "Bank of India",
            "ldm_office": "Lead District Manager Office, Bank of India Zonal Building, Gomti Nagar, Lucknow",
            "rrbs": ["Aryavart Bank"],
            "commercial": ["State Bank of India (Main Branch Hazratganj)", "Punjab National Bank", "Union Bank of India", "Canara Bank"],
            "dic_office": "District Industries Centre, Sarojini Nagar / Vikas Bhawan, Lucknow",
            "sca_office": "UP SC/ST Finance Development Corp, Head Office & Vikas Bhawan, Lucknow",
        },
        "kanpur": {
            "lead_bank": "Bank of Baroda",
            "ldm_office": "Lead District Manager Office, Bank of Baroda Regional Office, Civil Lines, Kanpur",
            "rrbs": ["Aryavart Bank"],
            "commercial": ["State Bank of India (Mall Road)", "Central Bank of India", "Punjab National Bank", "Union Bank of India"],
            "dic_office": "District Industries Centre, Fazalganj Industrial Area, Kanpur",
            "sca_office": "UPSCFDC District Office, Vikas Bhawan, Kanpur",
        },
        "agra": {
            "lead_bank": "Canara Bank",
            "ldm_office": "Lead District Manager Office, Canara Bank Circle Office, Sanjay Place, Agra",
            "rrbs": ["Aryavart Bank"],
            "commercial": ["State Bank of India (MG Road)", "Punjab National Bank", "Bank of Baroda"],
            "dic_office": "District Industries Centre, Nunhai Industrial Area, Agra",
            "sca_office": "UP Scheduled Castes Finance Corp, Vikas Bhawan, Agra",
        },
        "prayagraj": {
            "lead_bank": "Bank of Baroda",
            "ldm_office": "Lead District Manager Office, Bank of Baroda Building, Civil Lines, Prayagraj",
            "rrbs": ["Baroda UP Bank"],
            "commercial": ["State Bank of India (Main Branch Kachehri)", "Punjab National Bank", "Union Bank of India"],
            "dic_office": "District Industries Centre, Phaphamau / Vikas Bhawan, Prayagraj",
            "sca_office": "District SC Welfare Office, Vikas Bhawan, Prayagraj",
        },
        "meerut": {
            "lead_bank": "Punjab National Bank",
            "ldm_office": "Lead District Manager Office, PNB Circle Office, Meerut Cantt",
            "rrbs": ["Prathama UP Gramin Bank"],
            "commercial": ["State Bank of India (SME Branch)", "Canara Bank", "Union Bank of India"],
            "dic_office": "District Industries Centre, Delhi Road, Meerut",
            "sca_office": "UPSCFDC District Branch, Vikas Bhawan, Meerut",
        },
        "gorakhpur": {
            "lead_bank": "State Bank of India",
            "ldm_office": "Lead District Manager Office, SBI Administrative Office, Bank Road, Gorakhpur",
            "rrbs": ["Baroda UP Bank"],
            "commercial": ["Punjab National Bank", "Union Bank of India", "Central Bank of India"],
            "dic_office": "District Industries Centre, Gorakhpur Industrial Development Authority (GIDA) / Vikas Bhawan",
            "sca_office": "UPSCFDC Office, Vikas Bhawan, Gorakhpur",
        },
    },
    "maharashtra": {
        "mumbai": {
            "lead_bank": "State Bank of India",
            "ldm_office": "Lead District Manager Office, SBI Local Head Office, Fort / BKC, Mumbai",
            "rrbs": ["Maharashtra Gramin Bank"],
            "commercial": ["Bank of Baroda (Corporate Centre)", "Bank of India (Main Branch Fort)", "Union Bank of India", "Canara Bank"],
            "dic_office": "District Industries Centre, Old Custom House, Fort, Mumbai",
            "sca_office": "Mahatma Phule Backward Class Development Corp, Nariman Point, Mumbai",
        },
        "pune": {
            "lead_bank": "Bank of Maharashtra",
            "ldm_office": "Lead District Manager Office, Bank of Maharashtra, Lokmangal, Shivajinagar, Pune",
            "rrbs": ["Maharashtra Gramin Bank"],
            "commercial": ["State Bank of India (SME Centre Wakdewadi)", "Bank of Baroda", "Canara Bank", "Union Bank of India"],
            "dic_office": "District Industries Centre, Agriculture College Campus, Shivajinagar, Pune",
            "sca_office": "Mahatma Phule Backward Class Development Corp, Pune Administrative Complex",
        },
        "nagpur": {
            "lead_bank": "Bank of India",
            "ldm_office": "Lead District Manager Office, Bank of India Building, Kingsway, Nagpur",
            "rrbs": ["Vidharbha Konkan Gramin Bank"],
            "commercial": ["State Bank of India", "Bank of Maharashtra", "Punjab National Bank"],
            "dic_office": "District Industries Centre, Civil Lines / MIDC, Nagpur",
            "sca_office": "District Social Welfare Complex, Civil Lines, Nagpur",
        },
        "nashik": {
            "lead_bank": "Bank of Maharashtra",
            "ldm_office": "Lead District Manager Office, Bank of Maharashtra Zonal Office, Old Agra Road, Nashik",
            "rrbs": ["Maharashtra Gramin Bank"],
            "commercial": ["State Bank of India (SME Branch)", "Bank of Baroda", "Canara Bank"],
            "dic_office": "District Industries Centre, Satpur MIDC, Nashik",
            "sca_office": "Mahatma Phule Backward Class Development Corporation, Nashik",
        },
    },
    "tamil nadu": {
        "chennai": {
            "lead_bank": "Indian Bank",
            "ldm_office": "Lead District Manager Office, Indian Bank Circle Office, Rajaji Salai / Anna Salai, Chennai",
            "rrbs": ["Tamil Nadu Grama Bank"],
            "commercial": ["State Bank of India (SME Centre Mount Road)", "Canara Bank (Circle Office)", "Indian Overseas Bank (Central Office)"],
            "dic_office": "District Industries Centre, Guindy Industrial Estate, Chennai",
            "sca_office": "Tamil Nadu Adi Dravidar Housing and Development Corp (TAHDCO), Teynampet, Chennai",
        },
        "coimbatore": {
            "lead_bank": "Canara Bank",
            "ldm_office": "Lead District Manager Office, Canara Bank Circle Office, Oppanakara Street, Coimbatore",
            "rrbs": ["Tamil Nadu Grama Bank"],
            "commercial": ["State Bank of India (Kurichi SME Hub)", "Indian Bank", "Indian Overseas Bank"],
            "dic_office": "District Industries Centre, Patel Road, Ram Nagar, Coimbatore",
            "sca_office": "TAHDCO District Office, Collectorate Complex, Coimbatore",
        },
        "madurai": {
            "lead_bank": "Canara Bank",
            "ldm_office": "Lead District Manager Office, Canara Bank Building, Grand Kaveri, Madurai",
            "rrbs": ["Tamil Nadu Grama Bank"],
            "commercial": ["Indian Overseas Bank", "State Bank of India", "Indian Bank"],
            "dic_office": "District Industries Centre, K.Pudur, Madurai",
            "sca_office": "TAHDCO District Office, Madurai Collectorate",
        },
    },
    "karnataka": {
        "bengaluru": {
            "lead_bank": "Canara Bank",
            "ldm_office": "Lead District Manager Office, Canara Bank Head Office / Gandhinagar, Bengaluru",
            "rrbs": ["Karnataka Gramin Bank"],
            "commercial": ["State Bank of India (St. Marks Road SME Hub)", "Union Bank of India", "Punjab National Bank"],
            "dic_office": "District Industries Centre, Rajajinagar Industrial Estate, Bengaluru",
            "sca_office": "Dr. B.R. Ambedkar Development Corp, V.V. Towers, Bengaluru",
        },
        "mysuru": {
            "lead_bank": "State Bank of India",
            "ldm_office": "Lead District Manager Office, SBI Building, Sayyaji Rao Road, Mysuru",
            "rrbs": ["Karnataka Gramin Bank"],
            "commercial": ["Canara Bank", "Union Bank of India", "Bank of Baroda"],
            "dic_office": "District Industries Centre, Sayyaji Rao Road, Mysuru",
            "sca_office": "Dr. B.R. Ambedkar Development Corporation, DC Office Complex, Mysuru",
        },
    },
    "delhi": {
        "new delhi": {
            "lead_bank": "State Bank of India",
            "ldm_office": "Lead District Manager Office, SBI Parliament Street Main Branch, New Delhi",
            "rrbs": ["Sarva Haryana Gramin Bank / Baroda UP Bank (NCR network)"],
            "commercial": ["Punjab National Bank (Connaught Place)", "Canara Bank", "Bank of Baroda", "Union Bank of India"],
            "dic_office": "Department of Industries, Govt of NCT of Delhi, Udyog Sadan, Patparganj, Delhi",
            "sca_office": "Delhi SC/ST/OBC/Minorities Development Corp (DSFDC), Ambedkar Bhawan, Rohini/Patparganj",
        },
        "delhi": {
            "lead_bank": "Punjab National Bank",
            "ldm_office": "Lead District Manager Office, PNB Zonal Office, Rajendra Place, Delhi",
            "rrbs": ["Delhi State Co-operative Bank"],
            "commercial": ["State Bank of India", "Canara Bank", "Bank of Baroda"],
            "dic_office": "Delhi State Industrial and Infrastructure Development Corp (DSIIDC), Connaught Place",
            "sca_office": "Delhi SC/ST Financial Development Corp (DSFDC), Delhi",
        },
    },
    "west bengal": {
        "kolkata": {
            "lead_bank": "UCO Bank",
            "ldm_office": "Lead District Manager Office, UCO Bank Head Office Building, BTM Sarani, Kolkata",
            "rrbs": ["Bangiya Gramin Vikash Bank", "Paschim Banga Gramin Bank"],
            "commercial": ["State Bank of India (Samriddhi Bhawan Strand Road)", "Punjab National Bank", "Indian Bank"],
            "dic_office": "District Industries Centre, Camac Street / BBD Bagh, Kolkata",
            "sca_office": "West Bengal SC/ST Development & Finance Corp, Salt Lake, Sector II, Kolkata",
        },
    },
    "rajasthan": {
        "jaipur": {
            "lead_bank": "UCO Bank",
            "ldm_office": "Lead District Manager Office, UCO Bank Zonal Office, Tonk Road, Jaipur",
            "rrbs": ["Baroda Rajasthan Kshetriya Gramin Bank"],
            "commercial": ["State Bank of India (Tilak Marg SME Centre)", "Punjab National Bank", "Bank of Baroda"],
            "dic_office": "District Industries Centre, Malviya Industrial Area / Udyog Bhawan, Jaipur",
            "sca_office": "Rajasthan SC/ST Finance & Development Corp (Anuprati / Anuja Nigam), Nehru Sahkar Bhawan, Jaipur",
        },
    },
    "gujarat": {
        "ahmedabad": {
            "lead_bank": "Bank of Baroda",
            "ldm_office": "Lead District Manager Office, Bank of Baroda Building, Ashram Road, Ahmedabad",
            "rrbs": ["Saurashtra Gramin Bank", "Baroda Gujarat Gramin Bank"],
            "commercial": ["State Bank of India (Bhadra Main Branch)", "Canara Bank", "Union Bank of India"],
            "dic_office": "District Industries Centre, Bahumali Bhawan, Drive-In Road, Ahmedabad",
            "sca_office": "Gujarat Backward Classes / SC Development Corp, Gandhinagar/Ahmedabad",
        },
    },
    "bihar": {
        "patna": {
            "lead_bank": "Punjab National Bank",
            "ldm_office": "Lead District Manager Office, PNB Zonal Office, Exhibition Road, Patna",
            "rrbs": ["Dakshin Bihar Gramin Bank", "Uttar Bihar Gramin Bank"],
            "commercial": ["State Bank of India (West Gandhi Maidan)", "Canara Bank", "Central Bank of India"],
            "dic_office": "District Industries Centre, Industrial Estate, Patliputra, Patna",
            "sca_office": "Bihar State SC/ST Development Corp, Indira Bhawan, Patna",
        },
    },
    "telangana": {
        "hyderabad": {
            "lead_bank": "State Bank of India",
            "ldm_office": "Lead District Manager Office, SBI Local Head Office, Koti, Hyderabad",
            "rrbs": ["Telangana Grameena Bank", "Andhra Pradesh Grameena Vikas Bank"],
            "commercial": ["Canara Bank (Abids)", "Union Bank of India (Andhra Bank building Koti)", "Punjab National Bank"],
            "dic_office": "District Industries Centre, Chirag Ali Lane, Abids, Hyderabad",
            "sca_office": "Telangana SC Co-Operative Development Corp (TSSCCDC), Masab Tank, Hyderabad",
        },
    },
}


# Generic state Lead Bank fallback directory for districts not listed individually
STATE_LEAD_BANK_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "uttar pradesh": {"lead_bank": "Bank of Baroda", "rrbs": ["Baroda UP Bank", "Aryavart Bank"], "major_psb": "State Bank of India"},
    "maharashtra": {"lead_bank": "Bank of Maharashtra", "rrbs": ["Maharashtra Gramin Bank"], "major_psb": "State Bank of India"},
    "tamil nadu": {"lead_bank": "Indian Overseas Bank", "rrbs": ["Tamil Nadu Grama Bank"], "major_psb": "Canara Bank"},
    "karnataka": {"lead_bank": "Canara Bank", "rrbs": ["Karnataka Gramin Bank"], "major_psb": "State Bank of India"},
    "delhi": {"lead_bank": "State Bank of India", "rrbs": ["Delhi State Co-operative Bank"], "major_psb": "Punjab National Bank"},
    "west bengal": {"lead_bank": "UCO Bank", "rrbs": ["Bangiya Gramin Vikash Bank"], "major_psb": "State Bank of India"},
    "rajasthan": {"lead_bank": "Bank of Baroda", "rrbs": ["Baroda Rajasthan Kshetriya Gramin Bank"], "major_psb": "State Bank of India"},
    "madhya pradesh": {"lead_bank": "Bank of India", "rrbs": ["Madhyanchal Gramin Bank", "MP Gramin Bank"], "major_psb": "State Bank of India"},
    "gujarat": {"lead_bank": "Bank of Baroda", "rrbs": ["Baroda Gujarat Gramin Bank"], "major_psb": "State Bank of India"},
    "bihar": {"lead_bank": "Punjab National Bank", "rrbs": ["Dakshin Bihar Gramin Bank"], "major_psb": "State Bank of India"},
    "telangana": {"lead_bank": "State Bank of India", "rrbs": ["Telangana Grameena Bank"], "major_psb": "Union Bank of India"},
    "andhra pradesh": {"lead_bank": "Union Bank of India", "rrbs": ["Andhra Pragathi Grameena Bank"], "major_psb": "State Bank of India"},
    "kerala": {"lead_bank": "Canara Bank", "rrbs": ["Kerala Gramin Bank"], "major_psb": "State Bank of India"},
    "punjab": {"lead_bank": "Punjab National Bank", "rrbs": ["Punjab Gramin Bank"], "major_psb": "State Bank of India"},
    "haryana": {"lead_bank": "Punjab National Bank", "rrbs": ["Sarva Haryana Gramin Bank"], "major_psb": "State Bank of India"},
    "odisha": {"lead_bank": "UCO Bank", "rrbs": ["Odisha Gramya Bank"], "major_psb": "State Bank of India"},
    "assam": {"lead_bank": "State Bank of India", "rrbs": ["Assam Gramin Vikash Bank"], "major_psb": "Punjab National Bank"},
}


HINDI_LOCATION_ALIASES: Dict[str, Tuple[Optional[str], Optional[str]]] = {
    # Districts & Cities
    "वाराणसी": ("Uttar Pradesh", "Varanasi"),
    "बनारस": ("Uttar Pradesh", "Varanasi"),
    "काशी": ("Uttar Pradesh", "Varanasi"),
    "लखनऊ": ("Uttar Pradesh", "Lucknow"),
    "कानपुर": ("Uttar Pradesh", "Kanpur"),
    "आगरा": ("Uttar Pradesh", "Agra"),
    "प्रयागराज": ("Uttar Pradesh", "Prayagraj"),
    "इलाहाबाद": ("Uttar Pradesh", "Prayagraj"),
    "मेरठ": ("Uttar Pradesh", "Meerut"),
    "गोरखपुर": ("Uttar Pradesh", "Gorakhpur"),
    "मुंबई": ("Maharashtra", "Mumbai"),
    "बॉम्बे": ("Maharashtra", "Mumbai"),
    "पुणे": ("Maharashtra", "Pune"),
    "नागपुर": ("Maharashtra", "Nagpur"),
    "नासिक": ("Maharashtra", "Nashik"),
    "चेन्नई": ("Tamil Nadu", "Chennai"),
    "मद्रास": ("Tamil Nadu", "Chennai"),
    "कोयंबटूर": ("Tamil Nadu", "Coimbatore"),
    "मदुरै": ("Tamil Nadu", "Madurai"),
    "बेंगलुरु": ("Karnataka", "Bengaluru"),
    "बैंगलोर": ("Karnataka", "Bengaluru"),
    "मैसूर": ("Karnataka", "Mysuru"),
    "कोलकाता": ("West Bengal", "Kolkata"),
    "कलकत्ता": ("West Bengal", "Kolkata"),
    "जयपुर": ("Rajasthan", "Jaipur"),
    "अहमदाबाद": ("Gujarat", "Ahmedabad"),
    "सूरत": ("Gujarat", "Surat"),
    "पटना": ("Bihar", "Patna"),
    "हैदराबाद": ("Telangana", "Hyderabad"),
    "भोपाल": ("Madhya Pradesh", "Bhopal"),
    "इंदौर": ("Madhya Pradesh", "Indore"),
    # States
    "उत्तर प्रदेश": ("Uttar Pradesh", None),
    "यूपी": ("Uttar Pradesh", None),
    "महाराष्ट्र": ("Maharashtra", None),
    "तमिलनाडु": ("Tamil Nadu", None),
    "तमिल नाडु": ("Tamil Nadu", None),
    "कर्नाटक": ("Karnataka", None),
    "दिल्ली": ("Delhi", None),
    "नई दिल्ली": ("Delhi", "New Delhi"),
    "पश्चिम बंगाल": ("West Bengal", None),
    "राजस्थान": ("Rajasthan", None),
    "गुजरात": ("Gujarat", None),
    "बिहार": ("Bihar", None),
    "मध्य प्रदेश": ("Madhya Pradesh", None),
    "एमपी": ("Madhya Pradesh", None),
    "तेलंगाना": ("Telangana", None),
}


class BankLocatorService:
    """Service to locate Lead Banks, RRBs, and nodal offices based on scheme and location."""

    def __init__(self):
        pass

    def extract_location_from_text(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extract State and District mentions from natural language query text (English & Devanagari Hindi).
        """
        text_lower = text.lower()
        found_state = None
        found_district = None

        # 0. Check Devanagari Hindi aliases
        for alias, (st, dt) in HINDI_LOCATION_ALIASES.items():
            if alias in text:
                if st and not found_state:
                    found_state = st
                if dt and not found_district:
                    found_district = dt
                if found_state and found_district:
                    break

        # 1. Match State (English)
        if not found_state:
            for state_key in DISTRICT_BANK_DATABASE.keys():
                if state_key in text_lower:
                    found_state = state_key.title()
                    break
        if not found_state:
            for state_key in STATE_LEAD_BANK_DEFAULTS.keys():
                if state_key in text_lower:
                    found_state = state_key.title()
                    break

        # Check common state abbreviations
        if not found_state:
            abbrevs = {"up": "Uttar Pradesh", "tn": "Tamil Nadu", "mp": "Madhya Pradesh", "wb": "West Bengal"}
            for abbrev, full_name in abbrevs.items():
                if re_match := f"\\b{abbrev}\\b":
                    import re
                    if re.search(re_match, text_lower):
                        found_state = full_name
                        break

        # 2. Match District (English)
        if not found_district:
            search_states = [found_state.lower()] if found_state and found_state.lower() in DISTRICT_BANK_DATABASE else DISTRICT_BANK_DATABASE.keys()
            for sk in search_states:
                for dist_key in DISTRICT_BANK_DATABASE[sk].keys():
                    if dist_key in text_lower:
                        found_district = dist_key.title()
                        if not found_state:
                            found_state = sk.title()
                        break
                if found_district:
                    break

        return {"state": found_state, "district": found_district}

    def get_district_profile(self, state: str, district: Optional[str] = None) -> DistrictBankingProfile:
        """Fetch or synthesize a district banking profile."""
        norm_state = (state or "").strip().lower()
        norm_dist = (district or "").strip().lower()

        # Direct database hit
        if norm_state in DISTRICT_BANK_DATABASE and norm_dist in DISTRICT_BANK_DATABASE[norm_state]:
            info = DISTRICT_BANK_DATABASE[norm_state][norm_dist]
            return DistrictBankingProfile(
                state=state.title(),
                district=district.title(),
                lead_bank=info["lead_bank"],
                ldm_office=info["ldm_office"],
                regional_rural_banks=info.get("rrbs", []),
                prominent_commercial_banks=info.get("commercial", []),
                dic_office=info.get("dic_office", f"District Industries Centre (DIC), {district.title()}"),
                sca_office=info.get("sca_office", f"State SC/ST & Backward Classes Finance Development Corporation, Vikas Bhawan, {district.title()}"),
            )

        # Fallback using state default Lead Bank
        state_def = STATE_LEAD_BANK_DEFAULTS.get(norm_state, {
            "lead_bank": "State Bank of India",
            "rrbs": ["Local Regional Rural Bank (RRB)"],
            "major_psb": "Punjab National Bank"
        })

        dist_name = district.title() if district else "District Headquarters"
        lead_bank_name = state_def.get("lead_bank", "State Bank of India")

        return DistrictBankingProfile(
            state=state.title() if state else "All-India",
            district=dist_name,
            lead_bank=lead_bank_name,
            ldm_office=f"Lead District Manager (LDM) Office, {lead_bank_name} Administrative Office, {dist_name}",
            regional_rural_banks=state_def.get("rrbs", ["Regional Rural Bank (RRB) Network"]),
            prominent_commercial_banks=[
                f"State Bank of India (Main SME Branch, {dist_name})",
                f"{lead_bank_name} (Main Branch / SME Hub, {dist_name})",
                f"Punjab National Bank ({dist_name})",
                f"Canara Bank ({dist_name})",
            ],
            dic_office=f"District Industries Centre (DIC), Industrial Estate / Vikas Bhawan, {dist_name}",
            sca_office=f"State SC/ST & Backward Classes Development Corporation, Vikas Bhawan / Collectorate, {dist_name}",
        )

    def recommend_banks(
        self,
        scheme_code: str,
        scheme_name: str,
        state: str,
        district: Optional[str] = None,
    ) -> BankRecommendation:
        """
        Generate detailed, actionable bank and nodal agency recommendations for a scheme and location.
        """
        profile = self.get_district_profile(state=state, district=district)
        code_upper = (scheme_code or "").upper()

        primary_lending_banks = []
        rrbs_info = []
        nodal_offices = []
        steps = []
        documents = [
            "Aadhaar Card and PAN Card of the applicant/promoters",
            "Caste Certificate (issued by competent Tahsildar / SDO) for SC/ST/OBC applicants",
            "Detailed Project Report (DPR) / Business Plan with Cost Estimation",
            "Machinery / Equipment Quotations from GST-registered vendors",
            "Bank Account Statement for the last 6 months",
            "Proof of business premises (Rent agreement / Title deed / Electricity bill)",
            "Udyam Registration Certificate (can be obtained free on udyamregistration.gov.in)",
        ]

        # 1. Lead Bank Main Entry
        primary_lending_banks.append({
            "bank_name": profile.lead_bank,
            "category": "Designated Lead District Bank (LDB)",
            "priority": "Highest Recommendation",
            "branch_desk": f"MSME / Priority Sector Lending Desk, Main Branch, {profile.district}",
            "contact_guide": f"Ask for the Lead District Manager (LDM) or Chief Manager (Credit/MSME).",
        })

        # 2. Add prominent commercial branches
        for b_name in profile.prominent_commercial_banks:
            if profile.lead_bank not in b_name:
                primary_lending_banks.append({
                    "bank_name": b_name,
                    "category": "Scheduled Commercial Bank",
                    "priority": "Recommended",
                    "branch_desk": "SME City Credit Centre / MSME Loan Desk",
                    "contact_guide": "Meet the Credit Officer handling Government Sponsored Schemes.",
                })

        # 3. Regional Rural Banks
        for rrb in profile.regional_rural_banks:
            rrbs_info.append({
                "bank_name": rrb,
                "category": "Regional Rural Bank (RRB)",
                "specialty": "Fast-track rural and semi-urban small enterprise financing with priority sector focus.",
            })

        # 4. Scheme-specific Nodal routing & Guidance
        if "STANDUP" in code_upper:
            nodal_offices.append(NodalOffice(
                agency="Lead District Manager (LDM) Office",
                location=profile.ldm_office,
                role="Monitors mandatory branch quota: Every commercial bank branch must sanction at least 1 SC/ST and 1 Woman greenfield project (₹10L to ₹1Cr)."
            ))
            nodal_offices.append(NodalOffice(
                agency="SIDBI Stand-Up Mitra Desk",
                location="Online portal www.standupmitra.in & nearest SIDBI Branch",
                role="Connects applicants directly to Lead Bank branch managers and provides Handholding Agencies."
            ))
            steps = [
                "1. Register on www.standupmitra.in and fill in your greenfield project details (₹10L - ₹1Cr).",
                f"2. Select '{profile.lead_bank}' or 'State Bank of India' branch in {profile.district} as your preferred bank.",
                "3. Keep the 15% margin money proof ready (can be combined with eligible central/state subsidies).",
                f"4. Visit the branch MSME credit officer with your Stand-Up India Application Slip.",
                f"5. If branch delays, visit the Lead District Manager (LDM) at {profile.ldm_office} for prompt intervention.",
            ]

        elif "PMEGP" in code_upper:
            nodal_offices.append(NodalOffice(
                agency="District Industries Centre (DIC)",
                location=profile.dic_office,
                role="District implementing agency that convenes the DLTFC interview and forwards approved files to bank branches."
            ))
            nodal_offices.append(NodalOffice(
                agency="KVIC / KVIB District Office",
                location=f"Khadi and Village Industries Commission / Board, {profile.district}",
                role="Sponsors rural enterprise applications and disburses the 25% - 35% margin money subsidy."
            ))
            steps = [
                "1. Apply online on the KVIC PMEGP e-Portal (www.kviconline.gov.in) under Agency: DIC or KVIC.",
                f"2. Choose '{profile.lead_bank}' or your nearest nationalized bank in {profile.district} as Financing Bank.",
                "3. Submit self-attested EDP training certificate (or complete online e-EDP after application).",
                "4. DLTFC (District Level Task Force Committee) reviews and sends recommendation to your branch.",
                "5. Branch inspects premises, sanctions loan, and subsidy is held as 3-year term deposit credit.",
            ]

        elif "VISHWAKARMA" in code_upper:
            nodal_offices.append(NodalOffice(
                agency="District Industries Centre (DIC)",
                location=profile.dic_office,
                role="Verifies Stage-2 artisan verification submitted from Gram Panchayat / Urban Local Body."
            ))
            nodal_offices.append(NodalOffice(
                agency="MSME-DFO / District MSME Cell",
                location=f"MSME Development & Facilitation Office, {profile.state}",
                role="Conducts 5-day basic skill training, toolkit distribution voucher (₹15,000), and credit linkage."
            ))
            steps = [
                "1. Complete verification through Common Service Centre (CSC) or pmvishwakarma.gov.in.",
                "2. Complete 5 to 7 days Basic Skill Training (receives ₹500/day stipend + ₹15,000 toolkit voucher).",
                f"3. Apply for 1st Tranche Loan (₹1 Lakh @ 5% interest) through {profile.lead_bank} or your local RRB branch.",
                "4. Collateral-free loan with 100% guarantee by Credit Guarantee Trust for Micro and Small Enterprises (CGTMSE).",
            ]

        elif "SVANIDHI" in code_upper:
            nodal_offices.append(NodalOffice(
                agency="Urban Local Body (Nagar Nigam / Municipality)",
                location=f"Municipal Corporation Office / Town Vending Committee (TVC), {profile.district}",
                role="Issues Certificate of Vending / Letter of Recommendation (LoR) required for loan access."
            ))
            steps = [
                "1. Get Certificate of Vending from your Nagar Nigam / Municipality TVC in {profile.district}.",
                f"2. Apply via pmsvanidhi.mohua.gov.in choosing {profile.lead_bank} or nearby Small Finance Bank.",
                "3. Working capital loan of ₹10,000 (1st tranche) sanctioned directly to bank account within 7 days.",
                "4. Repay on time via UPI/digital transactions to unlock 7% interest subsidy and higher 2nd tranche (₹20,000).",
            ]

        elif "NSFDC" in code_upper or "NBCFDC" in code_upper or "VCF" in code_upper:
            nodal_offices.append(NodalOffice(
                agency="State SC/ST/OBC Development Corporation (SCA)",
                location=profile.sca_office or f"Vikas Bhawan, {profile.district}",
                role="Nodal Channelizing Agency for Ministry of Social Justice & Empowerment (MoSJE) concessional credit and subsidies."
            ))
            steps = [
                f"1. Collect the Channelizing Scheme application form from {profile.sca_office or 'Vikas Bhawan'}.",
                f"2. Submit Project proposal and Caste/Income proof to the District SC/OBC Welfare Officer.",
                f"3. State Corporation forwards file with subsidy endorsement to '{profile.lead_bank}' or partner RRB branch.",
                "4. Bank sanctions composite loan with concessional interest rate (4% - 6% p.a.).",
            ]

        else:
            # General / MUDRA / Other Schemes
            nodal_offices.append(NodalOffice(
                agency="District Industries Centre (DIC)",
                location=profile.dic_office,
                role=f"Industrial guidance and credit facilitation for {profile.district} entrepreneurs."
            ))
            nodal_offices.append(NodalOffice(
                agency="Lead District Manager (LDM) Office",
                location=profile.ldm_office,
                role="Coordinates credit disbursals and branch targets under Priority Sector Lending (PSL)."
            ))
            steps = [
                f"1. Approach the SME / Micro-Enterprise credit desk at '{profile.lead_bank}' or nearby commercial bank in {profile.district}.",
                "2. Submit your loan application under the scheme (MUDRA / General MSME Loan).",
                "3. Present Project Cost Sheet, vendor quotations, and Udyam Registration.",
                "4. Loans up to ₹10 Lakhs under MUDRA are strictly collateral-free (covered by CGFMU).",
            ]

        return BankRecommendation(
            state=profile.state,
            district=profile.district,
            scheme_name=scheme_name,
            scheme_code=scheme_code,
            lead_bank_name=profile.lead_bank,
            ldm_office_info=profile.ldm_office,
            primary_lending_banks=primary_lending_banks,
            regional_rural_banks=rrbs_info,
            district_nodal_offices=nodal_offices,
            application_steps=steps,
            required_documents=documents,
        )


# Global Bank Locator singleton
bank_locator = BankLocatorService()
