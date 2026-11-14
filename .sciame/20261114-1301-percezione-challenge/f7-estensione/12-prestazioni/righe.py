# righe.py — righe di C non vuote compilate per ogni rappresentazione (misura grezza della taglia del codice). Uso: python3 -I righe.py
import re
src = open("banco.c").read().split("\n")
R = dict(R_POLARE=1, R_IMMAGINE=2, R_FASCE=3, R_DENSA=4, R_HASH=5, R_HASHOCC=6, R_OCTREE=7, R_OCTPOT=8, R_COLBIT=9)
def conta(rep):
    env = dict(R); env["REP"] = R[rep]; env["E_VOXEL"] = R[rep] in (4, 5, 6, 7, 8)
    ev = lambda e: bool(eval(e.replace("||", " or ").replace("&&", " and ").replace("!", " not ").replace(" not =", "!="), {}, env))
    pila = []; n = set()
    for i, r in enumerate(src):
        s = r.strip()
        if s.startswith("#ifndef") or s.startswith("#error"): 
            if s.startswith("#ifndef"): pila.append([False, True])
            continue
        if s.startswith("#if "): a = ev(s[4:].split("/*")[0]); pila.append([a, a]); continue
        if s.startswith("#elif "): a = (not pila[-1][1]) and ev(s[6:].split("/*")[0]); pila[-1][0] = a; pila[-1][1] |= a; continue
        if s.startswith("#else"): pila[-1][0] = not pila[-1][1]; continue
        if s.startswith("#endif"): pila.pop(); continue
        if all(p[0] for p in pila) and s and not s.startswith("/*") and not s.startswith("*") and not s.startswith("//"): n.add(i)
    return n
tot = {k: conta(k) for k in R}
com = set.intersection(*tot.values())
print("righe comuni a tutte (sensore simulato, scene, statistiche, main):", len(com))
for k, v in tot.items(): print(f"{k:12s} righe proprie {len(v - com):4d}")
