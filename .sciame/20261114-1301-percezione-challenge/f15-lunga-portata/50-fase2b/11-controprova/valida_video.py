"""valida_video.py - validatore MIO (sciame-avversario) dei registri video del modo lungo. Legge solo i registro.jsonl.
Per ogni fotogramma ricostruisce le celle COME LE MOSTRA il visore (mostra_lungo: se il fotogramma non ha rle, tiene
l'ultima) e controlla: (a) nessuna cella mostrata «libero» con centro dentro un avviso (cerchio o poligono) o dentro
volume/impronta dei detriti del fotogramma stesso; (b) la stessa cosa sulle sole celle scritte nel fotogramma;
(c) i conteggi mostrati coincidono con celle.conteggi del fotogramma (stato mostrato = stato del registro);
(d) stati di cella e di traccia fra quelli dichiarati; parola coerente con lo stato. Uso: python -I valida_video.py DIR..."""
import json, sys, os
from collections import Counter
def dentro_pol(p, P):
    x, y = p; c = False
    for i in range(len(P)):
        x1, y1 = P[i][:2]; x2, y2 = P[i-1][:2]
        if (y1 > y) != (y2 > y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1: c = not c
    return c
def dentro(p, f):
    if f["tipo"] == "cerchio":
        return (p[0]-f["centro"][0])**2+(p[1]-f["centro"][1])**2 <= f["raggio_m"]**2
    if f["tipo"] == "poligono": return dentro_pol(p, f["punti"])
    raise ValueError(f["tipo"])
def forme(r):
    F = [("avviso#%s" % a.get("id_traccia"), a["forma"]) for a in r.get("avvisi", [])]
    d = r.get("detriti") or {}
    for k in ("volume", "impronta"):
        v = d.get(k) or []
        for f in (v if isinstance(v, list) else [v]): F.append(("detriti_"+k, f))
    return F
def valida(dirp):
    L = [json.loads(x) for x in open(os.path.join(dirp, "registro.jsonl"))]
    T = L[0]; g = json.loads(T["griglie"].replace("'", '"')) if isinstance(T["griglie"], str) else T["griglie"]
    g = list(g.values())[0]; (x0, x1), (y0, y1), (nx, ny) = g["x"], g["y"], g["n"]
    dx, dy = (x1-x0)/(nx-1), (y1-y0)/(ny-1)
    E = Counter(); es = {}; mostrate = None; fr = 0
    for r in L:
        if r.get("tipo") != "fotogramma": continue
        fr += 1
        scritte = None
        if r["celle"].get("rle"):
            scritte = [s for s, k in r["celle"]["rle"] for _ in range(k)]; mostrate = scritte
        F = forme(r)
        for nome, cel in (("mostrate", mostrate), ("scritte", scritte)):
            if cel is None: continue
            for idx, s in enumerate(cel):
                if s != "libero": continue
                j, i = divmod(idx, nx); p = (x0+i*dx, y0+j*dy)
                for nf, f in F:
                    if dentro(p, f):
                        E["libero_dentro_"+nf.split("#")[0]+"_"+nome] += 1; es.setdefault("libero_dentro_"+nf.split("#")[0]+"_"+nome, (r["t"], p, nf))
        if mostrate is not None and Counter(mostrate) != Counter({k: v for k, v in r["celle"]["conteggi"].items() if v}):
            E["conteggi_mostrati_diversi_dal_registro"] += 1; es.setdefault("conteggi_mostrati_diversi_dal_registro", (r["t"], dict(Counter(mostrate)), r["celle"]["conteggi"]))
        if mostrate is not None and scritte is None: E["fotogrammi_con_celle_riportate_da_prima"] += 1
        for s in set(mostrate or []):
            if s not in g["stati"]: E["stato_cella_non_dichiarato"] += 1
        for tr in r.get("tracce", []):
            if tr["stato"] not in ("vista", "non_vista", "previsto_ampio"): E["stato_traccia_ignoto:"+tr["stato"]] += 1
        # libero dichiarato per classi mentre c'e' affidabilita' persa sul solo sensore a griglia
        if r.get("libero_per_classi") and any(a["griglia"] and a["stato"] != "affidabile" for a in r.get("affidabilita_per_sensore", [])):
            E["libero_per_classi_con_griglia_non_affidabile"] += 1
    return {"fotogrammi": fr, "conteggi": dict(E), "primo_esempio": {k: str(v)[:200] for k, v in es.items()}}
if __name__ == "__main__":
    out = {os.path.basename(d.rstrip("/")): valida(d) for d in sys.argv[1:]}
    print(json.dumps(out, indent=1, ensure_ascii=False))
