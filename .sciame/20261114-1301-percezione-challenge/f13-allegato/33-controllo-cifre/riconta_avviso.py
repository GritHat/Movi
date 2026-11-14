#!/usr/bin/env python3
"""Riconteggio mio dei fotogrammi «soggetto nascosto» e «fuori dall'avviso» dai file grezzi .jsonl (sola lettura).
Scopo: sciogliere i due denominatori 4324/4325 e 3921/3922 e il «7 su 10» del pannello mobile."""
import sys, json, collections, os
F=sys.argv[1]
def leggi(p): return [json.loads(l) for l in open(p,encoding='utf-8') if l.strip()]
for nome in ('06-identita/risultati/nuovi424.jsonl','06-identita/risultati/nuovi848.jsonl',
             '07-controprova-identita/risultati/ultimi424_replica.jsonl','07-controprova-identita/risultati/ultimi848_replica.jsonl'):
    rr=leggi(os.path.join(F,nome))
    print('==',nome,'righe',len(rr),'conf',sorted({r.get('conf') for r in rr}))
    for conf in ('prima','tutte_p'):
        x=[r for r in rr if r.get('conf')==conf and 'cella_centro_nascosto' in r]
        if not x: continue
        g=collections.defaultdict(lambda: collections.Counter())
        for r in x:
            k=(r.get('tipo'),r.get('livello'))
            c=r['cella_centro_nascosto']
            g[k]['passaggi']+=1
            g[k]['entro3m']+=sum(v for kk,v in c.items() if kk!='fuori_griglia')
            g[k]['fuori_griglia']+=c.get('fuori_griglia',0)
            g[k]['senza_avviso']+=c.get('in_ombra_senza_avviso',0)
            g[k]['non_presenza']+=sum(v for kk,v in c.items() if kk not in('fuori_griglia','possibile_presenza'))
            g[k]['pannello_mobile']+=1 if r.get('pannello_si_muove') else 0
            g[k]['nascosti']+=r.get('nascosti',0)
        tot=collections.Counter()
        for k in sorted(g, key=str):
            print(f"   {conf:8s} tipo={k[0]!s:14s} livello={k[1]!s:9s}",dict(g[k]))
            tot.update(g[k])
        print(f"   {conf:8s} TOTALE",dict(tot))
        for esc in sorted({k[0] for k in g}, key=str):
            for liv in (None,'nominale'):
                s=collections.Counter()
                for k in g:
                    if k[0]!=esc and (liv is None or k[1]==liv): s.update(g[k])
                print(f"      senza tipo {esc!s:12s} livello {liv or 'tutti':9s}: passaggi {s['passaggi']} entro3m {s['entro3m']} senza_avviso {s['senza_avviso']} non_presenza {s['non_presenza']} pannello_mobile {s['pannello_mobile']}")
