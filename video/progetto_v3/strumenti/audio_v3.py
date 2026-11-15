#!/usr/bin/env python3
"""Mette la voce sotto l'immagine: ogni paragrafo della voce all'inizio della sua scena + anticipo; loudnorm a -14 LUFS.
Uso: python3 -I strumenti/audio_v3.py <immagine.mp4> <voce.wav> <tempi/scene_v3_en.json> <uscita.mp4>"""
import json, sys, subprocess, os
imm, voce, tj, out = sys.argv[1:5]
if os.path.exists(out): print("esiste gia':", out); sys.exit(3)
T = json.load(open(tj)); n = len(T["scene"]); f = []
cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", imm] + sum([["-i", voce] for _ in range(n)], [])
for i, s in enumerate(T["scene"]):
    a, b = max(0, s["voce_wav_da"] - 0.05), s["voce_wav_a"] + 0.25
    d = int(round((s["inizio"] + s["voce_da"] - 0.05) * 1000))
    f.append(f"[{i+1}:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,adelay={d}|{d}[v{i}]")
f.append("".join(f"[v{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0:duration=longest,apad,atrim=0:{T['totale']},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]")
cmd += ["-filter_complex", ";".join(f), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out]
subprocess.run(cmd, check=True, timeout=600)
print("scritto", out)
