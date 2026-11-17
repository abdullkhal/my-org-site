# Further visual and creative review — 17 November 2026

> Historical review snapshot. The current publication candidate and disabled registration state are documented in [launch readiness](launch-readiness.md).

## Design outcome

The website moves from an information-first layout to a property-led editorial identity, while retaining the existing positioning, free initial services, pre-launch limitations and all application logic.

- **Home:** a large cinematic image of contemporary Kenyan-inspired residential architecture. On desktop, a dark forest-green gradient supports the headline and two larger CTAs without losing the stone, glass, light and garden details. On mobile, the image precedes the text so there is no cramped text overlay or tiny action target.
- **Property guidance:** a paired apartment/land composition introduces the practical checklists. These are illustrative contexts, not listings or verification results. The interactive component remains the main task interface.
- **Professional Network:** a collaborative professional scene establishes a human presence; the three proposed benefits move into a calm, full-width row underneath. No people are represented as existing PIIK members.
- **Diaspora:** a relatable couple considering a home replaces the globe. Its crop retains both faces and enough laptop context, while the guidance remains beside it on desktop and below it on mobile.
- **About:** an original Nairobi-inspired cityscape reinforces Kenyan identity and ambition without implying an official affiliation or pretending to be a documentary photograph.
- **Visual rhythm:** warm imagery alternates with clean ivory space and forest-green sections. Button sizing, frame radii, spacing and serif/sans hierarchy are consistent. Checklists, resources and forms remain clear and readable.

## Original imagery and provenance

Six original photorealistic AI-generated editorial scenes were created with OpenAI imagegen specifically for the redesign. The reference photographs were not copied, edited, used as image inputs or stripped of watermarks. The older repository photographs with undocumented rights are not used by the page. The original PIIK logo is preserved.

Each active scene has contextual alternative text and a visible generated/illustrative disclosure. The skyline is explicitly a Nairobi-inspired conceptual illustration. The people, properties and land are fictional; none represents a real available opportunity, PIIK member, client story, verification result or professional endorsement. These are not presented as third-party licensed or documentary photographs.

`assets/imagery/manifest.json` records original file names, dimensions, creation date, provenance and SHA-256 checksums. Original PNG masters, including their generated-file metadata, remain separately preserved and are included in the review’s original-master archive. Only responsive WebP derivatives are committed to the website. `scripts/optimise-images.py` verifies source checksums before reproducing the derivatives; it requires Pillow as a maintenance tool only.

## Responsiveness, accessibility and performance

- Hero: eager loading and high fetch priority; 640, 1024 and 1536px variants.
- Below-fold scenes: lazy loading and asynchronous decoding; 640/1024px variants, with an additional 1536px cityscape for wide displays.
- Explicit `srcset`, `sizes`, intrinsic dimensions and stable frames support correct selection and avoid image-induced layout shifts.
- All images load locally. No new remote font, image host, tracking script, JavaScript library or runtime AI connection is added.
- The main regression suite passes 110 checks, including six viewport widths, navigation, menus, all four checklist categories, reset/print, both local form previews, validation, safe text rendering, zero form requests/storage and no-JavaScript safeguards.
- A separate imagery suite passes 74 checks: all 14 responsive derivatives serve; all six contexts load as needed; desktop, standard-mobile and high-density mobile select appropriate variants; distant imagery is deferred; no old unconfirmed photo is requested; and desktop hero text stays inside its frame at five additional widths.
- Image budgets cover the complete page, not just the first screen: under 1.4MB desktop, 500KB standard mobile, and 950KB high-density mobile. Actual measured transfers are provided with the review artifacts.
- axe-core 4.11.0 reports zero automated WCAG A/AA-tagged violations across all three pages at desktop/mobile sizes. This does not replace manual assistive-technology review.
- The print stylesheet excludes decorative property photography and retains a useful checklist with limitations. No photographic overlay is introduced into printed guidance.

## Retained safeguards and remaining external requirements

`app.js`, `CNAME` and the original logo are unchanged by the visual update. Both interest forms remain honest, local-only previews with no registration claim. All initial PIIK services remain free. No claims of existing members, certifications, official partnerships, transactions or verification capabilities are introduced.

Real submission endpoints and the corresponding data/privacy arrangements still need configuration and testing. Official links remain withheld because they could not be verified through the current network policy. This visual review does not claim those prerequisites have been resolved.

Work remains on `piik-prelaunch-redesign`. No merge, deployment or environment publication is part of this update.

## Review artifacts

`python3 scripts/package-preview.py /path/to/review-output` creates a self-contained three-page preview ZIP with embedded responsive images and preserved security policy hashes. The ZIP was validated over local HTTP for image decoding, guidance, professional response preview, privacy navigation, return navigation and zero external requests. Direct file-URL testing is blocked by the managed browser policy; the archive includes local-server instructions. Full-page desktop/mobile screenshots and section crops, test logs, image-transfer measurements, accessibility results and an original-master archive are supplied separately.
