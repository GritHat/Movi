#!/usr/bin/env python3
"""riconta4_arbitro.py - stato della traccia nei fotogrammi con la persona nascosta, su profondita' simulata da scheda (catena f10 e catena con le correzioni di 06-identita)."""
import sys, os, json, collections
F = sys.argv[1]
def leggi(p): return [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
for nome in ('06-identita/risultati/nuovi424.jsonl', '06-identita/risultati/nuovi848.jsonl',
             '07-controprova-identita/risultati/ultimi424_replica.jsonl', '07-controprova-identita/risultati/ultimi848_replica.jsonl'):
    tutte = leggi(os.path.join(F, nome))
    for conf in ('prima', 'tutte_p'):
        for liv in ('nominale', 'limite'):
            rr = [r for r in tutte if r.get('conf') == conf and r.get('livello') == liv and 'stato_traccia_nascosto' in r]
            if not rr: continue
            c = collections.Counter(); pieni = 0
            for r in rr:
                for k, v in r['stato_traccia_nascosto'].items(): c[k] += v
                s = r['stato_traccia_nascosto']; pieni += (s.get('perso', 0) + s.get('assente', 0) + s.get('altro', 0) + s.get('osservato', 0)) == 0
            tot = sum(c.values())
            print(f"{nome.split('/')[-1]:28s} {conf:8s} {liv:8s} passaggi {len(rr):3d}: fotogrammi nascosti {tot}: {dict(c)} | passaggi con «previsto» in ogni fotogramma nascosto: {pieni}/{len(rr)}")
