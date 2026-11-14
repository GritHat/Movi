"""Simulatore minimo dei SOLI frammenti e verifica dell'inviluppo dichiarato (regola EV-A di regole_eventi.json).
Uso: python3 -I frammenti.py   (scrive risultati_frammenti.json accanto). Solo libreria standard. Semi fissi.
Tutto e' simulazione: numero, masse, forme e velocita' dei frammenti sono IPOTESI dichiarate nel json."""
import json, math, os, random, sys, time

QUI = os.path.dirname(os.path.abspath(__file__))
G = 9.81


def t_balistico(z0, vup):
    """Tempo massimo di volo senza resistenza partendo da quota z0 con velocita' verticale vup >= 0."""
    return (vup + math.sqrt(vup * vup + 2 * G * z0)) / G


def inviluppo(tau, ev, par):
    """Volume dichiarato a tau dall'evento. ev: p0 [x,y,z], vc lista di velocita' [vx,vy,vz] delle tracce d'origine,
    r0 (incertezza + ingombro). par: dv, W, Wz, v_t_min. Ritorna r(tau), tau*, zmin, zmax, T_c."""
    z0 = ev["p0"][2]
    vcz_max = max(v[2] for v in ev["vc"]); vcz_min = min(v[2] for v in ev["vc"])
    vup = max(vcz_max + par["dv"] + par["Wz"], 0.0)
    ts = t_balistico(z0 + ev["r0"], vup)                      # tau*: oltre, il tratto balistico non cresce piu'
    tq = min(tau, ts)
    r = par["W"] * tau + (par["dv"] + par["W"]) * tq + ev["r0"]
    zmin = max(0.0, z0 - ev["r0"] + min(vcz_min - par["dv"], -par["Wz"]) * tau - 0.5 * G * tau * tau)
    s = min(tau, vup / G)
    zmax = z0 + ev["r0"] + par["Wz"] * tau + vup * s - 0.5 * G * s * s
    Tc = t_volo(par["v_t_min"], z0 + ev["r0"], vup, par)
    return r, tq, zmin, zmax, Tc


def t_volo(vt, h0, vup, par):
    """Tempo di volo PRUDENTE (non dimostrato) di un frammento con velocita' limite vt: salita verticale con
    resistenza, poi caduta da fermo con velocita' limite ridotta della corrente ascendente; tutto per k_tc."""
    t_su = vt / G * math.atan(vup / vt)
    h = h0 + vt * vt / (2 * G) * math.log(1 + (vup / vt) ** 2)
    ve = vt - par["Wz"]
    q = G * h / (ve * ve)
    t_giu = h / ve + ve * math.log(2) / G if q > 50 else ve / G * math.acosh(math.exp(q))
    return par["k_tc"] * (t_su + t_giu)


def impronta(ev, par, vt_max=None):
    """Raggio dell'impronta finale (disco attorno a p0) e v_t che lo decide: massimo, sulle velocita' limite
    ammesse, di deriva del vento per il tempo di volo piu' gittata nell'aria (limitata dalla resistenza)."""
    z0 = ev["p0"][2]
    vup = max(max(v[2] for v in ev["vc"]) + par["dv"] + par["Wz"], 0.0)
    ts = t_balistico(z0 + ev["r0"], vup)
    vrel = par["dv"] + par["W"] + max(math.hypot(v[0], v[1]) for v in ev["vc"])
    meglio = (0.0, None)
    for i in range(0, 241):
        vt = par["v_t_min"] * 10 ** (i / 80.0)          # da v_t_min a 1000 volte tanto (= senza resistenza)
        if vt_max is not None and vt > vt_max: break
        T = t_volo(vt, z0 + ev["r0"], vup, par)
        a = min(vrel * min(T, ts), vt * vt / G * math.log(1 + G * vrel * T / (vt * vt)))
        meglio = max(meglio, (par["W"] * T + a, vt))
    return meglio[0] + ev["r0"] + par["r_rimbalzo"], meglio[1]


def dist_segmento(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


def dentro_pianta(x, y, tau, ev, par, extra=0.0):
    """Pianta = unione, sulle tracce d'origine, del segmento [p0, p0 + vc_h * tau*] ingrossato di r(tau)."""
    r, tq, _, _, _ = inviluppo(tau, ev, par)
    d = min(dist_segmento(x, y, ev["p0"][0], ev["p0"][1], ev["p0"][0] + v[0] * tq, ev["p0"][1] + v[1] * tq) for v in ev["vc"])
    return d - (r + extra)


def simula(ev, par, vero, n, seme, dt=0.04, raffiche=False):
    """vero: dv_vero, W_vero, Wz_vero, intervallo di v_t [min,max] (log-uniforme), modo ('uniforme' o 'bordo')."""
    rng = random.Random(seme)
    _, _, _, _, Tc = inviluppo(0.0, ev, par)
    R_imp, vt_imp = impronta(ev, par)
    R_str, vt_str = impronta(ev, par, vt_max=vero["vt"][1])   # variante stretta: IPOTESI sul frammento piu' pesante
    dentro_str = 0
    tol = 0.05
    camp = fuori = 0; peggio = -1e9
    a_terra = entro_Tc = dentro_impr = 0
    t_volo_max = 0.0; gittata_max = 0.0; rapporto_gittata_max = 0.0
    T_fine = max(2 * Tc, 30.0)
    for i in range(n):
        v = ev["vc"][rng.randrange(len(ev["vc"]))]
        # direzione isotropa, modulo secondo il modo
        while True:
            d = [rng.gauss(0, 1) for _ in range(3)]
            nd = math.sqrt(sum(c * c for c in d))
            if nd > 1e-9: break
        mod = vero["dv"] * (1.0 if vero["modo"] == "bordo" else rng.random() ** (1 / 3))
        ro = ev["r0"] * rng.random() ** (1 / 3)
        while True:
            e = [rng.gauss(0, 1) for _ in range(3)]
            ne = math.sqrt(sum(c * c for c in e))
            if ne > 1e-9: break
        x, y, z = (ev["p0"][k] + ro * e[k] / ne for k in range(3))
        z = max(z, 0.01)
        vx, vy, vz = (v[k] + mod * d[k] / nd for k in range(3))
        vt = math.exp(rng.uniform(math.log(vero["vt"][0]), math.log(vero["vt"][1])))
        k = G / (vt * vt)
        az = rng.uniform(0, 2 * math.pi)
        wm = vero["W"] * (1.0 if vero["modo"] == "bordo" else math.sqrt(rng.random()))
        wx, wy, wz = wm * math.cos(az), wm * math.sin(az), rng.uniform(-vero["Wz"], vero["Wz"])
        x0, y0 = x, y
        t = 0.0; prossimo = 0.5; caduto = False
        while t < T_fine:
            if raffiche and int(round(t / dt)) % 12 == 0:        # ogni 0,48 s il vento cambia, restando entro i limiti
                az = rng.uniform(0, 2 * math.pi); wm = vero["W"] * math.sqrt(rng.random())
                wx, wy, wz = wm * math.cos(az), wm * math.sin(az), rng.uniform(-vero["Wz"], vero["Wz"])
            # punto medio (RK2) con sottopassi: h <= 0,2 / (k |v_rel|), altrimenti lo schema esplicito diverge
            resto = dt
            while resto > 1e-12 and z > 0.0:
                rx, ry, rz = vx - wx, vy - wy, vz - wz
                s = k * math.sqrt(rx * rx + ry * ry + rz * rz)
                h = min(resto, 0.2 / (s + 1e-9))
                mx, my, mz = vx - 0.5 * h * s * rx, vy - 0.5 * h * s * ry, vz + 0.5 * h * (-G - s * rz)
                rx, ry, rz = mx - wx, my - wy, mz - wz
                s = k * math.sqrt(rx * rx + ry * ry + rz * rz)
                x += h * mx; y += h * my; z += h * mz
                vx -= h * s * rx; vy -= h * s * ry; vz += h * (-G - s * rz)
                resto -= h
            t += dt
            if z <= 0.0:
                caduto = True; z = 0.0
            if t >= prossimo - 1e-9 or caduto:
                prossimo += 0.5
                r, tq, zmin, zmax, _ = inviluppo(t, ev, par)
                ecc = max(dentro_pianta(x, y, t, ev, par), zmin - z, z - zmax)
                camp += 1
                if ecc > tol: fuori += 1
                peggio = max(peggio, ecc)
            if caduto: break
        if caduto:
            a_terra += 1
            t_volo_max = max(t_volo_max, t)
            if t <= Tc: entro_Tc += 1
            if math.hypot(x - ev["p0"][0], y - ev["p0"][1]) <= R_imp + tol: dentro_impr += 1
            if math.hypot(x - ev["p0"][0], y - ev["p0"][1]) <= R_str + tol: dentro_str += 1
            gittata_max = max(gittata_max, math.hypot(x - x0, y - y0))
    r_c, tq_c, _, _, _ = inviluppo(Tc, ev, par)
    return {"n": n, "campioni": camp, "campioni_fuori_dal_volume": fuori,
            "quota_dentro_volume": round(1 - fuori / max(camp, 1), 6), "eccedenza_massima_m": round(peggio, 2),
            "a_terra_entro_fine": a_terra, "quota_a_terra_entro_Tc": round(entro_Tc / n, 6),
            "quota_cadute_dentro_impronta": round(dentro_impr / n, 6), "t_volo_max_s": round(t_volo_max, 1),
            "gittata_max_m": round(gittata_max, 1), "T_c_s": round(Tc, 1), "tau_stella_s": round(tq_c, 2),
            "raggio_pianta_volume_a_Tc_m": round(r_c, 1),
            "raggio_impronta_m": round(R_imp, 1), "raggio_impronta_stretta_m": round(R_str, 1),
            "quota_cadute_dentro_impronta_stretta": round(dentro_str / n, 6), "v_t_che_decide_stretta_m_s": round(vt_str, 1), "v_t_che_decide_impronta_m_s": round(vt_imp, 1)}


def tabella_inviluppo(ev, par, tempi=(0.5, 1, 2, 3, 5, 10, 20, 30, 60)):
    out = []
    for tau in tempi:
        r, tq, zmin, zmax, Tc = inviluppo(tau, ev, par)
        out.append({"tau_s": tau, "raggio_m": round(r, 1), "tratto_centri_m": [round(math.hypot(v[0], v[1]) * tq, 1) for v in ev["vc"]],
                    "z_min_m": round(zmin, 1), "z_max_m": round(zmax, 1)})
    return out


def main():
    reg = json.load(open(os.path.join(QUI, "regole_eventi.json")))
    fr = reg["EV-A_frammentazione"]
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    ris = {"avvertenza": "SIMULAZIONE: frammenti puntiformi, resistenza quadratica isotropa, ipotesi dichiarate in regole_eventi.json. Nessun dato reale.",
           "n_per_caso": n, "passo_s": 0.04, "casi": {}}
    t0 = time.time()
    for nome, sc in fr["casi_di_verifica"].items():
        ev = sc["evento"]
        for livello in ("nominale", "prudente"):
            par = dict(fr["inviluppo"][sc["profilo"]][livello]); par["k_tc"] = fr["k_tc"]; par["r_rimbalzo"] = fr["r_rimbalzo_m"]
            base = {"dv": par["dv"], "W": par["W"], "Wz": par["Wz"], "vt": [par["v_t_min"], sc["v_t_max_m_s"]]}
            casi = {
                "P1_uniforme": (dict(base, modo="uniforme"), False),
                "P1_bordo": (dict(base, modo="bordo"), False),
                "P5_raffiche": (dict(base, modo="bordo"), True),
                "P4_dv_vera_1.5x": (dict(base, dv=1.5 * par["dv"], modo="uniforme"), False),
                "P6_leggeri": (dict(base, vt=[par["v_t_min"] / 4, par["v_t_min"]], modo="uniforme"), False),
            }
            for c, (vero, raff) in casi.items():
                chiave = f"{nome}/{livello}/{c}"
                ris["casi"][chiave] = simula(ev, par, vero, n if c != "P6_leggeri" else n // 5, seme=hash_stabile(chiave), raffiche=raff)
                print(chiave, ris["casi"][chiave], flush=True)
            ris["casi"][f"{nome}/{livello}/tabella_inviluppo"] = tabella_inviluppo(ev, par)
    ris["durata_s"] = round(time.time() - t0, 1)
    json.dump(ris, open(os.path.join(QUI, "risultati_frammenti.json"), "w"), indent=1, ensure_ascii=False)


def hash_stabile(s):
    h = 0
    for ch in s: h = (h * 131 + ord(ch)) % 2147483647
    return h


if __name__ == "__main__":
    main()
