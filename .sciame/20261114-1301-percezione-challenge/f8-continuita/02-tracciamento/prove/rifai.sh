#!/bin/sh
# Rifa' tutte le prove di sciame-tracciamento (f8). Ogni lancio <= 2 minuti, uno alla volta, semi fissati.
cd "$(dirname "$0")"; export PYTHONDONTWRITEBYTECODE=1
gcc -O2 -o cont_v1 cont_v1.c -lm; gcc -O2 -o cont cont.c -lm
timeout 120 python3 gen_traj.py 1.0 2.0 6.0 4.0 400 8100 > traj_T1.txt
timeout 120 python3 gen_traj.py 1.0 2.0 6.0 4.0 400 9200 > traj_V1.txt
timeout 120 python3 gen_traj.py 2.0 2.0 6.0 4.0 400 9300 > traj_V2.txt
timeout 120 python3 gen_traj.py 1.0 1.9 3.0 2.3 400 9400 > traj_V3.txt
timeout 120 ./cont_v1 traj_T1.txt 2.0 6.0 0 0 81 > ris_T1_v1.txt          # primo lancio, previsioni T1-T11
timeout 120 ./cont traj_T1.txt 2.0 6.0 0 0 81 > tar_T1_cal.txt            # taratura (livelli nominali)
# i tre lanci tar_T1_LT*.txt (tasso di svolta 0.3, 0.6, 1.0) vengono da cont_v2.c: gcc -O2 -o cont_v2 cont_v2.c -lm; LT=0.6 ./cont_v2 traj_T1.txt 2.0 6.0 0 0 81
export L50="0.209 0.302 0.507 0.348 0.337 0.274" L90="0.672 0.744 0.983 0.866 0.841 0.870"
export W50="0.314 0.473 0.885 0.558 0.541 0.625" W90="0.734 0.905 0.986 0.987 0.985 0.984"
timeout 120 ./cont traj_V1.txt 2.0 6.0 0 0 92 > ris_V1.txt                # convalida, stessa geometria, semi nuovi
timeout 120 ./cont traj_V2.txt 2.0 6.0 0 0 93 > ris_V2.txt                # pannello da 2 m
timeout 120 ./cont traj_V3.txt 1.9 3.0 0 0 94 > ris_V3.txt                # geometria della demo
timeout 120 ./cont traj_V2.txt 2.0 6.0 0 0 93 2000 > espl_V2_np2000.txt   # esplorativo, 2000 particelle, livelli tarati ancora esportati
unset L50 L90 W50 W90
export HYB=1                                                              # giro finale: 2000 particelle, punto ibrido su d1
timeout 120 ./cont traj_V1.txt 2.0 6.0 0 0 92 2000 > fin_V1.txt
timeout 120 ./cont traj_V2.txt 2.0 6.0 0 0 93 2000 > fin_V2.txt
timeout 120 ./cont traj_V3.txt 1.9 3.0 0 0 94 2000 > fin_V3.txt
# tabelle: python3 tabella.py fin_V1.txt "d1 +sosta" c90   (colonne: err p90 c50 c90 a50 a90 punt lib)
# nota: nei file fin_* la riga "d3 ibr. tar." porta il PUNTO ibrido su d1 (HYB=1); le sue colonne di regione sono di d3 e non si usano
