"""attacco_f7.py (arbitro, f20/20-verdetto): attacco essenziale su F7 senza modificare scorta_f7.py.
Importa scorta_f7 (sola lettura), crea varianti di verita() per sostituzione testuale e scrive attacco_f7.jsonl (modo x)."""
import inspect, json, os, sys, collections
sys.dont_write_bytecode = True
SC = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f20-chiusura/05-scorta"
sys.path.insert(0, SC)
import scorta_f7 as sc  # noqa
QUI = os.path.dirname(os.path.abspath(__file__))
SRC = inspect.getsource(sc.verita)
ORIG = sc.verita
DV0 = sc.DETRITI["dv_sim"]
SOST = {
    "vicino": ("rel = np.array([rv.uniform(30, 100), rv.uniform(-10, 10), rv.uniform(-10, 10)])",
               "rel = np.array([rv.uniform(10, 30), rv.uniform(-10, 10), rv.uniform(-10, 10)])"),
    "F7c_vicino": ("off = np.array([0, 0, rv.uniform(30, 60)])", "off = np.array([0, 0, rv.uniform(5, 20)])"),
}
VAR_F = {}
for k, (a, b) in SOST.items():
    assert SRC.count(a) == 1, k
    ns = dict(sc.__dict__)
    exec(SRC.replace(a, b), ns)
    VAR_F[k] = ns["verita"]


def lavoro(a):
    gruppo, var, cfg, idx, base = a
    sc.verita = ORIG
    sc.DETRITI["dv_sim"] = DV0
    if gruppo == "vicino":
        sc.verita = VAR_F["vicino"]
    elif gruppo == "F7c_vicino":
        sc.verita = VAR_F["F7c_vicino"]
    elif gruppo == "dv100":
        sc.DETRITI["dv_sim"] = 100.0
    try:
        r = sc.passaggio(var, cfg, idx, base)
        r.pop("curva", None)
    except Exception as e:  # noqa
        r = {"errore": repr(e)}
    r["gruppo"] = gruppo
    return r


if __name__ == "__main__":
    L = []
    for v in ("lato", "davanti", "dietro", "vira"):
        for c in ("att", "sda"):
            L += [("semi_nuovi", v, c, i, 20261199) for i in range(20)]
    for c in ("att", "sda"):
        L += [("semi_nuovi", "F7c", c, i, 20261199) for i in range(60)]
        L += [("vicino", "davanti", c, i, 20261198) for i in range(20)]
        L += [("F7c_vicino", "F7c", c, i, 20261198) for i in range(60)]
    L += [("dv100", v, "sda", i, 20261197) for v in ("davanti", "lato") for i in range(20)]
    from multiprocessing import Pool
    with Pool(6) as p:
        out = p.map(lavoro, L, chunksize=2)
    with open(os.path.join(QUI, "attacco_f7.jsonl"), "x", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False, default=float) + "\n")
    print("fatto", len(out), collections.Counter(r["gruppo"] for r in out))
