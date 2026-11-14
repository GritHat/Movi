# [dopo il secondo lancio, dichiarato] C2 diviso: C2a = regione tratteggiata con l'eta' (prima), C2b = il resto.
# Uso: timeout 120 <python di f10> -I -B variante_c2.py > risultati_variante_c2.txt   (importa il modulo accanto)
import numpy as np
import piano_finale_mc as m

g = []
for cid, chi, pred in m.GRAFO:
    if cid == 'C2':
        g.append(('C2a', ['P3'], ['SK'])); g.append(('C2b', ['P3'], ['C2a']))
    else:
        g.append((cid, chi, ['C2b' if q == 'C2' else q for q in pred]))
MIE = dict(m.MIE, C2a=(.75, 1, 2), C2b=(1.25, 1.5, 3))
R2 = dict(m.RUOLO2, C2a=(.75, 1.25, 2.25), C2b=(1.25, 1.75, 3.25))
m.PIOLI = [(p, ['B2', 'C2a', 'SK'] if p == 'regione' else ['A5', 'A3r', 'C3a'] if p == 'salute' else c)
           for p, c in m.PIOLI]
print("== 5. C2 diviso (C2a prima): piolo 'regione' = B2 + C2a + SK")
for nome, st in (('FIN-C2 stime mie', MIE), ('FIN-C2 stime del secondo ruolo', R2)):
    for ip in (m.LEGGERO, m.MEDIO, m.DURO):
        m.riga(nome, st, ip, grafo=g, dettagli=True)
for s in (2, 3):
    m.riga(f'FIN-C2 stime mie, seme {s}', MIE, m.LEGGERO, seme=s, grafo=g)
    m.riga(f'FIN-C2 ruolo 2, seme {s}', R2, m.MEDIO, seme=s, grafo=g)
k0p = (.25, .4, .75)
for ip in (m.LEGGERO, m.MEDIO):
    m.riga('FIN-C2 K0 preparato prima (mie)', dict(MIE, K0=k0p), ip, grafo=g)
    m.riga('FIN-C2 K0 preparato prima (ruolo 2)', dict(R2, K0=k0p), ip, grafo=g)
