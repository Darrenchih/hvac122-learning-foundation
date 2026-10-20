/* Local original files: stored separately from content JSON in IndexedDB. */
(function(root){
'use strict';
function db(){return new Promise((resolve,reject)=>{if(!root.indexedDB){reject(Error('此瀏覽器無法使用本機附件儲存；可改貼教材文字。'));return;}const req=root.indexedDB.open('hvac122.materials.v1',1);req.onupgradeneeded=()=>req.result.createObjectStore('files',{keyPath:'id'});req.onerror=()=>reject(req.error);req.onblocked=()=>reject(Error('請關閉其他內容管理分頁後重試'));req.onsuccess=()=>resolve(req.result);});}
async function op(mode,action){const d=await db();return new Promise((resolve,reject)=>{const tx=d.transaction('files',mode);let result;try{const req=action(tx.objectStore('files'));req.onsuccess=()=>result=req.result;}catch(e){d.close();reject(e);return;}tx.oncomplete=()=>{d.close();resolve(result);};tx.onerror=()=>{d.close();reject(tx.error||Error('附件儲存失敗'));};tx.onabort=()=>{d.close();reject(tx.error||Error('附件交易已取消'));};});}
async function put(file,kind,chapter){if(!file||file.size>25*1024*1024)throw Error('單份附件上限 25 MB');if(!['lecture','lab','exam','other'].includes(kind))throw Error('附件分類無效');const record={id:'FILE-'+root.crypto.randomUUID(),name:file.name,type:file.type||'application/octet-stream',size:file.size,kind,chapter,at:Date.now(),blob:file};await op('readwrite',s=>s.put(record));return record.id;}
root.HVAC_MATERIALS={put,list:()=>op('readonly',s=>s.getAll()),get:id=>op('readonly',s=>s.get(id)),remove:id=>op('readwrite',s=>s.delete(id))};
})(typeof window!=='undefined'?window:globalThis);
