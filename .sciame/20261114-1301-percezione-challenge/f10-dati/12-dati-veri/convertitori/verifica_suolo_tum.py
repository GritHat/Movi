"""Verifica indipendente della posa di TUM: i punti del pavimento, portati nel mondo con la posa COMPLETA della
cattura del moto (rotazione intera, non solo altezza e inclinazione), devono stare a quota 0.
Uso: python -I -B verifica_suolo_tum.py <cartella_aperta_tum> <sequenza_convertita>"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune, numpy as np
from converti_tum import leggi_elenco, rot, FX, FY, CX, CY
aperta, seq = sys.argv[1], sys.argv[2]
gt = np.array([[float(x) for x in r] for r in leggi_elenco(os.path.join(aperta, "groundtruth.txt"))])
indici, tempi = comune.leggi_tempi(seq); meta = comune.leggi_meta(seq)
u, v = np.meshgrid(np.arange(640), np.arange(480))
picchi, larghezze, quote_suolo, sotto = [], [], [], []
for i in indici[::24]:
    z = comune.leggi_profondita(seq, i).astype(np.float64) / 1000
    k = int(np.argmin(np.abs(gt[:, 0] - (tempi[i] + meta["tempo_zero_unix_s"]))))
    R, t = rot(*gt[k, 4:8]), gt[k, 1:4]
    m = z > 0
    P = np.stack([(u[m] - CX) * z[m] / FX, (v[m] - CY) * z[m] / FY, z[m]])
    q = (R @ P)[2] + t[2]                       # quota nel mondo
    h, b = np.histogram(q, bins=np.arange(-0.5, 0.5, 0.01))
    c = b[np.argmax(h)] + 0.005
    vic = q[np.abs(q - c) < 0.10]
    picchi.append(c); larghezze.append(vic.std()); quote_suolo.append((np.abs(q) < 0.05).mean()); sotto.append((q < -0.10).mean())
p = np.array(picchi)
print(f"fotogrammi provati: {len(p)}; quota del picco più popolato fra -0,5 e 0,5 m: mediana {np.median(p)*100:.1f} cm, "
      f"min {p.min()*100:.1f}, max {p.max()*100:.1f}; scarto tipo attorno al picco: mediana {np.median(larghezze)*100:.1f} cm")
print(f"quota di pixel validi entro ±5 cm da quota 0: mediana {np.median(quote_suolo)*100:.1f}%, min {min(quote_suolo)*100:.1f}%; "
      f"pixel sotto -10 cm: mediana {np.median(sotto)*100:.2f}%, max {max(sotto)*100:.2f}%")
