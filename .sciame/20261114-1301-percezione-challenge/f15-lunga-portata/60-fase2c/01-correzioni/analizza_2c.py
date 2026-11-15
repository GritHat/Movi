"""analizza_2c.py - riconto per passaggio delle misure della fase 2c (Wilson 95 %). Legge i jsonl di questa cartella."""
import json, math, os, statistics as st
QUI = os.path.dirname(os.path.abspath(__file__))
def W(k, n, z=1.96):
    if n == 0: return [None, None]
    p = k/n; d = 1+z*z/n; c = (p+z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [round(max(0, c-h), 3), round(min(1, c+h), 3)]
def kn(rs, f): k = sum(1 for r in rs if f(r)); return [k, len(rs), W(k, len(rs))]
out = {}
for nome in ("riprova_passaggi_v3.jsonl", "riprova_passaggi_v3_letterale.jsonl"):
    R = [json.loads(l) for l in open(os.path.join(QUI, nome))]
    for cfg in ("alta", "min"):
        rs = [r for r in R if r["scen"] == "A1" and r["cfg"] == cfg]
        if not rs: continue
        nc0 = [r for r in rs if not r["c0"]]
        out[nome + ":A1_" + cfg] = {
            "libero_su_oggetto_non_C0": kn(nc0, lambda r: sum(v for k, v in r["libero_viol"].items() if not k.endswith("_C0")) > 0),
            "libero_su_oggetto_C0": kn([r for r in rs if r["c0"]], lambda r: sum(r["libero_viol"].values()) > 0),
            "istanti_non_C0": [sum(sum(v for k, v in r["libero_viol"].items() if not k.endswith("_C0")) for r in nc0),
                               sum(sum(v for k, v in r["libero_tot"].items() if not k.endswith("_C0")) for r in nc0)],
            "tempestivi": kn(rs, lambda r: r["tempestivo"]), "fuori_avviso": kn(rs, lambda r: r["fuori_avviso"] > 0),
            "senza_regione": kn(rs, lambda r: r["senza_regione"] > 0),
            "fuori_avviso_per_comportamento": {c: sum(1 for r in rs if r["fuori_avviso"] > 0 and r["comportamento"] == c) for c in set(r["comportamento"] for r in rs)},
            "falsi_confermati_mediana": st.median([r["falsi_confermati"] for r in rs])}
E = [json.loads(l) for l in open(os.path.join(QUI, "passaggi_v3.jsonl"))]
for eid in ("E1", "E2", "E5"):
    rs = [r for r in E if r["lavoro"][0] == eid and "errore" not in r]
    A = {"n": len(rs), "errori": sum(1 for r in E if r["lavoro"][0] == eid and "errore" in r)}
    A["evento"] = kn(rs, lambda r: r["evento"] is not None)
    A["entro_2s_0_le_rit"] = kn(rs, lambda r: r["ritardo_evento_s"] is not None and 0 <= r["ritardo_evento_s"] <= 2.0)
    A["prima_dell_urto"] = kn(rs, lambda r: r["ritardo_evento_s"] is not None and r["ritardo_evento_s"] < 0)
    A["falso_evento"] = kn(rs, lambda r: r["falso_evento"])
    rit = [r["ritardo_evento_s"] for r in rs if r["ritardo_evento_s"] is not None]
    A["ritardo_min_med_max"] = [min(rit), st.median(rit), max(rit)] if rit else None
    Rs = [r["evento"]["R_imp_m"] for r in rs if r["evento"]]
    Rr = [r["evento"]["R_residuo_m"] for r in rs if r["evento"]]
    if Rs:
        A["R_imp_m_min_med_max"] = [min(Rs), st.median(Rs), max(Rs)]
        A["R_residuo_m_min_med_max"] = [min(Rr), st.median(Rr), max(Rr)]
        A["R_residuo_ge_10km"] = kn([r for r in rs if r["evento"]], lambda r: r["evento"]["R_residuo_m"] >= 10000)
        A["passaggi_con_ispezione"] = kn([r for r in rs if r["evento"]], lambda r: r["evento"]["ispezionati"][0] > 0)
        A["Tc_s_min_med_max"] = [min(r["evento"]["Tc_s"] for r in rs if r["evento"]), st.median(r["evento"]["Tc_s"] for r in rs if r["evento"]), max(r["evento"]["Tc_s"] for r in rs if r["evento"])]
        A["t_b_meno_t_a_max_s"] = max(r["evento"]["t_b"] - r["evento"]["t_a"] for r in rs if r["evento"])
    A["libero_su_frammento"] = kn(rs, lambda r: r["libero_su_frammento_in_impronta"][0] > 0)
    A["libero_su_frammento_istanti"] = [sum(r["libero_su_frammento_in_impronta"][0] for r in rs), sum(r["libero_su_frammento_in_impronta"][1] for r in rs)]
    A["libero_in_impronta_punti"] = [sum(r["libero_in_impronta_punti"][0] for r in rs), sum(r["libero_in_impronta_punti"][1] for r in rs)]
    A["duplicati_fusi_mediana"] = st.median([r.get("duplicati_fusi", 0) for r in rs]) if rs else None
    A["tracce_avvisate_mediana"] = st.median([r.get("tracce_avvisate", 0) or 0 for r in rs]) if rs else None
    if eid == "E2":
        xs = [r.get("avviso_mezzo1") for r in rs]
        ok = [x for x in xs if x]
        # concordanza: avvisato <=> la verita' del mezzo entra nell'impronta dopo l'evento (dist_min_dopo <= 0)
        A["mezzo_avvisato"] = kn(ok, lambda x: x["t"] is not None)
        A["mezzo_entra_davvero"] = kn(ok, lambda x: x["dist_min_dopo_m"] <= 0)
        A["concordanza_avviso_entrata"] = kn(ok, lambda x: (x["t"] is not None) == (x["dist_min_dopo_m"] <= 0))
        A["mezzo_a_140m_dai_frammenti_veri"] = kn(ok, lambda x: (x.get("dist_dal_frammento_vero_piu_vicino_al_avviso_m") or -1) >= 140)
        A["camere_entro_3_cicli"] = kn(rs, lambda r: len([v for v in r["salute_cicli"].values() if v <= 3]) >= 2)
    out[eid] = A
print(json.dumps(out, indent=1, ensure_ascii=False))
