#!/bin/sh
# Esegue, convalida, tabellone e mostra (filmato + immagini) di una scena lunga. Uso: sh prove/scene_lunghe.sh <scena>
s=$1; u=uscite/$s; mkdir -p "$u"
timeout 900 sh movi.sh esegui "$s" --config "scene/$s.json" --uscita "$u" --celle > "$u/esegui.txt" 2>&1 || echo "esegui FALLITO $?" >> "$u/esegui.txt"
timeout 120 sh movi.sh convalida "$u/registro.jsonl" > "$u/convalida.txt" 2>&1
timeout 120 sh movi.sh tabellone "$u/registro.jsonl" > "$u/tabellone.txt" 2>&1
timeout 600 sh movi.sh mostra "$u/registro.jsonl" --filmato --uscita "$u/viste" > "$u/mostra.txt" 2>&1
echo "$s fatto: $(tail -1 $u/convalida.txt)"
