"""
Eligibility evaluation and personalized multi-criteria matching engine for government welfare and enterprise schemes.
Accurately differentiates matching scores and eligibility according to social category, gender, occupation,
income ceiling, and project cost limits.
"""

from typing import Dict, Any, List
from app.schemas.applicant import Applicant
from app.schemas.scheme import Scheme


def check_eligibility(applicant: Applicant, scheme: Scheme) -> dict:
    reasons = []

    # 1. Normalize categories and inputs
    norm_scheme_cats = [c.strip().upper() for c in scheme.eligible_categories] if scheme.eligible_categories else []
    if scheme.eligible_category and not norm_scheme_cats:
        norm_scheme_cats = [c.strip().upper() for c in scheme.eligible_category.split(",") if c.strip()]

    applicant_cat = (applicant.category or "General").strip().upper()
    applicant_gender = (applicant.gender or "").strip().upper()
    is_female = applicant_gender in ["FEMALE", "WOMAN", "WOMEN"]
    applicant_occ = (applicant.occupation or "").strip().upper()

    scheme_name_upper = (scheme.name or "").upper()
    scheme_code_upper = (scheme.scheme_code or "").upper()

    # 2. Strict Women-Exclusive Exclusion
    # Schemes like Mahila Samriddhi, New Swarnima, Adivasi Mahila are 100% reserved for women
    is_women_exclusive = (
        ("MAHILA" in scheme_name_upper or "SWARNIMA" in scheme_name_upper or scheme_code_upper in ["NSFDC-MSY", "NBCFDC-NEW-SWARNIMA", "NSTFDC-AMSY"])
        and not any(k in scheme_code_upper for k in ["PMEGP", "MUDRA", "CGTMSE", "VISHWAKARMA"])
    )
    if is_women_exclusive and not is_female:
        reasons.append(f"Scheme '{scheme.name}' is strictly reserved for Women entrepreneurs/beneficiaries.")

    # 3. Special Stand-Up India Mandate
    # Stand-Up India is ONLY for SC, ST, or Women (of any category). General category males are legally excluded.
    if "STANDUP" in scheme_code_upper:
        is_standup_eligible = (applicant_cat in ["SC", "ST"]) or is_female
        if not is_standup_eligible:
            reasons.append(
                "Stand-Up India is strictly reserved for SC/ST individuals or Women entrepreneurs. General category males are not eligible."
            )

    # 4. Strict Occupation Exclusions
    if "SVANIDHI" in scheme_code_upper:
        if applicant_occ and not any(k in applicant_occ for k in ["VENDOR", "HAWKER", "THELA", "STREET"]):
            reasons.append("PM SVANidhi is strictly reserved for urban Street Vendors and hawkers.")

    if "VISHWAKARMA" in scheme_code_upper:
        if applicant_occ and not any(k in applicant_occ for k in ["ARTISAN", "CRAFT", "TAILOR", "CARPENTER", "BLACKSMITH", "POTTER", "WEAVER"]):
            reasons.append("PM Vishwakarma is strictly reserved for traditional Artisans and Craftspersons.")

    # 5. General Category & Target Group Eligibility Check
    if norm_scheme_cats:
        cat_matches = applicant_cat in norm_scheme_cats
        gender_matches = is_female and "WOMEN" in norm_scheme_cats
        occ_matches = bool(applicant_occ) and any(applicant_occ in cat or cat in applicant_occ for cat in norm_scheme_cats)
        open_to_all = "ALL" in norm_scheme_cats or "GENERAL" in norm_scheme_cats

        if not (cat_matches or gender_matches or occ_matches or open_to_all):
            reasons.append(
                f"Applicant category '{applicant.category}' is not eligible. Required target group: {', '.join(scheme.eligible_categories or [scheme.eligible_category or 'Special Category'])}"
            )

    # 6. Income Ceiling Check
    if scheme.income_limit is not None and scheme.income_limit > 0:
        if applicant.annual_income > scheme.income_limit:
            reasons.append(
                f"Annual household income (₹{applicant.annual_income:,}) exceeds the scheme ceiling of ₹{scheme.income_limit:,}"
            )

    # 7. Project Cost Ceiling Check
    if scheme.max_project_cost is not None and scheme.max_project_cost > 0:
        if applicant.project_cost > scheme.max_project_cost:
            reasons.append(
                f"Required project cost (₹{applicant.project_cost:,}) exceeds the maximum scheme limit of ₹{scheme.max_project_cost:,}"
            )

    # 8. Age Limits Check
    if applicant.age is not None:
        if scheme.min_age is not None and applicant.age < scheme.min_age:
            reasons.append(f"Applicant age ({applicant.age}) is below minimum requirement ({scheme.min_age} years)")
        elif scheme.max_age is not None and applicant.age > scheme.max_age:
            reasons.append(f"Applicant age ({applicant.age}) exceeds maximum permissible limit ({scheme.max_age} years)")

    is_eligible = (len(reasons) == 0)

    # =========================================================================
    # MULTI-TIER DIFFERENTIATED SCORING ENGINE (Max 100 points)
    # =========================================================================
    if not is_eligible:
        final_score = 0
    else:
        score = 0

        # A. Community Target & Exclusivity Weight (Max 40 pts)
        # Schemes 100% dedicated to applicant's community receive maximum priority
        is_exclusive_community = (
            (applicant_cat == "SC" and "SC" in norm_scheme_cats and not any(k in norm_scheme_cats for k in ["GENERAL", "OBC"]))
            or (applicant_cat == "OBC" and "OBC" in norm_scheme_cats and not any(k in norm_scheme_cats for k in ["GENERAL", "SC"]))
            or (applicant_cat == "ST" and "ST" in norm_scheme_cats and not any(k in norm_scheme_cats for k in ["GENERAL", "OBC"]))
            or (applicant_cat == "MINORITY" and "MINORITY" in norm_scheme_cats and not any(k in norm_scheme_cats for k in ["GENERAL", "SC"]))
        )
        if is_exclusive_community:
            score += 40
        elif applicant_cat in norm_scheme_cats and applicant_cat != "GENERAL":
            score += 34
        elif is_female and "WOMEN" in norm_scheme_cats and applicant_cat == "GENERAL":
            score += 32
        elif "GENERAL" in norm_scheme_cats or "ALL" in norm_scheme_cats:
            score += 24
        else:
            score += 20

        # B. Gender Alignment & Women Empowerment Weight (Max 20 pts)
        if is_female:
            if is_women_exclusive:
                score += 20  # 100% dedicated women scheme
            elif "STANDUP" in scheme_code_upper or "PMEGP" in scheme_code_upper or "WOMEN" in norm_scheme_cats:
                score += 18  # Substantial women quota or 35% subsidy benefit
            else:
                score += 12
        else:
            score += 10

        # C. Financial Subsidy & Concession Value (Max 20 pts)
        if scheme.subsidy_percentage:
            if scheme.subsidy_percentage >= 25.0:
                score += 20
            elif scheme.subsidy_percentage >= 15.0:
                score += 16
            else:
                score += 12
        elif "VISHWAKARMA" in scheme_code_upper:
            score += 18
        elif scheme.income_limit:
            score += 14
        else:
            score += 8

        # D. Project Cost Fit & Proportionality (Max 10 pts)
        if scheme.max_project_cost and scheme.max_project_cost > 0:
            ratio = applicant.project_cost / scheme.max_project_cost
            if 0.15 <= ratio <= 1.0:
                score += 10
            else:
                score += 6
        else:
            score += 7

        # E. Means-Testing & Vulnerability Match (Max 10 pts)
        if scheme.income_limit and scheme.income_limit > 0:
            if applicant.annual_income <= scheme.income_limit:
                score += 10
            else:
                score += 4
        else:
            score += 7

        final_score = min(max(score, 10), 100)

    return {
        "eligible": is_eligible,
        "score": final_score,
        "reasons": reasons if not is_eligible else ["All eligibility criteria fulfilled"],
        "scheme": scheme.name,
        "scheme_code": scheme.scheme_code,
        "ministry": scheme.ministry,
        "description": scheme.description,
        "benefits": scheme.benefits,
        "subsidy_percentage": scheme.subsidy_percentage,
        "max_project_cost": scheme.max_project_cost,
        "source_url": scheme.source_url,
    }