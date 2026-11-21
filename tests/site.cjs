"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");
const sources = require("../data/sources.json").sources;
const profiles = require("../data/directory.json").profiles.filter(profile => profile.status === "approved");

const base = process.env.PIIK_TEST_URL || "http://127.0.0.1:3000";
const output = process.env.PIIK_TEST_OUTPUT || "/tmp/piik-publication";
const executablePath = process.env.PIIK_CHROMIUM || "/usr/bin/chromium";
const axe = process.env.PIIK_AXE_PATH;
const routes = ["/", "/verify.html", "/directory.html", "/weekly.html", "/watch.html", "/knowledge.html"];
let checks = 0;

function check(value, description) {
  assert.ok(value, description);
  checks += 1;
  console.log("PASS " + description);
}

async function main() {
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ executablePath, args: ["--no-sandbox"] });
  const context = await browser.newContext({ permissions: ["clipboard-read", "clipboard-write"] });
  const page = await context.newPage();
  const errors = [];
  const requests = [];
  page.on("pageerror", error => errors.push(error.message));
  page.on("console", message => { if (message.type() === "error") errors.push(message.text()); });
  page.on("request", request => requests.push([request.method(), request.url()]));

  try {
    for (const width of [320, 390, 768, 1024, 1440]) {
      await page.setViewportSize({ width, height: width < 768 ? 844 : 960 });
      for (const route of routes) {
        const response = await page.goto(base + route);
        check(response.ok() && await page.locator("h1").count() === 1, `${route} renders at ${width}px`);
        check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${route} fits ${width}px`);
      }
      await page.goto(base);
      const hero = page.locator(".hero-photo img");
      await hero.evaluate(img => img.decode());
      check(await hero.evaluate(img => img.naturalWidth > 0), `responsive hero decodes at ${width}px`);
      if (width === 390 || width === 1440) {
        await page.evaluate(async () => {
          await Promise.all([...document.images].map(async image => {
            image.loading = "eager";
            await image.decode();
          }));
        });
        await page.screenshot({ path: path.join(output, width === 390 ? "homepage-mobile.png" : "homepage-desktop.png"), fullPage: true });
      }
    }
    check((await page.locator("h1").innerText()).replace(/\s+/g, " ") === "Know before you commit.", "approved homepage headline");
    check(await page.locator(".service-grid a").count() === 4, "four primary services");
    check(await page.locator("#main-navigation a").count() === 6, "six primary navigation destinations");
    const imageBytes = await page.evaluate(() => performance.getEntriesByType("resource")
      .filter(entry => new URL(entry.name).pathname.endsWith(".webp"))
      .reduce((sum, entry) => sum + entry.encodedBodySize, 0));
    check(imageBytes > 0 && imageBytes < 650_000, `homepage WebP transfer is within 650 KB (${imageBytes} bytes)`);
    await page.locator("#home-query").fill("estate agents");
    await page.locator("#home-query").press("Enter");
    await page.waitForURL("**/search.html#*");
    check(await page.locator("#site-search").inputValue() === "estate agents", "homepage search carries the query");
    check(await page.locator("#site-search-results [data-result]:visible").count() > 0, "site search returns relevant results");
    await page.locator("#site-search").fill("<img src=x onerror=alert(1)>");
    check(await page.locator("#site-search-results [data-result]:visible").count() === 0, "search treats injected markup as text");

    await page.goto(base + "/#official-hub");
    await page.waitForURL("**/verify.html#official-hub");
    check(await page.locator(".resource-card").count() === sources.length, "old verification link leads to every retained authority");
    await page.locator("#official-search").fill("quantity surveyors");
    check(await page.locator("#resource-boraqs").isVisible() && !await page.locator("#resource-earb").isVisible(), "verification results filter by profession");
    await page.locator("#resource-boraqs summary").click();
    check(await page.locator("#resource-boraqs details").getAttribute("open") !== null, "access and limitations expand");
    await page.locator("#official-search").clear();
    for (const name of ["agents", "property", "developers", "professionals"]) {
      await page.locator(`.category:has(input[value="${name}"])`).click();
      const boxes = page.locator("#check-output input");
      check(await boxes.count() === 4, `${name} has four checklist steps`);
      await boxes.first().check();
      check((await page.locator("#check-progress").textContent()).startsWith("1 of 4"), `${name} tracks checklist progress`);
      await page.getByRole("button", { name: "Reset this checklist" }).click();
      check(!await boxes.first().isChecked(), `${name} checklist resets`);
    }
    await page.emulateMedia({ media: "print" });
    check(await page.locator(".print-heading").isVisible() && !await page.locator(".page-intro").isVisible(), "print layout includes checklist and excludes introduction");
    await page.emulateMedia({ media: "screen" });

    await page.goto(base + "/directory.html");
    check(await page.locator("#directory-search-results [data-result]").count() === profiles.length, "directory renders only approved profiles");
    check(await page.locator(".register-links a").count() >= 6, "directory links to independent professional discovery");
    const directory = await page.content();
    const fixtures = [
      ["Example architects", "Architects", "Nairobi", "Planning and design"],
      ["Example contractors", "Contractors", "Nairobi", "Construction"],
      ["Example coast architects", "Architects", "Kilifi", "Planning and design"],
    ];
    const snippet = fixtures.map(([name, category, place, summary]) =>
      `<article data-result data-category="${category}" data-place="${place}"><h3>${name}</h3><p>${summary}</p></article>`
    ).join("");
    const fixtureRoute = base + "/directory-fixture.html";
    await page.route(fixtureRoute, route => route.fulfill({
      contentType: "text/html",
      body: directory.replace(/(<div class="editorial-grid" id="directory-search-results">)[\s\S]*?(<\/div>)/, "$1" + snippet + "$2")
        .replace('<option value="">All locations</option>', '<option value="">All locations</option><option>Nairobi</option><option>Kilifi</option>'),
    }));
    await page.goto(fixtureRoute);
    await page.locator("select[data-category]").selectOption("Architects");
    check(await page.locator("#directory-search-results [data-result]:visible").count() === 2, "directory category filter works with synthetic records");
    await page.locator("select[data-place]").selectOption("Kilifi");
    check(await page.locator("#directory-search-results [data-result]:visible").count() === 1, "directory category and location filters combine");
    await page.locator("#directory-search").fill("construction");
    check(await page.locator("#directory-search-results [data-result]:visible").count() === 0, "directory search combines with both filters");

    await page.goto(base + "/weekly.html");
    await page.locator("#article-search").fill("regulation");
    const story = page.locator('#article-search-results [data-result]:visible a[href="article-estate-agent-gazette.html"]');
    check(await story.isVisible(), "property news archive filters by category");
    await story.click();
    check((await page.getAttribute('meta[property="og:type"]', "content")) === "article", "article has sharing metadata");
    check(await page.getByRole("link", { name: "Share on WhatsApp" }).getAttribute("href").then(href => href.startsWith("https://wa.me/?text=")), "WhatsApp uses a normal share link");
    await page.getByRole("button", { name: "Copy link" }).click();
    await page.waitForFunction(() => document.querySelector(".share-tools [role=status]").textContent === "Link copied.");
    check((await page.evaluate(() => navigator.clipboard.readText())).includes("https://piikkenya.com/article-"), "clipboard uses the canonical article URL");
    await page.locator('a[href="guide-agents.html"]').click();
    check((await page.locator("h1").textContent()).includes("Choose the person"), "related standalone knowledge guide works");

    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(base);
    const menu = page.getByRole("button", { name: "Menu" });
    await menu.click();
    check(await page.getByRole("navigation", { name: "Main navigation" }).isVisible(), "mobile menu opens");
    await page.keyboard.press("Escape");
    check(!await page.getByRole("navigation", { name: "Main navigation" }).isVisible(), "Escape closes the mobile menu");
    check(await menu.evaluate(element => element === document.activeElement), "menu focus is restored");

    const plain = await browser.newContext({ javaScriptEnabled: false });
    const plainPage = await plain.newPage({ viewport: { width: 390, height: 844 } });
    await plainPage.goto(base);
    check(await plainPage.getByRole("navigation", { name: "Main navigation" }).isVisible(), "mobile navigation works without JavaScript");
    await plainPage.getByRole("link", { name: "Start a check" }).click();
    check(await plainPage.locator("#resource-earb").isVisible(), "official links work without JavaScript");
    await plain.close();

    if (axe) {
      for (const route of [...routes, "/article-estate-agent-gazette.html", "/guide-agents.html", "/search.html"]) {
        await page.goto(base + route);
        const results = await page.evaluate(async source => {
          const run = new Function(source + "\nreturn axe.run();");
          return (await run()).violations.map(({ id, nodes }) => ({ id, targets: nodes.map(node => node.target) }));
        }, fs.readFileSync(axe, "utf8"));
        check(results.length === 0, `axe: ${route} ${JSON.stringify(results)}`);
      }
    }
    check(requests.every(([method, url]) => method === "GET" && url.startsWith(base + "/")), "browsing makes only same-origin GET requests");
    check(await page.evaluate(() => !document.cookie && !localStorage.length && !sessionStorage.length), "no cookies or browser storage");
    check(!errors.length, `no browser errors: ${errors.join(" | ")}`);
  } finally {
    await browser.close();
  }
  console.log(`${checks} publication checks passed.`);
}

main().catch(error => { console.error(error); process.exitCode = 1; });
