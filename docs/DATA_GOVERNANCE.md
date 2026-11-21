# Data governance

The public repository is the canonical store of release-safe records. `data/sources.json` holds verification destinations, `data/monitoring.json` holds research sources, `data/editorial.json` holds articles, notices, editions and corrections, `data/knowledge.json` holds guides, and `data/directory.json` holds organisational profiles. The generator derives HTML, indexes and feeds from these files.

Keep candidate reports and unsanitised drafts outside the checkout. GitHub Pages may make raw files accessible even when excluded from robots or search. Store no credentials, private contact details, personal documents, customer records or unreviewed allegations in Git or routine workflow artifacts. Record source references and short factual evidence notes. Organisation websites and business contact channels require public provenance; exclude personal details and copied registers. Apply minimal retention to monitoring and reporting artifacts.

Use stable lowercase identifiers and ISO calendar dates. Record unknown source and event dates explicitly where applicable. Preserve content IDs for corrections and withdrawals. Retain historical review scope and never substitute a connectivity check for factual review.

For new approved articles, notices, guides and profiles, include `review` with `reviewer`, `evidence`, `limitations`, `discovered_at`, `reviewed_at`, `updated_at` and `sources`. Each source names the original organisation, URL and source publication date (or null). Keep the PIIK publication date separate. The exact legacy content retains its historical approval scope. Editing it requires the normal evidence gate.

Editions reference approved articles with reviewed evidence and name the editor and review date. Corrections reference a stable public record ID. For withdrawal, retain only `id` and `status: withdrawn` in the target and add a dated, reviewed, release-safe correction. Update any dependent edition, notice or guide references before generating.
