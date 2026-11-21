#!/usr/bin/env python3
"""Report changes and HTTP health without modifying published content."""
import argparse
from datetime import date, timedelta
import errno
import hashlib
from html.parser import HTMLParser
import json
import re
import sys
from time import sleep
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import build_opener, HTTPRedirectHandler, Request
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from intelligence import validate_registry

AGENT = "PIIKKenyaSourceMonitor/1.0 (+https://piikkenya.com/about.html)"
LIMIT = 2_000_000
MAX_LINKS = 40
MAX_QUEUE = 200


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, new_url):
        return None


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ignored = 0
        self.parts = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self.ignored += 1
        if tag == "a" and not self.ignored:
            self.links.extend(value for key, value in attrs if key == "href" and value)

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
    opener = build_opener(NoRedirect())
    req = Request(url, method=method, headers={"User-Agent": AGENT})
    for attempt in range(2):
        try:
            return opener.open(req, timeout=6)
        except HTTPError as error:
            if attempt or error.code not in {500, 502, 503, 504}:
                raise
            error.close()
        except (URLError, TimeoutError) as error:
            transient = isinstance(error, TimeoutError) or getattr(
                getattr(error, "reason", None), "errno", None
            ) in {errno.ETIMEDOUT, errno.ECONNRESET}
            if attempt or not transient:
                raise
        sleep(1)


def discovered_links(base, references, prefix):
    origin = public_url(base)
    candidates = []
    for reference in references:
        try:
            url = public_url(urljoin(base, reference.strip()))
        except ValueError:
            continue
        if url.hostname == origin.hostname and url.path.startswith(prefix):
            candidate = urlunsplit(("https", origin.hostname, url.path, "", ""))
            if candidate != base and candidate not in candidates:
                candidates.append(candidate)
                if len(candidates) == MAX_LINKS:
                    break
    return candidates


def snapshot(url, *, mode="notice_index", prefix="/"):
    parsed = public_url(url)
    robots = RobotFileParser()
    try:
        with request(f"https://{parsed.netloc}/robots.txt") as response:
            policy = response.read(256_001)
        if len(policy) > 256_000:
            raise ValueError("robots.txt exceeds size limit")
        robots.parse(policy.decode("utf-8", "replace").splitlines())
    except HTTPError as error:
        if error.code not in {404, 410}:
            raise
        robots.allow_all = True
    if robots.crawl_delay(AGENT) or robots.request_rate(AGENT):
        raise ValueError("Source specifies an automated request schedule requiring review")
    if not robots.can_fetch(AGENT, url):
        raise ValueError("robots.txt disallows monitoring")
    with request(url) as response:
        media_type = response.headers.get_content_type()
        payload = response.read(LIMIT + 1)
        if len(payload) > LIMIT:
            raise ValueError("Source exceeds monitor size limit")
        text = payload.decode(response.headers.get_content_charset() or "utf-8", "replace")
    links = []
    if mode == "notice_index" and media_type in {"text/html", "application/xhtml+xml", "text/plain"}:
        if media_type != "text/plain":
            parser = VisibleText()
            parser.feed(text)
            links = parser.links
            text = " ".join(parser.parts)
    elif mode in {"rss", "atom"} and media_type in {
        "application/rss+xml", "application/atom+xml", "application/xml", "text/xml"
    }:
        if re.search(r"<!DOCTYPE|<!ENTITY", text, re.IGNORECASE):
            raise ValueError("Feed declares a document type or entity")
        root = ET.fromstring(text)
        for item in root.findall("./channel/item") + root.findall("./{*}entry"):
            for link in item.findall("./{*}link"):
                if link.get("rel", "alternate") == "alternate":
                    links.append(link.get("href") or link.text or "")
    else:
        raise ValueError(f"Unsupported source type for {mode}: {media_type}")
    normalized = " ".join(text.split())
    if not normalized:
        raise ValueError("No source text")
    links = discovered_links(url, links, prefix)
    fingerprint = hashlib.sha256(json.dumps([normalized, sorted(links)]).encode()).hexdigest()
    return fingerprint, links


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


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def collect(sources, state, today):
    changes, failures = [], []
    fingerprints = state["sources"]
    recent = state["candidates"]
    successes = 0
    for source in sources:
        key, url = source["id"], source["url"]
        prior = fingerprints.get(key, {})
        try:
            digest, links = snapshot(url, mode=source["method"], prefix=source["path_prefix"])
        except (OSError, ValueError, LookupError, ET.ParseError) as error:
            failures.append({"source": key, "url": url, "error": str(error)})
            continue
        successes += 1
        if prior.get("fingerprint") != digest:
            new_links = set(links) - set(prior.get("links", []))
            for destination in sorted(new_links) or [url]:
                identity = destination if destination != url else f"{url}#{digest}"
                candidate_id = hashlib.sha256(identity.encode()).hexdigest()
                if candidate_id in recent:
                    continue
                candidate = {"id": candidate_id, "source": key, "url": destination,
                             "discovered_at": today.isoformat(), "status": "needs editorial review",
                             "kind": "linked item" if destination != url else "index change"}
                recent[candidate_id] = candidate
                changes.append(candidate)
        fingerprints[key] = {"fingerprint": digest, "links": links, "last_successful_check": today.isoformat()}
    return changes, failures, successes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--mode", choices=("daily", "weekly", "monthly"), default="daily")
    args = parser.parse_args()
    state = json.loads(args.baseline.read_text()) if args.baseline.exists() else {"sources": {}, "candidates": {}}
    registry = json.loads((ROOT / "data/monitoring.json").read_text())["sources"]
    validate_registry(registry)
    sources = [source for source in registry if source["enabled"]]
    today = date.today()
    changes, failures, successes = collect(sources, state, today)
    recent = sorted(state["candidates"].values(), key=lambda item: item["discovered_at"], reverse=True)
    retained = [item for item in recent[:MAX_QUEUE] if date.fromisoformat(item["discovered_at"]) >= today - timedelta(days=30)]
    state["candidates"] = {item["id"]: item for item in retained}
    links = [link_status(url) for url in official_links()] if args.mode != "daily" else []
    due = [
        {"id": item["id"], "status": item["status"],
         "last_successful_check": state["sources"].get(item["id"], {}).get("last_successful_check")
         or item["last_successful_check"]}
        for item in registry
    ] if args.mode == "monthly" else []
    write_json(args.baseline, state)
    report = {"mode": args.mode, "date": today.isoformat(), "enabled_sources": len(sources),
              "successful_sources": successes, "review_candidates": changes if args.mode == "daily" else retained,
              "monitor_errors": failures, "official_link_health": links, "source_review": due}
    write_json(args.output / "review-queue.json", report)
    print(f"{args.mode}: {successes}/{len(sources)} sources collected, {len(changes)} new leads, "
          f"{len(failures)} collection errors, {len(links)} link probes.")
    if not sources:
        print("Collection inactive. No source has documented automated-access approval.")
    if failures or any(link["outcome"] == "broken" for link in links):
        raise SystemExit("Source review required; see the review queue artifact.")


if __name__ == "__main__":
    main()
