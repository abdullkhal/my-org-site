#!/usr/bin/env python3
"""Check public pages for broken internal routes, anchors and sitemap entries."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = set()
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                raise ValueError(f'Duplicate HTML id: {attrs["id"]}')
            self.ids.add(attrs["id"])
        attribute = "href" if tag in {"a", "link"} else "src" if tag in {"script", "img"} else None
        if attribute and attrs.get(attribute):
            self.links.add(attrs[attribute])

    handle_startendtag = handle_starttag


pages = {}
for path in sorted(ROOT.glob("*.html")):
    try:
        pages[path] = Page(path)
    except ValueError as error:
        raise SystemExit(f"{path.name}: {error}")

problems = []
for path, page in pages.items():
    for link in sorted(page.links):
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if not target.is_relative_to(ROOT) or not target.exists():
            problems.append(f"{path.name}: missing link target {link}")
        elif target in pages and url.fragment and unquote(url.fragment) not in pages[target].ids:
            problems.append(f"{path.name}: missing anchor {link}")

sitemap = ET.parse(ROOT / "sitemap.xml")
urls = [node.text for node in sitemap.findall(".//{*}loc")]
expected = {
    "https://piikkenya.com/" + ("" if path.name == "index.html" else path.name)
    for path in pages if path.name != "search.html"
}
if len(urls) != len(set(urls)) or set(urls) != expected:
    problems.append("Sitemap does not match the public indexable pages.")

if problems:
    raise SystemExit("\n".join(problems))
print(f"Checked internal links, anchors and sitemap entries across {len(pages)} pages.")
