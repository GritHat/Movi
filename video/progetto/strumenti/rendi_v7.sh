#!/bin/sh
# v7: animatic CON VOCE. Rende l'immagine (HyperFrames, locale, senza rete, telemetria spenta) con i tempi di scene_v7.json
# e i sottotitoli EN impressi dalla pagina; poi audio_v7.sh fa voce+musica+mix e riunisce. Non cancella niente.
# Uso: sh strumenti/rendi_v7.sh <draft|looks|delivery> <uscita_immagine.mp4> [lingua en|it]
set -eu
Q=${1:-looks}; OUT=${2:?uscita}; L=${3:-en}
QUI=$(cd "$(dirname "$0")" && pwd); P=$(dirname "$QUI")
D=$(cd "$P/../../.sciame/20261114-1301-percezione-challenge/f17-video/00-strumenti" && pwd)
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_BROWSER_PATH="$D/hyperframes/browser/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell"
HF="$D/hyperframes/cli/node_modules/.bin/hyperframes"
VOCE="$P/../voce/voce_guida_en_v4.wav"; VOCE_IT="$P/../voce/uscite/it_v5_1.0/voce_it.wav"
[ -e "$OUT" ] && { echo "esiste già: $OUT (scegli un nome nuovo)"; exit 3; }
cd "$P"
python3 -I strumenti/registri_a_js.py --scene scene/scene_v7.json --tempi tempi/NON_USATO_IN_V7.json
python3 -I strumenti/monta_v7.py --lingua "$L" --voce "$VOCE" --voce-it "$VOCE_IT"
timeout 120 "$HF" lint
timeout 1800 "$HF" render --quality "$Q" --fps 30 -o "$OUT"
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,nb_frames:format=duration,size -of default=nw=1 "$OUT"
