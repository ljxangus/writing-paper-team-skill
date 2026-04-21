#!/usr/bin/env python3
"""
scholar_search.py — Multi-database academic literature search script.

Supports: CrossRef, Semantic Scholar, arXiv
Output formats: json, bibtex, apa

Usage:
    python3 scholar_search.py "deep learning transformer"
    python3 scholar_search.py "neural network" --sources crossref,semanticscholar --year 2023-2026
    python3 scholar_search.py "network traffic classification" --format bibtex -o refs.bib
    python3 scholar_search.py "attention mechanism" --format apa --limit 5
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _fetch_json(url: str, headers: Optional[Dict] = None, timeout: int = 30) -> dict:
    """Fetch JSON from a URL with basic error handling."""
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} for {url}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        return {}


def _sanitize(text: str) -> str:
    """Remove newlines and excessive whitespace."""
    return " ".join(text.split())


# ---------------------------------------------------------------------------
# CrossRef
# ---------------------------------------------------------------------------

def search_crossref(query: str, year_from: Optional[int] = None,
                    year_to: Optional[int] = None, limit: int = 20) -> List[dict]:
    """Search CrossRef via its public API."""
    base = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": min(limit, 100),
        "sort": "relevance",
        "select": "DOI,title,author,published-print,published-online,container-title,type,score",
    }
    if year_from or year_to:
        yf = year_from or 1900
        yt = year_to or datetime.now().year
        params["filter"] = f"from-pub-date:{yf},until-pub-date:{yt}"

    url = f"{base}?{urllib.parse.urlencode(params)}"
    data = _fetch_json(url)

    results = []
    items = data.get("message", {}).get("items", [])
    for item in items:
        title_list = item.get("title", [])
        title = _sanitize(title_list[0]) if title_list else "N/A"
        authors = []
        for a in item.get("author", []):
            family = a.get("family", "")
            given = a.get("given", "")
            authors.append(f"{family}, {given}" if given else family)
        date_info = item.get("published-print") or item.get("published-online") or {}
        parts = date_info.get("date-parts", [[]])
        year = parts[0][0] if parts and parts[0] else None
        venue_list = item.get("container-title", [])
        venue = _sanitize(venue_list[0]) if venue_list else "N/A"

        results.append({
            "source": "crossref",
            "doi": item.get("DOI", ""),
            "title": title,
            "authors": "; ".join(authors),
            "year": year,
            "venue": venue,
            "type": item.get("type", ""),
            "score": item.get("score", 0),
        })
    return results


# ---------------------------------------------------------------------------
# Semantic Scholar
# ---------------------------------------------------------------------------

def search_semanticscholar(query: str, year_from: Optional[int] = None,
                           year_to: Optional[int] = None, limit: int = 20) -> List[dict]:
    """Search Semantic Scholar via its public API."""
    base = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": "externalIds,title,authors,year,venue,citationCount,abstract",
    }
    if year_from:
        params["year"] = f"{year_from}-{year_to or datetime.now().year}"

    url = f"{base}?{urllib.parse.urlencode(params)}"
    data = _fetch_json(url)

    results = []
    for item in data.get("data", []):
        ext = item.get("externalIds", {})
        doi = ext.get("DOI", "")
        authors = [a.get("name", "") for a in item.get("authors", [])]
        results.append({
            "source": "semanticscholar",
            "doi": doi,
            "title": _sanitize(item.get("title", "")),
            "authors": "; ".join(authors),
            "year": item.get("year"),
            "venue": _sanitize(item.get("venue", "")) or "N/A",
            "citation_count": item.get("citationCount", 0),
            "abstract": _sanitize(item.get("abstract", ""))[:500] if item.get("abstract") else "",
        })
    return results


# ---------------------------------------------------------------------------
# arXiv
# ---------------------------------------------------------------------------

def search_arxiv(query: str, year_from: Optional[int] = None,
                 year_to: Optional[int] = None, limit: int = 20) -> List[dict]:
    """Search arXiv via its public API (returns RSS-like XML)."""
    base = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": min(limit, 50),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = f"{base}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as resp:
            xml_data = resp.read().decode("utf-8")
    except Exception as e:
        print(f"arXiv request failed: {e}", file=sys.stderr)
        return []

    # Minimal XML parsing (no external dependency)
    import xml.etree.ElementTree as ET
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_data)

    results = []
    for entry in root.findall("atom:entry", ns):
        title = _sanitize(entry.find("atom:title", ns).text or "")
        summary = _sanitize(entry.find("atom:summary", ns).text or "")[:500]
        authors = [a.find("atom:name", ns).text or "" for a in entry.findall("atom:author", ns)]
        doi_elem = entry.find("atom:doi", ns)
        doi = doi_elem.text if doi_elem is not None else ""
        published = entry.find("atom:published", ns).text or ""
        year = int(published[:4]) if published else None

        if year_from and year and year < year_from:
            continue
        if year_to and year and year > year_to:
            continue

        results.append({
            "source": "arxiv",
            "doi": doi,
            "title": title,
            "authors": "; ".join(authors),
            "year": year,
            "venue": "arXiv",
            "abstract": summary,
        })
    return results


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_bibtex(results: List[dict]) -> str:
    """Format results as BibTeX entries."""
    entries = []
    for i, r in enumerate(results):
        key = f"ref{i+1}"
        first_author = r.get("authors", "").split(";")[0].split(",")[0].strip().replace(" ", "")
        year = r.get("year", "n.d.")
        key = f"{first_author}{year}" if first_author else key
        lines = [
            f"@article{{{key},",
            f"  title = {{{r.get('title', '')}}},",
            f"  author = {{{r.get('authors', '')}}},",
            f"  year = {{{r.get('year', '')}}},",
        ]
        if r.get("doi"):
            lines.append(f"  doi = {{{r['doi']}}},")
        if r.get("venue") and r["venue"] != "N/A":
            lines.append(f"  journal = {{{r['venue']}}},")
        lines.append("}")
        entries.append("\n".join(lines))
    return "\n\n".join(entries)


def format_apa(results: List[dict]) -> str:
    """Format results as APA citations (simplified)."""
    lines = []
    for r in results:
        authors = r.get("authors", "Unknown")
        year = r.get("year", "n.d.")
        title = r.get("title", "")
        venue = r.get("venue", "")
        doi = r.get("doi", "")
        parts = [f"{authors} ({year}). {title}."]
        if venue and venue != "N/A":
            parts.append(f" {venue}.")
        if doi:
            parts.append(f" https://doi.org/{doi}")
        lines.append("".join(parts))
    return "\n\n".join(lines)


def format_json(results: List[dict]) -> str:
    """Format results as JSON."""
    return json.dumps(results, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

SEARCH_FUNCS = {
    "crossref": search_crossref,
    "semanticscholar": search_semanticscholar,
    "arxiv": search_arxiv,
}

FORMAT_FUNCS = {
    "json": format_json,
    "bibtex": format_bibtex,
    "apa": format_apa,
}


def main():
    parser = argparse.ArgumentParser(description="Multi-database academic literature search")
    parser.add_argument("query", help="Search query string")
    parser.add_argument("--sources", default="crossref,semanticscholar",
                        help="Comma-separated list of databases (default: crossref,semanticscholar)")
    parser.add_argument("--year", default=None,
                        help="Year range, e.g. 2023-2026")
    parser.add_argument("--limit", type=int, default=20,
                        help="Maximum results per source (default: 20)")
    parser.add_argument("--format", default="json", choices=list(FORMAT_FUNCS.keys()),
                        help="Output format (default: json)")
    parser.add_argument("-o", "--output", default=None,
                        help="Output file path (default: stdout)")
    args = parser.parse_args()

    # Parse year range
    year_from, year_to = None, None
    if args.year:
        parts = args.year.split("-")
        year_from = int(parts[0])
        year_to = int(parts[1]) if len(parts) > 1 else None

    # Execute searches
    sources = [s.strip() for s in args.sources.split(",")]
    all_results = []
    for source in sources:
        func = SEARCH_FUNCS.get(source)
        if not func:
            print(f"Unknown source: {source}. Available: {list(SEARCH_FUNCS.keys())}", file=sys.stderr)
            continue
        print(f"Searching {source}...", file=sys.stderr)
        try:
            results = func(args.query, year_from=year_from, year_to=year_to, limit=args.limit)
            all_results.extend(results)
            print(f"  Found {len(results)} results", file=sys.stderr)
        except Exception as e:
            print(f"  Error: {e}", file=sys.stderr)
        time.sleep(0.5)  # Rate limiting

    # Format output
    formatter = FORMAT_FUNCS.get(args.format, format_json)
    output = formatter(all_results)

    # Write output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\nResults written to {args.output} ({len(all_results)} papers)", file=sys.stderr)
    else:
        print(output)

    # Summary
    print(f"\nTotal: {len(all_results)} papers from {len(sources)} source(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
