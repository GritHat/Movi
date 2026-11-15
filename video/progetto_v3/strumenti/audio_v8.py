#!/usr/bin/env python3
"""v7: voce montata + musica (tappeto sintetico del piano §8) + fruscio d'aria, mix e riunione con l'immagine.

- Voce: ogni paragrafo della voce guida (WAV + .tempi.json, campo «scena») spostato a scena.inizio + voce_da
  (tempi/voce_v7.json, scritto da monta_v7.py). Nessuna accelerazione.
- Musica: f17-video/00-strumenti/audio/uscite/tappeto_180s.wav a -14 dB con sidechain sulla voce; ambiente: rumore
  marrone filtrato a -26 dB (ffmpeg). Unico evento sonoro: 1 s di SILENZIO di musica e ambiente agli istanti
  «silenzi_musica» delle scene (ingresso di RELIABILITY LOST). Nessun suono legato agli stati.
- Mix: limitatore, poi loudnorm a due passate a -14 LUFS, TP -1,5 dBTP, lineare; misura ebur128.
- Riunione: video copiato (nessuna seconda codifica), AAC 48 kHz, faststart.
I file intermedi restano nella cartella di lavoro (nessun file si cancella).
Uso: python3 -I strumenti/audio_v7.py IMMAGINE.mp4 USCITA.mp4 CARTELLA_DI_LAVORO_NUOVA
"""
import json, os, re, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(QUI)
MUSICA = os.path.normpath(os.path.join(R, "..", "..", ".sciame", "20261114-1301-percezione-challenge", "f17-video",
                                       "00-strumenti", "audio", "uscite", "tappeto_180s.wav"))


def ff(args, **kw):
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-y"] + args, check=True, timeout=600,
                          capture_output=True, text=True, **kw)


def main():
    img, out, W = sys.argv[1], sys.argv[2], sys.argv[3]
    if os.path.exists(out) or os.path.exists(W):
        sys.exit(f"esiste già: {out} o {W}")
    os.makedirs(W)
    V = json.load(open(os.path.join(R, "tempi", "voce_v7.json")))
    S = {s["id"]: s for s in json.load(open(os.path.join(R, "scene", "scene_v7.json")))["scene"]}
    voce = V["voce"]; TE = json.load(open(voce + ".tempi.json"))
    D = round(sum(s["durata"] for s in V["scene"]), 3)
    rami, silenzi, k = [], [], 0
    for sc in V["scene"]:
        n = int(sc["id"][1:]); q = [x for x in TE if x["scena"] == n]
        for s0 in S[sc["id"]].get("silenzi_musica", []):
            silenzi.append(round(sc["inizio"] + s0, 3))
        if not q: continue
        lead = min(0.05, sc["inizio"] + sc["voce_da"], q[0]["inizio"])   # mai un ritardo negativo
        da, aa = q[0]["inizio"] - lead, q[-1]["fine"] + 0.1
        ms = int(round((sc["inizio"] + sc["voce_da"] - (q[0]["inizio"] - da)) * 1000))
        rami.append(f"[0:a]atrim={da:.3f}:{aa:.3f},asetpts=PTS-STARTPTS,adelay={ms}:all=1[p{k}]"); k += 1
    fv = ";".join(rami) + ";" + "".join(f"[p{i}]" for i in range(k)) + f"amix=inputs={k}:normalize=0:duration=longest,apad,atrim=0:{D}[v]"
    pv = os.path.join(W, "voce_montata.wav")
    ff(["-i", voce, "-filter_complex", fv, "-map", "[v]", "-ar", "48000", "-c:a", "pcm_s16le", pv])
    # guadagno 0 dentro [s, s+1], rampe di 40 ms ai bordi
    g = "*".join(f"min(1,max((({s:.3f})-t)/0.04,(t-({s + 1:.3f}))/0.04))" for s in silenzi) or "1"
    fuori = D - 3
    filt = (f"[0:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=70,alimiter=limit=0.7:level=false,asplit=2[v][chiave];"
            f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{D},volume=-14dB,afade=t=in:d=2,afade=t=out:st={fuori}:d=3[m0];"
            f"[m0][chiave]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=700:makeup=1[m1];"
            f"[m1]volume='{g}':eval=frame[m];"
            f"anoisesrc=color=brown:seed=7:amplitude=0.5:d={D}:r=48000,lowpass=f=600,aformat=channel_layouts=stereo,volume=-26dB,"
            f"afade=t=in:d=2,afade=t=out:st={fuori}:d=3,volume='{g}':eval=frame[a];"
            f"[v][m][a]amix=inputs=3:normalize=0:duration=first[mix]")
    pre = os.path.join(W, "premix.wav")
    ff(["-i", pv, "-i", MUSICA, "-filter_complex", filt, "-map", "[mix]", "-c:a", "pcm_s24le", pre])
    # v8: guadagno fisso verso -14 LUFS e limitatore PRIMA di loudnorm, così loudnorm resta lineare (STRUMENTI §5.2, avvertenza 1)
    r0 = ff(["-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    J0 = json.loads(re.search(r"\{[^{}]*\}", r0.stderr[r0.stderr.rfind("[Parsed_loudnorm"):], re.S).group(0))
    guad = -14.0 - float(J0["input_i"])
    pre2 = os.path.join(W, "premix_limitato.wav")
    ff(["-i", pre, "-af", f"volume={guad:.2f}dB,alimiter=limit=0.75:attack=2:release=60:level=false", "-c:a", "pcm_s24le", pre2])
    pre = pre2
    r = ff(["-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    J = json.loads(re.search(r"\{[^{}]*\}", r.stderr[r.stderr.rfind("[Parsed_loudnorm"):], re.S).group(0))
    open(os.path.join(W, "loudnorm_passata1.json"), "w").write(json.dumps(J, indent=1))
    mix = os.path.join(W, "mix.wav")
    r2 = ff(["-i", pre, "-af", f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={J['input_i']}:measured_TP={J['input_tp']}:"
             f"measured_LRA={J['input_lra']}:measured_thresh={J['input_thresh']}:offset={J['target_offset']}:linear=true:print_format=json,aresample=48000",
             "-c:a", "pcm_s24le", mix])
    J2 = json.loads(re.search(r"\{[^{}]*\}", r2.stderr[r2.stderr.rfind("[Parsed_loudnorm"):], re.S).group(0))
    open(os.path.join(W, "loudnorm_passata2.json"), "w").write(json.dumps(J2, indent=1))
    ff(["-i", img, "-i", mix, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-ac", "2", "-movflags", "+faststart", "-shortest", out])
    e = ff(["-i", out, "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    riass = e[e.rfind("Summary:"):]
    open(os.path.join(W, "ebur128_finale.txt"), "w").write(riass)
    print(f"durata {D} s; silenzi musica a {silenzi}; normalizzazione: {J2.get('normalization_type')}\n{riass}")


if __name__ == "__main__":
    main()
