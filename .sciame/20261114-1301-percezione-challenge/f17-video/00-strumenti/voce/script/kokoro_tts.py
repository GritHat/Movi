#!/usr/bin/env python3
"""Testo -> WAV 48 kHz mono 16 bit con Kokoro-82M (ONNX), su CPU.

Uso:
  venv-kokoro/bin/python script/kokoro_tts.py --testo testi/prova_en.txt \
      --voce bm_george --lingua en-gb --velocita 0.95 \
      --pausa-frase 0.35 --pausa-paragrafo 0.8 --uscita uscite/x.wav

Ogni frase è sintetizzata da sola (silenzi rifilati) e le pause sono inserite
qui, quindi sono esatte: --pausa-frase fra le frasi, --pausa-paragrafo fra i
paragrafi (separati da una riga vuota); un paragrafo fatto della sola riga
[pausa 1.5] inserisce quel silenzio in secondi al posto della pausa di paragrafo.
Le pause alle virgole sono quelle del modello.
Accanto al WAV scrive <uscita>.tempi.json con inizio e fine di ogni frase
(in secondi), utile per i sottotitoli e per sincronizzare le scene.
"""
import argparse, json, os, re, subprocess, time
import numpy as np

QUI = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.join(QUI, "..", "modelli", "kokoro")

p = argparse.ArgumentParser()
p.add_argument("--testo", required=True)
p.add_argument("--voce", default="bm_george")
p.add_argument("--lingua", default="en-gb", help="en-us, en-gb, it, ...")
p.add_argument("--velocita", type=float, default=1.0)
p.add_argument("--pausa-frase", type=float, default=0.35)
p.add_argument("--pausa-paragrafo", type=float, default=0.8)
p.add_argument("--uscita", required=True)
p.add_argument("--freq", type=int, default=48000)
a = p.parse_args()

from kokoro_onnx import Kokoro

t0 = time.perf_counter()
k = Kokoro(os.path.join(MOD, "kokoro-v1.0.onnx"), os.path.join(MOD, "voices-v1.0.bin"))
t_car = time.perf_counter() - t0

SR = 24000
BORDO = 0.15  # silenzio in testa e in coda: nessun attacco o rilascio tagliato
blocchi = [b.strip() for b in re.split(r"\n\s*\n", open(a.testo, encoding="utf-8").read()) if b.strip()]
pezzi, tempi, t = [np.zeros(int(BORDO * SR), np.float32)], [], BORDO
pausa_dovuta = 0.0  # silenzio da inserire prima della prossima frase


def silenzio(s):
    global t
    n = int(round(s * SR))
    if n:
        pezzi.append(np.zeros(n, np.float32))
        t += n / SR


t0 = time.perf_counter()
for b in blocchi:
    m = re.fullmatch(r"\[pausa\s+([0-9.]+)\]", b)
    if m:
        pausa_dovuta = float(m.group(1))
        continue
    frasi = [f for f in re.split(r"(?<=[.!?…])\s+", " ".join(b.split())) if f]
    for i, f in enumerate(frasi):
        if tempi:
            silenzio(pausa_dovuta)
        x, sr = k.create(f, voice=a.voce, speed=a.velocita, lang=a.lingua, trim=True)
        assert sr == SR
        x = x.astype(np.float32)
        pezzi.append(x)
        tempi.append({"inizio": round(t, 3), "fine": round(t + len(x) / SR, 3), "testo": f})
        t += len(x) / SR
        pausa_dovuta = a.pausa_frase
    pausa_dovuta = a.pausa_paragrafo
t_gen = time.perf_counter() - t0
pezzi.append(np.zeros(int(BORDO * SR), np.float32))
y = np.concatenate(pezzi)
picco = float(np.max(np.abs(y)))
y = y * (10 ** (-3 / 20) / picco)  # picco a -3 dBFS: il modello può superare 1.0 (misurato: 1,29 con if_sara)
pcm = (np.clip(y, -1, 1) * 32767).astype("<i2").tobytes()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-",
                "-af", f"aresample={a.freq}:resampler=soxr:precision=28", "-c:a", "pcm_s16le", a.uscita],
               input=pcm, check=True)
json.dump(tempi, open(a.uscita + ".tempi.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"uscita": a.uscita, "voce": a.voce, "picco_grezzo": round(picco, 3),
                  "durata_s": round(len(y) / SR, 3), "caricamento_s": round(t_car, 2),
                  "generazione_s": round(t_gen, 2), "rtf": round(t_gen / (len(y) / SR), 3)}))
