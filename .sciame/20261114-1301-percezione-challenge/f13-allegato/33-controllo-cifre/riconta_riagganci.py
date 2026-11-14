#!/usr/bin/env python3
"""Riagganci a soggetto nascosto e identita' per risoluzione, dal grezzo (sola lettura)."""
import json,sys,os,collections
F=sys.argv[1]
for nome in ('06-identita/risultati/nuovi424.jsonl','06-identita/risultati/nuovi848.jsonl'):
    rr=[json.loads(l) for l in open(os.path.join(F,nome),encoding='utf-8') if l.strip()]
    for conf in ('prima','tutte_p'):
        for liv in ('nominale','limite'):
            x=[r for r in rr if r.get('conf')==conf and r.get('livello')==liv and 'cella_centro_nascosto' in r]
            if not x: continue
            s=sum(r.get('riagganci_a_soggetto_nascosto',0) for r in x); p=sum(1 for r in x if r.get('riagganci_a_soggetto_nascosto',0)>0)
            es=collections.Counter((r.get('tipo'),r.get('esito_identita')) for r in x)
            print(f"{nome.split('/')[-1]} {conf:8s} {liv:9s}: passaggi {len(x)}; riagganci a nascosto: somma {s}, passaggi con almeno uno {p}; pannello mobile {sum(1 for r in x if r.get('pannello_si_muove'))}")
            if conf=='tutte_p' and liv=='nominale':
                for t in ('a12','a05','b','c','d'):
                    n=sum(v for (tt,e),v in es.items() if tt==t); print('      tipo',t,'n',n,{e:v for (tt,e),v in es.items() if tt==t})
