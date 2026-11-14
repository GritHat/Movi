#!/usr/bin/env python3
"""Compone CONTROLLO.md prendendo i testi corretti dal file LaTeX che è stato compilato (prova_latex/correzioni.tex),
così il testo consegnato è esattamente quello provato."""
import re,sys,os
O=os.path.dirname(os.path.abspath(__file__))
L=open(os.path.join(O,'prova_latex','correzioni.tex'),encoding='utf8').read().split('\n')
F={}
for i,l in enumerate(L):
    m=re.match(r'%(R\d+[a-z]?)\b',l)
    if m: F[m.group(1)]=L[i+1]
    if l.startswith('\\caption{Regola «mobile»'): F['R3']=l
def fr(k): return "```latex\n"+F[k]+"\n```"
T=open(os.path.join(O,'CONTROLLO_modello.md'),encoding='utf8').read()
T=re.sub(r'\{\{(R\d+[a-z]?)\}\}',lambda m: fr(m.group(1)),T)
open(os.path.join(O,'CONTROLLO.md'),'w',encoding='utf8').write(T)
print('frammenti:',sorted(F)); print('righe:',T.count('\n'))
