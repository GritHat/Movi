#!/usr/bin/env python3
"""Arbitro f8-f5: il difetto dei semi di gen.h (flussi contigui spostati di uno) tocca anche torneo.c e att.c?
Riscrivo in Python le righe d'inizializzazione lette in 12-torneo/torneo.c (riga 297) e 14-attacco/att.c (riga 44).
Rifare: PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 semi_altri.py > semi_altri.txt"""
M = (1 << 64) - 1
G = 0x9E3779B97F4A7C15
def nxt(s):
    s = (s + G) & M; z = s
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M
    return s, z ^ (z >> 31)
def flusso(s, n):
    o = []
    for _ in range(n):
        s, v = nxt(s); o.append(v)
    return o
# torneo.c: stato = seed*1000003 + beh*7919 (nessun mescolamento); due semi contigui distano 1000003
kinv = pow(G, -1, 1 << 64)
k = (1000003 * kinv) & M
print(f"torneo.c: lo stato del seme s+1 = stato del seme s + 1000003 = stato avanzato di k chiamate con k = {k} (oppure indietro di {(1<<64)-k})")
print("   -> i flussi di due semi contigui si sovrappongono solo dopo", min(k, (1 << 64) - k), "chiamate: nessuna sovrapposizione pratica")
a = set(flusso((9000 * 1000003) & M, 20000)); b = flusso((9001 * 1000003) & M, 20000)
print("   controllo diretto, 20000 numeri per seme (9000, 9001): numeri in comune =", sum(1 for v in b if v in a))
# att.c: stato = (a+1)*G ^ (b+7)*C1 ^ (c+13)*C2, poi 8 chiamate
def rseed(a_, b_, c_):
    s = (((a_ + 1) * G) & M) ^ (((b_ + 7) * 0xC2B2AE3D27D4EB4F) & M) ^ (((c_ + 13) * 0x165667B19E3779F9) & M)
    if s == 0: s = 1
    for _ in range(8): s, _v = nxt(s)
    return s
tot = 0
for geo in (ord('D'), ord('T'), ord('L'), 0, 1, 2):
    for beh in (0, 3):
        a = set(flusso(rseed(200000, beh, geo), 20000)); b = flusso(rseed(200001, beh, geo), 20000)
        tot += sum(1 for v in b if v in a)
print("att.c: semi 200000 e 200001, 20000 numeri per seme, 12 combinazioni (comportamento, geometria): numeri in comune =", tot)
print("   (il valore di GEO usato da att.c non l'ho letto: provo sei valori plausibili; se e' 0 per tutti: il difetto non c'e')")
