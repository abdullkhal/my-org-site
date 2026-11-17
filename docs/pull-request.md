Replaces the certification-led homepage with a free, independent pre-launch property-integrity website for PIIK Kenya. Adds four tailored property-guidance checklists, consumer/professional/diaspora journeys, educational guides, official-resource explanations and separate local-only response previews. Preserves the original PIIK logo and CNAME.

The forest-green, gold and ivory redesign uses plain HTML/CSS/JavaScript, local system fonts, original SVG icons and optimised WebP display assets. Adds responsive navigation, keyboard support, print guidance, SEO metadata, a restrictive Content Security Policy and privacy/source-status pages.

Validation: 104 Playwright/Chromium assertions passed across six viewport widths; axe-core reports zero automated WCAG A/AA-tagged violations on all three pages at desktop/mobile sizes. JavaScript syntax and whitespace checks passed. Tested forms send and store nothing; they are not registrations.

Review requirements before release:

- Configure and test real submission endpoints and the corresponding privacy/consent arrangements.
- Verify official links when network access permits; direct links are currently withheld.
- Confirm rights to the existing Nairobi photo or replace it with a documented licensed image. It is labelled as review-only.

No payments, claimed certifications, established memberships, partnerships or AI verification are introduced. No merge, live deployment or domain changes are authorised by this PR. See `docs/review.md` for the detailed results and limitations.
