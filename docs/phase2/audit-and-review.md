> Current amendment, 17 November 2026: the founder supplied independently researched URLs. Nine destinations for eight authorities are now enabled locally, with founder provenance; the development environment still cannot fetch them. EBK and NEMA remain pending. [Final source table](official-websites.md) and [official-link update](official-link-update.md) supersede the earlier all-pending link observations below. No merge, publication or deployment occurred.

# Phase 2 audit and founder review

Date: 17 November 2026. Base: latest fetched `origin/main`, commit `7159d013418b3d208bb5543837b9aa778d6395f9`. Working branch: `phase-2-improvements`. No push, merge, deployment, environment publication, purchase or real enquiry collection is part of this work.

## Audit findings and changes

| Area | Finding | Phase 2 result |
| --- | --- | --- |
| Identity/design | Strong static site, architectural hero, local WebP imagery, original logo, system typography | Preserved artwork/identity; exact requested headline, supporting text, button names and tagline. Closed-interest notice beside secondary CTA |
| Navigation | Existing CTA led to general network content | Secondary CTA now reaches the expression-of-interest status; primary opens the free checklists |
| Presentation | Repeated cautions and image overlays | Removed repetitive overlays; retained accurate contextual alt text, consolidated credits, concise checklist notice and new Terms of Use |
| Official resources | Five candidate authorities, no confirmed outbound links | Eleven scope/limitation records, plus clickable proposed URLs in the founder-review page and a tested independent-confirmation path; no unverified public-hub destination enabled |
| PIIK Check | Four useful interactive categories, wordy progress | Simpler “N of 4 steps reviewed”; resource-scope links on each step; state/reset/print retained, no registration |
| Network | Early cross-discipline concept | Nine proposed disciplines; expression-of-interest process defined without invented members, profiles or certifications |
| Diaspora/knowledge | Three short guides | Seven structured educational guides with source IDs, editorial status, audience, owner and review fields; expanded remote purchase planning |
| Enquiries | Disabled public status cards | Four disabled synthetic form prototypes, enquiry schema, offline categorisation/reporting demo, draft responses and secure-integration checklist |
| AI foundation | No operating model | Human-gated research, source monitoring, knowledge, categorisation, network administration and reporting workflow; no agent runtime or paid API |
| SEO | Homepage metadata only, no sitemap/robots | Canonicals on four public pages, concise metadata/social card, Organization/WebSite JSON-LD, sitemap and crawler rules |
| Measurement | No analytics | Inactive aggregate-event specification; no third-party script, cookies, storage or collector |

## Official-source verification blocker

Read-only HTTPS requests to the live domain and candidate authorities all returned proxy CONNECT 403 Forbidden. No official page was retrieved; neither identity nor service scope was independently verified in this run. This is a development-network restriction, not evidence of a site outage. **Zero outbound authority links are verified or active.** Internal checklist links lead to resource explanations, not to unconfirmed external destinations.

Candidate hosts for optional developer-side review: `earb.go.ke`, `ardhisasa.lands.go.ke`, `lands.go.ke`, `lsk.or.ke`, `lsb.or.ke`, `brs.go.ke`, `vrb.go.ke`, `boraqs.or.ke`, `ebk.go.ke`, `nca.go.ke`, `www.nema.go.ke`. Live comparison additionally needs `piikkenya.com`. Preserve existing network allowlist settings if adding these hosts; inspect any new redirect hosts before approving them. No environment configuration was changed in Phase 2. Development-network access is optional for source review: the founder can independently corroborate destinations using the new clickable review list. A recorded human review can enable a link without another request from this environment.

`data/sources.json` is the authoritative current source register. Candidate hostnames are hypotheses until first-party corroboration, HTTPS redirects and actual register/service content are inspected. County approval routes depend on property location; no single nationwide endpoint was invented. Do not substitute membership associations for statutory licensing authorities. General educational content is explicitly pending first-party review; specific fees, legal procedures and coverage are not asserted as verified facts. Revalidate before publication.

## Validation evidence

- `node --check app.js`: passed.
- `python3 scripts/render-content.py --check`: passed; static cards/guides match structured content.
- `node tests/site.cjs` with axe-core 4.11.0: **137 checks passed**, including desktop/mobile navigation, keyboard guide controls, four checklist categories, state switching/reset/print, no-JavaScript fallbacks, disabled registration, local assets/links, no cookies/storage and no browser JavaScript errors.
- Automated axe A/AA-tagged checks: **zero violations in 12 page/viewport scans**, covering homepage, Privacy, Terms, Credits disabled enquiry prototype and source-review page at 390px and 1440px. Automated audits do not establish complete accessibility compliance.
- `node tests/imagery.cjs`: **74 checks passed**, including appropriate responsive sources, lazy loading, dimensions, local-only imagery, hero containment and transfer budgets. Entire-page image bytes: desktop 794,758; mobile 341,564; retina mobile 785,454. Local HTTP measurements are not production or mobile-network speed scores.
- `node tests/phase2.cjs`: **126 checks passed**, including exact copy, source-link gating, guide targets, non-toggling resource links, canonical/schema checks, local navigation, all four enquiry categories, synthetic-only validation, founder-review routing, live-intake rejection and no prototype submission even with forced `form.submit()` under CSP.
- Preview ZIP integrity and six exported pages checked in Chromium; exported checklists/images work and no external requests or CSP/browser errors remain. A missing prototype favicon found during review was corrected and the export rerun.
- Original image files, PIIK logo and `CNAME` unchanged. No real messages sent, no provider secrets added, no tracking activated.

Local logs, screenshots, accessibility results, image metrics, synthetic report and review ZIP are collected outside the repository in `/workspace/piik-phase2-review`. The export embeds website assets and includes Terms, Privacy, Credits and the disabled enquiry prototype. Direct file URLs can be restricted by browser policy; if necessary serve the extracted folder locally. The full-page screenshots are long because the complete guides/resources are included.

## Approval decisions in plain language

1. **Review the design and copy.** The code is ready for review on the Phase 2 branch, not live.
2. **Confirm the proposed official destinations.** Use the clickable founder list, corroborate authority identity and actual service scope, and return the final URL/evidence/date. Your independent review is sufficient; the development-network restriction does not have to be lifted. Confirmed destinations can be enabled locally before publication; unresolved destinations can remain clearly marked.
3. **Choose an enquiry provider and monitored email.** Formspree is the proposed simple first option, subject to current price, privacy and capability checks. No account or subscription was created. Confirm whether `info@piikkenya.com` is monitored.
4. **Approve how enquiry data will be handled.** Confirm PIIK's controller/contact details, purposes/lawful basis, minimum fields, provider processing/transfer terms and deletion period. A 90-day post-closure period is a proposal, not an active policy.
5. **Decide on measurement later.** The proposed counts collect no enquiry content; any provider and data handling still need your approval. Tracking is currently off.

A separate explicit instruction is needed to merge/publish/deploy or open real collection. Approving the appearance alone does not authorize those actions. See `operations.md` for integration gates and `agent-foundation.md` for AI permissions.

## Limits of this review

Live-domain health, production HTTP security headers, search-engine indexing, provider delivery/bounces, real spam controls and official register usability were not verified. The site's meta CSP enforces local scripts/styles and blocks form/connect requests; it cannot supply response-header-only protections such as `frame-ancestors` or HSTS. Assess host-supported security headers separately before adding a backend. Robots/noindex are crawler guidance, not access control. All repository data and review prototypes are safe to be public; no personal data or credentials belong in them. Original image masters are not needed for this workflow and their availability was not verified.


## Completion follow-up

The follow-up adds `docs/phase2/official-websites.md` and `review/official-links.html`, both generated from source records by `scripts/render-source-review.py`. The record status is now `awaiting_independent_confirmation`; network observations are separate. `scripts/confirm-source.py` defaults to a dry run and accepts actual founder/independent evidence; it never deploys. Six synthetic unit tests verify review requirements, unsafe URL rejection, date checks, dry-run preservation and successful rendering after human review despite a recorded network block. No real authority was falsely marked confirmed.

Formspree remains the proposed provider, with disabled configuration, no endpoint and no selected business email. Provider field mapping and result handling are prepared in a mock-only adapter outside the public runtime. **37 integration-preparation checks** passed; no mock is represented as live provider delivery. **19 source-review page checks** passed, including all ten candidate links and widths from 320px through 1440px. Across the browser, imagery, workflow, integration and review-page suites: **393 checks passed**, plus **6 source-confirmation unit tests**. The 12 axe scans are included in the browser count, not additional tests.

Vendor documentation requests are also denied by the proxy. Current Formspree price/plan limits, server-side validation/spam controls, notification customisation, data location, processor terms and delivery remain unverified until account/vendor review. This does not block preparing the site for founder design/content approval. Website publication and customer-data collection are separate decisions: the website can be approved with collection still disabled. No new email address has been selected and no existing address is assumed to be the submission destination.

The local development port 3000 was occupied and did not return a useful response in this session. Validation used a separate server on port 3002; the review package was checked on port 3003. These are internal validation ports, not public deployments or preview links. Current logs and regenerated previews are in `/workspace/piik-phase2-review`; previous results were replaced with this run's results. No changes were made to the logo, imagery or domain file.
