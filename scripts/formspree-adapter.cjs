"use strict";
// Prepared provider contract only. Never loaded into the website.
// Transport is injected by tests; this module does not call fetch or send mail.
const policy = require("../data/enquiries.json");
const config = require("../data/formspree.json");
const allowed = new Set(["category", "name", "email", "message", "role", "service_area", "privacy_acknowledged", "_gotcha"]);
function validatePayload(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) throw new Error("Invalid enquiry");
  if (Object.keys(input).some(k => !allowed.has(k))) throw new Error("Unsupported field");
  if (!policy.categories.includes(input.category)) throw new Error("Choose an enquiry category");
  for (const field of ["name", "email", "message"]) {
    if (typeof input[field] !== "string" || !input[field].trim() || input[field].length > policy.fields.limits[field]) throw new Error(`Invalid ${field}`);
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.email) || /[\r\n]/.test(input.name+input.email)) throw new Error("Invalid contact fields");
  if (input.privacy_acknowledged !== true) throw new Error("Read the collection notice before submitting");
  if (input._gotcha !== undefined && input._gotcha !== "") throw new Error("Submission rejected");
  const payload = {
    category: input.category,
    name: input.name.trim(), email: input.email.trim(), message: input.message.trim(),
    privacy_acknowledged: true, _gotcha: "",
    _subject: `PIIK ${input.category} enquiry`, // Fixed category only, never user content.
  };
  for (const field of ["role", "service_area"]) {
    if (input[field] !== undefined) {
      if (input.category !== "professional" || typeof input[field] !== "string" || input[field].length > policy.fields.limits[field]) throw new Error(`Invalid ${field}`);
      if (input[field].trim()) payload[field] = input[field].trim();
    }
  }
  return payload;
}
async function submitSynthetic(input, transport) {
  const payload = validatePayload(input);
  if (!payload.email.endsWith("@example.invalid")) throw new Error("Use synthetic @example.invalid addresses only");
  if (typeof transport !== "function") throw new Error("An offline mock transport is required");
  // No real endpoint is passed, even if a mock is accidentally replaced with fetch.
  const request = { method: "POST", headers: {Accept: "application/json", "Content-Type": "application/json"}, body: JSON.stringify(payload) };
  try {
    const response = await transport({url: null, provider: "Formspree", synthetic: true, request});
    if (!response || response.ok !== true || !Number.isInteger(response.status) || response.status < 200 || response.status > 299) {
      return {accepted:false, status:response?.status===429 ? "rate_limited" : "delivery_failed", retry: "Review before retrying; do not assume the enquiry was received."};
    }
    const body = await response.json();
    if (body?.ok !== true) return {accepted:false,status:"unconfirmed",retry:"Receipt was not confirmed. Check before retrying."};
    return {accepted:true,status:"synthetic_accepted",requires_founder_review:true,sent:false,stored:false};
  } catch {
    // A timeout may follow provider acceptance: don't retry automatically or promise failure.
    return {accepted:false,status:"unconfirmed",retry:"Receipt is unknown. Check before retrying to avoid duplicates."};
  }
}
function submitLive() {
  // Intentionally no production escape hatch. An approved integration is separate work.
  throw new Error(`Live collection disabled (configured enabled=${config.enabled}); provider, mailbox and privacy approval required`);
}
module.exports = { validatePayload, submitSynthetic, submitLive };
