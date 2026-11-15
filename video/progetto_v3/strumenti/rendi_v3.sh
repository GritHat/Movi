#!/bin/sh
# Video v3 (volo ad alta velocita'): dai registri e dalla voce al file, in un comando. Non sovrascrive: si ferma se l'uscita esiste.
# Uso (da progetto_v3): sh strumenti/rendi_v3.sh <draft|standard|high> <voce_en.wav> <uscita.mp4>
set -eu
Q=${1:?qualita}; VOCE=${2:?voce}; OUT=${3:?uscita}
QUI=$(cd "$(dirname "$0")" && pwd); P=$(dirname "$QUI")
D=$(cd "$P/../../.sciame/20261114-1301-percezione-challenge/f17-video/00-strumenti" && pwd)
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_BROWSER_PATH="$D/hyperframes/browser/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell"
HF="$D/hyperframes/cli/node_modules/.bin/hyperframes"
IMM="${OUT%.mp4}_immagine.mp4"
for f in "$OUT" "$IMM"; do [ -e "$f" ] && { echo "esiste gia': $f"; exit 3; }; done
cd "$P"
# (i passi di costruzione: volo_a_js_v3.py, costruisci_v3.py, monta_v3.py; si rifanno solo su file nuovi)
timeout 120 "$HF" lint || true
timeout 1800 "$HF" render --quality "$Q" --fps 30 -o "$IMM"
python3 -I strumenti/audio_v3.py "$IMM" "$VOCE" tempi/scene_v3_en.json "$OUT"
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,nb_frames,sample_rate:format=duration,size -of default=nw=1 "$OUT"
