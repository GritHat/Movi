# g.py FILTRO cifra [cifra...] : stampa le righe (normalizzate) delle fonti che contengono la cifra come numero intero.
import re,sys,os,glob
B='/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge'
def norm(t):
    t=t.replace('{,}',',').replace('\\,','').replace('\u202f','').replace('\u2009','').replace('\u00a0',' ')
    t=re.sub(r'(?<=\d)[ ](?=\d{3}(?!\d))','',t); t=re.sub(r'(?<=\d)\.(?=\d)',',',t); return t
fs=[f for f in glob.glob(B+'/**/*.md',recursive=True)+glob.glob(B+'/f13-allegato/0*/**/*.txt',recursive=True)+glob.glob(B+'/f12-integrazione/30-arbitro/*.txt') if re.search(sys.argv[1],f) and '/1' not in f.split('f13-allegato')[-1][:3] and '20-unione' not in f and '2[1-9]-verifica' not in f]
W=int(os.environ.get('W','330'))
for n in sys.argv[2:]:
    print('#####',n)
    pat=re.compile(r'(?<![\d,])'+re.escape(n)+r'(?![\d]|,\d)')
    for f in fs:
        for i,l in enumerate(norm(open(f,errors='replace').read()).split('\n'),1):
            m=pat.search(l)
            if m: print(f"  {f.replace(B+'/','')}:{i}: …{l[max(0,m.start()-W//2):m.end()+W//2]}…")
