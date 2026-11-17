"use strict";
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const sources=require('../data/sources.json').sources;
const active=sources.filter(s=>s.status==='verified').flatMap(s=>[s.public_url,...(s.additional_links||[]).map(l=>l.url)]);
const base=process.env.PIIK_TEST_URL || 'http://127.0.0.1:3000';
let checks=0;
function check(value,label){assert.ok(value,label);checks++;console.log('PASS '+label);}
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.PIIK_CHROMIUM || '/usr/bin/chromium',args:['--no-sandbox']});
 try{
  const page=await browser.newPage();const requests=[];
  page.on('request',r=>requests.push(r.url()));
  await page.goto(base+'/review/official-links.html');
  check(await page.locator('h1').textContent()==='Official website link table','review clearly labels the current link table');
  check(await page.locator('a[href^="https:"]').count()===active.length,'review exposes accepted destinations, with unresolved authorities pending');
  for(const url of active){
   const link=page.locator(`a[href="${url}"]`);
   check(await link.count()===1 && (await link.getAttribute('rel')).includes('noreferrer'),'review destination matches accepted record and suppresses referrer');
  }
  check((await page.locator('meta[name="robots"]').getAttribute('content')).includes('noindex'),'review list is noindex');
  check(await page.locator('form,input,textarea,script').count()===0,'review list has no collection fields or scripts');
  for(const width of [320,390,768,1440]){
   await page.setViewportSize({width,height:1000});
   check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'review list fits '+width+'px');
  }
  check(requests.every(url=>url.startsWith(base)),'viewing the list does not contact candidate sites');
 }finally{await browser.close();}
 console.log(`\n${checks} source-review page checks passed.`);
})().catch(e=>{console.error(e);process.exitCode=1;});
