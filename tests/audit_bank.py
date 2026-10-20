"""Offline structural audit plus independent numeric and dimensional checks."""
import json,pathlib,unittest,math,re,collections,itertools,hashlib
from jsonschema import Draft202012Validator
ROOT=pathlib.Path(__file__).resolve().parents[1]
Q=json.loads((ROOT/'data/questions.json').read_text());K=json.loads((ROOT/'data/knowledge.json').read_text());KM={k['id']:k for k in K}
# Independent evaluator: never eval author-provided work strings.
MODELS={
'ohm_current':(lambda x:x['V']/x['R'],'A'), 'ohm_voltage':(lambda x:x['I']*x['R'],'V'), 'ohm_resistance':(lambda x:x['V']/x['I'],'Ω'),
'power_vi':(lambda x:x['V']*x['I'],'W'),'power_i2r':(lambda x:x['I']**2*x['R'],'W'),'power_v2r':(lambda x:x['V']**2/x['R'],'W'),
'power_pf':(lambda x:x['V']*x['I']*x['PF'],'W'),'energy':(lambda x:x['P']*x['h']/1000,'kWh'),'horsepower':(lambda x:x['hp']*746/x['efficiency'],'W'),
'series':(lambda x:sum([x['R1'],x['R2']]),'Ω'),'divider':(lambda x:x['V']/(x['R1']+x['R2'])*x['R2'],'V'),
'parallel':(lambda x:1/(1/x['R1']+1/x['R2']),'Ω'),'current_sum':(lambda x:sum([x['I1'],x['I2']]),'A'),
'clamp':(lambda x:x['reading']/x['turns'],'A'),'tolerance':(lambda x:x['nominal']*x['percent']/100,'Ω')}
def norm(s):return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()
def tokens(s):
 s=re.sub(r'\d+(?:\.\d+)?',' NUMBER ',s)
 return set(re.findall(r'[a-z]+',s.lower()))-set('a an the is are of in to what which how does do for with and or at as on it be by its'.split())
def candidates():
 result=[]
 for a,b in itertools.combinations(Q,2):
  aa,bb=tokens(a['question_en']),tokens(b['question_en']);score=len(aa&bb)/len(aa|bb) if aa|bb else 0
  if score>=.60:
   param=a['type']==b['type']=='calculation' and a['calculation']['model']==b['calculation']['model']
   result.append({'a':a['id'],'b':b['id'],'similarity':round(score,3),'classification':'intentional_parameter_variant' if param else 'manual_review_candidate','a_en':a['question_en'],'b_en':b['question_en']})
 return result
class BankAudit(unittest.TestCase):
 def test_json_schema(self):
  schema=json.loads((ROOT/'data/question.schema.json').read_text());Draft202012Validator.check_schema(schema);Draft202012Validator(schema).validate(Q)
 def test_four_unique_choices_one_correct(self):
  for q in Q:
   with self.subTest(q=q['id']):
    self.assertEqual(set(c['id'] for c in q['choices']),set('ABCD'));self.assertEqual(len(q['choices']),4)
    self.assertEqual(sum(c['id']==q['correct_choice'] for c in q['choices']),1)
    self.assertEqual(len(set(c['text_en'].lower().strip() for c in q['choices'])),4)
 def test_stable_unique_ids_and_links(self):
  self.assertEqual(len({q['id'] for q in Q}),len(Q));self.assertEqual(len(KM),74)
  for q in Q:
   for kid in q['knowledge_ids']:
    self.assertIn(kid,KM);self.assertEqual(q['chapter'],KM[kid]['chapter']);self.assertIn(q['id'],KM[kid]['related_question_ids'])
 def test_bilingual_complete(self):
  for q in Q:
   for x in [q['question_zh'],q['explanation_zh']]+[c['text_zh'] for c in q['choices']]+[r['zh'] for r in q['choice_explanations'].values()]:
    self.assertTrue(x.strip());self.assertTrue(re.search('[\u4e00-\u9fff]',x) or q['type']=='calculation' or re.search(r'\d|[=Ω]',x),x)
 def test_all_calculations_independent_numeric_units(self):
  calcs=[q for q in Q if q['type']=='calculation'];self.assertEqual(len(calcs),45)
  for q in calcs:
   c=q['calculation'];fn,unit=MODELS[c['model']];expected=fn(c['inputs']);self.assertEqual(c['unit'],unit);self.assertTrue(math.isclose(expected,c['answer'],rel_tol=1e-12))
   self.assertTrue(all(v>0 for v in c['inputs'].values()))
   option=next(o for o in q['choices'] if o['id']==q['correct_choice']);value,shown_unit=option['text_en'].split(' ')
   self.assertEqual(shown_unit,unit);self.assertTrue(math.isclose(float(value),expected,rel_tol=c['tolerance'],abs_tol=1e-6))
   matches=[o for o in q['choices'] if o['text_en'].endswith(' '+unit) and math.isclose(float(o['text_en'].split()[0]),expected,rel_tol=c['tolerance'],abs_tol=1e-6)]
   self.assertEqual(len(matches),1)
 def test_no_exact_or_word_order_duplicates(self):
  seen={};bags={}
  for q in Q:
   key=norm(q['question_en']);self.assertNotIn(key,seen);seen[key]=q['id']
   bag=tuple(sorted(key.split()));self.assertNotIn(bag,bags);bags[bag]=q['id']
 def test_near_duplicate_detector(self):
  self.assertEqual(tokens('What is 24 V?'),tokens('What is 120 V?'))
  cs=candidates();self.assertTrue(any(x['classification']=='intentional_parameter_variant' for x in cs))
  # Detection is a software check, not a claim of human clearance.
  (ROOT/'reports/near_duplicates.json').write_text(json.dumps(cs,ensure_ascii=False,indent=2),encoding='utf-8')
 def test_required_knowledge_fields_and_coverage(self):
  fields=['id','chapter','topic_key','term_en','term_zh','definition_en','explanation_zh','hvac_application','related_formulas','common_misconceptions','source_reference','verification_status','content_class']
  for k in K:
   for f in fields:self.assertIn(f,k)
   self.assertGreaterEqual(len(k['related_question_ids']),3)
   self.assertTrue(any(q['type'] in ['application','calculation'] and k['id'] in q['knowledge_ids'] for q in Q))
 def test_type_mix_and_answer_key_distribution(self):
  self.assertEqual(dict(collections.Counter(q['type'] for q in Q)),{'recall':60,'understanding':105,'application':90,'calculation':45})
  counts=collections.Counter(q['correct_choice'] for q in Q);self.assertEqual(len(counts),4);self.assertTrue(all(40<=v<=110 for v in counts.values()))
 def test_offline_asset_closure(self):
  html=(ROOT/'app/index.html').read_text();links=re.findall(r'(?:src|href)="([^"]+)"',html)
  for link in links:self.assertTrue((ROOT/'app'/link).is_file());self.assertFalse(re.match(r'https?:',link))
  for name in ['app.js','core.js','content.js','content-loader.js','manage.js','materials.js','style.css']:
   source=(ROOT/'app'/name).read_text();self.assertNotRegex(source,r'\bfetch\s*\(|XMLHttpRequest|@import|https?://')
 def test_source_honesty(self):
  for q in Q:self.assertFalse(q['original_teacher_question']);self.assertFalse(q['source_reference']['original_verified']);self.assertIn('pending',q['verification_status'])
 def test_private_sources_are_excluded_from_public_distribution(self):
  for p in ROOT.rglob('*'):
   if p.is_file():
    self.assertNotIn('source',p.relative_to(ROOT).parts)
    self.assertNotIn(p.suffix.lower(),['.zip','.pdf','.pptx','.docx','.pem','.key'])
  self.assertTrue((ROOT/'content/knowledge.seed.json').is_file())
if __name__=='__main__':unittest.main(verbosity=2)
