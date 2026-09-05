"""
Automated batch crawler and discovery engine for Indian Government Welfare & Enterprise schemes.
Iterates through the SourceCatalog, discovers guidelines/circulars, extracts structured schemes,
and merges them into the schemes database without requiring manual URL entry.
"""

import argparse
import sys
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

from app.miner.source_catalog import catalog, GovernmentSource
from app.miner.scheme_miner import mine_url, save_mined_data
from app.schemas.scheme import Scheme


def crawl_source(source: GovernmentSource, follow_pdfs: bool = True) -> Optional[Tuple[Scheme, dict]]:
    """Crawl a single government source from the catalog."""
    urls_to_try = [source.portal_url] + source.guideline_urls
    # Deduplicate while preserving order
    seen = set()
    deduped_urls = []
    for u in urls_to_try:
        if u and u not in seen:
            seen.add(u)
            deduped_urls.append(u)

    last_err = None
    for url in deduped_urls:
        try:
            scheme, doc = mine_url(url, follow_pdfs=follow_pdfs)

            # Enrich scheme with catalog metadata if missing or generic
            if not scheme.ministry and source.ministry:
                scheme.ministry = source.ministry

            # Merge any target categories from catalog that might have been omitted
            for cat in source.target_categories:
                if cat not in scheme.eligible_categories:
                    scheme.eligible_categories.append(cat)
            scheme.sync_categories()

            # Ensure scheme code has a meaningful value
            if not scheme.scheme_code or scheme.scheme_code == "SCHEME-UNKNOWN":
                scheme.scheme_code = source.id.upper()

            # Add source description if extracted is too short
            if (not scheme.description or len(scheme.description) < 30) and source.description:
                scheme.description = source.description

            return scheme, doc
        except Exception as e:
            last_err = e
            continue

    print(f"Failed to crawl source {source.name} ({source.id}): {last_err}")
    return None


def crawl_sources(
    ministry: Optional[str] = None,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    source_ids: Optional[List[str]] = None,
    follow_pdfs: bool = True,
    output_file: str = "schemes.json",
) -> Dict[str, Any]:
    """
    Batch crawl government sources filtered by criteria.
    Returns crawl summary report.
    """
    if source_ids:
        sources_to_crawl = [catalog.get_source_by_id(sid) for sid in source_ids if catalog.get_source_by_id(sid)]
    else:
        sources_to_crawl = catalog.filter_sources(ministry=ministry, category=category, tag=tag)

    total = len(sources_to_crawl)
    successful_schemes: List[Scheme] = []
    successful_docs: List[dict] = []
    errors: List[Dict[str, str]] = []

    print(f"\n=======================================================")
    print(f"Starting Automated Crawler for {total} Government Sources")
    print(f"Filters: Ministry={ministry}, Category={category}, Tag={tag}")
    print(f"=======================================================\n")

    for idx, src in enumerate(sources_to_crawl, start=1):
        print(f"[{idx}/{total}] Crawling: {src.name} ({src.portal_url})")
        res = crawl_source(src, follow_pdfs=follow_pdfs)
        if res:
            scheme, doc = res
            successful_schemes.append(scheme)
            successful_docs.append(doc)
            print(f"    ✓ Successfully mined: {scheme.name} [{scheme.scheme_code}]")
        else:
            errors.append({"source_id": src.id, "name": src.name, "url": src.portal_url})

    if successful_schemes:
        save_mined_data(successful_schemes, successful_docs, filename=output_file)

    return {
        "total_attempted": total,
        "successful_count": len(successful_schemes),
        "failed_count": len(errors),
        "successful_schemes": [
            {
                "name": s.name,
                "scheme_code": s.scheme_code,
                "categories": s.eligible_categories,
                "max_project_cost": s.max_project_cost,
                "subsidy_percentage": s.subsidy_percentage,
            }
            for s in successful_schemes
        ],
        "failed_sources": errors,
    }


def main():
    parser = argparse.ArgumentParser(description="Automated Government Scheme Batch Crawler")
    parser.add_argument("--all", action="store_true", help="Crawl all registered government sources")
    parser.add_argument("--ministry", type=str, default=None, help="Filter by ministry name (e.g. MSME, MoSJE)")
    parser.add_argument("--category", type=str, default=None, help="Filter by category (e.g. SC, ST, Artisan, Women)")
    parser.add_argument("--tag", type=str, default=None, help="Filter by tag (e.g. credit, subsidy, greenfield)")
    parser.add_argument("--source", type=str, default=None, help="Crawl a specific source ID (e.g. pm-vishwakarma)")
    parser.add_argument("--output", type=str, default="schemes.json", help="Output schemes.json path")
    parser.add_argument("--no-pdfs", action="store_true", help="Do not follow attached guideline PDFs")

    args = parser.parse_args()

    source_ids = [args.source] if args.source else None
    res = crawl_sources(
        ministry=args.ministry,
        category=args.category,
        tag=args.tag,
        source_ids=source_ids,
        follow_pdfs=not args.no_pdfs,
        output_file=args.output,
    )

    print("\n--- Crawl Finished ---")
    print(f"Total: {res['total_attempted']} | Success: {res['successful_count']} | Failed: {res['failed_count']}")


if __name__ == "__main__":
    main()
