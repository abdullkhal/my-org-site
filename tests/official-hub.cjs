"use strict";
const assert=require('node:assert/strict');
const{chromium}=require('playwright');
const sources=require('../data/sources.json').sources;
const base=process.env.PIIK_TEST_URL||'http://127.0.0.1:3000';
const output=process.env.PIIK_TEST_OUTPUT||'/tmp/piik-official-update';
const approved={
 earb:['https://estateagentsboard.or.ke/official-publication-of-the-2026-kenya-gazette-registered-estate-agents-and-estate-agents-companies/'],
 ardhisasa:['https://ardhisasa.lands.go.ke/'],
 lsk:['https://lsk.or.ke/faq/'],
 lsb:['https://www.lsb.go.ke/register'],
 brs:['https://brs.go.ke/'],
 vrb:['https://vrb.or.ke/'],
 boraqs:['https://boraqs.go.ke/registered/','https://boraqs.go.ke/registered/qs'],
 nca:['https://www.nca.go.ke/registered-contractors'],
};
let checks=0;function check(value,label){assert.ok(value,label);checks++;console.log('PASS '+label)}
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.PIIK_CHROMIUM||'/usr/bin/chromium',args:['--no-sandbox']});
 try{
  const context=await browser.newContext();const page=await context.newPage();const intercepted=[];
  await context.route('https://**/*',route=>{
   const url=route.request().url();intercepted.push(url);
   if(!Object.values(approved).flat().includes(url))return route.abort();
   return route.fulfill({status:200,contentType:'text/html',body:'<!doctype html><html><head><title>Synthetic destination</title><link rel="icon" href="data:,"></head><body><h1>Offline navigation fixture</h1></body></html>'});
  });
  await page.goto(base);
  check(await page.locator('#official-hub a[href^="https:"]').count()===9,'exactly nine researched external links, covering eight authorities');
  for(const [id,urls] of Object.entries(approved)){
   const record=sources.find(s=>s.id===id);
   check(record.status==='verified'&&record.verification_method==='founder_supplied_independent_research'&&record.checked_at==='2026-11-17',id+' records founder provenance and review date');
   check(urls.every(url=>record.evidence.some(e=>e.url===url&&e.type==='founder_supplied_destination')),id+' has evidence for each destination');
   const links=await page.locator('#resource-'+id+' a').evaluateAll(nodes=>nodes.map(n=>({url:n.href,rel:n.rel,label:n.textContent})));
   check(JSON.stringify(links.map(l=>l.url))===JSON.stringify(urls),id+' exactly matches supplied URLs');
   check(links.every(l=>l.rel.includes('noreferrer')&&l.label.trim()),id+' links have descriptive labels and no referrer');
  }
  for(const id of ['ebk','nema','approvals'])check(await page.locator('#resource-'+id+' a').count()===0,id+' remains pending without an external button');
  check((await page.locator('#resource-earb').textContent()).includes('dated publication, not a live'),'EARB distinguishes the 2026 publication from live status');
  check((await page.locator('#resource-lsk').textContent()).includes('not itself an advocate-status search'),'LSK FAQ is not presented as an individual lookup');
  for(const id of ['lsb','boraqs'])check((await page.locator('#resource-'+id).textContent()).includes('published register')||(await page.locator('#resource-'+id).textContent()).includes('published listings'),id+' explains published register limits');
  check((await page.locator('#resource-nca').textContent()).includes('separate from project registration'),'NCA contractor listing does not imply project registration');
  for(const url of Object.values(approved).flat()){
   await page.goto(base+'/#official-hub');
   await page.locator(`#official-hub a[href="${url}"]`).click();
   await page.waitForURL(url);
   check(page.url()===url,'outbound click reaches exactly the supplied destination (intercepted offline)');
  }
  check(intercepted.length===9,'all nine clicks were tested with offline interception, not live-site validation');
  await page.goto(base+'/#official-hub');await page.setViewportSize({width:1440,height:1000});
  await page.locator('#official-hub').screenshot({path:output+'/official-hub-desktop.png'});
  await page.setViewportSize({width:390,height:844});
  check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'expanded resource actions fit mobile');
  await page.locator('#official-hub').screenshot({path:output+'/official-hub-mobile.png'});
 }finally{await browser.close()}
 console.log(`\n${checks} official-hub checks passed.`);
})().catch(e=>{console.error(e);process.exitCode=1});
