#!/usr/bin/env python3
"""Report changes and HTTP health without modifying published content."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import build_opener, HTTPRedirectHandler, Request
from urllib.robotparser import RobotFileParser

ROOT = Path(__file__).resolve().parents[1]
AGENT = "PIIKKenyaSourceMonitor/1.0 (+https://piikkenya.com/about.html)"
LIMIT = 2_000_000


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, new_url):
        return None


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ignored = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self.ignored += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"} and self.ignored:
            self.ignored -= 1

    def handle_data(self, data):
        if not self.ignored and data.strip():
            self.parts.append(data.strip())


def public_url(url):
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password
            or parsed.port not in {None, 443}):
        raise ValueError(f"Expected a public HTTPS URL: {url}")
    return parsed


def request(url, method="GET"):
    public_url(url)
    return build_opener(NoRedirect()).open(Request(url, method=method, headers={"User-Agent": AGENT}), timeout=12)


def snapshot(url):
    parsed = public_url(url)
    robots = RobotFileParser()
    with request(f"https://{parsed.netloc}/robots.txt") as response:
        robots.parse(response.read(256_000).decode("utf-8", "replace").splitlines())
    if not robots.can_fetch(AGENT, url):
        raise ValueError("robots.txt disallows monitoring")
    with request(url) as response:
        media_type = response.headers.get_content_type()
        if media_type not in {"text/html", "application/xhtml+xml", "text/plain", "application/rss+xml", "application/atom+xml"}:
            raise ValueError(f"Unsupported source type: {media_type}")
        payload = response.read(LIMIT + 1)
        if len(payload) > LIMIT:
            raise ValueError("Source exceeds monitor size limit")
        text = payload.decode(response.headers.get_content_charset() or "utf-8", "replace")
    if media_type in {"text/html", "application/xhtml+xml"}:
        parser = VisibleText()
        parser.feed(text)
        text = " ".join(parser.parts)
    normalized = " ".join(text.split())
    if not normalized:
        raise ValueError("No source text")
    return hashlib.sha256(normalized.encode()).hexdigest()


def official_links():
    sources = json.loads((ROOT / "data/sources.json").read_text())["sources"]
    return sorted({
        url for source in sources if source["status"] == "verified"
        for url in [source["public_url"], *(item["url"] for item in source.get("additional_links", []))]
    })


def link_status(url):
    try:
        with request(url, method="HEAD") as response:
            return {"url": url, "status": response.status, "outcome": "reachable"}
    except HTTPError as error:
        if error.code in {404, 410}:
            outcome = "broken"
        elif 300 <= error.code < 400:
            outcome = "redirect; review destination"
        else:
            outcome = "inconclusive"
        return {"url": url, "status": error.code, "outcome": outcome}
    except (URLError, TimeoutError) as error:
        return {"url": url, "outcome": "inconclusive", "detail": str(error)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    baseline = json.loads(args.baseline.read_text()) if args.baseline.exists() else {}
    sources = json.loads((ROOT / "data/monitoring.json").read_text())["sources"]
    changes = []
    failures = []
    emitted = set()
    for source in sources:
        if not source["enabled"]:
            continue
        key, url = source["id"], source["url"]
        try:
            digest = snapshot(url)
        except (OSError, ValueError, LookupError) as error:
            failures.append({"source": key, "url": url, "error": str(error)})
            continue
        prior_hash = baseline.get(key)
        if prior_hash != digest and digest not in emitted:
            changes.append({
                "source": key, "url": url, "change": "updated" if prior_hash else "new baseline",
                "fingerprint": digest, "status": "needs editorial review",
            })
            emitted.add(digest)
        baseline[key] = digest
    links = [link_status(url) for url in official_links()]
    args.baseline.parent.mkdir(parents=True, exist_ok=True)
    args.baseline.write_text(json.dumps(baseline, indent=2) + "\n")
    report = {"review_candidates": changes, "monitor_errors": failures, "official_link_health": links}
    (args.output / "review-queue.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{len(changes)} candidate(s), {len(failures)} monitoring error(s), {len(links)} official link probe(s).")
    for link in links:
        print(f'{link["outcome"]}: {link["url"]}')
    if failures or any(link["outcome"] == "broken" for link in links):
        raise SystemExit("Source review required; see the review queue artifact.")


if __name__ == "__main__":
    main()
