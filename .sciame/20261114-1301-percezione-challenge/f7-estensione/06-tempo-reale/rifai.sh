#!/bin/sh
# Rifà tutte le misure di sciame-tempo-reale (estensione f7). Un lancio alla volta, ognuno con timeout di 120 s.
# Uso: sh rifai.sh <parte>   con parte = tempo | lento | sicurezza | interf | lasca | vecchi | tetto <blocchi>
# Core veloce = 4 (5,16 GHz massimi), core lento = 8 (3,29 GHz) su questa macchina: cambiare VELOCE e LENTO altrove.
cd "$(dirname "$0")" || exit 1
VELOCE=4; LENTO=8; ALTRO=5
[ -x ./banco ] || gcc -O2 -Wno-misleading-indentation -o banco banco.c -lm -lpthread || exit 1
L() { timeout 120 "$@" || echo "LANCIO FALLITO O SCADUTO ($?): $*"; }
echo "# parte=$1 inizio=$(date -Is) gcc=$(gcc -dumpversion)"
case "$1" in
tempo)
  for s in vuota tipica perturbazione; do
    L taskset -c $VELOCE ./banco tempo $s G 5 1 0
    for lato in 5 10; do
      for k in 1 2 4 8; do L taskset -c $VELOCE ./banco tempo $s D $lato $k 0; done
      L taskset -c $VELOCE ./banco tempo $s H $lato 1 0
      L taskset -c $VELOCE ./banco tempo $s H $lato 4 0
      L taskset -c $VELOCE ./banco tempo $s P $lato 1 0
    done
  done
  L taskset -c $VELOCE ./banco tempo tipica D 5 1 3
  L taskset -c $VELOCE ./banco tempo tipica D 5 4 3
  L taskset -c $VELOCE ./banco tempo tipica P 5 1 3
  L taskset -c $VELOCE ./banco tempo perturbazione D 5 4 3 0 0
  L taskset -c $VELOCE ./banco tempo perturbazione D 5 4 3 0 1
  ;;
lento)
  for m in "G 5 1" "D 5 1" "D 5 4" "P 5 1" "D 10 1" "D 10 4" "P 10 1"; do L taskset -c $LENTO ./banco tempo vuota $m 0; done
  ;;
sicurezza)
  L taskset -c $VELOCE ./banco sicurezza tipica 5 4
  L taskset -c $VELOCE ./banco sicurezza tipica 5 2
  L taskset -c $VELOCE ./banco sicurezza tipica 10 4
  L taskset -c $VELOCE ./banco sicurezza perturbazione 5 4
  ;;
interf)
  L ./banco interf tipica $VELOCE $ALTRO 0
  L ./banco interf tipica $VELOCE $ALTRO 1
  L ./banco interf tipica $VELOCE 16 1      # 16 è il filo gemello del core 4: caso sfavorevole
  ;;
lasca)
  for s in vuota tipica perturbazione; do L taskset -c $VELOCE ./banco tempo $s Q 5 1 3; L taskset -c $VELOCE ./banco tempo $s Q 10 1 3; done
  L taskset -c $VELOCE ./banco tempo perturbazione D 5 1 3
  L taskset -c $VELOCE ./banco tempo perturbazione P 5 1 3
  ;;
vecchi)
  L taskset -c $VELOCE ./banco vecchi 5 Q
  L taskset -c $VELOCE ./banco vecchi 5 D
  L taskset -c $VELOCE ./banco vecchi 10 Q
  ;;
tetto)
  # $2 = tetto dei blocchi (metà di quelli usati senza tetto nella scena tipica a 5 cm)
  L taskset -c $VELOCE ./banco tempo tipica H 5 1 0
  L taskset -c $VELOCE ./banco tempo tipica H 5 1 0 "$2"
  L taskset -c $VELOCE ./banco tempo perturbazione H 5 1 0 "$2"
  ;;
*) echo "parte sconosciuta"; exit 2;;
esac
echo "# fine=$(date -Is)"
