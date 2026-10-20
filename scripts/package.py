"""Package local deliverables only; never uploads any content."""
import pathlib,zipfile,hashlib,json,sys,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
files=[p for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name!='delivery_manifest.json']
manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
mp=ROOT/'reports/delivery_manifest.json';mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');files.append(mp)
name=sys.argv[1] if len(sys.argv)>1 else 'HVAC122_OpenSource_v2_1'
if not re.fullmatch(r'[A-Za-z0-9_-]+',name):raise ValueError('Invalid package name')
out=ROOT.parent/(name+'.zip')
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files:z.write(p,name+'/'+str(p.relative_to(ROOT)))
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(files)
 for name,digest in manifest.items():assert hashlib.sha256(z.read(out.stem+'/'+name)).hexdigest()==digest
sha=hashlib.sha256(out.read_bytes()).hexdigest();out.with_suffix('.zip.sha256').write_text(sha+'  '+out.name+'\n')
print(out,'bytes',out.stat().st_size,'files',len(files));print('SHA256',sha)
