#!/bin/sh
# Rifà gli attacchi di 22-avversario. Da lanciare da f10-dati/; ogni passo ha il suo tempo massimo. Un filo solo.
# Non scrive fuori da 22-avversario/ (uscite/a8/ è intermedio e rigenerabile: non va nel deposito).
set -u
PY="ambiente/venv/bin/python -I -B"
D=22-avversario
timeout 280 $PY $D/a1_posa.py                 > $D/uscite/a1_posa.txt                        # A1: posa sbagliata (20 s)
timeout 280 $PY $D/a234_scene.py              > $D/uscite/a234_scene.txt                     # A2, A3, A4: scene a mano
timeout 280 $PY $D/a5_thor.py                 > $D/uscite/a5_thor.txt                        # A5: THÖR nelle condizioni della catena
timeout 280 $PY $D/a678_sim.py a6             > $D/uscite/a6_ombra.txt                       # A6: ingrossamento dei bordi
timeout 280 $PY $D/a678_sim.py a6 0.484       > $D/uscite/a6bis_ombra_spigolo_15p05.txt      # A6bis: spigolo a 15,05°
timeout 120 $PY $D/a678_sim.py a7             > $D/uscite/a7_verita.txt                      # A7: tre fotogrammi della verità
timeout 290 $PY $D/a678_sim.py a8 z23 z21 z20 > $D/uscite/a8_soglia40_linea.txt              # A8a: linea a 2,1 m (60 s)
timeout 295 $PY $D/a678_sim.py a8 w848        > $D/uscite/a8_soglia40_848.txt                # A8b: 848×480 (35 s)
