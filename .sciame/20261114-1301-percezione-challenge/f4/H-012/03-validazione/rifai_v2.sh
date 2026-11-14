#!/bin/sh
# Rifa la riprova dell'insieme (versione 2). Un lancio alla volta, al piu' 120 s ciascuno.
cd "$(dirname "$0")" || exit 1
t() { o="$1"; shift; ( time timeout 120 python3 sim_v2.py "$@" ) > "$o" 2>&1; echo "$o: uscita $?"; }
t v2_R8.txt R8 400
t v2_R8_cut.txt R8 400 1.0 cut
t v2_R8_pd09.txt R8 400 0.9
t v2_C6.txt C6 2000
t v2_SECOND.txt SECOND 400
t v2_MOB.txt MOB 2000
t v2_WALLP.txt WALLP 400
t v2_PD.txt PD 20000
