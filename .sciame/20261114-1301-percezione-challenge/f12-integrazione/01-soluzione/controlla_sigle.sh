#!/bin/sh
# Controllo meccanico di completezza (P-int-1, P-int-2, P-int-4). Uso: sh controlla_sigle.sh  (dalla cartella 01-soluzione)
# Sola lettura; nessuna rete. Condivide con cio' che controlla: l'autore e l'elenco delle sigle (scritto da me).
T=TABELLA_CORREZIONI.md; S=SOLUZIONE_V3.md; manca=0; tot=0
for s in VN-1 VN-2 VN-3 VN-4 VN-5 VN-6 VN-7 VN-8 VN-9 VN-10 \
         AU-1 AU-2 AU-3 AU-4 AU-5 AU-6 AU-7 AU-8 AU-9 AU-10 AU-11 AU-12 \
         V7-a V7-b V7-c V7-d V7-e V7-f V7-g V7-h \
         "A7 §3.1" "A7 §3.2" "A7 §3.3" "A7 §3.4" "A7 §3.5" "A7 §3.6" "A7 §3.7" "A7 §3.8" "A7 §3.9" "A7 §3.10" \
         "| M1 " "| M2 " "| M3 " "| M4 " "| M5 " "| M6 " "| M7 " "| M8 " \
         "| c1 " "| c2 " "| c3 " "| c4 " "| c5 " "| c6 " "| c7 " "| c8 " "| c9 " "| c10 " \
         statistico-3 statistico-4 statistico-5 statistico-6 statistico-7 \
         "V8 §4.1 " "V8 §4.2" "V8 §4.3" "V8 §4.4" "V8 §4.5" "V8 §4.6" "V8 §4.7" "V8 §4.8" "V8 §4.9" "V8 §4.10" \
         "| S1 " "| S2 " "| S3 " "| S4 " "| S5 " "| S6 " "| S7 " "| S8 " "| S9 " "| S10 " "| S11 " "| S12 " \
         F-401 F-402 F-403 F-404 F-405 F-406 F-407 F-408 F-409 F-410 F-411 F-412 F-413 \
         "| C1 " "| C2 " "| C3 " "| C4 " "| C5 " "| C6 " "| C7 " "| C8 "; do
  tot=$((tot+1))
  if ! grep -q -F -- "$s" "$T"; then echo "MANCA nella tabella: $s"; manca=$((manca+1)); fi
done
echo "sigle controllate: $tot; mancanti: $manca"
echo "--- paragrafi citati nella tabella che non esistono nel documento"
for p in $(grep -o '§1\.[0-9]*' "$T" | sort -u); do n=${p#§}; grep -q "^### $n " "$S" || echo "MANCA paragrafo $p"; done
for i in $(grep -o 'I[0-9][0-9]*' "$T" | sort -u); do grep -q "^| $i |" "$S" || echo "MANCA invariante $i"; done
echo "--- frasi da non dire: righe di $S che le contengono (da leggere una per una)"
grep -n -i -E "validat|via libera|garantit|certificat|bassa latenza|sosta in ombra|360°|tarato" "$S" | cut -c1-170
echo "--- parole (solo gettoni con una lettera o una cifra)"
tr -s '[:space:]' '\n' < "$S" | grep -c '[[:alnum:]]'
tr -s '[:space:]' '\n' < "$T" | grep -c '[[:alnum:]]'
