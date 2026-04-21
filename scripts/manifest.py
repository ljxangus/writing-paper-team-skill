#!/usr/bin/env python3
"""
manifest.py — Generate reproducibility manifest with checksums.

Creates a manifest of all experiment files, code, data, and configuration
with SHA256 checksums for reproducibility verification.

Usage:
    python3 scripts/manifest.py --dir experiments/ --output experiments/MANIFEST.json
    python3 scripts/manifest.py --dir experiments/ --verify experiments/MANIFEST.json
"""

import argparse
import hashlib
import json
import os
import platform
import sys
from datetime import datetime
from pathlib import Path


def compute_sha256(filepath: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def generate_manifest(root_dir: Path) -> dict:
    """Generate manifest for all files in directory tree."""
    files = []

    for filepath in root_dir.rglob('*'):
        if filepath.is_file():
            try:
                rel_path = str(filepath.relative_to(root_dir))
                file_stat = filepath.stat()
                files.append({
                    'path': rel_path,
                    'size': file_stat.st_size,
                    'sha256': compute_sha256(filepath),
                    'mtime': file_stat.st_mtime
                })
            except (OSError, PermissionError) as e:
                print(f"Warning: Skipping {filepath}: {e}", file=sys.stderr)

    return {
        'manifest_version': '1.0',
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'generator': {
            'python_version': sys.version,
            'platform': platform.platform(),
            'system': platform.system()
        },
        'root_directory': str(root_dir),
        'file_count': len(files),
        'files': files
    }


def verify_manifest(manifest_path: Path, root_dir: Path) -> bool:
    """Verify existing manifest against current files."""
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    all_valid = True
    for entry in manifest.get('files', []):
        filepath = root_dir / entry['path']
        if not filepath.exists():
            print(f"MISSING: {entry['path']}")
            all_valid = False
        else:
            current_hash = compute_sha256(filepath)
            if current_hash != entry['sha256']:
                print(f"MODIFIED: {entry['path']}")
                print(f"  Expected: {entry['sha256']}")
                print(f"  Current:  {current_hash}")
                all_valid = False

    if all_valid:
        print(f"All {manifest['file_count']} files verified.")

    return all_valid


def main():
    parser = argparse.ArgumentParser(
        description='Generate reproducibility manifest with checksums'
    )
    parser.add_argument(
        '--dir',
        type=Path,
        required=True,
        help='Directory to scan'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output manifest file (JSON)'
    )
    parser.add_argument(
        '--verify',
        type=Path,
        help='Verify against existing manifest'
    )

    args = parser.parse_args()

    if args.verify:
        success = verify_manifest(args.verify, args.dir)
        sys.exit(0 if success else 1)

    manifest = generate_manifest(args.dir)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(manifest, f, indent=2)
        print(f"Manifest written to {args.output}")
    else:
        print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
