#!/usr/bin/env python3
"""Le cifre del rapporto, compatte: python3 cifre.py risultati/<blocco>.jsonl [...]  (solo libreria standard)."""
import json, sys
from collections import defaultdict
from riassumi import wilson, ORDINE

def q(k, n):
    if not n:
        return "–"
    a, b = wilson(k, n)
    return f"{k}/{n} [{100*a:.0f}–{100*b:.0f}]"

for percorso in sys.argv[1:]:
    R = [json.loads(x) for x in open(percorso, encoding="utf-8") if x.strip()]
    R = [r for r in R if not r["errore"]]
    conf = [c for c in ORDINE if any(r["conf"] == c for r in R)]
    print(f"\n== {percorso.split('/')[-1]} ({len(R)} righe) ==  colonne: " + " | ".join(conf))
    def nom(r): return r.get("livello", "nominale") != "limite" and "_lim__" not in r["nome"]
    def riga(titolo, f):
        print(f"{titolo}: " + " | ".join(f([r for r in R if r["conf"] == c]) for c in conf))
    P = lambda rs, lim=False: [r for r in rs if r.get("esito_identita") not in (None, "mai nascosto", "non ricompare") and (nom(r) != lim)]
    riga("continuità, nominale, tutti i casi", lambda rs: q(sum(bool(r.get("continuita_pulita")) for r in P(rs)), len(P(rs))))
    riga("continuità, limite", lambda rs: q(sum(bool(r.get("continuita_pulita")) for r in P(rs, True)), len(P(rs, True))))
    riga("passaggi nominali con pannello «si muove»", lambda rs: q(sum(bool(r.get("pannello_si_muove")) for r in rs if "esito_identita" in r and nom(r)), sum(1 for r in rs if "esito_identita" in r and nom(r))))
    riga("passaggi nominali con riaggancio a soggetto nascosto", lambda rs: q(sum((r.get("riagganci_a_soggetto_nascosto") or 0) > 0 for r in rs if "esito_identita" in r and nom(r)), sum(1 for r in rs if "esito_identita" in r and nom(r))))
    def fuori(rs):
        t = f = l = 0
        for r in rs:
            cc = r.get("cella_centro_nascosto")
            if cc and nom(r) and "_d__" not in r["nome"]:
                t += sum(cc.values()); l += cc["libero"]
                f += cc["non_osservato"] + cc["in_ombra_senza_avviso"] + cc["libero"] + cc["fuori_griglia"]
        return q(f, t) + f" lib {l}"
    riga("nascosta fuori dall'avviso (fot., nominale, senza il caso d)", fuori)
    riga("«libero» nell'ombra vera (celle·fot., tutto)", lambda rs: f"{sum(r['libero_in_ombra'] for r in rs)}/{sum(r['celle_ombra_fot'] for r in rs)}")
    riga("di cui nelle scene della scatola", lambda rs: f"{sum(r['libero_in_ombra'] for r in rs if 'scatola' in r['nome'])}")
    V = lambda rs, lim=False: [r for r in rs if "pavimento" in r["nome"] and (nom(r) != lim)]
    riga("pavimento vuoto nominale: tracce confermate (sequenze)", lambda rs: f"{sum(r['tracce_confermate'] for r in V(rs))} ({len(V(rs))})")
    riga("pavimento vuoto limite: tracce confermate (sequenze)", lambda rs: f"{sum(r['tracce_confermate'] for r in V(rs, True))} ({len(V(rs, True))})")
    def scat(rs):
        v = sum(o["fotogrammi_visto_entro_15cm"] for r in rs if "scatola" in r["nome"] for o in r.get("ostacoli", []))
        n = sum(o["fotogrammi"] for r in rs if "scatola" in r["nome"] for o in r.get("ostacoli", []))
        s = [r for r in rs if "scatola" in r["nome"]]
        return q(v, n) + f"; avviso acceso {sum(r['avviso_acceso_alla_fine'] for r in s)}/{len(s)}; tracce {sum(r['tracce_confermate'] for r in s)}"
    riga("scatola 15 cm a 2 m vista (fot.)", scat)
    def costo(rs, lim=False):
        rs = [r for r in rs if nom(r) != lim]
        n = sum(r["fotogrammi"] for r in rs)
        return f"{sum(r['ms_media'] * r['fotogrammi'] for r in rs) / max(1, n):.1f}; p95 max {max((r['ms_p95'] for r in rs), default=0):.0f}; max {max((r['ms_max'] for r in rs), default=0):.0f}" if n else "–"
    riga("costo per ciclo nominale, ms (media; p95 peggiore; massimo)", costo)
    riga("costo per ciclo limite, ms", lambda rs: costo(rs, True))
    riga("passaggi nominali che finiscono con l'avviso acceso", lambda rs: q(sum(r["avviso_acceso_alla_fine"] for r in rs if "esito_identita" in r and nom(r)), sum(1 for r in rs if "esito_identita" in r and nom(r))))
    for c in ("tutte_p",):
        for r in R:
            if r["conf"] == c and r.get("esito_identita") not in (None, "mai nascosto", "non ricompare") and not r.get("continuita_pulita") and nom(r):
                print(f"   non pulito [{c}] {r['nome']}: {r['esito_identita']}; osservato a nascosto {r['stato_traccia_nascosto']['osservato']}; riagganci a nascosto {r['riagganci_a_soggetto_nascosto']}; motivi {r['motivi_ambigua']}")
