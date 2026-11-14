#!/usr/bin/env python3
"""Conti dei profili (f14, 01-profili). Legge classi.json e profili_portatore.json dalla cartella
data come argomento e scrive conti_uscita.md e risultati.json nella stessa cartella.
Uso: python -I -B conti.py CARTELLA
Formula: d_avv = v_rel*(tau + T_r) + v_ego^2/(2*a_fr) + margine, v_rel = v_classe + v_ego (frontale).
Solo conti su valori a priori: niente e' misurato."""
import json, sys, os

def f(x, n=2):
    return "—" if x is None else f"{x:.{n}f}".replace(".", ",")

def main(cart):
    C = json.load(open(os.path.join(cart, "classi.json"), encoding="utf-8"))
    P = json.load(open(os.path.join(cart, "profili_portatore.json"), encoding="utf-8"))
    par = P["parametri_comuni"]
    tau, mar, R = par["tau_latenza_s"], par["margine_m"], par["portata_m"]
    t_fascia = par["eta_dato_s"] + tau + par["tenuta_s"]
    cl = {c["id"]: c for c in C["classi"]}
    veri = [c for c in C["classi"] if c["v_tip"] is not None]
    out, ris = [], {"parametri": par, "classi": {}, "coppie": [], "previsioni": {}}

    def d_avv(v_cl, p):
        s = 0.0 if not p["v_ego"] else p["v_ego"] ** 2 / (2 * p["a_fr"])
        return (v_cl + p["v_ego"]) * (tau + p["T_r"]) + s + mar

    out.append("## A. Per classe: arresto proprio, tempo sui 3 m, fascia di guardia che servirebbe\n")
    out.append(f"Fascia: w_cl = v_max * (eta' {par['eta_dato_s']} + latenza {tau} + tenuta {par['tenuta_s']}) = v_max * {f(t_fascia,3)} s; "
               f"w = {f(mar)} m copre {f(mar/t_fascia)} m/s.\n")
    out.append("| classe | v_tip | v_max | frenata v_tip²/(2·dec_tip) (m) | con reazione di chi guida (m) | tempo per 3 m a v_tip (s) | a v_max (s) | w_cl (m) |")
    out.append("|---|---|---|---|---|---|---|---|")
    for c in veri:
        sb = c["v_tip"] ** 2 / (2 * c["dec_tip"])
        st = None if c["T_r_classe"] is None else c["v_tip"] * c["T_r_classe"] + sb
        w = c["v_max"] * t_fascia
        ris["classi"][c["id"]] = {"s_frenata_m": round(sb, 2), "s_arresto_con_reazione_m": None if st is None else round(st, 2),
                                  "t_3m_tip_s": round(R / c["v_tip"], 2), "t_3m_max_s": round(R / c["v_max"], 2), "w_cl_m": round(w, 2)}
        out.append(f"| {c['id']} | {f(c['v_tip'],1)} | {f(c['v_max'],1)} | {f(sb)} | {f(st)} | {f(R/c['v_tip'])} | {f(R/c['v_max'])} | {f(w)} |")

    out.append("\n## B. Distanza d'avviso d_avv (m) alla velocita' TIPICA della classe, per profilo; in grassetto se <= 3 m\n")
    prof = P["profili"]
    out.append("| classe | " + " | ".join(p["id"] for p in prof) + " |")
    out.append("|---|" + "---|" * len(prof))
    righe = [("ostacolo_fermo", 0.0, 0.0)] + [(c["id"], c["v_tip"], c["v_max"]) for c in veri]
    for nome, vt, vm in righe:
        r = []
        for p in prof:
            d = d_avv(vt, p); dm = d_avv(vm, p)
            ris["coppie"].append({"classe": nome, "profilo": p["id"], "d_avv_tip_m": round(d, 2), "d_avv_max_m": round(dm, 2),
                                  "entro_portata_tip": d <= R, "entro_portata_max": dm <= R, "sensore_in_moto": p["sensore_in_moto"]})
            r.append(f"**{f(d)}**" if d <= R else f(d))
        out.append(f"| {nome} | " + " | ".join(r) + " |")

    out.append("\n## C. Per profilo: spazio d'arresto, velocita' di classe massima coperta dai 3 m, inviluppo del non classificato\n")
    out.append("| profilo | v_ego | T_r | a_fr | arresto proprio v_ego·(τ+T_r)+v²/2a (m) | v di classe massima coperta da 3 m (m/s) | classi ammesse: v_max d'inviluppo (m/s) | d_avv del non classificato (m) | portata che servirebbe alla v_max di persona_a_piedi (m) |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    ris["profili"] = {}
    for p in prof:
        s = 0.0 if not p["v_ego"] else p["v_ego"] ** 2 / (2 * p["a_fr"])
        proprio = p["v_ego"] * (tau + p["T_r"]) + s
        vcop = (R - mar - s) / (tau + p["T_r"]) - p["v_ego"]
        venv = max(cl[i]["v_max"] for i in p["classi_ammesse"])
        denv = d_avv(venv, p)
        dped = d_avv(cl["persona_a_piedi"]["v_max"], p)
        ris["profili"][p["id"]] = {"arresto_proprio_m": round(proprio, 2), "v_classe_coperta_ms": round(vcop, 2),
                                   "v_inviluppo_ms": venv, "d_avv_non_classificato_m": round(denv, 2), "d_avv_pedone_vmax_m": round(dped, 2)}
        out.append(f"| {p['id']} | {f(p['v_ego'],1)} | {f(p['T_r'],1)} | {f(p['a_fr'],1)} | {f(proprio)} | {f(vcop)} | {f(venv,1)} | {f(denv)} | {f(dped)} |")

    out.append("\n## D. Etichetta sbagliata: di quanto si accorcerebbe l'avviso se la distanza dipendesse SOLO dall'etichetta\n")
    out.append("Stazione fissa, v_max di classe. «Vero» = classe reale; «detto» = etichetta. Deficit = d_avv(vero) − d_avv(detto).\n")
    out.append("| vero | detto | d_avv vero (m) | d_avv detto (m) | deficit (m) | con la regola max(base, classe) e inviluppo per l'incerto |")
    out.append("|---|---|---|---|---|---|")
    p0 = prof[0]
    amm = ["persona_a_piedi", "carrello_elevatore", "auto_area_lavoro"]
    venv = max(cl[i]["v_max"] for i in amm)
    ris["etichetta_sbagliata"] = []
    for vero, detto in [("auto_area_lavoro", "persona_a_piedi"), ("carrello_elevatore", "persona_a_piedi"), ("carrello_elevatore", "agv_magazzino"), ("persona_di_corsa", "persona_a_piedi")]:
        dv, dd = d_avv(cl[vero]["v_max"], p0), d_avv(cl[detto]["v_max"], p0)
        ris["etichetta_sbagliata"].append({"vero": vero, "detto": detto, "deficit_m": round(dv - dd, 2)})
        out.append(f"| {vero} | {detto} | {f(dv)} | {f(dd)} | {f(dv-dd)} | un'etichetta sicura ma sbagliata NON e' coperta dalla regola: resta il deficit; l'etichetta incerta prende l'inviluppo ({f(d_avv(venv,p0))} m con {', '.join(amm)}) |")

    # Previsioni
    g = lambda c, p: next(x for x in ris["coppie"] if x["classe"] == c and x["profilo"] == p)
    e1 = g("persona_a_piedi", "stazione_fissa")["d_avv_tip_m"]
    e2 = d_avv(8.0, p0)
    n3 = sum(1 for c in veri if g(c["id"], "stazione_fissa")["d_avv_tip_m"] > R)
    e4a = g("ostacolo_fermo", "persona_non_vedente_bastone")["d_avv_tip_m"]; e4b = g("persona_a_piedi", "persona_non_vedente_bastone")["d_avv_tip_m"]
    e5p = g("persona_a_piedi", "ugv_lento")["d_avv_tip_m"]
    pu = next(p for p in prof if p["id"] == "ugv_lento")
    e5v = d_avv(5.0, pu)
    e6t = g("treno_banchina", "stazione_fissa")["d_avv_tip_m"]; e6a = g("aereo_rullaggio", "stazione_fissa")["d_avv_tip_m"]
    nv = sum(1 for c in veri for k in ("v_tip", "v_max") if c["fonti"].get(k, "I").startswith("F"))
    nr = sum(1 for c in veri for k in ("v_tip", "v_max") if c["fonti"].get(k, "I").startswith("R"))
    tot = 2 * len(veri)
    prev = {
        "E1": (f"d_avv = {f(e1)} m", "regge" if e1 <= R else "smentita"),
        "E2": (f"d_avv a 8 m/s = {f(e2)} m", "regge" if (e2 > R and 8 <= e2 <= 12) else "smentita"),
        "E3": (f"{n3} classi su {len(veri)} oltre 3 m", "regge" if n3 >= 8 else "smentita"),
        "E4": (f"ostacolo fermo {f(e4a)} m; pedone incontro {f(e4b)} m", "regge" if (e4a <= R and e4b > R) else "smentita"),
        "E5": (f"pedone {f(e5p)} m; veicolo a 5 m/s {f(e5v)} m", "regge" if (e5p <= R and e5v > R) else "smentita"),
        "E6": (f"treno in banchina {f(e6t)} m; aereo in rullaggio {f(e6a)} m", "regge" if (e6t > 20 and e6a > 20) else "smentita"),
        "E7": (f"velocita' con fonte aperta oggi: {nv} su {tot}; lette solo in un risultato di ricerca: {nr}; ipotesi o memoria: {tot-nv-nr}", "regge" if nv >= 2 * tot / 3 else ("smentita" if nv < tot / 2 else "non risolta")),
    }
    ris["previsioni"] = {k: {"misura": v[0], "esito": v[1]} for k, v in prev.items()}
    out.append("\n## E. Esiti delle previsioni (soglie scritte prima, in PREVISIONI.md)\n")
    out.append("| # | misura | esito |\n|---|---|---|")
    for k, v in prev.items():
        out.append(f"| {k} | {v[0]} | {v[1]} |")
    open(os.path.join(cart, "conti_uscita.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    json.dump(ris, open(os.path.join(cart, "risultati.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(out))

if __name__ == "__main__":
    main(sys.argv[1])
