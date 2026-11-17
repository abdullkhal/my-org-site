# PIIK Kenya — ready for approval to publish

Scope: a small launch-readiness pass on the approved `piik-prelaunch-redesign` branch. No rebuild, new operational service, hosting migration, merge or deployment.

## Candidate behaviour

- Approved design, original imagery/provenance, logo, domain and pre-launch positioning preserved.
- All four interactive property-guidance categories remain usable, including keyboard selection, per-category state, reset and clean print output.
- The two non-submitting enquiry previews are removed. Their anchor destinations remain as clearly labelled status cards with disabled buttons, no personal-information inputs and no form or submission code. They cannot be enabled accidentally by page JavaScript.
- Network CTA and footer labels now lead honestly to registration information/status. Privacy information reflects the disabled launch state.
- No payments, document uploads, claimed certifications, members or official partnerships introduced.
- Official links remain withheld pending verification; this is a disclosed content limitation, not a broken outbound-link dependency.

## Deployment evidence

Read-only inspection of GitHub's public Actions history confirms the repository uses GitHub Pages' managed `pages build and deployment` workflow on `main`.

Latest visible successful run:
https://github.com/abdullkhal/my-org-site/actions/runs/25317136442

The run summary identifies commit `6754a85ffd6d0589f5ea78036ec74064471f8af8` on `main`, a successful build and deploy, and destination **https://piikkenya.com/**. This is also the current remote `main` commit when checked on 17 November 2026. Root `CNAME` remains byte-for-byte unchanged as `piikkenya.com`; `main` has only a root-level static website and no checked-in custom deployment workflow. The redesign needs no package install or build command.

The latest visible deployment is historical (4 May 2026), not a newly executed validation. Live HTTP/HTTPS requests to the domain, the GitHub Pages origin, DNS resolution and the GitHub Pages API/settings are unavailable from this environment. Direct HTTPS requests to the live domain/API are denied by the outbound network policy. GitHub's public workflow/run pages are accessible and supplied the deployment evidence above. Do not claim current live-domain health or a new deployment from these observations.

## Approval and publication sequence

1. Await the owner's explicit **“Approve merge and publish”** instruction. The approved visual design alone is not publication permission.
2. Recheck the remote `main` and redesign heads and confirm the reviewed candidate still contains the launch fixes. If `main` has advanced, inspect the changes before proceeding.
3. Fast-forward `main` to the prepared redesign commit if the ancestry still permits it, using a normal non-forced Git update. If branch protection requires a PR, use the repository's required review/merge route instead. Do not change domain, DNS or Pages publishing settings.
4. Watch the existing managed Pages workflow created by that `main` update. Verify the run targets the exact published commit, build/deploy complete successfully and the reported destination remains piikkenya.com.
5. Verify the published headline, CSS/JS and images, mobile navigation, checklist interactions, disabled registration notices and privacy link through the live domain when network access permits. Report any access limitation separately from deployment success.

A successful push or merge is not proof that Pages has deployed. If publishing fails, inspect that run and correct only the concrete publishing issue; do not start Phase 2 or change hosting. The previous live source commit above is the rollback reference; any public rollback still requires appropriate user authorization.

## Deferred operational work

Real enquiry/registration endpoints, data-protection arrangements, verified official links and network operations can be completed later. They do not block publishing this honest, informational pre-launch website with registration disabled.

Current-candidate validation passed: **103 functional/browser checks and 74 imagery checks**. Automated axe-core audits report zero WCAG A/AA-tagged violations on all three pages at desktop/mobile widths. JavaScript syntax, whitespace, domain/logo preservation and fast-forward ancestry checks passed. The site remains on the redesign branch until approval. See the accompanying browser/image test logs and desktop/mobile screenshots.
