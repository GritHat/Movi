"""THÖR (tracce di persone dalla cattura del moto Qualisys, file *_6D.tsv) -> «tracce» per f10.

Uso:  …/ambiente/venv/bin/python -I -B converti_thor.py <file_6D.tsv> <nome>

NON è una sequenza del formato comune: THÖR non ha immagini di profondità, quindi non c'è `profondita/` né una
camera (niente fx, fy, posa). Si scrive in 12-dati-veri/tracce/<nome>/ ciò che del formato ha senso:
  - meta.json   (origine, licenza, frequenza, riferimento, corpi, punti fermi);
  - tempi.csv   (indice, tempo_s), 100 Hz;
  - tracce.npz  (senza pickle): `tempo_s` (T), `id` (N testi), `xy_m` (T×N×2, float32, NaN dove la cattura ha perso il
                corpo), `quota_m` (T×N), `residuo_mm` (T×N);
  - verita.json nello schema del formato comune, ma nel riferimento del MONDO della cattura (x = X, z = Y, in metri):
                un soggetto compare nel fotogramma solo se la cattura lo vede (sempre "visibile": true); se manca,
                la posizione è ignota (non è «nascosto con posizione nota»).
Convenzioni del file (intestazione di 11 righe scritta da Qualisys; verificate sui numeri, non su una documentazione):
  colonne separate da tabulazioni; per ogni corpo 16 valori più una colonna vuota: X Y Z (millimetri) Roll Pitch Yaw
  Residual Rot[0..8]; un corpo perso ha tutti i valori a 0. La posizione è quella del casco (testa), non dei piedi.
Trasformazione: metri = millimetri / 1000; (0, 0, 0) -> NaN.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune  # noqa: E402
import numpy as np  # noqa: E402


def main():
    p, nome = sys.argv[1], sys.argv[2]
    dest = os.path.join(comune.TRACCE, nome)
    if os.path.isdir(dest) and os.listdir(dest):
        raise SystemExit(f"{dest} esiste già")
    os.makedirs(dest, exist_ok=True)
    hdr = {}
    with open(p, encoding="utf-8", errors="replace") as f:
        for _ in range(11):
            r = f.readline().rstrip("\r\n").split("\t")
            hdr[r[0]] = r[1:]
    corpi = hdr["BODY_NAMES"]
    freq = float(hdr["FREQUENCY"][0])
    a = np.genfromtxt(p, delimiter="\t", skip_header=11, usecols=range(0, 2 + 17 * len(corpi)), filling_values=np.nan)
    if a.shape[0] != int(hdr["NO_OF_FRAMES"][0]):
        raise SystemExit(f"righe lette {a.shape[0]}, dichiarate {hdr['NO_OF_FRAMES'][0]}")
    t = a[:, 1]
    if not np.allclose(np.diff(t), 1 / freq, atol=1e-6):
        raise SystemExit("tempi non uniformi")
    persone, fermi = [], {}
    xy, quota, res = [], [], []
    for b, c in enumerate(corpi):
        k = 2 + 17 * b
        x, y, z, rr = a[:, k], a[:, k + 1], a[:, k + 2], a[:, k + 6]
        ok = np.isfinite(x) & ~((x == 0) & (y == 0) & (z == 0))
        if not c.startswith("Helmet"):
            if ok.sum():
                fermi[c] = {"x_m": round(float(np.median(x[ok])) / 1000, 3), "y_m": round(float(np.median(y[ok])) / 1000, 3),
                            "quota_m": round(float(np.median(z[ok])) / 1000, 3), "quota_valida": round(float(ok.mean()), 4)}
            continue
        if ok.sum() == 0:
            continue
        persone.append(c)
        xy.append(np.where(ok[:, None], np.stack([x, y], 1) / 1000.0, np.nan))
        quota.append(np.where(ok, z / 1000.0, np.nan)); res.append(np.where(ok, rr, np.nan))
    xy = np.stack(xy, 1).astype(np.float32); quota = np.stack(quota, 1).astype(np.float32); res = np.stack(res, 1).astype(np.float32)
    np.savez_compressed(os.path.join(dest, "tracce.npz"), tempo_s=t, id=np.array(persone), xy_m=xy, quota_m=quota, residuo_mm=res)
    with open(os.path.join(dest, "tempi.csv"), "w", encoding="utf-8", newline="") as f:
        f.write("indice,tempo_s\n")
        for i, x in enumerate(t):
            f.write(f"{i},{x:.6f}\n")
    fot = []
    for i in range(len(t)):
        ss = [{"id": persone[j], "x": round(float(xy[i, j, 0]), 4), "z": round(float(xy[i, j, 1]), 4), "visibile": True}
              for j in range(len(persone)) if np.isfinite(xy[i, j, 0])]
        fot.append({"indice": i, "soggetti": ss})
    with open(os.path.join(dest, "verita.json"), "w", encoding="utf-8") as f:
        json.dump({"fotogrammi": fot, "nota": "riferimento del mondo della cattura del moto (x = X, z = Y, metri), non di una camera; "
                   "un soggetto assente dal fotogramma è «non tracciato» (posizione ignota)"}, f)
        f.write("\n")
    meta = {
        "tipo": "tracce (nessuna immagine di profondità: NON è una sequenza del formato comune)",
        "fps": freq, "sensore": "cattura del moto Qualisys, 10 camere (caschi con marcatori)", "posa": None,
        "origine": f"THÖR, https://zenodo.org/records/3382145, file {os.path.basename(p)}", "licenza": "CC BY 4.0",
        "riferimento": "mondo della cattura del moto: x = X, z = Y (metri), quota = Z; posizione del casco (testa)",
        "persone": persone, "corpi_senza_dati": [c for c in corpi if c.startswith("Helmet") and c not in persone],
        "punti_fermi": fermi, "intestazione_originale": {k: v for k, v in hdr.items() if k not in ("Frame", "BODY_NAMES")},
        "trasformazione": "metri = millimetri / 1000; (0,0,0) -> NaN (corpo perso dalla cattura)",
        "verita": "posizioni vere a 100 Hz; nessuna annotazione di occlusione (i tratti nascosti vanno creati togliendo "
                  "misure, per esempio con un ostacolo virtuale fra un punto di vista scelto e la persona)",
    }
    comune.salva_json(os.path.join(dest, "meta.json"), meta)
    val = np.isfinite(xy[:, :, 0])
    v = np.hypot(*np.moveaxis(np.diff(xy, axis=0), 2, 0)) * freq
    vm = v[np.isfinite(v) & (v > 0.2)]
    print(f"{nome}: {len(t)} istanti a {freq:.0f} Hz, {len(persone)} persone con dati; quota di istanti tracciati per persona: "
          f"min {val.mean(0).min():.3f}, mediana {np.median(val.mean(0)):.3f}, max {val.mean(0).max():.3f}; "
          f"velocità mediana sopra 0,2 m/s: {np.median(vm):.2f} m/s; punti fermi: {list(fermi)}")


if __name__ == "__main__":
    main()
