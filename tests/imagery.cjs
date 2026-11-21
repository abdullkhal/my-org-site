"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");
const base = process.env.PIIK_TEST_URL || "http://127.0.0.1:3000";
const output = process.env.PIIK_TEST_OUTPUT || "/tmp/piik-review";
const root = path.resolve(__dirname, "..");
let checks = 0;
function check(value, label) {
  assert.ok(value, label);
  console.log(`PASS ${label}`);
  checks++;
}
(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.PIIK_CHROMIUM || "/usr/bin/chromium",
    args: ["--no-sandbox"],
  });
  const report = [];
  try {
    const manifest = JSON.parse(
      fs.readFileSync(path.join(root, "assets/imagery/manifest.json")),
    );
    check(
      manifest.length === 6 &&
        new Set(manifest.map((item) => item.master_sha256)).size === 6,
      "six distinct original generated image masters documented",
    );
    for (const { name, widths } of manifest)
      for (const width of widths) {
        const filename = `assets/imagery/${name}-${width}.webp`;
        const res = await fetch(new URL(filename, base));
        check(
          res.ok && (await res.arrayBuffer()).byteLength > 0,
          `${filename} serves successfully`,
        );
      }
    for (const [label, width, deviceScaleFactor] of [
      ["desktop", 1440, 1],
      ["mobile", 390, 1],
      ["retina-mobile", 390, 2],
    ]) {
      const context = await browser.newContext({
        viewport: { width, height: 1000 },
        deviceScaleFactor,
        reducedMotion: "reduce",
      });
      const page = await context.newPage();
      const requests = [];
      page.on("request", (r) => requests.push(r.url()));
      await page.goto(base, { waitUntil: "networkidle" });
      const firstLoad = await page.evaluate(() => ({
        hero: document.querySelector(".hero-photo img").currentSrc,
        bytes: performance
          .getEntriesByType("resource")
          .reduce((n, r) => n + r.encodedBodySize, 0),
        lateImages: [
          ...document.querySelectorAll(
            ".network-visual img,.diaspora-visual img,.about-skyline img",
          ),
        ].filter((i) => i.complete && i.naturalWidth > 0).length,
      }));
      check(
        firstLoad.hero.endsWith(
          label === "desktop"
            ? "skyline-1024.webp"
            : label === "mobile"
              ? "skyline-640.webp"
              : "skyline-1024.webp",
        ),
        `${label} chooses an appropriate hero image size`,
      );
      check(
        firstLoad.lateImages === 0,
        `${label} defers distant editorial images`,
      );
      const photos = page.locator("main img");
      check(
        (await photos.count()) === 2,
        `${label} renders homepage editorial images`,
      );
      for (const img of await photos.all()) {
        check(
          (await img.getAttribute("width")) > 0 &&
            (await img.getAttribute("height")) > 0 &&
            (await img.getAttribute("alt")).includes("AI-generated"),
          `${label} image has intrinsic dimensions and contextual generated-image alt text`,
        );
        await img.scrollIntoViewIfNeeded();
        await img.evaluate((i) => i.decode());
        check(
          await img.evaluate(
            (i) =>
              i.naturalWidth > 0 && i.currentSrc.includes("/assets/imagery/"),
          ),
          `${label} image loads locally when needed`,
        );
      }
      check(
        requests.every((u) => u.startsWith(base)),
        `${label} makes no third-party image requests`,
      );
      const sizes = await page.evaluate(() =>
        performance
          .getEntriesByType("resource")
          .filter((r) => r.initiatorType === "img")
          .map((r) => ({
            url: new URL(r.name).pathname,
            bytes: r.encodedBodySize,
          })),
      );
      const bytes = sizes.reduce((n, r) => n + r.bytes, 0);
      check(
        bytes <
          (label === "desktop"
            ? 1400000
            : label === "mobile"
              ? 500000
              : 950000),
        `${label} total image transfer remains within review budget`,
      );
      check(
        !requests.some(
          (u) =>
            u.includes("nairobi-preview.webp") ||
            u.includes("hero-nairobi.jpg"),
        ),
        `${label} never loads the old image with unconfirmed rights`,
      );
      report.push({
        label,
        width,
        deviceScaleFactor,
        initial: firstLoad,
        images: sizes,
        totalImageBytes: bytes,
      });
      await context.close();
    }
    const p = await browser.newPage({ reducedMotion: "reduce" });
    for (const width of [761, 900, 1024, 1100, 1440]) {
      await p.setViewportSize({ width, height: 1000 });
      await p.goto(base);
      const bounds = await p.evaluate(() => {
        const copy = document
          .querySelector(".hero-copy")
          .getBoundingClientRect();
        const frame = document
          .querySelector(".hero-photo")
          .getBoundingClientRect();
        return (
          copy.right <= frame.left && copy.width > 0 && frame.width > 0
        );
      });
      check(
        bounds,
        `desktop hero copy and image remain split at ${width}px`,
      );
    }
    await p.close();
    fs.mkdirSync(output, { recursive: true });
    fs.writeFileSync(
      path.join(output, "image-performance.json"),
      JSON.stringify(report, null, 2),
    );
    console.log(`\n${checks} imagery checks passed.`);
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
