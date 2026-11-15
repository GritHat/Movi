#!/bin/sh
# prova_tutto.sh — esegue le prove e tutte le scene d'esempio. Da lanciare in prototipo/:  sh prova_tutto.sh
# Tutto è SIMULATO: nessun sensore fisico. Tempo atteso: pochi minuti (ogni passo ha il suo timeout).
set -u
cd "$(dirname "$0")"
PY=${PY:-$(cd ../.sciame/20261114-1301-percezione-challenge/f10-dati/ambiente/venv/bin && pwd)/python}
export PY
SEQ=${SEQ:-../.sciame/20261114-1301-percezione-challenge/f10-dati/11-simulatore/sequenze}
mkdir -p uscite
ESITO=0
passo() { nome=$1; shift; printf '%-44s ' "$nome"; if "$@" > "uscite/$nome.txt" 2>&1; then echo ok; else c=$?; if [ $c = 4 ]; then echo "non ancora costruito"; else echo "FALLITO ($c): uscite/$nome.txt"; ESITO=1; fi; fi; }
T0=$(date +%s)
# 0. il codice riusato non è stato toccato
passo 00_impronte_riuso sh -c 'cd riuso && sha256sum -c --quiet IMPRONTE.txt'
# 1. le prove del codice riusato, dal nuovo posto
passo 01_prove_catena timeout 240 "$PY" -I -B riuso/catena/prove.py
passo 02_banco_c sh -c 'cd riuso/c && gcc -O2 -Wall -Wno-misleading-indentation -o insieme insieme.c -lm && timeout 60 ./insieme prova geo=T n=40 beh=01236 rh=0.75 assorb=0 m1n=2 vmin=0.3 c3=1 c7=1'
# 2. il pacchetto e il formato del registro
passo 03_importa timeout 60 "$PY" -I -B -c 'import importlib, sys; sys.path.insert(0, "."); [importlib.import_module("movi." + m) for m in "config corto esegui etichette eventi_registro livelli lungo mostra nucleo predittore_zona registro riuso scene sorgenti tabellone __main__".split()]'
passo 04_registro_corto timeout 120 "$PY" -I -B prove/prova_registro.py "$SEQ/d435i_nom__pannello_a12__s00" uscite/registro_prova.jsonl
passo 05_convalida timeout 60 sh movi.sh convalida uscite/registro_prova.jsonl
# 2b. principi e nucleo corto: pavimento vuoto, sensore coperto, etichette, controlli fra righe, tempo (versione rapida)
passo 06_principi timeout 900 "$PY" -I -B prove/prova_principi.py rapida
# 3. tutte le scene d'esempio: esegui, tabellone, mostra (le parti non ancora costruite escono con 4 e non contano)
for s in $(sh movi.sh scene | awk '{print $1}'); do
  passo "scena_${s}_esegui" timeout 120 sh movi.sh esegui "$s" --config "scene/$s.json" --uscita "uscite/$s" --celle
  [ -f "uscite/$s/registro.jsonl" ] && passo "scena_${s}_tabellone" timeout 60 sh movi.sh tabellone "uscite/$s/registro.jsonl"
  [ -f "uscite/$s/registro.jsonl" ] && passo "scena_${s}_mostra" timeout 300 sh movi.sh mostra "uscite/$s/registro.jsonl" --filmato --uscita "uscite/$s/viste"
done
echo "tempo: $(( $(date +%s) - T0 )) s; esito: $ESITO (0 = nessun fallimento; «non ancora costruito» non è un fallimento)"
exit $ESITO
