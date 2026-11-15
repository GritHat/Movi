#!/usr/bin/env python3
"""Controllo di intelligibilità: ritrascrive i WAV con faster-whisper (CPU) e conta le parole diverse dal testo.
Uso: venv-asr/bin/python script/asr_controllo.py <lingua en|it> <testo.txt> <wav> [<wav> ...]"""
import re, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

NUM = {"en": {"thirty": "30", "ninety": "90", "fifty": "50", "two": "2", "four": "4", "meters": "metres", "kilometers": "kilometres"},
       "it": {"trenta": "30", "novanta": "90", "cinquanta": "50", "due": "2", "quattro": "4", "centoventi": "120"}}


def norm(s, l):
    w = re.findall(r"[\wàèéìòù']+", s.lower())
    return [NUM[l].get(x, x) for x in w]


def dist(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]


l, rif = sys.argv[1], open(sys.argv[2], encoding="utf-8").read()
m = WhisperModel("small", device="cpu", compute_type="int8")
r = norm(rif, l)
for f in sys.argv[3:]:
    x = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True,check=True).stdout, np.float32)
    seg, _ = m.transcribe(x, language=l, beam_size=5)
    t = " ".join(s.text.strip() for s in seg)
    e = dist(r, norm(t, l))
    print(f"{f.split('/')[-1]} | errori {e}/{len(r)} | {t}")
