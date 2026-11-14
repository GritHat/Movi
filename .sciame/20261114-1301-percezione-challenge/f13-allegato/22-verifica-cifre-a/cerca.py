#!/usr/bin/env python3
# Cerca una cifra nei file d'origine (non in 20-unione). Uso: cerca.py [-w larghezza] cifra [cifra...]
# Normalizza: toglie \, e gli spazi (anche sottili) fra gruppi di cifre; accetta virgola o punto decimale.
import sys,re,glob,os
B='/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/'
pats=['f13-allegato/0*-*/*.md','f13-allegato/0*-*/*.txt','f13-allegato/0*-*/uscite/*','f13-allegato/DISCORDANZE_DEI_FASCICOLI.md',
 'f12-integrazione/20-finale/*.md','f12-integrazione/22-schermo-finale/*.md','f12-integrazione/02-prova-insieme/*.md','f12-integrazione/03-libero/*.md',
 'f12-integrazione/06-identita/*.md','f12-integrazione/07-controprova-identita/*.md','f12-integrazione/13-statistica/*.md','f12-integrazione/10-attacco/*.md',
 'f12-integrazione/30-arbitro/*.md','f12-integrazione/30-arbitro/*.txt','f14-classificazione/*/*.md','f4/H-012/09-arbitro/VERDETTO.md','f7-estensione/16-verdetto/VERDETTO_ESTENSIONE.md',
 'f8-continuita/16-verdetto/VERDETTO_CONTINUITA.md','f9-preproposta/13-verdetto/VERDETTO_PREPROPOSTA.md','f10-dati/23-verdetto/VERDETTO_DATI.md']
files=[]
for p in pats: files+=sorted(f for f in glob.glob(B+p) if os.path.isfile(f))
W=110; a=sys.argv[1:]
if a and a[0]=='-w': W=int(a[1]); a=a[2:]
MAX=6
if a and a[0]=='-m': MAX=int(a[1]); a=a[2:]
def norm(s):
    s=s.replace('\\,','').replace('\u202f',' ').replace('\u2009',' ').replace('\xa0',' ')
    s=re.sub(r'(?<=\d)[ ](?=\d{3}(\D|$))','',s)
    return s
for tok in a:
    t=re.escape(norm(tok)).replace(',','[,.]')
    rx=re.compile(r'(?<![\d,.])'+t+r'(?![\d])')
    n=0;print('=====',tok)
    for f in files:
        try: L=open(f,encoding='utf-8',errors='replace').read().split('\n')
        except Exception: continue
        for i,l in enumerate(L,1):
            l2=norm(l); m=rx.search(l2)
            if m:
                n+=1
                if n<=MAX: print(f"  {f[len(B):]}:{i}: …{l2[max(0,m.start()-W):m.end()+W]}…")
    print('  occorrenze:',n)
