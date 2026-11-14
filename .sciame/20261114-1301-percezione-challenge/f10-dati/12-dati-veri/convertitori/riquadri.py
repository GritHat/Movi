"""Dalla verità «a riquadri» (insiemi per il tracciamento di un bersaglio) al verita.json del formato comune.

Questi insiemi NON danno la posizione metrica del bersaglio: danno un riquadro nell'immagine. Il formato comune vuole
x e z in metri: qui sono DERIVATI dalla stessa profondità che si vuole valutare (mediana dei pixel validi nella metà
centrale del riquadro, riportata nel riferimento della camera: x = (u − cx)·Z/fx, z = Z). Non sono una verità
indipendente: servono per sapere dove guardare, non per misurare un errore metrico. Nei fotogrammi in cui il bersaglio
è nascosto (riquadro assente) x e z ripetono l'ultimo valore visibile e portano "posizione": "ultima_visibile".
"""
import numpy as np


def posizione_da_riquadro(prof_mm, riq, fx, cx):
    """riq = (x0, y0, x1, y1) in pixel a base 0, estremi esclusi a destra e in basso. Restituisce (x, z, quota_validi)."""
    x0, y0, x1, y1 = riq
    h, w = prof_mm.shape
    cxr, cyr, lw, lh = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 4, (y1 - y0) / 4
    a, b = int(max(0, round(cyr - lh))), int(min(h, round(cyr + lh) + 1))
    c, d = int(max(0, round(cxr - lw))), int(min(w, round(cxr + lw) + 1))
    r = prof_mm[a:b, c:d]
    v = r[r > 0]
    if v.size == 0:
        return None
    z = float(np.median(v)) / 1000.0
    return (cxr - cx) * z / fx, z, v.size / max(r.size, 1)


def verita_da_riquadri(leggi_prof, annot, fx, cx, ident, extra=None):
    """annot: lista di (indice, riquadro | None, campi_in_più). Restituisce il dizionario di verita.json e i conteggi."""
    fot, ultimo, in_attesa, senza_prof = [], None, [], 0
    for indice, riq, campi in annot:
        s = {"id": ident}
        if riq is not None:
            p = posizione_da_riquadro(leggi_prof(indice), riq, fx, cx)
            if p is None:
                senza_prof += 1
                if ultimo is None:
                    in_attesa.append((indice, riq, campi)); continue
                s.update(x=ultimo[0], z=ultimo[1], visibile=True, posizione="ultima_visibile (nessun pixel valido nel riquadro)")
            else:
                ultimo = (round(p[0], 4), round(p[1], 4))
                s.update(x=ultimo[0], z=ultimo[1], visibile=True, posizione="derivata_dalla_profondita",
                         quota_validi_nel_centro=round(p[2], 3))
            s["riquadro_px"] = [round(float(v), 1) for v in riq]
        else:
            if ultimo is None:
                in_attesa.append((indice, riq, campi)); continue
            s.update(x=ultimo[0], z=ultimo[1], visibile=False, posizione="ultima_visibile")
        s.update(campi or {})
        fot.append({"indice": indice, "soggetti": [s]})
    v = {"fotogrammi": fot,
         "nota": "x e z NON sono verità indipendente: derivati dalla profondità dentro il riquadro annotato (vedi riquadri.py); "
                 "riferimento della camera (posa ignota), non del suolo. La verità dell'insieme è solo «riquadro_px» e la visibilità."}
    if extra:
        v.update(extra)
    return v, {"saltati_all_inizio": len(in_attesa), "riquadri_senza_profondita": senza_prof}
