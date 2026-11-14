#!/usr/bin/env bash
# Compila un file di prova con lo stile numerico «plain» e conta errori e avvisi di bibtex.
set -u
qui="$(cd "$(dirname "$0")/.." && pwd)"
d="$qui/prova"; rm -rf "$d"; mkdir -p "$d"; cp "$qui/allegato.bib" "$d/"
cat > "$d/prova.tex" <<'TEX'
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{url}
\begin{document}
Prova della bibliografia.\nocite{*}
\bibliographystyle{plain}
\bibliography{allegato}
\end{document}
TEX
cd "$d" || exit 1
timeout 120 pdflatex -interaction=nonstopmode -halt-on-error prova.tex > latex1.log 2>&1 || { echo "pdflatex 1 fallito"; tail -5 latex1.log; }
timeout 60 bibtex prova > bibtex.log 2>&1; echo "bibtex: codice $?"
grep -c "^Warning--" bibtex.log | sed 's/^/avvisi di bibtex: /'
grep -ci "error" bibtex.log | sed 's/^/righe con «error» in bibtex.log: /'
grep -c '\\bibitem' prova.bbl | sed 's/^/voci nel .bbl: /'
timeout 120 pdflatex -interaction=nonstopmode -halt-on-error prova.tex > latex2.log 2>&1 || { echo "pdflatex 2 fallito"; grep -n "^!" -A3 latex2.log | head -20; }
timeout 120 pdflatex -interaction=nonstopmode -halt-on-error prova.tex > latex3.log 2>&1
grep -c "^!" latex3.log | sed 's/^/errori LaTeX al terzo giro: /'
grep -c "Citation.*undefined\|Missing character" latex3.log | sed 's/^/citazioni indefinite o caratteri mancanti: /'
grep "Output written" latex3.log
