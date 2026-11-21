"use strict";

const navToggle = document.querySelector(".editorial .menu-toggle");
if (navToggle) document.body.classList.add("js");

const legacyAnchors = {
  "piik-check": "verify.html", "official-hub": "verify.html",
  knowledge: "knowledge.html", diaspora: "knowledge.html",
  about: "about.html", network: "about.html", feedback: "about.html",
  "professional-form": "about.html",
};
if (/\/(index\.html)?$/.test(location.pathname)) {
  const anchor = location.hash.slice(1);
  let page = Object.hasOwn(legacyAnchors, anchor) ? legacyAnchors[anchor] : "";
  if (anchor.startsWith("resource-")) page = "verify.html";
  if (anchor.startsWith("guide-")) page = "knowledge.html";
  if (page) location.replace(page + location.hash);
}

const homeSearch = document.querySelector("[data-home-search]");
if (homeSearch) {
  const homeQuery = homeSearch.querySelector("input");
  const submitSearch = () => {
    const query = homeQuery.value.trim();
    location.assign(query ? "search.html#" + new URLSearchParams({ q: query }) : "search.html");
  };
  homeSearch.hidden = false;
  homeSearch.querySelector("button").addEventListener("click", submitSearch);
  homeQuery.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.isComposing) submitSearch();
  });
}

for (const tools of document.querySelectorAll("[data-filter]")) {
  const query = tools.querySelector("input");
  const category = tools.querySelector("[data-category]");
  const place = tools.querySelector("[data-place]");
  const count = tools.querySelector(".result-count");
  const cards = Array.from(document.getElementById(tools.dataset.filter + "-results").querySelectorAll("[data-result]"));
  const normalize = (value) => value.normalize("NFKC").toLocaleLowerCase("en-KE");
  const searchable = cards.map((card) => ({
    card,
    text: normalize(card.textContent + " " + (card.dataset.search || "")),
  }));
  const update = () => {
    const terms = normalize(query.value).split(/\s+/).filter(Boolean);
    let matches = 0;
    for (const { card, text } of searchable) {
      const visible = terms.every((term) => text.includes(term)) &&
        (!category?.value || card.dataset.category === category.value) &&
        (!place?.value || card.dataset.place === place.value);
      card.hidden = !visible;
      if (visible) matches += 1;
    }
    count.textContent = matches ? `${matches} ${matches === 1 ? "result" : "results"}` : "No matching results";
  };
  if (tools.dataset.filter === "site-search") {
    query.value = new URLSearchParams(location.hash.slice(1)).get("q") || "";
  }
  query.addEventListener("input", update);
  category?.addEventListener("change", update);
  place?.addEventListener("change", update);
  tools.hidden = false;
  if (cards.length) update();
}

for (const button of document.querySelectorAll("[data-copy]")) {
  const status = button.parentElement.querySelector("[role=status]");
  button.hidden = false;
  button.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      status.textContent = "Link copied.";
    } catch {
      status.textContent = "Copy the address from your browser’s address bar.";
    }
  });
}
