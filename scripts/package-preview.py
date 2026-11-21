#!/usr/bin/env python3
"""Export the current static publication and disabled review pages as a ZIP."""
import argparse
from pathlib import Path
import re
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]


def add_page(archive, page):
    html = page.read_text()
    if not re.search(r'<meta name="robots"[^>]*noindex', html):
        html = html.replace("</head>", '<meta name="robots" content="noindex,nofollow">\n</head>')
    archive.writestr(page.relative_to(ROOT).as_posix(), html)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    archive_path = args.output / "piik-publication-preview.zip"
    with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as archive:
        for html in sorted([*ROOT.glob("*.html"), *(ROOT / "review").glob("*.html")]):
            add_page(archive, html)
        assets = [ROOT / "assets" / name for name in ("piik-logo.webp", "favicon.svg")]
        assets += sorted((ROOT / "assets/imagery").glob("*.webp"))
        for path in [*(ROOT / name for name in ("style.css", "editorial.css", "app.js", "editorial.js")), *assets]:
            archive.write(path, path.relative_to(ROOT).as_posix())
        archive.writestr("READ-ME.txt", "Extract all files into one folder. Run python3 -m http.server in that folder and open the local address. This is a review copy of PIIK Kenya.\n")
        archive.writestr("robots.txt", "User-agent: *\nDisallow: /\n")
    with ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise SystemExit("Failed preview archive integrity check.")
    print(f"PASS preview ZIP integrity: {archive_path}")


if __name__ == "__main__":
    main()
