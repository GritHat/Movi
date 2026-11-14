#!/bin/sh
# lancia.sh CORE USCITA — matrice di misura, un processo alla volta, ognuno con timeout di 120 s.
# Rifare:  sh compila.sh && sh lancia.sh 2 risultati.txt        (core 2 = Zen 5 veloce; core 8 = Zen 5c lento)
cd "$(dirname "$0")" || exit 1
C=${1:-2}; OUT=${2:-risultati.txt}; F=${3:-300}
: > "$OUT"
echo "# inizio $(date -Is) core=$C carico=$(cut -d' ' -f1-3 /proc/loadavg)" >> "$OUT"
uno() { timeout 120 taskset -c "$C" "$@" >> "$OUT" 2>&1 || echo "# FALLITO($?): $*" >> "$OUT"; }
giro() { # scena res passo fotogrammi
  uno bin/banco_POLARE "$1" "$2" "$3" "$4" 3 3
  uno bin/banco_POLARE "$1" "$2" "$3" "$4" 3 6
  uno bin/banco_IMMAGINE "$1" "$2" "$3" "$4"
  for nb in 3 8 30; do uno bin/banco_FASCE "$1" "$2" "$3" "$4" $nb; done
  for r in DENSA HASH HASHOCC OCTREE OCTPOT; do uno bin/banco_$r "$1" "$2" "$3" "$4"; done
  uno bin/banco_COLBIT "$1" "$2" "$3" "$4"
}
solo_colbit() { uno bin/banco_COLBIT "$1" "$2" "$3" "$4"; }
if [ "${4:-tutto}" = "colbit" ]; then   # la variante aggiunta dopo il primo giro: stesse configurazioni
  for res in 10 5; do for sc in vuota rada densa carico; do solo_colbit $sc $res 4 "$F"; done; done
  for res in 10 5; do for p in 2 8; do solo_colbit densa $res $p "$F"; solo_colbit vuota $res $p "$F"; done; done
  for res in 10 5; do solo_colbit densa $res 1 "$F"; solo_colbit vuota $res 1 60; done
elif [ "${4:-tutto}" = "breve" ]; then
  for res in 10 5; do giro densa $res 4 "$F"; giro densa $res 1 100; done
else
  for res in 10 5; do for sc in vuota rada densa carico; do giro $sc $res 4 "$F"; done; done
  for res in 10 5; do for p in 2 8; do giro densa $res $p "$F"; giro vuota $res $p "$F"; done; done
  for res in 10 5; do giro densa $res 1 "$F"; giro vuota $res 1 60; done
fi
echo "# fine $(date -Is) carico=$(cut -d' ' -f1-3 /proc/loadavg)" >> "$OUT"
