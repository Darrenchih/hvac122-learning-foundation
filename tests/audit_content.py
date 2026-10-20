import pathlib,json,tempfile,subprocess,unittest
from jsonschema import Draft202012Validator
ROOT=pathlib.Path(__file__).resolve().parents[1]
class ContentContractAudit(unittest.TestCase):
 def run_cli(self,*args):return subprocess.run(['node',str(ROOT/'scripts/content_cli.cjs'),*map(str,args)],capture_output=True,text=True,encoding='utf-8',timeout=30)
 def test_content_schema_and_example(self):
  schema=json.loads((ROOT/'templates/content-pack.schema.json').read_text());Draft202012Validator.check_schema(schema);Draft202012Validator(schema).validate(json.loads((ROOT/'templates/content-pack.example.json').read_text()))
 def test_example_passes_runtime_validator(self):
  p=self.run_cli('validate',ROOT/'templates/content-pack.example.json');self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(json.loads(p.stdout)['stats']['enabled'],0)
 def test_exported_full_bank_validates_against_contract(self):
  with tempfile.TemporaryDirectory() as d:
   out=pathlib.Path(d)/'full.json';p=self.run_cli('export',out);self.assertEqual(p.returncode,0,p.stderr);schema=json.loads((ROOT/'templates/content-pack.schema.json').read_text());Draft202012Validator(schema).validate(json.loads(out.read_text()));self.assertEqual(self.run_cli('validate',out).returncode,0);before=out.read_bytes();self.assertNotEqual(self.run_cli('export',out).returncode,0);self.assertEqual(out.read_bytes(),before)
 def test_cli_build_preserves_engine_and_never_overwrites_output(self):
  with tempfile.TemporaryDirectory() as d:
   out=pathlib.Path(d)/'new-app';p=self.run_cli('build',ROOT/'templates/content-pack.example.json',out);self.assertEqual(p.returncode,0,p.stderr)
   self.assertEqual((out/'app/core.js').read_bytes(),(ROOT/'app/core.js').read_bytes());self.assertTrue((out/'開始練習.cmd').is_file());self.assertTrue((out/'content-pack.json').is_file());original=(out/'app/bank.js').read_bytes();self.assertNotEqual(self.run_cli('build',ROOT/'templates/content-pack.example.json',out).returncode,0);self.assertEqual(original,(out/'app/bank.js').read_bytes())
 def test_management_assets_are_local_and_served_by_launcher(self):
  import re
  launcher=(ROOT/'Start.ps1').read_text()
  for html in ['index.html','manage.html']:
   for name in re.findall(r'(?:src|href)="([^"]+)"',(ROOT/'app'/html).read_text()):
    self.assertTrue((ROOT/'app'/name).is_file());self.assertIn("'"+name+"'",launcher)
  for name in ['index.html','manage.html']:self.assertIn("'"+name+"'",launcher)
 def test_material_limits_and_storage_are_explicit(self):
  s=(ROOT/'app/materials.js').read_text();self.assertIn('indexedDB.open',s);self.assertIn('25*1024*1024',s);self.assertNotIn('fetch(',s)
  docs=(ROOT/'FOUNDATION.md').read_text();self.assertIn('內容包不包含附件',docs);self.assertIn('hvac122.learning.v2',docs)
if __name__=='__main__':unittest.main(verbosity=2)
