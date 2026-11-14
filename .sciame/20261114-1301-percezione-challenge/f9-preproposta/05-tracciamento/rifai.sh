#!/bin/sh
# Rifa' i quattro lanci del banco degli eventi (sciame-tracciamento, f9). Ognuno sotto i 30 s; uno alla volta.
# Uso: sh rifai.sh   (dalla cartella di questo file)
cd "$(dirname "$0")" || exit 1
timeout 120 python3 eventi_sim.py 400 0.9 0.0  > ris_pd09.txt
SMOOTH=6 timeout 120 python3 eventi_sim.py 400 0.9 0.0 > ris_pd09_smooth6.txt
timeout 120 python3 eventi_sim.py 400 0.9 0.02 > ris_pd09_pf002.txt
timeout 120 python3 eventi_sim.py 400 0.7 0.0  > ris_pd07.txt
# per leggere: python3 estrai.py ris_pd09.txt P7_ RIAPP_ LINEA_ G_
