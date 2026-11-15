#!/bin/sh
# Esegue un file Python nell'editor di Unreal aperto, tramite la cassetta di init_unreal.py. Uso: sh ue.sh file.py
D=$(cd "$(dirname "$0")" && pwd)
: > "$D/_outbox.txt.tmp"; mv "$D/_outbox.txt.tmp" "$D/_outbox.txt"
cp "$1" "$D/_inbox.py"; touch "$D/_inbox.py"
i=0; while [ ! -s "$D/_outbox.txt" ] && [ $i -lt ${2:-60} ]; do sleep 0.5; i=$((i+1)); done
cat "$D/_outbox.txt"
