#!/bin/sh
# Compila il documento definitivo: xelatex, bibtex, xelatex, xelatex (180 s ciascuno) e riassume il registro.
cd "$(dirname "$0")/.." || exit 1
timeout 180 xelatex -interaction=nonstopmode -halt-on-error allegato_tecnico.tex > strumenti/x1.txt 2>&1; echo "xelatex 1: $?"
timeout 180 bibtex allegato_tecnico > strumenti/b.txt 2>&1; echo "bibtex: $?"
timeout 180 xelatex -interaction=nonstopmode -halt-on-error allegato_tecnico.tex > strumenti/x2.txt 2>&1; echo "xelatex 2: $?"
timeout 180 xelatex -interaction=nonstopmode -halt-on-error allegato_tecnico.tex > strumenti/x3.txt 2>&1; echo "xelatex 3: $?"
echo "avvisi di BibTeX: $(grep -c 'Warning--' strumenti/b.txt)"
echo "errori (righe con !): $(grep -c '^!' allegato_tecnico.log)"
echo "riferimenti o citazioni indefiniti: $(grep -ci 'undefined' allegato_tecnico.log)"
echo "Overfull hbox: $(grep -c 'Overfull .hbox' allegato_tecnico.log)"
grep 'Overfull .hbox' allegato_tecnico.log | sort -t'(' -k2 -rn | head -5
echo "Float too large: $(grep -c 'Float too large' allegato_tecnico.log)"
grep 'Output written' allegato_tecnico.log
