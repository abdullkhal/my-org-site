# PIIK Kenya — Phase 2 review

A static HTML/CSS/JavaScript property-guidance website. The Phase 2 candidate preserves the architectural hero, original logo, green/gold identity, system typography and responsive design. Work is on `phase-2-improvements`, based on latest fetched `main` (`7159d01`). No deployment or merge is included.

## Develop locally

Use the existing isolated checkout; no Git worktree is necessary unless requested.

```sh
cd /workspace/my-org-site
python3 -m http.server 3000 --bind 0.0.0.0
```

Python 3 serves the site; there is no package installation or production build step. Node.js, environment-provided Playwright and `/usr/bin/chromium` run browser tests. The free checklists work without registration; navigation/guides also have non-JavaScript fallbacks.

## Maintain content

`data/sources.json` records authority candidates, scope, limitations and verification evidence. Nine destinations supplied through the founder’s independent research are enabled in the local Phase 2 hub. EBK and NEMA remain pending; published registers are distinguished from live status services. `data/knowledge.json` holds seven educational guides and review metadata. Checklist content is the structured `guidance` object in `app.js`.

After changing sources/guides, regenerate static content:

```sh
python3 scripts/render-content.py
python3 scripts/render-content.py --check
python3 scripts/render-source-review.py --check
```

Rendering is an editorial step; the deployed site reads static HTML and needs no runtime JSON fetch or API. See [AI-assisted maintenance](docs/phase2/agent-foundation.md) for evidence and founder-review gates.

## Validate

With the server running:

```sh
node --check app.js
node tests/site.cjs
node tests/imagery.cjs
node tests/phase2.cjs
node tests/integration-preparation.cjs
node tests/review-links.cjs
python3 -m unittest discover -s tests -p 'test_source_confirmation.py'
python3 scripts/render-content.py --check
python3 scripts/render-source-review.py --check
node scripts/enquiry-workflow.cjs
```

`PIIK_TEST_URL`, `PIIK_CHROMIUM` and `PIIK_TEST_OUTPUT` override defaults. Tests write logs/screenshots outside the repository, by default under `/tmp`. The optional axe audit runs when `PIIK_AXE_PATH` points to an installed axe-core script. For this review, axe-core 4.11.0 was installed in `/tmp/piik-phase2-tools` without adding a website dependency. Install/reinstall review tooling outside the checkout with a writable npm cache if required:

```sh
npm install --prefix /tmp/piik-phase2-tools --cache /tmp/piik-npm-cache --no-audit --no-fund --save-exact axe-core@4.11.0
PIIK_AXE_PATH=/tmp/piik-phase2-tools/node_modules/axe-core/axe.min.js node tests/site.cjs
```

## Review without deployment

```sh
python3 scripts/package-preview.py /tmp/piik-phase2-export
```

The ZIP embeds assets and includes homepage, Terms, Privacy, Credits and a disabled enquiry prototype with synthetic examples, plus `official-links.html` with the current nine-link review table and pending destinations. Preserve all extracted pages together. The live source remains unchanged. Optional image regeneration (`scripts/optimise-images.py`) requires separately preserved original masters and Pillow; it is not required for serving/testing existing imagery.

## Enquiries, measurement and approval

Online collection and tracking remain disabled. `review/enquiries.html` shows four disabled prototypes. `data/enquiries.json`, `data/response-templates.json` and the offline synthetic-only workflow prepare future operations; they are not production intake or notification services. Never add real enquiry records or credentials to this public repository.

Read [Phase 2 audit and approval report](docs/phase2/audit-and-review.md), [enquiry/measurement decisions](docs/phase2/operations.md) and [AI foundation](docs/phase2/agent-foundation.md). Provider, mailbox, privacy arrangements, official links and any third-party measurement require review before activation. Founder review is required for sensitive communications and business decisions. Do not push, merge, deploy, purchase services or collect real information without explicit approval.

Historical Phase 1 documents remain for context; the Phase 2 report and current structured records describe this candidate.

The [proposed official website list](docs/phase2/official-websites.md) accepts independent founder confirmation without requiring this environment to reach the service. Formspree mapping and mocked result handling are in `scripts/formspree-adapter.cjs`; live intake remains unavailable and `data/formspree.json` has no endpoint or selected email.

The [official link update](docs/phase2/official-link-update.md) records the founder-supplied URL corrections, the nine-link/eight-authority comparison and register-versus-live-status distinctions.
