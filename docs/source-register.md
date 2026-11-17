# Official-source and image register — current status

Recorded review: **17 November 2026**. The authoritative structured register is [`data/sources.json`](../data/sources.json); the [current clickable link table](phase2/official-websites.md) lists all supplied destinations, resource types and limitations.

Nine URLs covering eight authorities have been accepted from the founder’s independent research and enabled in the local Phase 2 hub. Evidence records clearly identify the founder as the source, not an automated page-content or current-status verification. The founder’s original research date was not supplied. All nine current retrieval attempts returned proxy CONNECT 403; this is separate from the accepted destination research and does not establish an outage.

The EARB link is a dated 2026 Gazette publication. LSK links to FAQ guidance; LSB and the two BORAQS pages are register destinations, not assumed to be live practising-status services. BRS and VRB homepages are gateways. Ardhisasa provides the route to supported land services; NCA’s contractor page is separate from project/county approval.

**Discrepancy:** the original checklist had ten candidate authorities. The founder supplied nine URLs for eight authorities because BORAQS has separate architect and quantity-surveyor pages. EBK and NEMA therefore both remain pending; county approvals remain property-specific. The earlier EARB, LSB, VRB and BORAQS candidate domains were superseded by the founder’s researched destinations. Original candidate URLs remain in the structured history.

The material below is historical Phase 1 evidence, not the current active-link list. Old network restrictions and references to visible image labels or master-file locations describe that earlier work. Current images, logo and CNAME remain unchanged.

---

# Source and image register

Checked: 17 November 2026. Runtime outbound proxy denied the candidate destinations below with HTTP CONNECT 403. This is an environment-policy limitation, not evidence that an official service is down or that a candidate URL is authoritative. No direct official links have been shipped in the UI.

| Intended body/service         | Candidate URL (not independently verified) | Current result         |
| ----------------------------- | ------------------------------------------ | ---------------------- |
| EARB                          | https://earb.go.ke/                        | Network policy blocked |
| Ardhisasa                     | https://ardhisasa.lands.go.ke/             | Network policy blocked |
| Law Society of Kenya          | https://lsk.or.ke/                         | Network policy blocked |
| Land Surveyors' Board         | https://lsb.or.ke/                         | Network policy blocked |
| Business Registration Service | https://brs.go.ke/                         | Network policy blocked |

Do not assume these are confirmed destinations. Use first-party government/regulator references to corroborate identity; follow HTTPS redirects and check the precise register/service page, login and fee requirements before adding links. The five homepage cards intentionally have no dead or misleading “visit” buttons. Update the homepage hub notice, source cards, privacy notice and credits together when verification is completed.

## Active imagery — original generated editorial artwork

All six active editorial images were created with OpenAI imagegen on 17 November 2026 for this redesign. They are original photorealistic illustrations, not licensed third-party photography. No reference photograph was copied, extracted, edited or passed as an image-generation input. The watermarked screenshots informed art direction only.

| Image           | Intended use                | Disclosure                                             |
| --------------- | --------------------------- | ------------------------------------------------------ |
| `residence`     | Cinematic home hero         | AI-generated architecture; not a listing               |
| `apartments`    | PIIK Check property context | Fictional development, no availability implied         |
| `land`          | PIIK Check land context     | Fictional landscape, no parcel/boundary assertion      |
| `collaboration` | Professional Network        | Fictional people, not existing PIIK members            |
| `diaspora`      | Diaspora Property Hub       | Fictional couple, not a client story                   |
| `skyline`       | About/national identity     | Nairobi-inspired conceptual cityscape, not documentary |

The manifest `assets/imagery/manifest.json` records generated master filenames, SHA-256 checksums, dimensions, creation dates and derivative widths. Original PNG masters remain in `/workspace/generated_images` and are provided separately in the review archive. Check each checksum before rebuilding. `scripts/optimise-images.py` produces 640/1024px WebP variants, plus 1536px for the hero and cityscape. Do not assert exclusive copyright or real-world identity from generated artwork.

All editorial images have contextual alternative text and visible generated/illustrative captions. The hero is eager/high-priority; below-fold photos are lazy and asynchronously decoded. Responsive `srcset`/`sizes`, intrinsic dimensions and stable frames prevent downloading unnecessarily large variants or shifting layouts. All assets load locally; no image host or tracker is contacted.

The original PIIK logo is unchanged; its cropped WebP derivative is retained. Original repository photographs are preserved but unused by the redesigned website, and no licence is asserted for them. The former `nairobi-preview.webp` derivative has been removed from active use. UI icons/favicon are original SVG; fonts are local system fonts.

The generated editorial option resolves the earlier active-image provenance blocker without claiming that a third-party stock licence was verified. A future owner-supplied real property or documentary Nairobi photograph still requires a recorded source and appropriate rights before use.
