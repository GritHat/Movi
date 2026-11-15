#!/usr/bin/env python3
"""MoVi video v3 FINALE: voce + musica + ambiente, loudnorm a due passate (-14 LUFS, TP -1.5 dBTP, lineare), unica codifica
finale «delivery» (libx264 High, CRF 18, yuv420p, 30 fps, bt709; AAC 48 kHz stereo; faststart). Derivato da audio_v9.py.
- Voce: ogni paragrafo del WAV (tempi da tempi/scene_finale_<l>.json: voce_wav_da/a) messo a scena.inizio + voce_da.
  Nessuna accelerazione, nessuno stiramento.
- Musica: tappeto sintetico di 180 s (f17-video/00-strumenti/audio/uscite/tappeto_180s.wav, generato con numpy: opera propria)
  a -14 dB con sidechain sulla voce; ambiente: rumore marrone filtrato a -26 dB; 1 s di silenzio di musica e ambiente
  agli istanti dati (--silenzi), per esempio all'urto di F7.
Uso: python3 -I strumenti/audio_finale.py IMMAGINE.mp4 USCITA.mp4 CARTELLA_NUOVA tempi/scene_finale_<l>.json VOCE.wav [--silenzi a,b] [--crf 18]
Non cancella niente: i file intermedi restano nella cartella di lavoro.
Correzione v1: apad=whole_dur (con apad semplice la voce montata finiva all'ultima parola, 170,9 s, e -shortest tagliava i titoli)."""
import json, os, re, subprocess, sys
QUI = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(QUI)
MUSICA = os.path.normpath(os.path.join(R, "..", "..", ".sciame", "20261114-1301-percezione-challenge", "f17-video", "00-strumenti", "audio", "uscite", "tappeto_180s.wav"))
def ff(a): return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-y"] + a, check=True, timeout=1500, capture_output=True, text=True)
def ln(stderr): return json.loads(re.search(r"\{[^{}]*\}", stderr[stderr.rfind("[Parsed_loudnorm"):], re.S).group(0))
img, out, W, TJ, voce = sys.argv[1:6]
sil = [float(x) for x in sys.argv[sys.argv.index("--silenzi") + 1].split(",")] if "--silenzi" in sys.argv else []
crf = sys.argv[sys.argv.index("--crf") + 1] if "--crf" in sys.argv else "18"
if os.path.exists(out) or os.path.exists(W): sys.exit(f"esiste gia': {out} o {W}")
os.makedirs(W)
T = json.load(open(TJ)); D = T["totale"]; rami = []
for k, sc in enumerate(T["scene"]):
    da, aa = max(0, sc["voce_wav_da"] - 0.05), sc["voce_wav_a"] + 0.1
    ms = int(round((sc["inizio"] + sc["voce_da"] - (sc["voce_wav_da"] - da)) * 1000))
    rami.append(f"[0:a]atrim={da:.3f}:{aa:.3f},asetpts=PTS-STARTPTS,adelay={ms}:all=1[p{k}]")
n = len(rami)
pv = os.path.join(W, "voce_montata.wav")
ff(["-i", voce, "-filter_complex", ";".join(rami) + ";" + "".join(f"[p{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0:duration=longest,apad=whole_dur={D},atrim=0:{D}[v]", "-map", "[v]", "-ar", "48000", "-c:a", "pcm_s16le", pv])
g = "*".join(f"min(1,max((({s:.3f})-t)/0.04,(t-({s + 1:.3f}))/0.04))" for s in sil) or "1"
fuori = D - 3
filt = (f"[0:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=70,alimiter=limit=0.7:level=false,asplit=2[v][chiave];"
        f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{D},volume=-14dB,afade=t=in:d=2,afade=t=out:st={fuori}:d=3[m0];"
        f"[m0][chiave]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=700:makeup=1[m1];[m1]volume='{g}':eval=frame[m];"
        f"anoisesrc=color=brown:seed=7:amplitude=0.5:d={D}:r=48000,lowpass=f=600,aformat=channel_layouts=stereo,volume=-26dB,"
        f"afade=t=in:d=2,afade=t=out:st={fuori}:d=3,volume='{g}':eval=frame[a];[v][m][a]amix=inputs=3:normalize=0:duration=first[mix]")
pre = os.path.join(W, "premix.wav"); ff(["-i", pv, "-i", MUSICA, "-filter_complex", filt, "-map", "[mix]", "-c:a", "pcm_s24le", pre])
J0 = ln(ff(["-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]).stderr)
pre2 = os.path.join(W, "premix_limitato.wav")
ff(["-i", pre, "-af", f"volume={-14.0 - float(J0['input_i']):.2f}dB,alimiter=limit=0.75:attack=2:release=60:level=false", "-c:a", "pcm_s24le", pre2])
J = ln(ff(["-i", pre2, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]).stderr)
open(os.path.join(W, "loudnorm_passata1.json"), "w").write(json.dumps(J, indent=1))
mix = os.path.join(W, "mix.wav")
J2 = ln(ff(["-i", pre2, "-af", f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={J['input_i']}:measured_TP={J['input_tp']}:measured_LRA={J['input_lra']}:measured_thresh={J['input_thresh']}:offset={J['target_offset']}:linear=true:print_format=json,aresample=48000", "-c:a", "pcm_s24le", mix]).stderr)
open(os.path.join(W, "loudnorm_passata2.json"), "w").write(json.dumps(J2, indent=1))
ff(["-i", img, "-i", mix, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", crf,
    "-pix_fmt", "yuv420p", "-r", "30", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
    "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-shortest", out])
e = ff(["-i", out, "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
open(os.path.join(W, "ebur128_finale.txt"), "w").write(e[e.rfind("Summary:"):])
print(f"durata {D}; silenzi {sil}; normalizzazione {J2.get('normalization_type')}\n" + e[e.rfind("Summary:"):])
