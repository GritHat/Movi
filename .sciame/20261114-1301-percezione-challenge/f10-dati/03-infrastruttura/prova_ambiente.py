"""Prova che l'ambiente f10 funziona. Si lancia con:
    f10-dati/ambiente/venv/bin/python -I prova_ambiente.py
Esce con 0 se tutte le prove passano. Non scrive file fuori dalla memoria e da una cartella temporanea."""
import io
import os
import sys
import tempfile
import time

import numpy as np

esiti = []


def prova(nome, ok, dettaglio):
    esiti.append(ok)
    print(f"[{'OK' if ok else 'FALLITA'}] {nome}: {dettaglio}")


print("interprete:", sys.executable)
print("python:", sys.version.split()[0], "| numpy:", np.__version__, "| processori:", os.cpu_count())

# 1. numpy: sistema lineare 500x500 (soglia scritta in PREVISIONI.md, infra-P3: residuo relativo < 1e-9)
g = np.random.default_rng(20261114)
a = g.standard_normal((500, 500)) + 500 * np.eye(500)
b = g.standard_normal(500)
x = np.linalg.solve(a, b)
residuo = float(np.linalg.norm(a @ x - b) / np.linalg.norm(b))
prova("numpy, sistema lineare 500x500", residuo < 1e-9, f"residuo relativo {residuo:.2e}")

# 2. numpy: prodotto 1000x1000 (soglia infra-P3: < 1 s), migliore di 3
m1 = g.standard_normal((1000, 1000))
m2 = g.standard_normal((1000, 1000))
tempi = []
for _ in range(3):
    t0 = time.perf_counter()
    m1 @ m2
    tempi.append(time.perf_counter() - t0)
prova("numpy, prodotto 1000x1000", min(tempi) < 1.0, f"migliore di 3: {min(tempi) * 1000:.1f} ms")

# 3. numpy: andata e ritorno di una profondità uint16 su file .npy senza pickle
prof = g.integers(0, 4000, size=(480, 640), dtype=np.uint16)
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "000000.npy")
    np.save(p, prof, allow_pickle=False)
    letta = np.load(p, allow_pickle=False)
prova("numpy, .npy uint16 andata e ritorno", letta.dtype == np.uint16 and np.array_equal(letta, prof),
      f"{letta.shape} {letta.dtype}")

# 4. scipy
import scipy
from scipy import ndimage
etichette, n = ndimage.label(np.array([[1, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 1]]))
prova("scipy.ndimage.label", n == 2, f"scipy {scipy.__version__}, componenti trovate: {n} (attese 2)")

# 5. opencv: PNG a 16 bit in memoria (è il formato della profondità in molti insiemi di dati pubblici)
import cv2
ok, buf = cv2.imencode(".png", prof)
dec = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)
prova("opencv, PNG a 16 bit andata e ritorno", bool(ok) and dec.dtype == np.uint16 and np.array_equal(dec, prof),
      f"opencv {cv2.__version__}, {len(buf)} byte")

# 6. pillow: lo stesso PNG letto da un'altra libreria (controllo incrociato: codice diverso da opencv)
import PIL
from PIL import Image
im = np.array(Image.open(io.BytesIO(buf.tobytes())))
prova("pillow, legge il PNG a 16 bit scritto da opencv", np.array_equal(im.astype(np.uint16), prof),
      f"pillow {PIL.__version__}, modo letto come {im.dtype}")

# 7. rosbags: scrive e rilegge una registrazione ROS1 minima con un'immagine di profondità 16UC1
from importlib.metadata import version
from pathlib import Path
from rosbags.highlevel import AnyReader
from rosbags.rosbag1 import Writer
from rosbags.typesys import Stores, get_typestore

ts = get_typestore(Stores.ROS1_NOETIC)
Immagine = ts.types["sensor_msgs/msg/Image"]
Intestazione = ts.types["std_msgs/msg/Header"]
Tempo = ts.types["builtin_interfaces/msg/Time"]
piccola = prof[:4, :6].copy()
with tempfile.TemporaryDirectory() as d:
    bag = Path(d) / "prova.bag"
    with Writer(bag) as w:
        c = w.add_connection("/camera/depth/image_raw", Immagine.__msgtype__, typestore=ts)
        msg = Immagine(header=Intestazione(seq=0, stamp=Tempo(sec=1, nanosec=500), frame_id="cam"),
                       height=4, width=6, encoding="16UC1", is_bigendian=0, step=12,
                       data=np.frombuffer(piccola.tobytes(), dtype=np.uint8))
        w.write(c, 1_000_000_500, ts.serialize_ros1(msg, Immagine.__msgtype__))
    with AnyReader([bag], default_typestore=ts) as r:
        lette = [(conn.topic, t, r.deserialize(raw, conn.msgtype)) for conn, t, raw in r.messages()]
argomento, t_ns, m = lette[0]
riletta = np.frombuffer(m.data, dtype=np.uint16).reshape(m.height, m.width)
prova("rosbags, .bag ROS1 con immagine 16UC1 andata e ritorno",
      len(lette) == 1 and t_ns == 1_000_000_500 and m.encoding == "16UC1" and np.array_equal(riletta, piccola),
      f"rosbags {version('rosbags')}, argomento {argomento}, {m.width}x{m.height}")

print(f"ESITO: {sum(esiti)}/{len(esiti)} prove passate")
sys.exit(0 if all(esiti) else 1)
