"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");
const base = process.env.PIIK_TEST_URL || "http://127.0.0.1:3000";
const output = process.env.PIIK_TEST_OUTPUT || "/tmp/piik-review";
const axePath = process.env.PIIK_AXE_PATH;
const sourceRecords = require("../data/sources.json").sources;
const officialURLs = sourceRecords.filter(s => s.status === "verified").flatMap(s => [s.public_url, ...(s.additional_links || []).map(link => link.url)]);
async function loadEditorialImages(page) {
  for (const image of await page.locator("img").all()) {
    await image.scrollIntoViewIfNeeded();
    await image.evaluate((el) => el.decode());
  }
  await page.evaluate(() => window.scrollTo(0, 0));
}
let checks = 0;
function check(value, label) {
  assert.ok(value, label);
  checks++;
  console.log(`PASS ${label}`);
}

(async () => {
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({
    executablePath: process.env.PIIK_CHROMIUM || "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
  try {
    const context = await browser.newContext({
      viewport: { width: 1440, height: 1000 },
      reducedMotion: "reduce",
    });
    const page = await context.newPage();
    const errors = [];
    const requests = [];
    page.on("pageerror", (error) => errors.push(error.message));
    page.on("request", (request) =>
      requests.push({ url: request.url(), method: request.method() }),
    );
    const response = await page.goto(base, { waitUntil: "networkidle" });
    check(response.status() === 200, "homepage serves successfully");
    await loadEditorialImages(page);
    check(
      (await page.locator("h1").textContent()).includes("Know what to check."),
      "requested homepage headline",
    );
    check(
      (await page.locator("#year").textContent()) ===
        String(new Date().getFullYear()),
      "footer year script",
    );
    check(
      await page.locator(".menu-toggle").isHidden(),
      "desktop navigation needs no menu toggle",
    );
    check(
      await page.evaluate(() =>
        [...document.images].every(
          (img) => img.complete && img.naturalWidth > 0,
        ),
      ),
      "all images loaded",
    );
    check(
      (await page.locator("input[type=file]").count()) === 0,
      "no document uploads",
    );
    check(
      await page.evaluate(() => {
        const ids = [...document.querySelectorAll("[id]")].map((el) => el.id);
        return ids.length === new Set(ids).size;
      }),
      "unique element IDs",
    );

    const links = await page
      .locator("a")
      .evaluateAll((nodes) => nodes.map((node) => node.getAttribute("href")));
    for (const href of new Set(links)) {
      if (href.startsWith("#")) {
        check(
          (await page.locator(`[id="${href.slice(1)}"]`).count()) === 1,
          `anchor target ${href}`,
        );
      } else if (href.startsWith("https://")) {
        check(officialURLs.includes(href), `external destination is in the reviewed source register: ${href}`);
      } else if (!href.startsWith("mailto:")) {
        const res = await context.request.get(new URL(href, base).href);
        check(res.status() === 200, `local navigation ${href}`);
      }
    }
    for (const resource of [
      "style.css",
      "app.js",
      "assets/piik-logo.webp",
      "assets/imagery/residence-1536.webp",
      "assets/imagery/apartments-1024.webp",
      "assets/imagery/land-1024.webp",
      "assets/imagery/collaboration-1024.webp",
      "assets/imagery/diaspora-1024.webp",
      "assets/imagery/skyline-1024.webp",
      "assets/favicon.svg",
    ]) {
      const res = await context.request.get(`${base}/${resource}`);
      check(
        res.status() === 200 && (await res.body()).length > 0,
        `asset ${resource}`,
      );
    }
    await page
      .getByRole("link", { name: "Check Before You Commit", exact: true })
      .click();
    check(page.url().endsWith("#piik-check"), "primary CTA reaches PIIK Check");
    await page
      .getByRole("link", { name: "Register Your Professional Interest", exact: true })
      .click();
    check(
      page.url().endsWith("#professional-form"),
      "secondary CTA reaches professional interest status",
    );
    await page
      .getByRole("link", {
        name: "Registration information",
        exact: false,
      })
      .click();
    check(
      page.url().endsWith("#professional-form"),
      "network pathway reaches professional registration status",
    );

    const categories = {
      agents: "An agent or agency",
      property: "A property or land opportunity",
      developers: "A developer or housing project",
      professionals: "A property professional",
    };
    for (const [key, title] of Object.entries(categories)) {
      // Exercise the visible label rather than force-clicking the visually hidden radio.
      await page.locator(`.category:has(input[value="${key}"])`).click();
      check(
        (await page.locator("#check-title").textContent()) === title,
        `${key} tailored guidance displayed`,
      );
      const boxes = page.locator("#check-output input[type=checkbox]");
      check((await boxes.count()) === 4, `${key} has four actionable steps`);
      for (let index = 0; index < 4; index++) await boxes.nth(index).check();
      check(
        (await page.locator("#check-progress").textContent()).includes(
          "Review complete",
        ),
        `${key} completion reports review only`,
      );
    }
    await page.locator('.category:has(input[value="agents"])').click();
    check(
      (await page.locator("#check-progress").textContent()).startsWith(
        "4 of 4",
      ),
      "per-category state survives switching",
    );
    await page
      .getByRole("button", { name: "Reset this checklist", exact: true })
      .click();
    check(
      (await page.locator("#check-progress").textContent()).startsWith(
        "0 of 4",
      ),
      "checklist reset clears only current category",
    );
    await page.locator('input[value="agents"]').focus();
    await page.keyboard.press("ArrowRight");
    check(
      (await page.locator("#check-title").textContent()) ===
        categories.property,
      "radio guidance selection works by keyboard",
    );
    await page.evaluate(() => {
      window.print = () => {
        window.__piikPrintCalled = true;
      };
    });
    await page
      .getByRole("button", { name: "Print checklist", exact: true })
      .click();
    check(
      await page.evaluate(() => window.__piikPrintCalled),
      "print control invokes print",
    );
    await page.emulateMedia({ media: "print" });
    check(
      (await page.locator(".hero").isHidden()) &&
        (await page.locator(".print-heading").isVisible()),
      "print layout shows checklist and limitations",
    );
    check(
      await page.locator(".property-context").isHidden(),
      "print layout excludes decorative property photography",
    );
    await page.pdf({
      path: path.join(output, "property-checklist.pdf"),
      format: "A4",
      printBackground: true,
    });
    await page.emulateMedia({ media: "screen" });

    for (const detail of await page.locator(".article").all()) {
      await detail.locator("summary").focus();
      await page.keyboard.press("Enter");
      check(
        (await detail.getAttribute("open")) !== null,
        "knowledge guide opens with keyboard",
      );
      check(
        await detail.locator(".article-body").isVisible(),
        "knowledge guide content visible",
      );
      await page.keyboard.press("Enter");
      check(
        (await detail.getAttribute("open")) === null,
        "knowledge guide closes with keyboard",
      );
    }

    await loadEditorialImages(page);
    const requestCount = requests.length;
    check(
      (await page.locator("form").count()) === 0,
      "no non-submitting enquiry forms are exposed",
    );
    for (const kind of ["consumer", "professional"]) {
      const card = page.locator(`#${kind}-form`);
      check(await card.isVisible(), `${kind} unavailable status is visible`);
      check(
        (await card.textContent()).includes("Not accepting online submissions"),
        `${kind} clearly discloses that submissions are unavailable`,
      );
      check(
        (await card.locator("input, select, textarea").count()) === 0,
        `${kind} has no personal-information fields`,
      );
      check(
        await card.getByRole("button").isDisabled(),
        `${kind} enquiry or registration button stays disabled with JavaScript`,
      );
    }
    check(
      requests.length === requestCount,
      "registration status makes no submission requests",
    );
    check(
      requests.every((r) => r.method === "GET" && r.url.startsWith(base)),
      "website makes only same-origin GET requests",
    );
    check(
      await page.evaluate(
        () =>
          localStorage.length === 0 &&
          sessionStorage.length === 0 &&
          document.cookie === "",
      ),
      "no cookies or browser storage written",
    );
    check(
      (await page.locator("#official-hub a[href^='https:']").count()) === officialURLs.length,
      "hub exposes only recorded independently researched destinations",
    );
    check(
      (await page.locator(".image-label, .photo-note").count()) === 0,
      "repeated decorative image labels removed; credits retained",
    );
    await page.reload({ waitUntil: "networkidle" });
    check(
      (await page.locator("#check-progress").textContent()).startsWith(
        "0 of 4",
      ),
      "checklist state not persisted across reload",
    );

    const sizes = [320, 390, 768, 1024, 1440, 1920];
    for (const width of sizes) {
      await page.setViewportSize({ width, height: 900 });
      check(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
        `no horizontal overflow at ${width}px`,
      );
      if (width === 390 || width === 1440) {
        await page.goto(base, { waitUntil: "networkidle" });
        await loadEditorialImages(page);
        await page.screenshot({
          path: path.join(
            output,
            `${width === 390 ? "mobile" : "desktop"}-full.png`,
          ),
          fullPage: true,
        });
        await page.screenshot({
          path: path.join(
            output,
            `${width === 390 ? "mobile" : "desktop"}-hero.png`,
          ),
        });
      }
    }
    await page.setViewportSize({ width: 390, height: 844 });
    const menu = page.getByRole("button", { name: "Menu", exact: false });
    check(
      (await menu.isVisible()) &&
        (await page.locator("#main-navigation").isHidden()),
      "mobile navigation is collapsed by default",
    );
    await menu.click();
    check(
      (await menu.getAttribute("aria-expanded")) === "true" &&
        (await page.locator("#main-navigation").isVisible()),
      "mobile menu opens",
    );
    await page.keyboard.press("Escape");
    check(
      (await menu.getAttribute("aria-expanded")) === "false" &&
        (await menu.evaluate((el) => el === document.activeElement)),
      "Escape closes menu and returns focus",
    );
    await menu.click();
    await page
      .locator("#main-navigation")
      .getByRole("link", { name: "Diaspora", exact: true })
      .click();
    check(
      page.url().endsWith("#diaspora") &&
        (await page.locator("#main-navigation").isHidden()),
      "mobile navigation follows link and closes",
    );
    await menu.click();
    await page.locator("#home .eyebrow").click();
    check(
      (await menu.getAttribute("aria-expanded")) === "false",
      "click outside closes mobile menu",
    );

    for (const file of ["privacy.html", "credits.html", "terms.html"]) {
      await page.goto(`${base}/${file}`, { waitUntil: "networkidle" });
      check(
        await page.locator("main h1").isVisible(),
        `${file} content renders`,
      );
      check(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
        `${file} fits mobile viewport`,
      );
      await page
        .getByRole("link", { name: "Return to PIIK Kenya", exact: false })
        .click();
      check(
        await page.locator("#home").isVisible(),
        `${file} return link works`,
      );
    }

    const noJs = await browser.newContext({
      javaScriptEnabled: false,
      viewport: { width: 390, height: 844 },
    });
    const fallback = await noJs.newPage();
    await fallback.goto(base);
    check(
      await fallback.locator("#main-navigation").isVisible(),
      "navigation available without JavaScript",
    );
    check(
      await fallback.locator("#check-output noscript").isVisible(),
      "guidance fallback available without JavaScript",
    );
    check(
      (await fallback
        .locator(
          ".interest-form input:enabled, .interest-form select:enabled, .interest-form textarea:enabled, .interest-form button[type=submit]:enabled",
        )
        .count()) === 0,
      "no active enquiry inputs without JavaScript",
    );
    for (const kind of ["consumer", "professional"]) {
      check(
        await fallback.locator(`#${kind}-form button`).isDisabled(),
        `${kind} stays disabled without JavaScript`,
      );
    }
    await noJs.close();

    if (axePath) {
      const results = [];
      for (const width of [390, 1440]) {
        await page.setViewportSize({ width, height: 1000 });
        for (const route of ["/", "/privacy.html", "/credits.html", "/terms.html", "/review/enquiries.html", "/review/official-links.html"]) {
          await page.goto(`${base}${route}`, { waitUntil: "networkidle" });
          await page.evaluate(fs.readFileSync(axePath, "utf8"));
          const audit = await page.evaluate(async () =>
            window.axe.run(document, {
              runOnly: {
                type: "tag",
                values: ["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"],
              },
            }),
          );
          results.push({
            route,
            width,
            violations: audit.violations,
            incomplete: audit.incomplete,
          });
          check(
            audit.violations.length === 0,
            `axe accessibility audit ${route} at ${width}px: ${audit.violations.map((v) => v.id).join(", ") || "zero violations"}`,
          );
        }
      }
      fs.writeFileSync(
        path.join(output, "accessibility.json"),
        JSON.stringify(results, null, 2),
      );
    } else
      console.log(
        "NOT RUN: optional axe accessibility audit (set PIIK_AXE_PATH)",
      );
    check(
      errors.length === 0,
      `no browser JavaScript errors: ${errors.join("; ")}`,
    );
    await context.close();
    console.log(`\n${checks} checks passed. Review artifacts: ${output}`);
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
