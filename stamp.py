# Nach jeder Änderung an index.html ausführen:  python3 stamp.py
# Setzt den Update-Check (vor </body>) mit neuer Versionsnummer und schreibt version.txt.
import hashlib, os, re
root=os.path.dirname(os.path.abspath(__file__)); p=os.path.join(root,'index.html')
s=open(p,encoding='utf-8').read()
s=re.sub(r'var V="[0-9a-f_A-Z]*"','var V="__APPVER__"',s)
# Gemeinsames Design (design.css, wortgleich mit src/design.css der anderen Apps) einsetzen
design=open(os.path.join(root,'design.css'),encoding='utf-8').read().strip()
s=re.sub(r'/\*DESIGN\*/.*?/\*DESIGN-ENDE\*/', lambda _: '/*DESIGN*/\n'+design+'\n/*DESIGN-ENDE*/', s, flags=re.S)
# Claude-Brücke: letzte Logbuch-Einträge dieser App aus CLAUDE.md in die App übernehmen
import json
log=[]
try:
  md=open(os.path.join(root,'CLAUDE.md'),encoding='utf-8').read()
  sec=md.split('### Logbuch',1)[1].split('<!--',1)[0]
  for l in sec.splitlines():
    m=re.match(r'^- (\d{4}-\d\d-\d\d) · (.+?) · (.+?) · (.+?) · (.+)$',l.strip())
    if m and ('W&G I' in m.group(2) or m.group(2)=='alle'): log.append({'d':m.group(1),'a':m.group(2),'w':m.group(4),'y':m.group(5)})
except Exception as e: print('Brücke:',e)
s=re.sub(r'/\*BRUECKE\*/.*?/\*BRUECKE-ENDE\*/', lambda _: '/*BRUECKE*/'+json.dumps(log[:6],ensure_ascii=False)+'/*BRUECKE-ENDE*/', s, flags=re.S)
ver=hashlib.sha1(s.encode('utf-8')).hexdigest()[:12]
s=s.replace('__APPVER__',ver)
open(p,'w',encoding='utf-8').write(s)
open(os.path.join(root,'version.txt'),'w',encoding='utf-8').write(ver+'\n')
print(ver)
