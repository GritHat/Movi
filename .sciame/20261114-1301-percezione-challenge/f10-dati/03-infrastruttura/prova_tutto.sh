#!/usr/bin/env bash
# Rilancia tutte le prove dell'infrastruttura f10. Si può rilanciare quante volte si vuole.
#   bash prova_tutto.sh          # senza rete: ambiente, archivi, formato della sequenza
#   bash prova_tutto.sh --rete   # in più: scaricamento vero (scheda VL53L7CX, 2,7 MB) e prove del tetto
# Esce con 0 solo se tutte le prove passano. Scrive solo in 03-infrastruttura/ e in scaricati/prova-*.
set -uo pipefail
QUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RADICE="$(cd "$QUI/.." && pwd)"
PY="$RADICE/ambiente/venv/bin/python"
INDIRIZZO="https://www.pololu.com/file/0J1992/vl53l7cx.pdf"
falliti=0
passo() {  # passo <descrizione> <uscita attesa> <comando...>
  local nome="$1" atteso="$2"; shift 2
  "$@"; local esito=$?
  if [ "$esito" -eq "$atteso" ]; then echo "== [OK] $nome (uscita $esito)"; else echo "== [FALLITA] $nome (uscita $esito, attesa $atteso)"; falliti=$((falliti + 1)); fi
}
echo "ora: $(date -Is)"
[ -x "$PY" ] || { echo "manca l'ambiente: lancia prima crea_ambiente.sh" >&2; exit 2; }
passo "ambiente (numpy, scipy, opencv, pillow, rosbags)" 0 timeout 120 "$PY" -I "$QUI/prova_ambiente.py"
passo "apritore di archivi (ostili e buoni)" 0 timeout 280 python3 -I "$QUI/prova_archivi.py"
passo "programma di controllo (valide, difettose, sospette)" 0 timeout 280 "$PY" -I "$QUI/prova_controllo.py"
passo "la sequenza d'esempio rispetta il formato, in modo rigoroso" 0 timeout 60 "$PY" -I "$QUI/controlla_sequenza.py" "$QUI/esempio_sequenza" --rigoroso --tutti --silenzioso
if [ "${1:-}" = "--rete" ]; then
  passo "scarica.sh: scheda pubblica entro il tetto (o già presente e integra)" 0 timeout 90 bash "$QUI/scarica.sh" prova-infrastruttura "$INDIRIZZO" 5M --tempo 60 --licenza "scheda tecnica pubblica del produttore; licenza non verificata"
  passo "scarica.sh: rilancio senza riscaricare" 0 timeout 90 bash "$QUI/scarica.sh" prova-infrastruttura "$INDIRIZZO" 5M --tempo 60
  passo "scarica.sh: tetto di 1M superato (dimensione dichiarata)" 4 timeout 90 bash "$QUI/scarica.sh" prova-tetto "$INDIRIZZO" 1M --tempo 60
  passo "scarica.sh: tetto di 1M superato (solo ulimit)" 4 timeout 90 env SCARICA_PROVA_SOLO_ULIMIT=1 bash "$QUI/scarica.sh" prova-tetto "$INDIRIZZO" 1M --tempo 60
  resti="$(find "$RADICE/scaricati/prova-tetto" -type f ! -name .blocco 2>/dev/null | wc -l)"
  passo "scarica.sh: nessun file rimasto dopo il rifiuto ($resti)" 0 test "$resti" -eq 0
  rm -rf -- "$RADICE/scaricati/prova-tetto"
  passo "scarica.sh: indirizzo non https rifiutato" 2 timeout 20 bash "$QUI/scarica.sh" prova-tetto "http://example.com/a.pdf" 1M
  passo "scarica.sh: nome con «..» rifiutato" 2 timeout 20 bash "$QUI/scarica.sh" "../fuori" "$INDIRIZZO" 1M
fi
echo "ESITO COMPLESSIVO: $falliti prove fallite — $(date -Is)"
exit $((falliti > 0))
