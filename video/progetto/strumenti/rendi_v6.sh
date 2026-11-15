#!/bin/sh
# Rende il video di MoVi in locale, senza rete: CLI e Chrome di f17-video/00-strumenti, telemetria spenta.
# Uso: sh strumenti/rendi.sh <draft|looks|delivery> <uscita.mp4> [lingua en|it]
# Non cancella niente: se l'uscita esiste, si ferma.
set -eu
Q=${1:-draft}; OUT=${2:?uscita}; L=${3:-en}
QUI=$(cd "$(dirname "$0")" && pwd); P=$(dirname "$QUI")
D=$(cd "$P/../../.sciame/20261114-1301-percezione-challenge/f17-video/00-strumenti" && pwd)
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_BROWSER_PATH="$D/hyperframes/browser/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell"
HF="$D/hyperframes/cli/node_modules/.bin/hyperframes"
[ -e "$OUT" ] && { echo "esiste già: $OUT (scegli un nome nuovo)"; exit 3; }
cd "$P"
python3 -I strumenti/registri_a_js.py --scene scene/scene_v6.json
if [ "$Q" = delivery ]; then python3 -I strumenti/monta_v6.py --lingua "$L" --finale; else python3 -I strumenti/monta_v6.py --lingua "$L"; fi
timeout 120 "$HF" lint
timeout 1800 "$HF" render --quality "$Q" --fps 30 -o "$OUT"
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,nb_frames:format=duration,size -of default=nw=1 "$OUT"
