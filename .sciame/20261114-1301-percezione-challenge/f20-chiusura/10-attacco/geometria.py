"""geometria.py (sciame-avversario) - varianti di geometria di F3 ed F6 con il nucleo v4 congelato (regola v4c),
importato senza modificarlo. Semi nuovi: idx 5000-5019. Uso: python -I geometria.py uscita.jsonl"""
import copy, importlib.util, json, math, os, sys
os.environ.setdefault("VOLO_REGOLA", "v4c")
QUI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(QUI), "01-contatto", "prove_volo_v4_congelato.py")
spec = importlib.util.spec_from_file_location("pv4", SRC)
pv4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(pv4)
import numpy as np
BASE = copy.deepcopy(pv4.SCV)

def variante(nome):
    e = nome.split("-")[0]
    sc = copy.deepcopy(BASE[e])
    O = {o["id"]: o for o in sc["oggetti"]}
    if nome in ("F3-ang30", "F3-ang150"):
        th = math.radians(30 if nome.endswith("30") else 150)
        O["droneB"]["punti"] = [[-700*math.cos(th), -700*math.sin(th), 120], [0, 0, 120]]
    elif nome in ("F3-quota40", "F3-quota400"):
        dz = -80 if nome.endswith("40") else 280
        for o in O.values():
            o["punti"] = [[p[0], p[1], p[2]+dz] for p in o["punti"]]
        for ev in sc["eventi"]:
            ev["parametri"]["p"][2] += dz
    elif nome in ("F3-radar600", "F3-radar4200"):
        q = -400 if nome.endswith("600") else -3000
        for s in sc["sensori"]:
            s["pos"] = [q, q, s["pos"][2]]
    elif nome.startswith("F6-"):
        # incrocio portato DENTRO la finestra di 40 s: A a x = 0 e B a y = 0 a t = 20 s
        dx, dz = 1500, 300
        th = math.radians(90)
        if nome == "F6-vicino": dx, dz = 500, 150
        if nome == "F6-ang45": th = math.radians(45)
        O["aereo1"]["punti"] = [[-2400, 0, 600], [6000, 0, 600]]
        u = np.array([math.cos(th), math.sin(th)])
        a = np.array([dx, 0.0]) - 2000*u; b = np.array([dx, 0.0]) + 6000*u
        O["aereo2"]["punti"] = [[a[0], a[1], 600+dz], [b[0], b[1], 600+dz]]
        if nome == "F6-radar6km":
            for s in sc["sensori"]:
                s["pos"] = [0, -6000, s["pos"][2]]
    return e, sc

def lavoro(a):
    nome, cfg, idx = a
    try:
        e, sc = variante(nome)
        pv4.SCV[e] = sc
        R, _ = pv4.passaggio_volo(e, cfg, idx)
        D = pv4._G["D"]
        ks = [k for k in D["ogg"] if D["ogg"][k]["classe"] != "frammento"]
        dmin = None
        if len(ks) >= 2:
            P1, P2 = D["ver"][ks[0]][1], D["ver"][ks[1]][1]
            n = min(len(P1), len(P2), int(20.0/0.1) if e == "F3" else len(P1))
            dd = np.linalg.norm(P1[:n]-P2[:n], axis=1); dmin = [float(dd.min()), float(np.argmin(dd)*0.1)]
        return {"var": nome, "cfg": cfg, "idx": idx, "evento": R.get("evento") is not None,
                "ritardo": R.get("ritardo_evento_s"), "falso": bool(R.get("falso_evento")),
                "libero_vero": R["libero_sul_vero"][0], "innesco": R.get("innesco_v4c"), "dmin_vero_m_t": dmin}
    except Exception as ex:
        import traceback
        return {"var": nome, "cfg": cfg, "idx": idx, "errore": repr(ex), "tr": traceback.format_exc()[-800:]}

if __name__ == "__main__":
    from multiprocessing import Pool
    V = sys.argv[2].split(",")
    N = int(sys.argv[3])
    lav = [(v, c, i) for v in V for c in ("att", "sda") for i in range(5000, 5000+N)]
    with Pool(6) as p, open(sys.argv[1], "w") as f:
        for r in p.imap_unordered(lavoro, lav):
            f.write(json.dumps(r, default=float) + "\n"); f.flush()
