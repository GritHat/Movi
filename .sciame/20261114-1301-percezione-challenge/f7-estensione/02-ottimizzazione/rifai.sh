#!/bin/sh
# Rifa le misure di sciame-ottimizzazione (f7). Uso: ./rifai.sh N   (N = 0..10, un lotto alla volta, ciascuno sotto i due minuti)
# Ogni lotto aggiunge righe a risultati_N.txt. Un thread, fissato sul nucleo $CPU (predefinito 1; il primo lotto sul nucleo 2 e' risultato conteso da un altro processo: risultati_1_contaminato_cpu2.txt).
cd "$(dirname "$0")" || exit 1
CPU="${CPU:-1}"
B="taskset -c $CPU ./banco"
# chi altro sta usando la macchina (altri agenti lanciano prove in parallelo): le prime tre righe per uso di CPU
[ "$1" != 0 ] && ps -eo pcpu,psr,comm --sort=-pcpu | head -4 | sed "s/^/# carico prima: /"
case "$1" in
0) gcc -O2 -Wall -Wextra -o banco banco.c -lm ;;
1) for sc in rada densa; do for r in 10 5; do for s in nulla densa densafix hash hashnc octree pol3 pol6 ibr3 ibr6; do $B $s $r $sc 160 120 300; done; done; done ;;
2) for sc in rada densa; do for s in densa densafix hash octree pol3 pol6 ibr6; do $B $s 10 $sc 320 240 300; done; done ;;
3) for sc in rada densa; do for s in densa densafix hash octree ibr6; do $B $s 5 $sc 320 240 300; done; done ;;
4) for s in densa hash pol3 pol6 ibr6; do $B $s 10 rada 640 480 200; done; $B octree 10 rada 640 480 200 ;;
5) for s in densa hash ibr6; do $B $s 5 rada 640 480 200; done ;;
6) $B octree 5 rada 640 480 200 ;;
7) for s in densa hash; do $B $s 5 densa 640 480 200; done; $B csr 10 rada 160 120 200; $B csr 10 densa 160 120 200 ;;
8) for sc in rada densa; do for r in 10 5; do $B hash $r $sc 160 120 300 1 0; $B densa $r $sc 160 120 300 1 0; done; done
   for r in 10 5; do $B hash $r rada 160 120 300 0 1; done
   $B hash 5 rada 160 120 300 0 0 300; $B hash 10 rada 160 120 300 0 0 60 ;;
9) for sc in rada densa; do $B densa 10 $sc 160 120 200; $B hash 10 $sc 160 120 200; $B octree 10 $sc 160 120 200; done ;;
10) taskset -c $CPU python3 dda_python.py ;;
*) echo "lotto 0..10"; exit 2 ;;
esac
