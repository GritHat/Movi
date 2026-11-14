"""Princeton Tracking Benchmark (ValidationSet) -> formato comune di f10.

Uso:  …/ambiente/venv/bin/python -I -B converti_princeton.py <cartella_ValidationSet> <sequenza> <nome_sequenza>

Convenzioni (https://tracking.cs.princeton.edu/dataset.html, copia in 01-ricercatore/pagine/princeton_dataset.html):
  - depth/d-<tempo>-<id>.png: 16 bit con i 3 bit bassi spostati in alto; si rimettono a posto con
    valore = (v >> 3) | (v << 13) (su 16 bit), come nel codice d'esempio della pagina; poi è in millimetri, e il
    codice d'esempio lo usa come Z (X = (x − cx)·Z/fx): profondità lungo l'asse ottico;
  - frames.json: K (fx = fy = 575,8157496; cx = 320; cy = 240 con pixel contati da 1: qui cx = 319, cy = 239),
    depthTimestamp in microsecondi, depthFrameID;
  - <sequenza>.txt: x, y, larghezza, altezza del riquadro del bersaglio (pixel da 1), poi il numero del fotogramma;
    «NaN» quando il bersaglio non è visibile (e allora il numero ripete l'ultimo visibile: vale l'ordine delle righe). La pagina non dichiara una licenza.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune  # noqa: E402
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from riquadri import verita_da_riquadri  # noqa: E402

BERSAGLI = {"child_no1": "bambino che cammina (persona)", "new_ex_occ4": "persona che cammina, coperta da un'altra persona",
            "face_occ5": "viso di una persona seduta, coperto da un libro (non è una persona che cammina)",
            "bear_front": "pupazzo tenuto in mano, coperto da un libro (non è una persona)", "zcup_move_1": "tazza (non è una persona)"}


def main():
    radice, seq, nome = sys.argv[1], sys.argv[2], sys.argv[3]
    if not seq.replace("_", "").isalnum():
        raise SystemExit("nome di sequenza non valido")
    dest = comune.cartella_nuova(nome)
    base = os.path.join(radice, seq)
    with open(os.path.join(base, "frames.json"), encoding="utf-8") as f:
        fr = json.load(f)
    K = fr["K"]
    fx, fy, cx, cy = float(K[0][0]), float(K[1][1]), float(K[0][2]) - 1.0, float(K[1][2]) - 1.0
    n = int(fr["length"])
    tempi = np.array([int(t) for t in fr["depthTimestamp"][:n]], dtype=np.float64) / 1e6
    ids = [int(i) for i in fr["depthFrameID"][:n]]
    if np.diff(tempi).min() <= 0:
        raise SystemExit("tempi della profondità non crescenti")

    # Il Kinect è a 30 Hz nominali, ma alcune sequenze sono registrate un fotogramma sì e uno no: «fps» segue i tempi.
    fps = round(1.0 / float(np.median(np.diff(tempi))), 1)

    def fotogrammi():
        for t, i in zip(fr["depthTimestamp"][:n], ids):
            a = cv2.imread(os.path.join(base, "depth", f"d-{int(t)}-{int(i)}.png"), cv2.IMREAD_UNCHANGED)
            if a is None or a.dtype != np.uint16 or a.shape != (480, 640):
                raise SystemExit(f"d-{t}-{i}.png: attesa uint16 480x640")
            yield ((a >> 3) | (a << 13)).astype(np.uint16)

    meta = {
        "larghezza": 640, "altezza": 480, "fx": fx, "fy": fy, "cx": cx, "cy": cy, "fps": fps,
        "sensore": "Microsoft Kinect v1 (luce strutturata) via OpenNI; profondità registrata sul colore (non verificato)",
        "posa": None,
        "origine": f"Princeton Tracking Benchmark, ValidationSet, sequenza {seq}, https://tracking.cs.princeton.edu/ValidationSet.zip",
        "licenza": "non dichiarata nella pagina dell'insieme; non verificata",
        "fonte_parametri": "frames.json della sequenza (K); cx e cy diminuiti di 1 perché il codice d'esempio conta i pixel da 1",
        "bersaglio": BERSAGLI.get(seq, "non descritto"),
        "trasformazione": "millimetri = (v >> 3) | (v << 13) su 16 bit; tempi = depthTimestamp / 1e6",
        "nota_fps": "fps = inverso del passo mediano dei tempi (il sensore è a 30 Hz nominali)",
        "nota_verita": "posa ignota: x e z sono nel riferimento della camera e sono DERIVATI dalla profondità dentro il "
                       "riquadro annotato (mediana della metà centrale); la verità dell'insieme è il riquadro e la visibilità",
    }
    comune.scrivi_sequenza(dest, meta, tempi - tempi[0], fotogrammi())
    annot = []
    with open(os.path.join(base, seq + ".txt"), encoding="ascii", errors="replace") as f:
        for r in f:
            c = r.strip().split(",")
            if len(c) < 5:
                continue
            k = len(annot)                             # la riga k-esima vale per il fotogramma k-esimo
            # Nelle righe «NaN» la quinta colonna ripete l'ultimo numero visibile: la si controlla solo sulle altre.
            if "nan" not in c[0].lower() and (k >= n or ids[k] != int(float(c[4]))):
                raise SystemExit(f"riga {k}: numero di fotogramma {c[4]} diverso da quello atteso")
            if "nan" in c[0].lower():
                annot.append((k, None, None))
            else:
                x, y, w, h = [float(v) for v in c[:4]]
                annot.append((k, (x - 1, y - 1, x - 1 + w, y - 1 + h), None))
    annot.sort(key=lambda a: a[0])
    v, cont = verita_da_riquadri(lambda i: comune.leggi_profondita(dest, i), annot, fx, cx, "bersaglio")
    comune.salva_json(os.path.join(dest, "verita.json"), v)
    print(f"{nome}: {n} fotogrammi, {len(annot)} annotati, {sum(1 for a in annot if a[1] is None)} nascosti, {cont}")


if __name__ == "__main__":
    main()
