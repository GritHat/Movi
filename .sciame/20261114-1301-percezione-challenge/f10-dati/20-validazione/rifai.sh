#!/bin/sh
# Rifà tutte le misure di 20-validazione, nell'ordine. Da lanciare da f10-dati/20-validazione; ogni passo ha il suo
# tempo massimo (al più 5 minuti). Un filo solo (lo impone comune.py). Non scrive fuori da questa cartella.
set -u
PY="../ambiente/venv/bin/python -I -B"
timeout 290 $PY corri_sim.py                                              # la catena, parametri del nucleo → uscite/sim (62 s)
timeout 200 $PY corri_sim.py --etichetta sim_p40 -p min_punti_ostacolo=40  # → uscite/sim_p40 (11 s)
for e in sim sim_p40; do
  timeout 280 $PY misura_libero.py   $e > uscite/$e/misura_libero.txt      # misura 1 (K-014, celle per stato, falsi occupati)
  timeout 280 $PY misura_ombra.py    $e > uscite/$e/misura_ombra.txt       # misura 2 (bordo d'ombra, filtri, classe 2)
  timeout 280 $PY misura_passaggi.py $e > uscite/$e/misura_passaggi.txt    # misure 3 (in moto), 4, 5 (pannello «si muove»)
  timeout 100 $PY misura_ostacoli.py $e > uscite/$e/misura_ostacoli.txt    # misura 5 (ostacoli per scena)
done
timeout 290 $PY taratura.py tara        > uscite/taratura_tara.txt         # V23: 8 coppie di soglie sui passaggi pari (70 s)
( timeout 120 $PY taratura.py prova 20 1; timeout 120 $PY taratura.py prova 40 1 ) > uscite/taratura_prova.txt
( timeout 120 $PY sim_memoria.py coperto; timeout 200 $PY sim_memoria.py bordi 3 ) > uscite/mem_coperto_bordi.txt   # V24, V22
( timeout 290 $PY sim_memoria.py fermi 3 0,1; timeout 290 $PY sim_memoria.py fermi 3 2,3,4; timeout 140 $PY sim_memoria.py fermi 40 ) > uscite/mem_fermi.txt
( timeout 285 $PY sim_memoria.py lenti 40; timeout 290 $PY sim_memoria.py lenti 3 0,3 ) > uscite/mem_lenti.txt       # V11
timeout 280 $PY banco_thor.py           > uscite/banco_thor.txt            # misura 4 su pedoni veri (4 s)
rm -f uscite/vere/RIEPILOGO.jsonl
for s in tum realsense_stands realsense_stairs realsense_structured; do timeout 100 $PY corri_vere.py $s 120 > /dev/null; done
timeout 290 $PY corri_vere.py depthtrack 320 > /dev/null                    # 41 s
for s in princeton_new princeton_child princeton_face; do timeout 120 $PY corri_vere.py $s 170 > /dev/null; done
python3 vedi_vere.py uscite/vere/RIEPILOGO.jsonl > uscite/vere/RIEPILOGO.txt
timeout 200 $PY misure_brevi.py         > uscite/misure_brevi.txt           # costo, sensore coperto, THÖR q = 0,1
# un passaggio fotogramma per fotogramma (casi minimi citati nel rapporto):
#   $PY diagnosi.py sim d455_nom__pannello_a12__s00 8 40
