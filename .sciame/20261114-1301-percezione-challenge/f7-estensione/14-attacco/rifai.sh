#!/bin/sh
# Rifa' tutte le prove dell'avversario (f7, fase f4). Semi fissi; ogni lancio sotto i due minuti; uno alla volta.
cd "$(dirname "$0")" || exit 1
timeout 120 python3 -I av1.py > risultati_av1.txt
timeout 120 python3 -I av2_av3_av8.py > risultati_av2_av3_av8.txt
timeout 120 python3 -I av4.py > risultati_av4.txt
timeout 120 python3 -I av5_av6_av7.py > risultati_av5_av6_av7.txt
timeout 120 python3 -I av10.py > risultati_av10.txt
