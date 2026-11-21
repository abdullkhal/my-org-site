# PIIK editorial operations

Use a development branch for reviewed changes. GitHub Pages publishes the static files from the repository’s existing Pages configuration. Keep the checked-in HTML and sitemap in sync with their structured sources. The publication remains informational. It does not take payments, broker transactions, publish paid placements or collect enquiries.

## Review and publish

1. Inspect the original source. Save its URL, date, scope and any access limitations. Check terms and robots rules before enabling monitoring for a source. Discuss sensitive allegations privately with the founder. Keep unpublished sensitive material, personal records and private notes off GitHub.
2. Write an original summary. Separate official notices, published data, third-party reporting and PIIK analysis. Recheck all dates, geographical scope and attribution before publication. Use only images and business information that may lawfully be republished.
3. Add the reviewed content to the appropriate data file. Only records with an explicit `approved` status render in Weekly, Watch and the Directory. Each directory profile needs a public business source. Add a separate registration record only if the authority, scope and date were independently checked.
4. Run `python3 scripts/build-site.py` and `python3 scripts/check-links.py`. Review the generated diff, get a passing **Validate PIIK site** run and merge through the permitted repository workflow.
5. Check the resulting **pages build and deployment** run and the **production-smoke** job in **Validate PIIK site**. The smoke job compares the public homepage, service pages and sitemap to the release commit. To restore a prior release, revert the release commits on the publishing branch without rewriting history, and verify the resulting deployment.

## Source review queue

**Review public sources** runs Tuesday and Friday, runs after relevant updates on main, and can also be started manually from GitHub Actions. Download the `piik-source-review` artifact and read `review-queue.json`. A new fingerprint is a review lead and may only reflect a navigation or layout change. Source failures and broken links are recorded in the run log and artifact. Access refusals, unsupported HEAD requests and redirects are inconclusive and should be checked separately. Identical text candidates are deduplicated within each run.

`data/monitoring.json` is the source allowlist. The initial candidates are disabled pending live access and permission checks. The workflow still checks links already in the verification hub. It does not follow redirects or scrape search results, use authenticated endpoints, or publish data. Browser-local search and filtering send no searches to a server.

## Current content and watch list

The launch articles are editorial analyses based on recorded official destinations. The market roundup and individual business profiles require reviewed material. The requested EARB member directory is a candidate at `https://members.estateagentsboard.or.ke/directory`. The existing Gazette link remains the recorded destination. Independently review EBK, NEMA, and county-specific sources before adding public verification links. A technical health probe alone does not verify practising status or the scope of an official service.
