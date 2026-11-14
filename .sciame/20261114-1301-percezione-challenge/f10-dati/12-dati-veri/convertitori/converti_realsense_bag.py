"""File .bag di esempio RealSense (ROS bag 1, registrati da librealsense) -> formato comune di f10.

Uso:  …/ambiente/venv/bin/python -I -B converti_realsense_bag.py <file.bag> <nome_sequenza>

Lettura con la libreria `rosbags` dell'ambiente (puro Python): dal file si leggono solo byte. Si usano:
  - `…/Depth_0/image/data` (sensor_msgs/Image, «mono16» piccolo-endiano): i valori grezzi a 16 bit;
  - `…/Depth_0/info/camera_info` (matrice K e distorsione, come le ha scritte il dispositivo nel file);
  - l'unità di profondità: `…/option/Depth Units/value` (Float32) oppure la proprietà «Depth Units» del sensore;
  - `…/Depth_0/info` (realsense_msgs/StreamInfo): i primi 4 byte sono gli fps nominali (uint32);
  - `/device_0/info`: nome del dispositivo (il numero di serie non viene copiato).
Trasformazione: millimetri = arrotonda(valore × unità × 1000); 65535 grezzo -> 0 (contato); oltre 65534 mm -> 0.
Profondità lungo l'asse ottico: è la convenzione di librealsense (NON verificata oggi sulla documentazione; per
stands_still c'è una verifica empirica in verifica_piano.py). Posa: ignota (null). Verità: nessuna.
"""
import os
import struct
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune  # noqa: E402
import numpy as np  # noqa: E402
from rosbags.rosbag1 import Reader  # noqa: E402
from rosbags.typesys import Stores, get_typestore  # noqa: E402


def main():
    bag, nome = sys.argv[1], sys.argv[2]
    dest = comune.cartella_nuova(nome)
    ts = get_typestore(Stores.ROS1_NOETIC)
    info, unita, fps, K, D, modello, tempi, dispositivo, modulo = {}, None, None, None, None, None, [], None, None
    conta = {"saturi_65535": 0, "oltre_scala": 0, "pixel": 0}
    forma = [None]

    with Reader(Path(bag)) as r:
        # Primo passaggio: metadati (sono pochi messaggi, ma sparsi nel file).
        for c, _, raw in r.messages():
            if c.topic.endswith("Depth_0/image/data"):
                continue
            if c.msgtype == "std_msgs/msg/Float32" and c.topic.endswith("option/Depth Units/value"):
                unita = float(ts.deserialize_ros1(raw, c.msgtype).data)
            elif c.msgtype == "diagnostic_msgs/msg/KeyValue" and "image" not in c.topic and "imu" not in c.topic:
                m = ts.deserialize_ros1(raw, c.msgtype)
                if c.topic == "/device_0/info" and m.key == "Name":
                    dispositivo = m.value
                elif c.topic == "/device_0/sensor_0/info" and m.key == "Name":
                    modulo = m.value
                elif c.topic == "/device_0/sensor_0/property" and m.key == "Depth Units" and unita is None:
                    unita = float(m.value)
            elif c.topic.endswith("Depth_0/info/camera_info"):
                m = ts.deserialize_ros1(raw, c.msgtype)
                K, D, modello = [float(x) for x in m.K], [float(x) for x in m.D], m.distortion_model
                info = {"larghezza": int(m.width), "altezza": int(m.height)}
            elif c.topic.endswith("Depth_0/info") and c.msgtype == "realsense_msgs/msg/StreamInfo":
                fps = struct.unpack("<I", raw[:4])[0]
        if unita is None or K is None or not fps:
            raise SystemExit(f"mancano metadati: unità {unita}, K {K}, fps {fps}")

        def fotogrammi():
            for c, _, raw in r.messages():
                if not c.topic.endswith("Depth_0/image/data"):
                    continue
                m = ts.deserialize_ros1(raw, c.msgtype)
                if m.encoding != "mono16" or m.is_bigendian or (m.height, m.width) != (info["altezza"], info["larghezza"]):
                    raise SystemExit(f"immagine inattesa: {m.encoding} {m.width}x{m.height} bigendian={m.is_bigendian}")
                a = np.frombuffer(m.data, dtype="<u2").reshape(m.height, m.width)
                tempi.append(m.header.stamp.sec + m.header.stamp.nanosec * 1e-9)
                saturi = a == 65535
                mm = np.rint(a.astype(np.float64) * (unita * 1000.0))
                oltre = (mm > 65534) & ~saturi
                conta["saturi_65535"] += int(saturi.sum()); conta["oltre_scala"] += int(oltre.sum()); conta["pixel"] += a.size
                mm[saturi | oltre] = 0
                yield mm.astype(np.uint16)

        fot = fotogrammi()
        # scrivi_sequenza vuole i tempi alla fine: li raccoglie il generatore; si passa una vista pigra.
        class Tempi:
            def __iter__(self):
                t0 = tempi[0]
                return iter([t - t0 for t in tempi])
            def __len__(self):
                return len(tempi)
        tipo = "stereo attivo a infrarossi" if modulo == "Stereo Module" else f"NON stereo attivo: «{modulo}» (luce codificata)"
        meta = {
            "larghezza": info["larghezza"], "altezza": info["altezza"], "fx": K[0], "fy": K[4], "cx": K[2], "cy": K[5],
            "fps": float(fps), "sensore": f"{dispositivo} ({tipo})", "posa": None,
            "origine": f"file di esempio di librealsense, https://librealsense.realsenseai.com/rs-tests/ ({os.path.basename(bag)})",
            "licenza": "non dichiarata nella pagina dei file di esempio; non verificata",
            "fonte_parametri": "camera_info e «Depth Units» scritti dal dispositivo dentro il file .bag",
            "distorsione": {"modello": modello, "coefficienti": D,
                            "nota": "le immagini NON sono state corrette: con coefficienti non nulli il modello a foro stenopeico è approssimato"},
            "unita_grezza_m": unita,
            "trasformazione": "millimetri = arrotonda(valore × unità × 1000); 65535 grezzo -> 0; tempi = header.stamp meno il primo",
            "verita": "nessuna; posa della camera ignota",
        }
        # I tempi servono dopo aver letto i fotogrammi: si materializza l'elenco prima di scrivere tempi.csv.
        import controlla_sequenza as cs
        os.makedirs(os.path.join(dest, "profondita"), exist_ok=True)
        n = 0
        for n, f in enumerate(fot, start=1):
            np.save(cs.percorso_profondita(dest, n - 1), np.ascontiguousarray(f, dtype="<u2"), allow_pickle=False)
        t = np.array(list(Tempi()))
        if n != len(t) or (n > 1 and np.diff(t).min() <= 0):
            raise SystemExit(f"tempi non crescenti o numero diverso: {n} fotogrammi, {len(t)} tempi")
        with open(os.path.join(dest, "tempi.csv"), "w", encoding="utf-8", newline="") as fo:
            fo.write("indice,tempo_s\n")
            for i, x in enumerate(t):
                fo.write(f"{i},{x:.6f}\n")
        meta["conteggi_conversione"] = conta
        meta["tempo_zero_unix_s"] = tempi[0]
        comune.salva_json(os.path.join(dest, "meta.json"), meta)
    print(f"{nome}: {n} fotogrammi {info['larghezza']}x{info['altezza']}, {dispositivo} / {modulo}, unità {unita}, fps nominali {fps}, "
          f"saturi {conta['saturi_65535']}, oltre scala {conta['oltre_scala']} su {conta['pixel']} pixel")


if __name__ == "__main__":
    main()
