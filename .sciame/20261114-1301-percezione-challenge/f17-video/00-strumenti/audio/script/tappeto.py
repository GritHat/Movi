"""Tappeto sonoro sintetico (nessun diritto di terzi): accordi lenti, 48 kHz stereo.

Uso: uv run --with numpy python tappeto.py USCITA.wav [DURATA_S=180] [SEME=7]
Deterministico a parita' di seme. Solo numpy e libreria standard.
"""
import sys
import wave

import numpy as np

SR = 48000
uscita = sys.argv[1]
durata = float(sys.argv[2]) if len(sys.argv) > 2 else 180.0
seme = int(sys.argv[3]) if len(sys.argv) > 3 else 7
rng = np.random.default_rng(seme)

# Progressione lenta in re minore (frequenze in Hz): Dm9, Bbmaj7, Fmaj7, Am7
ACCORDI = [
    [73.42, 146.83, 220.00, 261.63, 329.63],   # D2 D3 A3 C4 E4
    [58.27, 116.54, 174.61, 220.00, 293.66],   # Bb1 Bb2 F3 A3 D4
    [87.31, 130.81, 174.61, 220.00, 329.63],   # F2 C3 F3 A3 E4
    [55.00, 110.00, 164.81, 196.00, 261.63],   # A1 A2 E3 G3 C4
]
PASSO = 15.0      # secondi per accordo
SFUMA = 6.0       # dissolvenza incrociata fra accordi
n = int(durata * SR)
t = np.arange(n) / SR
mix = np.zeros((n, 2))


def inviluppo(inizio, fine):
    """Finestra a coseno rialzato con salita e discesa di SFUMA secondi."""
    e = np.zeros(n)
    a, b = inizio - SFUMA / 2, fine + SFUMA / 2
    su = (t >= a) & (t < a + SFUMA)
    e[su] = 0.5 - 0.5 * np.cos(np.pi * (t[su] - a) / SFUMA)
    e[(t >= a + SFUMA) & (t < b - SFUMA)] = 1.0
    giu = (t >= b - SFUMA) & (t < b)
    e[giu] = 0.5 + 0.5 * np.cos(np.pi * (t[giu] - (b - SFUMA)) / SFUMA)
    return e


k = 0
while k * PASSO < durata:
    env = inviluppo(k * PASSO, (k + 1) * PASSO)
    for i, f in enumerate(ACCORDI[k % len(ACCORDI)]):
        peso = 1.0 / (1.0 + 0.6 * i)
        for scarto in (-0.11, 0.0, 0.13):               # tre voci leggermente scordate
            fase = rng.uniform(0, 2 * np.pi)
            lfo = 1.0 + 0.25 * np.sin(2 * np.pi * rng.uniform(0.03, 0.09) * t + fase)
            ff = f * (1 + scarto / 100)
            voce = np.sin(2 * np.pi * ff * t + fase)
            voce += 0.25 * np.sin(2 * np.pi * 2 * ff * t + 2 * fase)   # seconda armonica
            voce += 0.08 * np.sin(2 * np.pi * 3 * ff * t + 3 * fase)   # terza armonica
            pan = 0.5 + 0.35 * np.sin(2 * np.pi * rng.uniform(0.01, 0.04) * t + fase)
            v = voce * lfo * env * peso
            mix[:, 0] += v * np.sqrt(1 - pan)
            mix[:, 1] += v * np.sqrt(pan)
    k += 1

# Aria: rumore filtrato passa-basso (media mobile) a livello molto basso
rumore = rng.standard_normal((n, 2))
nucleo = np.ones(64) / 64
for c in range(2):
    mix[:, c] += 0.6 * np.convolve(rumore[:, c], nucleo, mode="same") * (
        1 + 0.5 * np.sin(2 * np.pi * 0.05 * t + c)
    )

# Dissolvenze generali: 4 s in entrata, 8 s in uscita
fi, fo = int(4 * SR), int(8 * SR)
mix[:fi] *= (0.5 - 0.5 * np.cos(np.pi * np.arange(fi) / fi))[:, None]
mix[-fo:] *= (0.5 + 0.5 * np.cos(np.pi * np.arange(fo) / fo))[:, None]

mix *= 10 ** (-6 / 20) / np.max(np.abs(mix))            # picco a -6 dBFS
pcm = (mix * 32767).astype("<i2")
with wave.open(uscita, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(f"scritto {uscita}: {durata:.1f} s, {SR} Hz, stereo, picco -6 dBFS")
