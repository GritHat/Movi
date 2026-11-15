#!/bin/sh
# Registri per il video: uno alla volta (un processo pesante). Da prototipo/: sh <questo> [scene…]
cd /home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo || exit 1
mkdir -p uscite/video
for s in ${*:-lp_A1 lp_A1_ingenua lp_A2 lp_A3 lp_E1 lp_E2 lp_E3 lp_E4}; do
  u=uscite/video/$s; mkdir -p "$u"
  t0=$(date +%s)
  timeout 900 sh movi.sh esegui "$s" --config "scene/video/$s.json" --uscita "$u" --celle > "$u/esegui.txt" 2>&1 || echo "esegui FALLITO $?" >> "$u/esegui.txt"
  timeout 120 sh movi.sh convalida "$u/registro.jsonl" > "$u/convalida.txt" 2>&1
  timeout 600 sh movi.sh mostra "$u/registro.jsonl" --filmato --uscita "$u/viste" > "$u/mostra.txt" 2>&1
  echo "$s fatto in $(( $(date +%s) - t0 )) s: $(tail -1 $u/convalida.txt)"
done
