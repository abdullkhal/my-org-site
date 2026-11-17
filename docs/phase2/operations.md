# Enquiries, privacy and measurement — approval draft

No provider is connected. The public site has no active inputs; `review/enquiries.html` is a disabled visual prototype with synthetic examples. The offline workflow accepts synthetic fixtures only and has no transport/storage adapter. Do not use this prototype as a production handler.

## Recommended first system

Start with a hosted form inbox such as **Formspree**, using its dashboard for restricted enquiry tracking and email for notifications. It fits a static GitHub Pages website and avoids managing a database or paid AI. This is a recommendation to assess, not a verified integration, vendor endorsement or purchase. Current pricing, free-tier volume limits, spam protection, processor terms, data location, subprocessor list, export/deletion and transfer arrangements remain unverified. Do not promise it is free indefinitely.

Alternative: a small serverless endpoint with a private enquiry store and mail delivery. This gives more control but creates maintenance, security, availability and cost responsibilities. Do not introduce it until hosted-provider suitability has been assessed.

## Founder decisions before activation

1. Approve the provider and any cost/plan limit after checking current terms.
2. Confirm the monitored destination mailbox. `info@piikkenya.com` is already displayed on the site, but readiness is unconfirmed. Never put mailbox credentials in code.
3. Confirm PIIK's data controller identity/contact, collection purposes and lawful basis with appropriate Kenyan privacy/legal advice. Review obligations under applicable Kenyan data-protection law, processor contracts, international transfers, rights handling and any registration requirements.
4. Approve the minimum fields and the proposed 90-day post-closure deletion period, including how deletion covers inbox copies and exports. No marketing by default.
5. Approve collection notice, roles and founder-reviewed reply process. Keep consumer/diaspora/professional/general categories separate from mailing-list consent. Expression of interest does not grant membership.

## Prepared process

`data/enquiries.json` defines field limits, categories, statuses and tracking metadata. `data/response-templates.json` holds draft replies, all requiring founder review. `node scripts/enquiry-workflow.cjs` runs an offline synthetic-only demonstration and founder count report. It sends/stores nothing. No real customer records belong in this public Git repository.

After approval, a separate integration must perform **server-side** allowlist validation, length limits, safe output encoding and email-header protection; rate limiting and accessible spam controls; idempotency/retry handling; restricted dashboard access with MFA; privacy-safe logs and deletion; tested acknowledgement, notification, failure and bounce handling. Browser validation is supplemental. Do not store provider secrets in frontend JavaScript. Test with synthetic addresses in a provider-approved sandbox; do not send to random real mailboxes.

Notify the approved mailbox of reference/category/status only; view message content through the protected inbox. Provider default notifications must be inspected and adjusted if they include personal content. Only show success after durable server acceptance; on failure, preserve clear retry guidance without creating a false record. Never include message content in analytics or notification subjects. Assign each real enquiry a unique opaque reference and actual timestamps; synthetic IDs in this demo are deliberately non-production.

Update CSP `form-action`/`connect-src` only for the approved exact provider destinations, update privacy copy, and remove disabled public status cards only after end-to-end and failure tests pass. Require a specific founder approval to open collection. No current CSP permission enables transmission.

## Measurement decision

`data/measurement.json` specifies an inactive aggregate-event plan. There is intentionally no tracking script, listener, collector or persistence in the website. Count visits (not inferred unique people), checklist category/completion, verified resource clicks and server-accepted enquiries. Distinguish internal resource-guide clicks from official outbound links. Collect no answers, query strings, names, identifiers or free text. Avoid session replay and fingerprinting.

Start with a manual synthetic reporting example and assess whether available hosting-level aggregate metrics are sufficient. Hosting may still process IP addresses; “no cookies” does not mean “no personal data”. A later cookieless aggregate provider or first-party endpoint needs founder approval, a current provider/privacy assessment, documented retention and implementation/testing. Do not turn on Google Analytics or third-party scripts by default.

## Formspree integration preparation — current follow-up

`data/formspree.json` now records the proposed provider explicitly, with `enabled: false`, no endpoint and **no chosen business email**. The existing website contact address is not treated as the approved enquiry destination. `scripts/formspree-adapter.cjs` prepares the allowlisted JSON field mapping, category-only notification subject, minimal contact validation, field limits, optional professional fields, honeypot rejection and provider-result handling. It is not loaded by any page, contains no live transport and always rejects its production entry point. The four visual prototypes remain disabled. Native fields have names, limits, required flags and category mappings ready for later integration.

`node tests/integration-preparation.cjs` exercises mocked success, invalid contact/header fields, spam field, unknown categories, oversized content, missing acknowledgement, non-synthetic addresses, rate limits, errors, redirects, malformed responses and timeouts. It uses only `@example.invalid` fixtures, no real account/endpoint and no email delivery. A timeout is treated as unknown receipt, not as permission for automatic retry. The expected `ok:true` JSON contract remains subject to current vendor documentation and an approved synthetic account test. Client-side validation does not establish provider-side enforcement.

### What you will need to approve, in order

1. **Founder-controlled Formspree account and plan.** You retain ownership/recovery access; enable MFA if available. Check current cost/limits, spam features, roles, deletion/export, processor terms and data location. No account or plan has been opened or purchased here. Vendor documentation is also blocked by the development network, so no current capability/price claim is made.
2. **A business mailbox, later.** Choose the monitored address when ready, verify it in the provider and decide who checks it, how quickly and from which devices. No mailbox or fallback destination has been selected. Do not send mailbox passwords to Codex or put them in the website. An endpoint/form ID is public configuration, not a mailbox credential; any private account keys must stay outside frontend code/Git.
3. **A form and its routing.** For the simplest setup, use one approved form/inbox with four sender-selected categories. Confirm the chosen plan supports the required routing, spam and validation controls; otherwise use separate category forms or review another provider before implementation. PIIK's extra tracking fields can start as a simple private review register if vendor dashboard fields are insufficient. Do not promise full case management from a form inbox.
4. **Privacy arrangements.** Identify the legal data controller and a contact for rights requests, explain purposes/lawful basis, required versus optional fields, provider/recipients, retention/deletion including email copies, security and any international processing. Approve processor terms and applicable Kenyan privacy obligations. The proposed 90 days after closure is for your decision, not an activated retention policy. A privacy acknowledgement is not consent to marketing.
5. **Notification and response rules.** Inspect vendor defaults before enabling them. Prefer reference/category/status-only notifications; if that cannot be configured, approve the minimum disclosed content or disable email notifications and review the protected dashboard. Do not claim such redaction is supported until tested. Founder review remains mandatory before replies or sensitive business decisions.
6. **Synthetic account testing, then a separate go-live approval.** Verify receipt, notification, spam/rate limits, server validation, failure/duplicate handling, deletion and access controls with test data. Validate changes to CSP and privacy copy. Only after those checks and explicit activation approval should real public fields and a real endpoint be introduced. Website publication may proceed separately with collection still closed.

The local integration is prepared as far as possible without an account, selected mailbox or approval. No mock result is described as verified Formspree delivery. No real-data endpoint will be activated merely by changing a JSON flag.
