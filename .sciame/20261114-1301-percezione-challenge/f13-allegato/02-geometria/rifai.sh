#!/bin/bash
# Rifa' tutti i ricalcoli del fascicolo (pochi secondi). Scrive solo ricalcoli.txt in questa cartella.
set -eu
qui="$(cd "$(dirname "$0")" && pwd)"
py="$qui/../../f10-dati/ambiente/venv/bin/python"
timeout 300 "$py" -I -B "$qui/ricalcoli.py" > "$qui/ricalcoli.txt"
echo "fatto: $qui/ricalcoli.txt ($(wc -l < "$qui/ricalcoli.txt") righe)"
