"""DepthTrack (formato VOT-RGBD: depth/%08d.png, groundtruth.txt, *.tag) -> formato comune di f10.

Uso:  …/ambiente/venv/bin/python -I -B converti_depthtrack.py <cartella_sequenza> <nome_sequenza>

Che cosa è documentato (articolo, https://ar5iv.labs.arxiv.org/html/2108.13962, aperto il 14-11-2026, copia in
12-dati-veri/pagine/): sensore Intel RealSense 415, 640×360, 30 fps, profondità in PNG a 16 bit.
Che cosa NON è documentato nelle pagine lette: l'unità della profondità (qui ASSUNTA 1 unità = 1 mm, il valore
predefinito dei RealSense D400), i parametri della camera (qui valori NOMINALI: campo orizzontale 69,4° della camera a
colori del D415, nell'ipotesi che la profondità sia allineata al colore: fx = fy = 320 / tan(34,7°) = 462,1; se non è
allineata, col campo di 65° della profondità sarebbe fx = 502,3), la posa. Chi usa x, z o le distanze laterali di
questa sequenza eredita un errore di scala laterale fino a circa il 9 %.
Trasformazione: valore copiato; 65535 -> 0 (contato). groundtruth.txt: x, y, larghezza, altezza (pixel), «nan» se
il bersaglio è del tutto nascosto. Le etichette per fotogramma (occlusione parziale e totale) vanno in verita.json.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune  # noqa: E402
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from riquadri import verita_da_riquadri  # noqa: E402


def main():
    base, nome = sys.argv[1], sys.argv[2]
    dest = comune.cartella_nuova(nome)
    with open(os.path.join(base, "groundtruth.txt"), encoding="ascii", errors="replace") as f:
        gt = [r.strip().split(",") for r in f if r.strip()]
    n = len(gt)
    tag = {}
    for t in ("full-occlusion", "partial-occlusion", "out-of-frame", "moving-view"):
        with open(os.path.join(base, t + ".tag"), encoding="ascii", errors="replace") as f:
            tag[t] = [r.strip() == "1" for r in f if r.strip()]
        if len(tag[t]) != n:
            raise SystemExit(f"{t}.tag ha {len(tag[t])} righe, groundtruth {n}")
    conta = {"saturi_65535": 0, "pixel": 0}

    def fotogrammi():
        for i in range(n):
            a = cv2.imread(os.path.join(base, "depth", f"{i + 1:08d}.png"), cv2.IMREAD_UNCHANGED)
            if a is None or a.dtype != np.uint16 or a.shape != (360, 640):
                raise SystemExit(f"depth/{i + 1:08d}.png: attesa uint16 360x640")
            s = a == 65535
            conta["saturi_65535"] += int(s.sum()); conta["pixel"] += a.size
            a = a.copy(); a[s] = 0
            yield a

    fx = 320.0 / math.tan(math.radians(69.4 / 2))
    meta = {
        "larghezza": 640, "altezza": 360, "fx": round(fx, 2), "fy": round(fx, 2), "cx": 319.5, "cy": 179.5, "fps": 30.0,
        "sensore": "Intel RealSense D415 (stereo attivo a infrarossi)", "posa": None,
        "origine": "DepthTrack (ICCV 2021), insieme di prova, sequenza human02_indoor, "
                   "https://zenodo.org/records/5792146 (human02_indoor.zip)",
        "licenza": "CC BY 4.0",
        "fonte_parametri": "NESSUNA: l'insieme non dà i parametri della camera. fx, fy, cx, cy sono NOMINALI (campo "
                           "orizzontale 69,4° della camera a colori del D415, pixel quadrati, centro al centro dell'immagine)",
        "parametri_affidabili": False,
        "unita_profondita": "ASSUNTA 1 unità = 1 mm (predefinito dei RealSense D400); non documentata nelle pagine lette",
        "trasformazione": "valore copiato; 65535 -> 0; tempi = indice / 30 (l'insieme non dà marche temporali)",
        "bersaglio": "una persona che cammina fra altre persone, in una sala con tavoli e sedie; camera ferma secondo l'etichetta moving-view = 0",
        "nota_verita": "posa ignota: x e z sono nel riferimento della camera e sono DERIVATI dalla profondità dentro il "
                       "riquadro annotato; la verità dell'insieme è il riquadro e le etichette di occlusione",
    }
    comune.scrivi_sequenza(dest, meta, np.arange(n) / 30.0, fotogrammi())
    meta["conteggi_conversione"] = conta
    comune.salva_json(os.path.join(dest, "meta.json"), meta)
    annot = []
    for i, c in enumerate(gt):
        campi = {"occlusione_parziale": tag["partial-occlusion"][i], "occlusione_totale": tag["full-occlusion"][i]}
        if "nan" in c[0].lower():
            annot.append((i, None, campi))
        else:
            x, y, w, h = [float(v) for v in c[:4]]
            annot.append((i, (x, y, x + w, y + h), campi))
    v, cont = verita_da_riquadri(lambda i: comune.leggi_profondita(dest, i), annot, fx, 319.5, "bersaglio")
    comune.salva_json(os.path.join(dest, "verita.json"), v)
    print(f"{nome}: {n} fotogrammi, nascosti {sum(1 for a in annot if a[1] is None)}, parziali {sum(tag['partial-occlusion'])}, "
          f"saturi {conta['saturi_65535']} su {conta['pixel']}, {cont}")


if __name__ == "__main__":
    main()
