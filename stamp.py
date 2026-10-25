# Nach jeder Änderung an index.html ausführen:  python3 stamp.py
# Setzt den Update-Check (vor </body>) mit neuer Versionsnummer und schreibt version.txt.
import hashlib, os, re
root=os.path.dirname(os.path.abspath(__file__)); p=os.path.join(root,'index.html')
s=open(p,encoding='utf-8').read()
s=re.sub(r'var V="[0-9a-f_A-Z]*"','var V="__APPVER__"',s)
ver=hashlib.sha1(s.encode('utf-8')).hexdigest()[:12]
s=s.replace('__APPVER__',ver)
open(p,'w',encoding='utf-8').write(s)
open(os.path.join(root,'version.txt'),'w',encoding='utf-8').write(ver+'\n')
print(ver)
