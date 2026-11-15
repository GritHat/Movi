#!/bin/sh
# Rigenera il video completo IT v4 da zero (la voce va generata prima: python3 voce/genera_voce_v4d.py). Non sovrascrive.
# Uso: sh video/progetto_v4d/fai_tutto.sh <etichetta>   ->  video/rendering/MoVi_pitch_IT_v4_<etichetta>.mp4 (+ .srt e copione accanto)
set -eu
E=${1:?etichetta}
P=$(cd "$(dirname "$0")" && pwd); R="$P/../rendering"
mkdir -p "$R/v4d_$E"
python3 "$P/costruisci_v4d.py" "$R/v4d_$E"
sh "$P/rendi30.sh" standard "$R/MoVi_pitch_IT_v4_${E}_immagine.mp4"
python3 "$P/audio_v4d.py" "$R/MoVi_pitch_IT_v4_${E}_immagine.mp4" "$R/MoVi_pitch_IT_v4_$E.mp4" "$R/v4d_$E/audio"
