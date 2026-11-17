"use strict";
// Offline planning module. No network, filesystem writes, notifications or live intake.
const policy = require("../data/enquiries.json");
const templates = require("../data/response-templates.json").templates;
function prepareSyntheticEnquiry(input) {
  if (input.synthetic !== true || !input.email?.endsWith("@example.invalid")) {
    throw new Error("This prototype accepts synthetic @example.invalid fixtures only");
  }
  if (!policy.categories.includes(input.category)) throw new Error("Unknown category");
  for (const field of ["name", "email", "message"]) {
    if (typeof input[field] !== "string" || !input[field].trim() || input[field].length > policy.fields.limits[field]) throw new Error(`Invalid ${field}`);
  }
  if (input.privacy_acknowledged !== true) throw new Error("Synthetic privacy acknowledgement required");
  const sensitive = /fraud|legal|refund|identity|title deed|bank|complaint|threat|payment/i.test(input.message);
  const template = templates.find(t => t.id === (sensitive ? "sensitive-escalation" : input.category === "professional" ? "professional-interest" : input.category === "general" ? "general" : `${input.category}-guidance`));
  return {
    enquiry_id: `SYNTHETIC-${input.category.toUpperCase()}`,
    category: input.category, // Sender-selected; future suggestions never override it silently.
    status: "needs_founder_review",
    sensitive,
    owner: "founder",
    notification_draft: {subject: `PIIK review: ${input.category}`, category: input.category, status: "needs_founder_review"},
    response_draft: template.text,
    requires_founder_review: true,
    sent: false,
    stored: false,
  };
}
function acceptLiveEnquiry() { throw new Error("Personal-data collection is disabled pending founder approval and secure integration"); }
module.exports = { prepareSyntheticEnquiry, acceptLiveEnquiry };
if (require.main === module) {
  const records = policy.categories.map(category => prepareSyntheticEnquiry({synthetic:true,category,name:"Example Person",email:"review@example.invalid",message:"Synthetic guidance request",privacy_acknowledged:true}));
  console.log(JSON.stringify({mode:"offline-synthetic-only",records,founder_report:{total:records.length,by_category:Object.fromEntries(records.map(r => [r.category,1])),awaiting_review:records.length,sent:0}},null,2));
}
