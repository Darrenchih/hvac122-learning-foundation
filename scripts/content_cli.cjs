#!/usr/bin/env node
/* Offline AI/developer entrypoint. Never alters the original project or learning data. */
const fs=require('node:fs'),path=require('node:path'),M=require('../app/content.js');
const root=path.resolve(__dirname,'..'),read=p=>JSON.parse(fs.readFileSync(p,'utf8')),write=(p,data)=>{if(fs.existsSync(p))throw Error('Output file already exists; choose a new filename.');fs.writeFileSync(p,JSON.stringify(data,null,2),'utf8');};
function builtIn(){return M.fromBank({version:'2.0.0',questions:read(path.join(root,'data/questions.json')),knowledge:read(path.join(root,'data/knowledge.json')),chapters:read(path.join(root,'data/chapters.json'))});}
try{
 const [command,...args]=process.argv.slice(2);
 if(command==='export'&&args.length===1){write(args[0],builtIn());console.log('Exported full built-in content pack:',args[0]);}
 else if(command==='validate'&&args.length===1){const p=M.validate(read(args[0]));console.log(JSON.stringify(M.inspect(p),null,2));}
 else if(command==='merge'&&args.length===3){const before=M.validate(read(args[0])),next=M.merge(before,read(args[1]));M.assertRevisions(next,before);write(args[2],next);console.log('Merged content pack:',args[2]);}
 else if(command==='build'&&args.length===2){
  const pack=M.validate(read(args[0])),out=path.resolve(args[1]);if(fs.existsSync(out))throw Error('Output directory already exists; choose a new directory. No existing app is overwritten.');
  const bank=M.toBank(pack);fs.mkdirSync(path.join(out,'app'),{recursive:true});
  for(const name of fs.readdirSync(path.join(root,'app')))if(fs.statSync(path.join(root,'app',name)).isFile())fs.copyFileSync(path.join(root,'app',name),path.join(out,'app',name));
  fs.writeFileSync(path.join(out,'app/bank.js'),'window.HVAC_BANK = '+JSON.stringify(bank)+';\n','utf8');
  for(const name of ['Start.ps1','開始練習.cmd','FOUNDATION.md'])fs.copyFileSync(path.join(root,name),path.join(out,name));
  write(path.join(out,'content-pack.json'),pack);console.log('Built app with',bank.questions.length,'enabled questions at',out);
 }else{console.error('Usage:\n node scripts/content_cli.cjs export output.json\n node scripts/content_cli.cjs validate pack.json\n node scripts/content_cli.cjs merge current.json incoming.json output.json\n node scripts/content_cli.cjs build pack.json NEW_OUTPUT_DIRECTORY');process.exitCode=1;}
}catch(error){console.error(error.message);process.exitCode=1;}
