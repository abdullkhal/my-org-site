"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");
const { prepareSyntheticEnquiry, acceptLiveEnquiry } = require("../scripts/enquiry-workflow.cjs");
const root=path.resolve(__dirname,"..");
const sources=require("../data/sources.json").sources;
const knowledge=require("../data/knowledge.json").guides;
const policy=require("../data/enquiries.json");
const measurement=require("../data/measurement.json");
const base=process.env.PIIK_TEST_URL || "http://127.0.0.1:3000";
const output=process.env.PIIK_TEST_OUTPUT || "/tmp/piik-phase2-review";
let count=0;
function check(value,label) {assert.ok(value,label);count++;console.log(`PASS ${label}`);}
(async()=>{
  check(!policy.collection_enabled && !policy.provider && !policy.notification_destination,"live enquiry configuration is closed");
  check(!measurement.enabled && !measurement.provider,"measurement is inactive");
  for(const category of policy.categories) {
    const record=prepareSyntheticEnquiry({synthetic:true,category,name:"Example",email:"test@example.invalid",message:"A synthetic question",privacy_acknowledged:true});
    check(record.category===category && !record.sent && !record.stored && record.requires_founder_review,`${category} synthetic routing requires review and has no effects`);
    check(!JSON.stringify(record.notification_draft).includes("test@example.invalid"),`${category} notification draft excludes contact details`);
  }
  for(const bad of [{synthetic:false},{category:"unknown"},{email:"person@actual-domain.test"},{privacy_acknowledged:false},{message:"x".repeat(1501)}]) {
    assert.throws(()=>prepareSyntheticEnquiry({synthetic:true,category:"consumer",name:"Example",email:"test@example.invalid",message:"Synthetic",privacy_acknowledged:true,...bad}));count++;
  }
  assert.throws(()=>acceptLiveEnquiry({}));count++;
  check(prepareSyntheticEnquiry({synthetic:true,category:"general",name:"Example",email:"test@example.invalid",message:"Synthetic legal complaint",privacy_acknowledged:true}).sensitive,"sensitive fixture escalates");
  const browser=await chromium.launch({executablePath:process.env.PIIK_CHROMIUM || "/usr/bin/chromium",args:["--no-sandbox"]});
  try {
    const context=await browser.newContext();const page=await context.newPage();const requests=[];const errors=[];
    page.on("request",r=>requests.push({url:r.url(),method:r.method()}));page.on("pageerror",e=>errors.push(e.message));
    await page.goto(base,{waitUntil:"networkidle"});
    check((await page.locator("h1").innerText()).replace(/\s+/g," ").trim()==="Know who you're dealing with. Know what to check.","exact homepage headline");
    check(await page.locator(".hero-lead").textContent()==="Your starting point for navigating Kenya's property sector. Access practical guidance, discover official resources and connect with a growing community of property professionals as the network develops.","exact supporting copy");
    check(await page.locator(".hero-interest-note").isVisible(),"closed-registration notice is next to hero CTA");
    check(await page.locator(".hero-visual img").getAttribute("src")==="assets/imagery/residence-1536.webp","existing architecture image retained");
    check(await page.locator(".network-disciplines span").count()===9,"nine proposed network disciplines");
    check(await page.locator(".article").count()===knowledge.length && knowledge.length===7,"seven structured guides rendered");
    check(await page.locator(".source-card").count()===sources.length,"all source records rendered");
    for(const source of sources) {
      const card=page.locator(`#resource-${source.id}`);
      check(await card.count()===1,`${source.id} stable resource target`);
      if(source.status!=="verified") check(await card.locator("a[href^='https:']").count()===0,`${source.id} has no unverified outbound link`);
      else check(JSON.stringify(await card.locator("a[href^='https:']").evaluateAll(nodes=>nodes.map(n=>n.href)))===JSON.stringify([source.public_url,...(source.additional_links||[]).map(l=>l.url)]),`${source.id} exposes exactly its reviewed destinations`);
    }
    for(const category of ["agents","property","developers","professionals"]) {
      await page.locator(`.category:has(input[value="${category}"])`).click();
      for(const link of await page.locator(".step-resource").all()) {
        const href=await link.getAttribute("href");
        check(await page.locator(href).count()===1,`${category} step has valid authority-scope destination`);
      }
      const before=await page.locator("#check-progress").textContent();await page.locator(".step-resource").first().click();
      check(await page.locator("#check-progress").textContent()===before,`${category} resource click does not toggle checkbox`);
    }
    check(await page.locator("a[href='terms.html']").count()>0,"Terms accessible from homepage");
    const structured=JSON.parse(await page.locator('script[type="application/ld+json"]').textContent());
    check(structured['@graph'].map(x=>x['@type']).join(',')==='Organization,WebSite',"accurate Organization and WebSite schema, no invented members or ratings");
    for(const file of ["index.html","terms.html","privacy.html","credits.html"]) {
      await page.goto(`${base}/${file}`,{waitUntil:"networkidle"});
      const canonical=await page.locator('link[rel="canonical"]').getAttribute("href");
      check(canonical===`https://piikkenya.com/${file==='index.html'?'':file}`,`${file} canonical matches production path`);
      const links=await page.locator("a[href]").evaluateAll(nodes=>nodes.map(n=>n.getAttribute("href")));
      for(const href of new Set(links.filter(h=>!h.startsWith('mailto:')&&!h.startsWith('https:')))) {
        const url=new URL(href,page.url());
        if(url.pathname===new URL(page.url()).pathname&&url.hash) check(await page.locator(url.hash).count()===1,`${file} anchor ${url.hash}`);
        else {const res=await context.request.get(url.href);check(res.ok(),`${file} local link ${href}`);}
      }
    }
    for(const js of [true,false]) {
      const c=await browser.newContext({javaScriptEnabled:js});const p=await c.newPage();const posts=[];
      p.on("request",r=>{if(r.method()!=="GET") posts.push(r.url());});
      await p.goto(`${base}/review/enquiries.html`);
      check(await p.locator("form").count()===4,"four enquiry prototypes");
      check(await p.locator("input:enabled,textarea:enabled,select:enabled,button:enabled").count()===0,`all prototype controls disabled with JS=${js}`);
      check((await p.locator('meta[name="robots"]').getAttribute('content')).includes('noindex'),"prototype excluded from indexing");
      if(js) {
        await p.evaluate(()=>document.querySelector('form').submit());
        await p.waitForTimeout(100);
      }
      check(posts.length===0,"prototype makes no submission requests, including forced form.submit");
      check(await p.evaluate(()=>document.cookie===""&&localStorage.length===0&&sessionStorage.length===0),"prototype writes no cookies or browser storage");
      fs.mkdirSync(output,{recursive:true});
      if(js) await p.screenshot({path:path.join(output,"enquiry-prototype.png"),fullPage:true});
      await c.close();
    }
    const robots=await (await context.request.get(`${base}/robots.txt`)).text();
    check(robots.includes('Sitemap: https://piikkenya.com/sitemap.xml')&&robots.includes('Disallow: /review/'),"robots declares sitemap and excludes prototypes");
    const xml=await (await context.request.get(`${base}/sitemap.xml`)).text();
    check((xml.match(/<loc>/g)||[]).length===4 && !xml.includes('/review/'),"sitemap contains four public pages only");
    check(requests.every(r=>r.method==='GET' && r.url.startsWith(base)),"website uses only local GETs");
    check(errors.length===0,"no browser runtime errors");
    await context.close();
  }finally{await browser.close();}
  console.log(`\n${count} Phase 2 checks passed.`);
})().catch(e=>{console.error(e);process.exitCode=1;});
