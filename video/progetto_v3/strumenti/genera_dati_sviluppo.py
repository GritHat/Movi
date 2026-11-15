#!/usr/bin/env python3
"""DATI DI SVILUPPO per il video di MoVi: registri FINTI nel formato di prototipo/movi/registro.py (modo «lungo»).

NON sono risultati. Servono solo a costruire e provare i componenti del video finché i registri veri del prototipo
non ci sono. Ogni file esce come  dati_sviluppo/<ID>.SVILUPPO.jsonl  e ogni riga porta
dichiarazioni.dati = "SVILUPPO_NON_RISULTATO": FasceOnesta, vedendolo, stampa «SCHEMATIC · DEV DATA · NOT A RESULT»
e il controllo di monta.py rifiuta il montaggio «finale» se un registro di sviluppo è ancora in uso.

Le traiettorie degli oggetti vengono da scenari_eventi.json (E1, E2, E3) o sono scritte qui (V1, piazzale). Stati,
regioni, sensori, volumi e nubi sono REGOLE GIOCATTOLO scritte qui per avere qualcosa da disegnare: non sono le
regole EV-A…EV-E e non ne imitano i numeri. Deterministico (nessun caso, seme fisso dove serve).

Uso:  python3 -I strumenti/genera_dati_sviluppo.py  [--scenari PERCORSO/scenari_eventi.json]
"""
import argparse, json, math, os, random

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(QUI)
FPS = 30
SCENARI_DEFAULT = os.path.join(RADICE, "..", "..", ".sciame", "20261114-1301-percezione-challenge", "f15-lunga-portata",
                               "40-eventi", "02-regole", "scenari_eventi.json")
DICH = {"dati": "SVILUPPO_NON_RISULTATO", "etichette": "a mano (finte)", "regole_accese": ["giocattolo_video"],
        "config": "sviluppo"}
CAMPI_PROPOSTI = ["sensori[].portata_utile_m", "volumi[]", "ritorni[]", "nubi[]", "avvisi_operatore[]",
                  "eventi[].indizi", "sistema[]", "meteo"]


def pos_su_polilinea(punti, v, t0, t):
    """Posizione lungo i segmenti di `punti` con velocità costante `v[i]` per segmento; ferma alla fine."""
    tt = max(0.0, t - t0)
    for i in range(len(punti) - 1):
        a, b = punti[i], punti[i + 1]
        L = math.dist(a[:2], b[:2]) if len(a) else 0
        L3 = math.dist(a, b)
        d = L3 / max(v[min(i, len(v) - 1)], 1e-6)
        if tt <= d:
            f = tt / d
            return [a[k] + f * (b[k] - a[k]) for k in range(len(a))]
        tt -= d
    return list(punti[-1])


def cerchio(c, r, livello="non_vista"):
    return {"tipo": "cerchio", "centro": [round(c[0], 2), round(c[1], 2)], "raggio_m": round(r, 2), "livello": livello}


def riga_base(i, t):
    return {"tipo": "fotogramma", "modo": "lungo", "indice": i, "t": round(t, 4), "dichiarazioni": DICH,
            "verita": {"oggetti": []}, "sensori": [], "affidabilita": "ok",
            "celle": {"griglia": "sito", "conteggi": {}}, "settori": [], "tracce": [], "avvisi": [], "eventi": [],
            "tabellone": None, "tempo_ciclo_ms": None}


def intest(id_, nome, sensori, ostacoli, aree, nota):
    return {"tipo": "intestazione", "formato": 1, "movi": "SVILUPPO", "modo": "lungo", "id_registro": id_,
            "scenario": nome, "configurazione": {"modo": "lungo", "scenario": nome, "sviluppo": True},
            "dichiarazioni": DICH, "principi": [], "riferimento": {"origine": "punto della scena", "assi": "x est, y nord"},
            "griglie": {}, "ostacoli": ostacoli, "aree": aree, "sensori": sensori, "campi_proposti": CAMPI_PROPOSTI,
            "nota": "DATI DI SVILUPPO GENERATI DA genera_dati_sviluppo.py: NON SONO RISULTATI. " + nota}


class Tracker:
    """Regola giocattolo: vista se visibile; altrimenti non_vista con cerchio che cresce a v_max·dt; oltre `t_ampio`
    previsto_ampio (regione = `ampia` o cerchio grande, nessun punto). Avviso di possibile presenza finché non si
    rivede. Alla ricomparsa: ricomparsa, identità presunta, per 2 s."""

    def __init__(self, id_, classe, vmax, t_ampio=2.5, ampia=None):
        self.id, self.classe, self.vmax, self.t_ampio, self.ampia = id_, classe, vmax, t_ampio, ampia
        self.ultimo, self.t_perso, self.t_ricomparsa, self.nato = None, None, None, False

    def passo(self, t, pos, visibile, sensori):
        tr = {"id": self.id, "classe": self.classe, "origine_etichetta": "a_mano", "identita": "certa",
              "non_vista_da_s": 0.0, "pos": None, "vel": None, "regione": None, "sensori": sensori}
        if visibile:
            if self.t_perso is not None:
                self.t_ricomparsa, self.t_perso = t, None
            self.ultimo = pos[:2]
            tr["pos"] = [round(pos[0], 2), round(pos[1], 2)]
            if self.t_ricomparsa is not None and t - self.t_ricomparsa < 2.0:
                tr["stato"], tr["identita"] = "ricomparsa", "presunta"
            else:
                tr["stato"] = "vista"
            return tr, None
        if self.ultimo is None:
            return None, None
        if self.t_perso is None:
            self.t_perso = t
        dt = t - self.t_perso
        tr["non_vista_da_s"] = round(dt, 3)
        tr["sensori"] = []
        if dt < self.t_ampio:
            tr["stato"] = "non_vista"
            tr["pos"] = [round(self.ultimo[0], 2), round(self.ultimo[1], 2)]
            tr["regione"] = cerchio(self.ultimo, 2 + self.vmax * dt)
        else:
            tr["stato"], tr["identita"] = "previsto_ampio", "presunta"
            tr["regione"] = self.ampia or cerchio(self.ultimo, 2 + self.vmax * dt, "previsto_ampio")
        avv = {"tipo": "possibile_presenza", "id_traccia": self.id, "eta_s": round(dt, 3), "forma": tr["regione"]}
        return tr, avv


def sensore(id_, tipo, salute="in_salute", causa="", portata=None):
    s = {"id": id_, "tipo": tipo, "salute": salute, "causa": causa, "validi": None, "eta_dato_s": 0.0}
    if portata:
        s["portata_utile_m"] = portata
    return s


def scrivi(id_, righe):
    p = os.path.join(RADICE, "dati_sviluppo", f"{id_}.SVILUPPO.jsonl")
    with open(p, "w", encoding="utf-8") as f:
        for r in righe:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        f.write(json.dumps({"tipo": "riassunto", "fotogrammi": len(righe) - 1, "SVILUPPO": True}) + "\n")
    print(f"{p}: {len(righe) - 1} fotogrammi")


# ---------------------------------------------------------------- R1: piazzale (scena 1)
def r1():
    hangar = [[40, 60], [100, 60], [100, 100], [40, 100]]
    sens = [{"id": "s_radar", "tipo": "radar", "pos": [0, 0, 10], "portata_m": 3000, "campo_gradi": [-180, 180]},
            {"id": "s_eo", "tipo": "eo", "pos": [5, 0, 12], "portata_m": 2000, "campo_gradi": [-60, 60]},
            {"id": "s_ir", "tipo": "ir", "pos": [5, 0, 12], "portata_m": 1500, "campo_gradi": [-60, 60]},
            {"id": "s_lidar", "tipo": "lidar", "pos": [-5, 0, 3], "portata_m": 250, "campo_gradi": [-60, 60]},
            {"id": "s_adsb", "tipo": "cooperativo", "pos": [0, -5, 5], "portata_m": 100000, "campo_gradi": [-180, 180]}]
    ombra = {"tipo": "poligono", "punti": [[40, 100], [100, 100], [130, 190], [52, 190]], "livello": "previsto_ampio"}
    h = intest("R1", "V1 piazzale (sviluppo)", sens,
               [{"id": "hangar", "punti": hangar, "genere": "hangar"}],
               [{"id": "piazzale", "poligono": [[-60, 20], [180, 20], [180, 190], [-60, 190]]}],
               "Hangar 60x40 m; drone2 passa dietro l'hangar fra t=5 e t=12.")
    dA, dB = Tracker("D1", "multirotore", 15), Tracker("D2", "multirotore", 15, 3.0, ombra)
    ac = Tracker("A1", "aereo_rullaggio", 15)
    righe = [h]
    for i in range(12 * FPS + 1):
        t = i / FPS
        r = riga_base(i, t)
        pA = [-30 + 4 * t, 140 + 3 * math.sin(t / 2), 30]
        pB = [10 + 6.5 * t, 120 if t < 4 else 120 + (t - 4) * 3.5, 25]
        pC = [150 - 3 * t, 40, 3]
        visB = not (t > 5.2)              # dietro l'hangar dal punto dei sensori (regola giocattolo)
        r["verita"]["oggetti"] = [
            {"id": "D1", "classe": "multirotore", "pos": [round(x, 2) for x in pA], "visibile": True},
            {"id": "D2", "classe": "multirotore", "pos": [round(x, 2) for x in pB], "visibile": visB},
            {"id": "A1", "classe": "aereo_rullaggio", "pos": [round(x, 2) for x in pC], "visibile": True}]
        r["sensori"] = [sensore(s["id"], s["tipo"]) for s in sens]
        r["zone_non_verificate"] = [{"forma": dict(ombra, livello="zona_non_verificata"), "causa": "ombra_hangar"}]
        for trk, p, v, ss in ((dA, pA, True, ["s_radar", "s_eo"]), (dB, pB, visB, ["s_radar", "s_eo"]),
                              (ac, pC, True, ["s_radar", "s_adsb"])):
            tr, av = trk.passo(t, p, v, ss)
            if tr:
                r["tracce"].append(tr)
            if av:
                r["avvisi"].append(av)
        righe.append(r)
    scrivi("R1", righe)


# ---------------------------------------------------------------- R3a/b/c: meteo e guasto (scena 4)
def r3(sc, variante):
    E3 = sc["E3"]
    sens = [{"id": s["id"], "tipo": {"radar_sorveglianza_droni": "radar", "camera_eo_ottica_lunga": "eo",
                                     "camera_termica_ottica_lunga": "ir", "ads_b": "cooperativo"}[s["tipo"]],
             "pos": s["pos"], "portata_m": {"s_radar": 5000, "s_eo": 4000, "s_ir": 3500, "s_adsb": 100000}[s["id"]],
             "campo_gradi": [-180, 180] if s["id"] in ("s_radar", "s_adsb") else [-150, -30]} for s in E3["sensori"]]
    oggetto = E3["oggetti"][1] if variante == "b" else E3["oggetti"][0]
    t0, t1 = {"a": (0, 40), "b": (0, 8), "c": (95, 125)}[variante]
    h = intest("R3" + variante, f"E3({variante}) (sviluppo)", sens, [], E3["aree"],
               "Portate utili GIOCATTOLO, non i conti di EV-D.")
    trk = Tracker(oggetto["id"], oggetto["classe"], oggetto["v_max"], 6.0)
    righe = [h]
    for i in range(int((t1 - t0) * FPS) + 1):
        t = t0 + i / FPS
        r = riga_base(i, t)
        p = pos_su_polilinea(oggetto["punti"], oggetto["v"], oggetto["t0"], t)
        guasto = variante == "c" and 100 <= t < 120
        meteo = "nebbia_fitta" if variante in "ac" else "pioggia_forte"
        f = min(1.0, (t - t0) / 3.0) if variante != "c" else 1.0
        pu_eo = 4000 - f * (4000 - (900 if meteo == "nebbia_fitta" else 2200))
        pu_ir = 3500 - f * (3500 - (1300 if meteo == "nebbia_fitta" else 2000))
        r["meteo"] = meteo
        r["sensori"] = [
            sensore("s_radar", "radar", "affidabilita_persa" if guasto else "in_salute",
                    "guasto simulato (iniettato)" if guasto else ""),
            sensore("s_eo", "eo", "degradato", meteo, {oggetto["classe"]: round(pu_eo)}),
            sensore("s_ir", "ir", "degradato", meteo, {oggetto["classe"]: round(pu_ir)}),
            sensore("s_adsb", "cooperativo", "in_salute", "nessun trasmettitore a bordo")]
        r["sistema"] = ["NO_REDUNDANCY"] if (variante == "c" or t - t0 > 2.5) else []
        if guasto:
            r["affidabilita"] = "persa"
            r["sistema"] = ["NO_REDUNDANCY", "WARNING_NOT_TIMELY:all"]
        elif variante == "b":
            r["sistema"].append("WARNING_NOT_TIMELY:multirotore")
        r["verita"]["oggetti"] = [{"id": oggetto["id"], "classe": oggetto["classe"],
                                   "pos": [round(x, 1) for x in p], "visibile": not guasto}]
        tr, av = trk.passo(t, p, not guasto, ["s_radar"])
        if tr:
            if guasto and tr["regione"]:
                tr["regione"] = {"tipo": "poligono", "livello": tr["stato"], "punti": tubo(oggetto, t, trk)}
            r["tracce"].append(tr)
        if av:
            av["forma"] = tr["regione"]
            r["avvisi"].append(av)
        righe.append(r)
    scrivi("R3" + variante, righe)


def tubo(o, t, trk):
    """Regione «a tubo» giocattolo lungo il sentiero, da dove si è perso fino a v_max·dt avanti."""
    a = trk.ultimo
    dt = t - trk.t_perso
    L = 2 + o["v_max"] * dt
    w = 30 + 3 * dt
    return [[a[0] - 20, a[1] - w], [a[0] + L, a[1] - w], [a[0] + L, a[1] + w], [a[0] - 20, a[1] + w]]


# ---------------------------------------------------------------- R1E: collisione fra droni (scena 5)
def r1e(sc):
    E1 = sc["E1"]
    sens = [{"id": s["id"], "tipo": {"radar_sorveglianza_droni": "radar", "camera_eo_ottica_lunga": "eo",
                                     "camera_termica_ottica_lunga": "ir"}[s["tipo"]], "pos": s["pos"],
             "portata_m": {"s_radar": 3000, "s_eo": 2000, "s_ir": 1500}[s["id"]],
             "campo_gradi": [-180, 180] if s["id"] == "s_radar" else [0, 90]} for s in E1["sensori"]]
    h = intest("R1E", "E1 (sviluppo)", sens, [], E1["aree"], "Volume e impronta GIOCATTOLO, non V(tau) di EV-A.")
    A, B, P = E1["oggetti"]
    tA, tB = Tracker("droneA", "multirotore", 19, 3.0), Tracker("droneB", "multirotore", 19, 3.0)
    rnd = random.Random(7)
    ritorni_fissi = [(rnd.uniform(-1, 1), rnd.uniform(-1, 1)) for _ in range(6)]
    righe = [h]
    t_a, t_ev = 13.65, 16.2
    for i in range(int(60 * FPS) + 1):
        t = i / FPS
        r = riga_base(i, t)
        pA = pos_su_polilinea(A["punti"], A["v"], 0, t)
        pB = pos_su_polilinea(B["punti"], B["v"], 0, min(t, 15.0))
        if t > 15.0:
            pB = [120 + 2 * (t - 15), 260 + 1 * (t - 15), max(0.0, 80 - 12.5 * (t - 15))]
        pP = pos_su_polilinea(P["punti"], P["v"], 0, t)
        r["verita"]["oggetti"] = [
            {"id": "droneA", "classe": "multirotore", "pos": [round(x, 1) for x in pA], "visibile": True},
            {"id": "droneB", "classe": "multirotore", "pos": [round(x, 1) for x in pB], "visibile": pB[2] > 5},
            {"id": "persona1", "classe": "persona_a_piedi", "pos": [round(x, 1) for x in pP], "visibile": True}]
        r["sensori"] = [sensore(s["id"], s["tipo"]) for s in sens]
        if t_a <= t < 15.0:   # tracce non risolte
            for tr_id, p in (("droneA", pA), ("droneB", pB)):
                r["tracce"].append({"id": tr_id, "classe": "multirotore", "origine_etichetta": "a_mano",
                                    "stato": "vista_in_parte", "identita": "ambigua", "non_vista_da_s": 0.0,
                                    "pos": [round(p[0], 1), round(p[1], 1)], "vel": None, "regione": None,
                                    "sensori": ["s_radar"]})
            if i == int(t_a * FPS) + 1:
                r["eventi"].append({"t": round(t, 3), "tipo": "identita_ambigua", "come_lo_so": "osservato",
                                    "traccia": "droneA", "settore": None})
        else:
            trA, avA = tA.passo(t, pA, True, ["s_radar"])
            if t >= t_ev:
                trA["stato"], trA["identita"], trA["pos"] = "previsto_ampio", "presunta", None
                trA["regione"] = cerchio(pA, 25 + 2 * (t - t_ev), "previsto_ampio")
            r["tracce"].append(trA)
            trB, avB = tB.passo(t, pB, pB[2] > 5 and t < 15.0, ["s_radar"])
            if trB:
                r["tracce"].append(trB)
                if avB:
                    r["avvisi"].append(avB)
        r["tracce"].append({"id": "persona1", "classe": "persona_a_piedi", "origine_etichetta": "a_mano",
                            "stato": "vista", "identita": "certa", "non_vista_da_s": 0.0,
                            "pos": [round(pP[0], 1), round(pP[1], 1)], "vel": None, "regione": None,
                            "sensori": ["s_eo"]})
        if t >= t_ev:
            tau = t - t_a
            raggio = min(15 + 9 * tau, 220)
            r["volumi"] = [{"evento": "contatto", "t_a": t_a, "tau": round(tau, 2),
                            "forma": cerchio([120 + 4 * tau, 260 + 2 * tau], raggio, "possibili_detriti"),
                            "quota_m": [0, 80], "raggi_passati_m": [round(min(15 + 9 * k, 220), 1)
                                                                    for k in range(1, int(tau))],
                            "impronta": cerchio([128 + 4 * tau, 264 + 2 * tau], min(10 + 7 * tau, 180),
                                                "impronta")}]
            if t < t_ev + 3:
                r["ritorni"] = [[round(120 + 4 * tau + 25 * a, 1), round(260 + 2 * tau + 25 * b, 1)]
                                for a, b in ritorni_fissi]
            r["avvisi"].append({"tipo": "possibile_presenza", "id_traccia": None, "eta_s": round(t - t_ev, 2),
                                "forma": r["volumi"][0]["impronta"], "motivo": "possibili_detriti"})
            r["avvisi_operatore"] = [{"codice": "PERSON_IN_FOOTPRINT", "traccia": "persona1"}]
            r["zone_non_verificate"] = [{"forma": r["volumi"][0]["impronta"], "causa": "possibili_detriti"}]
        if i == int(t_ev * FPS):
            r["eventi"].append({"t": round(t, 3), "tipo": "contatto", "come_lo_so": "dedotto", "traccia": "droneA",
                                "settore": None, "indizi": ["fusione_tracce", "nuovi_ritorni"]})
        righe.append(r)
    scrivi("R1E", righe)


# ---------------------------------------------------------------- R2E: avaria motore, fiammata, fumo (scena 6)
def r2e(sc):
    E2 = sc["E2"]
    tipo = {"radar_movimento_a_terra": "radar", "camera_eo_ottica_lunga": "eo", "camera_termica_ottica_lunga": "ir",
            "ads_b": "cooperativo"}
    sens = [{"id": s["id"], "tipo": tipo[s["tipo"]], "pos": s["pos"],
             "portata_m": {"s_smr": 5000, "s_eo": 4000, "s_ir": 3500, "s_adsb": 100000}[s["id"]],
             "campo_gradi": [-180, 180] if s["id"] in ("s_smr", "s_adsb") else [-130, -50]} for s in E2["sensori"]]
    h = intest("R2E", "E2 (sviluppo)", sens, [], E2["aree"], "Nube, cecità e detriti GIOCATTOLO.")
    ac, mz = E2["oggetti"]
    tA, tM = Tracker("aereo1", ac["classe"], 80), Tracker("mezzo1", mz["classe"], 14)
    righe = [h]
    for i in range(int(45 * FPS) + 1):
        t = i / FPS
        r = riga_base(i, t)
        pA = pos_su_polilinea(ac["punti"], ac["v"], 0, t)
        pM = pos_su_polilinea(mz["punti"], mz["v"], mz["t0"], t) if t >= mz["t0"] else None
        cieca_eo, cieca_ir = 15.7 <= t < 20.7, 15.7 <= t < 28.7
        r["verita"]["oggetti"] = [{"id": "aereo1", "classe": ac["classe"], "pos": [round(x, 1) for x in pA],
                                   "visibile": True}]
        if pM:
            r["verita"]["oggetti"].append({"id": "mezzo1", "classe": mz["classe"], "pos": [round(x, 1) for x in pM],
                                           "visibile": True})
        if 15.7 <= t < 18.7:
            r["verita"]["fiammata"] = {"pos": [600, 0], "raggio_m": 30, "schematica": True}
        r["sensori"] = [sensore("s_smr", "radar"),
                        sensore("s_eo", "eo", "affidabilita_persa" if cieca_eo else "in_salute",
                                "fiammata" if cieca_eo else ""),
                        sensore("s_ir", "ir", "affidabilita_persa" if cieca_ir else "in_salute",
                                "fiammata" if cieca_ir else ""),
                        sensore("s_adsb", "cooperativo")]
        trA, _ = tA.passo(t, pA, True, ["s_smr"] if cieca_eo else ["s_smr", "s_eo", "s_adsb"])
        r["tracce"].append(trA)
        if pM:
            trM, _ = tM.passo(t, pM, True, ["s_smr"])
            r["tracce"].append(trM)
        if t >= 16.0:
            rr = min(50, 20 + 1.0 * (t - 16))
            cx = min(pA[0], 1000)
            r["nubi"] = [{"id": "fumo1", "tipo": "fumo", "forma": cerchio([cx - 40, 8], rr, "nube"),
                          "opaca_per": ["eo", "ir"]}]
            r["volumi"] = [{"evento": "separazione", "t_a": 15.7, "tau": round(t - 15.7, 2),
                            "forma": {"tipo": "poligono", "livello": "possibili_detriti",
                                      "punti": [[600, -22], [min(600 + 30 * (t - 15.7), 1150), -40],
                                                [min(600 + 30 * (t - 15.7), 1150), 40], [600, 22]]},
                            "quota_m": [0, 10], "raggi_passati_m": [], "impronta": None}]
            r["zone_non_verificate"] = [{"forma": r["volumi"][0]["forma"], "causa": "possibili_detriti"}]
            r["avvisi_operatore"] = [{"codice": "UNVERIFIED_ZONE_ON_VEHICLE_PATH", "traccia": "mezzo1"}]
            if 16.5 <= t < 22:
                r["ritorni"] = [[round(640 + 37 * k, 1), round(-12 + 6 * (k % 4), 1)] for k in range(5)]
        if i == int(16.5 * FPS):
            r["eventi"].append({"t": round(t, 3), "tipo": "separazione", "come_lo_so": "dedotto", "traccia": "aereo1",
                                "settore": None, "indizi": ["nuovi_ritorni_dietro_aereo"]})
        righe.append(r)
    scrivi("R2E", righe)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenari", default=SCENARI_DEFAULT)
    a = ap.parse_args()
    sc = {s["id"]: s for s in json.load(open(a.scenari, encoding="utf-8"))["scenari"]}
    r1()
    for v in "abc":
        r3(sc, v)
    r1e(sc)
    r2e(sc)


if __name__ == "__main__":
    main()
