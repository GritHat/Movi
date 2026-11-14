#!/bin/sh
# Chiusura dell'anomalia Pd 0,9 / -20 cm. Un lancio alla volta, al piu' 120 s ciascuno.
cd "$(dirname "$0")" || exit 1
t() { o="$1"; shift; ( time timeout 120 python3 sim_v2bis.py "$@" ) > "$o" 2>&1; echo "$o: uscita $?"; }
t bis_R8a.txt R8 400 a
t bis_R8b.txt R8 400 b
t bis_DAVANTI.txt DAVANTI 4000
t bis_FURTO.txt FURTO 400
