#!/usr/bin/env bash
# Rifà tutti i controlli del fascicolo 06. Con «--rete» riapre anche i registri bibliografici.
set -u
qui="$(cd "$(dirname "$0")/.." && pwd)"; p="$qui/programmi"
prog="$(cd "$qui/../../../.." && pwd)"   # radice del progetto
py="python3 -I -B"
[ "${1:-}" = "--rete" ] && timeout 300 bash "$p/scarica.sh" | cut -f2,3
echo "== elenco"; timeout 60 $py "$p/leggi_elenco.py" "$prog/documentazione/RIFERIMENTI.md" "$p/elenco.json"
echo "== conteggi"; grep -v '^#' "$p/candidate.txt" | cut -d: -f2 | wc -w | sed 's/^/candidate: /'; grep -v '^#' "$p/citabili.txt" | cut -d: -f2 | wc -w | sed 's/^/citabili: /'
echo "== bib"; timeout 60 $py "$p/costruisci_bib.py" "$prog/documentazione/riferimenti.bib" "$p/citabili.txt" "$p/voci_aggiunte.bib" "$qui/allegato.bib"
timeout 60 $py "$p/controlla_bib.py" "$qui/allegato.bib" "$p/citabili.txt" "$p/elenco.json"
echo "== bibtex"; bash "$p/prova_bibtex.sh"
echo "== registri (copie in scaricati/)"; timeout 60 $py "$p/leggi_crossref.py" "$qui/scaricati/crossref" 0 | grep -c '^==' | sed 's/^/risposte Crossref leggibili: /'
echo "== conti"; timeout 30 $py "$p/ricalcoli.py"
echo "== parte I"; timeout 30 $py "$p/controlla_parte1.py" "$qui/FASCICOLO_BIBLIOGRAFIA.md" "$qui/allegato.bib"
