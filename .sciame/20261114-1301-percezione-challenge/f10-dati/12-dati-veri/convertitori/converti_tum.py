"""TUM RGB-D (formato «tgz» di TUM e Bonn) -> formato comune di f10.

Uso:  …/ambiente/venv/bin/python -I -B converti_tum.py <cartella_aperta> <nome_sequenza>
      <cartella_aperta> contiene depth.txt, groundtruth.txt, depth/*.png (archivio già aperto con apri_archivio.py)

Convenzioni dell'insieme (https://cvg.cit.tum.de/data/datasets/rgbd-dataset/file_formats, pagina aperta dal
ricercatore il 14-11-2026, copia in 01-ricercatore/pagine/tum_file_formats.html):
  - PNG a 16 bit, valore 5000 = 1 metro, 0 = nessun dato; il codice d'esempio usa Z = valore / 5000 e
    X = (u − cx)·Z/fx: è la profondità lungo l'asse ottico, non lungo il raggio;
  - la profondità è già registrata sull'immagine a colori: valgono i parametri della camera a colori «Freiburg 3
    RGB» (fx 535,4; fy 539,2; cx 320,1; cy 247,6; distorsione nulla); il fattore di scala di fr3 è 1,000;
  - groundtruth.txt: posa del centro ottico della camera a colori nel riferimento della cattura del moto
    (tx ty tz qx qy qz qw); nessuna annotazione delle persone.
Trasformazione: millimetri = valore / 5 (i valori sono multipli di 5: lo si verifica e si conta chi non lo è).
"""
import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune  # noqa: E402
import cv2  # noqa: E402
import numpy as np  # noqa: E402

FX, FY, CX, CY = 535.4, 539.2, 320.1, 247.6


def leggi_elenco(p):
    righe = []
    with open(p, encoding="ascii", errors="replace") as f:
        for r in f:
            if r.startswith("#") or not r.strip():
                continue
            righe.append(r.split())
    return righe


def rot(qx, qy, qz, qw):
    n = math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw)
    x, y, z, w = qx / n, qy / n, qz / n, qw / n
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def main():
    aperta, nome = sys.argv[1], sys.argv[2]
    dest = comune.cartella_nuova(nome)
    elenco = leggi_elenco(os.path.join(aperta, "depth.txt"))
    tempi = np.array([float(r[0]) for r in elenco])
    gt = np.array([[float(x) for x in r] for r in leggi_elenco(os.path.join(aperta, "groundtruth.txt"))])
    # Posa per fotogramma: la riga di groundtruth più vicina nel tempo (scarto annotato).
    pose = []
    for t in tempi:
        k = int(np.argmin(np.abs(gt[:, 0] - t)))
        R = rot(*gt[k, 4:8])
        asse, destra = R[:, 2], R[:, 0]            # asse ottico e asse x della camera nel mondo (z in alto)
        pose.append((gt[k, 3], math.degrees(math.asin(-asse[2])), math.degrees(math.asin(-destra[2])),
                     abs(gt[k, 0] - t), gt[k, 1], gt[k, 2], math.degrees(math.atan2(asse[1], asse[0]))))
    pose = np.array(pose)
    conta = {"non_multipli_di_5": 0, "pixel": 0}

    def fotogrammi():
        for r in elenco:
            nomefile = r[1]
            if "/" in nomefile.replace("depth/", "", 1) or ".." in nomefile:
                raise SystemExit(f"nome sospetto in depth.txt: {nomefile!r}")
            a = cv2.imread(os.path.join(aperta, nomefile), cv2.IMREAD_UNCHANGED)
            if a is None or a.dtype != np.uint16 or a.shape != (480, 640):
                raise SystemExit(f"{nomefile}: attesa immagine uint16 480x640, trovata {None if a is None else (a.dtype, a.shape)}")
            conta["non_multipli_di_5"] += int((a % 5 != 0).sum())
            conta["pixel"] += a.size
            yield ((a.astype(np.uint32) + 2) // 5).astype(np.uint16)

    h_med, t_med = float(np.median(pose[:, 0])), float(np.median(pose[:, 1]))
    meta = {
        "larghezza": 640, "altezza": 480, "fx": FX, "fy": FY, "cx": CX, "cy": CY, "fps": 30.0,
        "sensore": "Microsoft Kinect v1 (luce strutturata), profondità registrata sul colore dal driver OpenNI",
        "posa": {"altezza_m": round(h_med, 4), "inclinazione_gradi": round(t_med, 3)},
        "origine": "TUM RGB-D benchmark, freiburg3/walking_static, "
                   "https://cvg.cit.tum.de/rgbd/dataset/freiburg3/rgbd_dataset_freiburg3_walking_static.tgz",
        "licenza": "CC BY 4.0",
        "fonte_parametri": "https://cvg.cit.tum.de/data/datasets/rgbd-dataset/file_formats (tabella «Freiburg 3 RGB»)",
        "nota_posa": "camera tenuta in mano, quasi ferma: la posa in «posa» è la MEDIANA sulla sequenza della posa "
                     "della cattura del moto (groundtruth.txt, asse z del mondo assunto verticale con il suolo a quota 0: "
                     "verificato a posteriori sui punti del pavimento, vedi DATI_VERI.md). La posa di ogni fotogramma "
                     "(altezza, inclinazione, rollio, posizione e direzione nel mondo) sta in posa_per_fotogramma.csv.",
        "posa_intervallo": {"altezza_m": [round(float(pose[:, 0].min()), 4), round(float(pose[:, 0].max()), 4)],
                            "inclinazione_gradi": [round(float(pose[:, 1].min()), 3), round(float(pose[:, 1].max()), 3)],
                            "rollio_gradi": [round(float(pose[:, 2].min()), 3), round(float(pose[:, 2].max()), 3)]},
        "verita": "nessuna annotazione delle persone (due persone camminano nella scena); solo la posa della camera",
        "trasformazione": "millimetri = valore_png / 5 (5000 unità = 1 m); tempi = marca temporale di depth.txt meno la prima",
        "tempo_zero_unix_s": float(tempi[0]),
    }
    comune.scrivi_sequenza(dest, meta, tempi - tempi[0], fotogrammi())
    with open(os.path.join(dest, "posa_per_fotogramma.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["indice", "altezza_m", "inclinazione_gradi", "rollio_gradi", "scarto_tempo_posa_s",
                    "x_mondo_m", "y_mondo_m", "direzione_mondo_gradi"])
        for i, p in enumerate(pose):
            w.writerow([i] + [f"{x:.5f}" for x in p])
    print(f"{nome}: {len(elenco)} fotogrammi; pixel non multipli di 5: {conta['non_multipli_di_5']} su {conta['pixel']}; "
          f"posa mediana: altezza {h_med:.3f} m, inclinazione {t_med:.2f}°; scarto massimo tempo-posa {pose[:, 3].max():.4f} s")


if __name__ == "__main__":
    main()
