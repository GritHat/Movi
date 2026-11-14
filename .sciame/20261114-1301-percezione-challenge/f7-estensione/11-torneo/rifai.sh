#!/bin/sh
# Rifa' tutte le prove del torneo (un lancio alla volta, ognuno sotto i due minuti; semi fissi nel sorgente).
set -e
cd "$(dirname "$0")"
gcc -O2 -o torneo torneo.c -lm
for t in statica s10 a5 a5c a6 a8 a9 a2 pp a3 a4 k102 scenB scenC scenA k105 a10; do
  timeout 120 ./torneo $t > risultati_$t.txt 2>&1
done
( timeout 120 ./torneo k106 ; timeout 120 ./torneo k106 3c ) > risultati_k106.txt 2>&1
timeout 120 python3 -I prova7.py > risultati_prova7.txt
timeout 120 python3 -I s11.py > risultati_s11.txt
