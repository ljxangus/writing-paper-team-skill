#!/usr/bin/env python3
"""
claim_verify.py — Automated claim verification against experimental evidence.

Cross-verifies quantitative claims in paper text against experiment results.

Usage:
    python3 claim_verify.py --paper chapters/ --experiments experiments/ --output audit/claim-report.json
    python3 claim_verify.py --paper chapters/results.md --experiments experiments/results/ --check-all
"""

import argparse
import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class Claim:
    """A quantitative claim extracted from paper text."""
    text: str
    source_file: str
    line_number: int
    claim_type: str  # 'percentage', 'comparison', 'value'
    value: Optional[float]
    expected_value: Optional[float] = None
    status: str = 'pending'  # 'verified', 'mismatch', 'unverified'


@dataclass
class VerificationReport:
    """Summary of claim verification results."""
    total_claims: int
    verified: int
    mismatches: int
    unverified: int
    claims: List[Dict[str, Any]]


class ClaimExtractor:
    """Extract quantitative claims from markdown files."""

    # Pattern for percentages: "95.5%", "achieved 95%", etc.
    PERCENTAGE_PATTERN = re.compile(
        r'(?:achieved|reached|obtained|gained|scored)?\s*(\d+\.?\d*)\s*%',
        re.IGNORECASE
    )

    # Pattern for comparisons: "outperforms X by 15%", "15% better than"
    COMPARISON_PATTERN = re.compile(
        r'(?:outperforms|beats|exceeds|surpasses|improves|better|worse)(?:\s+\w+)?\s+(?:by\s+)?(\d+\.?\d*)\s*%',
        re.IGNORECASE
    )

    # Pattern for quantitative values: "accuracy of 0.95", "score: 87.3"
    VALUE_PATTERN = re.compile(
        r'(?:accuracy|precision|recall|f1|score|performance|value)?\s*(?:of|:)?\s*(\d+\.?\d*)',
        re.IGNORECASE
    )

    def __init__(self, paper_path: Path):
        self.paper_path = paper_path

    def extract_from_file(self, file_path: Path) -> List[Claim]:
        """Extract claims from a single markdown file."""
        claims = []
        content = file_path.read_text(encoding='utf-8')

        for line_num, line in enumerate(content.split('\n'), 1):
            # Skip code blocks and headers
            if line.strip().startswith('```') or line.strip().startswith('#'):
                continue

            # Extract percentages
            for match in self.PERCENTAGE_PATTERN.finditer(line):
                claims.append(Claim(
                    text=line.strip(),
                    source_file=str(file_path.relative_to(self.paper_path)),
                    line_number=line_num,
                    claim_type='percentage',
                    value=float(match.group(1))
                ))

            # Extract comparisons
            for match in self.COMPARISON_PATTERN.finditer(line):
                claims.append(Claim(
                    text=line.strip(),
                    source_file=str(file_path.relative_to(self.paper_path)),
                    line_number=line_num,
                    claim_type='comparison',
                    value=float(match.group(1))
                ))

            # Extract values (limit to lines with metrics context)
            if any(word in line.lower() for word in ['accuracy', 'precision', 'recall', 'f1', 'score', 'performance']):
                for match in self.VALUE_PATTERN.finditer(line):
                    value = float(match.group(1))
                    # Only include reasonable metric values (0-100 or 0-1)
                    if 0 <= value <= 100:
                        claims.append(Claim(
                            text=line.strip(),
                            source_file=str(file_path.relative_to(self.paper_path)),
                            line_number=line_num,
                            claim_type='value',
                            value=value
                        ))

        return claims

    def extract_all(self) -> List[Claim]:
        """Extract claims from all markdown files in the paper path."""
        claims = []
        if self.paper_path.is_file() and self.paper_path.suffix == '.md':
            claims.extend(self.extract_from_file(self.paper_path))
        elif self.paper_path.is_dir():
            for md_file in self.paper_path.rglob('*.md'):
                claims.extend(self.extract_from_file(md_file))
        return claims


class ExperimentDataLoader:
    """Load experimental data from JSON and CSV files."""

    def __init__(self, experiments_path: Path):
        self.experiments_path = experiments_path
        self.data: Dict[str, Any] = {}

    def load_json(self, file_path: Path) -> Dict[str, Any]:
        """Load data from a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load {file_path}: {e}", file=sys.stderr)
            return {}

    def load_csv(self, file_path: Path) -> List[Dict[str, str]]:
        """Load data from a CSV file (simple implementation)."""
        try:
            lines = file_path.read_text(encoding='utf-8').strip().split('\n')
            if not lines:
                return []

            headers = [h.strip() for h in lines[0].split(',')]
            data = []
            for line in lines[1:]:
                values = [v.strip() for v in line.split(',')]
                data.append(dict(zip(headers, values)))
            return data
        except IOError as e:
            print(f"Warning: Could not load {file_path}: {e}", file=sys.stderr)
            return []

    def load_all(self) -> None:
        """Load all experimental data."""
        if not self.experiments_path.exists():
            print(f"Warning: Experiments path {self.experiments_path} does not exist", file=sys.stderr)
            return

        if self.experiments_path.is_file():
            if self.experiments_path.suffix == '.json':
                self.data[self.experiments_path.stem] = self.load_json(self.experiments_path)
            elif self.experiments_path.suffix == '.csv':
                self.data[self.experiments_path.stem] = self.load_csv(self.experiments_path)
        elif self.experiments_path.is_dir():
            for json_file in self.experiments_path.rglob('*.json'):
                self.data[json_file.stem] = self.load_json(json_file)
            for csv_file in self.experiments_path.rglob('*.csv'):
                self.data[csv_file.stem] = self.load_csv(csv_file)

    def find_matching_value(self, claim: Claim) -> Optional[float]:
        """Find a matching experimental value for a claim."""
        # Search through all loaded data for numeric values
        for source, data in self.data.items():
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (int, float)):
                        # Check if the value matches (with tolerance for percentage conversion)
                        if abs(value - claim.value) < 0.01 or abs(value * 100 - claim.value) < 1:
                            return value
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        for key, value in item.items():
                            if isinstance(value, str):
                                # Try to extract numbers from string values
                                numbers = re.findall(r'(\d+\.?\d*)', value)
                                for num_str in numbers:
                                    num = float(num_str)
                                    if abs(num - claim.value) < 0.01 or abs(num * 100 - claim.value) < 1:
                                        return num
        return None


class ClaimVerifier:
    """Verify claims against experimental data."""

    def __init__(self, claims: List[Claim], experiment_loader: ExperimentDataLoader):
        self.claims = claims
        self.loader = experiment_loader

    def verify(self) -> List[Claim]:
        """Verify all claims against experimental data."""
        for claim in self.claims:
            matching_value = self.loader.find_matching_value(claim)

            if matching_value is not None:
                # Check if values match (allowing for percentage scale differences)
                if self._values_match(claim.value, matching_value):
                    claim.status = 'verified'
                    claim.expected_value = matching_value
                else:
                    claim.status = 'mismatch'
                    claim.expected_value = matching_value
            else:
                claim.status = 'unverified'

        return self.claims

    def _values_match(self, claimed: float, expected: float, tolerance: float = 0.01) -> bool:
        """Check if claimed value matches expected value."""
        # Handle percentage scale (e.g., 95 vs 0.95)
        if abs(claimed - expected) <= tolerance:
            return True
        if abs(claimed - expected * 100) <= tolerance * 100:
            return True
        if abs(claimed * 100 - expected) <= tolerance * 100:
            return True
        return False


def generate_report(claims: List[Claim]) -> VerificationReport:
    """Generate a summary report from verified claims."""
    verified = [c for c in claims if c.status == 'verified']
    mismatches = [c for c in claims if c.status == 'mismatch']
    unverified = [c for c in claims if c.status == 'unverified']

    return VerificationReport(
        total_claims=len(claims),
        verified=len(verified),
        mismatches=len(mismatches),
        unverified=len(unverified),
        claims=[{
            'text': c.text,
            'source': c.source_file,
            'line': c.line_number,
            'type': c.claim_type,
            'claimed_value': c.value,
            'expected_value': c.expected_value,
            'status': c.status
        } for c in claims]
    )


def main():
    parser = argparse.ArgumentParser(
        description='Verify quantitative claims in papers against experimental data.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --paper chapters/ --experiments experiments/ --output audit/claim-report.json
  %(prog)s --paper chapters/results.md --experiments results.json --check-all
        """
    )

    parser.add_argument(
        '--paper', '-p',
        type=Path,
        required=True,
        help='Path to paper markdown file or directory containing chapters'
    )

    parser.add_argument(
        '--experiments', '-e',
        type=Path,
        required=True,
        help='Path to experiment results (JSON/CSV file or directory)'
    )

    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=Path('audit/claim-report.json'),
        help='Output path for verification report (default: audit/claim-report.json)'
    )

    parser.add_argument(
        '--check-all',
        action='store_true',
        help='Report all claims including verified ones (default: only issues)'
    )

    args = parser.parse_args()

    # Extract claims from paper
    print(f"Extracting claims from {args.paper}...")
    extractor = ClaimExtractor(args.paper)
    claims = extractor.extract_all()

    if not claims:
        print("No quantitative claims found in paper.", file=sys.stderr)
        sys.exit(0)

    print(f"Found {len(claims)} quantitative claims.")

    # Load experimental data
    print(f"Loading experimental data from {args.experiments}...")
    loader = ExperimentDataLoader(args.experiments)
    loader.load_all()

    if not loader.data:
        print("Warning: No experimental data loaded. All claims will be unverified.", file=sys.stderr)

    # Verify claims
    print("Verifying claims...")
    verifier = ClaimVerifier(claims, loader)
    verified_claims = verifier.verify()

    # Generate and output report
    report = generate_report(verified_claims)

    # Create output directory if needed
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(asdict(report), f, indent=2)

    print(f"\nVerification complete. Report saved to {args.output}")
    print(f"Total claims: {report.total_claims}")
    print(f"Verified: {report.verified}")
    print(f"Mismatches: {report.mismatches}")
    print(f"Unverified: {report.unverified}")

    if report.mismatches > 0:
        print(f"\nWarning: {report.mismatches} claims do not match experimental data!", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
