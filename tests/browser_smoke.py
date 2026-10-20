"""Real-browser acceptance suite. Requires Playwright + an installed browser.
Windows default: installed Edge. Linux default: /usr/bin/chromium.
A failed launch returns 77 (BLOCKED), never a passing result.
"""
import os,sys,json,tempfile,pathlib,traceback,threading,functools
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parents[1]
results=[]
def ok(name):results.append({'name':name,'status':'passed'});print('PASS',name)
def options():
 if os.environ.get('HVAC_BROWSER'):return {'executable_path':os.environ['HVAC_BROWSER'],'timezone_id':'America/Toronto'}
 return {'channel':'msedge','timezone_id':'America/Toronto'} if os.name=='nt' else {'executable_path':'/usr/bin/chromium','args':['--no-sandbox'],'timezone_id':'America/Toronto'}
class QuietHandler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
class LocalServer:
 def __enter__(self):
  self.server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT/'app')))
  threading.Thread(target=self.server.serve_forever,daemon=True).start()
  return 'http://127.0.0.1:'+str(self.server.server_port)
 def __exit__(self,*args):self.server.shutdown();self.server.server_close()

def run():
 errors=[];external=[]
 with LocalServer() as url,tempfile.TemporaryDirectory(prefix='hvac-browser-') as profile,sync_playwright() as p:
  try:ctx=p.chromium.launch_persistent_context(profile,headless=True,**options())
  except Exception as exc:
   results.append({'name':'browser_launch','status':'blocked','reason':str(exc)[:1200]});return 77
  page=ctx.new_page();page.on('pageerror',lambda x:errors.append(str(x)))
  page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) and not r.url.startswith(url+'/') else None)
  ctx.route('**/*',lambda r:r.continue_() if r.request.url.startswith(url+'/') else r.abort());page.goto(url+'/');page.locator('h1').filter(has_text='今天').wait_for();ctx.set_offline(True);ok('local load with external network blocked; practice runs offline')
  page.locator('nav [data-act="nav"][data-page="practice"]').click()
  page.select_option('#practice-mode','chapter');page.select_option('#practice-chapter','2');page.fill('#practice-count','2');page.locator('[data-act="start-practice"]').click()
  assert page.locator('.translation').count()==0
  assert page.locator('[data-testid="explanation"]').count()==0
  page.locator('[data-act="translation"]').click();assert page.locator('.translation').count()>0
  page.locator('[data-act="translation"]').click();assert page.locator('.translation').count()==0;ok('English default, translation toggle and hidden answer')
  qid=page.evaluate("JSON.parse(localStorage.getItem('hvac122.learning.v2')).session.items[0].id")
  bad=page.evaluate('(id)=>{const q=HVAC_BANK.questions.find(q=>q.id===id);return q.choices.find(c=>c.id!==q.correct_choice).id}',qid)
  page.locator('[data-act="choose"][data-id="'+bad+'"]').click();page.locator('[data-act="submit"]').click()
  assert page.locator('[data-testid="explanation"]').count()==1
  assert 'Incorrect' in page.locator('[data-testid="explanation"]').inner_text();ok('submitted result and full explanation')
  page.locator('[data-reason]').select_option(label='計算錯誤')
  ctx.set_offline(False);page.reload();page.locator('[data-testid="explanation"]').wait_for();ctx.set_offline(True);assert 'Incorrect' in page.locator('[data-testid="explanation"]').inner_text();ok('reload preserves answer and wrong record')
  ctx.close()
  ctx=p.chromium.launch_persistent_context(profile,headless=True,**options());ctx.route('**/*',lambda r:r.continue_() if r.request.url.startswith(url+'/') else r.abort());page=ctx.new_page();page.on('pageerror',lambda x:errors.append(str(x)));page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) and not r.url.startswith(url+'/') else None);page.goto(url+'/');page.locator('[data-testid="explanation"]').wait_for();ctx.set_offline(True)
  assert 'Incorrect' in page.locator('[data-testid="explanation"]').inner_text();assert page.locator('[data-reason]').input_value()=='計算錯誤';ok('actual browser process restart preserves learning data')
  page.locator('[data-act="end-session"]').click();page.locator('[data-act="nav"][data-page="exam"]').click();page.select_option('#exam-count','custom');page.fill('#exam-custom','2');page.locator('[data-act="start-exam"]').click()
  for i in range(2):
   page.locator('[data-act="choose"]').first.click();assert page.locator('[data-testid="explanation"]').count()==0
   assert '正確答案：' not in page.locator('main').inner_text()
   if i==0:page.locator('[data-act="flag"]').click();page.locator('[data-act="next"]').click()
  assert page.evaluate("JSON.parse(localStorage.getItem('hvac122.learning.v2')).attempts.length")==1
  page.locator('[data-act="exam-submit-preview"]').click();page.locator('[data-act="finish-exam"]').click();assert '模擬考成績與解析' in page.locator('main').inner_text();ok('exam withholds all scoring until hand-in')
  page.locator('[data-act="nav"][data-page="settings"]').click()
  with page.expect_download() as d:page.locator('[data-act="export"]').click()
  saved=pathlib.Path(profile)/'backup.json';d.value.save_as(saved)
  backup=json.loads(saved.read_text());assert len(backup['attempts'])==3
  page.locator('#import').set_input_files(saved);page.locator('[data-act="confirm-import"]').wait_for();page.locator('[data-act="confirm-import"]').click();ok('browser export and restore')
  page.locator('[data-act="nav"][data-page="knowledge"]').click();page.fill('#kb-query','電容');page.locator('[data-act="search-k"]').click();assert '電容' in page.locator('main').inner_text();ok('Chinese knowledge search')
  for width,height,label in [(1440,1000,'desktop'),(390,844,'mobile')]:
   page.set_viewport_size({'width':width,'height':height});page.locator('[data-act="nav"][data-page="home"]').click()
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
   page.screenshot(path=str(ROOT/'reports'/('screenshot-'+label+'.png')),full_page=True);ok(label+' no horizontal overflow')
  assert not errors,errors;assert not external,external;ok('zero script errors and zero external requests while offline');ctx.close();return 0
if __name__=='__main__':
 try:code=run()
 except PermissionError as exc:results.append({'name':'local_browser_environment','status':'blocked','reason':str(exc)});code=77
 except Exception as exc:results.append({'name':'browser_flow','status':'failed','reason':str(exc)});traceback.print_exc();code=1
 (ROOT/'reports/browser-results.json').write_text(json.dumps({'exitCode':code,'results':results},ensure_ascii=False,indent=2),encoding='utf-8');sys.exit(code)
