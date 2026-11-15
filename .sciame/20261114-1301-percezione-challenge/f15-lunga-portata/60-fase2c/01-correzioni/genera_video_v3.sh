#!/bin/sh
# Registri v3 per il video: uno alla volta (un processo pesante). Copia adattata di 50-fase2b/10-riprova/genera_video.sh.
# Scrive in prototipo/uscite/video/<scena>_v3/ (le vecchie cartelle restano). Poi il validatore della controprova.
cd /home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo || exit 1
PY=/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f10-dati/ambiente/venv/bin/python
VV=/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f15-lunga-portata/50-fase2b/11-controprova/valida_video.py
for s in ${*:-lp_A1 lp_E1 lp_A1_ingenua lp_A2 lp_A3 lp_E2 lp_E3 lp_E4}; do
  n=${s}_v3; u=uscite/video/$n; mkdir -p "$u"
  t0=$(date +%s)
  timeout 900 sh movi.sh esegui "$n" --config "scene/video/$n.json" --uscita "$u" --celle > "$u/esegui.txt" 2>&1 || echo "esegui FALLITO $?" >> "$u/esegui.txt"
  timeout 120 sh movi.sh convalida "$u/registro.jsonl" > "$u/convalida.txt" 2>&1
  timeout 300 "$PY" -I -B "$VV" "$u" > "$u/valida_video_controprova.txt" 2>&1
  timeout 600 sh movi.sh mostra "$u/registro.jsonl" --filmato --uscita "$u/viste" > "$u/mostra.txt" 2>&1
  echo "$n fatto in $(( $(date +%s) - t0 )) s: $(tail -1 $u/convalida.txt) | controprova: $(tail -1 $u/valida_video_controprova.txt | cut -c1-300)"
done
