#!/bin/sh
# Rifa' le prove dell'attacco (sciame-avversario, f8 f4). Da eseguire in questa cartella; un lancio alla volta, ognuno <= 120 s.
set -e
gcc -O2 -Wall -Wno-misleading-indentation -o att att.c -lm
mkdir -p ris
R() { out=$1; shift; timeout 120 ./att "$@" > ris/$out.txt; }
# P-av-1, 6, 7: base con corpo 0,45 m e C6 a una cella; sensibilita' a 0,05 m; soggetto puntiforme a 0,22 m (come il banco)
for g in D T L; do R base_$g prova geo=$g n=400 beh=0123; R punto_$g prova geo=$g rb=0 c6=0.22 n=400 beh=0123; R c605_$g prova geo=$g c6=0.05 n=400 beh=0123; done
R demo_D prova geo=D vlo=0.8 vhi=1.5 n=400 beh=0
# P-av-2, P-av-10: sessione di 120 passaggi
for g in D T L; do R sess_$g sessione geo=$g; R sess_punto_$g sessione geo=$g rb=0 c6=0.22; done
# P-av-3: tutto insieme
R tutto_T prova geo=T e=-0.20 pd=0.7 n=400 beh=0123
R tutto_T_pd09 prova geo=T e=-0.20 pd=0.9 n=400 beh=0123
R tutto_T_e0_pd07 prova geo=T pd=0.7 n=400 beh=0123
R tutto_T_e10 prova geo=T e=-0.10 pd=0.7 n=400 beh=0123
R tutto_T_punto prova geo=T e=-0.20 pd=0.7 rb=0 c6=0.22 n=400 beh=0123
R tutto_D prova geo=D e=-0.20 pd=0.7 n=400 beh=0123
# P-av-4: sbircia e fermo in vista
for g in D T; do R sbircia_$g prova geo=$g n=400 beh=7; R fermo_$g prova geo=$g n=400 beh=8; done
R fermo_T_pd07 prova geo=T pd=0.7 n=400 beh=8
R fermo_T_punto prova geo=T rb=0 c6=0.22 n=400 beh=8
# P-av-5: taratura fuori distribuzione
for w in 0 3 6 10; do R curva_T_$w prova geo=T omega=$w n=400 beh=9; R curva_L_$w prova geo=L omega=$w n=400 beh=9; done
R lib30_calmi_su_vivaci_T prova geo=T nlib=30 libviv=0 viv=1 n=400 beh=0123
R lib200_vivaci_su_vivaci_T prova geo=T nlib=200 libviv=1 viv=1 n=400 beh=0123
R lib30_calmi_su_calmi_T prova geo=T nlib=30 n=400 beh=0123
R lib200_calmi_su_vivaci_T prova geo=T libviv=0 viv=1 n=400 beh=0123
# P-av-9: errore d'imbardata della maschera stimata
R imb_trem1_T prova geo=T yawj=1 n=200 beh=0123
R imb_trem2_T prova geo=T yawj=2 n=200 beh=0123
R imb_fisso3_T prova geo=T yawb=3 n=400 beh=0123
R imb_fisso6_T prova geo=T yawb=6 n=400 beh=0123
# P-av-8: costo in C, con le pendenti accumulate
for n in 1 10 60 120; do timeout 120 ./att tempo geo=T n=$n | tail -1; done > ris/tempo_C.txt
# ---- aggiunti DOPO la prova principale (17:10): misure in piu' e bracci di correzione; att.c del primo giro = att_congelato_1704.c ----
PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 tempo_py.py > ris/tempo_py.txt
for g in D T L; do R dopo_base_$g prova geo=$g n=400 beh=0123; R dopo_rh075_$g prova geo=$g rh=0.75 n=400 beh=0123; done
R dopo_rh075_senzabordo_D prova geo=D rh=0.75 bordo=0 n=400 beh=0123
R dopo_demo_D prova geo=D vlo=0.8 vhi=1.5 n=400 beh=0
for g in D T; do R dopo_sess_corr_$g sessione geo=$g rh=0.75 assorb=0; done
R dopo_sess_corr_senzabordo_D sessione geo=D rh=0.75 assorb=0 bordo=0
R dopo_fermo_T_vmin prova geo=T vmin=0.3 n=400 beh=8
R dopo_fermo_T_m1n2 prova geo=T m1n=2 n=400 beh=8
R dopo_base_T_m1n2 prova geo=T m1n=2 n=400 beh=0123
R dopo_base_T_m1n2_pd07 prova geo=T m1n=2 pd=0.7 n=400 beh=0123
R dopo_tutte_T prova geo=T rh=0.75 assorb=0 vmin=0.3 m1n=2 n=400 beh=01238
R dopo_tutte_D prova geo=D rh=0.75 assorb=0 vmin=0.3 m1n=2 bordo=0 n=400 beh=01238
