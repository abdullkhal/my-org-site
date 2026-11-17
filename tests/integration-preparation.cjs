"use strict";
const assert=require("node:assert/strict");
const {validatePayload,submitSynthetic,submitLive}=require("../scripts/formspree-adapter.cjs");
const config=require("../data/formspree.json");
let count=0;
function check(value,label){assert.ok(value,label);count++;console.log(`PASS ${label}`)}
const base={category:"consumer",name:"Synthetic Example",email:"review@example.invalid",message:"Synthetic guidance question",privacy_acknowledged:true};
(async()=>{
 check(!config.enabled && !config.endpoint && !config.business_email,"no enabled provider, endpoint or selected business email");
 check(Object.values(config.approval).every(v=>v===false),"approval gates remain closed");
 for(const category of ["consumer","diaspora","professional","general"]){
  const result=await submitSynthetic({...base,category},async({url,synthetic,request})=>{
   check(url===null&&synthetic===true,"mock request has no live destination");
   const body=JSON.parse(request.body);
   check(body.category===category&&body._subject===`PIIK ${category} enquiry`,`${category} uses allowlisted category and subject`);
   return {status:200,ok:true,json:async()=>({ok:true})};
  });
  check(result.accepted&&!result.sent&&!result.stored&&result.requires_founder_review,`${category} mocked acceptance is review-only`);
 }
 for(const patch of [{email:"bad"},{email:"a@example.invalid\r\nBcc:test@example.invalid"},{name:"Example\nHeader"},{message:"x".repeat(1501)},{category:"other"},{privacy_acknowledged:false},{_gotcha:"spam"},{upload:"not-allowed"},{role:"Architect"}]){
  assert.throws(()=>validatePayload({...base,...patch}));count++;
 }
 check(validatePayload({...base,category:"professional",role:"Architect",service_area:"Nairobi"}).role==="Architect","professional fields map correctly");
 await assert.rejects(()=>submitSynthetic({...base,email:"someone@real-domain.test"},async()=>{}));count++;
 await assert.rejects(()=>submitSynthetic(base));count++;
 for(const status of [400,403,422,429,500]){
  const r=await submitSynthetic(base,async()=>({status,ok:false,json:async()=>({ok:false})}));
  check(!r.accepted&&r.status===(status===429?"rate_limited":"delivery_failed"),`HTTP ${status} never claims success`);
 }
 for(const transport of [async()=>({status:200,ok:true,json:async()=>({ok:false})}),async()=>({status:200,ok:true,json:async()=>{throw Error("invalid JSON")}}),async()=>{throw Error("timeout")},async()=>({status:302,ok:true,json:async()=>({ok:true})})]){
  check(!(await submitSynthetic(base,transport)).accepted,"unconfirmed/redirect/transport outcome never claims success");
 }
 assert.throws(()=>submitLive());count++;
 check(validatePayload({...base,message:"<script>synthetic</script>"}).message==="<script>synthetic</script>","message remains data; never rendered as HTML");
 console.log(`\n${count} integration-preparation checks passed.`);
})().catch(e=>{console.error(e);process.exitCode=1});
