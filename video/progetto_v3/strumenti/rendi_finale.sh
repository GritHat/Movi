#!/bin/sh
# Video v3 FINALE: index.html (gia' montato da monta_finale.py) -> immagine muta. Non sovrascrive.
# Uso (da progetto_v3): sh strumenti/rendi_finale.sh <draft|standard|high|delivery> <uscita_immagine.mp4>
set -eu
Q=${1:?qualita}; OUT=${2:?uscita}
QUI=$(cd "$(dirname "$0")" && pwd); P=$(dirname "$QUI")
D=$(cd "$P/../../.sciame/20261114-1301-percezione-challenge/f17-video/00-strumenti" && pwd)
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_BROWSER_PATH="$D/hyperframes/browser/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell"
HF="$D/hyperframes/cli/node_modules/.bin/hyperframes"
[ -e "$OUT" ] && { echo "esiste gia': $OUT"; exit 3; }
cd "$P"
timeout 120 "$HF" lint || true
timeout 1800 "$HF" render --quality "$Q" --fps 30 -o "$OUT"
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,nb_frames:format=duration,size -of default=nw=1 "$OUT"
