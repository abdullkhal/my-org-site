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
