#!/usr/bin/env bash
# Rifà gli scaricamenti di sciame-dati (f10) con lo script dell'infrastruttura. Rilanciabile: ciò che c'è già
# con l'impronta annotata non viene riscaricato. Uso: bash scarica_tutto.sh   (dalla cartella che si vuole)
set -u
QUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
F10="$(cd "$QUI/../.." && pwd)"
L="$F10/12-dati-veri/registro_scaricamenti.txt"
s() { echo "== $1 $2 $(date -Is)" >> "$L"; bash "$F10/03-infrastruttura/scarica.sh" "$@" --tempo 590 >> "$L" 2>&1; echo "uscita $? $(date -Is)" >> "$L"; }
s tum_fr3_walking_static https://cvg.cit.tum.de/rgbd/dataset/freiburg3/rgbd_dataset_freiburg3_walking_static.tgz 500M --file walking_static.tgz --licenza "CC BY 4.0 (TUM RGB-D benchmark, https://cvg.cit.tum.de/data/datasets/rgbd-dataset)"
LT="CC BY 4.0 (THOR, Zenodo record 3382145, https://zenodo.org/records/3382145)"
s thor https://zenodo.org/api/records/3382145/files/Exp_1_run_1_6D.tsv/content 60M --file Exp_1_run_1_6D.tsv --licenza "$LT"
s thor https://zenodo.org/api/records/3382145/files/Exp_3_run_1_6D.tsv/content 60M --file Exp_3_run_1_6D.tsv --licenza "$LT"
B=https://librealsense.realsenseai.com/rs-tests
LR="non dichiarata nella pagina dei file di esempio (https://github.com/realsenseai/librealsense/blob/master/doc/sample-data.md); non verificata"
s realsense_bag $B/D435i_Depth_and_IMU_Stands_still.bag 120M --file stands_still.bag --licenza "$LR"
s realsense_bag $B/TestData/stairs.bag 420M --file stairs.bag --licenza "$LR"
s realsense_bag $B/TestData/structured.bag 150M --file structured.bag --licenza "$LR"
s princeton_tracking https://tracking.cs.princeton.edu/ValidationSet.zip 650M --licenza "non dichiarata nella pagina https://tracking.cs.princeton.edu/dataset.html (secondo la ricognizione del ricercatore); non verificata"
s depthtrack https://zenodo.org/api/records/5792146/files/human02_indoor.zip/content 600M --file human02_indoor.zip --licenza "CC BY 4.0 (DepthTrack, Zenodo record 5792146, https://zenodo.org/records/5792146)"
echo "== fine $(date -Is)" >> "$L"
