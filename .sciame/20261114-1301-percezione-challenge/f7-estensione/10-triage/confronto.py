#!/usr/bin/env python3
"""confronto.py — sciame-arbitro, triage f7. Ricalcola dai file dei ruoli (sola lettura):
 (1) il costo per passo di raggio di 'ottimizzazione' e 'tempo-reale' e i rapporti fra coppie confrontabili;
 (2) le distanze di osservabilita' delle tre fasce di S10 con il montaggio del nucleo;
 (3) i conteggi di voxel e la memoria densa.
Uso: python3 -I confronto.py   (nessun file scritto; uscita su stdout)"""
import re, math, glob, os
B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def num(s, key):
    m = re.search(key + r'=\s*([-0-9.]+)', s); return float(m.group(1)) if m else None
print("== (3) voxel e memoria densa, regione 6 x 4 x 3 m")
for cm in (10, 5):
    n = round(6/(cm/100))*round(4/(cm/100))*round(3/(cm/100))
    print(f"  {cm} cm: {n} voxel; " + "; ".join(f"{b} B/voxel = {n*b} B = {n*b/1e6:.3f} MB = {n*b/2**20:.3f} MiB" for b in (1,2,4,8,12)))
print("== (1a) ottimizzazione: densa (anello), densafix, hash; scena rada")
ott = {}
for f in sorted(glob.glob(B + "/02-ottimizzazione/risultati_[0-9]*.txt")):
    if 'contaminato' in f: continue
    for l in open(f, encoding='utf-8'):
        m = re.match(r'(\w+)\s+ris=\s*(\d+)cm scena=(\w+)\s+raggi=\s*(\d+) fot=(\d+) ombra=(\d) arena=(\d)', l)
        if not m: continue
        s, r, sc, rg, fot, om, ar = m.groups()
        if om != '0' or ar != '0' or 'scartati=0' not in l: continue
        k = (s, int(r), sc, int(rg))
        rec = dict(media=num(l, 'agg_ms media'), p95=num(l, r'agg_ms media=[0-9.]+ p95'), mx=num(l, r'p95=[0-9.]+ max'),
                   passi=num(l, r'passi/fot media'), blocchi=num(l, 'blocchi'), file=os.path.basename(f), fot=int(fot))
        ott.setdefault(k, []).append(rec)
for k in sorted(ott):
    if k[0] in ('densa', 'densafix', 'hash') and k[2] == 'rada':
        for r in ott[k]:
            ns = r['media']*1e6/r['passi'] if r['passi'] else float('nan')
            print(f"  {k[0]:8s} {k[1]:2d} cm raggi={k[3]:6d}: media {r['media']:7.3f} p95 {r['p95']:7.3f} max {r['mx']:7.3f} ms; passi {r['passi']:.0f}; {ns:.2f} ns/passo; blocchi {r['blocchi']:.0f} [{r['file']}, {r['fot']} fot]")
print("== (1b) tempo-reale: D (densa), H (hash); scena vuota; file risultati_tempo_binario_finale.txt")
tr = {}
for l in open(B + "/06-tempo-reale/risultati_tempo_binario_finale.txt", encoding='utf-8'):
    m = re.match(r'scena=(\w+) metodo=(\w) lato_cm=(\d+) k=(\d+) margine=(\d+)', l)
    if not m: continue
    sc, me, lato, k, mar = m.groups()
    if mar != '0': continue
    tr[(sc, me, int(lato), int(k))] = dict(media=num(l, 'media'), p95=num(l, 'p95'), mx=num(l, 'max'), passi=num(l, 'passi/fot'),
                                           colpi=num(l, 'colpi/fot'), raggi=num(l, 'raggi/fot'), blocchi=re.search(r'blocchi=(\d+/\d+)', l))
for k in sorted(tr):
    if k[0] == 'vuota' and k[1] in 'DH':
        r = tr[k]; ns = r['media']*1e6/r['passi'] if r['passi'] else float('nan')
        b = r['blocchi'].group(1) if r['blocchi'] else '-'
        print(f"  {k[1]} {k[2]:2d} cm k={k[3]}: media {r['media']:7.3f} p95 {r['p95']:7.3f} max {r['mx']:7.3f} ms; raggi {r['raggi']:.0f}; passi {r['passi']:.0f}; colpi {r['colpi']:.0f}; lordo {ns:.2f} ns/passo; blocchi {b}")
print("== (1c) tempo-reale, costo fisso (colpi a piena risoluzione) e costo marginale per passo, da due punti (k=8, k=4) e (k=4, k=1)")
marg = {}
for lato in (5, 10):
    a, b, c = tr[('vuota','D',lato,8)], tr[('vuota','D',lato,4)], tr[('vuota','D',lato,1)]
    m84 = (b['media']-a['media'])*1e6/(b['passi']-a['passi']); fisso = b['media'] - m84*b['passi']/1e6
    m41 = (c['media']-b['media'])*1e6/(c['passi']-b['passi'])
    marg[lato] = (m84, m41, fisso)
    print(f"  {lato} cm: marginale k8->k4 {m84:.2f} ns/passo, k4->k1 {m41:.2f} ns/passo; costo fisso stimato {fisso:.2f} ms")
print("== (1d) coppie fra i due ruoli")
def o(s, r, rg): return ott[(s, r, 'rada', rg)][0]
pairs = [
 ("densa, 5 cm, 307 200 raggi (tutti)            [confrontabile]", o('densa',5,307200), tr[('vuota','D',5,1)]),
 ("hash 8^3, 5 cm, 307 200 raggi                 [confrontabile]", o('hash',5,307200), tr[('vuota','H',5,1)]),
 ("densa, 10 cm, 307 200 raggi                   [confrontabile]", o('densa',10,307200), tr[('vuota','D',10,1)]),
 ("hash 8^3, 10 cm, 307 200 raggi                [confrontabile]", o('hash',10,307200), tr[('vuota','H',10,1)]),
 ("densa, 5 cm, 76 800 raggi liberi              [NON confr.: TR tratta i colpi a piena risoluzione]", o('densa',5,76800), tr[('vuota','D',5,2)]),
 ("densa, 10 cm, 76 800 raggi liberi             [NON confr.]", o('densa',10,76800), tr[('vuota','D',10,2)]),
 ("densa, 5 cm, 19 200 raggi liberi              [NON confr.]", o('densa',5,19200), tr[('vuota','D',5,4)]),
 ("densa, 10 cm, 19 200 raggi liberi             [NON confr.]", o('densa',10,19200), tr[('vuota','D',10,4)]),
]
for name, a, b in pairs:
    print(f"  {name}: ott {a['media']:.2f} / p95 {a['p95']:.2f} ms ({a['passi']:.0f} passi) — tr {b['media']:.2f} / p95 {b['p95']:.2f} ms ({b['passi']:.0f} passi) — rapporto medie {b['media']/a['media']:.2f}, p95 {b['p95']/a['p95']:.2f}; passi {b['passi']/a['passi']:.2f}")
for lato in (5, 10):
    a = o('densa', lato, 19200); nsa = a['media']*1e6/a['passi']
    print(f"  costo per passo a {lato} cm: ott {nsa:.2f} ns (19 200 raggi) contro tr marginale {marg[lato][0]:.2f} ns -> rapporto {marg[lato][0]/nsa:.2f}")
print("  rapporto hash/densa: ott 5 cm %.2f, 10 cm %.2f; tr 5 cm %.2f, 10 cm %.2f" % (
    o('hash',5,307200)['media']/o('densa',5,307200)['media'], o('hash',10,307200)['media']/o('densa',10,307200)['media'],
    tr[('vuota','H',5,1)]['media']/tr[('vuota','D',5,1)]['media'], tr[('vuota','H',10,1)]['media']/tr[('vuota','D',10,1)]['media']))
print("  sovraccosto assoluto dell'hash per passo: ott 5 cm %.2f ns, tr 5 cm %.2f ns" % (
    (o('hash',5,307200)['media']-o('densa',5,307200)['media'])*1e6/o('densa',5,307200)['passi'],
    (tr[('vuota','H',5,1)]['media']-tr[('vuota','D',5,1)]['media'])*1e6/tr[('vuota','D',5,1)]['passi']))
print("== (2) fasce di S10 con il montaggio del nucleo: sensore a 1,2 m, asse 15 gradi in basso, campo verticale 58 gradi")
hs, su, giu = 1.2, math.tan(math.radians(29-15)), math.tan(math.radians(29+15))
print(f"  bordo alto: quota = 1,2 + {su:.4f} r ; bordo basso: quota = 1,2 - {giu:.4f} r")
for q in (1.60, 1.80, 1.90, 2.00):
    print(f"  quota {q:.2f} m vista da r >= {(q-hs)/su:.2f} m")
for q in (0.0, 0.07, 0.15, 0.60):
    print(f"  quota {q:.2f} m vista da r >= {(hs-q)/giu:.2f} m")
for r in (1.24, 2.0, 2.41, 3.0):
    print(f"  a r = {r:.2f} m il campo copre le quote da {max(0.0, hs-giu*r):.2f} a {hs+su*r:.2f} m")
print("  ombra al suolo di un ostacolo alto h a distanza d: fine a d*1,2/(1,2-h)")
for h, d in ((0.3,1.3),(0.3,1.7),(0.5,1.5),(0.5,2.0),(0.4,1.7),(1.0,1.9),(0.2,2.0)):
    print(f"    h={h} m, d={d} m -> {d*hs/(hs-h):.2f} m")
print(f"  piramide vista (87 x 58 gradi, profondita' 3 m): {4*math.tan(math.radians(43.5))*math.tan(math.radians(29))*27/3:.2f} m3 = {4*math.tan(math.radians(43.5))*math.tan(math.radians(29))*9/72*100:.1f} % di 72 m3")
print(f"  1 grado a 3 m = {300*math.tan(math.radians(1)):.1f} cm; 0,5 gradi a 3 m = {300*math.tan(math.radians(0.5)):.1f} cm; 0,5 gradi a 6 m = {600*math.tan(math.radians(0.5)):.1f} cm")
