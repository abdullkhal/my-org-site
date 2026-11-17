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

## Imagery

- `assets/logo.png`: supplied PIIK logo retained unmodified. `piik-logo.webp` is a trimmed, resized derivative for web display.
- `assets/hero-nairobi.jpg`: supplied Nairobi image, photographer/licence not recorded. `nairobi-preview.webp` is a resized WebP derivative, 1200×900. **Preview only; release blocked pending confirmed rights or replacement.** The preview labels its status and links to `credits.html`.
- Original stock/property images in `assets/` are left untouched, not used by the redesign, and have no newly asserted licences.
- No screenshot/watermarked reference photograph reused.
- UI icons/favicon/globe: original simple SVG/CSS geometry authored for this implementation.
- Fonts: local Georgia and Arial/system fallbacks, no downloads.

External image-source and licence checks could not be completed because Wikimedia API access was denied. A documented licensed Nairobi/property photo is an outstanding release requirement, not an optional cosmetic improvement.
