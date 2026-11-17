#!/usr/bin/env python3
"""Export three self-contained review pages and a ZIP, without deploying anything.

Usage: python3 scripts/package-preview.py /path/to/review-output
Uses only the Python standard library. The preview includes no external assets.
"""
from pathlib import Path
import base64
import hashlib
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def sha(text):
    return base64.b64encode(hashlib.sha256(text.encode()).digest()).decode()

def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    output = Path(sys.argv[1]).resolve()
    preview = output / 'preview'
    preview.mkdir(parents=True, exist_ok=True)
    css = (ROOT / 'style.css').read_text()
    js = (ROOT / 'app.js').read_text()
    assets = [(ROOT/'assets/piik-logo.webp','image/webp'), (ROOT/'assets/favicon.svg','image/svg+xml')]
    assets += [(p,'image/webp') for p in sorted((ROOT/'assets/imagery').glob('*.webp'))]
    for name in ['index.html','privacy.html','credits.html']:
        page = (ROOT / name).read_text()
        page = page.replace('<link rel="stylesheet" href="style.css" />', '<style>'+css+'</style>')
        if '<script src="app.js" defer></script>' in page:
            page = page.replace('<script src="app.js" defer></script>', '')
            page = page.replace('</body>', '<script>'+js+'</script></body>')
        for source, mime in assets:
            data = base64.b64encode(source.read_bytes()).decode()
            page = page.replace(str(source.relative_to(ROOT)), 'data:'+mime+';base64,'+data)
        hashes = [sha(code) for code in re.findall(r'<script(?: [^>]*)?>(.*?)</script>',page,re.S)]
        policy = "default-src 'self'; script-src 'self' "+' '.join("'sha256-"+h+"'" for h in hashes)+"; style-src 'self' 'sha256-"+sha(css)+"'; img-src 'self' data:; object-src 'none'; base-uri 'none'; form-action 'none'; connect-src 'none'"
        page = re.sub(r'(<meta\s+http-equiv="Content-Security-Policy"\s+content=")[^"]*("\s*/>)',lambda m:m.group(1)+policy+m.group(2),page)
        page = page.replace('</head>','<meta name="robots" content="noindex, nofollow"></head>')
        (preview/name).write_text(page)
    (preview/'READ-ME.txt').write_text('''PIIK KENYA — PHOTOGRAPHIC VISUAL REVIEW

Extract this ZIP and keep all three HTML files together. Scripts, styles and
responsive images are embedded. Try opening index.html in a modern browser.
If file URLs are restricted, run the following command in the extracted folder:

  python3 -m http.server 3000

Open that local server in your browser. The preview was validated over local
HTTP; direct file URLs are blocked by the managed development browser policy.
No external image host, font, tracking script or AI service is contacted.

This is a review preview, not the live website. All six editorial scenes are
original photorealistic AI-generated illustrations, not actual listings,
network members, client stories or documentary city photographs. The credits
page and visible captions explain their provenance.

Enquiries and registration are unavailable: disabled status cards, no inputs,
no submissions and no registration claims.
Official-resource links remain withheld pending verification.
The source branch is piik-prelaunch-redesign. No merge or deployment occurred.
''')
    archive=output/'piik-visual-review-preview.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name in ['index.html','privacy.html','credits.html','READ-ME.txt']:
            z.write(preview/name,name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name in z.namelist():
            assert z.read(name)==(preview/name).read_bytes()
    print(f'PASS preview ZIP integrity: {archive}')

if __name__ == '__main__':
    main()
