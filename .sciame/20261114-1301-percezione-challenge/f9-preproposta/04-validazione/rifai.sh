#!/bin/sh
# Rifa' tutte le misure del banco S3+S4 (sciame-validazione, f9). Un lancio alla volta, ognuno con timeout 120.
# Uso: sh rifai.sh [gruppo]   (gruppi: 1 2 3 4; senza argomento li fa tutti)
cd "$(dirname "$0")" || exit 1
gcc -O2 -Wall -Wno-misleading-indentation -o banco banco_s3s4.c -lm || exit 1
r() { out="$1"; shift; timeout 120 ./banco "$@" > "$out" 2>&1; echo "$out: uscita $?"; }
g="$1"
if [ -z "$g" ] || [ "$g" = 1 ]; then
r ris_01_p1_pd1_W1_L1_Na.txt -panel 1 -pd 1 -w 1 -l 1 -n 0
r ris_02_p1_pd1_W2_L1_Na.txt -panel 1 -pd 1 -w 2 -l 1 -n 0
r ris_03_p1_pd1_W1_L1_Nb.txt -panel 1 -pd 1 -w 1 -l 1 -n 1
r ris_04_p1_pd1_W2_L1_Nb.txt -panel 1 -pd 1 -w 2 -l 1 -n 1
fi
if [ -z "$g" ] || [ "$g" = 2 ]; then
r ris_05_p1_pd1_W1_L2_Na.txt -panel 1 -pd 1 -w 1 -l 2 -n 0
r ris_06_p1_pd09_W1_L1_Na.txt -panel 1 -pd 0.9 -w 1 -l 1 -n 0
r ris_07_p1_pd09_W2_L1_Nb.txt -panel 1 -pd 0.9 -w 2 -l 1 -n 1
r ris_08_p2_pd1_W1_L1_Na.txt -panel 2 -pd 1 -w 1 -l 1 -n 0
r ris_09_p2_pd1_W2_L1_Nb.txt -panel 2 -pd 1 -w 2 -l 1 -n 1
fi
if [ -z "$g" ] || [ "$g" = 3 ]; then
# attacco 1 alla lettera: 1,2 m/s, sosta di colpo a meta' pannello (7) e transito normale (0)
for w in 1 2; do for n in 0 1; do for pd in 1 0.9; do
r ris_10_att1_ferma_W${w}_N${n}_pd${pd}.txt -panel 1 -pd $pd -w $w -l 1 -n $n -v 1.2 -beh 7
r ris_10_att1_prosegue_W${w}_N${n}_pd${pd}.txt -panel 1 -pd $pd -w $w -l 1 -n $n -v 1.2 -beh 0
done; done; done
fi
if [ -z "$g" ] || [ "$g" = 4 ]; then
r ris_11_ombra_piu10_W1_Na.txt -panel 1 -pd 1 -w 1 -l 1 -n 0 -mask 0.10
r ris_12_ombra_meno10_W1_Na.txt -panel 1 -pd 1 -w 1 -l 1 -n 0 -mask -0.10
r ris_12_ombra_meno20_W1_Na.txt -panel 1 -pd 1 -w 1 -l 1 -n 0 -mask -0.20
r ris_13_senza_ritaglio.txt -panel 1 -pd 1 -w 1 -l 1 -n 0 -clamp 0
r ris_14_seme2_W1_Na.txt -panel 1 -pd 1 -w 1 -l 1 -n 0 -seed 777
r ris_14_seme2_W2_Nb.txt -panel 1 -pd 1 -w 2 -l 1 -n 1 -seed 777
fi
if [ -z "$g" ] || [ "$g" = 5 ]; then
# attacco 2, velocita' tripla, per velocita' d'ingresso (lettura W2, Nb; la porta non dipende dalla lettura)
for v in 0.6 0.9 1.2 1.8; do r ris_15_tripla_v${v}.txt -panel 1 -pd 1 -w 2 -l 1 -n 1 -beh 6 -v $v; done
fi
if [ -z "$g" ] || [ "$g" = 6 ]; then
# braccio «falso libero» sul cuneo per 1 e 3 fotogrammi (0,07 e 0,2 s), transito normale e sosta
for k in 1 3; do
r ris_16_falso${k}_W1_Nb.txt -panel 1 -pd 1 -w 1 -l 1 -n 1 -falso $k
r ris_16_falso${k}_W2_Nb.txt -panel 1 -pd 1 -w 2 -l 1 -n 1 -falso $k
r ris_16_falso${k}_W1_Na.txt -panel 1 -pd 1 -w 1 -l 1 -n 0 -falso $k
done
fi
