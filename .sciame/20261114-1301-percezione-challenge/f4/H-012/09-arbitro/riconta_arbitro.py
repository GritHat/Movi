# Riconteggi dell'arbitro (f4, H-012): legge soltanto i file dei risultati, non riesegue nessuna simulazione.
import re, os, sys
B = os.path.dirname(os.path.abspath(__file__)) + "/.."
V = B + "/03-validazione/"
A = B + "/01-avversario/"
def righe(p):
    with open(p, encoding="utf-8") as f:
        return f.read().splitlines()
def r8(nome):
    tot = {}
    for l in righe(V + nome):
        m = re.match(r"\s*(\S+)\s+(principale|BRACCIO)\s+fascia (\S+) errore (\S+) (\S+)\s*: falliti (\d+)/(\d+)", l)
        if not m: continue
        geo, tipo, fascia, err, comp, k, n = m.groups()
        key = (tipo, fascia, err) if tipo == "BRACCIO" else (tipo, err)
        t = tot.setdefault(key, [0, 0, 0, [], set()])
        t[0] += int(k); t[1] += int(n); t[2] += 1; t[3].append(int(k)); t[4].add(geo)
    return tot
for nome in ("v2_R8.txt", "v2_R8_pd09.txt", "v2_R8_cut.txt"):
    print("==", nome)
    tot = r8(nome)
    pk = pn = pc = 0
    for key in sorted(tot):
        k, n, c, lst, geo = tot[key]
        print("  ", key, "falliti", k, "su", n, "celle", c, "min", min(lst), "max", max(lst), "celle>0:", sum(1 for x in lst if x), "geometrie", sorted(geo))
        if key[0] == "principale": pk += k; pn += n; pc += c
    print("   principali in tutto:", pk, "su", pn, "in", pc, "celle")
for nome in ("bis_R8a.txt", "bis_R8b.txt"):
    print("==", nome)
    for l in righe(V + nome):
        m = re.match(r"\s*(.+?)\s+errore -0.2: falliti (\d+)/(\d+).*?soggetto visibile (\d+).*?errore \+0.0: falliti (\d+)/(\d+).*?errore \+0.2: falliti (\d+)/(\d+)", l)
        if m: print("  ", m.group(1), "| -20:", m.group(2), "/", m.group(3), "| 0:", m.group(5), "| +20:", m.group(7), "| accesi(-20):", m.group(4))
print("== bis_FURTO.txt")
s = {}
for l in righe(V + "bis_FURTO.txt"):
    m = re.match(r"\s*(\S+) errore (\S+): sosta (\d+)/(\d+) ; torna (\d+)/(\d+) ; lontano (\d+)/(\d+)", l)
    if m:
        e = m.group(2); g = list(map(int, m.groups()[2:]))
        t = s.setdefault(e, [0]*6)
        for i in range(6): t[i] += g[i]
for e in s: print("  ", e, "sosta %d/%d torna %d/%d lontano %d/%d" % tuple(s[e]))
for nome in ("v2_SECOND.txt", "v2_C6.txt", "v2_WALLP.txt", "v2_MOB.txt", "v2_PD.txt", "bis_DAVANTI.txt"):
    print("==", nome)
    for l in righe(V + nome): print("  ", l[:400])
