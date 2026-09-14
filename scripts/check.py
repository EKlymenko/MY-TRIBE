from playwright.sync_api import sync_playwright
from pathlib import Path
import json
report=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [390,1440]:
  page=b.new_page(viewport={'width':width,'height':900})
  for route in ['', 'my-tribe/']:
   page.goto('http://127.0.0.1:8000/'+route)
   page.wait_for_timeout(1000)
   result=page.evaluate("({overflow:document.documentElement.scrollWidth>innerWidth,broken:[...document.images].filter(x=>!x.complete||x.naturalWidth===0).map(x=>x.alt)})")
   assert not result['overflow'],result
   assert not result['broken'],result
   report.append({'width':width,'route':route,**result})
   page.screenshot(path='checks/'+str(width)+('-tribe' if route else '-home')+'.png',full_page=True)
  page.close()
 page=b.new_page()
 page.route('http**/*',lambda route:route.abort())
 page.goto(Path('Jane_My_Tribe_Stage_1.html').resolve().as_uri())
 assert page.locator('h1').inner_text()=='My Tribe'
 assert page.evaluate("[...document.images].every(x=>x.complete&&x.naturalWidth>0)")
 b.close()
Path('checks/results.json').write_text(json.dumps(report,indent=2))
print('CHECKS',report)
