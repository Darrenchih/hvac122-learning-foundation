"""Real browser management/learning/attachment smoke test on a single HTTP origin.
No external requests or uploads. Binding/browser failures are BLOCKED (77).
"""
import pathlib,tempfile,threading,json,sys,functools,hashlib,traceback
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from browser_smoke import options
ROOT=pathlib.Path(__file__).resolve().parents[1];results=[]
def passed(name):results.append({'name':name,'status':'passed'});print('PASS',name)
class QuietHandler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def run():
 try:server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT/'app')))
 except Exception as exc:results.append({'name':'loopback_http_server','status':'blocked','reason':str(exc)});return 77
 threading.Thread(target=server.serve_forever,daemon=True).start();url='http://127.0.0.1:'+str(server.server_port)
 try:
  with tempfile.TemporaryDirectory(prefix='hvac-content-browser-') as profile,sync_playwright() as p:
   try:ctx=p.chromium.launch_persistent_context(profile,headless=True,**options())
   except Exception as exc:results.append({'name':'browser_launch','status':'blocked','reason':str(exc)[:1000]});return 77
   ctx.route('**/*',lambda route:route.continue_() if route.request.url.startswith(url+'/') else route.abort());page=ctx.new_page();errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
   page.goto(url+'/');page.locator('[data-act="nav"][data-page="manage"]').click();page.locator('h1').filter(has_text='內容總覽').wait_for();passed('open management from learning app')
   page.locator('[data-action="tab"][data-id="questions"]').click();page.locator('[data-action="new"]').click()
   q=page.evaluate('HVAC_BANK.questions[0]');page.fill('#id','USER-BROWSER-Q');page.select_option('#chapter',str(q['chapter']));page.select_option('#kid',q['knowledge_ids'][0]);page.fill('#topic',q['topic']);page.fill('#q-en','Added browser test: '+q['question_en']);page.fill('#q-zh','新增測試：'+q['question_zh']);page.select_option('#correct',q['correct_choice']);page.fill('#ex-en',q['explanation_en']);page.fill('#ex-zh',q['explanation_zh'])
   for c in q['choices']:
    page.fill('#'+c['id']+'-en',c['text_en']);page.fill('#'+c['id']+'-zh',c['text_zh']);page.fill('#'+c['id']+'-reason-en',q['choice_explanations'][c['id']]['en']);page.fill('#'+c['id']+'-reason-zh',q['choice_explanations'][c['id']]['zh'])
   page.locator('#eligible').check();page.locator('[data-action="save-item"]').click();page.wait_for_function("localStorage.getItem('hvac122.content.draft.v1')!==null")
   page.locator('[data-action="tab"][data-id="home"]').click();page.locator('[data-action="publish-preview"]').click();page.locator('[data-action="publish"]').click();page.locator('a[href="index.html"]').click();assert page.evaluate('HVAC_BANK.questions.length')==301;passed('manual authoring and publication visible in learning bank')
   page.locator('[data-act="nav"][data-page="manage"]').click();page.locator('[data-action="tab"][data-id="resources"]').click();payload=b'Local original course notes - browser acceptance test.'
   page.locator('#attachment').set_input_files({'name':'acceptance-notes.txt','mimeType':'text/plain','buffer':payload});page.locator('.row').filter(has_text='acceptance-notes.txt').wait_for();passed('save original local attachment to IndexedDB')
   ctx.close();ctx=p.chromium.launch_persistent_context(profile,headless=True,**options());ctx.route('**/*',lambda route:route.continue_() if route.request.url.startswith(url+'/') else route.abort());page=ctx.new_page();page.goto(url+'/manage.html');page.locator('[data-action="tab"][data-id="resources"]').click();page.locator('.row').filter(has_text='acceptance-notes.txt').wait_for()
   with page.expect_download() as d:page.locator('[data-action="file-download"]').click()
   downloaded=pathlib.Path(profile)/'returned.txt';d.value.save_as(downloaded);assert hashlib.sha256(downloaded.read_bytes()).digest()==hashlib.sha256(payload).digest();passed('actual browser restart preserves attachment bytes')
   page.goto(url+'/');assert page.evaluate('HVAC_BANK.questions.length')==301;assert not errors,errors;passed('actual browser restart preserves published content');ctx.close();return 0
 finally:server.shutdown();server.server_close()
if __name__=='__main__':
 try:code=run()
 except Exception as exc:traceback.print_exc();results.append({'name':'content_browser_flow','status':'failed','reason':str(exc)});code=1
 (ROOT/'reports/content-browser-results.json').write_text(json.dumps({'exitCode':code,'results':results},ensure_ascii=False,indent=2),encoding='utf-8');sys.exit(code)
