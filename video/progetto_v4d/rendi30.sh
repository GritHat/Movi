#!/bin/sh
# Uso: sh video/progetto_v4d/rendi30.sh <draft|standard|high> <uscita.mp4>   Immagine muta a 30 fps. Non sovrascrive.
set -eu
Q=${1:?qualita}; OUT=$(realpath -m "${2:?uscita}")
P=$(cd "$(dirname "$0")" && pwd)
D=$(cd "$P/../../.sciame/20261114-1301-percezione-challenge/f17-video/00-strumenti" && pwd)
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_BROWSER_PATH="$D/hyperframes/browser/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell"
HF="$D/hyperframes/cli/node_modules/.bin/hyperframes"
[ -e "$OUT" ] && { echo "esiste gia': $OUT"; exit 3; }
cd "$P"
timeout 1200 "$HF" render --quality "$Q" --fps 30 -o "$OUT"
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,nb_frames:format=duration,size -of default=nw=1 "$OUT"
