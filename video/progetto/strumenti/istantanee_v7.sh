#!/bin/sh
# v7: istantanee ai momenti chiave di ogni scena (s globali) + un foglio di controllo. Cartella nuova; non cancella niente.
# Uso: sh strumenti/istantanee_v7.sh VIDEO.mp4 CARTELLA_NUOVA "t1 t2 …"
set -eu
V=${1:?video}; O=${2:?cartella}; TT=${3:-"2 9 17.5 22 26.7 29.5 45.5 51.5 55.5 64.7 75 77.5 90.5 97.5 107.5 130.5 145.5 154 170"}
[ -e "$O" ] && { echo "esiste già: $O"; exit 3; }
mkdir -p "$O"
i=0
for t in $TT; do i=$((i+1)); timeout 60 ffmpeg -v error -ss "$t" -i "$V" -frames:v 1 "$O/$(printf %02d $i)_t$t.png"; done
timeout 120 ffmpeg -v error -pattern_type glob -i "$O/*.png" -vf "scale=640:360,tile=4x5:padding=6:color=0x24344A" -frames:v 1 "$O/foglio.png"
ls "$O" | wc -l
