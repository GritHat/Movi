#!/usr/bin/env bash
# Riapre le fonti in rete: solo DOI, identificativi arXiv e indirizzi pubblici. Il materiale va in scaricati/ e non si esegue.
set -u
qui="$(cd "$(dirname "$0")" && pwd)"; dest="$qui/../scaricati"; mkdir -p "$dest"
: > "$dest/esito_richieste.tsv"
scarica() { f="$1"; u="$2"; c=$(timeout 40 curl -sS -L -m 35 -A "verifica-bibliografica/1.0" -o "$dest/$f" -w "%{http_code}" "$u" 2>/dev/null); echo -e "$f\t$u\t${c:-fallita}\t$(stat -c %s "$dest/$f" 2>/dev/null || echo 0)" >> "$dest/esito_richieste.tsv"; }
export -f scarica; export dest
# 3 richieste alla volta; arXiv in serie con pausa per non avere 429
grep -v "arxiv.org" "$qui/elenco_richieste.tsv" | xargs -P 3 -d '\n' -I{} bash -c 'IFS=$'"'"'\t'"'"' read -r f u <<< "{}"; scarica "$f" "$u"'
grep "arxiv.org" "$qui/elenco_richieste.tsv" | while IFS=$'\t' read -r f u; do scarica "$f" "$u"; sleep 3; done
