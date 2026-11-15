#!/bin/sh
# Versione inglese definitiva in un comando (montaggio finale). Non cancella niente.
set -eu
V=/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/video
cd "$V/progetto"
EN="$V/voce/uscite/en_v6_finale/voce_en.wav"; IT="$V/voce/uscite/it_v6_finale_draft/voce_it.wav"
sh strumenti/rendi_v9.sh delivery "$V/rendering/MoVi_pitch_EN_v1_immagine.mp4" en "$EN" "$IT" --finale
timeout 1800 python3 -I strumenti/audio_v9.py "$V/rendering/MoVi_pitch_EN_v1_immagine.mp4" "$V/consegna/MoVi_pitch_EN_v1.mp4" "$V/rendering/audio_MoVi_pitch_EN_v1" scene/scene_v9_en.json tempi/voce_v9_en.json
cp -n "$V/sottotitoli/movi_en_v9_en.srt" "$V/consegna/MoVi_pitch_EN_v1.srt"
cp -n "$V/sottotitoli/movi_it_v9_en.srt" "$V/consegna/MoVi_pitch_IT_v1.srt"
