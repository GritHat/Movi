#!/usr/bin/env python3
"""Riconteggio mio delle righe «R» dei file a_* della prova d'insieme (sola lettura): su quali passaggi vale lo zero della continuita'."""
import glob,os,sys,collections
T=collections.defaultdict(lambda: collections.Counter())
for f in sorted(glob.glob(os.path.join(sys.argv[1],'a_*.txt'))):
    for ln in open(f,encoding='utf-8'):
        if ln.startswith('R '):
            d={}
            for kv in ln.split()[1:]:
                k,v=kv.split('=',1)
                try: d[k]=int(v)
                except ValueError: pass
            c7=d.get('c7')
            for k in ('validi','nonconf','gap_p','scop_p','scop3_p','nc_scop','nc_scop3'):
                T[c7][k]+=d.get(k,0)
            T[c7]['righe']+=1
for c7 in sorted(T):
    t=T[c7]; n=t['validi']+t['nonconf']; s=t['scop_p']+t['nc_scop']
    print(f"c7={c7}: righe {t['righe']}; confermati {t['validi']}; non confermati prima dell'ombra {t['nonconf']}; somma {n}; con un vuoto {t['gap_p']}; scoperti: fra i confermati {t['scop_p']}, fra i non confermati {t['nc_scop']}, in tutto {s} ({100*s/n:.2f} %); passaggi con ingresso riconosciuto (somma - scoperti) {n-s}")

print("-- per rilevamento e corpo (c7 = 1 e c7 = 0) --")
import re
G=collections.defaultdict(lambda: collections.Counter())
for f in sorted(glob.glob(os.path.join(sys.argv[1],'a_*.txt'))):
    m=re.match(r'a_([DTL])_pd([0-9.]+)_(esteso|punto)_c7([01])',os.path.basename(f))
    for ln in open(f,encoding='utf-8'):
        if ln.startswith('R '):
            d=dict(kv.split('=',1) for kv in ln.split()[1:])
            k=(m.group(4),m.group(2),m.group(3))
            G[k]['n']+=int(d['validi'])+int(d['nonconf']); G[k]['scoperti']+=int(d['scop_p'])+int(d['nc_scop']); G[k]['vuoti']+=int(d['gap_p'])
            G[k]['geo_'+m.group(1)]+=int(d['validi'])+int(d['nonconf'])
for k in sorted(G): print(" c7=%s pd=%s corpo=%s:"%k, dict(G[k]))
