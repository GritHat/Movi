# fotogrammi_f10.py — le regole su fotogrammi di f10 (formato comune): tre sequenze del modello del sensore e una VERA.
# Non c'e' verita' sul «libero»: si riporta solo cio' che si puo' dire (quante celle, fin dove, quanto sfarfalla) e,
# dove verita.json da' la pianta di ostacoli e soggetti, le celle libere col centro dentro quelle piante.
# Lettura sola, np.load(allow_pickle=False). Rifare: vedi rifai.sh.
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from libero import *

F10 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "f10-dati"))
SEQ = [("11-simulatore/sequenze/d435i_lim__pavimento_vuoto", 0.0100, "modello D435i, livello limite, pavimento vuoto"),
       ("11-simulatore/sequenze/d435i_lim__pavimento_lucido", 0.0100, "modello D435i, livello limite, pavimento lucido"),
       ("11-simulatore/sequenze/d435i_nom__cassa_persona__s00", 0.0040, "modello D435i, nominale, cassa e persona"),
       ("12-dati-veri/sequenze/tum_fr3_walking_static", 0.0040, "VERO: Kinect v1, TUM fr3 walking_static (k assunto, non verificato)"),
       ("12-dati-veri/sequenze/tum_fr3_walking_static", 0.0040, "VERO, lo stesso, ma con la POSA DEL FOTOGRAMMA (posa_per_fotogramma.csv; rollio ignorato)")]
REG = ("V17", "V18-1", "V18-m", "PR4")
NFOT = 6
out = []
for rel, k, desc in SEQ:
    d = os.path.join(F10, rel)
    meta = json.load(open(os.path.join(d, "meta.json")))
    n = len([f for f in os.listdir(os.path.join(d, "profondita")) if f.endswith(".npy")])
    cam = Camera(meta["larghezza"], meta["altezza"], meta["fx"], meta["fy"], meta["cx"], meta["cy"],
                 meta["posa"]["altezza_m"], meta["posa"]["inclinazione_gradi"])
    reg = Regole(cam, k)
    dom = reg.fp_tot > 0
    ver = None
    vp = os.path.join(d, "verita.json")
    if os.path.exists(vp):
        ver = json.load(open(vp))
    i0 = n // 2 - NFOT // 2
    acc = {r: dict(lib=[], lont=[], cambi=0, dentro=0) for r in REG}
    validi, prec = [], None
    pf = None
    if "POSA DEL FOTOGRAMMA" in desc:
        pf = {int(r.split(",")[0]): (float(r.split(",")[1]), float(r.split(",")[2]), float(r.split(",")[3]))
              for r in open(os.path.join(d, "posa_per_fotogramma.csv")).read().split("\n")[1:] if r.strip()}
    for f in range(i0, i0 + NFOT):
        if pf:
            cam = Camera(meta["larghezza"], meta["altezza"], meta["fx"], meta["fy"], meta["cx"], meta["cy"], pf[f][0], pf[f][1])
            reg = Regole(cam, k)
            dom = reg.fp_tot > 0
        D = np.load(os.path.join(d, "profondita", "%06d.npy" % f), allow_pickle=False).astype(np.float64) / 1000.0
        validi.append(100.0 * (D > 0).mean())
        o, qv, occ, omb = reg.tutte(D)
        piante = np.zeros(dom.shape, bool)
        if ver:
            for ob in ver.get("ostacoli", []):
                if ob.get("tipo") == "poligono":
                    v = np.array(ob["vertici"])
                    piante |= (reg.cx >= v[:, 0].min()) & (reg.cx <= v[:, 0].max()) & (reg.cy >= v[:, 1].min()) & (reg.cy <= v[:, 1].max())
                elif ob.get("tipo") == "cerchio":
                    piante |= np.hypot(reg.cx - ob["x"], reg.cy - ob["z"]) <= ob["raggio_m"]
            for fr in ver.get("fotogrammi", []):
                if fr["indice"] == f:
                    for sg in fr["soggetti"]:
                        piante |= np.hypot(reg.cx - sg["x"], reg.cy - sg["z"]) <= sg.get("raggio_m", 0.2)
        for r in REG:
            L = o[r]
            a = acc[r]
            a["lib"].append(int(L.sum()))
            rr = np.where(L, (reg.rix + 1) * DR, 0.0)
            a["lont"].append(float(rr.max()))
            a["dentro"] += int((L & piante).sum())
            if prec is not None and L.shape == prec[r].shape:
                a["cambi"] += int(((L != prec[r]) & dom).sum())
        prec = o
    fps = meta["fps"]
    if pf:
        desc += " [altezza %.3f-%.3f m, inclinazione %.2f-%.2f, rollio %.2f-%.2f gradi nei 6 fotogrammi]" % (
            min(pf[f][0] for f in range(i0, i0 + NFOT)), max(pf[f][0] for f in range(i0, i0 + NFOT)), min(pf[f][1] for f in range(i0, i0 + NFOT)),
            max(pf[f][1] for f in range(i0, i0 + NFOT)), min(pf[f][2] for f in range(i0, i0 + NFOT)), max(pf[f][2] for f in range(i0, i0 + NFOT)))
    out.append("%s\n  %s ; %d x %d ; posa dichiarata %.2f m, %.1f gradi ; k del margine %.4f ; fotogrammi %d-%d di %d ; pixel validi %.1f %% ; celle con impronta %d di %d ; verita' delle piante: %s"
               % (rel, desc, cam.W, cam.H, cam.h, cam.pitch, k, i0, i0 + NFOT - 1, n, np.mean(validi), int(dom.sum()), dom.size, "si'" if ver else "no"))
    for r in REG:
        a = acc[r]
        out.append("    %-5s celle libere per fotogramma %6.1f (%.1f %% delle celle con impronta) ; libero piu' lontano %.1f m ; cambi %.2f /s per cella ; libere col centro nella pianta di un ostacolo o soggetto noto: %s"
                   % (r, np.mean(a["lib"]), 100.0 * np.mean(a["lib"]) / max(1, dom.sum()), np.max(a["lont"]), fps * a["cambi"] / (max(1, dom.sum()) * (NFOT - 1)), a["dentro"] if ver else "n.d."))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "risultati_f10.txt"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
