#!/bin/sh
# rifai.sh — rifa' tutta la prova d'insieme (sciame-validazione, f12, C-C). Da lanciare in questa cartella: sh rifai.sh
# Tempo: circa 3-4 minuti con 4 processi leggeri in parallelo (P=1 per farli uno alla volta: circa 10 minuti).
# I risultati di un giro precedente NON si perdono: ris/ viene spostata in ris_prec_<ora>/.
set -e
cd "$(dirname "$0")"
P=${P:-4}
PY=/home/fede/Scrivania/ed/GitHub/Movi-Hackthon/.sciame/20261114-1301-percezione-challenge/f10-dati/ambiente/venv/bin/python
ATT=../../f8-continuita/14-attacco/att.c
T0=$(date +%s)
[ -d ris ] && mv ris "ris_prec_$(date +%Y%m%dT%H%M%S)"
mkdir -p ris
"$PY" -I -B componi.py "$ATT" insieme.c > ris/componi.txt
diff "$ATT" insieme.c > DIFFERENZE.txt || true
gcc -O2 -Wall -Wno-misleading-indentation -o insieme insieme.c -lm
sha256sum "$ATT" componi.py insieme.c > ris/IMPRONTE.txt
timeout 60 ./insieme semi > ris/semi.txt
# INS = c1 + c2 + c3 (forma simulabile) + c4 + c5 + c7, sopra M1-M8. In D c1 e' «senza il margine dalla portata».
INS="rh=0.75 assorb=0 m1n=2 vmin=0.3 c3=1 c7=1"
: > ris/comandi.txt
C() { echo "$*" >> ris/comandi.txt; }
bd() { if [ "$1" = D ]; then echo "bordo=0"; fi; }
for g in D T L; do
  # (b) precisione, (f) riaggancio: corpo esteso, rilevamento 0,9, maschera esatta
  if [ $g = D ]; then n=4000; else n=2400; fi
  C b_${g}_percorso prova geo=$g n=$n beh=01236 $INS $(bd $g)
  C b_${g}_parte prova geo=$g n=$n beh=458 $INS $(bd $g)
  # (a) continuita' e (e) sicurezza: rilevamento 0,9 e 0,7, puntiforme ed esteso, con c7 e senza
  for pd in 0.9 0.7; do for c7 in 1 0; do
    C a_${g}_pd${pd}_esteso_c7$c7 prova geo=$g pd=$pd n=400 beh=01236 $INS $(bd $g) c7=$c7
    C a_${g}_pd${pd}_punto_c7$c7 prova geo=$g pd=$pd rb=0 c6=0.22 n=400 beh=01236 $INS $(bd $g) c7=$c7
  done; done
  # (c) K-215: ombra stimata piu' stretta, corpo esteso; senza c3, con c3, con c3 che manca il bordo 2 cicli su 10
  if [ $g = T ]; then pds="0.9 0.7"; n=800; else pds="0.9"; n=400; fi
  for e in -0.10 -0.20; do for pd in $pds; do
    C c_${g}_e${e}_pd${pd}_c3no prova geo=$g e=$e pd=$pd n=$n beh=01236 $INS $(bd $g) c3=0
    C c_${g}_e${e}_pd${pd}_c3si prova geo=$g e=$e pd=$pd n=$n beh=01236 $INS $(bd $g)
    C c_${g}_e${e}_pd${pd}_c3p08 prova geo=$g e=$e pd=$pd n=$n beh=01236 $INS $(bd $g) c3p=0.8
  done; done
  # (d) estraneo mai visto che esce dalla stessa ombra: con c1 e con la regola di prima (0,40 m e margine dalla portata)
  C d_${g}_c1si prova geo=$g n=2000 beh=26 $INS $(bd $g) estr=1
  C d_${g}_c1no prova geo=$g n=2000 beh=26 $INS rh=0.40 bordo=1 estr=1
  # (e) chiusura «fuori dall'area osservata»: forma debole (punto del filtro fuori area), che lascia o toglie l'avviso; forma scritta
  C e_${g}_ch5debole_lascia prova geo=$g n=400 beh=56 $INS $(bd $g) ch5=2
  C e_${g}_ch5debole_toglie prova geo=$g n=400 beh=56 $INS $(bd $g) ch5=2 toglie=1
  C e_${g}_ch5scritta prova geo=$g n=400 beh=56 $INS $(bd $g) ch5=1
  # c5: chi parte da fermo; senza c5, con c5, con «fermo negli ultimi 2 s»
  C f_${g}_fermo_c5no prova geo=$g n=800 beh=8 $INS $(bd $g) vmin=0
  C f_${g}_fermo_c5b prova geo=$g n=800 beh=8 $INS $(bd $g) c5b=1
  # c2: sessione di 120 passaggi di fila
  C s_${g} sessione geo=$g $INS $(bd $g)
done
# un lancio = un processo a un filo, meno di 20 MB, tempo massimo 280 s
xargs -P "$P" -L 1 sh -c 'out=$0; timeout 280 ./insieme "$@" nome=$out > ris/$out.txt || echo "FALLITO $out" >> ris/falliti.txt' < ris/comandi.txt
if [ -f ris/falliti.txt ]; then cat ris/falliti.txt; fi
# (g) costo: da solo, senza altri lanci
for g in D T L; do for r in 1 2 3; do timeout 120 ./insieme tempo geo=$g n=10 | tail -1; done; done > ris/tempo_C.txt
"$PY" -I -B leggi.py ris > ris/TABELLE.txt
echo "rifatto in $(( $(date +%s) - T0 )) s; $(ls ris | wc -l) file in ris/" | tee ris/DURATA.txt
