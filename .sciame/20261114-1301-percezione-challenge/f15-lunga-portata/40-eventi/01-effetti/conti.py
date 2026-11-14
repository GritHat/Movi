#!/usr/bin/env python3
"""Conti degli effetti di meteo, fumo, fiammata e detriti sui sensori simulati (MoVi, f15, 40-eventi/01-effetti).

Uso:  timeout 60 python3 -I conti.py        (scrive effetti_eventi.json e stampa i conti; solo libreria standard)

Tutto e' conto o simulazione: nessun sensore fisico. Solo osservazione, monitoraggio e avviso.
Stato delle fonti:  A = pagina aperta e letta oggi;  S = riassunto del motore di ricerca (fonte secondaria, pagina
non aperta);  I = ipotesi.  Il formato dei campi e' quello di 02-sensori: [valore, unita', fonte].
"""
import json
import math
import os

QUI = os.path.dirname(os.path.abspath(__file__))

FONTI = {
    "NADEEM": "A - Nadeem, Leitgeb, Radioengineering 19(2), 2010, eq. 1-3 (leggi di Kruse e di Kim), "
              "https://www.radioeng.cz/fulltexts/2010/10_02_223_227.pdf (aperta oggi, letta con pdftotext)",
    "ZHANG": "A - Zhang et al., Perception and Sensing for Autonomous Vehicles Under Adverse Weather Conditions: "
             "A Survey, https://arxiv.org/pdf/2112.08936 (aperta oggi, letta con pdftotext; rassegna: fonte "
             "secondaria rispetto alle misure che cita)",
    "P838": "A - ITU-R P.838-3 nei coefficienti riportati da itu-rpy, "
            "https://itu-rpy.readthedocs.io/en/latest/_modules/itur/models/itu838.html (aperta oggi; la "
            "raccomandazione ITU non e' stata aperta)",
    "P840": "S - ITU-R P.840-9, https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.840-9-202308-I!!PDF-E.pdf "
            "(riassunto di ricerca: acqua liquida 0.05 g/m3 a ~300 m di visibilita', 0.5 g/m3 a ~50 m)",
    "WOJT_S": "S - Wojtanowski et al. 2014, citato in ZHANG: a 25 mm/h il 905 nm arriva circa al doppio del 1550 nm",
    "ASW": "S - Flight Safety Foundation, AeroSafety World, 'Clean Sweep', "
           "https://flightsafety.org/asw-article/clean-sweep/ (riassunto di ricerca dei requisiti FAA AC "
           "150/5220-24; la circolare, https://www.faa.gov/documentLibrary/media/Advisory_Circular/150_5220_24.pdf, "
           "oggi risponde 403)",
    "FODRIC": "S - studi FOD a onde millimetriche, https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7916495/ e "
              "risultati vicini (riassunto di ricerca: sfera metallica di 50 mm a ~660 m a 93 GHz; sfera di 2 cm = "
              "-35 dBsm; cilindro da -20 dBsm fino a 35 m a 76.5 GHz)",
    "FAA_SUAS": "S - FAA Airport Technology R&D, FOD con piccoli droni, https://airporttech.tc.faa.gov/Products/"
                "Airport-Safety-Papers-Publications/Airport-Safety-Detail/small-unmanned-aircraft-based-foreign-"
                "object-debris-detection-on-airport-surfaces (riassunto di ricerca: 96 % di rilevamento)",
    "RCS_BLOG": "S - https://migflug.com/afterburner/why-radar-cannot-detect-small-drones-rcs-micro-doppler-birds/ "
                "(riassunto di ricerca, blog: Phantom 4 mediana 0.020 m2 a 9 GHz, da 0.004 a 0.27 secondo l'angolo)",
    "UDRI": "S - prova UDRI 2018, https://www.livescience.com/63828-drone-crashes-into-airplane.html (riassunto di "
            "ricerca: un quadricottero da 0.95 kg a 383 km/h contro un'ala 'non si e' frantumato')",
    "ASSURE": "S - ASSURE, UAS Ground Collision Severity, https://assure.msstate.edu/projects/"
              "uas-ground-collision-severity-evaluation-2/ (riassunto di ricerca: un multirotore cade piu' piano "
              "di un detrito metallico di pari massa)",
    "AC20128": "S - FAA AC 20-128A, https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-128A.pdf "
               "(riassunto di ricerca: 676 eventi non contenuti nella tabella storica; nessuna distribuzione dei "
               "frammenti trovata)",
    "LLNL83": "S - 'Electromagnetic Radiation Propagation in Large Fires' (1983), "
              "https://contrails.library.iit.edu/item/164237 (riassunto di ricerca: visibilita' a decine di piedi, "
              "attenuazione IR dell'ordine di 1 per km, radar molto meno)",
    "BOLO_S": "S - brevetti e articoli sui microbolometri (riassunto di ricerca: dinamica progettata fino a ~200 "
              "gradi; immagine ferma < 0.5 s al cambio di guadagno; impronta residua che decade)",
    "TELE15": "A (da 02-sensori) - Livox Tele-15, https://www.livoxtech.com/tele-15/specs",
    "IRIS": "A (da 02-sensori) - Robin Radar IRIS, scheda 04/2026",
    "P02": "parametri_lunga_portata.json di 02-sensori (stesso ruolo, stessa notte)",
}

# ------------------------------------------------------------------ leggi di propagazione

def q_kim(V_km):
    """Esponente di Kim (NADEEM eq. 3)."""
    if V_km > 50:
        return 1.6
    if V_km > 6:
        return 1.3
    if V_km > 1:
        return 0.16 * V_km + 0.34
    if V_km > 0.5:
        return V_km - 0.5
    return 0.0


def gamma_ottica_db_km(V_km, lam_nm, q=None):
    """Attenuazione specifica ottica in dB/km dalla visibilita' (NADEEM eq. 1): (17/V)*(lam/550)^-q, soglia 2 %."""
    if q is None:
        q = q_kim(V_km)
    return 10 * math.log10(1 / 0.02) / V_km * (lam_nm / 550.0) ** (-q)


_KH = ([(-5.33980, -0.10008, 1.13098), (-0.35351, 1.2697, 0.454), (-0.23789, 0.86036, 0.15354),
        (-0.94158, 0.64552, 0.16817)], -0.18961, 0.71147)
_AH = ([(-0.14318, 1.82442, -0.55187), (0.29591, 0.77564, 0.19822), (0.32177, 0.63773, 0.13164),
        (-5.37610, -0.96230, 1.47828), (16.1721, -3.29980, 3.4399)], 0.67849, -1.95537)


def p838(f_ghz):
    """k e alfa di ITU-R P.838-3, polarizzazione orizzontale (coefficienti da P838)."""
    x = math.log10(f_ghz)
    def somma(tab):
        righe, m, c = tab
        return sum(a * math.exp(-((x - b) / cc) ** 2) for a, b, cc in righe) + m * x + c
    return 10 ** somma(_KH), somma(_AH)


def gamma_pioggia_radar(f_ghz, R_mmh):
    k, a = p838(f_ghz)
    return k * R_mmh ** a


def gamma_pioggia_ottica(R_mmh):
    """IPOTESI (a memoria, non aperta oggi): Carbonneau, 1.076*R^0.67 dB/km, indipendente dalla lunghezza d'onda."""
    return 1.076 * R_mmh ** 0.67


# coefficiente di nebbia per il radar, (dB/km)/(g/m3): IPOTESI a memoria (P.840 da' la formula, non calcolata qui)
KL_NEBBIA = {3.0: 0.01, 9.4: 0.09, 77.0: 4.0}


def portata_attiva(R0_m, gamma_db_km, esponente):
    """Risolve R^n * 10^(2*gamma*R/10) = R0^n  (andata e ritorno): n=2 bersaglio esteso (LiDAR), n=4 puntiforme."""
    if gamma_db_km <= 0:
        return R0_m
    lo, hi = 0.0, R0_m
    for _ in range(80):
        mid = (lo + hi) / 2
        perdita_db = 2 * gamma_db_km * mid / 1000.0
        if esponente * 10 * math.log10(mid / R0_m) + perdita_db > 0:
            hi = mid
        else:
            lo = mid
    return lo


def portata_passiva(gamma_db_km, C0, Cth, tetto_m):
    """Camera: il contrasto cala come 10^(-gamma*R/10) (sola andata); visibile finche' C0*T >= Cth."""
    if gamma_db_km <= 0:
        return tetto_m
    return min(tetto_m, 1000.0 * 10 * math.log10(C0 / Cth) / gamma_db_km)


# ------------------------------------------------------------------ condizioni (nominale, prudente)

CONDIZIONI = {
    # V = visibilita' meteorologica (km), Rr = pioggia (mm/h), M = acqua liquida della nebbia (g/m3)
    "sereno":        {"nom": dict(V=20.0, Rr=0, M=0),    "pru": dict(V=10.0, Rr=0, M=0),    "fonte": "ipotesi"},
    "foschia":       {"nom": dict(V=4.0, Rr=0, M=0),     "pru": dict(V=2.0, Rr=0, M=0),     "fonte": "ipotesi"},
    "nebbia":        {"nom": dict(V=0.3, Rr=0, M=0.05),  "pru": dict(V=0.2, Rr=0, M=0.1),   "fonte": "P840 (0.05 g/m3 a ~300 m)"},
    "nebbia_fitta":  {"nom": dict(V=0.1, Rr=0, M=0.25),  "pru": dict(V=0.05, Rr=0, M=0.5),  "fonte": "P840 (0.5 g/m3 a ~50 m)"},
    "pioggia_forte": {"nom": dict(V=None, Rr=25, M=0),   "pru": dict(V=None, Rr=50, M=0),   "fonte": "ipotesi (25 mm/h forte, 50 mm/h violenta: ZHANG)"},
    "neve":          {"nom": dict(V=0.5, Rr=0, M=0, neve77=3.0), "pru": dict(V=0.1, Rr=0, M=0, neve77=6.0),
                      "fonte": "ZHANG: neve a 10 mm/h, visibilita' < 0.1 km, ~6 dB/km a 77 GHz; il nominale e' ipotesi"},
}

# sensori: nome come in 02-sensori; (tipo, parametri in aria limpida)
SENSORI = {
    "lidar_tele":                 dict(tipo="lidar", lam=905, R0=320.0, nota="Livox Tele-15, 320 m al 10 % (TELE15)"),
    "lidar_1550_ipotetico":       dict(tipo="lidar", lam=1550, R0=320.0, nota="stesso R0 per confronto: ipotesi"),
    "camera_eo_ottica_lunga":     dict(tipo="camera", lam=550, tetto=2000.0, nota="tetto: portata pratica drone 2 km (P02, ipotesi)"),
    "camera_termica_onda_media":  dict(tipo="camera", lam=4000, tetto=1200.0, nota="3-5 um: non e' in 02-sensori, ipotesi"),
    "camera_termica_ottica_lunga": dict(tipo="camera", lam=10000, tetto=1200.0, nota="8-14 um, tetto geometrico drone 1.2 km (P02)"),
    "radar_4d_auto":              dict(tipo="radar", f=77.0, R0=300.0, nota="77 GHz, 300 m (P02)"),
    "radar_sorveglianza_droni":   dict(tipo="radar", f=9.4, R0=3100.0, nota="banda X, 3100 m per 0.01 m2 (IRIS)"),
    "radar_banda_S_ipotetico":    dict(tipo="radar", f=3.0, R0=10000.0, nota="sorveglianza in banda bassa: R0 ipotesi"),
}
# soglie di contrasto delle camere: IPOTESI. EO: contrasto proprio del bersaglio e soglia (2 % Koschmieder, 5 % prudente)
CAM = {"nom": dict(C0=0.5, Cth=0.02), "pru": dict(C0=0.3, Cth=0.05)}
# termiche: trasmissione minima utile (segnale/NETD): IPOTESI
TERM = {"nom": 0.1, "pru": 0.3}


def gamma_per(sensore, cond, caso):
    """Attenuazione specifica (dB/km) del mezzo per un sensore in una condizione ('nom' o 'pru')."""
    p = CONDIZIONI[cond][caso]
    s = SENSORI[sensore]
    if s["tipo"] == "radar":
        g = gamma_pioggia_radar(s["f"], p["Rr"]) if p["Rr"] else 0.0
        g += KL_NEBBIA[s["f"]] * p["M"]
        if "neve77" in p:
            g += p["neve77"] * (s["f"] / 77.0) ** 2   # scalatura in f^2: ipotesi
        return g
    g = 0.0
    if p["V"]:
        # nominale: Kim (per il termico e' un'ESTRAPOLAZIONE fuori da 785-1550 nm: ipotesi); prudente: q = 0
        q = None if caso == "nom" else 0.0
        g += gamma_ottica_db_km(p["V"], s["lam"], q)
    if p["Rr"]:
        g += gamma_pioggia_ottica(p["Rr"]) * (2.0 if (s["lam"] == 1550 and caso == "pru") else 1.0)
    return g


def portata_in(sensore, cond, caso):
    s = SENSORI[sensore]
    g = gamma_per(sensore, cond, caso)
    if s["tipo"] == "lidar":
        return portata_attiva(s["R0"], g, 2), g
    if s["tipo"] == "radar":
        return portata_attiva(s["R0"], g, 4), g
    if s["lam"] == 550:
        return portata_passiva(g, CAM[caso]["C0"], CAM[caso]["Cth"], s["tetto"]), g
    return portata_passiva(g, 1.0, TERM[caso], s["tetto"]), g


# ------------------------------------------------------------------ falsi ritorni da pioggia (radar)

def clutter_pioggia_m2(f_ghz, R_mmh, dist_m, az_deg, el_deg, dR_m):
    """Sezione radar del volume di pioggia in una cella. IPOTESI da manuale (non aperta oggi):
    eta = pi^5 |K|^2 Z / lambda^4, Z = 200 R^1.6 mm6/m3 (Marshall-Palmer), |K|^2 = 0.93; valida in regime di
    Rayleigh (banda S e X, non 77 GHz)."""
    lam = 0.2998 / f_ghz
    Z = 200 * R_mmh ** 1.6 * 1e-18
    eta = math.pi ** 5 * 0.93 * Z / lam ** 4
    vol = math.pi / 4 * (dist_m * math.radians(az_deg)) * (dist_m * math.radians(el_deg)) * dR_m
    return eta * vol, eta, vol


# ------------------------------------------------------------------ fumo

def fumo(tau_vis, rapporti, caso):
    """tau = profondita' ottica nel visibile lungo la corda (sola andata). rapporti[lam] = tau(lam)/tau(vis)."""
    out = {}
    for nome, s in SENSORI.items():
        if s["tipo"] == "radar":
            out[nome] = dict(tau=0.0, trasmissione=1.0, fattore_portata=1.0, osservato_dietro=True)
            continue
        tau = tau_vis * rapporti[s["lam"]]
        if s["tipo"] == "lidar":
            T2 = math.exp(-2 * tau)
            f = math.sqrt(T2)
            out[nome] = dict(tau=round(tau, 2), trasmissione=T2, fattore_portata=f, osservato_dietro=f >= 0.5)
        elif s["lam"] == 550:
            T = math.exp(-tau)
            ok = CAM[caso]["C0"] * T >= CAM[caso]["Cth"]
            out[nome] = dict(tau=round(tau, 2), trasmissione=T, fattore_portata=None, osservato_dietro=ok)
        else:
            T = math.exp(-tau)
            out[nome] = dict(tau=round(tau, 2), trasmissione=T, fattore_portata=None, osservato_dietro=T >= TERM[caso])
    return out


# ------------------------------------------------------------------ detriti

def rcs_sfera(d_m):
    return math.pi * (d_m / 2) ** 2


def portata_radar_frammento(sigma, R_ref=3100.0, sigma_ref=0.01):
    return R_ref * (sigma / sigma_ref) ** 0.25


def portata_lidar_frammento(d_m, rho=0.1, R_ref=320.0, rho_ref=0.1, div_deg=(0.02, 0.12)):
    """Frammento quadrato di lato d; fascio del Tele-15 (TELE15). Sotto il fascio il ritorno cala come 1/R^4."""
    th = math.radians(div_deg[0]) * math.radians(div_deg[1])
    A = d_m * d_m
    R_est = R_ref * math.sqrt(rho / rho_ref)
    if A >= th * R_est ** 2:
        return R_est
    return (rho / rho_ref * A * R_ref ** 2 / th) ** 0.25


def portata_camera_frammento(d_m, ifov_urad, n_pixel=2):
    return d_m / (n_pixel * ifov_urad * 1e-6)


def v_terminale(m_kg, A_m2, Cd):
    return math.sqrt(2 * m_kg * 9.81 / (1.225 * Cd * A_m2))


def t_caduta(h_m, vt):
    """Caduta da fermo con resistenza quadratica: h = (vt^2/g) ln cosh(g t / vt)."""
    return vt / 9.81 * math.acosh(math.exp(h_m * 9.81 / vt ** 2))


# ------------------------------------------------------------------ esecuzione

def r(x, n=3):
    if x is None:
        return None
    if x == 0:
        return 0
    return float(f"{x:.{n}g}")


def main():
    P = print
    P("== 1. Controlli delle previsioni ==")
    k10, a10 = p838(10.0)
    P(f"P1  P.838-3 a 10 GHz (H): k={k10:.5f} (atteso 0.01217), alfa={a10:.4f} (atteso 1.2571)")
    g77 = gamma_pioggia_radar(77.0, 25)
    P(f"P2  77 GHz, 25 mm/h: {g77:.2f} dB/km (atteso 8-13)")
    gk = gamma_ottica_db_km(0.5, 905)
    P(f"P3  Kim, 905 nm, V=0.5 km: {gk:.1f} dB/km (atteso 32-36)")
    s2 = 10 * math.log10(rcs_sfera(0.02))
    P(f"P4  sfera di 2 cm: {s2:.1f} dBsm (atteso -36..-34)")

    P("\n== 2. Attenuazione specifica (dB/km, sola andata) ==")
    att = {}
    for f in (3.0, 9.4, 77.0):
        k, a = p838(f)
        att[f"radar_{f}_GHz"] = {"k": r(k, 4), "alfa": r(a, 4),
                                 "pioggia_4_25_50_mmh": [r(k * x ** a) for x in (4, 25, 50)],
                                 "nebbia_M_0.05_0.5": [r(KL_NEBBIA[f] * m) for m in (0.05, 0.5)]}
        P(f"radar {f:5.1f} GHz: k={k:.5f} alfa={a:.3f}  pioggia 4/25/50 mm/h = "
          + "/".join(f"{k * x ** a:.3f}" for x in (4, 25, 50))
          + f" ; nebbia 0.05/0.5 g/m3 = {KL_NEBBIA[f] * 0.05:.3f}/{KL_NEBBIA[f] * 0.5:.3f} (Kl ipotesi)")
    for lam in (550, 905, 1550, 4000, 10000):
        riga = [gamma_ottica_db_km(V, lam) for V in (10, 4, 1, 0.3, 0.05)]
        att[f"ottico_{lam}_nm_Kim_V_10_4_1_0.3_0.05_km"] = [r(x) for x in riga]
        P(f"ottico {lam:5d} nm (Kim), V=10/4/1/0.3/0.05 km: " + " / ".join(f"{x:.2f}" for x in riga))
    P("pioggia ottica (Carbonneau, ipotesi) 4/25/50 mm/h: "
      + " / ".join(f"{gamma_pioggia_ottica(x):.1f}" for x in (4, 25, 50)) + " dB/km")

    P("\n== 3. Portata nelle condizioni meteo: metri (frazione dell'aria limpida), nominale | prudente ==")
    meteo = {}
    for cond in CONDIZIONI:
        meteo[cond] = {"parametri": {"nominale": CONDIZIONI[cond]["nom"], "prudente": CONDIZIONI[cond]["pru"],
                                     "fonte": CONDIZIONI[cond]["fonte"]}, "per_sensore": {}}
        P(f"-- {cond}: nom {CONDIZIONI[cond]['nom']}  pru {CONDIZIONI[cond]['pru']}")
        for nome, s in SENSORI.items():
            base = s.get("R0", s.get("tetto"))
            Rn, gn = portata_in(nome, cond, "nom")
            Rp, gp = portata_in(nome, cond, "pru")
            meteo[cond]["per_sensore"][nome] = {
                "gamma_db_km": [[r(gn), r(gp)], "dB/km (nominale, prudente)", "conto"],
                "portata_m": [[round(Rn), round(Rp)], "m (nominale, prudente)", "conto"],
                "fattore_portata": [[r(Rn / base, 2), r(Rp / base, 2)], "frazione dell'aria limpida", "conto"],
            }
            P(f"   {nome:30s} gamma {gn:8.3f} | {gp:8.3f} dB/km   R {Rn:7.0f} ({Rn / base:4.2f}) | {Rp:7.0f} ({Rp / base:4.2f})")

    P("\n== 4. Falsi ritorni da pioggia, radar in banda X (formula da manuale: ipotesi) ==")
    cl = {}
    for Rr in (4, 25, 50):
        for d in (1000, 3000):
            sig, eta, vol = clutter_pioggia_m2(9.4, Rr, d, 1.0, 10.0, 3.0)
            cl[f"{Rr}_mmh_{d}_m"] = r(sig)
            P(f"   {Rr:2d} mm/h a {d} m: eta={eta:.2e} m2/m3, cella={vol:.0f} m3, pioggia={sig:.4f} m2 "
              f"({sig / 0.01:.1f} volte un multirotore da 0.01 m2)")

    P("\n== 5. Fumo: oggetto dietro una nube ==")
    rapp_nom = {550: 1.0, 905: 550 / 905, 1550: 550 / 1550, 4000: 550 / 4000, 10000: 550 / 10000}
    rapp_pru = {550: 1.0, 905: 1.0, 1550: 1.0, 4000: 0.5, 10000: 0.2}
    fumo_n = fumo(5.0, rapp_nom, "nom")
    fumo_p = fumo(10.0, rapp_pru, "pru")
    for nome in SENSORI:
        P(f"   {nome:30s} nom tau={fumo_n[nome]['tau']:5.2f} T={fumo_n[nome]['trasmissione']:.3g} "
          f"dietro={'osservato' if fumo_n[nome]['osservato_dietro'] else 'NON osservato'}"
          f" | pru tau={fumo_p[nome]['tau']:5.2f} T={fumo_p[nome]['trasmissione']:.3g} "
          f"dietro={'osservato' if fumo_p[nome]['osservato_dietro'] else 'NON osservato'}")

    P("\n== 6. Detriti: sezione radar e distanza di rilevamento ==")
    det = {}
    for d in (0.05, 0.10, 0.30):
        sm = rcs_sfera(d)
        sp = sm / 10
        det[f"{int(d * 100)}_cm"] = {
            "sezione_radar_m2": [[r(sm), r(sp)], "m2 (metallo: sfera ottica; plastica o carbonio: -10 dB, ipotesi)", "conto"],
            "radar_sorveglianza_droni_m": [[round(portata_radar_frammento(sm)), round(portata_radar_frammento(sp))],
                                           "m (nominale metallo, prudente -10 dB); Pd 0.5 (ipotesi di 02-sensori)", "conto"],
            "lidar_tele_m": [[round(portata_lidar_frammento(d, 0.1)), round(portata_lidar_frammento(d, 0.05))],
                             "m (riflettivita' 10 %, prudente 5 %)", "conto"],
            "camera_eo_ottica_lunga_m": [[round(portata_camera_frammento(d, 11.5, 2)), round(portata_camera_frammento(d, 11.5, 8))],
                                         "m (2 pixel: limite geometrico; prudente 8 pixel); solo se gia' puntata, di giorno", "conto"],
            "camera_termica_ottica_lunga_m": [[round(portata_camera_frammento(d, 120, 2)), 0],
                                              "m (2 pixel, se il frammento e' caldo; prudente: freddo, nessun contrasto)", "conto"],
        }
        v = det[f"{int(d * 100)}_cm"]
        P(f"   {d * 100:3.0f} cm: sigma {sm:.4f} m2 ({10 * math.log10(sm):.1f} dBsm) | -10 dB {sp:.5f}; "
          f"radar X {v['radar_sorveglianza_droni_m'][0]}; LiDAR tele {v['lidar_tele_m'][0]}; "
          f"EO {v['camera_eo_ottica_lunga_m'][0]}; termica {v['camera_termica_ottica_lunga_m'][0]}")

    P("\n== 7. Caduta dei detriti da 100 m (resistenza quadratica; masse, aree e Cd: ipotesi) ==")
    cad = {}
    for nome, m, A, Cd in (("corpo_drone_1kg", 1.0, 0.03, 1.0), ("batteria_0.25kg", 0.25, 0.006, 1.0),
                           ("braccio_con_motore_0.08kg", 0.08, 0.006, 1.0), ("frammento_elica_5g", 0.005, 0.002, 1.2)):
        vt = v_terminale(m, A, Cd)
        t = t_caduta(100.0, vt)
        cad[nome] = {"v_terminale_ms": r(vt), "t_caduta_da_100m_s": r(t), "deriva_vento_10ms_m": r(10 * t)}
        P(f"   {nome:28s} vt={vt:5.1f} m/s  t={t:5.1f} s  deriva con vento a 10 m/s: {10 * t:5.0f} m")

    # ------------------------------------------------------------ il file per il simulatore
    I = "ipotesi"
    effetti = {
        "_meta": {
            "titolo": "Effetti di meteo, fumo, fiammata e detriti sui sensori simulati (MoVi, f15, 40-eventi/01-effetti)",
            "data": "2026-11-15 (orologio della macchina)",
            "generato_da": "conti.py (timeout 60 python3 -I conti.py)",
            "avvertenza": "Tutto e' conto, scheda o ipotesi: nessun sensore fisico, niente e' validato.",
            "formato_campo": "[valore, unita', fonte]; dove il valore e' una coppia e' [nominale, prudente]. fonte = chiave di 'fonti', 'conto' o 'ipotesi'.",
            "stato_fonti": "A = pagina aperta e letta oggi; S = riassunto del motore di ricerca, pagina non aperta (fonte secondaria); ipotesi = nessuna fonte aperta",
            "nomi_sensori": "quelli di 02-sensori/parametri_lunga_portata.json, piu' tre ipotetici per confronto (lidar_1550_ipotetico, camera_termica_onda_media, radar_banda_S_ipotetico)",
            "principi": ["cio' che non e' osservato non e' mai 'libero'", "l'avviso non si toglie se non guardando",
                         "nessuna etichetta riduce un avviso",
                         "un effetto puo' solo TOGLIERE osservazione o accendere avvisi: mai dichiarare libero un volume"],
            "ambito": "Solo osservazione, monitoraggio e avviso. Nessuna funzione di ingaggio, puntamento o contrasto.",
            "uso_nel_simulatore": "meteo: moltiplica la portata del sensore per fattore_portata (o ricalcola con 'modelli'); fumo e fiammata: volumi e intervalli in cui le celle del sensore tornano 'non osservato'; fiammata: chiama affidabilita_persa(t, sensore) di movi_lp.py per la durata di cecita' e ripristina solo dopo aver riguardato; detriti: oggetti nuovi con sezione radar e dimensione, piu' un volume di 'possibile presenza'",
        },
        "fonti": FONTI,
        "modelli": {
            "ottico_visibilita": "gamma[dB/km] = (17/V[km]) * (lambda/550 nm)^(-q); q di Kim: 1.6 (V>50), 1.3 (6-50), 0.16V+0.34 (1-6), V-0.5 (0.5-1), 0 (V<0.5). Fonte NADEEM. Prudente: q = 0 sempre. Per 4 e 10 um e' un'estrapolazione (ipotesi).",
            "radar_pioggia": "gamma[dB/km] = k * R[mm/h]^alfa, k e alfa di ITU-R P.838-3 (P838), polarizzazione orizzontale",
            "radar_nebbia": "gamma = Kl * M; M da P840; Kl = 0.01 / 0.09 / 4 (dB/km)/(g/m3) a 3 / 9.4 / 77 GHz: ipotesi a memoria",
            "ottico_pioggia": "gamma = 1.076 * R^0.67 dB/km (Carbonneau): ipotesi a memoria, non aperta; prudente a 1550 nm: doppia (WOJT_S)",
            "portata_attiva": "R^n * 10^(2*gamma*R/10000) = R0^n con R in m; n = 2 LiDAR su bersaglio esteso, n = 4 radar e LiDAR su bersaglio piu' piccolo del fascio",
            "portata_camera": "R = 10*log10(C0/Cth)/gamma, col tetto della portata in aria limpida; EO: C0 0.5|0.3, Cth 0.02|0.05 (ipotesi); termica: trasmissione minima 0.1|0.3 (ipotesi)",
            "pioggia_falsi_ritorni_radar": "sigma = eta * volume della cella; eta = pi^5*0.93*Z/lambda^4, Z = 200 R^1.6 (Marshall-Palmer): ipotesi da manuale, solo banda S e X",
            "fumo": "trasmissione = exp(-tau) per le camere (sola andata), exp(-2 tau) per LiDAR; tau(lambda) = tau_vis * 550/lambda (fuliggine fine: ipotesi) | prudente: 1 fino a 1550 nm, 0.5 a 4 um, 0.2 a 10 um",
            "frammento_radar": "sigma = pi*(d/2)^2 (sfera metallica, regime ottico) | prudente -10 dB; R = 3100 m * (sigma/0.01)^(1/4) (IRIS, ipotesi di 02-sensori sul riferimento)",
            "frammento_lidar": "sotto il fascio: R = (rho/rho_ref * d^2 * R_ref^2 / (theta_h*theta_v))^(1/4), Tele-15: 320 m al 10 %, fascio 0.02 x 0.12 gradi (TELE15)",
            "frammento_camera": "R = d / (n * IFOV): n = 2 | 8 pixel; IFOV 11.5 urad (EO), 120 urad (termica) da 02-sensori",
        },
        "attenuazione_specifica": att,
        "effetti": {},
    }
    E = effetti["effetti"]
    for cond in CONDIZIONI:
        E["meteo_" + cond] = {"tipo": "meteo", **meteo[cond]}
    E["meteo_pioggia_forte"]["falsi_ritorni"] = {
        "radar_banda_X_pioggia_in_cella_m2": [cl, "m2 per cella (fascio 1 x 10 gradi e cella di 3 m: ipotesi)", "conto"],
        "cancellazione_doppler_db": [[25, 15], "dB (nominale, prudente)", I],
        "lidar_punti_falsi_frazione": [[0.001, 0.01], "frazione dei punti entro 30 m (gocce e spruzzi)", I],
        "nota": ["a 25 mm/h e 1 km la pioggia in cella vale alcune volte un multirotore piccolo: senza filtro Doppler il bersaglio e' sommerso; i 'fantasmi' da spruzzi sul LiDAR sono riportati da ZHANG", "", "ZHANG"],
    }
    E["meteo_nebbia"]["falsi_ritorni"] = {
        "lidar_ritorni_dalla_nebbia": [[0.01, 0.05], "frazione dei raggi con un falso ritorno vicino (< 20 m)", I],
        "nota": ["sotto 10 m di visibilita' il LiDAR e' bloccato quasi del tutto", "", "ZHANG"],
    }
    E["meteo_neve"]["falsi_ritorni"] = {
        "lidar_fiocchi": [[0.005, 0.03], "frazione dei punti (fiocchi come punti isolati, tolti con un filtro di vicinato)", I],
        "nota": ["i fiocchi causano falsi rilevamenti del LiDAR e bloccano la linea di vista", "", "ZHANG"],
    }
    E["fumo_nube"] = {
        "tipo": "evento: nube di fumo o polvere dopo un incendio o un'esplosione",
        "tau_visibile_lungo_la_corda": [[5.0, 10.0], "profondita' ottica, sola andata (nominale, prudente)", I],
        "rapporto_tau_per_lunghezza_d_onda": [{"nominale": {str(k): r(v) for k, v in rapp_nom.items()},
                                               "prudente": {str(k): v for k, v in rapp_pru.items()}}, "tau(lambda)/tau(550 nm)", I],
        "raggio_m": [{"due_multirotori_piccoli": [3, 10], "avaria_motore_aereo": [20, 50]}, "m (nominale, prudente)", I],
        "durata_s": [{"due_multirotori_piccoli": [20, 120], "avaria_motore_aereo": [60, 300]}, "s (nominale, prudente); con vento v la nube si sposta di v*t e si allunga", I],
        "scia_m": [{"avaria_motore_aereo": [300, 1000]}, "m di scia dietro il velivolo in volo", I],
        "evidenza": ["nei grandi incendi la visibilita' scende a decine di piedi; l'infrarosso e' attenuato dell'ordine di 1 per km, il radar molto meno", "", "LLNL83"],
        "per_sensore": {n: {"nominale": {k: (r(v) if isinstance(v, float) else v) for k, v in fumo_n[n].items()},
                            "prudente": {k: (r(v) if isinstance(v, float) else v) for k, v in fumo_p[n].items()},
                            "fonte": "conto su ipotesi"} for n in SENSORI},
        "regola": "il volume della nube e il cono d'ombra dietro di essa sono 'non osservato' per ogni sensore con osservato_dietro = false; il fronte della nube da' al LiDAR ritorni veri di 'qualcosa' (non un falso allarme: un volume opaco)",
    }
    E["fiammata_lampo"] = {
        "tipo": "evento impulsivo: fiammata, lampo, palla di fuoco",
        "durata_sorgente_s": [{"batteria_al_litio_di_un_drone": [2, 10], "fiammata_di_un_motore": [0.5, 3]}, "s (nominale, prudente)", I],
        "camera_eo_ottica_lunga": {
            "cecita_s": [[0.5, 2.0], "s oltre la durata della sorgente: tempo di rientro dell'esposizione automatica", I],
            "frazione_pixel_saturi": [[0.2, 1.0], "frazione del quadro (campo di 2.7 gradi: la fiammata lo riempie)", I],
            "alone_raggio_volte_sorgente": [[2, 5], "volte il raggio apparente della sorgente", I],
            "evidenza": ["una luce troppo forte porta la visibilita' di una camera quasi a zero; i riflessi rendono difficile la scelta dell'esposizione", "", "ZHANG"],
        },
        "camera_termica_ottica_lunga": {
            "cecita_s": [[1.0, 10.0], "s oltre la sorgente: saturazione, cambio di guadagno (immagine ferma < 0.5 s), impronta residua", "ipotesi (ordini di grandezza da BOLO_S)"],
            "saturazione": ["una fiamma supera la dinamica progettata (~200 gradi): pixel saturi nella regione calda; il resto del quadro resta leggibile se il guadagno non cambia", "", "BOLO_S"],
            "frazione_pixel_saturi": [[0.05, 0.5], "frazione del quadro", I],
        },
        "lidar_tele": {
            "cecita_s": [[0.0, 1.0], "s: solo finche' la sorgente e' nel campo", I],
            "effetto": ["area nera (nessun ritorno) attorno a una sorgente molto intensa: provato a 200 klx", "", "ZHANG"],
            "cono_cieco_deg": [[1, 5], "gradi attorno alla direzione della sorgente", I],
            "falsi_punti_frazione": [[0.0001, 0.001], "< 0.01 % a 100 klx di luce ambiente (TELE15); con la fiamma nel campo: ipotesi", "TELE15 / ipotesi"],
        },
        "radar": {
            "effetto": ["nessun effetto MODELLATO: non ho una fonte aperta ne' per l'assenza di effetto ne' per l'attenuazione da plasma di una fiamma; non verificato", "", "non verificato"],
            "cecita_s": [[0.0, 0.0], "s (nominale); prudente: da decidere con una fonte", I],
        },
        "ads_b_identificazione_remota": {
            "effetto": ["la radio non e' toccata dal lampo, ma il mezzo danneggiato puo' smettere di trasmettere: il silenzio non e' un'osservazione", "", "P02"],
        },
        "regola": "durante sorgente + cecita' il sensore dichiara affidabilita' persa (movi_lp.affidabilita_persa): tutte le sue celle tornano 'non osservato' e gli avvisi restano accesi; si ripristina solo quando le statistiche rientrano E il sensore ha riguardato",
    }
    E["salute_sensore"] = {
        "tipo": "come un sensore si accorge di essere accecato o degradato (statistiche d'immagine; soglie: ipotesi)",
        "camera_eo": {
            "pixel_saturi": [0.05, "frazione di pixel al fondo scala oltre la quale il quadro e' 'abbagliato'", I],
            "salto_media": [0.5, "variazione relativa del livello medio fra due quadri oltre la quale c'e' un 'lampo'", I],
            "contrasto_perso": [0.5, "caduta relativa dell'energia dei bordi (varianza del laplaciano) rispetto alla media mobile di 10 s: nebbia, fumo, lente bagnata", I],
            "quadri_buoni_per_rientrare": [10, "quadri consecutivi entro le soglie (1 s a 10 Hz)", I],
        },
        "camera_termica": {
            "pixel_saturi": [0.02, "frazione al fondo scala", I],
            "contrasto_perso": [0.5, "caduta relativa della deviazione standard della scena", I],
        },
        "lidar": {
            "caduta_ritorni": [0.3, "caduta relativa del numero di ritorni oltre 50 m rispetto alla media mobile", I],
            "ritorni_vicini": [0.02, "frazione dei raggi con ritorno sotto 20 m senza oggetto seguito: nebbia, pioggia, fumo", I],
        },
        "radar": {
            "rumore_di_fondo_db": [6, "dB di aumento del fondo (pioggia) oltre il quale la portata dichiarata si accorcia", I],
        },
        "regola": "la salute e' una misura del sensore su se' stesso: quando scatta, il sensore ACCORCIA la portata che dichiara (o la azzera); non allunga mai. Indipendenza: le soglie usano gli stessi dati che il sensore produce, quindi non vedono un guasto che lascia l'immagine plausibile",
    }
    E["detriti_in_volo"] = {
        "tipo": "evento: frammenti dopo una collisione fra due multirotori piccoli o dopo un'avaria di motore",
        "collisione_due_multirotori": {
            "corpi_principali": [[2, 2], "oggetti di ~30 cm che cadono quasi interi", "ipotesi (UDRI: il drone 'non si e' frantumato' nemmeno a 383 km/h)"],
            "frammenti_5_15_cm": [[8, 40], "numero: eliche, bracci, carrello, batteria, camera (2 droni x 4 eliche, 4 bracci...)", I],
            "frammenti_sotto_5_cm": [[20, 200], "numero: schegge di elica e di guscio: sotto la soglia di ogni sensore oltre ~100 m", I],
            "velocita_relativa_ms": [[10, 40], "m/s", I],
        },
        "avaria_motore": {
            "frammenti": [[10, 100], "numero di pezzi fra 5 e 50 cm (palette, pannelli della gondola)", "ipotesi (AC20128: 676 eventi non contenuti in tabella, nessuna distribuzione trovata)"],
            "angolo_di_dispersione_deg": [[15, 30], "gradi avanti e dietro il piano di rotazione (i valori di AC 20-128A non sono stati aperti)", I],
        },
        "rilevabilita": det,
        "caduta_da_100_m": {**cad, "fonte": "conto su ipotesi; ASSURE (S): un multirotore cade piu' piano di un detrito metallico di pari massa"},
        "sezione_radar_drone_intero_m2": [[0.02, 0.004], "m2 (mediana a 9 GHz, minimo secondo l'angolo)", "RCS_BLOG"],
        "regola": "al momento dell'evento le due tracce diventano un volume di 'possibile presenza' che cresce con (velocita' relativa + vento) * t e scende fino al suolo; i frammenti sotto soglia NON sono osservati: il volume resta in avviso finche' non lo si riguarda, e l'area a terra sotto di esso resta 'possibili detriti' fino all'ispezione",
    }
    E["detriti_a_terra_FOD"] = {
        "tipo": "detriti su pista o piazzale: sistemi esistenti e prestazioni DICHIARATE (non provate qui)",
        "requisito_faa": {
            "oggetto_minimo": [[3.0, 3.8], "cm (cilindro metallico non verniciato, alto 1.2 in, diametro 1.5 in)", "ASW"],
            "sfera": [4.3, "cm (bianca, grigia o nera, come una palla da golf, 1.7 in)", "ASW"],
            "oggetti_rilevati": ["almeno 9 su 10 del gruppo di prova (asfalto, pezzo di luce di pista, gomma di pneumatico, chiave da 20 cm, striscia metallica, dado di ruota...)", "", "ASW"],
            "accuratezza_posizione_m": [5, "m (16 piedi)", "ASW"],
            "falsi_allarmi_al_giorno": [[1, 3], "con conferma visiva, senza", "ASW"],
            "portata_radar_fisso_m": [1000, "m per il cilindro (radar fisso a onde millimetriche)", "ASW"],
        },
        "sistemi": {
            "radar_fisso_94_GHz_con_camera": ["Tarsier (QinetiQ): moduli a ~94 GHz piu' una camera per l'identificazione", "", "FODRIC"],
            "radar_mobile_su_veicolo": ["FOD Finder: la relazione FAA lo dice soddisfacente di notte, di giorno, con pioggia, foschia, nebbia e neve", "", "ASW"],
            "ibrido_radar_e_camera_sulle_luci_di_bordo": ["FODetect (Xsight)", "", "ipotesi (a memoria, non aperta)"],
            "solo_elettro_ottico": ["iFerret (Stratech)", "", "ipotesi (a memoria, non aperta)"],
            "piccolo_drone_con_camera": [0.96, "frazione rilevata degli oggetti della circolare", "FAA_SUAS"],
        },
        "ricerca": {
            "sfera_50_mm_a_93_GHz_m": [660, "m (prova in aeroporto)", "FODRIC"],
            "cilindro_-20_dBsm_a_76.5_GHz_m": [35, "m", "FODRIC"],
        },
        "con_i_sensori_di_02": {
            "radar_movimento_a_terra": ["cella di 3 m x 15 m a 3 km e soglia attorno a 1 m2: NON vede i detriti (02-sensori lo dichiara fra i non osservati)", "", "P02"],
            "lidar_tele_m": [[det["5_cm"]["lidar_tele_m"][0][0], det["5_cm"]["lidar_tele_m"][0][1]], "m per un frammento di 5 cm, ma a incidenza radente sulla pavimentazione la separazione dal suolo e' il limite vero", "conto / ipotesi"],
        },
        "regola": "dopo un evento sopra o vicino a una pista, la striscia sotto il volume di caduta resta 'possibili detriti' finche' un sensore capace (radar a onde millimetriche, camera, ispezione) non l'ha guardata: il radar del movimento a terra non basta a toglierlo",
    }
    stato = lambda fn, fp: "osservato" if fp >= 0.8 else ("degradato" if fn >= 0.3 else ("degradato (solo nominale)" if fn > 0.1 else "non osservato"))
    matrice = {}
    for nome in SENSORI:
        matrice[nome] = {}
        for cond in CONDIZIONI:
            fn, fp = meteo[cond]["per_sensore"][nome]["fattore_portata"][0]
            matrice[nome][cond] = {"fattore_portata": [fn, fp],
                                   "stato_oltre_la_portata_ridotta": "non osservato",
                                   "stato_sintetico": stato(fn, fp)}
        matrice[nome]["fumo_dietro_la_nube"] = ("osservato" if fumo_p[nome]["osservato_dietro"] else
                                                ("osservato solo nel caso nominale" if fumo_n[nome]["osservato_dietro"] else "non osservato"))
    for n in ("camera_eo_ottica_lunga", "camera_termica_ottica_lunga", "camera_termica_onda_media"):
        matrice[n]["fiammata"] = "non osservato per sorgente + cecita' (affidabilita' persa)"
    for n in ("lidar_tele", "lidar_1550_ipotetico"):
        matrice[n]["fiammata"] = "non osservato nel cono attorno alla sorgente; il resto osservato"
    for n in ("radar_4d_auto", "radar_sorveglianza_droni", "radar_banda_S_ipotetico"):
        matrice[n]["fiammata"] = "osservato (nessun effetto modellato: non verificato)"
    matrice["ads_b / identificazione_remota"] = {
        "meteo": "invariato (solo chi trasmette)", "fumo_dietro_la_nube": "invariato", "fiammata": "invariato",
        "dopo_un_danno": "il trasmettitore puo' tacere: nessuna osservazione, l'avviso resta", "fonte": "P02; ZHANG per la banda L in pioggia"}
    effetti["matrice_osservato_non_osservato"] = matrice
    effetti["combinazioni_che_reggono"] = {
        "nebbia_e_nebbia_fitta": "radar (X o S) per esistenza, distanza e velocita' radiale; cooperativi per l'identita'. Camere e LiDAR: solo entro poche decine o centinaia di metri. Nessuna classificazione visiva.",
        "pioggia_forte": "radar in banda S o X con filtro Doppler (portata X ridotta, vedi fattore); camere a portata ridotta; 77 GHz solo vicino.",
        "neve": "radar X o S; termica a corto raggio; LiDAR con filtro dei fiocchi.",
        "fumo": "radar attraverso la nube; termica a onda lunga nel caso nominale (non nel prudente); EO e LiDAR vedono solo il fronte della nube.",
        "fiammata": "radar (non verificato) e cooperativi durante la cecita'; LiDAR fuori dal cono della sorgente; camere dopo il rientro.",
        "detriti_in_volo": "radar per i pezzi >= 5-10 cm entro 1-2 km, per i pochi secondi di caduta; camera EO puntata dal radar per confermare; sotto 5 cm niente: resta il volume d'avviso.",
        "detriti_a_terra": "radar a onde millimetriche dedicato o camera/ispezione: nessuno dei sensori a lunga portata di 02-sensori basta.",
        "sintesi": "nessun sensore regge in tutte le condizioni; radar + una camera (EO o termica) + cooperativi lascia almeno 'esistenza e posizione' in ogni evento, ma l'identita' e i frammenti piccoli si perdono: li' il sistema deve dire 'non osservato'.",
    }
    with open(os.path.join(QUI, "effetti_eventi.json"), "w", encoding="utf-8") as f:
        json.dump(effetti, f, ensure_ascii=False, indent=1)
    n_campi = n_ip = 0
    def conta(o):
        nonlocal n_campi, n_ip
        if isinstance(o, dict):
            for v in o.values():
                conta(v)
        elif isinstance(o, list) and len(o) == 3 and isinstance(o[2], str) and isinstance(o[1], str):
            n_campi += 1
            if "ipotesi" in o[2] or "non verificato" in o[2]:
                n_ip += 1
    conta(effetti["effetti"])
    P(f"\n== 8. File scritto: effetti_eventi.json; {len(E)} effetti; campi [valore, unita', fonte]: {n_campi}, "
      f"di cui ipotesi o non verificati: {n_ip}, conti: vedi sopra ==")


if __name__ == "__main__":
    main()
