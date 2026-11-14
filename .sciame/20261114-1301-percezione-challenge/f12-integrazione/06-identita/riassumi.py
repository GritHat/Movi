#!/usr/bin/env python3
"""Tabelle da risultati/<blocco>.jsonl. Uso: python3 riassumi.py <file.jsonl> [...]  (solo libreria standard)."""
import json
import math
import sys
from collections import defaultdict

ORDINE = ["prima", "f401", "f401p", "f402", "f408", "f409", "tutte", "tutte_p", "tutte_p2"]


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def q(k, n):
    if n == 0:
        return "–"
    a, b = wilson(k, n)
    return f"{k}/{n} [{100 * a:.0f}–{100 * b:.0f}]"


def gruppo(r):
    n, t = r["nome"], r["tipo"]
    if t == "disco":
        p = n.split("__")
        return p[0] + " " + p[1]
    return f"{r['profilo']}_{r['livello'][:3]} {t}"


def main():
    for percorso in sys.argv[1:]:
        righe = [json.loads(x) for x in open(percorso, encoding="utf-8") if x.strip()]
        print(f"\n## {percorso.split('/')[-1]} — {len(righe)} righe; errori: {sum(1 for r in righe if r['errore'])}")
        for r in righe:
            if r["errore"]:
                print("  ERRORE", r["nome"], r["conf"], r["errore"])
        G = defaultdict(lambda: defaultdict(list))
        for r in righe:
            if not r["errore"]:
                G[gruppo(r)][r["conf"]].append(r)
        conf = [c for c in ORDINE if any(c in g for g in G.values())]
        print("\n### Continuità dell'identità (continuita_pulita; passaggi con ricomparsa) [IC di Wilson 95 %, in %]")
        print("| caso | " + " | ".join(conf) + " |\n|---|" + "---|" * len(conf))
        for g in sorted(G):
            if not any("esito_identita" in r for r in G[g].get(conf[0], [])):
                continue
            celle = []
            for c in conf:
                rs = [r for r in G[g][c] if r.get("esito_identita") not in (None, "mai nascosto", "non ricompare")]
                celle.append(q(sum(1 for r in rs if r.get("continuita_pulita")), len(rs)))
            print(f"| {g} | " + " | ".join(celle) + " |")
        print("\n### Stessa identità (anche non pulita) | pannello «si muove» (passaggi) | riagganci a soggetto nascosto (passaggi) | fantasmi (mediana per passaggio)")
        print("| caso | " + " | ".join(conf) + " |\n|---|" + "---|" * len(conf))
        for g in sorted(G):
            if not any("esito_identita" in r for r in G[g].get(conf[0], [])):
                continue
            celle = []
            for c in conf:
                rs = [r for r in G[g][c] if "esito_identita" in r]
                st = sum(1 for r in rs if r.get("esito_identita") == "stessa")
                pm = sum(1 for r in rs if r.get("pannello_si_muove"))
                rn = sum(1 for r in rs if (r.get("riagganci_a_soggetto_nascosto") or 0) > 0)
                fa = sorted(r.get("tracce_fantasma", 0) for r in rs)
                celle.append(f"{st} · {pm} · {rn} · {fa[len(fa) // 2] if fa else '–'} (N={len(rs)})")
            print(f"| {g} | " + " | ".join(celle) + " |")
        print("\n### Centro della persona nascosta: fotogrammi fuori dall'avviso (non in possibile presenza né occupato) / nascosti; di cui su «libero»")
        print("| caso | " + " | ".join(conf) + " |\n|---|" + "---|" * len(conf))
        for g in sorted(G):
            if not any(r.get("cella_centro_nascosto") for r in G[g].get(conf[0], [])):
                continue
            celle = []
            for c in conf:
                tot = fuori = lib = 0
                for r in G[g][c]:
                    cc = r.get("cella_centro_nascosto")
                    if not cc:
                        continue
                    tot += sum(cc.values())
                    fuori += cc["non_osservato"] + cc["in_ombra_senza_avviso"] + cc["libero"] + cc["fuori_griglia"]
                    lib += cc["libero"]
                celle.append(f"{q(fuori, tot)}; libero {lib}")
            print(f"| {g} | " + " | ".join(celle) + " |")
        print("\n### Per scena: «libero» nell'ombra vera (celle·fot.) | tracce confermate (scene vuote: somma) | ms per ciclo (media delle medie; p95 massimo) | avviso acceso alla fine")
        print("| caso | " + " | ".join(conf) + " |\n|---|" + "---|" * len(conf))
        for g in sorted(G):
            celle = []
            for c in conf:
                rs = G[g][c]
                lo = sum(r["libero_in_ombra"] for r in rs)
                co = sum(r["celle_ombra_fot"] for r in rs)
                tc = sum(r["tracce_confermate"] for r in rs)
                ms = sum(r["ms_media"] for r in rs) / max(1, len(rs))
                p95 = max((r["ms_p95"] for r in rs), default=0)
                av = sum(1 for r in rs if r["avviso_acceso_alla_fine"])
                muove = sum(r.get("tracce_si_muove", 0) for r in rs)
                celle.append(f"{lo}/{co} · {tc} (muove {muove}) · {ms:.1f}; {p95:.0f} · {av}/{len(rs)}")
            print(f"| {g} | " + " | ".join(celle) + " |")
        print("\n### Ostacoli fermi visti entro 15 cm (fotogrammi)")
        print("| caso | " + " | ".join(conf) + " |\n|---|" + "---|" * len(conf))
        for g in sorted(G):
            if not any(r.get("ostacoli") for r in G[g].get(conf[0], [])):
                continue
            celle = []
            for c in conf:
                v = sum(o["fotogrammi_visto_entro_15cm"] for r in G[g][c] for o in r.get("ostacoli", []))
                n = sum(o["fotogrammi"] for r in G[g][c] for o in r.get("ostacoli", []))
                seq = [min((o["fotogrammi_visto_entro_15cm"] for o in r["ostacoli"]), default=0) for r in G[g][c] if r.get("ostacoli")]
                celle.append(f"{q(v, n)}; sequenze ≥9/10: {sum(1 for s in seq if s >= 9)}/{len(seq)}")
            print(f"| {g} | " + " | ".join(celle) + " |")
        if any(r.get("ferma") for r in righe):
            print("\n### Persona ferma mai vista nell'ombra: fotogrammi fuori dall'avviso dopo l'ingresso di chi cammina | dopo il riaggancio | identità di chi cammina pulita")
            print("| caso | " + " | ".join(conf) + " |\n|---|" + "---|" * len(conf))
            for g in sorted(G):
                celle = []
                for c in conf:
                    rs = [r for r in G[g][c] if r.get("ferma")]
                    a = sum(r["ferma"]["fuori_avviso_dopo_ingresso"] for r in rs)
                    an = sum(r["ferma"]["nascosta_dopo_ingresso"] for r in rs)
                    b = sum(r["ferma"]["fuori_avviso_dopo_riaggancio"] for r in rs)
                    bn = sum(r["ferma"]["nascosta_dopo_riaggancio"] for r in rs)
                    pu = sum(1 for r in rs if r.get("continuita_pulita"))
                    celle.append(f"{q(a, an)} · {q(b, bn)} · {q(pu, len(rs))}")
                print(f"| {g} | " + " | ".join(celle) + " |")


if __name__ == "__main__":
    main()
