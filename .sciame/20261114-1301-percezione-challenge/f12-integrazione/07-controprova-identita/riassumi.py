#!/usr/bin/env python3
"""Riassume risultati/att_*.jsonl (gli attacchi di attacco.py): una riga per gruppo e configurazione, con Wilson 95 %.
Uso: python3 riassumi.py > risultati/ATTACCHI.md"""
import glob
import json
import math
import os
import statistics

QUI = os.path.dirname(os.path.abspath(__file__))


def wilson(k, n, z=1.96):
    if n == 0:
        return "[–]"
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return f"[{100 * max(0, c - h):.0f}–{100 * min(1, c + h):.0f}]"


def q(k, n):
    return f"{k}/{n} {wilson(k, n)}"


R = []
for p in sorted(glob.glob(os.path.join(QUI, "risultati", "att_*.jsonl"))):
    with open(p, encoding="utf-8") as f:
        R += [json.loads(r) for r in f if r.strip()]
gruppi = sorted({r["gruppo"] for r in R})
print(f"# Attacchi di 07-controprova-identita — {len(R)} righe, {len(gruppi)} gruppi (semi k = 300…; tutto simulazione)\n")
tot_lib = {}
for g in gruppi:
    print(f"## {g}")
    for conf in ("prima", "tutte_p"):
        rr = [r for r in R if r["gruppo"] == g and r["conf"] == conf]
        if not rr:
            continue
        err = [r for r in rr if r.get("errore")]
        rr = [r for r in rr if not r.get("errore")]
        lib = sum(r["libero_in_ombra"] for r in rr)
        omb = sum(r["celle_ombra_fot"] for r in rr)
        tot_lib[conf] = tot_lib.get(conf, 0) + lib
        s = [f"N = {len(rr)} sequenze" + (f", {len(err)} ERRORI: {err[0]['errore'][:80]}" if err else ""),
             f"«libero» in ombra vera {lib}/{omb}", f"tracce confermate {sum(r['tracce_confermate'] for r in rr)}"]
        t = rr[0]["tipo"] if rr else None
        if t == "passa" and "rimozione" not in rr[0]:
            n = len(rr)
            k = sum(r.get("continuita_pulita") is True for r in rr)
            es = {}
            for r in rr:
                es[str(r.get("esito_identita"))] = es.get(str(r.get("esito_identita")), 0) + 1
            fuori = sum(v for r in rr for k_, v in (r.get("cella_centro_nascosto") or {}).items()
                        if k_ not in ("possibile_presenza", "fuori_griglia"))
            fg = sum((r.get("cella_centro_nascosto") or {}).get("fuori_griglia", 0) for r in rr)
            libc = sum((r.get("cella_centro_nascosto") or {}).get("libero", 0) for r in rr)
            nasc = sum(r.get("nascosti") or 0 for r in rr)
            s += [f"**continuità {q(k, n)}**", f"esiti {es}", f"nascosta in griglia fuori dall'avviso {fuori}/{nasc - fg} fot. (di cui cella «libero» {libc}; fuori griglia {fg})",
                  f"riagganci a persona nascosta {sum(r.get('riagganci_a_soggetto_nascosto') or 0 for r in rr)}",
                  f"pannello «in movimento» {sum(bool(r.get('pannello_si_muove')) for r in rr)}/{n}"]
            vv = [r["vuoto"] for r in rr if r.get("vuoto") and r["vuoto"]["dopo"]]
            if vv:
                s.append(f"dopo l'ombra: visibile ≥ 50 % senza traccia {sum(v['senza_traccia'] for v in vv)}/{sum(v['dopo'] for v in vv)} fot. "
                         f"(mediana per passaggio {statistics.median(v['senza_traccia'] for v in vv)}, massimo {max(v['senza_traccia'] for v in vv)}); "
                         f"mai ritracciata in {sum(v['attesa_prima_traccia'] is None for v in vv)}/{len(vv)}; "
                         f"avviso acceso dopo l'ombra {sum(v['avviso_acceso_dopo'] for v in vv)}/{sum(v['fotogrammi_dopo_ombra'] for v in vv)} fot.")
            mot = {}
            for r in rr:
                for m in r.get("motivi_ambigua") or []:
                    mot[m] = mot.get(m, 0) + 1
            if mot:
                s.append("motivi di «identità ambigua» (passaggi): " + "; ".join(f"{m}: {c}" for m, c in sorted(mot.items(), key=lambda x: -x[1])[:4]))
        if rr and "rimozione" in rr[0]:
            x = [r["rimozione"] for r in rr]
            s.append(f"**avviso acceso alla rimozione del pannello {sum(v['acceso_alla_rimozione'] for v in x)}/{len(x)}; "
                     f"ancora acceso 30 fot. dopo {q(sum(v['acceso_alla_fine'] for v in x), len(x))}**; ultimo fotogramma acceso dopo la rimozione: "
                     f"{sorted(v['ultimo_acceso'] for v in x)}")
        if t == "estraneo":
            x = [r["estraneo"] for r in rr if r["estraneo"].get("idA") is not None]
            s += [f"A tracciata prima {len(x)}/{len(rr)}", f"**identità di A passata a B {q(sum(v['identita_passata_a_B'] for v in x), len(x))}**",
                  f"B senza alcuna traccia {sum(v['idB'] is None for v in x)}",
                  f"A nascosta fuori dall'avviso: sempre {sum(v['A_fuori_avviso'] for v in x)}/{sum(v['A_nascosta'] for v in x)} fot.; "
                  f"**dopo l'uscita di B {sum(v['A_fuori_avviso_dopo_B'] for v in x)}/{sum(v['A_nascosta_dopo_B'] for v in x)}**; "
                  f"dopo il riaggancio {sum(v['A_fuori_avviso_dopo_riaggancio'] for v in x)}/{sum(v['A_nascosta_dopo_riaggancio'] for v in x)}",
                  f"cella di A «libero» {sum(v['A_cella_libero'] for v in x)} fot.", f"riagganci {sum(v['riagganci'] for v in x)}"]
        if t == "statica":
            if any("ostacoli" in r for r in rr):
                v = sum(o["fotogrammi_visto_entro_15cm"] for r in rr for o in r.get("ostacoli", []) if o["ostacolo"] != "pannello")
                n = sum(o["fotogrammi"] for r in rr for o in r.get("ostacoli", []) if o["ostacolo"] != "pannello")
                if n:
                    s.append(f"**«occupato» entro 15 cm dall'ostacolo {q(v, n)} fot.**")
            if any("gruppo_sul_bersaglio" in r for r in rr):
                n = sum(r["fotogrammi"] for r in rr)
                s.append(f"**gruppo proprio sul bersaglio {q(sum(r['gruppo_sul_bersaglio'] for r in rr), n)} fot.**; "
                         f"traccia «osservato» sul bersaglio {q(sum(r['traccia_sul_bersaglio'] for r in rr), n)}")
        print(f"- **{conf}** — " + "; ".join(s))
    print()
print(f"**Somma di «libero» nell'ombra vera su tutti gli attacchi:** {tot_lib}")
