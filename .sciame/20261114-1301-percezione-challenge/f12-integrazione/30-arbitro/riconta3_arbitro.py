#!/usr/bin/env python3
"""riconta3_arbitro.py - tre dettagli notati nel riconteggio: pannello «mobile» nella replica, riagganci a nascosto, rimozione del pannello."""
import sys, os, json, collections
F = sys.argv[1]
def leggi(p): return [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
for nome in ('06-identita/risultati/nuovi424.jsonl', '06-identita/risultati/nuovi848.jsonl',
             '07-controprova-identita/risultati/ultimi424_replica.jsonl', '07-controprova-identita/risultati/ultimi848_replica.jsonl'):
    rr = [r for r in leggi(os.path.join(F, nome)) if r.get('conf') == 'tutte_p' and 'pannello_si_muove' in r]
    c = collections.Counter(); n = collections.Counter(); h = collections.Counter(); hp = collections.Counter()
    for r in rr:
        k = (r.get('profilo'), r.get('livello'), r.get('tipo')); n[k] += 1
        c[k] += bool(r['pannello_si_muove']); h[k] += r.get('riagganci_a_soggetto_nascosto', 0); hp[k] += r.get('riagganci_a_soggetto_nascosto', 0) > 0
    print(nome.split('/')[-1], '| righe con il campo:', len(rr))
    print('   pannello «mobile» per (profilo, livello, tipo):', {str(k): f'{c[k]}/{n[k]}' for k in sorted(n, key=str) if c[k]})
    print('   riagganci a soggetto nascosto, eventi (passaggi):', {str(k): f'{h[k]} ({hp[k]}/{n[k]})' for k in sorted(n, key=str) if h[k]})
    nom = [r for r in rr if r.get('livello') == 'nominale']
    print(f"   solo nominale: pannello mobile {sum(bool(r['pannello_si_muove']) for r in nom)}/{len(nom)}; passaggi con riaggancio a nascosto {sum(r.get('riagganci_a_soggetto_nascosto',0)>0 for r in nom)}/{len(nom)}")
rr = [r for r in leggi(os.path.join(F, '07-controprova-identita/risultati/att_rotto.jsonl')) if r.get('gruppo') == 'B4_rimozione']
for r in rr[:2]:
    print('rimozione, riga di esempio:', {k: r[k] for k in ('conf', 'nome', 'fotogrammi', 'tracce_confermate', 'rimozione') if k in r}, '| eventi', r.get('eventi'))
print('rimozione: configurazioni presenti', collections.Counter(r['conf'] for r in rr))
