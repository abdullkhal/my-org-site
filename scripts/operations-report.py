#!/usr/bin/env python3
"""Summarise the latest source report and verify website health."""
import argparse
from collections import Counter
from datetime import date, timedelta
import json
from pathlib import Path
import subprocess
import sys
from urllib.request import HTTPRedirectHandler, build_opener

ROOT = Path(__file__).resolve().parents[1]
LIVE = "https://piikkenya.com/"
ROUTES = ("index.html", "verify.html", "directory.html", "weekly.html", "watch.html",
          "knowledge.html", "sitemap.xml", "feed.xml")
CHECKS = (("build-site.py", "--check"), ("check-links.py",), ("render-source-review.py", "--check"))


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, new_url):
        return None


def site_health(live):
    checks = []
    for check in CHECKS:
        result = subprocess.run([sys.executable, "scripts/" + check[0], *check[1:]], cwd=ROOT,
                                capture_output=True, text=True, timeout=30)
        checks.append((check[0], "passed" if result.returncode == 0 else "failed"))
        if result.returncode:
            print(result.stderr or result.stdout, file=sys.stderr)
    if live:
        opener = build_opener(NoRedirect())
        for path in ROUTES:
            try:
                expected = (ROOT / path).read_bytes()
                with opener.open(LIVE if path == "index.html" else LIVE + path, timeout=6) as response:
                    payload = response.read(len(expected) + 1)
                checks.append((path, "matches release" if payload == expected else "release differs"))
            except OSError as error:
                print(f"{path}: {error}", file=sys.stderr)
                checks.append((path, "inconclusive"))
                if "Tunnel connection failed" in str(error):
                    break
    return checks


def load(name):
    return json.loads((ROOT / "data" / f"{name}.json").read_text())


def recent(records, key, today):
    dates = [item.get(key) for item in records if item["status"] == "approved"]
    return sum(today - timedelta(days=6) <= date.fromisoformat(value) <= today
               for value in dates if value)


def report(queue, health, today):
    editorial = load("editorial")
    profiles = load("directory")["profiles"]
    leads = queue.get("review_candidates", [])
    errors = queue.get("monitor_errors", [])
    statuses = Counter(item["outcome"] for item in queue.get("official_link_health", []))
    queue_date = queue.get("date")
    inactive = not queue_date or date.fromisoformat(queue_date) < today - timedelta(days=2)
    link_health = ", ".join(f"{count} {status}" for status, count in sorted(statuses.items())) or "unavailable"
    site_results = ", ".join(f"{name} {status}" for name, status in health) or "unavailable"
    lines = [
        f"# PIIK Kenya weekly executive report — {today}",
        "",
        f"- The latest queue contains {len(leads)} leads awaiting evidence review.",
        f'- This week PIIK published {recent(editorial["articles"], "published", today)} articles, '
        f'{recent(editorial["editions"], "published", today)} Brief editions and '
        f'{recent(editorial["notices"], "date", today)} Watch entries.',
        f'- The Directory added {recent(profiles, "published", today)} profiles and recorded '
        f'{recent(profiles, "checked_at", today)} reviews this week.',
        f'- Collection succeeded for {queue.get("successful_sources", 0)} of {queue.get("enabled_sources", 0)} '
        f'enabled sources and reported {len(errors)} errors.',
        f'- Official link check results are {link_health}.',
        f'- Website check results are {site_results}.',
        "- The collection report is missing or overdue." if inactive else f"- The latest collection report is dated {queue_date}.",
        "- Bring sensitive or disputed editorial decisions to the founder after evidence review.",
        "- The repository workflows use existing services and no AI API.",
        "",
        "## Exceptions and next priority",
        "",
    ]
    if errors:
        lines.append("- Check collector failures for " + ", ".join(sorted({item["source"] for item in errors})) + ".")
    if inactive:
        lines.append("- Check the latest scheduled Actions run and restore the reporting cadence.")
    if not queue.get("enabled_sources"):
        lines.append("- Review and activate one accessible official source before attempting an evidence-led Brief.")
    elif leads:
        lines.append("- Review the candidate queue and advance eligible leads in the weekly Codex cycle.")
    else:
        lines.append("- Review source coverage and update the roadmap checkpoint.")
    checkpoint = (ROOT / "ROADMAP.md").read_text().partition("## Checkpoint")[2]
    lines.extend(["", "## Roadmap checkpoint", "", checkpoint.strip(), ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--live", action="store_true", help="Compare public routes against this checkout")
    args = parser.parse_args()
    queue = json.loads(args.queue.read_text()) if args.queue.exists() else {}
    health = site_health(args.live)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report(queue, health, date.today()))
    print(f"Executive report written to {args.output}")
    if any(status not in {"passed", "matches release"} for _, status in health):
        raise SystemExit("Website health requires review. See the executive report.")


if __name__ == "__main__":
    main()
