#!/usr/bin/env python3
"""Rebuild responsive WebP derivatives from the archived original imagegen PNGs.

Usage: python3 scripts/optimise-images.py /path/to/original-masters
Requires Pillow for this maintenance task only; the website has no dependencies.
"""
from pathlib import Path
import hashlib
import json
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'assets/imagery/manifest.json'

def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    masters = Path(sys.argv[1]).resolve()
    for item in json.loads(MANIFEST.read_text()):
        source = masters / item['master_file']
        if hashlib.sha256(source.read_bytes()).hexdigest() != item['master_sha256']:
            raise SystemExit(f"Master checksum mismatch: {source.name}")
        with Image.open(source) as original:
            original = original.convert('RGB')
            for width in item['widths']:
                height = round(width * original.height / original.width)
                image = original.resize((width, height), Image.Resampling.LANCZOS)
                target = ROOT / f"assets/imagery/{item['name']}-{width}.webp"
                image.save(target, format='WEBP', quality=79 if item['name'] == 'residence' else 77, method=6)
                print(f"{target.relative_to(ROOT)}: {target.stat().st_size:,} bytes")

if __name__ == '__main__':
    main()
