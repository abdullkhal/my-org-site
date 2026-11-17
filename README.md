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
- Separate consumer and professional response previews: validation, safe local review, clear/reset and no network submission or persistence.
- Privacy, service limitations and transparent image/source status.

## Before any release

- Configure and test real submission endpoints and data-protection arrangements before opening registration. See [form integration notes](docs/forms.md).
- Independently verify official resource URLs; network policy prevented verification. Direct links are withheld. See [source register](docs/source-register.md).
- Confirm usage rights for the supplied Nairobi image or replace it with licensed imagery. It is explicitly marked for review only.
- Confirm privacy contact readiness and any additional organisation-specific legal notices.
- Review and explicitly approve merge/deployment. `CNAME` is preserved as `piikkenya.com`; no domain, deployment or environment publication is part of this change.

## Validation

The browser checks in `tests/site.cjs` use the environment-provided Playwright and Chromium (no runtime web dependencies). Start the server, then run:

```sh
node --check app.js
node tests/site.cjs
```

Set `PIIK_TEST_URL` to change the default test target, or `PIIK_CHROMIUM` to change the browser executable. Browser output/screenshots are written outside the checkout to `/tmp/piik-review` by default. An optional axe-core accessibility audit can be run from the environment without adding it as a website dependency.
