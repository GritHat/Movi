#!/bin/sh
# MoVi · versione ITALIANA del video pitch in un solo comando (montaggio finale, sciame-videomaker, 2026-11-15).
# Voce im_nicola dal testo italiano (video/voce/testi/voce_it_v4.modello.txt + video/progetto/cifre.json), rimontaggio dei
# tempi sulla voce italiana (ogni scena dura almeno quanto nella versione inglese), sottotitoli italiani impressi, stesso
# mix (musica, nessun suono legato agli stati, 1 s di silenzio all'ingresso di «reliability lost»), stessa esportazione.
# Non cancella niente: ogni uscita ha un nome nuovo (se esiste, lo script si ferma).
#
# Uso:  sh video/consegna/genera_versione_italiana.sh [delivery|looks|draft] [etichetta]
#   delivery (predefinito) -> video/consegna/MoVi_pitch_IT_v1.mp4
#   draft                  -> video/consegna/MoVi_pitch_IT_v1_draft.mp4 (prova veloce)
# Richiede: la versione inglese già montata (video/progetto/scene/scene_v9_en.json e la voce inglese qui sotto).
set -eu
Q=${1:-delivery}; ET=${2:-}
QUI=$(cd "$(dirname "$0")" && pwd); VID=$(dirname "$QUI"); P="$VID/progetto"
D=$(cd "$VID/../.sciame/20261114-1301-percezione-challenge/f17-video/00-strumenti" && pwd)
VOCE_EN="$VID/voce/uscite/en_v6_finale/voce_en.wav"
case "$Q" in delivery) SUF="" ;; *) SUF="_$Q" ;; esac
OUT="$QUI/MoVi_pitch_IT_v1$SUF$ET.mp4"
IMG="$VID/rendering/MoVi_pitch_IT_v1$SUF${ET}_immagine.mp4"
LAV="$VID/rendering/audio_MoVi_pitch_IT_v1$SUF$ET"
LOG="$VID/rendering/MoVi_pitch_IT_v1$SUF$ET.log"
for f in "$OUT" "$IMG" "$LAV"; do [ -e "$f" ] && { echo "esiste già: $f (usa un'etichetta nuova come 2° argomento)"; exit 3; }; done
[ -e "$VOCE_EN" ] || { echo "manca la voce inglese $VOCE_EN"; exit 4; }
exec > "$LOG" 2>&1
echo "inizio $(date -Is) qualità $Q"
# 1. voce italiana (Kokoro, im_nicola, 1.0), cartella nuova in video/voce/uscite/
timeout 900 bash "$VID/voce/genera_voce_v2.sh" it 1.0 "it_v6_finale$SUF$ET" | tee "$LAV.voce.txt"
VOCE_IT=$(sed -n 's/^uscita: //p' "$LAV.voce.txt" | tail -1)/voce_it.wav
[ -e "$VOCE_IT" ] || { echo "voce italiana non trovata"; exit 5; }
# 2. tempi: ogni scena dura almeno come in inglese; se la voce italiana è più lunga, la scena si allunga
cd "$P"
MIN=$(python3 -I -c "import json;print(','.join(str(s['durata']) for s in json.load(open('scene/scene_v9_en.json'))['scene']))")
python3 -I strumenti/costruisci_scene_v9.py "$VOCE_IT" it "$MIN"
python3 -I - "$VOCE_IT" <<'EOF'
import json, sys
E = {s["n"]: s["durata"] for s in json.load(open("scene/scene_v9_en.json"))["scene"]}
I = {s["n"]: s["durata"] for s in json.load(open("scene/scene_v9_it.json"))["scene"]}
T = json.load(open(sys.argv[1] + ".tempi.json"))
print("scena | EN s | IT s | voce IT s | sfora")
for n in sorted(E):
    q = [x for x in T if x["scena"] == n]; v = q[-1]["fine"] - q[0]["inizio"]
    print(f"{n} | {E[n]:.2f} | {I[n]:.2f} | {v:.2f} | {'SI, +%.2f s' % (I[n] - E[n]) if I[n] > E[n] + 1e-6 else 'no'}")
tot = sum(I.values()); print(f"TOTALE IT {tot:.2f} s (EN {sum(E.values()):.2f} s); fra 165 e 175 s: {'sì' if 165 <= tot <= 175 else 'NO'}")
EOF
# 3. immagine (registri veri _v3, testi e sottotitoli italiani impressi)
python3 -I strumenti/registri_a_js_v9.py --scene scene/scene_v9_it.json
python3 -I strumenti/monta_v9.py --lingua it --voce "$VOCE_IT" --voce-altra "$VOCE_EN" --scene scene/scene_v9_it.json --finale
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_BROWSER_PATH="$D/hyperframes/browser/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell"
HF="$D/hyperframes/cli/node_modules/.bin/hyperframes"
timeout 120 "$HF" lint
timeout 2400 "$HF" render --quality "$Q" --fps 30 -o "$IMG"
# 4. stesso mix ed esportazione (H.264 High CRF 18, AAC 48 kHz 320 kbps, faststart, -14 LUFS)
timeout 1800 python3 -I strumenti/audio_v9.py "$IMG" "$OUT" "$LAV" scene/scene_v9_it.json tempi/voce_v9_it.json
cp -n "$VID/sottotitoli/movi_it_v9_it.srt" "${OUT%.mp4}_video_italiano.srt"
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,sample_rate,bit_rate:format=duration,size -of default=nw=1 "$OUT"
echo "fine $(date -Is): $OUT"
