#!/bin/sh
# Rifà conti e controlli di 22-schermo-finale (pochi secondi). Lanciare da questa cartella.
PY=../../f10-dati/ambiente/venv/bin/python
timeout 60 "$PY" -I -B conti_finali.py > risultati_conti.txt && echo "conti: risultati_conti.txt"
timeout 60 sh controlla.sh > esito_controlli.txt && cat esito_controlli.txt
# pagine (facoltativo, serve pandoc con xelatex; scrive solo in una cartella temporanea):
# pandoc SCHERMO_E_DEMO.md -o /tmp/p.pdf --pdf-engine=xelatex -V papersize=a4 -V documentclass=extarticle -V fontsize=9pt -V geometry:margin=1.5cm -V mainfont="Noto Serif" -V monofont="DejaVu Sans Mono"; pdfinfo /tmp/p.pdf | grep Pages
