"""
Source catalog of verified Central and State Government scheme portals and guidelines.
Allows automated discovery and batch crawling without requiring users to manually specify URLs.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class GovernmentSource(BaseModel):
    id: str
    name: str
    ministry: str
    target_categories: List[str]
    portal_url: str
    guideline_urls: List[str] = Field(default_factory=list)
    description: str
    tags: List[str] = Field(default_factory=list)
    state: Optional[str] = None  # None for Central schemes


# Pre-seeded verified Government sources
DEFAULT_SOURCES: List[GovernmentSource] = [
    GovernmentSource(
        id="pm-vishwakarma",
        name="PM Vishwakarma Scheme",
        ministry="Ministry of Micro, Small and Medium Enterprises (MSME)",
        target_categories=["Artisan", "SC", "ST", "OBC", "Women"],
        portal_url="https://pmvishwakarma.gov.in",
        guideline_urls=["https://pmvishwakarma.gov.in"],
        description="Holistic end-to-end support to traditional artisans and craftspeople (Vishwakarmas) with collateral-free loans up to Rs. 3 Lakhs, toolkit incentives, and skill training.",
        tags=["artisan", "credit", "subsidy", "training", "toolkits"],
    ),
    GovernmentSource(
        id="standup-india",
        name="Stand-Up India Scheme",
        ministry="Ministry of Finance / SIDBI",
        target_categories=["SC", "ST", "Women"],
        portal_url="https://www.standupmitra.in",
        guideline_urls=["https://www.standupmitra.in"],
        description="Facilitates bank loans between Rs. 10 Lakhs and Rs. 1 Crore to at least one SC or ST borrower and at least one woman borrower per bank branch for setting up a greenfield enterprise.",
        tags=["enterprise", "women", "sc", "st", "greenfield"],
    ),
    GovernmentSource(
        id="pmegp",
        name="Prime Minister's Employment Generation Programme (PMEGP)",
        ministry="Ministry of Micro, Small and Medium Enterprises (MSME)",
        target_categories=["SC", "ST", "OBC", "Women", "Minority", "PwD", "General"],
        portal_url="https://www.kviconline.gov.in/pmegpeportal/pmegphome/index.jsp",
        guideline_urls=["https://www.kviconline.gov.in"],
        description="Credit-linked subsidy programme for generation of employment opportunities through establishment of micro enterprises up to Rs. 50 Lakhs (manufacturing) and Rs. 20 Lakhs (services) with up to 35% subsidy.",
        tags=["msme", "credit-linked", "subsidy", "self-employment"],
    ),
    GovernmentSource(
        id="pm-mudra",
        name="Pradhan Mantri MUDRA Yojana (PMMY)",
        ministry="Ministry of Finance",
        target_categories=["General", "OBC", "SC", "ST", "Women"],
        portal_url="https://www.mudra.org.in",
        guideline_urls=["https://www.mudra.org.in"],
        description="Provides loans up to Rs. 20 Lakhs to non-corporate, non-farm small/micro enterprises categorized under Shishu, Kishore, and Tarun buckets.",
        tags=["mudra", "micro-finance", "working-capital", "collateral-free"],
    ),
    GovernmentSource(
        id="pm-svanidhi",
        name="PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)",
        ministry="Ministry of Housing and Urban Affairs (MoHUA)",
        target_categories=["Street Vendor", "General", "OBC", "SC", "ST"],
        portal_url="https://pmsvanidhi.mohua.gov.in",
        guideline_urls=["https://pmsvanidhi.mohua.gov.in"],
        description="Micro-credit facility for street vendors to access affordable collateral-free working capital loan starting at Rs. 10,000 up to Rs. 50,000 with 7% interest subsidy.",
        tags=["street-vendors", "working-capital", "interest-subsidy", "urban"],
    ),
    GovernmentSource(
        id="nsfdc-term-loan",
        name="NSFDC Term Loan Scheme",
        ministry="Ministry of Social Justice and Empowerment (MoSJE)",
        target_categories=["SC"],
        portal_url="https://nsfdc.nic.in",
        guideline_urls=["https://nsfdc.nic.in"],
        description="Financial assistance for viable income-generating projects up to Rs. 50 Lakhs for Scheduled Caste beneficiaries living below double poverty line / annual income Rs. 3 Lakhs.",
        tags=["sc", "mosje", "term-loan", "concessional-credit"],
    ),
    GovernmentSource(
        id="nsfdc-mcf",
        name="NSFDC Micro Credit Finance (MCF)",
        ministry="Ministry of Social Justice and Empowerment (MoSJE)",
        target_categories=["SC"],
        portal_url="https://nsfdc.nic.in",
        guideline_urls=["https://nsfdc.nic.in"],
        description="Small loans up to Rs. 1.5 Lakhs per beneficiary through State Channelizing Agencies / Micro Finance Institutions for target group SC entrepreneurs.",
        tags=["sc", "micro-credit", "mosje", "poverty-alleviation"],
    ),
    GovernmentSource(
        id="nbcfdc-general",
        name="NBCFDC General Loan Scheme",
        ministry="Ministry of Social Justice and Empowerment (MoSJE)",
        target_categories=["OBC"],
        portal_url="https://nbcfdc.gov.in",
        guideline_urls=["https://nbcfdc.gov.in"],
        description="Concessional financial assistance to Other Backward Classes (OBC) for establishing self-employment ventures with project cost up to Rs. 15 Lakhs.",
        tags=["obc", "mosje", "concessional-loan", "backward-classes"],
    ),
    GovernmentSource(
        id="nskfdc-swachhata",
        name="NSKFDC Swachhata Udyami Yojana (SUY)",
        ministry="Ministry of Social Justice and Empowerment (MoSJE)",
        target_categories=["Safai Karamchari", "SC"],
        portal_url="https://nskfdc.nic.in",
        guideline_urls=["https://nskfdc.nic.in"],
        description="Financial assistance to Safai Karamcharis, manual scavengers, and their dependents for procurement and operation of sanitation-related equipment/vehicles up to Rs. 50 Lakhs with capital subsidy.",
        tags=["safai-karamchari", "sanitation", "mechanization", "subsidy"],
    ),
    GovernmentSource(
        id="vcf-sc",
        name="Venture Capital Fund for Scheduled Castes (VCF-SC)",
        ministry="Ministry of Social Justice and Empowerment (MoSJE)",
        target_categories=["SC"],
        portal_url="https://vcfsc.in",
        guideline_urls=["https://vcfsc.in"],
        description="Concessional equity and quasi-equity funding up to Rs. 15 Crores for SC entrepreneurs establishing high-growth manufacturing, technology, and service companies.",
        tags=["sc", "venture-capital", "equity", "high-growth"],
    ),
    GovernmentSource(
        id="nstfdc-amasy",
        name="Adivasi Mahila Sashaktikaran Yojana (AMASY)",
        ministry="Ministry of Tribal Affairs (MoTA)",
        target_categories=["ST", "Women"],
        portal_url="https://nstfdc.tribal.gov.in",
        guideline_urls=["https://nstfdc.tribal.gov.in"],
        description="Concessional scheme exclusively for economic development of Scheduled Tribe women. Loan assistance up to Rs. 2 Lakhs per unit at highly subsidized interest rate of 4% per annum.",
        tags=["st", "tribal", "women", "concessional-interest"],
    ),
    GovernmentSource(
        id="nstfdc-term-loan",
        name="NSTFDC Term Loan Scheme for Scheduled Tribes",
        ministry="Ministry of Tribal Affairs (MoTA)",
        target_categories=["ST"],
        portal_url="https://nstfdc.tribal.gov.in",
        guideline_urls=["https://nstfdc.tribal.gov.in"],
        description="Term loans up to Rs. 50 Lakhs for individual or group income-generating activities for eligible Scheduled Tribe members.",
        tags=["st", "tribal", "term-loan", "self-employment"],
    ),
    GovernmentSource(
        id="nmdfc-term-loan",
        name="NMDFC Term Loan Scheme for Minorities",
        ministry="Ministry of Minority Affairs (MoMA)",
        target_categories=["Minority"],
        portal_url="https://nmdfc.org",
        guideline_urls=["https://nmdfc.org"],
        description="Concessional credit to notified minority communities (Muslims, Christians, Sikhs, Buddhists, Jains, Parsis) with project cost up to Rs. 30 Lakhs for setting up enterprises.",
        tags=["minority", "concessional-credit", "moma", "entrepreneurship"],
    ),
    GovernmentSource(
        id="day-nrlm",
        name="Deendayal Antyodaya Yojana - National Rural Livelihoods Mission (DAY-NRLM)",
        ministry="Ministry of Rural Development (MoRD)",
        target_categories=["Women", "SC", "ST", "General"],
        portal_url="https://aajeevika.gov.in",
        guideline_urls=["https://aajeevika.gov.in"],
        description="Poverty relief program promoting self-employment through Self Help Groups (SHGs), revolving funds, capital subsidy, and bank credit linkage with interest subvention down to 7%.",
        tags=["shg", "rural", "women-empowerment", "interest-subvention"],
    ),
    GovernmentSource(
        id="up-yuva-swarojgar",
        name="Mukhyamantri Yuva Swarojgar Yojana (Uttar Pradesh)",
        ministry="Department of MSME and Export Promotion, Government of Uttar Pradesh",
        target_categories=["SC", "ST", "OBC", "General", "Women"],
        portal_url="https://diupmsme.upsdc.gov.in",
        guideline_urls=["https://diupmsme.upsdc.gov.in"],
        description="State self-employment scheme offering composite loans up to Rs. 25 Lakhs for industry and Rs. 10 Lakhs for service sector with 25% margin money subsidy.",
        tags=["state-scheme", "uttar-pradesh", "youth", "subsidy"],
        state="Uttar Pradesh",
    ),
    GovernmentSource(
        id="tn-needs",
        name="New Entrepreneur-cum-Enterprise Development Scheme (NEEDS - Tamil Nadu)",
        ministry="Micro, Small and Medium Enterprises Department, Tamil Nadu",
        target_categories=["General", "SC", "ST", "OBC", "Women"],
        portal_url="https://msmeonline.tn.gov.in/needs",
        guideline_urls=["https://msmeonline.tn.gov.in/needs"],
        description="Assisting educated youth to establish manufacturing or service greenfield projects with project cost Rs. 10 Lakhs to Rs. 5 Crores and 25% capital subsidy.",
        tags=["state-scheme", "tamil-nadu", "greenfield", "capital-subsidy"],
        state="Tamil Nadu",
    ),
]


class SourceCatalog:
    """Registry that holds pre-configured sources and dynamically added sources."""

    def __init__(self):
        self._sources: Dict[str, GovernmentSource] = {s.id: s for s in DEFAULT_SOURCES}

    def get_all_sources(self) -> List[GovernmentSource]:
        return list(self._sources.values())

    def get_source_by_id(self, source_id: str) -> Optional[GovernmentSource]:
        return self._sources.get(source_id)

    def filter_sources(
        self,
        ministry: Optional[str] = None,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        state: Optional[str] = None,
    ) -> List[GovernmentSource]:
        results = list(self._sources.values())

        if ministry:
            min_lower = ministry.lower()
            results = [s for s in results if min_lower in s.ministry.lower()]

        if category:
            cat_upper = category.strip().upper()
            results = [
                s for s in results
                if any(c.upper() == cat_upper or c.upper() in ["ALL", "GENERAL"] for c in s.target_categories)
            ]

        if tag:
            tag_lower = tag.strip().lower()
            results = [s for s in results if any(tag_lower in t.lower() for t in s.tags)]

        if state is not None:
            if state == "":
                results = [s for s in results if s.state is None]
            else:
                results = [s for s in results if s.state and state.lower() in s.state.lower()]

        return results

    def add_source(self, source: GovernmentSource) -> GovernmentSource:
        self._sources[source.id] = source
        return source

    def get_unique_ministries(self) -> List[str]:
        return sorted(list(set(s.ministry for s in self._sources.values())))

    def get_unique_categories(self) -> List[str]:
        cats = set()
        for s in self._sources.values():
            cats.update(s.target_categories)
        return sorted(list(cats))


# Global catalog singleton instance
catalog = SourceCatalog()
