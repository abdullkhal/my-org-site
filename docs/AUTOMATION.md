# Automation and specialist roles

Each role uses repository instructions and release-safe evidence. Run deterministic stages with GitHub Actions and standard-library tools. Use Codex in the editorial session when judgement is needed.

| Role | Inputs | Outputs and authority | On failure |
| --- | --- | --- | --- |
| Research and discovery | Approved registry and prior collection state | Rate-limited candidate report; read-only external access | Retain prior fingerprints, report access limits |
| Evidence and verification | Original evidence and related records | Review notes, scope and disposition; no live publishing | Hold disputed, missing or sensitive evidence for human review |
| Editorial intelligence | Reviewed evidence and guides | Original draft, edition and share wording; approval only within policy | Keep insufficient or sensitive material private |
| Directory research | Public organisational pages and applicable authorities | Reviewable profile and scope of any official check | Omit unsupported fields or hold the profile |
| Publishing | Approved records, templates and passing validation | Static pages, RSS, search, sitemap and permitted release | Stop before merge or revert a defective release |
| Quality and operations | Local tests, deployment and source reports | Website health and one executive report; no source promotion | Escalate consolidated exceptions, retain working release |

No recurring Codex or ChatGPT editorial entitlement has been verified in this environment. The weekly Codex command is the manual editorial handoff. GitHub Actions can collect and validate deterministically.

## Collection schedule and evidence

**Review public sources** defines daily collection at 06:25 UTC, a Saturday collection and link review at 06:40 UTC, and a monthly registry and link review at 06:55 UTC on the first. Its manual run accepts any of the three modes.

The workflow retains a small rolling candidate queue and source fingerprints. It stores links, dates and identifiers only. Candidates are leads. A changed index, an HTTP response and official factual review have separate meanings. The cache can expire and recreate a baseline. Check the latest successful run and artifact before the weekly cycle. A missed run or missing artifact is an operations exception.

Enable a source only after documenting first-party identity, robots and site terms, reviewing the actual public index or feed, and setting its path prefix and latest successful check. Current sources remain pending or reference-only. The cloud proxy denied the known launch destinations, so this session verified collection and failure handling with fixtures and ran the production configuration in inactive mode. GitHub schedule execution for the replacement workflow remains unconfirmed.

## Founder report

The weekly workflow queues the same evidence for review, checks generated pages and links, compares the checked-out primary routes with the public release, and writes one executive report to the run summary and the same artifact. For a local rehearsal, use a current queue outside the checkout.

```sh
python3 scripts/operations-report.py \
  --queue /tmp/piik-review/review-queue.json \
  --output /tmp/piik-review/executive-report.md
```

Append `--live` when the custom domain is reachable. A blocked response is inconclusive, and a comparison is meaningful only against the release currently intended to be live. An inactive Actions schedule requires checking the last run in GitHub because a stalled schedule cannot generate its own exception report.
