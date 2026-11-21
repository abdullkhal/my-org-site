# Project 003 baseline audit

21 November 2026. GitHub `main` and the initial clean checkout resolved to `9ac2d2bc79e6331e37a0c19cc927d970a747ffb4`. This is the remote source baseline. The cloud proxy denied HTTPS access to the custom domain. The live version is therefore unconfirmed. Historical release evidence is in [launch-readiness.md](launch-readiness.md).

| Area | Baseline and reuse |
| --- | --- |
| Page inventory | Home, Verify, Directory, Weekly, Watch, Knowledge, Search, About, Terms, Privacy and Credits, plus two articles and 12 educational guides. Two review pages support the inactive enquiry prototype and official-link review. Preserve all these routes and existing anchor handling. |
| Generation and SEO | The Python generator owns editorial routes, titles, descriptions, canonicals, Open Graph, article structured data and the sitemap; three legal/credits pages are handwritten. Search is a static generated index filtered in the browser. Reuse the generator and filters. |
| Presentation and behaviour | `style.css`, `editorial.css`, `app.js` and `editorial.js` provide responsive layout, reduced motion, local checklist state, filter controls and share links. The current browser suites exercise desktop/mobile journeys and axe where supplied. Preserve existing styling and behaviour. |
| Editorial evidence | Existing source, editorial, knowledge and directory JSON support sources, articles, notices, guidance and an empty directory. Some guide records still carry historical draft wording despite already being deployed as general education. Founder-supplied source destinations have limited documented evidence. No edition archive, correction workflow or enforceable evidence contract existed. |
| Collection | The source monitor fingerprints whole pages and probes published links. All seven discovery sources are disabled. The monitor lacks durable candidate deduplication and a failed run prevents its Actions fingerprint cache from saving. |
| Release and data hygiene | Root-branch GitHub Pages uses `CNAME` and `.nojekyll`. CI checks output and compares the release to the custom domain on main pushes. Public repository files, including raw JSON, are public even when absent from search and sitemaps. Keep draft material private. |
| Prior operations | Reviewed the existing editorial runbook, launch and visual reviews, source registry, and Phase 2 verification, handover and deferred-enquiry material. Existing enquiry, analytics and payment posture is inactive. |

Cloud Git authenticated for a read of `main`. GitHub API run listing and the custom-domain connection were denied from this runtime. Browser and accessibility coverage is established by the onboarding baseline and must be rerun against this branch before release.
