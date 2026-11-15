#!/bin/sh
# Rifà le prove F1-F6 (sciame-validazione, f19-volo/10-prove). Nessun file cancellato: uscite con nomi nuovi.
PY=/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f10-dati/ambiente/venv/bin/python
cd "$(dirname "$0")"
VOLO_REGOLA=v3 VOLO_USCITA=passaggi_volo_v3b.jsonl timeout 1500 $PY -I -B prove_volo.py 60 200 7
VOLO_REGOLA=v4 VOLO_USCITA=passaggi_volo_v4.jsonl timeout 1500 $PY -I -B prove_volo.py 60 200 7
VOLO_REGOLA=v3i VOLO_USCITA=passaggi_volo_v3i.jsonl timeout 1500 $PY -I -B prove_volo.py 60 200 7
$PY -I -B analizza_volo.py passaggi_volo_v3i.jsonl risultati_volo_v3i.json > /dev/null
$PY -I -B analizza_volo.py passaggi_volo_v3b.jsonl risultati_volo_v3b.json > /dev/null
$PY -I -B analizza_volo.py passaggi_volo_v4.jsonl risultati_volo_v4.json > /dev/null
VOLO_REGOLA=v3i timeout 600 $PY -I -B prove_volo.py --registro /home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo/uscite/video_volo
timeout 120 $PY -I -B indice_video.py /home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo/uscite/video_volo > /dev/null
timeout 120 $PY -I -B /home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo/prove/convalida_volo.py /home/fede/Scrivania/ed/GitHub/Movi-Hackthon/prototipo/uscite/video_volo/registro_F*.jsonl
