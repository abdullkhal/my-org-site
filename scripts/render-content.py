#!/usr/bin/env python3
"""Render reviewed structured content to static HTML. No runtime API or build dependency.
Run after editing data/sources.json or data/knowledge.json; use --check in CI/review.
"""
import json,re,sys
from html import escape as e
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sources=json.loads((ROOT/'data/sources.json').read_text())['sources']
guides=json.loads((ROOT/'data/knowledge.json').read_text())['guides']
assert len({s['id'] for s in sources})==len(sources)
by_id={s['id']:s for s in sources}
cards=[]
for n,s in enumerate(sources,1):
    if s['status']=='verified':
        assert s['public_url'] and s['public_url'].startswith('https://') and s['evidence'] and s['reviewer'] and s['next_review_at']
        assert all(item.get('url', '').startswith('https://') and item.get('excerpt') and item.get('checked_at') for item in s['evidence'])
        urls=[{'url':s['public_url'], 'label':s.get('link_label','Visit official resource →')}, *s.get('additional_links',[])]
        assert all(link['url'].startswith('https://') and (link['url']==s['public_url'] or any(item['url']==link['url'] for item in s['evidence'])) for link in urls)
        action='<div class="source-actions">'+''.join(f'<a class="text-link" href="{e(link["url"],quote=True)}" rel="external noreferrer">{e(link["label"])}</a>' for link in urls)+'</div>'
    else:
        assert s['public_url'] is None
        action='<span class="unverified" aria-disabled="true">'+('Identify the county and project first' if s['id']=='approvals' else 'Awaiting independent confirmation')+'</span>'
    cards.append(f'<article class="source-card" id="resource-{e(s["id"])}"><span class="source-number">{n:02d} / {e(s.get("resource_kind", "Resource guide")).upper()}</span><h3>{e(s["title"])}</h3><p class="source-name">{e(s["authority"])}</p><p>{e(s["scope"])}</p><p class="source-limit">{e(s["limitations"])}</p>{action}</article>')
knowledge=[]
for g in guides:
    assert all(id in by_id for id in g['source_ids'])
    refs=' · '.join(f'<a href="#resource-{e(id)}">{e(by_id[id]["title"])}</a>' for id in g['source_ids'])
    knowledge.append(f'<details class="article" id="guide-{e(g["id"])}"><summary><span class="article-category">{e(g["category"])}</span><span class="article-title">{e(g["title"])}</span><span class="plus" aria-hidden="true">+</span></summary><div class="article-body">'+''.join(f'<p>{e(p)}</p>' for p in g['paragraphs'])+f'<p class="small">Relevant authorities: {refs}</p></div></details>')
p=ROOT/'index.html';old=p.read_text();new=old
for name,content in [('SOURCES','<div class="sources-grid">'+ '\n'.join(cards)+'</div>'),('KNOWLEDGE','<div class="knowledge-grid">'+ '\n'.join(knowledge)+'</div>')]:
    new=re.sub(f'(<!-- {name}:START -->).*?(<!-- {name}:END -->)',lambda m:m[1]+'\n'+content+'\n'+m[2],new,flags=re.S)
if '--check' in sys.argv:
    if old!=new: raise SystemExit('Structured content is stale: run python3 scripts/render-content.py')
    print('PASS structured content matches static HTML')
else:p.write_text(new)
