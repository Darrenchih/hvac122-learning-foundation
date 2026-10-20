/* Pure domain logic shared by browser and Node tests; no network dependencies. */
(function(root){
'use strict';
const DAY=86400000, VERSION=2, STORAGE='hvac122.learning.v2';
const fresh=()=>({schemaVersion:VERSION,bankVersion:'2.0.0',attempts:[],reviews:{},manualReasons:{},exams:[],session:null,settings:{font:18}});
const uid=()=>globalThis.crypto?.randomUUID?.()||'a-'+Date.now()+'-'+Math.random().toString(16).slice(2);
function shuffle(a,rng=Math.random){a=[...a];for(let i=a.length-1;i>0;i--){let j=Math.floor(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function prepare(q,rng){return {id:q.id,order:shuffle(q.choices.map(c=>c.id),rng),selected:null,submitted:false,translation:false,everTranslation:false,elapsed:0,flagged:false};}
function schedule(old,correct,now){
 const r=old?{...old}:{everWrong:false,errors:0,stage:0,due:now,last:0,lastAdvance:0};
 if(!correct){r.everWrong=true;r.errors++;r.stage=0;r.lastAdvance=now;r.due=now+DAY;}
 else if(!old){r.due=now+DAY;r.lastAdvance=now;}
 else if(now>=r.due && now-r.lastAdvance>=DAY){r.stage=Math.min(4,r.stage+1);r.lastAdvance=now;r.due=now+[1,3,7,14,30][r.stage]*DAY;}
 r.last=now;return r;
}
function record(state,q,item,now=Date.now(),mode='practice'){
 if(item.submitted) return null;
 const a={id:uid(),questionId:q.id,knowledgeIds:[...q.knowledge_ids],chapter:q.chapter,type:q.type,bankVersion:state.bankVersion,selected:item.selected,correct:item.selected===q.correct_choice,usedTranslation:!!item.everTranslation,durationMs:Math.max(0,item.elapsed||0),at:now,mode};
 state.attempts.push(a);state.reviews[q.id]=schedule(state.reviews[q.id],a.correct,now);item.submitted=true;item.attemptId=a.id;return a;
}
function firstAttempts(attempts){let seen=new Set();return attempts.filter(a=>{if(seen.has(a.questionId))return false;seen.add(a.questionId);return true;});}
function accuracy(a){return a.length?Math.round(100*a.filter(x=>x.correct).length/a.length):null;}
function mastery(kid,attempts,now=Date.now()){
 let a=attempts.filter(x=>x.knowledgeIds.includes(kid)),first=firstAttempts(a),ids=new Set(a.map(x=>x.questionId));
 let last=new Map();a.forEach(x=>last.set(x.questionId,x));let distinct=[...last.values()];
 const good=distinct.filter(x=>x.correct&&!x.usedTranslation&&x.durationMs<=90000);
 const recovered=good.filter(x=>a.some(y=>y.questionId===x.questionId&&x.at-y.at>=7*DAY)).length>=3;
 const applied=good.some(x=>['application','calculation'].includes(x.type));
 const delayed=a.some(x=>x.correct&&!x.usedTranslation&&a.some(y=>y.questionId!==x.questionId&&x.at-y.at>=7*DAY));
 let level=0;
 if(a.length)level=1;
 if(ids.size>=3&&good.length>=3&&accuracy(distinct)>=75&&(accuracy(first)>=60||recovered)&&applied)level=2;
 if(level===2&&ids.size>=3&&accuracy(distinct)>=90&&(accuracy(first)>=75||recovered)&&delayed)level=3;
 return {level,label:['尚未掌握','學習中','基本掌握','熟練掌握'][level],unique:ids.size,first:accuracy(first),latest:accuracy(distinct)};
}
function priority(q,state,now=Date.now()){
 const a=state.attempts.filter(x=>x.knowledgeIds.some(k=>q.knowledge_ids.includes(k)));
 const r=state.reviews[q.id];const wrong=a.filter(x=>!x.correct).length;
 return wrong*8+(r?Math.max(0,(now-r.due)/DAY):2)+a.filter(x=>x.usedTranslation).length*2+a.filter(x=>x.durationMs>90000).length*2+(3-mastery(q.knowledge_ids[0],state.attempts).level)*3;
}
function pool(bank,state,{mode='mixed',chapter='',knowledge='',count=20},now=Date.now()){
 let a=bank.questions.filter(q=>q.eligible&&(!chapter||q.chapter===Number(chapter))&&(!knowledge||q.knowledge_ids.includes(knowledge)));
 let done=new Set(state.attempts.map(x=>x.questionId));
 if(mode==='wrong')a=a.filter(q=>state.reviews[q.id]?.everWrong&&state.reviews[q.id].stage<3);
 if(mode==='new')a=a.filter(q=>!done.has(q.id));
 if(mode==='calculation')a=a.filter(q=>q.type==='calculation');
 if(mode==='due')a=a.filter(q=>state.reviews[q.id]?.due<=now);
 if(['weak','due','wrong'].includes(mode))a=shuffle(a).sort((x,y)=>priority(y,state,now)-priority(x,state,now));else a=shuffle(a);
 return a.slice(0,Math.max(1,Math.min(300,Number(count)||20)));
}
const REASONS=['英文題目看不懂','不理解電學原理','計算錯誤','混淆相似概念','粗心','猜測答案'];
function validateState(s){
 if(!s||s.schemaVersion!==VERSION||typeof s.bankVersion!=='string'||!Array.isArray(s.attempts)||!s.reviews||typeof s.reviews!=='object'||Array.isArray(s.reviews)||!Array.isArray(s.exams)||!s.manualReasons||typeof s.manualReasons!=='object')throw Error('備份格式或版本不支援');
 if(s.attempts.length>200000)throw Error('備份過大');
 let ids=new Set();for(const a of s.attempts){
  if(!a||typeof a.id!=='string'||ids.has(a.id)||typeof a.questionId!=='string'||!Array.isArray(a.knowledgeIds)||!a.knowledgeIds.every(x=>typeof x==='string')||typeof a.correct!=='boolean'||typeof a.usedTranslation!=='boolean'||!Number.isFinite(a.at)||!Number.isFinite(a.durationMs)||a.durationMs<0||!Number.isInteger(a.chapter)||a.chapter<1||a.chapter>5||!['A','B','C','D',null].includes(a.selected)||!['recall','understanding','application','calculation'].includes(a.type))throw Error('作答紀錄格式錯誤');
  ids.add(a.id);
 }
 for(const [key,r] of Object.entries(s.reviews)){if(!key||!r||typeof r.everWrong!=='boolean'||!Number.isInteger(r.errors)||r.errors<0||!Number.isInteger(r.stage)||r.stage<0||r.stage>4||![r.due,r.last,r.lastAdvance].every(Number.isFinite))throw Error('複習排程格式錯誤');}
 for(const [aid,reason] of Object.entries(s.manualReasons)){if(!ids.has(aid)||!REASONS.includes(reason))throw Error('錯因標記格式錯誤');}
 for(const e of s.exams){if(!e||typeof e.id!=='string'||!Number.isFinite(e.at)||!Array.isArray(e.attemptIds)||!e.attemptIds.every(x=>ids.has(x)))throw Error('考試紀錄格式錯誤');}
 if(!s.settings||![16,18,20,22,24].includes(s.settings.font))throw Error('字型設定格式錯誤');
 if(s.session!==null){const x=s.session;if(!x||!['practice','exam'].includes(x.mode)||!Array.isArray(x.items)||!x.items.length||x.items.length>300||!Number.isInteger(x.index)||x.index<0||x.index>=x.items.length||!Number.isFinite(x.startedAt)||!(x.limitMs===null||Number.isFinite(x.limitMs)&&x.limitMs>0)||!Number.isFinite(x.lastTick)||typeof x.finished!=='boolean')throw Error('練習階段格式錯誤');
  for(const t of x.items){if(typeof t.id!=='string'||!Array.isArray(t.order)||new Set(t.order).size!==4||t.order.some(c=>!'ABCD'.includes(c))||!['A','B','C','D',null].includes(t.selected)||typeof t.submitted!=='boolean'||typeof t.everTranslation!=='boolean'||typeof t.translation!=='boolean'||typeof t.flagged!=='boolean'||!Number.isFinite(t.elapsed)||t.elapsed<0)throw Error('練習題狀態錯誤');}
 }
 return s;
}
function save(storage,state){validateState(state);storage.setItem(STORAGE,JSON.stringify(state));}
function restore(storage){const raw=storage.getItem(STORAGE);return raw?validateState(JSON.parse(raw)):fresh();}
function finishExam(state,bank,now=Date.now()){
 const s=state.session;if(!s||s.mode!=='exam'||s.finished)return null;
 let ids=[];for(const item of s.items){const q=bank.questions.find(q=>q.id===item.id);if(!q)throw Error('考試題目版本已變更，請還原原題庫或保留紀錄後結束階段');const a=record(state,q,item,now,'exam');if(a)ids.push(a.id);}
 const e={id:uid(),at:now,attemptIds:ids,durationMs:now-s.startedAt,limitMs:s.limitMs};state.exams.push(e);s.finished=true;return e;
}
const api={DAY,STORAGE,REASONS,fresh,uid,shuffle,prepare,schedule,record,firstAttempts,accuracy,mastery,priority,pool,validateState,save,restore,finishExam};
root.HVAC_CORE=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
