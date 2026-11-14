#!/bin/sh
# Rifa tutte le prove A e B di H-012 (f4). Un lancio alla volta, al piu' 120 s ciascuno.
cd "$(dirname "$0")" || exit 1
t() { o="$1"; shift; ( time timeout 120 python3 sim_h012.py "$@" ) > "$o" 2>&1; echo "$o: uscita $?"; }
t out_A_T_w1.txt A T 1 400
t out_A_T_w2.txt A T 2 400
t out_A_D_w05.txt A D 0.5 400
t out_A_D_w1.txt A D 1 400
t out_A_T_w1_lim.txt A T 1 400 lim
t out_A_T_w1_pd09.txt A T 1 400 nom 0.9
t out_SWEEP.txt SWEEP 400
t out_A2.txt A2
t out_A6.txt A6 400
t out_WALL.txt WALL 12000
t out_PED.txt PED 2000
t out_V1.txt V1 2000
( time timeout 120 python3 extra.py ) > out_EXTRA.txt 2>&1; echo "out_EXTRA.txt: uscita $?"
