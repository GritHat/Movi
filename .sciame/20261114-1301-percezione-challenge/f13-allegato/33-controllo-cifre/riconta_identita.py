#!/usr/bin/env python3
"""176/180 e 174/180: «continuita' pulita» su D435i nominale, tre comportamenti (a12, a05, b), due serie di semi (sola lettura)."""
import json,sys,collections
F=sys.argv[1]
for lar,files in ((424,('06-identita/risultati/nuovi424.jsonl','07-controprova-identita/risultati/ultimi424_replica.jsonl')),(848,('06-identita/risultati/nuovi848.jsonl','07-controprova-identita/risultati/ultimi848_replica.jsonl'))):
    tot=0;n=0
    for nome in files:
        rr=[json.loads(l) for l in open(F+'/'+nome,encoding='utf-8') if l.strip()]
        for t in ('a12','a05','b'):
            x=[r for r in rr if r.get('conf')=='tutte_p' and r.get('livello')=='nominale' and r.get('profilo')=='d435i' and r.get('tipo')==t]
            k=sum(1 for r in x if r.get('continuita_pulita')); tot+=k; n+=len(x)
            print(f" {lar} {nome.split('/')[-1]:28s} {t}: continuita' pulita {k}/{len(x)}; esito «stessa» {sum(1 for r in x if r.get('esito_identita')=='stessa')}")
    print(f" {lar} px: {tot} su {n}")
