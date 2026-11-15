#!/bin/sh
# Rifà simulatore, verifica e prove (f15/10-simulatore e 11-prove). Al più 8 processi; ogni passo con timeout.
# Uso: sh rifai.sh [N_principale=200] [N_variante=50] [N_E3_E4=100] [N_E5_5m=300] [N_E1_E2=20] [N_E5_altre=100]
# Tutto è simulazione: nessuna prova su un sensore fisico.
set -e
QUI=$(cd "$(dirname "$0")" && pwd)
PY=/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f10-dati/ambiente/venv/bin/python
N=${1:-200}; NV=${2:-50}; NE=${3:-100}; N5=${4:-300}; N12=${5:-20}; NS=${6:-100}
cd "$QUI"
date -Is
timeout 300 "$PY" -I -B -c "import sys; sys.path.insert(0,'.'); import sim_lp, json; r=sim_lp.verifica(n=4000); json.dump(r, open('verifica_simulatore.json','w'), ensure_ascii=False, indent=1, default=float); print('V1', r['V1_pd']['fasce_dentro_wilson'])"
MOVI_CHIAMANTE=interfaccia timeout 1500 "$PY" -I -B prove_lp.py "$N" 8
MOVI_CHIAMANTE=prudente timeout 1200 "$PY" -I -B prove_lp.py "$NV" 8
timeout 1500 "$PY" -I -B eventi_lp.py "$NE" 8 "$N5" "$N12" "$NS"
date -Is
