/* Stable content-pack API. No UI, network, eval, or runtime AI dependencies. */
(function(root){
'use strict';
const KEYS={active:'hvac122.content.active.v1',draft:'hvac122.content.draft.v1',previous:'hvac122.content.previous.v1'};
const clone=x=>JSON.parse(JSON.stringify(x));
const arrays=['chapters','knowledge','questions','examProfiles','resources'];
const types=['recall','understanding','application','calculation'];
const idOk=x=>typeof x==='string'&&/^[A-Za-z0-9][A-Za-z0-9_.:-]{0,95}$/.test(x);
const text=x=>typeof x==='string'&&x.trim().length>0;
function fromBank(bank){return {format:'hvac122-content-pack',schemaVersion:1,version:bank.version,title:bank.title||'HVAC-122 Electrical Fundamentals',chapters:clone(bank.chapters),knowledge:clone(bank.knowledge),questions:clone(bank.questions).map(q=>({...q,publishedOnce:!!q.eligible})),examProfiles:clone(bank.examProfiles||[]),resources:clone(bank.resources||[])};}
const models={
 ohm_current:[x=>x.V/x.R,'A'],ohm_voltage:[x=>x.I*x.R,'V'],ohm_resistance:[x=>x.V/x.I,'Ω'],
 power_vi:[x=>x.V*x.I,'W'],power_i2r:[x=>x.I*x.I*x.R,'W'],power_v2r:[x=>x.V*x.V/x.R,'W'],power_pf:[x=>x.V*x.I*x.PF,'W'],
 energy:[x=>x.P*x.h/1000,'kWh'],horsepower:[x=>x.hp*746/x.efficiency,'W'],series:[x=>x.R1+x.R2,'Ω'],
 divider:[x=>x.V*x.R2/(x.R1+x.R2),'V'],parallel:[x=>1/(1/x.R1+1/x.R2),'Ω'],current_sum:[x=>x.I1+x.I2,'A'],clamp:[x=>x.reading/x.turns,'A'],tolerance:[x=>x.nominal*x.percent/100,'Ω']
};
function calcError(q){
 const c=q.calculation,m=c&&models[c.model];if(!m)return '計算題須使用支援的 calculation.model';
 if(!c.inputs||!Object.values(c.inputs).length||Object.values(c.inputs).some(v=>!Number.isFinite(v)||v<=0))return '計算輸入必須為正的有限數字';
 if(c.model==='power_pf'&&c.inputs.PF>1||c.model==='horsepower'&&c.inputs.efficiency>1||c.model==='clamp'&&!Number.isInteger(c.inputs.turns))return 'PF／效率／圈數超出適用範圍';
 let result=m[0](c.inputs);if(!Number.isFinite(result)||!Number.isFinite(c.answer)||Math.abs(result-c.answer)>Math.max(1e-6,Math.abs(result)*1e-8)||c.unit!==m[1])return '計算模型答案或單位不符';
 const correct=q.choices?.find(x=>x.id===q.correct_choice);const parts=correct?.text_en?.trim().split(/\s+/);
 if(!parts||parts.length!==2||parts[1]!==m[1]||!Number.isFinite(Number(parts[0]))||Math.abs(Number(parts[0])-result)>Math.max(1e-6,Math.abs(result)*1e-5))return '正確選項須為模型結果及單位，例如 2 A';
 const matches=q.choices.filter(x=>{const p=x.text_en.trim().split(/\s+/);return p.length===2&&p[1]===m[1]&&Math.abs(Number(p[0])-result)<=Math.max(1e-6,Math.abs(result)*1e-5);});
 if(matches.length!==1)return '計算題不能有兩個等值正確選項';return null;
}
function examCandidates(profile,pack){
 const ids=new Set(profile.questionIds||[]);
 return pack.questions.filter(q=>q.eligible&&(ids.size?ids.has(q.id):(!profile.chapters.length||profile.chapters.includes(q.chapter))&&(!profile.types.length||profile.types.includes(q.type))));
}
function inspect(p){
 const errors=[],warnings=[],fail=m=>errors.push(m);
 if(!p||p.format!=='hvac122-content-pack'||p.schemaVersion!==1)return {errors:['不是支援的內容包格式（schemaVersion 1）'],warnings,stats:{}};
 if(!text(p.version)||!text(p.title))fail('內容包需有 version 及 title');
 for(const a of arrays)if(!Array.isArray(p[a]))fail(a+' 必須是陣列');
 if(errors.length)return {errors,warnings,stats:{}};
 if(p.questions.length>5000||p.knowledge.length>1000||p.resources.length>500)fail('超過本機內容數量上限');
 const chapterSet=new Set(),kids=new Set(),qids=new Set();
 for(const ch of p.chapters){if(!ch||!Number.isInteger(ch.id)||ch.id<1||ch.id>5||chapterSet.has(ch.id)||!text(ch.name_en)||!text(ch.name_zh))fail('章節須為不同的 1–5 並有雙語名稱');else chapterSet.add(ch.id);}
 function unique(list,seen,label){for(const x of list){if(!x||!idOk(x.id)||seen.has(x.id))fail(label+' ID 無效或重複：'+String(x?.id));else seen.add(x.id);}}
 unique(p.knowledge,kids,'Knowledge');unique(p.questions,qids,'Question');unique(p.examProfiles,new Set(),'Exam');unique(p.resources,new Set(),'Resource');
 for(const k of p.knowledge){if(!k)continue;const at='知識點 '+k.id+'：';
  for(const f of ['topic_key','term_en','term_zh','definition_en','explanation_zh','hvac_application','exam_note_en','verification_status','content_class','source_limitations'])if(!text(k[f]))fail(at+f+' 不可空白');
  if(!chapterSet.has(k.chapter))fail(at+'chapter 無效');
  for(const f of ['related_formulas','common_misconceptions'])if(!Array.isArray(k[f])||k[f].some(x=>!text(x)))fail(at+f+' 須為文字陣列');
  if(!k.source_reference||!text(k.source_reference.file)||!text(k.source_reference.record))fail(at+'須有來源位置與記錄');
 }
 const norms=new Set();
 for(const q of p.questions){if(!q)continue;const at='題目 '+q.id+'：';
  for(const f of ['topic','difficulty','question_en','question_zh','explanation_en','explanation_zh','verification_status'])if(!text(q[f]))fail(at+f+' 不可空白');
  if(!types.includes(q.type))fail(at+'題型不支援');if(!['basic','intermediate','applied'].includes(q.difficulty))fail(at+'難度不支援');if(!chapterSet.has(q.chapter))fail(at+'章節無效');
  if(!Array.isArray(q.knowledge_ids)||!q.knowledge_ids.length||new Set(q.knowledge_ids).size!==q.knowledge_ids.length||q.knowledge_ids.some(id=>!kids.has(id)||p.knowledge.find(k=>k.id===id)?.chapter!==q.chapter))fail(at+'Knowledge ID 不存在、重複或章節不符');
  if(!Array.isArray(q.choices)||q.choices.length!==4||new Set(q.choices?.map(c=>c?.id)).size!==4||q.choices?.some(c=>!c||!['A','B','C','D'].includes(c.id)||!text(c.text_en)||!text(c.text_zh)))fail(at+'須有 A–D 四個雙語選項');
  else{if(new Set(q.choices.map(c=>c.text_en.trim().toLowerCase())).size!==4)fail(at+'選項重複');if(q.choices.filter(c=>c.id===q.correct_choice).length!==1)fail(at+'須有唯一正確答案');}
  for(const id of ['A','B','C','D'])if(!text(q.choice_explanations?.[id]?.en)||!text(q.choice_explanations?.[id]?.zh))fail(at+id+' 須有英中選項解析');
  if(typeof q.eligible!=='boolean'||typeof q.original_teacher_question!=='boolean')fail(at+'eligible／original_teacher_question 須為布林值');
  if(!q.source_reference||!text(q.source_reference.file)||!text(q.source_reference.record)||typeof q.source_reference.original_verified!=='boolean'||!text(q.source_reference.note))fail(at+'來源欄位不完整');
  if(q.eligible&&['draft','unverified','generated_unreviewed'].includes(q.verification_status))fail(at+'未核對草稿不可啟用');
  const normalized=String(q.question_en).toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
  if(normalized&&norms.has(normalized))warnings.push(at+'與另一題題幹相同，請檢查');norms.add(normalized);
  if(q.type==='calculation'&&Array.isArray(q.choices)&&q.choices.every(c=>typeof c?.text_en==='string')){const error=calcError(q);if(error)fail(at+error);}
 }
 for(const x of p.examProfiles){if(!x)continue;const at='考試 '+x.id+'：';
  if(!text(x.name)||typeof x.enabled!=='boolean'||!Number.isInteger(x.count)||x.count<1||x.count>300||!(x.minutes===null||Number.isFinite(x.minutes)&&x.minutes>=1&&x.minutes<=600))fail(at+'名稱、啟用、題數或分鐘格式無效');
  if(!Array.isArray(x.chapters)||x.chapters.some(id=>!chapterSet.has(id))||!Array.isArray(x.types)||x.types.some(t=>!types.includes(t))||!Array.isArray(x.questionIds)||new Set(x.questionIds).size!==x.questionIds.length||x.questionIds.some(id=>!qids.has(id)))fail(at+'篩選或固定題目 ID 無效');
  else if(x.enabled&&examCandidates(x,p).length<x.count)fail(at+'可用的已啟用題目少於指定題數');
 }
 for(const r of p.resources){if(!r)continue;if(!text(r.title)||!text(r.text)||!text(r.source)||!['lecture','lab','exam','other'].includes(r.kind)||!(r.chapter===null||chapterSet.has(r.chapter))||typeof r.verified!=='boolean')fail('教材 '+r.id+' 欄位不完整');}
 const stats={questions:p.questions.length,enabled:p.questions.filter(q=>q?.eligible).length,drafts:p.questions.filter(q=>!q?.eligible).length,knowledge:p.knowledge.length,exams:p.examProfiles.length,resources:p.resources.length};
 return {errors,warnings,stats};
}
function validate(p){const r=inspect(p);if(r.errors.length)throw Error(r.errors.slice(0,25).join('\n'));return p;}
function signature(q){return JSON.stringify([q.chapter,q.knowledge_ids,q.type,q.question_en,[...q.choices].sort((a,b)=>a.id.localeCompare(b.id)).map(c=>[c.id,c.text_en]),q.correct_choice]);}
function assertRevisions(next,previous){const old=new Map(previous.questions.filter(q=>q.eligible||q.publishedOnce).map(q=>[q.id,q]));for(const q of next.questions){if(old.has(q.id)&&signature(q)!==signature(old.get(q.id)))throw Error('已啟用題目 '+q.id+' 的題幹／正解／選項已改，請另建新 Question ID，保護舊作答紀錄。');}}
function fingerprint(x){let h=2166136261;const s=JSON.stringify(x);for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619);}return (h>>>0).toString(16);}
function envelope(pack,base){const data={format:'hvac122-content-delta',schemaVersion:1,baseFingerprint:fingerprint(base),version:pack.version,title:pack.title,changes:{}};
 for(const key of arrays){const before=new Map(base[key].map(x=>[x.id,x])),after=new Set(pack[key].map(x=>x.id));data.changes[key]={upsert:pack[key].filter(x=>!before.has(x.id)||JSON.stringify(x)!==JSON.stringify(before.get(x.id))),remove:base[key].filter(x=>!after.has(x.id)).map(x=>x.id)};}
 return data;
}
function expand(data,base){if(!data||data.format!=='hvac122-content-delta'||data.schemaVersion!==1||data.baseFingerprint!==fingerprint(base))throw Error('內建題庫版本已改變或內容儲存格式無效。請保留原資料並用完整內容包重新匯入。');
 const result=clone(base);result.version=data.version;result.title=data.title;
 for(const key of arrays){const c=data.changes[key];if(!c||!Array.isArray(c.upsert)||!Array.isArray(c.remove))throw Error('內容差異格式損壞');const map=new Map(result[key].map(x=>[x.id,x]));c.remove.forEach(id=>map.delete(id));c.upsert.forEach(x=>map.set(x.id,x));result[key]=[...map.values()];}return validate(result);
}
function read(storage,key,base){const raw=storage.getItem(key);return raw?expand(JSON.parse(raw),base):clone(base);}
function saveDraft(storage,pack,base){validate(pack);storage.setItem(KEYS.draft,JSON.stringify(envelope(pack,base)));}
function install(storage,pack,base){validate(pack);const previous=read(storage,KEYS.active,base);assertRevisions(pack,previous);if(previous.version===pack.version&&JSON.stringify(previous)!==JSON.stringify(pack))throw Error('發布有變更的內容前，請先更新內容版本。');const raw=storage.getItem(KEYS.active);storage.setItem(KEYS.previous,raw||JSON.stringify(envelope(base,base)));const normalized=clone(pack),oldById=new Map(previous.questions.map(q=>[q.id,q]));for(const q of normalized.questions)q.publishedOnce=!!(q.eligible||q.publishedOnce||oldById.get(q.id)?.publishedOnce||oldById.get(q.id)?.eligible);storage.setItem(KEYS.active,JSON.stringify(envelope(normalized,base)));}
function toBank(pack){validate(pack);const q=clone(pack.questions.filter(x=>x.eligible)),k=clone(pack.knowledge);k.forEach(x=>x.related_question_ids=q.filter(q=>q.knowledge_ids.includes(x.id)).map(q=>q.id));const chapters=clone(pack.chapters);chapters.forEach(ch=>ch.knowledge_ids=k.filter(k=>k.chapter===ch.id).map(k=>k.id));return {version:pack.version,title:pack.title,customContent:true,questions:q,knowledge:k,chapters,examProfiles:clone(pack.examProfiles.filter(x=>x.enabled)),resources:clone(pack.resources)};}
function merge(current,incoming){validate(incoming);const p=clone(current);p.version=incoming.version;p.title=incoming.title;for(const key of arrays){const map=new Map(p[key].map(x=>[x.id,x]));incoming[key].forEach(x=>map.set(x.id,clone(x)));p[key]=[...map.values()];}validate(p);return p;}
function examPool(profile,bank,rng=Math.random){const p={questions:bank.questions};let list=examCandidates(profile,p);if(list.length<profile.count)throw Error('考試可用題目不足');for(let i=list.length-1;i>0;i--){const j=Math.floor(rng()*(i+1));[list[i],list[j]]=[list[j],list[i]];}return list.slice(0,profile.count);}
const api={KEYS,types,clone,fromBank,inspect,validate,signature,assertRevisions,envelope,expand,read,saveDraft,install,toBank,merge,examPool,calcError};root.HVAC_CONTENT=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
