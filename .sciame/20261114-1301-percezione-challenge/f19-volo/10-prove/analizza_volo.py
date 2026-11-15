"""analizza_volo.py - aggrega passaggi_volo*.jsonl (un record per passaggio) in risultati_volo*.json.
Wilson 95 % PER PASSAGGIO dove l'unita' e' il passaggio; per la calibrazione anche per campione (campioni correlati
dentro un passaggio: quel Wilson e' ottimista, lo si dice). Uso: python -I -B analizza_volo.py passaggi.jsonl uscita.json"""
import json
import math
import sys
from collections import defaultdict

T_EV = {"F3": 20.0, "F4": 30.0}
T_CPA = {"F1": 80.0, "F5": 40.24}


def wilson(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - h) / d, 4), round((c + h) / d, 4)]


def kn(k, n):
    return [k, n, round(k / n, 4) if n else None] + wilson(k, n)


def mediana(x):
    x = sorted(x)
    return None if not x else (x[len(x) // 2] if len(x) % 2 else 0.5 * (x[len(x) // 2 - 1] + x[len(x) // 2]))


FASCE_C = [(0, .2), (.2, .4), (.4, .6), (.6, .8), (.8, .9), (.9, .95), (.95, .99), (.99, 1.0001)]
FASCE_T = [(0, .5), (.5, 1), (1, 2), (2, 3), (3, 5), (5, 10), (10, 1e9)]


def calibrazione(rr, eid):
    out = {}
    for regime in ("nel_modello", "dopo_evento_impulsivo"):
        def sel(c):
            dopo = eid in T_EV and c[0] >= T_EV[eid]
            return dopo if regime == "dopo_evento_impulsivo" else not dopo
        tutti = [(i, c) for i, r in enumerate(rr) for c in r["calib"] if sel(c)]
        if not tutti:
            continue
        R = {"campioni": len(tutti)}
        k99 = sum(c[4] for _, c in tutti)
        R["vero_in_zona99_campioni"] = kn(k99, len(tutti))
        kip = sum(c[4] or c[5] for _, c in tutti)
        R["vero_in_zona99_o_insieme_presenza_campioni"] = kn(kip, len(tutti))
        primo = {}
        for i, c in tutti:
            primo.setdefault(i, c)
        R["vero_in_zona99_primo_per_passaggio"] = kn(sum(c[4] for c in primo.values()), len(primo))
        R["vero_in_zona99_o_insieme_primo_per_passaggio"] = kn(sum(c[4] or c[5] for c in primo.values()), len(primo))
        bande = []
        for a, b in FASCE_C:
            cs = [(i, c) for i, c in tutti if a <= c[2] < b]
            if not cs:
                continue
            pp = {}
            for i, c in cs:
                pp.setdefault(i, c)
            bande.append({"C_prevista": [a, round(min(b, 1), 2)], "C_media": round(sum(c[2] for _, c in cs) / len(cs), 4),
                          "osservata_campioni": kn(sum(c[3] for _, c in cs), len(cs)),
                          "osservata_un_campione_per_passaggio": kn(sum(c[3] for c in pp.values()), len(pp)),
                          "C_media_un_campione_per_passaggio": round(sum(c[2] for c in pp.values()) / len(pp), 4)})
        R["per_fasce_di_C"] = bande
        curva = []
        for a, b in FASCE_T:
            cs = [(i, c) for i, c in tutti if a <= c[1] < b]
            if not cs:
                continue
            curva.append({"tau_s": [a, b if b < 1e8 else None], "C_media": round(sum(c[2] for _, c in cs) / len(cs), 4),
                          "osservata_in_porta": kn(sum(c[3] for _, c in cs), len(cs)),
                          "vero_in_zona99": kn(sum(c[4] for _, c in cs), len(cs)),
                          "vero_in_99_o_insieme": kn(sum(c[4] or c[5] for _, c in cs), len(cs)),
                          "passaggi": len(set(i for i, _ in cs))})
        R["curva_nel_tempo"] = curva
        ecc = sum(abs(bd["C_media"] - bd["osservata_campioni"][2]) * bd["osservata_campioni"][1] for bd in bande) / max(1, len(tutti))
        R["scarto_medio_pesato_C_vs_osservata"] = round(ecc, 4)
        out[regime] = R
    return out


def aggrega(rr, eid):
    n = len(rr)
    A = {"n": n}
    if eid in T_EV:
        rit = [r["ritardo_evento_s"] for r in rr]
        for s in (1.0, 2.0, 3.0):
            A["evento_entro_%gs" % s] = kn(sum(x is not None and x <= s for x in rit), n)
        ok = [x for x in rit if x is not None]
        A["ritardo_s_min_mediana_max"] = [min(ok), mediana(ok), max(ok)] if ok else None
        A["tipi_evento"] = sorted(set(r["evento"]["tipo"] for r in rr if r["evento"]))
        for chi in ("bordo", "operatore"):
            A["tempestivo_" + chi] = kn(sum(r.get("margine_%s_s" % chi) is not None and r["margine_%s_s" % chi] >= 0 for r in rr), n)
            mm = [r["margine_%s_s" % chi] for r in rr if r.get("margine_%s_s" % chi) is not None]
            A["margine_%s_s_mediana" % chi] = mediana(mm)
        A["t_primo_frammento_a_terra_mediana"] = mediana([r["t_primo_frammento_a_terra"] - T_EV[eid] for r in rr if r["t_primo_frammento_a_terra"]])
        dv = [sum(r["frammenti_dentro_V"][0] for r in rr), sum(r["frammenti_dentro_V"][1] for r in rr)]
        A["frammenti_dentro_V_campioni"] = kn(*dv) if dv[1] else None
        A["passaggi_tutti_frammenti_in_V"] = kn(sum(r["frammenti_dentro_V"][1] > 0 and r["frammenti_dentro_V"][0] == r["frammenti_dentro_V"][1] for r in rr),
                                                sum(r["frammenti_dentro_V"][1] > 0 for r in rr))
        A["passaggi_libero_su_frammento_in_impronta"] = kn(sum(r["libero_su_frammento_in_impronta"][0] > 0 for r in rr), n)
        A["libero_in_impronta_punti"] = [sum(r["libero_in_impronta_punti"][0] for r in rr), sum(r["libero_in_impronta_punti"][1] for r in rr)]
        A["R_impronta_m_mediana"] = mediana([r["evento"]["R_imp_m"] for r in rr if r["evento"]])
    else:
        A["falsi_eventi"] = kn(sum(r["evento"] is not None for r in rr), n)
    A["passaggi_libero_sul_vero"] = kn(sum(r["libero_sul_vero"][0] > 0 for r in rr), n)
    A["libero_sul_vero_istanti"] = [sum(r["libero_sul_vero"][0] for r in rr), sum(r["libero_sul_vero"][1] for r in rr)]
    A["continuita_passaggi_senza_buchi"] = kn(sum(sum(r["buchi_continuita"].values()) == 0 for r in rr), n)
    A["continuita_cicli_senza_regione"] = [sum(sum(r["buchi_continuita"].values()) for r in rr), sum(sum(r["campioni_continuita"].values()) for r in rr)]
    if eid in T_EV:
        A["continuita_passaggi_senza_buchi_prima_evento"] = "vedi buchi per oggetto nei passaggi"
    if eid in T_CPA:
        ant = [T_CPA[eid] - r["avviso_prossimita"][0] if r["avviso_prossimita"] else None for r in rr]
        A["avviso_prossimita_anticipo_ge_20s"] = kn(sum(a is not None and a >= 20 for a in ant), n)
        A["avviso_prossimita_anticipo_ge_10s"] = kn(sum(a is not None and a >= 10 for a in ant), n)
        A["avviso_prossimita_anticipo_ge_0s"] = kn(sum(a is not None and a >= 0 for a in ant), n)
        A["anticipo_s_mediana"] = mediana([a for a in ant if a is not None])
    if eid in ("F4", "F5"):
        A["camere_affidabilita_persa_entro_3_cicli"] = kn(sum(len([v for v in r["salute_cicli"].values() if v <= 3]) >= 2 for r in rr), n)
    if eid == "F5":
        sw, nn = 0, 0
        for r in rr:
            a0, a1 = r["assoc_F5"].get("38.5", {}), r["assoc_F5"].get("46.0", {})
            com = [t for t in a0 if t in a1]
            if com:
                nn += 1
                sw += any(a0[t] != a1[t] for t in com)
        A["scambio_identita_passaggi"] = kn(sw, nn)
        for d in (2.0, 3.0, 4.0):
            sub = [r for r in rr if r.get("sep") == d]
            A["falsi_eventi_cecita_%gs" % d] = kn(sum(r["evento"] is not None for r in sub), len(sub))
    A["calibrazione"] = calibrazione(rr, eid)
    A["calcolo_s_mediana"] = mediana([r["durata_calcolo_s"] for r in rr])
    return A


def main():
    src, dst = sys.argv[1], sys.argv[2]
    g = defaultdict(list)
    err = defaultdict(int)
    for riga in open(src, encoding="utf-8"):
        r = json.loads(riga)
        key = "%s/%s" % (r["lavoro"][0], r["lavoro"][1])
        if "errore" in r:
            err[key] += 1
            continue
        g[key].append(r)
    out = {"avvertenza": "SIMULAZIONE (nucleo v3 + strato eventi v3 + estensioni di volo); nessun sensore fisico; stesso simulatore della specifica",
           "sorgente": src, "errori": dict(err), "risultati": {}}
    for key in sorted(g):
        out["risultati"][key] = aggrega(sorted(g[key], key=lambda r: r["idx"]), key.split("/")[0])
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False)[:3000])


if __name__ == "__main__":
    main()
