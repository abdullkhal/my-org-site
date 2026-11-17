#!/usr/bin/env python3
"""Export self-contained Phase 2 review pages and a ZIP, without deploying anything.

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
    for name in ['index.html','privacy.html','credits.html','terms.html']:
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
    for name in ['enquiries.html', 'official-links.html']:
        prototype = (ROOT/'review'/name).read_text().replace('<link rel="stylesheet" href="../style.css" />','<style>'+css+'</style>').replace('../index.html','index.html')
        prototype = prototype.replace('../assets/favicon.svg', 'data:image/svg+xml;base64,'+base64.b64encode((ROOT/'assets/favicon.svg').read_bytes()).decode())
        prototype = prototype.replace("style-src 'self'", "style-src 'self' 'sha256-"+sha(css)+"'")
        (preview/name).write_text(prototype)
    (preview/'READ-ME.txt').write_text("PIIK KENYA — PHASE 2 REVIEW\n\nExtract all files together. Open index.html or serve this folder with python3 -m http.server. All website assets are embedded. terms.html, privacy.html and credits.html are included. enquiries.html is a disabled prototype with synthetic examples. No real collection, tracking, deployment or paid service is enabled. official-links.html records nine founder-researched linked destinations; EBK and NEMA remain pending. Published registers are distinguished from live status checks. Source branch: phase-2-improvements.\n")
    archive=output/'piik-visual-review-preview.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name in ['index.html','privacy.html','credits.html','terms.html','enquiries.html','official-links.html','READ-ME.txt']:
            z.write(preview/name,name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name in z.namelist():
            assert z.read(name)==(preview/name).read_bytes()
    print(f'PASS preview ZIP integrity: {archive}')

if __name__ == '__main__':
    main()
