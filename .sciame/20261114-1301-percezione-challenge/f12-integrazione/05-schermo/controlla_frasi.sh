#!/bin/sh
# P-int-6: parole del testo e frasi «da non dire» fuori dal paragrafo 7 di SCHERMO_E_DEMO.md. Sola lettura.
F=SCHERMO_E_DEMO.md
echo "parole (wc -w): $(wc -w < $F)   (soglia scritta prima: 3100)"
# tutto il testo tranne il paragrafo 7 (da '## 7.' fino a '## 8.' escluso)
awk '/^## 7\./{s=1} /^## 8\./{s=0} !s' $F > /dev/null
N=$(awk '/^## 7\./{s=1} /^## 8\./{s=0} !s' $F | grep -n -i -E 'validat|certificat|garantit|tarato|via libera|bassa latenza|prevede dove|30 prove|confidenza|conf Z|±|riconosce la sosta|si è fermato dietro|è uscito|sosta in ombra|15 cicli al secondo|mappa 3D|voxel|ostacoli bassi|360|ACAS|TA/RA|bird|detect and avoid|minaccia|NOMINAL|HOLD|FAIL-SAFE|preallarme|drone|UAV|in volo|in movimento|orientamento|dispositivo medico|conforme a|ispezione|Intelligenza Artificiale|massa e|è stata adottata|in cinque ci sta|taglio garantito|il vetro è risolto' || true)
if [ -z "$N" ]; then echo "frasi da non dire fuori dal paragrafo 7: 0"; else echo "frasi da non dire fuori dal paragrafo 7:"; echo "$N"; fi
echo "«dal vivo» fuori dal paragrafo 7 (ammessa solo nell'etichetta CAMERA DAL VIVO):"
awk '/^## 7\./{s=1} /^## 8\./{s=0} !s' $F | grep -n -i -o -E '.{0,25}dal vivo.{0,10}' || true
# pagine: stessa misura dell'arbitro di f7 (pandoc e xelatex, A4, corpo 10, margini 1,8 cm); il PDF va in una cartella temporanea
T=$(mktemp -d) && timeout 100 pandoc $F -o $T/s.pdf --pdf-engine=xelatex -V geometry:a4paper,margin=1.8cm -V fontsize=10pt 2>/dev/null && echo "pagine: $(pdfinfo $T/s.pdf | grep -i pages | tr -s ' ' | cut -d' ' -f2)   (limite 4)"; rm -rf "$T"
