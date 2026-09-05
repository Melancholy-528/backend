"""
Detailed Project Report (DPR) & Financial Subsidy / EMI Calculator.
Calculates Own Margin Money, Government Subsidy, Bank Loan components, and monthly EMI
specifically adapted for Indian welfare and enterprise schemes (PMEGP, Stand-Up India, MUDRA, PM Vishwakarma).
"""

import math
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class DPRRequest(BaseModel):
    project_cost: float = Field(..., gt=0, description="Total project or business cost in INR (e.g. 1500000)")
    scheme_code: str = Field(..., description="Target scheme code (e.g. PMEGP, STANDUP-INDIA, MUDRA, PM-VISHWAKARMA)")
    category: str = Field(default="General", description="Applicant category: SC, ST, OBC, Women, Minority, PwD, General")
    is_rural: bool = Field(default=True, description="Whether the enterprise is located in a rural or urban area")
    tenure_years: int = Field(default=5, ge=1, le=10, description="Repayment tenure in years (typically 3 to 7 years)")
    interest_rate: Optional[float] = Field(default=None, description="Annual interest rate percentage (optional override)")


class EMIPlan(BaseModel):
    tenure_years: int
    monthly_emi: float
    total_interest: float
    total_payment: float


class DPRResponse(BaseModel):
    scheme_code: str
    scheme_name: str
    total_project_cost: float
    category: str
    area_type: str
    
    # Financial breakdown
    own_contribution_rate_pct: float
    own_contribution_amount: float
    subsidy_rate_pct: float
    subsidy_amount: float
    bank_loan_amount: float
    term_loan_estimate: float
    working_capital_estimate: float
    
    # Repayment & EMI
    annual_interest_rate_pct: float
    emi_details: EMIPlan
    
    # Bank appraisal readiness notes
    subsidy_mechanism: str
    collateral_requirement: str
    recommended_nodal_portal: str
    checklist_for_bank_interview: List[str]


class DPRCalculatorService:
    """Computes bank appraisal and DPR cost breakdowns."""

    def compute_dpr(self, req: DPRRequest) -> DPRResponse:
        cost = req.project_cost
        code = req.scheme_code.strip().upper()
        cat = req.category.strip().upper()
        is_special = any(k in cat for k in ["SC", "ST", "WOMEN", "OBC", "MINORITY", "PWD", "DIVYANG", "ARTISAN"])

        # Default rules
        own_pct = 10.0
        subsidy_pct = 0.0
        interest_rate = req.interest_rate or 9.5
        scheme_name = req.scheme_code
        subsidy_mechanism = "No direct capital subsidy. Interest subvention or low interest rate applies."
        collateral_req = "Covered under CGTMSE credit guarantee up to ₹5 Crore (No third-party collateral needed)."
        portal = "https://www.udyamregistration.gov.in"

        if "PMEGP" in code:
            scheme_name = "Prime Minister’s Employment Generation Programme (PMEGP)"
            portal = "https://www.kviconline.gov.in"
            if is_special:
                own_pct = 5.0
                subsidy_pct = 35.0 if req.is_rural else 25.0
            else:
                own_pct = 10.0
                subsidy_pct = 25.0 if req.is_rural else 15.0

            interest_rate = req.interest_rate or 9.0
            subsidy_mechanism = (
                f"Government capital subsidy of {subsidy_pct}% (₹{(cost * subsidy_pct / 100):,.0f}) is credited into "
                "a Margin Money TDR account by KVIC/DIC and adjusted against the loan after 3 years of physical verification."
            )
            collateral_req = "Strictly collateral-free for projects up to ₹10 Lakhs (covered under CGTMSE without collateral)."

        elif "STANDUP" in code or "STAND-UP" in code:
            scheme_name = "Stand-Up India Scheme for SC, ST & Women Entrepreneurs"
            portal = "https://www.standupmitra.in"
            own_pct = 15.0  # Margin money
            subsidy_pct = 15.0  # Margin money assistance / state convergence
            interest_rate = req.interest_rate or 8.5
            subsidy_mechanism = (
                "Composite loan (Term Loan + Working Capital) covering up to 85% of project cost. "
                "The 15% margin money requirement can be met through eligible Central/State capital subsidies."
            )
            collateral_req = "Collateral-free through Credit Guarantee Scheme for Stand-Up India (CGSSI) or primary security of assets created."

        elif "VISHWAKARMA" in code:
            scheme_name = "PM Vishwakarma Scheme"
            portal = "https://pmvishwakarma.gov.in"
            own_pct = 0.0
            subsidy_pct = 0.0
            interest_rate = 5.0  # Concessional 5% interest with 8% subvention paid by MoMSME
            subsidy_mechanism = "Direct 8% interest subvention paid by Central Govt to the bank + ₹15,000 modern toolkit voucher."
            collateral_req = "100% collateral-free, guaranteed by NCGTC."

        elif "MUDRA" in code:
            scheme_name = "Pradhan Mantri Mudra Yojana (PMMY)"
            portal = "https://www.mudra.org.in"
            own_pct = 10.0
            subsidy_pct = 0.0
            interest_rate = req.interest_rate or 9.5
            subsidy_mechanism = "No capital subsidy. Refinance support provided to banks with collateral-free lending under CGFMU."
            collateral_req = "Strictly NO collateral or third-party guarantee permitted by RBI guidelines."

        elif "NSFDC" in code or "NBCFDC" in code:
            scheme_name = "National SC/ST/OBC Finance and Development Corporation Loan"
            portal = "https://nsfdc.nic.in"
            own_pct = 5.0 if is_special else 10.0
            subsidy_pct = 10.0
            interest_rate = req.interest_rate or 6.0
            subsidy_mechanism = "MoSJE margin money grant/subsidy up to ₹10,000 or 10% of project cost through State SCA."
            collateral_req = "Hypothecation of assets created out of loan assistance."

        # Calculations
        own_amount = cost * (own_pct / 100.0)
        subsidy_amount = cost * (subsidy_pct / 100.0)
        bank_loan = cost - own_amount

        # Split into Term Loan (Machinery/CapEx ~70%) and Working Capital (~30%)
        term_loan = round(bank_loan * 0.70, 2)
        working_cap = round(bank_loan * 0.30, 2)

        # Standard Equated Monthly Installment (EMI) Formula:
        # P * r * (1 + r)^n / ((1 + r)^n - 1)
        # where P = bank_loan, r = monthly interest, n = total months
        n_months = req.tenure_years * 12
        monthly_r = (interest_rate / 100.0) / 12.0

        if monthly_r > 0:
            emi = bank_loan * (monthly_r * math.pow(1 + monthly_r, n_months)) / (math.pow(1 + monthly_r, n_months) - 1)
        else:
            emi = bank_loan / n_months

        monthly_emi = round(emi, 2)
        total_payment = round(monthly_emi * n_months, 2)
        total_interest = round(total_payment - bank_loan, 2)

        checklist = [
            f"1. Proof of Own Contribution: ₹{own_amount:,.0f} ready in your bank savings account.",
            "2. Machinery / Equipment Quotations with GST numbers from authorized dealers.",
            "3. Project Feasibility Sheet showing projected sales, cost of raw materials, and gross margin.",
            "4. KYC: Aadhaar, PAN Card, Category/Caste Certificate (if SC/ST/OBC), and 6 months bank statement.",
            f"5. Apply through the official portal ({portal}) before meeting the bank branch credit officer.",
        ]

        return DPRResponse(
            scheme_code=code,
            scheme_name=scheme_name,
            total_project_cost=cost,
            category=req.category,
            area_type="Rural Area" if req.is_rural else "Urban Area",
            own_contribution_rate_pct=own_pct,
            own_contribution_amount=round(own_amount, 2),
            subsidy_rate_pct=subsidy_pct,
            subsidy_amount=round(subsidy_amount, 2),
            bank_loan_amount=round(bank_loan, 2),
            term_loan_estimate=term_loan,
            working_capital_estimate=working_cap,
            annual_interest_rate_pct=interest_rate,
            emi_details=EMIPlan(
                tenure_years=req.tenure_years,
                monthly_emi=monthly_emi,
                total_interest=total_interest,
                total_payment=total_payment,
            ),
            subsidy_mechanism=subsidy_mechanism,
            collateral_requirement=collateral_req,
            recommended_nodal_portal=portal,
            checklist_for_bank_interview=checklist,
        )


dpr_calculator = DPRCalculatorService()
