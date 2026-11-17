#!/usr/bin/env python3
"""Record an independently completed official-source review; no network required.
Default is a dry run. --apply updates data/sources.json, never deploys or publishes.
Use only after the named reviewer has actually supplied the stated evidence.
"""
import argparse
import copy
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]

def https_url(value):
    parsed = urlsplit(value)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.port not in (None, 443):
        raise ValueError('Use an HTTPS URL without credentials or a custom port')
    return value

def confirm_source(source, *, url, checked_at, reviewer, evidence_url, note, next_review_at):
    checked, review = date.fromisoformat(checked_at), date.fromisoformat(next_review_at)
    if checked > date.today() or review <= checked:
        raise ValueError('Check date cannot be in the future; next review must follow the check')
    if not reviewer.strip() or len(note.strip()) < 20:
        raise ValueError('Reviewer and a factual evidence note of at least 20 characters are required')
    result = copy.deepcopy(source)
    result.update(status='verified', public_url=https_url(url), checked_at=checked_at,
                  reviewer=reviewer.strip(), next_review_at=next_review_at,
                  verification_method='independent_human_review',
                  evidence=[{'url': https_url(evidence_url), 'excerpt': note.strip(),
                             'checked_at': checked_at, 'reviewer': reviewer.strip()}])
    # Environment reachability remains a separate historical observation.
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for field in ['source-id', 'url', 'checked-at', 'reviewer', 'evidence-url', 'note', 'next-review-at']:
        parser.add_argument('--'+field, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    path = ROOT/'data/sources.json'
    data = json.loads(path.read_text())
    source = next((s for s in data['sources'] if s['id'] == args.source_id), None)
    if source is None:
        parser.error('Unknown source ID')
    updated = confirm_source(source, url=args.url, checked_at=args.checked_at, reviewer=args.reviewer,
                             evidence_url=args.evidence_url, note=args.note, next_review_at=args.next_review_at)
    if args.apply:
        data['sources'][data['sources'].index(source)] = updated
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
        print('Recorded review. Run python3 scripts/render-content.py and tests; nothing was published.')
    else:
        print(json.dumps(updated, ensure_ascii=False, indent=2))
        print('Dry run only. Nothing changed.')

if __name__ == '__main__':
    main()
