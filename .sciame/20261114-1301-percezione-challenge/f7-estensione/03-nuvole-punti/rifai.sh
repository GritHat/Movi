#!/bin/sh
# Rifa' le prove di sciame-nuvole-punti (f7). Un lancio alla volta, ciascuno sotto i due minuti. Seme fisso nel codice (20261114).
cd "$(dirname "$0")" || exit 1
gcc -O2 -o sim3d sim3d.c -lm || exit 1
timeout 120 ./sim3d scene      > risultati_scene.txt
timeout 120 ./sim3d sweep      > risultati_sweep.txt
timeout 120 ./sim3d rumore     > risultati_rumore.txt
timeout 120 ./sim3d scene zona > risultati_scene_zona.txt   # variante aggiunta dopo le previsioni
