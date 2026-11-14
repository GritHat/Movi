#!/bin/sh
# Rifa tutte le prove di sciame-statistico (f8, corsia A). Un lancio alla volta, ciascuno sotto timeout 120. Semi fissati negli script.
cd "$(dirname "$0")" || exit 1
for m in tabelle misure fotogrammi conforme unione incrociata; do
  PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -B misure_f8.py $m > out_$m.txt 2>&1
done
timeout 60 python3 -B h9_cieco.py > out_h9.txt
