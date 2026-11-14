#!/bin/sh
# Controlli Q1, Q2, Q7 sul documento finale. Solo lettura, solo strumenti di base.
F=SCHERMO_E_DEMO.md
echo "== Q1: frasi «da non dire» fuori dal paragrafo 6"
awk '/^## 6\./{s=1} /^## 7\./{s=0} !s' "$F" > /tmp/claude-1000/-home-fede-Scrivania-ed-GitHub-Movi-Hackthon/5e23f93d-4455-4e40-867d-5818514a7c35/scratchpad/fuori6.txt 2>/dev/null || awk '/^## 6\./{s=1} /^## 7\./{s=0} !s' "$F" > fuori6.tmp
T=/tmp/claude-1000/-home-fede-Scrivania-ed-GitHub-Movi-Hackthon/5e23f93d-4455-4e40-867d-5818514a7c35/scratchpad/fuori6.txt; [ -f "$T" ] || T=fuori6.tmp
tot=0
while IFS= read -r frase; do
  n=$(grep -o $(case "$frase" in NOMINAL|HOLD|ACAS|UAV) ;; *) printf %s -i;; esac) -F -- "$frase" "$T" | wc -l); tot=$((tot+n))
  [ "$n" -gt 0 ] && echo "  $n  «$frase»"
done <<'FRASI'
validato
certificato
garantit
tarato
via libera
nessun ostacolo osservato
bassa latenza
prevede dove sarà
continuità garantita
100 %
mai dato per libero
solo guardando
mappa 3D
voxel
360°
ACAS
TA/RA
anti-bird
detect and avoid
minaccia
NOMINAL
HOLD
FAIL-SAFE
preallarme
drone
UAV
in volo
orientamento
dispositivo medico
conforme a
ispezione
Intelligenza Artificiale
massa e accelerazione
riconosce la sosta
si è fermato
è uscito
30 prove bastano
ellisse al 95
identità mantenuta
soglia 40
15 Hz
validato su dati veri
dal vivo
in cinque ci sta
adottata
0,85 m
FRASI
echo "  totale fuori dal paragrafo 6: $tot"
echo "== Q2: stati della versione 3 contro righe della tabella dei segni"
manca=0; n=0
grep -v '^#' stati_v3.txt | while IFS= read -r riga; do
  k=${riga%% *}
  grep -q "^| $k " "$F" || echo "  SENZA SEGNO: $riga"
done
st=$(grep -vc '^#' stati_v3.txt)
ri=$(awk '/^\| Stato \(V3\)/{s=1;next} s&&/^\|---/{next} s&&/^\|/{c++} s&&!/^\|/{s=0} END{print c}' "$F")
echo "  stati nell'elenco: $st; righe della tabella dei segni: $ri"
awk '/^\| Stato \(V3\)/{s=1;next} s&&/^\|---/{next} s&&/^\|/{split($0,a," "); print a[2]} s&&!/^\|/{s=0}' "$F" | while read k; do grep -q "^$k " stati_v3.txt || echo "  RIGA SENZA STATO: $k"; done
echo "== Q7: lunghezza"
wc -w -c "$F"
