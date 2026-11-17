# Deferred response forms and future integration

**Launch state:** The website now displays two static unavailable-status cards with disabled buttons and no inputs. It contains no enquiry forms or submission-preview JavaScript. Collection is deferred and is not a prerequisite for publishing the informational site.

The following notes describe the earlier review prototype and proposed future integration, not current live functionality. The prototype had two local-only preview forms: `consumer-form` and `professional-form`. Neither has a working endpoint. No response is sent, persisted or registered. Native validation applies; rendering uses `textContent`, never user-controlled HTML. Each form has explicit labels, a separate acknowledgement and an independently cleared preview. JavaScript-disabled users cannot submit or enter responses.

## Structured data contract

A future adapter should explicitly allowlist fields rather than posting arbitrary DOM contents:

- `schema_version`: `1`
- `audience`: `consumer` or `professional`, derived from the form's `data-form-type`
- `name`: optional, max 80 characters
- `email`: optional in this preview, max 254 characters; decide necessity for real follow-up
- `goal` (consumer) or `role` (professional): required enum from the select choices
- `location`: optional country or county, max 100 characters
- `needs`: optional general feedback, max 600 characters
- Future explicit consent records: purpose, choice, notice version and timestamp; do not treat the preview acknowledgement as marketing consent.

These stable identifiers support future validation, routing and carefully scoped AI categorisation. AI is not integrated in Phase 1. Do not send free text to an AI service by default or infer regulatory standing, fraud, verification or creditworthiness from a response.

## Required before live submissions

1. Confirm PIIK's data-controller identity and monitored contact, collection purposes and lawful basis, retention/deletion process, processor arrangements, access controls and cross-border safeguards. Update `privacy.html` with confirmed facts.
2. Configure separate real Formspree endpoints or a suitable backend. Public form endpoint IDs are not secrets, but API keys must never be placed in client-side code. No placeholder endpoint may be treated as working.
3. Add server-side enum, email and length validation, abuse protection/rate limits, output escaping and allowlisted fields. Never enable document uploads or sensitive record collection.
4. Update the restrictive Content Security Policy only for the confirmed HTTPS submission destination (`connect-src` or `form-action` as appropriate); retain the other protections. Implement a small submission adapter in `app.js`: HTTPS POST only, explicit pending/success/error states, timeouts, duplicate prevention and no success on failed or ambiguous responses. Preserve entries on failures. No third-party tracking.
5. Require a consent choice for any optional follow-up distinct from permission to process the requested response. Keep an honest no-JavaScript fallback. Do not enable native GET submissions with personal data in URLs.
6. Test both endpoints using authorised synthetic entries; verify receipt, error paths and deletion. Only then replace “local preview” copy with accurate registration copy.
7. Confirm all initial services stay free; submissions confer no membership, certification or endorsement.

No endpoint can be fabricated or verified using the current access. No personal submissions were sent during development.
