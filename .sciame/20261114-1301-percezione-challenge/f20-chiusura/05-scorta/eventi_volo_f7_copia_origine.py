"""eventi_volo.py - estensioni per il VOLO del simulatore degli eventi (f19-volo/04-scenari, scenari F1-F6).

Si appoggia a ../../f15-lunga-portata/10-simulatore/eventi_lp.py e sim_lp.py SENZA modificarli (li importa soltanto).
Aggiunge:
  1. frammenti_volo(): frammenti con velocita' iniziale del mezzo (vc = velocita' dell'aereo o dei droni) piu' u, |u| <= dv;
  2. nube in quota: cilindro fra z_base e z_top, con deriva in 3D e crescita (sim_lp conosce solo nubi dal suolo);
  3. perdita totale degli ottici: finestre di cecita' per TUTTI i sensori di tipo camera (lampo + nube);
  4. SensoreVolo: sottoclasse di sim_lp.SensoreSim che applica 2 e 3 (visibile() e guasto() sovrascritti);
  5. la confidenza nel tempo durante la perdita di continuita', in forma chiusa (modello gaussiano a rumore bianco di
     accelerazione), con il controllo Monte Carlo, e la probabilita' di scambio d'identita' di due tracce;
  6. --prova: frammenti in volo (F3, F4) contro il volume dichiarato V(tau) di frammenti.py.

Uso:  python -I -B eventi_volo.py --conti   (curve di confidenza e controllo Monte Carlo; scrive conti_volo.json)
      python -I -B eventi_volo.py --prova N (frammenti F3/F4 dentro V; scrive prova_frammenti_volo.json)
Tutto e' SIMULAZIONE o CONTO: nessun dato di un sensore fisico. Solo osservazione, monitoraggio e avviso.
Stesso autore degli scenari: il controllo non e' indipendente dalla specifica (vale solo per errori di codice).
"""
import json
import math
import os
import sys

sys.dont_write_bytecode = True
QUI = os.path.dirname(os.path.abspath(__file__))
F15 = os.path.normpath(os.path.join(QUI, "..", "..", "f15-lunga-portata"))
sys.path.insert(0, os.path.join(F15, "10-simulatore"))
import numpy as np  # noqa: E402

import eventi_lp as EL  # noqa: E402  (carica regole e scenari E1-E5 in sola lettura; main() NON viene chiamato)
import sim_lp as S  # noqa: E402

FR = EL.FR
G = 9.81
SC = json.load(open(os.path.join(QUI, "scenari_volo.json"), encoding="utf-8"))


# ------------------------------------------------------------------ 1. frammenti con la velocita' del mezzo
def frammenti_volo_euler(ev, rng, dt=0.05):
    """PRIMA VERSIONE (tenuta per traccia): riusa eventi_lp.frammenti (Euler esplicito). INSTABILE in volo: con
    |v| = 195 m/s e v_t = 6 m/s il passo k|v|dt = g|v|dt/v_t^2 vale circa 2,6 > 2 e il frammento 'esplode' a centinaia
    di km (trovato il 15-11 alle 04:45 sui campioni fuori da V di F4). Va bene a terra (E1, E2: |v| piccole)."""
    return EL.frammenti(dict(ev, vc=list(ev["vc"])), rng, dt)


def frammenti_volo(ev, rng, dt=0.05, t_max=90.0):
    """ev: p [x,y,z], vc [vx,vy,vz] del mezzo (o media delle due tracce), n_frammenti, v_t_m_s [min,max], dv_max_m_s,
    vento. Stessa fisica e stesse estrazioni casuali di eventi_lp.frammenti (resistenza quadratica, vento costante, fermo
    a terra), ma resistenza SEMI-IMPLICITA: v' = (v + g dt + k|v_a| w dt) / (1 + k|v_a| dt), k = g / v_t^2, stabile per
    ogni passo (il fattore 1/(1+x) non cambia segno). t_max 90 s: un frammento da 600 m con v_t 5 m/s cade in ~120 s;
    quelli ancora in aria a t_max restano in aria (limite dichiarato)."""
    p0 = np.asarray(ev["p"], float)
    vc = np.asarray(ev["vc"], float)
    w = np.asarray(ev.get("vento", [0, 0, 0]), float)
    gv = np.array([0.0, 0.0, -G])
    out = []
    for _ in range(ev["n_frammenti"]):
        u = rng.standard_normal(3)
        u = u / np.linalg.norm(u) * ev["dv_max_m_s"] * rng.random() ** (1 / 3)
        vt = math.exp(rng.uniform(math.log(ev["v_t_m_s"][0]), math.log(ev["v_t_m_s"][1])))
        k = G / vt ** 2
        p, v, T, P, t = p0.copy(), vc + u, [0.0], [p0.copy()], 0.0
        while t < t_max - 1e-9:
            if p[2] <= 0:
                p[2], v = 0.0, np.zeros(3)
            else:
                kv = k * np.linalg.norm(v - w) * dt
                v = (v + gv * dt + kv * w) / (1 + kv)
                p = p + v * dt
                if p[2] <= 0:
                    p[2], v = 0.0, np.zeros(3)
            t += dt
            T.append(t)
            P.append(p.copy())
        out.append((np.array(T), np.array(P), vt, float(np.linalg.norm(u))))
    return out


# ------------------------------------------------------------------ 2. nube in quota
def nube_quota_al_tempo(n, t):
    """n: {centro[x,y,z_centro], raggio_m, crescita_m_s, raggio_max_m, spessore_m, crescita_z_m_s, deriva[3], t_ini, t_fine}.
    Ritorna (c_xy, r, z_base, z_top) o None."""
    if t < n["t_ini"] or t > n["t_fine"]:
        return None
    dt = t - n["t_ini"]
    c = np.asarray(n["centro"], float) + np.asarray(n.get("deriva", [0, 0, 0]), float) * dt
    r = min(n["raggio_m"] + n.get("crescita_m_s", 0.0) * dt, n.get("raggio_max_m", 1e9))
    h = min(n["spessore_m"] + n.get("crescita_z_m_s", 0.0) * dt, n.get("spessore_max_m", 1e9))
    return c[:2], r, c[2] - h / 2, c[2] + h / 2


def segmento_in_cilindro(ps, p, c, r, z0, z1, n=96):
    """True se il segmento ps-p attraversa il cilindro (campionato in n punti: errore di passo <= |p-ps|/n)."""
    s = np.linspace(0.0, 1.0, n)[:, None]
    q = np.asarray(ps, float) + s * (np.asarray(p, float) - np.asarray(ps, float))
    d = np.hypot(q[:, 0] - c[0], q[:, 1] - c[1])
    return bool(np.any((d <= r) & (q[:, 2] >= z0) & (q[:, 2] <= z1)))


# ------------------------------------------------------------------ 3. perdita totale degli ottici
def finestre_cecita(eventi, tipo_sensore):
    """Dagli eventi 'perdita_ottici_totale' e 'fiammata' dello scenario: [(t_ini, t_fine, 'abbagliamento')] per le camere."""
    out = []
    for e in eventi:
        p = e["parametri"]
        if e["tipo"] == "perdita_ottici_totale" and tipo_sensore.startswith("camera"):
            out.append((e["t"], e["t"] + p["durata_s"], "abbagliamento"))
        if e["tipo"] == "fiammata":
            fino = p.get("cieca_eo_fino_a_t") if "eo" in tipo_sensore else p.get("cieca_termica_fino_a_t")
            if fino is not None and tipo_sensore.startswith("camera"):
                out.append((e["t"], fino, "abbagliamento"))
    return out


class SensoreVolo(S.SensoreSim):
    """Come SensoreSim, piu' nubi in quota (opache per i tipi indicati) e finestre di cecita' degli ottici."""

    def __init__(self, nome, pos, par, tipo_scheda, nubi_quota=(), cecita=(), **kw):
        kw["salute"] = list(kw.get("salute") or []) + list(cecita)
        super().__init__(nome, pos, par, **kw)
        self.tipo_scheda, self.nubi_quota = tipo_scheda, list(nubi_quota)

    def visibile(self, p, t):
        if not super().visibile(p, t):
            return False
        for n in self.nubi_quota:
            if self.tipo_scheda not in n["opaca_per"]:
                continue
            x = nube_quota_al_tempo(n, t)
            if x is not None and segmento_in_cilindro(self.pos, p, *x):
                return False
        return True


# ------------------------------------------------------------------ 5. confidenza nel tempo
def sigma2(tau, s0, sv0, q):
    """Varianza per asse dell'errore di posizione predetto a tau dall'ultima osservazione:
    s0^2 + sv0^2 tau^2 + q tau^3 / 3 (moto a velocita' costante con rumore bianco d'accelerazione di densita' q,
    stato iniziale con errori di posizione e velocita' indipendenti). Esatta per quel modello."""
    return s0 * s0 + sv0 * sv0 * tau * tau + q * tau ** 3 / 3.0


def chi2_3_cdf(x):
    """CDF della chi quadro a 3 gradi: erf(sqrt(x/2)) - sqrt(2x/pi) exp(-x/2) (forma chiusa)."""
    if x <= 0:
        return 0.0
    return math.erf(math.sqrt(x / 2)) - math.sqrt(2 * x / math.pi) * math.exp(-x / 2)


def confidenza(tau, g, s0, sv0, q):
    """C(tau) = P(|errore| <= g) = F_chi2_3(g^2 / sigma^2(tau)): confidenza che l'oggetto sia nella porta di raggio g."""
    return chi2_3_cdf(g * g / sigma2(tau, s0, sv0, q))


K99 = 3.3682    # sqrt(chi2_3 quantile 0,99) = sqrt(11,345)


def raggio_conf(tau, s0, sv0, q, k=K99):
    """Raggio della sfera che contiene l'oggetto con probabilita' 0,99 (modello gaussiano)."""
    return k * math.sqrt(sigma2(tau, s0, sv0, q))


def raggio_inviluppo(tau, r0, dv, a_max):
    """Zona garantita (non probabilistica): |e| <= r0 + dv tau + a_max tau^2 / 2 se |a| <= a_max e |e_v0| <= dv."""
    return r0 + dv * tau + 0.5 * a_max * tau * tau


def p_scambio(d, s_rel):
    """Probabilita' di scambio di due tracce alla riacquisizione con assegnazione a costo minimo (somma dei quadrati):
    Phi(-d / (sqrt(2) s)), d distanza fra le due posizioni vere, s = sigma per asse di ciascuna predizione
    (errori indipendenti, isotropi). Derivazione: lo scambio vince se d.(e_b - e_a) > |d|^2, e d.(e_b-e_a)/|d| ~ N(0, 2 s^2)."""
    return 0.5 * math.erfc(d / (math.sqrt(2) * s_rel) / math.sqrt(2))


def montecarlo_conf(taus, g, s0, sv0, q, n=200000, dt=0.005, seme=20261115):
    rng = np.random.default_rng(seme)
    e = rng.standard_normal((n, 3)) * s0
    v = rng.standard_normal((n, 3)) * sv0
    out, t, k = {}, 0.0, 0
    taus = sorted(taus)
    for tau in taus:
        while t < tau - 1e-12:
            # passo esatto del modello discreto equivalente: incremento integrato di velocita' e posizione
            a = rng.standard_normal((n, 3))
            b = rng.standard_normal((n, 3))
            dvv = math.sqrt(q * dt) * a
            dpp = math.sqrt(q * dt ** 3 / 12) * b + 0.5 * dt * dvv     # covarianza esatta [dt^3/3, dt^2/2; dt^2/2, dt] q
            e = e + v * dt + dpp
            v = v + dvv
            t += dt
            k += 1
        out[tau] = float(np.mean(np.einsum("ij,ij->i", e, e) <= g * g))
    return out


def conti():
    cf = SC["confidenza"]
    res = {"avvertenza": "CONTO e controllo Monte Carlo dello stesso modello (non indipendente dal modello)", "casi": {}}
    for nome, p in cf["casi"].items():
        taus = [0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 8.0, 10.0]
        mc = montecarlo_conf([t for t in taus if t <= 5.0], p["g_m"], p["s0_m"], p["sv0_m_s"], p["q_m2_s3"])
        righe = []
        for t in taus:
            c = confidenza(t, p["g_m"], p["s0_m"], p["sv0_m_s"], p["q_m2_s3"])
            righe.append({"tau_s": t, "C_forma_chiusa": round(c, 4), "C_montecarlo": None if t not in mc else round(mc[t], 4),
                          "r99_m": round(raggio_conf(t, p["s0_m"], p["sv0_m_s"], p["q_m2_s3"]), 1),
                          "r_inviluppo_m": round(raggio_inviluppo(t, p["r0_inv_m"], p["dv_inv_m_s"], p["a_max_m_s2"]), 1)})
        sc = [abs(r["C_forma_chiusa"] - r["C_montecarlo"]) for r in righe if r["C_montecarlo"] is not None]
        # tempo in cui C scende sotto 0,9 e sotto 0,5 (bisezione sulla forma chiusa)
        def t_sotto(lv):
            a, b = 0.0, 60.0
            if confidenza(b, p["g_m"], p["s0_m"], p["sv0_m_s"], p["q_m2_s3"]) > lv:
                return None
            for _ in range(60):
                mm = (a + b) / 2
                a, b = (mm, b) if confidenza(mm, p["g_m"], p["s0_m"], p["sv0_m_s"], p["q_m2_s3"]) > lv else (a, mm)
            return round(b, 3)
        res["casi"][nome] = {"parametri": p, "tabella": righe, "scarto_max_mc": round(max(sc), 4),
                             "t_C_0_9_s": t_sotto(0.9), "t_C_0_5_s": t_sotto(0.5)}
    # F5: scambio d'identita' alla riacquisizione dopo T s di cecita' (solo radar resta: qui il caso "radar perso")
    f5 = cf["scambio_F5"]
    tab = []
    for T in f5["durate_s"]:
        for d in f5["distanze_m"]:
            s_pred = math.sqrt(sigma2(T, f5["s0_m"], f5["sv0_m_s"], f5["q_m2_s3"]) + f5["sigma_mis_m"] ** 2)
            tab.append({"T_s": T, "d_m": d, "sigma_m": round(s_pred, 2), "p_scambio": round(p_scambio(d, s_pred), 4),
                        "confidenza_identita": round(1 - p_scambio(d, s_pred), 4)})
    # controllo Monte Carlo di p_scambio (un caso)
    rng = np.random.default_rng(7)
    s, d = 10.0, 15.0
    a, b = np.array([0, 0, 0.0]), np.array([d, 0, 0.0])
    ea, eb = rng.standard_normal((400000, 3)) * s, rng.standard_normal((400000, 3)) * s
    giusto = np.sum((ea) ** 2, 1) + np.sum((eb) ** 2, 1)
    scamb = np.sum((a - (b + eb)) ** 2, 1) + np.sum((b - (a + ea)) ** 2, 1)
    res["scambio_F5"] = {"parametri": f5, "tabella": tab,
                         "controllo_mc": {"s": s, "d": d, "forma_chiusa": round(p_scambio(d, s), 4), "mc": round(float(np.mean(scamb < giusto)), 4), "n": 400000}}
    return res


# ------------------------------------------------------------------ 6. frammenti in volo contro V(tau)
def prova(n_pass=10):
    out = {}
    for sid in ("F3", "F4"):
        sc = next(s for s in SC["scenari"] if s["id"] == sid)
        e = next(x for x in sc["eventi"] if x["tipo"] in ("collisione", "avaria_motore"))
        pe = e["parametri"]
        par = dict(EL.INV[pe["inviluppo"]]["prudente"], k_tc=EL.FRAM["k_tc"], r_rimbalzo=EL.FRAM["r_rimbalzo_m"])
        ev_decl = {"p0": pe["p"], "vc": pe["vc_tracce"], "r0": pe["r0_m"]}
        dentro, tot, a_terra_fuori, n_fr, cadute, fr_ok = 0, 0, 0, 0, [], 0
        R_imp, vt_imp = FR.impronta(ev_decl, par)
        for i in range(n_pass):
            rng = np.random.default_rng(np.random.SeedSequence(20261115, spawn_key=(300 + int(sid[1]), i)))
            frs = frammenti_volo({"p": pe["p"], "vc": pe["vc_medio"], "n_frammenti": pe["n_frammenti"], "v_t_m_s": pe["v_t_m_s"],
                                  "dv_max_m_s": pe["dv_max_m_s"], "vento": pe["vento"]}, rng)
            for (T, P, vt, un) in frs:
                n_fr += 1
                d0 = dentro
                ia = np.argmax(P[:, 2] <= 0) if np.any(P[:, 2] <= 0) else None
                if ia is not None:
                    cadute.append(float(T[ia]))
                    if math.hypot(P[ia, 0] - pe["p"][0], P[ia, 1] - pe["p"][1]) > R_imp:
                        a_terra_fuori += 1
                for j in range(0, len(T), 10):            # ogni 0,5 s
                    tau = T[j]
                    r, tq, zmin, zmax, Tc = FR.inviluppo(tau, ev_decl, par)
                    p = P[j]
                    tot += 1
                    dentro += int(FR.dentro_pianta(p[0], p[1], tau, ev_decl, par) <= 1e-9 and zmin - 1e-6 <= p[2] <= zmax + 1e-6)
                fr_ok += int(dentro - d0 == (len(T) + 9) // 10)
        lo, hi = EL.m.wilson(dentro, tot)
        out[sid] = {"frammenti": n_fr, "campioni": tot, "dentro_V": dentro, "quota": round(dentro / tot, 5), "wilson95": [round(lo, 5), round(hi, 5)],
                    "frammenti_sempre_dentro": [fr_ok, n_fr, *[round(x, 5) for x in EL.m.wilson(fr_ok, n_fr)]], "impronta_raggio_m": round(R_imp, 1), "vt_che_decide": vt_imp, "a_terra_fuori_impronta": a_terra_fuori,
                    "caduta_s_min_med_max": [round(min(cadute), 1), round(float(np.median(cadute)), 1), round(max(cadute), 1)] if cadute else None,
                    "parametri_inviluppo": par,
                    "nota": "campioni non indipendenti (stesso frammento in istanti diversi): Wilson per campione e' ottimista; vedi a_terra_fuori"}
    return out


if __name__ == "__main__":
    if "--conti" in sys.argv:
        r = conti()
        json.dump(r, open(os.path.join(QUI, "conti_volo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(json.dumps(r, ensure_ascii=False)[:5000])
    if "--prova" in sys.argv:
        n = int(sys.argv[sys.argv.index("--prova") + 1]) if len(sys.argv) > sys.argv.index("--prova") + 1 else 10
        r = prova(n)
        json.dump(r, open(os.path.join(QUI, "prova_frammenti_volo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
        print(json.dumps(r, ensure_ascii=False, default=float))
