# Project 003 roadmap

Work in order. Enable dependent public features after the previous phase passes its local gate. External execution, deployment and scheduling require independent evidence.

| Phase | Priority and dependencies | Completion gate |
| --- | --- | --- |
| 1. Foundation | Audit, operating rules, versioned content validation and source registry | Audit recorded, baseline pages pass, approved records have evidenced gates and monitoring policy is explicit |
| 2. Monitoring | Phase 1 plus accessible, permitted public sources | Candidate and deduplication tests pass, partial failures preserve prior state, a real approved source is collected, Actions execution is evidenced |
| 3. Editorial and publishing | Phase 2 and reviewed evidence | Approved-only rendering, correction and withdrawal, edition archive, search, sharing and feed pass. Publish a first edition when the evidence supports it |
| 4. Directory | Phase 3 and independently reviewed organisational sources | Evidence and duplicate checks, searchable profiles, review dates and disclaimers. Aim for 10–20 eligible profiles |
| 5. Quality and operations | Previous phases and repository permissions | Mobile/accessibility, integrity, founder report, CI, deployment and rollback evidence. Separately verify any recurring AI execution |

## Checkpoint

The baseline and initial risks are in [the audit](docs/project-003-audit.md). See [the changelog](docs/CHANGELOG.md) for implementation and verification evidence.

- Phase 1 local gate passed. Verification of candidate research destinations remains source-by-source.
- Phase 2 implementation and fixture tests passed. The real-source and hosted-schedule gates are open. Activate individual sources only after permission, access and first-party evidence review.
- Phase 3 is staged on the development branch. Local publication, withdrawal, archive, RSS and search tests passed. The first edition and any new notices await reviewed evidence. Keep public activation behind the Phase 2 gate.
- Phase 4 is staged and passed local profile and duplicate tests. Add the initial organisational profiles after direct first-party review.
- Phase 5 local health and executive report passed. The [hosted branch validation](https://github.com/abdullkhal/my-org-site/actions/runs/44925385081) passed for the publishing implementation. A disposable revert restored the exact baseline tree. The cloud proxy blocked GitHub API access to open the draft pull request. Resume with a permitted source review and the authorised pull request path. Verify the deployed SHA and scheduled runs after release. Recurring Codex entitlement and execution remain unverified.
