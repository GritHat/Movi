#!/usr/bin/env python3
"""Controlla che una cartella rispetti il formato comune di una sequenza (vedi formato_sequenza.md).

Uso:
    f10-dati/ambiente/venv/bin/python -I controlla_sequenza.py <cartella> [--rigoroso] [--tutti] [--silenzioso]

  --rigoroso    anche gli avvisi fanno fallire il controllo
  --tutti       carica i valori di tutti i fotogrammi (se manca: intestazioni di tutti, valori di 50 al più)
  --silenzioso  stampa solo errori, avvisi ed esito

Codici d'uscita: 0 la cartella rispetta il formato; 1 non lo rispetta; 2 uso sbagliato.

Si può anche importare (gli stessi lettori usati dal controllo, così il formato ha una sola realizzazione):
    import sys; sys.path.insert(0, ".../f10-dati/03-infrastruttura")
    from controlla_sequenza import leggi_meta, leggi_tempi, leggi_profondita, leggi_verita, scrivi_sequenza

I file .npy si leggono SEMPRE con allow_pickle=False: un .npy con oggetti serializzati può eseguire codice.
"""
import csv
import json
import math
import os
import sys

import numpy as np

CHIAVI_META = ("larghezza", "altezza", "fx", "fy", "cx", "cy", "fps", "sensore", "posa", "origine", "licenza")
CHIAVI_POSA = ("altezza_m", "inclinazione_gradi")
INTESTAZIONE_TEMPI = ["indice", "tempo_s"]
NOMI_SBAGLIATI = {"width": "larghezza", "height": "altezza", "w": "larghezza", "h": "altezza",
                  "sensor": "sensore", "nome_sensore": "sensore", "profilo": "sensore", "pose": "posa",
                  "license": "licenza", "source": "origine", "fonte": "origine", "frame_rate": "fps",
                  "altezza_camera": "posa.altezza_m", "inclinazione": "posa.inclinazione_gradi",
                  "altezza_m": "posa.altezza_m", "inclinazione_gradi": "posa.inclinazione_gradi"}
CAMPIONE = 50


class FormatoErrato(Exception):
    pass


def _numero(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _intero(v):
    return isinstance(v, int) and not isinstance(v, bool)


# --------------------------------------------------------------------------------------------- lettori
def leggi_meta(cartella):
    """Restituisce il dizionario di meta.json (senza controlli di merito: quelli li fa controlla())."""
    with open(os.path.join(cartella, "meta.json"), encoding="utf-8") as f:
        meta = json.load(f)
    if not isinstance(meta, dict):
        raise FormatoErrato("meta.json non è un oggetto JSON")
    return meta


def leggi_tempi(cartella):
    """Restituisce (indici, tempi): lista di interi e vettore float64 in secondi. Tollera l'intestazione assente."""
    indici, tempi = [], []
    with open(os.path.join(cartella, "tempi.csv"), encoding="utf-8", newline="") as f:
        for k, riga in enumerate(csv.reader(f)):
            riga = [c.strip() for c in riga]
            if not riga or riga == [""]:
                continue
            if k == 0 and riga == INTESTAZIONE_TEMPI:
                continue
            if len(riga) != 2:
                raise FormatoErrato(f"tempi.csv, riga {k + 1}: attese 2 colonne, trovate {len(riga)}")
            try:
                indici.append(int(riga[0]))
                tempi.append(float(riga[1]))
            except ValueError:
                raise FormatoErrato(f"tempi.csv, riga {k + 1}: valori non numerici {riga!r}") from None
    return indici, np.asarray(tempi, dtype=np.float64)


def percorso_profondita(cartella, indice):
    return os.path.join(cartella, "profondita", f"{indice:06d}.npy")


def leggi_profondita(cartella, indice, mappa=False):
    """Profondità del fotogramma: uint16, millimetri lungo l'asse ottico, 0 = nessun dato. Mai pickle."""
    a = np.load(percorso_profondita(cartella, indice), mmap_mode="r" if mappa else None, allow_pickle=False)
    if a.dtype != np.dtype("<u2") or a.ndim != 2:
        raise FormatoErrato(f"profondita/{indice:06d}.npy: attesa matrice uint16 a 2 dimensioni, "
                            f"trovata {a.dtype} con forma {a.shape}")
    return a


def leggi_verita(cartella):
    """Restituisce il dizionario di verita.json, oppure None se il file non c'è."""
    p = os.path.join(cartella, "verita.json")
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def scrivi_sequenza(cartella, meta, tempi, fotogrammi, verita=None):
    """Scrive una sequenza nel formato comune. `cartella` deve essere nuova o vuota.

    meta: dizionario con le chiavi di CHIAVI_META; tempi: sequenza di secondi (uno per fotogramma);
    fotogrammi: iterabile di matrici uint16 (altezza, larghezza) in millimetri; verita: dizionario o None.
    Non converte niente di nascosto: una matrice che non è uint16 viene rifiutata."""
    if os.path.isdir(cartella) and os.listdir(cartella):
        raise FormatoErrato(f"la cartella esiste e non è vuota: {cartella}")
    os.makedirs(os.path.join(cartella, "profondita"), exist_ok=True)
    n = 0
    for n, f in enumerate(fotogrammi, start=1):
        f = np.asarray(f)
        if f.dtype != np.uint16 or f.shape != (meta["altezza"], meta["larghezza"]):
            raise FormatoErrato(f"fotogramma {n - 1}: atteso uint16 {(meta['altezza'], meta['larghezza'])}, "
                                f"trovato {f.dtype} {f.shape}")
        np.save(percorso_profondita(cartella, n - 1), np.ascontiguousarray(f, dtype="<u2"), allow_pickle=False)
    tempi = [float(t) for t in tempi]
    if len(tempi) != n:
        raise FormatoErrato(f"{n} fotogrammi ma {len(tempi)} tempi")
    with open(os.path.join(cartella, "tempi.csv"), "w", encoding="utf-8", newline="") as f:
        f.write(",".join(INTESTAZIONE_TEMPI) + "\n")
        for i, t in enumerate(tempi):
            f.write(f"{i},{t:.6f}\n")
    with open(os.path.join(cartella, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write("\n")
    if verita is not None:
        with open(os.path.join(cartella, "verita.json"), "w", encoding="utf-8") as f:
            json.dump(verita, f, ensure_ascii=False)
            f.write("\n")


def profondita_del_suolo(meta):
    """Profondità (metri, lungo l'asse ottico) a cui ogni pixel vedrebbe un suolo piano, data la posa.

    Riga v, colonna u; inclinazione t verso il basso; altezza h:  Z = h / (((v - cy) / fy) * cos t + sin t).
    Dove il denominatore non è positivo il pixel guarda sopra l'orizzonte: lì il valore è +inf."""
    h, t = meta["posa"]["altezza_m"], math.radians(meta["posa"]["inclinazione_gradi"])
    v = (np.arange(meta["altezza"], dtype=np.float64) - meta["cy"]) / meta["fy"]
    den = v * math.cos(t) + math.sin(t)
    z = np.where(den > 1e-9, h / np.maximum(den, 1e-9), np.inf)
    return np.repeat(z[:, None], meta["larghezza"], axis=1)


# -------------------------------------------------------------------------------------------- controllo
def controlla(cartella, tutti=False):
    """Restituisce (errori, avvisi, note): tre liste di stringhe. La cartella è valida se errori è vuota."""
    errori, avvisi, note = [], [], []
    if not os.path.isdir(cartella):
        return [f"non è una cartella: {cartella}"], avvisi, note

    # ---- meta.json
    meta = None
    try:
        meta = leggi_meta(cartella)
    except FileNotFoundError:
        errori.append("manca meta.json")
    except (json.JSONDecodeError, UnicodeDecodeError, FormatoErrato) as e:
        errori.append(f"meta.json illeggibile: {e}")
    meta_ok = False
    if meta is not None:
        prima = len(errori)
        for k in CHIAVI_META:
            if k not in meta:
                errori.append(f"meta.json: manca la chiave «{k}»")
        for k in meta:
            if k not in CHIAVI_META:
                if k in NOMI_SBAGLIATI:
                    errori.append(f"meta.json: chiave «{k}» non ammessa: il nome giusto è «{NOMI_SBAGLIATI[k]}»")
                else:
                    note.append(f"meta.json: chiave in più «{k}» (ammessa, ignorata dal controllo)")
        for k in ("larghezza", "altezza"):
            if k in meta and not (_intero(meta[k]) and meta[k] > 0):
                errori.append(f"meta.json: «{k}» deve essere un intero positivo (pixel), trovato {meta[k]!r}")
        for k in ("fx", "fy", "fps"):
            if k in meta and not (_numero(meta[k]) and meta[k] > 0):
                errori.append(f"meta.json: «{k}» deve essere un numero positivo, trovato {meta[k]!r}")
        for k in ("cx", "cy"):
            if k in meta and not _numero(meta[k]):
                errori.append(f"meta.json: «{k}» deve essere un numero (pixel), trovato {meta[k]!r}")
        for k in ("sensore", "origine", "licenza"):
            if k in meta and not (isinstance(meta[k], str) and meta[k].strip()):
                errori.append(f"meta.json: «{k}» deve essere un testo non vuoto, trovato {meta[k]!r}")
        if "posa" in meta and meta["posa"] is not None:
            posa = meta["posa"]
            if not isinstance(posa, dict) or set(posa) != set(CHIAVI_POSA):
                errori.append("meta.json: «posa» deve essere null oppure un oggetto con esattamente le chiavi "
                              f"«altezza_m» e «inclinazione_gradi», trovato {posa!r}")
            else:
                if not (_numero(posa["altezza_m"]) and posa["altezza_m"] > 0):
                    errori.append(f"meta.json: posa.altezza_m deve essere positiva (metri), trovato {posa['altezza_m']!r}")
                elif posa["altezza_m"] > 5:
                    avvisi.append(f"meta.json: posa.altezza_m = {posa['altezza_m']}: più di 5 m, forse non è in metri")
                if not (_numero(posa["inclinazione_gradi"]) and -90 <= posa["inclinazione_gradi"] <= 90):
                    errori.append("meta.json: posa.inclinazione_gradi deve stare fra -90 e 90 (positiva verso il "
                                  f"basso), trovato {posa['inclinazione_gradi']!r}")
        meta_ok = len(errori) == prima
        if meta_ok:
            campo = 2 * math.degrees(math.atan(meta["larghezza"] / (2 * meta["fx"])))
            note.append(f"meta: {meta['larghezza']}x{meta['altezza']} px, {meta['fps']} fps, campo orizzontale "
                        f"{campo:.1f}°, sensore «{meta['sensore']}», posa {meta['posa']}")
            if not 20 <= campo <= 150:
                avvisi.append(f"meta.json: il campo orizzontale ricavato da fx è {campo:.1f}°: fx è in pixel?")
            if not (0 <= meta["cx"] <= meta["larghezza"] and 0 <= meta["cy"] <= meta["altezza"]):
                avvisi.append("meta.json: il centro ottico (cx, cy) cade fuori dall'immagine")

    # ---- tempi.csv
    indici, tempi = None, None
    try:
        with open(os.path.join(cartella, "tempi.csv"), encoding="utf-8") as f:
            prima_riga = [c.strip() for c in f.readline().strip().split(",")]
        indici, tempi = leggi_tempi(cartella)
    except FileNotFoundError:
        errori.append("manca tempi.csv")
    except (FormatoErrato, UnicodeDecodeError) as e:
        errori.append(str(e))
    n = None
    if indici is not None:
        n = len(indici)
        if prima_riga != INTESTAZIONE_TEMPI:
            avvisi.append("tempi.csv: manca l'intestazione «indice,tempo_s» (tollerata dal lettore di riferimento)")
        if n == 0:
            errori.append("tempi.csv: nessun fotogramma")
        elif indici != list(range(n)):
            k = next(i for i, v in enumerate(indici) if v != i)
            errori.append(f"tempi.csv: gli indici devono essere 0, 1, 2, …: alla riga {k + 1} dei dati c'è {indici[k]}")
        if n and not np.all(np.isfinite(tempi)):
            errori.append("tempi.csv: tempi non finiti")
        elif n and n > 1:
            passi = np.diff(tempi)
            if np.any(passi <= 0):
                k = int(np.argmax(passi <= 0))
                errori.append(f"tempi.csv: i tempi devono crescere: fra gli indici {k} e {k + 1} il passo è "
                              f"{passi[k]:.6f} s")
            else:
                mediano = float(np.median(passi))
                note.append(f"tempi: {n} fotogrammi, durata {tempi[-1] - tempi[0]:.3f} s, passo mediano "
                            f"{mediano * 1000:.1f} ms, massimo {float(passi.max()) * 1000:.1f} ms")
                if meta_ok and abs(mediano * meta["fps"] - 1) > 0.2:
                    avvisi.append(f"tempi.csv: il passo mediano ({mediano * 1000:.1f} ms) non corrisponde a fps = "
                                  f"{meta['fps']} (attesi {1000 / meta['fps']:.1f} ms)")
                if float(passi.max()) > 2.5 * mediano:
                    avvisi.append(f"tempi.csv: ci sono salti (passo massimo {float(passi.max()) * 1000:.1f} ms, "
                                  f"{int(np.sum(passi > 2.5 * mediano))} oltre 2,5 volte il mediano)")

    # ---- profondita/
    dir_prof = os.path.join(cartella, "profondita")
    if not os.path.isdir(dir_prof):
        errori.append("manca la cartella profondita/")
    elif n:
        presenti = set(os.listdir(dir_prof))
        attesi = {f"{i:06d}.npy" for i in range(n)}
        mancanti, in_piu = sorted(attesi - presenti), sorted(presenti - attesi)
        if mancanti:
            errori.append(f"profondita/: mancano {len(mancanti)} file su {n} (primo: {mancanti[0]})")
        if in_piu:
            errori.append(f"profondita/: {len(in_piu)} file in più rispetto a tempi.csv (primo: {in_piu[0]})")
        forma_ok = True
        for i in range(n):
            if f"{i:06d}.npy" not in presenti:
                continue
            try:
                a = np.load(percorso_profondita(cartella, i), mmap_mode="r", allow_pickle=False)
            except Exception as e:  # file troncato, non .npy, oggetti serializzati…
                errori.append(f"profondita/{i:06d}.npy illeggibile senza pickle: {type(e).__name__}: {str(e)[:80]}")
                forma_ok = False
                break
            if a.dtype != np.dtype("<u2"):
                errori.append(f"profondita/{i:06d}.npy: il tipo deve essere uint16 (millimetri), trovato {a.dtype}")
                forma_ok = False
                break
            if meta_ok and a.shape != (meta["altezza"], meta["larghezza"]):
                errori.append(f"profondita/{i:06d}.npy: forma {a.shape}, attesa (altezza, larghezza) = "
                              f"{(meta['altezza'], meta['larghezza'])}")
                forma_ok = False
                break
        if forma_ok and not mancanti and meta_ok:
            scelti = list(range(n)) if tutti or n <= CAMPIONE else sorted(
                {int(round(k)) for k in np.linspace(0, n - 1, CAMPIONE)})
            suolo = profondita_del_suolo(meta) if meta["posa"] is not None else None
            zeri, validi, bassi, alti, saturi, sul_suolo, sotto = 0, [], 0, 0, 0, 0, 0
            for i in scelti:
                a = np.asarray(leggi_profondita(cartella, i))
                v = a[a > 0]
                zeri += a.size - v.size
                saturi += int(np.sum(a == 65535))
                if v.size:
                    validi.append(v[:: max(1, v.size // 20000)])
                if suolo is not None and v.size:
                    rapporto = (a.astype(np.float64) / 1000.0)[a > 0] / suolo[a > 0]
                    sul_suolo += int(np.sum(np.abs(rapporto - 1) <= 0.05))
                    sotto += int(np.sum(rapporto > 1.10))
            totale = len(scelti) * meta["altezza"] * meta["larghezza"]
            n_validi = totale - zeri
            come = "tutti" if len(scelti) == n else f"{len(scelti)} su {n}, equispaziati"
            if n_validi == 0:
                avvisi.append(f"profondita/: nei fotogrammi letti ({come}) non c'è nessun dato (tutto 0)")
            else:
                v = np.concatenate(validi)
                q = np.percentile(v, [1, 50, 99])
                note.append(f"profondità ({come}): senza dato {100 * zeri / totale:.1f}%; valori validi: 1° "
                            f"percentile {q[0]:.0f} mm, mediana {q[1]:.0f} mm, 99° {q[2]:.0f} mm, massimo {int(v.max())} mm")
                if q[1] < 50:
                    avvisi.append(f"profondita/: mediana {q[1]:.0f}: valori troppo piccoli per dei millimetri "
                                  "(forse metri, decimetri o centimetri)")
                if q[2] > 20000:
                    avvisi.append(f"profondita/: 99° percentile {q[2]:.0f}: oltre 20 m; forse l'unità non è il "
                                  "millimetro (per esempio 1/5000 di metro, o 0,1 mm)")
                if saturi > 0.001 * totale:
                    avvisi.append(f"profondita/: {100 * saturi / totale:.2f}% dei pixel vale 65535: «nessun dato» "
                                  "si scrive 0, non 65535")
                if suolo is not None:
                    f_suolo, f_sotto = sul_suolo / n_validi, sotto / n_validi
                    note.append(f"confronto con il suolo piano previsto dalla posa (solo descrittivo): "
                                f"{100 * f_suolo:.1f}% dei pixel validi entro ±5%, {100 * f_sotto:.1f}% oltre il "
                                f"suolo di più del 10%")
                    if f_suolo < 0.02:
                        avvisi.append("profondita/: meno del 2% dei pixel validi è compatibile con il suolo previsto "
                                      "dalla posa: controlla altezza, segno dell'inclinazione, unità, e che la "
                                      "profondità sia lungo l'asse ottico (non lungo il raggio)")
                    if f_sotto > 0.05:
                        avvisi.append(f"profondita/: {100 * f_sotto:.1f}% dei pixel validi vede più lontano del "
                                      "suolo previsto dalla posa: posa sbagliata, suolo non piano, o profondità "
                                      "lungo il raggio")

    # ---- verita.json (facoltativo)
    try:
        verita = leggi_verita(cartella)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        verita = None
        errori.append(f"verita.json illeggibile: {e}")
    if verita is not None:
        errori_v = _controlla_verita(verita, n, note, avvisi)
        errori.extend(errori_v[:8])
        if len(errori_v) > 8:
            errori.append(f"verita.json: altri {len(errori_v) - 8} errori non elencati")
    else:
        note.append("verita.json: assente (ammesso: senza verità la misura è solo descrittiva)")
    return errori, avvisi, note


def _controlla_verita(verita, n, note, avvisi):
    e = []
    if not isinstance(verita, dict) or not isinstance(verita.get("fotogrammi"), list):
        return ["verita.json: deve essere un oggetto con la lista «fotogrammi»"]
    precedente, soggetti, nascosti, passaggi, stato = -1, set(), 0, 0, {}
    for k, f in enumerate(verita["fotogrammi"]):
        if not isinstance(f, dict) or not _intero(f.get("indice")) or not isinstance(f.get("soggetti"), list):
            e.append(f"verita.json: fotogrammi[{k}] deve avere «indice» (intero) e «soggetti» (lista)")
            continue
        i = f["indice"]
        if i <= precedente:
            e.append(f"verita.json: gli indici devono crescere: fotogrammi[{k}] ha indice {i} dopo {precedente}")
        if n is not None and not 0 <= i < n:
            e.append(f"verita.json: fotogrammi[{k}] ha indice {i}, che non esiste in tempi.csv (0…{n - 1})")
        precedente = max(precedente, i)
        visti = set()
        for j, s in enumerate(f["soggetti"]):
            dove = f"verita.json: fotogrammi[{k}].soggetti[{j}]"
            if not isinstance(s, dict):
                e.append(f"{dove} deve essere un oggetto")
                continue
            if not (isinstance(s.get("id"), str) and s["id"]):
                e.append(f"{dove}: «id» deve essere un testo non vuoto, trovato {s.get('id')!r}")
                continue
            if s["id"] in visti:
                e.append(f"{dove}: identità «{s['id']}» ripetuta nello stesso fotogramma")
            visti.add(s["id"])
            for c in ("x", "z"):
                if not _numero(s.get(c)):
                    e.append(f"{dove}: «{c}» deve essere un numero finito (metri), trovato {s.get(c)!r}")
            if not isinstance(s.get("visibile"), bool):
                e.append(f"{dove}: «visibile» deve essere true o false, trovato {s.get('visibile')!r}")
                continue
            if "frazione_visibile" in s:
                fr = s["frazione_visibile"]
                if not (_numero(fr) and 0 <= fr <= 1):
                    e.append(f"{dove}: «frazione_visibile» deve stare fra 0 e 1, trovato {fr!r}")
                elif (fr > 0) != s["visibile"]:
                    avvisi.append(f"{dove}: visibile = {s['visibile']} ma frazione_visibile = {fr}")
            soggetti.add(s["id"])
            nascosti += not s["visibile"]
            if stato.get(s["id"]) is True and s["visibile"] is False:
                passaggi += 1
            stato[s["id"]] = s["visibile"]
    ostacoli = verita.get("ostacoli", [])
    if not isinstance(ostacoli, list):
        e.append("verita.json: «ostacoli», se c'è, deve essere una lista")
        ostacoli = []
    for k, o in enumerate(ostacoli):
        dove = f"verita.json: ostacoli[{k}]"
        if not isinstance(o, dict) or not (isinstance(o.get("id"), str) and o["id"]) or "tipo" not in o:
            e.append(f"{dove} deve essere un oggetto con «id» (testo) e «tipo»")
            continue
        if o["tipo"] == "poligono":
            vv = o.get("vertici")
            if not (isinstance(vv, list) and len(vv) >= 3 and all(
                    isinstance(p, list) and len(p) == 2 and _numero(p[0]) and _numero(p[1]) for p in vv)):
                e.append(f"{dove}: un poligono vuole «vertici»: almeno 3 coppie [x, z] in metri")
        elif o["tipo"] == "cerchio":
            if not (_numero(o.get("x")) and _numero(o.get("z")) and _numero(o.get("raggio_m")) and o["raggio_m"] > 0):
                e.append(f"{dove}: un cerchio vuole «x», «z» e «raggio_m» positivo, in metri")
        else:
            avvisi.append(f"{dove}: tipo «{o['tipo']}» non previsto dal formato (previsti: poligono, cerchio)")
        if "altezza_m" in o and not (_numero(o["altezza_m"]) and o["altezza_m"] > 0):
            e.append(f"{dove}: «altezza_m», se c'è, deve essere positiva")
    if not e:
        note.append(f"verità: {len(verita['fotogrammi'])} fotogrammi annotati, {len(soggetti)} soggetti "
                    f"({', '.join(sorted(soggetti)[:6])}), {nascosti} presenze nascoste, {passaggi} passaggi da "
                    f"visibile a nascosto, {len(ostacoli)} ostacoli")
    return e


def main(argv):
    opzioni = {a for a in argv if a.startswith("--")}
    resto = [a for a in argv if not a.startswith("--")]
    if len(resto) != 1 or opzioni - {"--rigoroso", "--tutti", "--silenzioso"}:
        print(__doc__, file=sys.stderr)
        return 2
    errori, avvisi, note = controlla(resto[0], tutti="--tutti" in opzioni)
    if "--silenzioso" not in opzioni:
        for r in note:
            print("nota:", r)
    for r in avvisi:
        print("AVVISO:", r)
    for r in errori:
        print("ERRORE:", r)
    fallita = bool(errori) or ("--rigoroso" in opzioni and bool(avvisi))
    print(f"ESITO: {'NON rispetta' if fallita else 'rispetta'} il formato ({len(errori)} errori, {len(avvisi)} avvisi)"
          f" — {resto[0]}")
    return 1 if fallita else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
