#!/usr/bin/env python3
"""Generate the current official-link review table from source records; --check detects drift."""
from pathlib import Path
from html import escape as e
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
records = json.loads((ROOT/'data/sources.json').read_text())['sources']

def save(name, text):
    if '--check' in sys.argv:
        if (ROOT/name).read_text() != text:
            raise SystemExit('Stale source review: run python3 scripts/render-source-review.py')
    else:
        (ROOT/name).write_text(text)

intro = '''# Official website links — Phase 2 review table

Recorded review date: **17 November 2026**. Nine destinations covering eight authorities were supplied by the founder following independent research and are enabled in the local Phase 2 hub. The founder’s research date was not specified. This environment could not retrieve the pages; no live individual-status or service-availability check is claimed. PIIK does not perform these checks and has no claimed affiliation or endorsement.

The earlier ten-destination checklist covered ten authorities. Two BORAQS URLs still represent one authority: **EBK and NEMA are both absent from the supplied list**, not just one missing tenth destination. They remain pending. County development approvals are a separate location-specific route, not one of the original ten candidate URLs.

| Authority / service | Destination | Type and what it establishes | Limits | Review status |
| --- | --- | --- | --- | --- |
'''
rows = []
cards = []
for source in records:
    active = source['status'] == 'verified'
    links = [{'url':source['public_url'], 'label':source.get('link_label',source['title']), 'resource_kind':source.get('resource_kind','Resource')}, *source.get('additional_links',[])] if active else []
    if active:
        for link in links:
            title = 'BORAQS — quantity surveyors' if '/registered/qs' in link['url'] else 'BORAQS — architects' if source['id']=='boraqs' else source['title']
            rows.append(f'| {title} | [{link["url"]}]({link["url"]}) | {link["resource_kind"]}. {source["scope"]} | {source["limitations"]} | Founder-supplied research; recorded {source["checked_at"]} |')
        actions = ''.join(f'<p><a href="{e(link["url"],quote=True)}" rel="external noreferrer">{e(link["label"])}</a></p>' for link in links)
        status = 'Enabled from founder-supplied independent research · recorded '+source['checked_at']
    else:
        candidate = ('Unconfirmed candidate: `'+source['candidate_url']+'`') if source['candidate_url'] else 'Identify the responsible county and property first'
        rows.append(f'| {source["title"]} | {candidate} | {source["scope"]} | {source["limitations"]} | Pending — no active hub link |')
        actions = '<p class="unverified">'+('Unconfirmed candidate: '+e(source['candidate_url']) if source['candidate_url'] else 'Identify the county and property first')+'</p>'
        status = 'Pending independent confirmation'
    cards.append(f'<article class="source-card"><h2>{e(source["title"])}</h2><p>{e(source["authority"])}</p>{actions}<p>{e(source["scope"])}</p><p>{e(source["limitations"])}</p><p class="small">{e(status)} · ID: {e(source["id"])}</p></article>')
ending = '''

## Registers are not all live checks

EARB is a published **2026 Gazette**: an entry reflects that publication, not an assurance of current practising status. LSB and BORAQS register pages should be treated as published listings unless the authority explicitly provides a current live-status function. LSK’s FAQ is guidance, not an individual search result. BRS and VRB homepages are gateways, not individual/company verification results. Ardhisasa is a service portal; property-specific official applications/results are separate. NCA’s contractor page is not project approval or a completion guarantee.

Confirm identity matches, register dates, current standing, applicable service coverage and fees directly with the responsible authority. No register entry establishes land ownership, authority to sell, project permission or transaction safety outside that record’s actual scope.

## Provenance and later changes

`data/sources.json` records each accepted URL, founder provenance, review date, resource type, limitations, evidence note and next review date. Earlier candidate URLs are retained as history, not active links. Monthly recheck is scheduled as a local editorial reminder for 17 December 2026; there is no automated monitoring. Network errors remain separate observations. Use `scripts/confirm-source.py` only when actual new evidence is supplied, then regenerate both content and this review table. No change publishes the website.
'''
save('docs/phase2/official-websites.md',intro+'\n'.join(rows)+ending)
page = '''<!doctype html><html lang="en-KE"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width,initial-scale=1" /><meta name="robots" content="noindex,nofollow" /><meta name="referrer" content="no-referrer" /><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'none'; style-src 'self'; img-src 'self' data:; connect-src 'none'; form-action 'none'; object-src 'none'; base-uri 'none'" /><link rel="stylesheet" href="../style.css" /><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml" /><title>Official link review | PIIK Kenya</title></head><body><main class="container document-main" id="main"><p class="eyebrow">FOUNDER REVIEW · NOT PUBLISHED</p><h1>Official website link table</h1><p>Recorded on 17 November 2026: nine destinations supplied through the founder’s independent research cover eight authorities. Development-network access remains blocked; no live status checks are claimed.</p><p>EARB is a dated 2026 Gazette publication. LSK’s FAQ is guidance. Published register entries must be distinguished from current practising status and property-specific checks.</p><p>EBK and NEMA both remain pending. BORAQS has two profession-specific destinations, so nine URLs do not cover nine authorities. County approvals require the property location. PIIK performs no official checks and claims no affiliation or endorsement.</p><div class="sources-grid">'''+''.join(cards)+'''</div><a class="button green" href="../index.html#official-hub">Return to PIIK Kenya →</a></main></body></html>'''
save('review/official-links.html',page)
