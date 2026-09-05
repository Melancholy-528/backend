from app.schemas.applicant import Applicant
from app.schemas.scheme import Scheme


def check_eligibility(applicant: Applicant, scheme: Scheme) -> dict:
    reasons = []
    match_score = 0

    # Category and target group matching
    norm_scheme_cats = [c.strip().upper() for c in scheme.eligible_categories] if scheme.eligible_categories else []
    if scheme.eligible_category and not norm_scheme_cats:
        norm_scheme_cats = [c.strip().upper() for c in scheme.eligible_category.split(",") if c.strip()]

    if norm_scheme_cats:
        norm_applicant_cat = applicant.category.strip().upper()
        norm_applicant_occ = (applicant.occupation or "").strip().upper()

        is_category_eligible = (
            "ALL" in norm_scheme_cats
            or "GENERAL" in norm_scheme_cats
            or norm_applicant_cat in norm_scheme_cats
            or (applicant.gender and applicant.gender.strip().upper() == "FEMALE" and "WOMEN" in norm_scheme_cats)
            or (bool(norm_applicant_occ) and any(norm_applicant_occ in cat or cat in norm_applicant_occ for cat in norm_scheme_cats))
        )

        if not is_category_eligible:
            reasons.append(
                f"Applicant category '{applicant.category}' is not eligible. Required target group: {', '.join(scheme.eligible_categories or [scheme.eligible_category])}"
            )
        else:
            if norm_applicant_cat in norm_scheme_cats or (norm_applicant_occ and any(norm_applicant_occ in c for c in norm_scheme_cats)):
                match_score += 40
            else:
                match_score += 25
    else:
        match_score += 30

    # Income limit check
    if scheme.income_limit is not None and scheme.income_limit > 0:
        if applicant.annual_income > scheme.income_limit:
            reasons.append(
                f"Annual income (₹{applicant.annual_income:,}) exceeds the scheme ceiling (₹{scheme.income_limit:,})"
            )
        else:
            ratio = applicant.annual_income / scheme.income_limit
            match_score += int(30 * (1 - ratio * 0.5))
    else:
        match_score += 20

    # Project cost check
    if scheme.max_project_cost is not None and scheme.max_project_cost > 0:
        if applicant.project_cost > scheme.max_project_cost:
            reasons.append(
                f"Project cost (₹{applicant.project_cost:,}) exceeds maximum permissible limit (₹{scheme.max_project_cost:,})"
            )
        else:
            match_score += 25
    else:
        match_score += 15

    # Age checks
    if applicant.age is not None:
        if scheme.min_age is not None and applicant.age < scheme.min_age:
            reasons.append(f"Applicant age ({applicant.age}) is below minimum limit ({scheme.min_age})")
        elif scheme.max_age is not None and applicant.age > scheme.max_age:
            reasons.append(f"Applicant age ({applicant.age}) exceeds maximum limit ({scheme.max_age})")
        else:
            match_score += 15
    else:
        match_score += 10

    is_eligible = (len(reasons) == 0)
    final_score = min(match_score, 100) if is_eligible else 0

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