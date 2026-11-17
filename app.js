"use strict";

// No analytics, third-party scripts, storage or remote verification requests.
const guidance = {
  agents: {
    title: "An agent or agency",
    intro:
      "Start with the person, their registration and their authority to act. Advertising a property does not establish any of these.",
    items: [
      [
        "Confirm who you are dealing with",
        "Ask for a full practising name and business details. Cross-check contact details independently, rather than relying only on a social media profile.",
      ],
      [
        "Check the relevant registration",
        "Consult EARB about the agent’s registration and current practising requirements. A company registration is a separate check.",
      ],
      [
        "Ask about authority to act",
        "Have an independent advocate confirm the seller’s or landlord’s identity and the agent’s written authority for the specific property.",
      ],
      [
        "Understand fees before committing",
        "Request written terms, the full fee breakdown and refund conditions. Independently confirm payment instructions before transferring any money.",
      ],
    ],
  },
  property: {
    title: "A property or land opportunity",
    intro:
      "The listing is a starting point. Ownership, boundaries, restrictions and the transaction need their own independent checks.",
    items: [
      [
        "Arrange an independent site visit",
        "Inspect access, location and occupation. Ask a licensed surveyor about boundaries and parcel details where relevant.",
      ],
      [
        "Ask an advocate about official searches",
        "Confirm the appropriate land registry and official search process, including whether Ardhisasa supports the property. Do not rely on a title copy alone.",
      ],
      [
        "Check ownership and authority",
        "Have your advocate examine seller identity, authority to sell, restrictions, charges and any necessary consents or approvals.",
      ],
      [
        "Review the agreement and payment safeguards",
        "Understand the price, taxes, fees, conditions and refund terms. Obtain independent advice before signing or paying a reservation fee or deposit.",
      ],
    ],
  },
  developers: {
    title: "A developer or housing project",
    intro:
      "A polished brochure is not proof of delivery. Check the legal entity, land, approvals and contractual protections independently.",
    items: [
      [
        "Identify the legal entity",
        "Use BRS services to investigate the entity behind the project. Registration alone does not prove investment safety or project legitimacy.",
      ],
      [
        "Check the land and project permissions",
        "Ask an independent advocate to examine land ownership and authority to develop. Confirm applicable planning, building and other approvals with the responsible authorities.",
      ],
      [
        "Look beyond marketing claims",
        "Arrange an independent site visit and professional assessment. Review past delivery claims, timelines and who is responsible for construction and oversight.",
      ],
      [
        "Understand off-plan and payment risks",
        "Have your advocate review milestones, delays, refund terms and payment safeguards. Do not assume a model home or promised return guarantees completion.",
      ],
    ],
  },
  professionals: {
    title: "A property professional",
    intro:
      "Different roles need different checks. Confirm the person’s current standing and whether their expertise matches the work you need.",
    items: [
      [
        "Define the role and scope",
        "Clarify whether you need an advocate, surveyor, valuer, agent or another specialist, and agree the work in writing.",
      ],
      [
        "Check the appropriate official body",
        "For advocates consult LSK; for licensed land surveyors consult the Land Surveyors’ Board; for estate agents consult EARB. For valuers, identify the responsible statutory registration body independently.",
      ],
      [
        "Confirm current status independently",
        "Ask the relevant body about current practising status and scope. A copied certificate, professional title or association logo is not sufficient.",
      ],
      [
        "Agree accountability and fees",
        "Request written engagement terms, fees and timelines. Discuss conflicts of interest and how concerns will be handled before appointing the professional.",
      ],
    ],
  },
};

const checkOutput = document.querySelector("#check-output");
const checklistStates = Object.fromEntries(
  Object.keys(guidance).map((key) => [key, new Set()]),
);
let currentCategory = "agents";

function makeElement(tag, text, className) {
  const el = document.createElement(tag);
  if (text !== undefined) el.textContent = text;
  if (className) el.className = className;
  return el;
}

function updateProgress() {
  const count = checklistStates[currentCategory].size;
  const progress = document.querySelector("#check-progress");
  progress.textContent = `${count} of 4 guidance steps marked as reviewed. ${count === 4 ? "Checklist reviewed — this is not a verification result." : "Reviewed does not mean verified."}`;
}

function renderChecklist(category, announce = false) {
  currentCategory = category;
  const { title, intro, items } = guidance[category];
  checkOutput.replaceChildren();
  checkOutput.append(
    makeElement("p", "PIIK Kenya · Property-check guidance", "print-heading"),
  );
  checkOutput.append(
    makeElement("p", "STEP 2 · EXPLORE YOUR CHECKLIST", "step-label"),
  );
  const heading = makeElement("h3", title);
  heading.id = "check-title";
  checkOutput.append(heading, makeElement("p", intro, "check-intro"));
  const itemList = makeElement("div", undefined, "check-items");
  items.forEach(([label, detail], index) => {
    const row = makeElement("label", undefined, "check-item");
    const box = document.createElement("input");
    box.type = "checkbox";
    box.name = `${category}-step-${index + 1}`;
    box.checked = checklistStates[category].has(index);
    const copy = makeElement("span");
    copy.append(makeElement("strong", label), document.createTextNode(detail));
    row.append(box, copy);
    box.addEventListener("change", () => {
      if (box.checked) checklistStates[category].add(index);
      else checklistStates[category].delete(index);
      updateProgress();
    });
    itemList.append(row);
  });
  const progress = makeElement("p", "", "progress-copy");
  progress.id = "check-progress";
  progress.setAttribute("role", "status");
  const actions = makeElement("div", undefined, "check-actions");
  const hubLink = makeElement("a", "Explore official resources →", "text-link");
  hubLink.href = "#official-hub";
  const reset = makeElement("button", "Reset this checklist", "reset-link");
  reset.type = "button";
  reset.addEventListener("click", () => {
    checklistStates[currentCategory].clear();
    checkOutput.querySelectorAll('input[type="checkbox"]').forEach((input) => {
      input.checked = false;
    });
    updateProgress();
  });
  const print = makeElement("button", "Print checklist", "reset-link");
  print.type = "button";
  print.addEventListener("click", () => window.print());
  actions.append(hubLink, reset, print);
  checkOutput.append(itemList, progress, actions);
  updateProgress();
  if (announce)
    document.querySelector("#category-status").textContent =
      `${title} guidance loaded. Four steps to explore. Guidance only, not verification.`;
}

if (checkOutput) {
  document.body.classList.add("js");
  const categoryStatus = makeElement("div", "", "sr-only");
  categoryStatus.id = "category-status";
  categoryStatus.setAttribute("role", "status");
  checkOutput.before(categoryStatus);
  document.querySelectorAll('[name="check-category"]').forEach((input) => {
    input.addEventListener("change", () => renderChecklist(input.value, true));
  });
  renderChecklist("agents");
}

const menuToggle = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#main-navigation");
if (menuToggle && navigation) {
  menuToggle.hidden = false;
  function closeMenu(returnFocus = false) {
    navigation.classList.remove("is-open");
    menuToggle.setAttribute("aria-expanded", "false");
    if (returnFocus) menuToggle.focus();
  }
  menuToggle.addEventListener("click", () => {
    const expanded = menuToggle.getAttribute("aria-expanded") === "true";
    menuToggle.setAttribute("aria-expanded", String(!expanded));
    navigation.classList.toggle("is-open", !expanded);
  });
  navigation
    .querySelectorAll("a")
    .forEach((link) => link.addEventListener("click", () => closeMenu()));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && navigation.classList.contains("is-open"))
      closeMenu(true);
  });
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".site-header")) closeMenu();
  });
}

// Online enquiries and registration are intentionally unavailable for launch.
// Do not enable collection until a real endpoint and privacy arrangements are tested.
const year = document.querySelector("#year");
if (year) year.textContent = String(new Date().getFullYear());
