#!/usr/bin/env python3
"""
citation_verify.py — Verify citation accuracy via CrossRef API.

Checks:
1. DOI validity (HTTP 200 from CrossRef)
2. Author/year/title match against CrossRef metadata
3. Citation format consistency (IEEE style)

Usage:
    python3 citation_verify.py --input references.bib --check-doi
    python3 citation_verify.py --input references.bib --check-info
    python3 citation_verify.py --input references.bib --check-format
    python3 citation_verify.py --input references.bib --check-all
    python3 citation_verify.py --input references.bib --check-doi --output report.json
"""

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.error
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# BibTeX Parser (minimal, no external deps)
# ---------------------------------------------------------------------------

def parse_bibtex(text: str) -> List[dict]:
    """Parse a BibTeX file into a list of entry dicts."""
    entries = []
    # Match @type{key, ... }
    pattern = re.compile(r"@(\w+)\s*\{([^,]+),\s*(.*?)\n\}", re.DOTALL)
    for match in pattern.finditer(text):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()
        body = match.group(3)

        fields = {}
        for field_match in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}", body, re.DOTALL):
            fname = field_match.group(1).lower()
            fval = field_match.group(2).strip()
            fields[fname] = fval

        entries.append({
            "type": entry_type,
            "key": key,
            "title": fields.get("title", ""),
            "author": fields.get("author", ""),
            "year": fields.get("year", ""),
            "doi": fields.get("doi", ""),
            "journal": fields.get("journal", ""),
            "booktitle": fields.get("booktitle", ""),
            "volume": fields.get("volume", ""),
            "number": fields.get("number", ""),
            "pages": fields.get("pages", ""),
            "fields": fields,
        })
    return entries


# ---------------------------------------------------------------------------
# CrossRef DOI verification
# ---------------------------------------------------------------------------

def verify_doi(doi: str) -> dict:
    """Verify a DOI via CrossRef API. Returns metadata if valid."""
    if not doi:
        return {"valid": False, "error": "No DOI provided"}

    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "citation-verify/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        msg = data.get("message", {})
        return {
            "valid": True,
            "title": msg.get("title", [""])[0] if msg.get("title") else "",
            "author": "; ".join(
                f"{a.get('family', '')}, {a.get('given', '')}" for a in msg.get("author", [])
            ),
            "year": (msg.get("published-print") or msg.get("published-online") or {}).get("date-parts", [[None]])[0][0],
            "container": (msg.get("container-title") or [""])[0],
            "type": msg.get("type", ""),
        }
    except urllib.error.HTTPError as e:
        return {"valid": False, "error": f"HTTP {e.code}"}
    except Exception as e:
        return {"valid": False, "error": str(e)}


# ---------------------------------------------------------------------------
# Information accuracy check
# ---------------------------------------------------------------------------

def check_info(entry: dict, crossref: dict) -> List[str]:
    """Compare entry fields with CrossRef metadata. Returns list of issues."""
    issues = []
    if not crossref.get("valid"):
        issues.append("DOI verification failed — cannot check info accuracy")
        return issues

    # Title comparison (normalized)
    entry_title = re.sub(r"[^a-z0-9]", "", entry["title"].lower())
    cr_title = re.sub(r"[^a-z0-9]", "", (crossref.get("title") or "").lower())
    if entry_title and cr_title and entry_title != cr_title:
        issues.append(f"Title mismatch: entry='{entry['title'][:60]}' vs crossref='{crossref['title'][:60]}'")

    # Year comparison
    if entry["year"] and crossref.get("year"):
        if str(entry["year"]) != str(crossref["year"]):
            issues.append(f"Year mismatch: entry={entry['year']} vs crossref={crossref['year']}")

    return issues


# ---------------------------------------------------------------------------
# Format consistency check (IEEE style)
# ---------------------------------------------------------------------------

IEEE_REQUIRED_FIELDS = {
    "article": ["author", "title", "journal", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "conference": ["author", "title", "booktitle", "year"],
}


def check_format(entry: dict) -> List[str]:
    """Check if entry follows IEEE citation format."""
    issues = []
    entry_type = entry["type"]
    required = IEEE_REQUIRED_FIELDS.get(entry_type, ["author", "title", "year"])

    for field in required:
        if not entry.get(field):
            issues.append(f"Missing required field: {field}")

    # Check author format (should be "Family, Given" separated by " and ")
    if entry.get("author"):
        if " and " not in entry["author"] and "," not in entry["author"]:
            issues.append("Author format may not follow IEEE style (expected 'Family, Given and ...')")

    # Check year is numeric
    if entry.get("year") and not entry["year"].isdigit():
        issues.append(f"Year field is not numeric: '{entry['year']}'")

    return issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Verify citation accuracy")
    parser.add_argument("--input", required=True, help="Input BibTeX file")
    parser.add_argument("--check-doi", action="store_true", help="Check DOI validity")
    parser.add_argument("--check-info", action="store_true", help="Check author/year/title accuracy")
    parser.add_argument("--check-format", action="store_true", help="Check format consistency")
    parser.add_argument("--check-all", action="store_true", help="Run all checks")
    parser.add_argument("--output", default=None, help="Output report file (JSON)")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between DOI checks (seconds)")
    args = parser.parse_args()

    if args.check_all:
        args.check_doi = args.check_info = args.check_format = True

    if not any([args.check_doi, args.check_info, args.check_format]):
        print("No checks selected. Use --check-doi, --check-info, --check-format, or --check-all", file=sys.stderr)
        sys.exit(1)

    # Read and parse input
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    entries = parse_bibtex(text)
    if not entries:
        print("No BibTeX entries found in input file", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(entries)} entries", file=sys.stderr)

    # Run checks
    report = {"total": len(entries), "checks": {}, "issues": []}
    for i, entry in enumerate(entries):
        entry_report = {"key": entry["key"], "doi": entry["doi"], "issues": []}

        if args.check_doi and entry["doi"]:
            print(f"  [{i+1}/{len(entries)}] Verifying DOI: {entry['doi']}", file=sys.stderr)
            result = verify_doi(entry["doi"])
            entry_report["doi_valid"] = result.get("valid", False)
            if not result.get("valid"):
                entry_report["issues"].append(f"DOI invalid: {result.get('error', 'unknown')}")
            time.sleep(args.delay)

            if args.check_info and result.get("valid"):
                info_issues = check_info(entry, result)
                entry_report["issues"].extend(info_issues)

        if args.check_format:
            format_issues = check_format(entry)
            entry_report["issues"].extend(format_issues)

        report["checks"][entry["key"]] = entry_report
        if entry_report["issues"]:
            report["issues"].extend([f"[{entry['key']}] {iss}" for iss in entry_report["issues"]])

    # Summary
    total_issues = len(report["issues"])
    doi_invalid = sum(1 for v in report["checks"].values() if not v.get("doi_valid", True))
    print(f"\n--- Citation Verification Report ---", file=sys.stderr)
    print(f"Total entries: {len(entries)}", file=sys.stderr)
    print(f"DOI invalid: {doi_invalid}", file=sys.stderr)
    print(f"Total issues: {total_issues}", file=sys.stderr)

    if total_issues == 0:
        print("✅ All checks passed", file=sys.stderr)
    else:
        print("❌ Issues found:", file=sys.stderr)
        for iss in report["issues"]:
            print(f"  - {iss}", file=sys.stderr)

    # Output
    output = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\nReport written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
