# Voce (clip ai loro tempi) + musica (tappeto sintetico, opera propria del progetto) sotto la voce, portato a -14 LUFS,
# e unica codifica finale: H.264 High yuv420p 30 fps, AAC 48 kHz, faststart. Non sovrascrive.
# Uso: python3 audio_v4d.py IMMAGINE.mp4 USCITA.mp4 CARTELLA_LAVORO
import json, os, re, subprocess, sys
q = os.path.dirname(os.path.abspath(__file__))
IMG, OUT, W = sys.argv[1:4]
assert not os.path.exists(OUT), "esiste già: " + OUT
os.makedirs(W, exist_ok=True)
MUSICA = os.path.normpath(os.path.join(q, "..", "..", ".sciame", "20261114-1301-percezione-challenge", "f17-video", "00-strumenti", "audio", "uscite", "tappeto_180s.wav"))
T = json.load(open(os.path.join(q, "tempi.json"))); D = T["durata"]; RIT = T["ritardo_voce"]
def ff(a): return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-y"] + a, capture_output=True, text=True, timeout=600)
def ln(e): return json.loads(re.search(r"\{[^{}]*\}", e[e.rfind("[Parsed_loudnorm"):], re.S).group(0))
ins = []; fl = []
for i, (cid, t0, d, _) in enumerate(T["clip"]):
    ins += ["-i", T["wav"][cid]]
    ms = int(round((t0 + RIT) * 1000))
    fl.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}:all=1[v{i}]")
n = len(T["clip"])
fl.append("".join(f"[v{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0:duration=longest,apad=whole_dur={D},atrim=0:{D},asplit[v][chiave]")
fl.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{D},volume=-13dB,afade=t=in:d=2,afade=t=out:st={D-3}:d=3[m0]")
fl.append("[m0][chiave]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=700:makeup=1[m]")
fl.append(f"[v][m]amix=inputs=2:normalize=0:duration=longest,atrim=0:{D}[mix]")
pre = os.path.join(W, "premix.wav")
r = ff(ins + ["-i", MUSICA, "-filter_complex", ";".join(fl), "-map", "[mix]", "-c:a", "pcm_s24le", pre]); assert r.returncode == 0, r.stderr[-2000:]
J0 = ln(ff(["-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]).stderr)
mix = os.path.join(W, "mix.wav")
g = -14.0 - float(J0["input_i"])
r = ff(["-i", pre, "-af", f"volume={g:.2f}dB,alimiter=limit=0.8:attack=2:release=60:level=false", "-c:a", "pcm_s24le", mix]); assert r.returncode == 0, r.stderr[-2000:]
J1 = ln(ff(["-i", mix, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]).stderr)
g2 = -14.0 - float(J1["input_i"])
if abs(g2) > 0.15:
    mix2 = os.path.join(W, "mix2.wav")
    ff(["-i", mix, "-af", f"volume={g2:.2f}dB,alimiter=limit=0.84:attack=2:release=60:level=false", "-c:a", "pcm_s24le", mix2]); mix = mix2
    J1 = ln(ff(["-i", mix, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]).stderr)
json.dump({"premix": J0, "finale": J1}, open(os.path.join(W, "loudness.json"), "w"), indent=1)
print("LUFS", J1["input_i"], "TP", J1["input_tp"])
r = ff(["-i", IMG, "-i", mix, "-map", "0:v", "-map", "1:a", "-t", str(D), "-r", "30", "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", OUT]); assert r.returncode == 0, r.stderr[-2000:]
print(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,sample_rate:format=duration,size", "-of", "default=nw=1", OUT], capture_output=True, text=True).stdout)
