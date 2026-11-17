# PIIK Kenya — pre-launch redesign

A lightweight, free property-guidance website in plain HTML, CSS and JavaScript. The Phase 1 redesign lives on `piik-prelaunch-redesign`; no build step, backend, payment flow or AI integration is needed.

## Local review

```sh
cd /workspace/my-org-site
python3 -m http.server 3000 --bind 0.0.0.0
```

Open the running server through your environment's supported preview/port forwarding or browser. The server is for development only. No new public deployment has been made. Use the existing isolated checkout; no worktree is necessary.

## What works

- Responsive navigation, keyboard focus, skip links and reduced-motion support.
- Four tailored PIIK Check categories with per-category checklist state, reset and print. No verification lookup, score or approval is produced.
- Consumer, professional and diaspora journeys, official resource explanations and expandable educational guides.
- Separate consumer and professional status cards: registration/enquiries are unavailable, buttons are disabled and no personal information is collected.
- Privacy, service limitations and transparent image/source status.

## Before any release

- Registration remains disabled for this launch. Configure and test real submission endpoints and data-protection arrangements only before opening registration later. See [form integration notes](docs/forms.md).
- Independently verify official resource URLs; network policy prevented verification. Direct links are withheld. See [source register](docs/source-register.md).
- Retain the visible disclosures for original AI-generated editorial imagery. These scenes are not actual properties, network members or client stories. Real documentary replacements require appropriate rights and provenance.
- Confirm privacy contact readiness and any additional organisation-specific legal notices.
- Review and explicitly approve merge/deployment. `CNAME` is preserved as `piikkenya.com`; no domain, deployment or environment publication is part of this change.

## Validation

The browser checks in `tests/site.cjs` use the environment-provided Playwright and Chromium (no runtime web dependencies). Start the server, then run:

```sh
node --check app.js
node tests/site.cjs
```

Set `PIIK_TEST_URL` to change the default test target, or `PIIK_CHROMIUM` to change the browser executable. Browser output/screenshots are written outside the checkout to `/tmp/piik-review` by default. An optional axe-core accessibility audit can be run from the environment without adding it as a website dependency.

## Visual review update

The redesign now includes six original photorealistic AI-generated editorial scenes: residential architecture, apartments, land, professional collaboration, diaspora buyers and a Nairobi-inspired cityscape. The cinematic desktop hero becomes a photo-first stacked layout on mobile. All existing guidance, preview forms and safeguards remain in place.

Responsive assets and provenance live in `assets/imagery/`. To regenerate WebP variants from the separately preserved PNG masters, run `python3 scripts/optimise-images.py /path/to/masters` with Pillow installed. This is a maintenance tool, not a website dependency. See [visual review](docs/visual-review.md) and [image/source register](docs/source-register.md).

To export self-contained review pages without deploying, run `python3 scripts/package-preview.py /path/to/review-output`. The resulting ZIP includes desktop/mobile responsive HTML and embedded assets. Use `node tests/imagery.cjs` for the additional image-loading and transfer-budget checks.

## Publication readiness

The approved design has received a small launch-readiness pass. Non-submitting form previews have been replaced by explicit disabled status cards; checklists and approved visuals are retained. GitHub Pages deployment evidence, approval requirements and post-approval verification steps are recorded in [launch readiness](docs/launch-readiness.md). Do not merge or publish without the owner's explicit approval. Earlier visual-review reports describe historical validation; the launch-review test artifacts cover the current candidate.
