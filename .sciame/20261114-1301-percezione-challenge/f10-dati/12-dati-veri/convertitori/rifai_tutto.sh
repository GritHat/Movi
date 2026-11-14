#!/usr/bin/env bash
# Rifà tutto da zero: scaricamenti, apertura degli archivi, conversioni, controlli, statistiche, manifesto.
# Uso: bash rifai_tutto.sh     (le cartelle sequenze/<nome> e tracce/<nome> già presenti NON vengono sovrascritte:
# i convertitori si fermano; per rifarle vanno tolte a mano). Un processo alla volta, ognuno con il suo tempo massimo.
set -u
QUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; F10="$(cd "$QUI/../.." && pwd)"
PY="$F10/ambiente/venv/bin/python"; S="$F10/scaricati"; export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
timeout 3000 bash "$QUI/scarica_tutto.sh"
apri() { [ -d "$2" ] || timeout 280 python3 -I "$F10/03-infrastruttura/apri_archivio.py" "$1" "$2" --tetto "$3"; }
apri "$S/tum_fr3_walking_static/walking_static.tgz" "$S/tum_fr3_walking_static/aperto" 1500M
apri "$S/princeton_tracking/ValidationSet.zip" "$S/princeton_tracking/aperto" 800M
apri "$S/depthtrack/human02_indoor.zip" "$S/depthtrack/aperto" 800M
c() { timeout 280 "$PY" -I -B "$QUI/$1" "${@:2}"; }
c converti_tum.py "$S/tum_fr3_walking_static/aperto/rgbd_dataset_freiburg3_walking_static" tum_fr3_walking_static
for b in stands_still stairs structured; do c converti_realsense_bag.py "$S/realsense_bag/$b.bag" "realsense_$b"; done
for q in child_no1 new_ex_occ4 face_occ5; do c converti_princeton.py "$S/princeton_tracking/aperto/ValidationSet" "$q" "princeton_$q"; done
c converti_depthtrack.py "$S/depthtrack/aperto/human02_indoor" depthtrack_human02_indoor
c converti_thor.py "$S/thor/Exp_1_run_1_6D.tsv" thor_exp1_run1
c converti_thor.py "$S/thor/Exp_3_run_1_6D.tsv" thor_exp3_run1
c statistiche_tutte.py
c scrivi_manifesto.py
c verifica_suolo_tum.py "$S/tum_fr3_walking_static/aperto/rgbd_dataset_freiburg3_walking_static" "$F10/12-dati-veri/sequenze/tum_fr3_walking_static"
c verifica_piano.py "$F10/12-dati-veri/sequenze/realsense_stands_still" 60
