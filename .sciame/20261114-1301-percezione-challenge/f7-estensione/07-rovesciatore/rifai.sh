#!/bin/sh
# Rifa' le prove del rovesciatore (f7). Nessun numero casuale: la scena e' deterministica.
# Un lancio alla volta, ciascuno sotto i due minuti. I tempi dipendono dal carico della macchina.
set -e
cd "$(dirname "$0")"
gcc -O2 -w -o rovescia rovescia.c -lm
gcc -O2 -w -o p7 p7.c -lm
gcc -O2 -w -o p8 p8.c -lm
timeout 120 ./rovescia analisi > risultati_analisi.txt
timeout 120 taskset -c 0 ./rovescia tempi > risultati_tempi_2.txt
timeout 60 taskset -c 0 ./p7 > risultati_p7.txt
timeout 60 ./p8 > risultati_p8_p9.txt
# La prima esecuzione (griglia allineata alle superfici): gcc -O2 -w -o rovescia_prima rovescia_prima.c -lm && ./rovescia_prima analisi
