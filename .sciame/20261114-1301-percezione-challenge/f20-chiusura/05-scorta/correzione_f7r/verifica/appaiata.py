# Ripete il codice F7r ORIGINALE (scorta_f7r.py, senza c1) sul seme 20261124: confronto appaiato con c1.
import sys, json, importlib.util
from multiprocessing import Pool
SRC = "/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f20-chiusura/05-scorta/scorta_f7r.py"
def carica():
    s = importlib.util.spec_from_file_location("f7r_orig", SRC); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
M = None
def lav(a):
    global M
    if M is None: M = carica()
    v, c, i = a
    r = M.passaggio(v, c, i, 20261124)
    r.pop("curva", None)
    return {k: (x if isinstance(x, (int, float, str, bool, type(None))) else str(x)) for k, x in r.items()}
if __name__ == "__main__":
    lavori = [(v, "att", i) for v in ("davanti", "vira", "totale") for i in range(60)]
    with Pool(5) as p:
        out = p.map(lav, lavori)
    with open(sys.argv[1], "x") as f:
        for r in out: f.write(json.dumps(r) + "\n")
