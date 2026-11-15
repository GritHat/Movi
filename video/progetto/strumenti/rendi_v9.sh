#!/bin/sh
# v9 (montaggio finale): immagine con HyperFrames (locale, senza rete, telemetria spenta) dai registri veri _v3.
# Uso: sh strumenti/rendi_v9.sh <draft|looks|delivery> <uscita_immagine.mp4> <en|it> <voce.wav> <voce_altra.wav> [--finale]
set -eu
Q=${1:?qualita}; OUT=${2:?uscita}; L=${3:?lingua}; VOCE=${4:?voce}; ALTRA=${5:?voce_altra}; FIN=${6:-}
QUI=$(cd "$(dirname "$0")" && pwd); P=$(dirname "$QUI")
D=$(cd "$P/../../.sciame/20261114-1301-percezione-challenge/f17-video/00-strumenti" && pwd)
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_BROWSER_PATH="$D/hyperframes/browser/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell"
HF="$D/hyperframes/cli/node_modules/.bin/hyperframes"
[ -e "$OUT" ] && { echo "esiste già: $OUT (scegli un nome nuovo)"; exit 3; }
cd "$P"
python3 -I strumenti/costruisci_scene_v9.py "$VOCE" "$L"
python3 -I strumenti/registri_a_js_v9.py --scene "scene/scene_v9_$L.json"
python3 -I strumenti/monta_v9.py --lingua "$L" --voce "$VOCE" --voce-altra "$ALTRA" --scene "scene/scene_v9_$L.json" $FIN
timeout 120 "$HF" lint
timeout 2400 "$HF" render --quality "$Q" --fps 30 -o "$OUT"
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,nb_frames:format=duration,size -of default=nw=1 "$OUT"
