#!/bin/sh
# Versione inglese v2 (consegna dopo il controllo qualità) in un comando. Non cancella niente: si ferma se un'uscita esiste.
set -eu
V=/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/video
cd "$V/progetto"
EN="$V/voce/uscite/en_v7b_consegna_v2_0.95/voce_en.wav"; IT="$V/voce/uscite/it_v7_consegna_v2/voce_it.wav"
for f in "$V/consegna/MoVi_pitch_EN_v2.mp4" "$V/rendering/audio_MoVi_pitch_EN_v2"; do [ -e "$f" ] && { echo "esiste già: $f"; exit 3; }; done
sh strumenti/rendi_v10.sh delivery "$V/rendering/MoVi_pitch_EN_v2_immagine.mp4" en "$EN" "$IT" --finale
timeout 1800 python3 -I strumenti/audio_v9.py "$V/rendering/MoVi_pitch_EN_v2_immagine.mp4" "$V/consegna/MoVi_pitch_EN_v2.mp4" "$V/rendering/audio_MoVi_pitch_EN_v2" scene/scene_v10_en.json tempi/voce_v10_en.json
cp -n "$V/sottotitoli/movi_en_v10_en.srt" "$V/consegna/MoVi_pitch_EN_v2.srt"
cp -n "$V/sottotitoli/movi_it_v10_en.srt" "$V/consegna/MoVi_pitch_IT_v2.srt"
