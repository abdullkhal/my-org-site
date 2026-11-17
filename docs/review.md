# Phase 1 review and validation

> Historical review snapshot. The current publication candidate and disabled registration state are documented in [launch readiness](launch-readiness.md).

## Purpose and scope

Replace the certification-led site with an honest pre-launch property-integrity initiative. The journeys support consumer education, learning about demand and proposed professional collaboration. All initial PIIK services are free; there is no payment, subscription or paid membership flow.

The design uses #103A32 forest green, #D7BA79 muted gold and #F4F5F0 ivory, with a preserved PIIK logo, system serif/sans-serif typography, rounded cards, original SVG icons and optimised local imagery. No framework, build step, analytics, third-party script or runtime AI service is required. The static editorial imagery is original AI-generated artwork; see `visual-review.md`.

## Review journeys

1. **Consumer:** “Check Before You Commit” → choose a category → review practical steps → identify the official bodies to consult → explore a local-only consumer response preview.
2. **Professional:** network proposition → proposed collaboration/transparency/profile benefits → separate professional response preview. No claim of existing members or verified profiles.
3. **Diaspora:** independent representation, official property checks and payment planning → property checklist.
4. **Education:** keyboard-accessible expandable guides on fraud awareness, credentials and pre-payment decisions.
5. **Trust:** pre-launch status, limits, privacy information and image/source status remain explicit.

## Verified in the development environment

- JavaScript syntax check: passed.
- 110 browser assertions passed using installed Playwright and Chromium.
- All navigation targets/local assets, both main CTAs, network form pathway and document return links work.
- Four guidance categories, four distinct actionable steps per category, keyboard radio navigation, per-category in-memory state, reset and print work. A printed PDF was inspected via text extraction and contains the limitation notice.
- Knowledge guides open/close by keyboard.
- Both forms validate required selections, acknowledgement and optional-email syntax; safely render text without interpreting HTML; move focus to the local review; invalidate stale reviews when edited; and clear entries on reset.
- Form interactions make zero network requests. No cookies, localStorage or sessionStorage are written by the site code. There are no upload fields.
- No horizontal overflow at 320, 390, 768, 1024, 1440 and 1920 pixels. Desktop/mobile screenshots captured; the desktop toggle visibility defect found during review was fixed.
- Mobile menu opens, closes after navigation/outside clicks and responds to Escape with focus restored.
- No-JavaScript navigation and educational fallback work; response controls remain disabled so personal data cannot be accidentally submitted as a GET request.
- axe-core 4.11.0 reports zero WCAG A/AA-tagged automated violations on the homepage, privacy and credits pages at 390 and 1440 pixels. An initially identified desktop text-link distinction issue was fixed and the full suite rerun. Automated checks do not establish complete accessibility compliance; a production assistive-technology review is still recommended.
- No browser JavaScript errors. A restrictive meta Content Security Policy prevents connections and native form submissions, forbids embedded objects/base overrides and permits only local scripts/styles plus the hash-authorised structured data. Hosting-level HTTPS, framing and other security headers should also be confirmed before release.
- `CNAME` is unchanged; original logo and original assets are preserved.

Tests use only synthetic entries. No real registration, official search, title check, professional verification, network membership or external submission was performed.

## Outstanding external requirements

1. **Submission/data protection:** configure real endpoints and test receipt/failure handling, confirm controller/contact details, retention and processors, and update privacy/consent copy before accepting registrations. See `forms.md`.
2. **Official sources:** network restrictions prevented first-party link verification. The resource hub contains useful descriptions but withholds direct links. See `source-register.md`.
3. **Imagery disclosure:** the older image with unconfirmed rights has been replaced by six original AI-generated editorial scenes. Maintain the visible fictional/illustrative disclosures. No watermarked reference photograph was copied. A future real photographic replacement needs recorded rights and provenance.
4. **GitHub PR:** Git operations use the platform proxy. API access is denied by the current network policy; a PR body is prepared in `pull-request.md`. Do not claim a PR exists unless a successful create result is obtained.
5. **Release:** owner review and explicit approval are required before merging or deploying. No deployment workflow or domain configuration was added or changed. The published cloud environment configuration was not changed or republished.

## Demand-validation next step

Once real form collection is configured, assess consumer concerns by goal, professional interest by discipline/location and common unmet needs. Keep reporting aggregate and purpose-limited, rather than collecting documents or unnecessary personal details. Establish a small follow-up research process with separate permission before promising new capabilities. Phase 1 does not invent conversion metrics, members or demand figures.

## Photographic visual review

See `visual-review.md` for the new architectural hero, property imagery, professional collaboration, diaspora family scene and Nairobi-inspired cityscape, plus responsive-image/performance validation. No application logic was changed in this visual update.
