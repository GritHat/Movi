#!/usr/bin/env python3
"""registra_sequenza.py -- registra, converte e controlla una sequenza nel FORMATO COMUNE dello sciame.

Formato comune (una cartella per sequenza):
  meta.json          larghezza, altezza, fx, fy, cx, cy (pixel); fps; sensore; posa (altezza in metri e
                     inclinazione in gradi verso il basso, oppure null); origine; licenza
  tempi.csv          una riga per fotogramma: indice,tempo in secondi (dal primo fotogramma)
  profondita/        000000.npy, 000001.npy, ...  matrice numpy uint16, profondita' lungo l'asse ottico
                     in MILLIMETRI, 0 = nessun dato

Comandi:
  registra    --sorgente realsense|oak|orbbec --uscita CARTELLA --durata SECONDI [...]
  converti-stray  CARTELLA_STRAY --uscita CARTELLA      (iPhone/iPad con LiDAR, app Stray Scanner)
  sintetica   --uscita CARTELLA                         (nessun hardware: serve a provare lo script)
  controlla   CARTELLA                                  (conformita' al formato; codice d'uscita 0 o 1)
  riassunto   CARTELLA                                  (fotogrammi, fps veri, pixel validi, distanza al centro)
  impacchetta CARTELLA                                  (CARTELLA.tar.gz per la spedizione)

Dipendenze: numpy sempre; per `registra` il pacchetto del sensore (pyrealsense2, depthai, pyorbbecsdk2);
per `converti-stray` Pillow oppure opencv. Niente altro.

STATO DELLE PROVE (14 novembre 2026): `sintetica`, `controlla`, `riassunto`, `impacchetta` e `converti-stray`
sono stati eseguiti (il convertitore solo su una cartella finta costruita secondo la documentazione dell'app).
I tre rami di `registra` NON sono mai stati eseguiti con un dispositivo collegato: e' verificato solo che
ogni funzione chiamata esiste nei pacchetti pyrealsense2 2.59.1, depthai 3.12.1, pyorbbecsdk2 2.1.3.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import tarfile
import time

import numpy as np

# I nomi delle chiavi stanno qui e solo qui: se la catena ne usa altri, si cambia questa tabella.
K_LARGHEZZA, K_ALTEZZA, K_FPS, K_SENSORE = "larghezza", "altezza", "fps", "sensore"
K_POSA, K_POSA_ALTEZZA, K_POSA_INCLINAZIONE = "posa", "altezza_m", "inclinazione_gradi"
K_ORIGINE, K_LICENZA, K_EXTRA = "origine", "licenza", "extra"
CHIAVI_OBBLIGATORIE = (K_LARGHEZZA, K_ALTEZZA, "fx", "fy", "cx", "cy", K_FPS, K_SENSORE, K_POSA,
                       K_ORIGINE, K_LICENZA)
INTESTAZIONE_TEMPI = ("indice", "tempo_s")
CARTELLA_PROFONDITA = "profondita"


# --------------------------------------------------------------------------------------------------
# Scrittura
# --------------------------------------------------------------------------------------------------
class Scrittore:
    """Scrive i fotogrammi man mano che arrivano; meta.json e tempi.csv alla chiusura."""

    def __init__(self, cartella: str, intestazione: bool = True):
        if os.path.exists(cartella) and os.listdir(cartella):
            raise SystemExit(f"La cartella {cartella} esiste e non e' vuota: scegline una nuova.")
        self.cartella = cartella
        self.intestazione = intestazione
        os.makedirs(os.path.join(cartella, CARTELLA_PROFONDITA), exist_ok=True)
        self.tempi: list[float] = []
        self.forma: tuple[int, int] | None = None

    def aggiungi(self, profondita_mm: np.ndarray, tempo_s: float) -> None:
        a = np.asarray(profondita_mm)
        if a.dtype != np.uint16:
            raise TypeError(f"profondita' di tipo {a.dtype}: deve essere uint16 in millimetri")
        if a.ndim != 2:
            raise ValueError(f"profondita' con forma {a.shape}: deve essere una matrice altezza x larghezza")
        if self.forma is None:
            self.forma = a.shape
        elif a.shape != self.forma:
            raise ValueError(f"fotogramma {len(self.tempi)} con forma {a.shape}, attesa {self.forma}")
        nome = os.path.join(self.cartella, CARTELLA_PROFONDITA, f"{len(self.tempi):06d}.npy")
        np.save(nome, np.ascontiguousarray(a), allow_pickle=False)
        self.tempi.append(float(tempo_s))

    def chiudi(self, *, fx, fy, cx, cy, fps, sensore, posa, origine, licenza, extra=None) -> None:
        if self.forma is None:
            raise SystemExit("Nessun fotogramma ricevuto: niente da salvare.")
        t0 = self.tempi[0]
        with open(os.path.join(self.cartella, "tempi.csv"), "w", newline="") as f:
            w = csv.writer(f)
            if self.intestazione:
                w.writerow(INTESTAZIONE_TEMPI)
            for i, t in enumerate(self.tempi):
                w.writerow((i, f"{t - t0:.6f}"))
        meta = {
            K_LARGHEZZA: int(self.forma[1]), K_ALTEZZA: int(self.forma[0]),
            "fx": float(fx), "fy": float(fy), "cx": float(cx), "cy": float(cy),
            K_FPS: float(fps), K_SENSORE: str(sensore), K_POSA: posa,
            K_ORIGINE: str(origine), K_LICENZA: str(licenza),
        }
        if extra:
            meta[K_EXTRA] = extra
        with open(os.path.join(self.cartella, "meta.json"), "w") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
            f.write("\n")


def posa_da_argomenti(args) -> dict | None:
    if args.altezza_camera is None or args.inclinazione is None:
        return None
    return {K_POSA_ALTEZZA: float(args.altezza_camera), K_POSA_INCLINAZIONE: float(args.inclinazione)}


def in_millimetri(grezzo: np.ndarray, mm_per_unita: float) -> np.ndarray:
    """Porta la profondita' grezza del sensore a uint16 in millimetri (0 resta 0)."""
    if abs(mm_per_unita - 1.0) < 1e-9:
        return np.ascontiguousarray(grezzo, dtype=np.uint16)
    mm = np.rint(grezzo.astype(np.float64) * mm_per_unita)
    mm[(mm < 0) | (mm > 65535)] = 0
    return mm.astype(np.uint16)


# --------------------------------------------------------------------------------------------------
# Sorgenti vere (mai provate con un dispositivo: vedi l'intestazione)
# --------------------------------------------------------------------------------------------------
def registra_realsense(args, scr: Scrittore) -> dict:
    import pyrealsense2 as rs  # pip install pyrealsense2   (L515/SR300: pyrealsense2==2.54.2.5684, Python <= 3.11)

    pipe, cfg = rs.pipeline(), rs.config()
    cfg.enable_stream(rs.stream.depth, args.larghezza, args.altezza, rs.format.z16, args.fps)
    prof = pipe.start(cfg)
    try:
        dev = prof.get_device()
        mm_per_unita = dev.first_depth_sensor().get_depth_scale() * 1000.0  # metri per unita' -> mm
        intr = prof.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()
        nome = f"{dev.get_info(rs.camera_info.name)} (fw {dev.get_info(rs.camera_info.firmware_version)})"
        try:
            usb = dev.get_info(rs.camera_info.usb_type_descriptor)
        except Exception:
            usb = "ignoto"
        print(f"Sensore: {nome}; USB {usb}; {intr.width}x{intr.height}; {mm_per_unita:.4f} mm per unita'")
        for _ in range(args.scarta):  # l'esposizione automatica si assesta
            pipe.wait_for_frames(5000)
        primo_numero, ultimo_numero, t_inizio = None, None, time.monotonic()
        while time.monotonic() - t_inizio < args.durata:
            d = pipe.wait_for_frames(5000).get_depth_frame()
            if not d:
                continue
            scr.aggiungi(in_millimetri(np.asanyarray(d.get_data()), mm_per_unita), d.get_timestamp() / 1000.0)
            n = d.get_frame_number()
            primo_numero = n if primo_numero is None else primo_numero
            ultimo_numero = n
        persi = (ultimo_numero - primo_numero + 1) - len(scr.tempi) if primo_numero is not None else None
    finally:
        pipe.stop()
    return dict(fx=intr.fx, fy=intr.fy, cx=intr.ppx, cy=intr.ppy, sensore=nome,
                extra={"usb": usb, "fotogrammi_persi": persi, "mm_per_unita": mm_per_unita})


def registra_oak(args, scr: Scrittore) -> dict:
    import depthai as dai  # pip install depthai   (versione 3.x)

    pipeline = dai.Pipeline()
    sinistra = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_B)
    destra = pipeline.create(dai.node.Camera).build(dai.CameraBoardSocket.CAM_C)
    stereo = pipeline.create(dai.node.StereoDepth)
    sinistra.requestOutput((args.larghezza, args.altezza), fps=args.fps).link(stereo.left)
    destra.requestOutput((args.larghezza, args.altezza), fps=args.fps).link(stereo.right)
    stereo.setRectification(True)
    stereo.setLeftRightCheck(True)
    stereo.setSubpixel(True)
    coda = stereo.depth.createOutputQueue()
    with pipeline:
        pipeline.start()
        dispositivo = pipeline.getDefaultDevice()
        nome = f"OAK {dispositivo.getDeviceName()}"
        # Intrinseche della camera destra alla risoluzione chiesta: la profondita' e' sull'immagine
        # RETTIFICATA, le cui intrinseche possono differire di qualche pixel. Non verificato.
        k = dispositivo.readCalibration().getCameraIntrinsics(dai.CameraBoardSocket.CAM_C,
                                                              args.larghezza, args.altezza)
        print(f"Sensore: {nome}; USB {dispositivo.getUsbSpeed()}")
        for _ in range(args.scarta):
            coda.get()
        t_inizio = time.monotonic()
        while pipeline.isRunning() and time.monotonic() - t_inizio < args.durata:
            f = coda.get()
            scr.aggiungi(np.ascontiguousarray(f.getFrame(), dtype=np.uint16), f.getTimestamp().total_seconds())
        pipeline.stop()
    return dict(fx=k[0][0], fy=k[1][1], cx=k[0][2], cy=k[1][2], sensore=nome,
                extra={"intrinseche": "camera destra non rettificata, valore approssimato"})


def registra_orbbec(args, scr: Scrittore) -> dict:
    import pyorbbecsdk as ob  # pip install pyorbbecsdk2   (Femto, Gemini 2 / 33x, Astra 2, Astra Mini Pro con fw 2.x)

    pipe, cfg = ob.Pipeline(), ob.Config()
    elenco = pipe.get_stream_profile_list(ob.OBSensorType.DEPTH_SENSOR)
    try:
        prof = elenco.get_video_stream_profile(args.larghezza, args.altezza, ob.OBFormat.Y16, args.fps)
    except ob.OBError:
        prof = elenco.get_default_video_stream_profile()
        print(f"Profilo chiesto non disponibile: uso il predefinito {prof.get_width()}x{prof.get_height()} "
              f"a {prof.get_fps()} fps")
    cfg.enable_stream(prof)
    intr = prof.get_intrinsic()
    pipe.start(cfg)
    try:
        info = pipe.get_device().get_device_info()
        nome = f"{info.get_name()} (fw {info.get_firmware_version()})"
        print(f"Sensore: {nome}; {prof.get_width()}x{prof.get_height()}")
        scartati, t_inizio = 0, None
        while True:
            frames = pipe.wait_for_frames(1000)
            d = frames.get_depth_frame() if frames is not None else None
            if d is None:
                continue
            if scartati < args.scarta:
                scartati += 1
                continue
            t_inizio = time.monotonic() if t_inizio is None else t_inizio
            if time.monotonic() - t_inizio >= args.durata:
                break
            grezzo = np.frombuffer(d.get_data(), dtype=np.uint16).reshape(d.get_height(), d.get_width())
            scr.aggiungi(in_millimetri(grezzo, float(d.get_depth_scale())), d.get_timestamp_us() / 1e6)
    finally:
        pipe.stop()
    return dict(fx=intr.fx, fy=intr.fy, cx=intr.cx, cy=intr.cy, sensore=nome, extra=None)


SORGENTI = {"realsense": registra_realsense, "oak": registra_oak, "orbbec": registra_orbbec}


def comando_registra(args) -> int:
    scr = Scrittore(args.uscita, intestazione=not args.senza_intestazione)
    print(f"Registro {args.durata:.0f} s da «{args.sorgente}» in {args.uscita} ... (Ctrl+C per fermare prima)")
    try:
        dati = SORGENTI[args.sorgente](args, scr)
    except KeyboardInterrupt:
        raise SystemExit("Interrotto prima della fine: la cartella e' incompleta, cancellala e riprova.")
    extra = dict(dati.pop("extra") or {})
    extra.update({"ora_inizio": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "scena": args.scena or ""})
    scr.chiudi(fps=args.fps, posa=posa_da_argomenti(args), origine=args.origine, licenza=args.licenza,
               extra=extra, **dati)
    return comando_riassunto(argparse.Namespace(cartella=args.uscita)) or comando_controlla(
        argparse.Namespace(cartella=args.uscita))


# --------------------------------------------------------------------------------------------------
# iPhone / iPad con LiDAR: conversione di una registrazione dell'app Stray Scanner
# (formato: https://github.com/strayrobots/scanner/blob/main/docs/format.md)
# --------------------------------------------------------------------------------------------------
def leggi_png16(percorso: str) -> np.ndarray:
    try:
        from PIL import Image
        with Image.open(percorso) as im:
            a = np.array(im)
    except ImportError:
        import cv2
        a = cv2.imread(percorso, -1)
        if a is None:
            raise ValueError(f"PNG illeggibile: {percorso}")
    if a.ndim != 2 or a.dtype.kind not in "ui" or a.max(initial=0) > 65535 or a.min(initial=0) < 0:
        raise ValueError(f"{percorso}: attesa un'immagine a un canale a 16 bit, trovata {a.dtype} {a.shape}")
    return a.astype(np.uint16)


def comando_converti_stray(args) -> int:
    src = args.cartella
    righe = list(csv.DictReader(open(os.path.join(src, "odometry.csv"), newline=""), skipinitialspace=True))
    if not righe:
        raise SystemExit("odometry.csv vuoto")
    scr = Scrittore(args.uscita, intestazione=not args.senza_intestazione)
    usati, kx = [], []
    for r in righe:
        nome = r["frame"].strip()
        p = os.path.join(src, "depth", f"{nome}.png")
        if not os.path.exists(p):
            continue
        d = leggi_png16(p)
        if args.confidenza_minima > 0:
            c = leggi_png16(os.path.join(src, "confidence", f"{nome}.png"))
            d = np.where(c >= args.confidenza_minima, d, 0).astype(np.uint16)
        scr.aggiungi(d, float(r["timestamp"]))
        usati.append(r)
        kx.append([float(r[k]) for k in ("fx", "fy", "cx", "cy")])
    if not usati:
        raise SystemExit("nessuna immagine di profondita' trovata in depth/")
    fx, fy, cx, cy = np.median(np.array(kx), axis=0)
    h, w = scr.forma
    # Le intrinseche dell'app sono riferite all'immagine a colori: si riportano alla matrice di profondita'.
    larghezza_rgb = args.larghezza_rgb
    if not 0.35 * larghezza_rgb < cx < 0.65 * larghezza_rgb:
        raise SystemExit(f"cx = {cx:.1f} non sta al centro di un'immagine larga {larghezza_rgb}: "
                         "indica la larghezza vera del video con --larghezza-rgb")
    s = w / larghezza_rgb
    dt = np.diff([float(r["timestamp"]) for r in usati])
    fps = float(1.0 / np.median(dt)) if len(dt) else 0.0
    scr.chiudi(fx=fx * s, fy=fy * s, cx=cx * s, cy=cy * s, fps=round(fps, 3),
               sensore=args.sensore, posa=posa_da_argomenti(args), origine=args.origine, licenza=args.licenza,
               extra={"convertito_da": "Stray Scanner", "larghezza_rgb_assunta": larghezza_rgb,
                      "confidenza_minima": args.confidenza_minima, "scena": args.scena or ""})
    return comando_riassunto(argparse.Namespace(cartella=args.uscita)) or comando_controlla(
        argparse.Namespace(cartella=args.uscita))


# --------------------------------------------------------------------------------------------------
# Sequenza sintetica (prova dello script senza hardware) -- NON e' il simulatore dello sciame
# --------------------------------------------------------------------------------------------------
def comando_sintetica(args) -> int:
    w, h, fps, n = 640, 480, 15.0, args.fotogrammi
    fx = fy = 0.5 * w / np.tan(np.radians(87.0 / 2))  # campo orizzontale di 87 gradi (D435i/D455)
    cx, cy = (w - 1) / 2, (h - 1) / 2
    alt, incl = 1.2, np.radians(15.0)
    v = (np.arange(h) - cy) / fy
    # Pavimento piano visto da 1,2 m con 15 gradi d'inclinazione, parete di fondo a 3 m lungo l'asse.
    den = np.sin(incl) + v * np.cos(incl)
    z_suolo = np.where(den > 1e-6, alt / np.maximum(den, 1e-6), np.inf)
    z = np.minimum(z_suolo, 3.0)[:, None] * np.ones((1, w))
    gen = np.random.default_rng(20261114)
    scr = Scrittore(args.uscita, intestazione=not args.senza_intestazione)
    for i in range(n):
        zi = z.copy()
        c0 = int(100 + (w - 260) * i / max(n - 1, 1))  # una «persona» larga 60 colonne che attraversa a 2 m
        zi[60:, c0:c0 + 60] = np.minimum(zi[60:, c0:c0 + 60], 2.0)
        zi = zi + gen.normal(0.0, 0.004 * zi ** 2)  # rumore che cresce con il quadrato della distanza
        mm = np.clip(np.rint(zi * 1000), 0, 65535).astype(np.uint16)
        mm[gen.random((h, w)) < 0.03] = 0  # 3 % di buchi
        scr.aggiungi(mm, i / fps)
    scr.chiudi(fx=fx, fy=fy, cx=cx, cy=cy, fps=fps, sensore="sintetica (prova dello script)",
               posa={K_POSA_ALTEZZA: alt, K_POSA_INCLINAZIONE: 15.0},
               origine="generata da registra_sequenza.py", licenza="nessun vincolo")
    return comando_controlla(argparse.Namespace(cartella=args.uscita))


# --------------------------------------------------------------------------------------------------
# Controllo, riassunto, pacco
# --------------------------------------------------------------------------------------------------
def leggi_tempi(cartella: str) -> list[tuple[int, float]]:
    out = []
    with open(os.path.join(cartella, "tempi.csv"), newline="") as f:
        for riga in csv.reader(f):
            if not riga:
                continue
            try:
                out.append((int(riga[0]), float(riga[1])))
            except ValueError:
                if out:  # una riga non numerica dopo la prima e' un errore, non un'intestazione
                    raise
    return out


def difetti(cartella: str) -> list[str]:
    err: list[str] = []
    try:
        meta = json.load(open(os.path.join(cartella, "meta.json")))
    except Exception as e:
        return [f"meta.json illeggibile: {e}"]
    for k in CHIAVI_OBBLIGATORIE:
        if k not in meta:
            err.append(f"meta.json: manca la chiave «{k}»")
    for k in (K_LARGHEZZA, K_ALTEZZA, "fx", "fy", K_FPS):
        if k in meta and not (isinstance(meta[k], (int, float)) and meta[k] > 0):
            err.append(f"meta.json: «{k}» deve essere un numero positivo")
    posa = meta.get(K_POSA)
    if posa is not None and not (isinstance(posa, dict) and K_POSA_ALTEZZA in posa and K_POSA_INCLINAZIONE in posa):
        err.append("meta.json: «posa» deve essere null oppure avere altezza e inclinazione")
    try:
        tempi = leggi_tempi(cartella)
    except Exception as e:
        return err + [f"tempi.csv illeggibile: {e}"]
    if not tempi:
        err.append("tempi.csv: nessun fotogramma")
    if [i for i, _ in tempi] != list(range(len(tempi))):
        err.append("tempi.csv: gli indici non sono 0, 1, 2, ...")
    t = np.array([x for _, x in tempi])
    if len(t) > 1 and not np.all(np.diff(t) > 0):
        err.append("tempi.csv: i tempi non sono strettamente crescenti")
    cart = os.path.join(cartella, CARTELLA_PROFONDITA)
    nomi = sorted(os.listdir(cart)) if os.path.isdir(cart) else []
    if nomi != [f"{i:06d}.npy" for i in range(len(tempi))]:
        err.append(f"profondita/: {len(nomi)} file, attesi {len(tempi)} con nomi 000000.npy, 000001.npy, ...")
    for nome in nomi:
        try:
            a = np.load(os.path.join(cart, nome), allow_pickle=False, mmap_mode="r")
        except Exception as e:
            err.append(f"{nome}: illeggibile ({e})")
            break
        if a.dtype != np.uint16:
            err.append(f"{nome}: tipo {a.dtype}, atteso uint16 (millimetri)")
            break
        if a.shape != (meta.get(K_ALTEZZA), meta.get(K_LARGHEZZA)):
            err.append(f"{nome}: forma {a.shape}, attesa ({meta.get(K_ALTEZZA)}, {meta.get(K_LARGHEZZA)})")
            break
    return err


def comando_controlla(args) -> int:
    err = difetti(args.cartella)
    if err:
        print(f"NON CONFORME: {args.cartella}")
        for e in err:
            print("  -", e)
        return 1
    print(f"conforme: {args.cartella}")
    return 0


def comando_riassunto(args) -> int:
    meta = json.load(open(os.path.join(args.cartella, "meta.json")))
    tempi = leggi_tempi(args.cartella)
    t = np.array([x for _, x in tempi])
    n = len(t)
    cart = os.path.join(args.cartella, CARTELLA_PROFONDITA)
    campione = sorted(set(np.linspace(0, n - 1, min(n, 30)).astype(int)))
    validi, centro = [], []
    for i in campione:
        a = np.load(os.path.join(cart, f"{i:06d}.npy"), allow_pickle=False)
        validi.append(float(np.count_nonzero(a)) / a.size)
        h, w = a.shape
        q = a[h // 2 - h // 20:h // 2 + h // 20 + 1, w // 2 - w // 20:w // 2 + w // 20 + 1]
        q = q[q > 0]
        centro.append(float(np.median(q)) if q.size else float("nan"))
    durata = float(t[-1] - t[0]) if n > 1 else 0.0
    dt = np.diff(t)
    peso = sum(os.path.getsize(os.path.join(cart, f)) for f in os.listdir(cart)) / 1e6
    print(f"{args.cartella}: {meta[K_SENSORE]}, {meta[K_LARGHEZZA]}x{meta[K_ALTEZZA]}, {n} fotogrammi in "
          f"{durata:.2f} s")
    if n > 1:
        print(f"  fps veri {(n - 1) / durata:.2f} (dichiarati {meta[K_FPS]}); intervallo massimo "
              f"{dt.max() * 1000:.0f} ms; {peso:.0f} MB su disco")
    print(f"  pixel validi: mediana {100 * np.median(validi):.1f} %, minimo {100 * np.min(validi):.1f} %")
    if np.isfinite(centro).any():
        print(f"  distanza al centro dell'immagine: mediana {np.nanmedian(centro):.0f} mm "
              f"(da {np.nanmin(centro):.0f} a {np.nanmax(centro):.0f}) -- confrontala con il metro")
    else:
        print("  distanza al centro: nessun dato valido")
    return 0


def comando_impacchetta(args) -> int:
    cartella = args.cartella.rstrip("/")
    if comando_controlla(argparse.Namespace(cartella=cartella)):
        return 1
    uscita = cartella + ".tar.gz"
    t0 = time.monotonic()
    with tarfile.open(uscita, "w:gz", compresslevel=args.livello) as tar:
        tar.add(cartella, arcname=os.path.basename(cartella))
    grezzo = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(cartella) for f in fs)
    print(f"{uscita}: {os.path.getsize(uscita) / 1e6:.1f} MB (da {grezzo / 1e6:.1f} MB) in "
          f"{time.monotonic() - t0:.1f} s")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="comando", required=True)

    def comuni(q):
        q.add_argument("--uscita", required=True, help="cartella nuova della sequenza")
        q.add_argument("--altezza-camera", type=float, default=None, help="altezza dell'ottica da terra, in metri")
        q.add_argument("--inclinazione", type=float, default=None, help="gradi verso il basso (0 = orizzontale)")
        q.add_argument("--scena", default="", help="nota libera, per esempio «parete a 2,00 m»")
        q.add_argument("--origine", default="registrazione propria della squadra")
        q.add_argument("--licenza", default="uso interno della squadra")
        q.add_argument("--senza-intestazione", action="store_true", help="tempi.csv senza la riga dei nomi")

    r = sub.add_parser("registra")
    r.add_argument("--sorgente", required=True, choices=sorted(SORGENTI))
    r.add_argument("--durata", type=float, required=True, help="secondi")
    r.add_argument("--larghezza", type=int, default=640)
    r.add_argument("--altezza", type=int, default=480)
    r.add_argument("--fps", type=int, default=30)
    r.add_argument("--scarta", type=int, default=30, help="fotogrammi iniziali da buttare")
    comuni(r)
    r.set_defaults(f=comando_registra)

    c = sub.add_parser("converti-stray")
    c.add_argument("cartella")
    c.add_argument("--sensore", default="iPhone/iPad LiDAR (Stray Scanner)")
    c.add_argument("--larghezza-rgb", type=float, default=1920.0)
    c.add_argument("--confidenza-minima", type=int, default=0, choices=(0, 1, 2),
                   help="i pixel con confidenza minore diventano 0 = nessun dato")
    comuni(c)
    c.set_defaults(f=comando_converti_stray)

    s = sub.add_parser("sintetica")
    s.add_argument("--uscita", required=True)
    s.add_argument("--fotogrammi", type=int, default=45)
    s.add_argument("--senza-intestazione", action="store_true")
    s.set_defaults(f=comando_sintetica)

    for nome, f in (("controlla", comando_controlla), ("riassunto", comando_riassunto)):
        q = sub.add_parser(nome)
        q.add_argument("cartella")
        q.set_defaults(f=f)

    i = sub.add_parser("impacchetta")
    i.add_argument("cartella")
    i.add_argument("--livello", type=int, default=3)
    i.set_defaults(f=comando_impacchetta)

    args = p.parse_args()
    return int(args.f(args) or 0)


if __name__ == "__main__":
    sys.exit(main())
