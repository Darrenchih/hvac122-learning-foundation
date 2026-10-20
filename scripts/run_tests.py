"""Run reproducible checks; BLOCKED is never converted to PASS."""
import subprocess,sys,pathlib,json,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]
commands=[('bank_audit',[sys.executable,'tests/audit_bank.py'],12),('core_logic',['node','tests/test_core.cjs'],14),('render_event_harness',['node','tests/ui_harness.cjs'],9),('content_contract',['node','tests/test_content.cjs'],17),('management_harness',['node','tests/manager_harness.cjs'],9),('content_schema_cli',[sys.executable,'tests/audit_content.py'],6)]
if '--browser' in sys.argv:
 commands.append(('real_browser',[sys.executable,'tests/browser_smoke.py'],None))
 commands.append(('real_content_browser',[sys.executable,'tests/browser_content_smoke.py'],None))
results=[]
for name,cmd,count in commands:
 try:
  p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',timeout=90)
  output=p.stdout+p.stderr;status='passed' if p.returncode==0 else 'blocked' if p.returncode==77 else 'failed';code=p.returncode
 except Exception as exc:output=str(exc);status='blocked';code=None
 (ROOT/'reports'/f'{name}.log').write_text(output,encoding='utf-8');results.append({'name':name,'status':status,'exitCode':code,'checks':count,'log':f'{name}.log'});print(name,status)
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'environment':'Linux; Node 24; Python 3.12; no Windows runtime','suites':results,'windowsPowerShell':'not_executed','note':'VM rendering harness is not a real DOM/browser test.'}
(ROOT/'reports/test-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
sys.exit(1 if any(x['status']=='failed' for x in results) else 2 if any(x['status']=='blocked' for x in results) else 0)
