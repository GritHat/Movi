#!/usr/bin/env python3
"""Misure 4 e 5 sui passaggi simulati dietro il pannello: identità alla ricomparsa, stati a soggetto nascosto,
strato di possibile presenza, errore della previsione (filtro del nucleo e due linee di base) contro il tempo
d'occlusione, copertura della regione dichiarata, falsi «si muove» sul pannello, tracce fantasma.

Legge uscite/<etichetta>/<sequenza>/{fotogrammi.jsonl, griglie.npz, ingressi.json} e la verità del simulatore.
Uso: <python> -I -B misura_passaggi.py [etichetta]   → uscite/<etichetta>/misura_passaggi.json e una tabella."""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune as K                                             # noqa: E402
import numpy as np                                             # noqa: E402

CHI2_90, CHI2_95 = 4.605, 5.9915
FASCE = [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 99.0)]
NOMI_FASCE = ["0-0,25", "0,25-0,5", "0,5-0,75", "0,75-1", "1-2", "2-3", ">3"]


def traccia_del_soggetto(riga, x, z, raggio=0.5, solo_osservato=True):
    """La traccia con una misura nel ciclo più vicina alla verità (entro `raggio`), o None."""
    meglio, d_meglio = None, raggio
    for tr in riga["tracce"]:
        if not tr["misura_nel_ciclo"]:
            continue
        if solo_osservato and tr["stato"] != "osservato":
            continue
        d = math.hypot(tr["ultima_misura"][0] - x, tr["ultima_misura"][1] - z)
        if d <= d_meglio:
            meglio, d_meglio = tr, d
    return meglio


def sul_pannello(x, z):
    return abs(x) <= 0.65 and 1.6 <= z <= 2.0


def misura(nome, radice):
    usc = os.path.join(radice, nome)
    righe = K.leggi_righe(usc)
    g = K.leggi_griglie(usc)
    stati, pres = g["stati"], g["possibile_presenza"]
    ver = K.leggi_verita(os.path.join(K.SEQ_SIM, nome))
    with open(os.path.join(usc, "ingressi.json"), encoding="utf-8") as f:
        ingressi = json.load(f)["ingressi"]
    T = len(righe)
    sog = [f["soggetti"][0] for f in ver["fotogrammi"][:T]]
    t = np.array([r["t"] for r in righe])
    fraz = np.array([s["frazione_visibile"] for s in sog])
    vx = np.array([s["x"] for s in sog])
    vz = np.array([s["z"] for s in sog])
    nasc = np.nonzero(fraz < 0.02)[0]
    out = {"nome": nome, "fotogrammi": T, "nascosti": int(len(nasc))}
    # tracce fantasma e falsi «si muove»
    conf, sul_sogg, pann, muove_pann, muove_fant = set(), set(), set(), set(), set()
    for k, r in enumerate(righe):
        for tr in r["tracce"]:
            if tr["stato"] == "in_conferma":
                continue
            conf.add(tr["id"])
            mx, mz = tr["ultima_misura"][0], tr["ultima_misura"][1]
            if math.hypot(mx - vx[k], mz - vz[k]) <= 0.5 and fraz[k] >= 0.02:
                sul_sogg.add(tr["id"])
            elif sul_pannello(mx, mz):
                pann.add(tr["id"])
                if tr["si_muove"] is True:
                    muove_pann.add(tr["id"])
    for k, r in enumerate(righe):
        for tr in r["tracce"]:
            if tr["id"] in conf and tr["id"] not in sul_sogg and tr["id"] not in pann and tr["si_muove"] is True:
                muove_fant.add(tr["id"])
    out.update(tracce_confermate=len(conf), tracce_fantasma=len(conf - sul_sogg - pann),
               pannello_si_muove=len(muove_pann) > 0, fantasmi_si_muove=len(muove_fant))
    if len(nasc) == 0:
        out["esito_identita"] = "mai nascosto"
        return out
    k0, k1 = int(nasc[0]), int(nasc[-1])
    out["t_nascosto_s"] = float(t[k1] - t[k0] + (t[1] - t[0]))
    # --- prima dell'ombra: l'identità più frequente sui fotogrammi in cui il soggetto è intero (corretto dopo la
    #     prima corsa: l'ultimo fotogramma utile poteva dare la traccia del pannello fuso con la persona)
    id_prima, storia = None, []
    primo_visto = None
    voti = {}
    for k in range(k0):
        tr = traccia_del_soggetto(righe[k], vx[k], vz[k])
        if tr is not None and primo_visto is None:
            primo_visto = k
        if tr is not None and fraz[k] >= 0.98:
            voti[tr["id"]] = voti.get(tr["id"], 0) + 1
    if voti:
        id_prima = max(voti, key=lambda i: (voti[i], -i))
    # fusione persona–pannello: un gruppo sul pannello più largo di 1,2 m mentre il soggetto è ancora in vista
    fus_interi, fus_parziali = 0, 0
    for k in range(T):
        if fraz[k] < 0.5:
            continue
        if any(abs(g_["x"]) < 0.6 and 1.6 < g_["z"] < 2.1 and g_["larghezza_m"] > 1.2 for g_ in righe[k]["gruppi"]):
            fus_parziali += 1
            fus_interi += fraz[k] >= 0.98
    out["fusione_fotogrammi_interi"] = int(fus_interi)
    out["fusione_fotogrammi"] = int(fus_parziali)
    out["riagganci_a_soggetto_nascosto"] = sum(1 for k in nasc for e in righe[k]["eventi"] if e["tipo"] == "riaggancio")
    out["id_prima"] = id_prima
    interi = int((fraz[:k0] >= 0.98).sum())
    out["fotogrammi_interi_prima"] = interi
    # scarto sistematico centro misurato − verità (radiale, trasversale) e misure piene della traccia
    scarti, muove_t = [], None
    if id_prima is not None:
        for k in range(k0):
            for tr in righe[k]["tracce"]:
                if tr["id"] != id_prima:
                    continue
                if tr["si_muove"] is True and muove_t is None:
                    muove_t = float(t[k])
                if tr["misura_nel_ciclo"] and not tr["misura_tagliata"]:
                    mx, mz = tr["ultima_misura"][0], tr["ultima_misura"][1]
                    storia.append((float(t[k]), mx, mz))
                    if fraz[k] >= 0.98:
                        d = math.hypot(vx[k], vz[k])
                        ur, ut = (vx[k] / d, vz[k] / d), (vz[k] / d, -vx[k] / d)
                        ex, ez = mx - vx[k], mz - vz[k]
                        scarti.append((ex * ur[0] + ez * ur[1], ex * ut[0] + ez * ut[1]))
    o_r, o_t = (np.mean(scarti, axis=0) if scarti else (0.0, 0.0))
    out["scarto_centro_m"] = [float(o_r), float(o_t)]
    out["sigma_centro_in_moto_m"] = [float(v) for v in np.std(scarti, axis=0)] if len(scarti) >= 4 else None
    out["soggetto_si_muove_prima"] = muove_t is not None
    out["si_muove_dopo_s"] = (muove_t - float(t[primo_visto])) if (muove_t is not None and primo_visto is not None) else None

    def vera_misurata(k):
        d = math.hypot(vx[k], vz[k])
        return vx[k] + o_r * vx[k] / d + o_t * vz[k] / d, vz[k] + o_r * vz[k] / d - o_t * vx[k] / d

    # --- a soggetto nascosto: stato della traccia, cella del centro vero
    st_tr = {"osservato": 0, "previsto": 0, "perso": 0, "assente": 0, "altro": 0}
    cella_c = {"possibile_presenza": 0, "occupato": 0, "non_osservato": 0, "in_ombra_senza_avviso": 0, "libero": 0,
               "fuori_griglia": 0}
    ing = [i for i in ingressi if i["id"] == id_prima]
    err = {m: [[] for _ in FASCE] for m in ("nucleo", "fermo", "retta")}
    dentro90, dentro95, n_prev = 0, 0, 0
    retta = None
    if len(storia) >= 3:
        ult = storia[-8:]
        tt = np.array([u[0] for u in ult])
        ax = np.polyfit(tt, [u[1] for u in ult], 1)
        az = np.polyfit(tt, [u[2] for u in ult], 1)
        retta = (ax, az)
    for k in nasc:
        riga = righe[k]
        tr = next((x for x in riga["tracce"] if x["id"] == id_prima), None) if id_prima is not None else None
        if tr is None:
            st_tr["assente"] += 1
        else:
            st_tr[tr["stato"] if tr["stato"] in st_tr else "altro"] += 1
        c = K.cella(vx[k], vz[k])
        if c is None:
            cella_c["fuori_griglia"] += 1
        elif pres[k][c]:
            cella_c["possibile_presenza"] += 1
        elif stati[k][c] == K.OCCUPATO:
            cella_c["occupato"] += 1
        elif stati[k][c] == K.NON_OSSERVATO:
            cella_c["non_osservato"] += 1
        elif stati[k][c] == K.IN_OMBRA:
            cella_c["in_ombra_senza_avviso"] += 1
        else:
            cella_c["libero"] += 1
        tau = float(t[k] - t[k0])
        fb = next(i for i, (a, b) in enumerate(FASCE) if a <= tau < b)
        mx, mz = vera_misurata(k)
        if tr is not None and "previsione_diagnostica" in tr:
            d = tr["previsione_diagnostica"]
            e = np.array([d["x"] - mx, d["z"] - mz])
            err["nucleo"][fb].append(float(np.hypot(*e)))
            cxx, cxz, czz = d["covarianza"]
            p = np.array([[cxx, cxz], [cxz, czz]])
            m2 = float(e @ np.linalg.solve(p, e))
            dentro90 += m2 <= CHI2_90
            dentro95 += float(np.hypot(*e)) <= d["raggio95_m"]
            n_prev += 1
        if storia:
            err["fermo"][fb].append(math.hypot(storia[-1][1] - mx, storia[-1][2] - mz))
        if retta is not None:
            err["retta"][fb].append(math.hypot(np.polyval(retta[0], t[k]) - mx, np.polyval(retta[1], t[k]) - mz))
    out["stato_traccia_nascosto"] = st_tr
    out["cella_centro_nascosto"] = cella_c
    out["errore_per_fascia"] = {m: [float(np.mean(v)) if v else None for v in err[m]] for m in err}
    out["previsioni"] = n_prev
    out["copertura90"] = dentro90 / n_prev if n_prev else None
    out["copertura95_cerchio"] = dentro95 / n_prev if n_prev else None
    out["ingressi"] = len(ing)
    if ing:
        out["buio_prima_dell_ingresso_s"] = ing[0]["t"] - ing[0]["ultima_misura"][2]
        out["ingresso_meno_primo_nascosto_s"] = ing[0]["t"] - float(t[k0])
        out["velocita_ingresso"] = [ing[0]["x"][2], ing[0]["x"][3]]
        out["velocita_vera_ingresso"] = [sog[k0]["vx"], sog[k0]["vz"]]
    # --- eventi della traccia
    ev = {"riaggancio": [], "identita_ambigua": [], "perso": [], "strato_finito": [], "chiusura": []}
    for r in righe:
        for e in r["eventi"]:
            if e.get("id") == id_prima and e["tipo"] in ev:
                ev[e["tipo"]].append(dict(e, t=r["t"]))
    out["eventi"] = {k_: len(v) for k_, v in ev.items()}
    out["motivi_ambigua"] = sorted(set(e["motivo"] for e in ev["identita_ambigua"]))
    out["previsto_s"] = ev["perso"][0]["previsto_s"] if ev["perso"] else None
    if ev["riaggancio"]:
        e = ev["riaggancio"][0]
        out["riaggancio"] = {k_: e[k_] for k_ in ("durata_s", "buio_s", "errore_previsione_m", "raggio95_m", "d2",
                                                  "in95", "misura_tagliata", "stato_prima")}
        out["riaggancio"]["in90"] = e["d2"] <= CHI2_90
    # --- ricomparsa
    dopo = [k for k in range(k1 + 1, T) if fraz[k] >= 0.5]
    out["fotogrammi_dopo"] = len(dopo)
    if not dopo:
        out["esito_identita"] = "non ricompare"
    elif id_prima is None:
        out["esito_identita"] = "nessuna traccia prima"
    else:
        id_dopo, quando = None, None
        voti_d = {}
        for k in dopo:
            tr = traccia_del_soggetto(righe[k], vx[k], vz[k])
            if tr is not None and fraz[k] >= 0.98:
                voti_d[tr["id"]] = voti_d.get(tr["id"], 0) + 1
                if quando is None:
                    quando = k
        if voti_d:
            id_dopo = max(voti_d, key=lambda i: (voti_d[i], -i))
        if id_dopo is None:
            out["esito_identita"] = "nessuna traccia dopo"
        else:
            out["esito_identita"] = "stessa" if id_dopo == id_prima else "diversa"
            out["continuita_pulita"] = bool(id_dopo == id_prima and st_tr["osservato"] == 0
                                            and not any(e["t"] <= float(t[k1]) for e in ev["riaggancio"]))
            out["ritardo_ritraccia_s"] = float(t[quando] - t[dopo[0]])
            # errore delle linee di base e del nucleo alla prima misura dopo (contro la misura, non la verità)
            trd = traccia_del_soggetto(righe[quando], vx[quando], vz[quando])
            mx, mz = trd["ultima_misura"][0], trd["ultima_misura"][1]
            b = {}
            if storia:
                b["fermo"] = math.hypot(storia[-1][1] - mx, storia[-1][2] - mz)
            if retta is not None:
                b["retta"] = math.hypot(np.polyval(retta[0], t[quando]) - mx, np.polyval(retta[1], t[quando]) - mz)
            if ing:
                i0 = ing[0]
                tau = float(t[quando]) - i0["t"]
                b["nucleo"] = math.hypot(i0["x"][0] + i0["x"][2] * tau - mx, i0["x"][1] + i0["x"][3] * tau - mz)
                # regione al 90 % dichiarata dal filtro del nucleo a questo istante (forma chiusa, q della corsa)
                b["tau_s"] = tau
            out["errore_alla_ricomparsa"] = b
    return out


def riepilogo(tutti, radice):
    def gruppo(n):
        p = n.split("__")
        return p[0] + "__" + p[1] + ("__filtri" if n.endswith("__filtri") else "")
    gruppi = {}
    for m in tutti:
        gruppi.setdefault(gruppo(m["nome"]), []).append(m)
    med = lambda v: (f"{np.median(v):.2f}" if len(v) else "—")                                  # noqa: E731
    print("== identità alla ricomparsa e stati a soggetto nascosto ==")
    print("gruppo; N; stessa identità; diversa; nessuna traccia dopo; nessuna prima; non ricompare; riagganci; "
          "passaggi con «identità ambigua» [motivi]; passaggi con ≥1 fot. «osservato» a soggetto nascosto; "
          "fotogrammi nascosti: traccia previsto/perso/assente/osservato; cella del centro: possibile presenza / "
          "occupato / non osservato / in ombra senza avviso / LIBERO; tracce fantasma mediana [min–max]; "
          "pannello «si muove»; soggetto «si muove» prima dell'ombra; continuità pulita (stessa identità, nessun "
          "«osservato» né riaggancio a soggetto nascosto); fusione; riagganci falsi; mai tracciato")
    for gname, ms in sorted(gruppi.items()):
        ms = [m for m in ms if m.get("esito_identita") != "mai nascosto"]
        if not ms:
            continue
        N = len(ms)
        es = [m["esito_identita"] for m in ms]
        st = {k: sum(m["stato_traccia_nascosto"][k] for m in ms) for k in ("previsto", "perso", "assente", "osservato", "altro")}
        cc = {k: sum(m["cella_centro_nascosto"][k] for m in ms) for k in ms[0]["cella_centro_nascosto"]}
        mot = {}
        for m in ms:
            for x in sorted(set(("più tracce pendenti" if x.endswith("tracce pendenti") else x) for x in m["motivi_ambigua"])):
                mot[x] = mot.get(x, 0) + 1
        fant = [m["tracce_fantasma"] for m in ms]
        ric = sum(1 for e in es if e in ("stessa", "diversa", "nessuna traccia dopo"))
        print(f"{gname}; {N}; {K.quota(es.count('stessa'), ric) if ric else '—'}; {es.count('diversa')}; "
              f"{es.count('nessuna traccia dopo')}; {es.count('nessuna traccia prima')}; {es.count('non ricompare')}; "
              f"{sum(1 for m in ms if m['eventi']['riaggancio'])}; {sum(1 for m in ms if m['eventi']['identita_ambigua'])} "
              f"{mot}; {sum(1 for m in ms if m['stato_traccia_nascosto']['osservato'])}; "
              f"{st['previsto']}/{st['perso']}/{st['assente']}/{st['osservato']}(+{st['altro']} altro); "
              f"{cc['possibile_presenza']}/{cc['occupato']}/{cc['non_osservato']}/{cc['in_ombra_senza_avviso']}/{cc['libero']}"
              f"(+{cc['fuori_griglia']} fuori griglia); {np.median(fant):.0f} [{min(fant)}–{max(fant)}]; "
              f"{sum(1 for m in ms if m['pannello_si_muove'])} su {N}; "
              f"{sum(1 for m in ms if m.get('soggetto_si_muove_prima'))} su {N}; CONTINUITÀ PULITA "
              f"{K.quota(sum(1 for m in ms if m.get('continuita_pulita')), ric) if ric else '—'}; fusione col pannello a "
              f"soggetto intero: {sum(1 for m in ms if m.get('fusione_fotogrammi_interi', 0) > 0)} su {N} passaggi; "
              f"riagganci a soggetto nascosto: {sum(1 for m in ms if m.get('riagganci_a_soggetto_nascosto', 0) > 0)} su {N} passaggi; "
              f"mai tracciato prima: {sum(1 for m in ms if m.get('id_prima') is None)}")
    print("\n== previsione durante l'occlusione: errore medio per fascia di tempo dal primo fotogramma nascosto "
          "(mediana fra i passaggi [N passaggi con dati]) ==")
    print("gruppo; metodo; " + "; ".join(NOMI_FASCE) + " (s)")
    for gname, ms in sorted(gruppi.items()):
        ms = [m for m in ms if "errore_per_fascia" in m]
        if not ms:
            continue
        for metodo in ("nucleo", "fermo", "retta"):
            celle = []
            for i in range(len(FASCE)):
                v = [m["errore_per_fascia"][metodo][i] for m in ms if m["errore_per_fascia"][metodo][i] is not None]
                celle.append(f"{np.median(v):.2f} [{len(v)}]" if v else "—")
            print(f"{gname}; {metodo}; " + "; ".join(celle))
    print("\n== regione dichiarata e ricomparsa ==")
    print("gruppo; N con previsioni; copertura 90 % (ellisse) mediana fra i passaggi; passaggi con copertura ≥ 0,85; "
          "copertura cerchio 95 % mediana; durata del «previsto» mediana (s); buio prima dell'ingresso mediana (s); "
          "riagganci: errore mediano (m), in90, in95; errore alla prima misura dopo: nucleo / fermo / retta (mediana, m)")
    for gname, ms in sorted(gruppi.items()):
        mp = [m for m in ms if m.get("previsioni")]
        if not mp:
            continue
        c90 = [m["copertura90"] for m in mp]
        c95 = [m["copertura95_cerchio"] for m in mp]
        pr = [m["previsto_s"] for m in ms if m.get("previsto_s") is not None]
        bu = [m["buio_prima_dell_ingresso_s"] for m in ms if "buio_prima_dell_ingresso_s" in m]
        ri = [m["riaggancio"] for m in ms if "riaggancio" in m]
        er = {k: [m["errore_alla_ricomparsa"][k] for m in ms if k in m.get("errore_alla_ricomparsa", {})]
              for k in ("nucleo", "fermo", "retta")}
        print(f"{gname}; {len(mp)}; {med(c90)}; {sum(1 for c in c90 if c >= 0.85)} su {len(c90)}; {med(c95)}; "
              f"{med(pr)} [{len(pr)}]; {med(bu)}; {med([r['errore_previsione_m'] for r in ri])} [{len(ri)}], "
              f"{sum(1 for r in ri if r['in90'])}, {sum(1 for r in ri if r['in95'])}; "
              f"{med(er['nucleo'])} [{len(er['nucleo'])}] / {med(er['fermo'])} [{len(er['fermo'])}] / "
              f"{med(er['retta'])} [{len(er['retta'])}]")
    print("\n== rumore del centro di una persona in moto (scarto tipo del centro misurato − verità sui fotogrammi "
          "interi prima dell'ombra, per passaggio; mediana) e scarto sistematico ==")
    for gname, ms in sorted(gruppi.items()):
        s = [m["sigma_centro_in_moto_m"] for m in ms if m.get("sigma_centro_in_moto_m")]
        o = [m["scarto_centro_m"] for m in ms if m.get("sigma_centro_in_moto_m")]
        if s:
            s, o = np.array(s), np.array(o)
            print(f"{gname}; N {len(s)}; sigma radiale {100 * np.median(s[:, 0]):.1f} cm (max {100 * s[:, 0].max():.1f}); "
                  f"trasversale {100 * np.median(s[:, 1]):.1f} cm (max {100 * s[:, 1].max():.1f}); scarto radiale "
                  f"{100 * np.median(o[:, 0]):.1f} cm; trasversale {100 * np.median(o[:, 1]):.1f} cm")


def main():
    et = sys.argv[1] if len(sys.argv) > 1 else "sim"
    radice = os.path.join(K.USCITE, et)
    nomi = sorted(n for n in os.listdir(radice) if os.path.isdir(os.path.join(radice, n))
                  and "__pannello_" in n and "vuoto" not in n)
    tutti = [misura(n, radice) for n in nomi]
    with open(os.path.join(radice, "misura_passaggi.json"), "w", encoding="utf-8") as f:
        json.dump(tutti, f, ensure_ascii=False, indent=1)
    riepilogo(tutti, radice)


if __name__ == "__main__":
    main()
