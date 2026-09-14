from pathlib import Path
import re,base64,urllib.request,json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read()
s=Path('site-source/my-tribe.html').read_text()
soup=BeautifulSoup(s,'html.parser')
for link in list(soup.select('link[rel=stylesheet]')):
    css=get(link['href']).decode()
    def embed(m):
        url=m.group(1).strip("'\"")
        return 'url(data:font/woff2;base64,'+base64.b64encode(get(url)).decode()+')'
    css=re.sub(r'url\(([^)]+)\)',embed,css)
    style=soup.new_tag('style');style.string=css;link.replace_with(style)
for l in soup.select('link[rel=preconnect]'):l.decompose()
s=str(soup)
Path('my-tribe').mkdir(exist_ok=True)
Path('my-tribe/index.html').write_text(s)
Path('Jane_My_Tribe_Stage_1.html').write_text(s)
h=Path('index.html').read_text()
h=h.replace('href="#my-tribe"','href="./my-tribe/"')
home=BeautifulSoup(h,'html.parser')
card=home.find(id='my-tribe')
if card:
    parent=card.find_parent('article')
    if parent:
        for x in parent.find_all('a'):x['href']='./my-tribe/';x.string='Explore My Tribe'
for el in home.find_all(string=re.compile('Atrya')):el.replace_with(str(el).replace('Atrya','Atria'))
logos=home.select_one('.logos')
if logos:
    logos.clear()
    pic=home.new_tag('img',src='assets/logos/globallogic.png',alt='GlobalLogic')
    pic['style']='width:180px;height:68px;object-fit:contain'
    logos.append(pic)
    p=home.new_tag('p');p.string='Bosch & Siemens · GlobalLogic · Creatio · Trustonic · Avenga · Atria Brokers · XQL Group · Sunsoft'
    logos.insert_after(p)
label=home.select_one('.logo-label')
if label:label.string='Selected organisations I have worked with'
Path('assets/logos').mkdir(parents=True,exist_ok=True)
Path('assets/logos/globallogic.png').write_bytes(get('https://www.globallogic.com/wp-content/uploads/2024/07/Logo.png'))
Path('index.html').write_text(str(home))
for name,u in [('Creatio','https://www.creatio.com/'),('XQL','https://xql.group/'),('Avenga','https://www.avenga.com/'),('Trustonic','https://www.trustonic.com/'),('BSH','https://www.bsh-group.com/'),('Sunsoft','http://sunsoft.pro/')]:
    try:
        doc=BeautifulSoup(get(u),'html.parser')
        header=doc.find('header') or doc
        print('BRAND',name,str(header)[:18000])
    except Exception as e:print('BRAND',name,str(e))
