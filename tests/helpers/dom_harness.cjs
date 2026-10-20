const vm=require('node:vm'),fs=require('node:fs');
function boot(shared=new Map(), mode='learner'){
 let rootHtml='',listeners={},docListeners={},windowListeners={},cache=new Map();
 const decode=s=>s.replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
 const storage={getItem:k=>shared.get(k)||null,setItem:(k,v)=>shared.set(k,v),removeItem:k=>shared.delete(k)};
 const app={addEventListener:(type,fn)=>listeners[type]=fn,get innerHTML(){return rootHtml;},set innerHTML(v){rootHtml=v;cache.clear();}};
 const toast={textContent:'',style:{}};
 function click(act,data={}){return listeners.click({preventDefault(){},target:{closest:()=>({dataset:mode==='manager'?{action:act,...data}:{act,...data}})}});}
 function query(sel){
  if(sel==='#app'||sel==='#manager')return app;if(sel==='#toast')return toast;if(sel==='main')return app;
  if(cache.has(sel))return cache.get(sel);
  if(sel.startsWith('#')){
   const id=sel.slice(1),area=rootHtml.match(new RegExp('<textarea[^>]*id="'+id+'"[^>]*>([\\s\\S]*?)</textarea>'));if(area){const el={value:decode(area[1]),tagName:'TEXTAREA'};cache.set(sel,el);return el;}const select=rootHtml.match(new RegExp('<select[^>]*id="'+id+'"[^>]*>([\\s\\S]*?)</select>'));
   if(select){const opts=[...select[1].matchAll(/<option([^>]*)>([\s\S]*?)<\/option>/g)];let chosen=opts.find(x=>/\bselected\b/.test(x[1]))||opts[0];let val=chosen?((chosen[1].match(/value="([^"]*)"/)||[])[1]??chosen[2]):'';let el={value:decode(val),tagName:'SELECT'};cache.set(sel,el);return el;}
   const match=rootHtml.match(new RegExp('<[^>]*id="'+id+'"[^>]*>'));
   if(match){let el={value:decode((match[0].match(/value="([^"]*)"/)||[])[1]||''),checked:/\bchecked\b/.test(match[0]),tagName:'INPUT',innerHTML:'',textContent:''};cache.set(sel,el);return el;}
   return null;
  }
  if(sel.startsWith('[data-act=')){const act=sel.match(/data-act="([^"]+)"/)?.[1],id=sel.match(/data-id="([^"]+)"/)?.[1];if(!rootHtml.includes('data-act="'+act+'"'))return null;return {click:()=>click(act,id?{id}:{}),tagName:'BUTTON'};}
  return null;
 }
 const document={querySelector:query,documentElement:{style:{setProperty(){}}},hidden:false,body:{},addEventListener:(t,fn)=>docListeners[t]=fn,createElement:()=>({click(){},href:'',download:''})};
 const context={console,document,localStorage:storage,setTimeout(){},setInterval(){},Date,Math,Map,Set,Blob,URL,crypto:require('node:crypto').webcrypto};
 context.window=context;context.location={href:''};context.addEventListener=(t,fn)=>windowListeners[t]=fn;vm.createContext(context);
 for(const file of (mode==='manager'?['bank.js','content.js','materials.js','manage.js']:['bank.js','content.js','content-loader.js','core.js','app.js']))vm.runInContext(fs.readFileSync(__dirname+'/../../app/'+file,'utf8'),context,{filename:file});
 return {click,query,html:()=>rootHtml,toast:()=>toast.textContent,shared,state:()=>JSON.parse(storage.getItem('hvac122.learning.v2')||'null'),change:(el)=>listeners.change({target:el}),close:()=>windowListeners.beforeunload?.(),key:(key,altKey=false)=>docListeners.keydown({key,altKey,target:document.body,preventDefault(){}}),context};
}

module.exports={boot};
