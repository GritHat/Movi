# Per ogni cifra dei capitoli 6,7,8,A,B,1(sintesi),9: cerca la stessa cifra nel corpus delle fonti (fascicoli, f12, verdetti, f14).
# Sola lettura. Uscita: cifre NON trovate nel corpus, con il contesto. (Trovata != giusta: e' solo un setaccio.)
import re,sys,os,glob
B='/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge'
src=[]
for pat in ('f13-allegato/0*-*/**/*.md','f13-allegato/0*-*/**/*.txt','f13-allegato/DISCORDANZE_DEI_FASCICOLI.md','f12-integrazione/**/*.md','f12-integrazione/**/*.txt','f14-classificazione/**/*.md','f14-classificazione/**/*.txt','f4/H-012/09-arbitro/*.md','f7-estensione/16-verdetto/*.md','f8-continuita/16-verdetto/*.md','f9-preproposta/13-verdetto/*.md','f10-dati/23-verdetto/*.md'):
    src+=glob.glob(os.path.join(B,pat),recursive=True)
import json
SEL=sys.argv[1]
src=[s for s in src if '/scaricat' not in s and '/40-documento' not in s and '/41-' not in s and '/42-' not in s and os.path.getsize(s)<3_000_000]
def norm(t):
    t=t.replace('{,}',',').replace('\\,','').replace('\u202f','').replace('\u2009','').replace('\u00a0',' ')
    t=re.sub(r'(?<=\d)[ ](?=\d{3}(?!\d))','',t)
    t=re.sub(r'(?<=\d)\.(?=\d)',',',t)
    return t
if SEL!='tutto':
    src=[s for s in src if re.search(SEL,s)]
corpus={}
for s in src:
    try: corpus[s]=norm(open(s,errors='replace').read())
    except Exception as e: pass
allt='\n'.join(corpus.values())
toks=set(re.findall(r'\d+(?:,\d+)?',allt))
print('file nel corpus:',len(corpus),' cifre distinte:',len(toks),file=sys.stderr)
caps=sys.argv[2:]
for cap in caps:
    tx=norm(open(os.path.join(B,'f13-allegato/20-unione/capitoli',cap)).read())
    print('=====',cap)
    for ln,line in enumerate(tx.split('\n'),1):
        l2=re.sub(r'\\(ref|label|cite|eqref)\{[^}]*\}','',line)
        for m in re.finditer(r'\d+(?:,\d+)?',l2):
            t=m.group(0)
            if ',' not in t and int(t)<13: continue
            if t in toks: continue
            alt=None
            if ',' in t:
                # percentuale <-> quota ; zeri finali
                v=float(t.replace(',','.'))
                cands={('%.4f'%(v/100)).rstrip('0').replace('.',','),('%.3f'%(v/100)).replace('.',','),('%g'%(v*100)).replace('.',','),t.rstrip('0').rstrip(','),t+'0'}
                alt=[c for c in cands if c in toks]
            print(f'{ln}: [{t}] alt={alt} :: ...{l2[max(0,m.start()-70):m.end()+50]}...')
