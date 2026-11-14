#!/bin/sh
# Controlli testuali sulla versione 3 finale (previsioni F1-F6 di PREVISIONI.md). Uso: sh controlla_finale.sh
cd "$(dirname "$0")" || exit 1
D=SOLUZIONE_V3.md; T=TABELLA_CORREZIONI.md
echo "== F1: sigle delle critiche nella tabella (0 = manca)"
m=0; for s in AT-1 AT-2 AT-3 AT-4 AT-5 AT-6 AT-7 AT-8 AT-9 AT-10 AT-11 AT-12 CO-1 CO-2 CO-3 CO-4 CO-5 CO-6 CO-7 CO-8 CO-9 CO-10 CO-11 PR-1 PR-2 PR-3 PR-4 PR-5 PR-6 PR-7 PR-8 ST-1 ST-2 ST-3 ST-4 ST-5 ST-6 ST-7 CI-1 CI-2 CI-3 CI-4 CI-5 CI-6 CI-7; do
  n=$(grep -c "^| $s |" $T); [ "$n" -eq 1 ] || { echo "  $s: $n righe"; m=$((m+1)); }
  grep "^| $s |" $T | grep -q "applicat" || { echo "  $s: senza esito"; m=$((m+1)); }
done; echo "  difetti: $m"
echo "== F2: sigle nel documento (0 = manca)"
m=0; for s in F-401 F-402 F-403 F-404 F-405 F-406 F-407 F-408 F-409 F-410 F-411 F-412 F-413 K-003 K-216 K-305 K-404 K-406 K-016 K-214 K-108 K-219 K-014 K-107 K-215 K-407 logico-K1 sd-K7 sd-K8 CI-1 CI-4 CI-5 CI-6; do
  n=$(grep -c -- "$s" $D); [ "$n" -ge 1 ] || { echo "  $s: 0"; m=$((m+1)); }
done; echo "  mancanti: $m"
echo "== F3: frasi da non dire, righe in cui compaiono"
for f in "essun ostacolo" "100 % degli istanti" "olo guardando" "ia libera" "alidato"; do echo "  [$f]"; grep -n -- "$f" $D | cut -c1-150 | sed 's/^/    /'; done
echo "== F4: rimandi alla prima stesura"
grep -n "01-soluzione" $D | cut -c1-120
echo "== F5: lunghezza"
wc -w -c $D $T
echo "== F6: controprova"
ls ../07-controprova-identita/ | tr '\n' ' '; echo; ls ../07-controprova-identita/CONTROPROVA_IDENTITA.md 2>&1 | tail -1
date -Is
