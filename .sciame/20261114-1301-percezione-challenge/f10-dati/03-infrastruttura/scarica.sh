#!/usr/bin/env bash
# Scarica UN file pubblico in f10-dati/scaricati/<nome>/ e ne annota la provenienza.
#
# Uso:  bash scarica.sh <nome> <indirizzo> <tetto> [--file NOME] [--licenza TESTO] [--tempo SECONDI] [--riprendi]
#
#   <nome>       sottocartella di f10-dati/scaricati (minuscole, cifre, punto, trattino, trattino basso)
#   <indirizzo>  solo https://, senza credenziali dentro
#   <tetto>      dimensione massima ammessa: byte, oppure con suffisso K, M o G (potenze di 1024)
#   --file       nome del file salvato (se manca: l'ultimo tratto dell'indirizzo)
#   --licenza    licenza della fonte, da annotare (se manca: «DA COMPILARE», e va compilata a mano)
#   --tempo      tempo massimo in secondi (se manca: 600; massimo 600, come da contratto)
#   --riprendi   continua uno scaricamento interrotto dal tempo massimo (file .parziale rimasto)
#
# Garanzie:
#   - tempo massimo imposto due volte (curl --max-time e il comando timeout);
#   - tetto imposto tre volte: curl --max-filesize, il limite del sistema «ulimit -f» (vale anche se il
#     server non dichiara la dimensione) e un controllo finale sulla dimensione;
#   - tetto complessivo di scaricati/: 6 GB (contratto f10); spazio libero controllato prima;
#   - il contenuto non viene mai eseguito, importato né interpretato: il file è salvato senza permesso
#     d'esecuzione (0644) e se ne leggono solo dimensione, impronta e tipo (comando «file»);
#   - sha256, indirizzo, ora e dimensione finiscono in scaricati/<nome>/PROVENIENZA.md;
#   - si può rilanciare: se il file c'è già e l'impronta coincide con quella annotata, non riscarica.
#
# Codici d'uscita: 0 fatto (o già presente e integro); 2 uso sbagliato; 3 file presente ma impronta diversa
# o non annotata; 4 tetto superato; 5 errore di rete o del server; 6 tempo scaduto (resta il .parziale).
set -euo pipefail

QUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RADICE="$(cd "$QUI/.." && pwd)"
SCARICATI="$RADICE/scaricati"
TETTO_TOTALE=6000000000

errore() { echo "ERRORE: $*" >&2; }
uso() { sed -n '2,13p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//' >&2; exit 2; }

[ "$(basename "$RADICE")" = "f10-dati" ] || { errore "lo script deve stare in f10-dati/03-infrastruttura"; exit 2; }
[ $# -ge 3 ] || uso
NOME="$1"; INDIRIZZO="$2"; TETTO_TXT="$3"; shift 3
FILE=""; LICENZA="DA COMPILARE"; TEMPO=600; RIPRENDI=0
while [ $# -gt 0 ]; do
  case "$1" in
    --file) FILE="${2:-}"; shift 2 ;;
    --licenza) LICENZA="${2:-}"; shift 2 ;;
    --tempo) TEMPO="${2:-}"; shift 2 ;;
    --riprendi) RIPRENDI=1; shift ;;
    *) errore "opzione sconosciuta: $1"; uso ;;
  esac
done

# --- controlli sugli argomenti ---------------------------------------------------------------
[[ "$NOME" =~ ^[a-z0-9][a-z0-9._-]{0,63}$ ]] || { errore "nome non valido: «$NOME»"; exit 2; }
[[ "$INDIRIZZO" =~ ^https://[A-Za-z0-9.-]+(:[0-9]+)?(/[^[:space:]\`\"\'\\]*)?$ ]] \
  || { errore "indirizzo non valido (serve https://, senza spazi né credenziali): «$INDIRIZZO»"; exit 2; }
[[ "$TETTO_TXT" =~ ^([0-9]+)([KMG]?)$ ]] || { errore "tetto non valido: «$TETTO_TXT» (esempi: 5000000, 5M, 2G)"; exit 2; }
TETTO="${BASH_REMATCH[1]}"
case "${BASH_REMATCH[2]}" in K) TETTO=$((TETTO * 1024)) ;; M) TETTO=$((TETTO * 1024 * 1024)) ;; G) TETTO=$((TETTO * 1024 * 1024 * 1024)) ;; esac
[ "$TETTO" -gt 0 ] || { errore "il tetto deve essere maggiore di zero"; exit 2; }
[[ "$TEMPO" =~ ^[0-9]+$ ]] && [ "$TEMPO" -ge 1 ] && [ "$TEMPO" -le 600 ] || { errore "tempo non valido: «$TEMPO» (da 1 a 600 secondi)"; exit 2; }
if [ -z "$FILE" ]; then
  FILE="${INDIRIZZO%%\?*}"; FILE="${FILE%%#*}"; FILE="${FILE##*/}"
fi
[[ "$FILE" =~ ^[A-Za-z0-9][A-Za-z0-9._+-]{0,127}$ ]] && [ "$FILE" != "PROVENIENZA.md" ] \
  || { errore "nome del file non valido o non ricavabile dall'indirizzo: «$FILE» (usa --file)"; exit 2; }
LICENZA="$(printf '%s' "$LICENZA" | tr -d '\n\r`|' | cut -c1-300)"

DEST="$SCARICATI/$NOME"
FINALE="$DEST/$FILE"
PARZIALE="$DEST/$FILE.parziale"
PROV="$DEST/PROVENIENZA.md"
mkdir -p "$DEST"

# Un solo scaricamento alla volta per cartella.
exec 9>"$DEST/.blocco"
flock -n 9 || { errore "un altro scaricamento è in corso in $DEST"; exit 5; }

# --- già presente? ---------------------------------------------------------------------------
if [ -e "$FINALE" ]; then
  IMPRONTA="$(sha256sum -- "$FINALE" | cut -d' ' -f1)"
  if [ -f "$PROV" ] && grep -qF -- "- sha256: \`$IMPRONTA\`" "$PROV" && grep -qF -- "## \`$FILE\`" "$PROV"; then
    echo "GIÀ PRESENTE: $FINALE ($(stat -c %s -- "$FINALE") byte), impronta uguale a quella annotata: non riscarico."
    exit 0
  fi
  errore "$FINALE esiste ma la sua impronta ($IMPRONTA) non è annotata in PROVENIENZA.md: non lo tocco."
  exit 3
fi

# --- tetto complessivo e spazio libero ---------------------------------------------------------
USATO="$(du -sb --apparent-size -- "$SCARICATI" | cut -f1)"
if [ $((USATO + TETTO)) -gt "$TETTO_TOTALE" ]; then
  errore "scaricati/ occupa già $USATO byte: con un tetto di $TETTO byte si supererebbero i 6 GB del contratto."
  exit 4
fi
LIBERO="$(df --output=avail -B1 -- "$DEST" | tail -1 | tr -d ' ')"
if [ "$LIBERO" -lt $((TETTO + 1073741824)) ]; then
  errore "spazio libero insufficiente: $LIBERO byte (servono il tetto più 1 GiB di margine)."
  exit 4
fi

# --- scaricamento -------------------------------------------------------------------------------
RIPRESA=()
if [ -e "$PARZIALE" ]; then
  if [ "$RIPRENDI" -eq 1 ]; then RIPRESA=(--continue-at -); else rm -f -- "$PARZIALE"; fi
fi
LIMITE_CURL=(--max-filesize "$TETTO")
# Solo per la prova del limite di sistema: toglie il controllo di curl e lascia «ulimit -f».
[ "${SCARICA_PROVA_SOLO_ULIMIT:-0}" = "1" ] && LIMITE_CURL=()

INIZIO="$(date -Is)"
ESITO_CURL=0
RISPOSTA="$(
  # Oltre il limite il sistema manda SIGXFSZ: lo si ignora, così curl riceve un errore di scrittura
  # (uscita 23) invece di morire lasciando un'immagine della memoria (core).
  trap '' XFSZ
  ulimit -c 0
  ulimit -f $(((TETTO + 1023) / 1024))
  timeout --kill-after=10 "$((TEMPO + 5))" \
    curl --fail --location --max-redirs 5 --proto '=https' --proto-redir '=https' \
      --connect-timeout 20 --max-time "$TEMPO" "${LIMITE_CURL[@]}" "${RIPRESA[@]}" \
      --silent --show-error --no-netrc --output "$PARZIALE" \
      --write-out '%{http_code}\t%{url_effective}\t%{content_type}\t%{time_total}' \
      -- "$INDIRIZZO"
)" || ESITO_CURL=$?

DIM=0; [ -e "$PARZIALE" ] && DIM="$(stat -c %s -- "$PARZIALE")"
if [ "$ESITO_CURL" -eq 28 ] || [ "$ESITO_CURL" -eq 124 ] || [ "$ESITO_CURL" -eq 137 ]; then
  errore "tempo scaduto dopo $TEMPO s ($DIM byte scaricati). Resta $PARZIALE: rilancia con --riprendi."
  exit 6
fi
if [ "$ESITO_CURL" -eq 63 ] || [ "$ESITO_CURL" -eq 153 ] || [ "$DIM" -gt "$TETTO" ] \
   || { [ "$ESITO_CURL" -ne 0 ] && [ "$DIM" -ge $((((TETTO + 1023) / 1024) * 1024)) ]; }; then
  rm -f -- "$PARZIALE"
  errore "tetto superato: il file è più grande di $TETTO byte (curl: $ESITO_CURL). Niente è stato tenuto."
  exit 4
fi
if [ "$ESITO_CURL" -ne 0 ]; then
  rm -f -- "$PARZIALE"
  errore "scaricamento fallito (curl: $ESITO_CURL; risposta: $(printf '%s' "$RISPOSTA" | cut -f1)). Niente è stato tenuto."
  exit 5
fi
[ "$DIM" -gt 0 ] || { rm -f -- "$PARZIALE"; errore "il file scaricato è vuoto. Niente è stato tenuto."; exit 5; }

# --- impronta, tipo, provenienza ----------------------------------------------------------------
chmod 0644 -- "$PARZIALE"
IMPRONTA="$(sha256sum -- "$PARZIALE" | cut -d' ' -f1)"
TIPO="$(file --brief --mime-type -- "$PARZIALE" 2>/dev/null || echo sconosciuto)"
pulisci() { printf '%s' "$1" | tr -cd 'A-Za-z0-9 .,:;/_=+%?&@()~-' | cut -c1-500; }
CODICE="$(pulisci "$(printf '%s' "$RISPOSTA" | cut -f1)")"
FINALE_URL="$(pulisci "$(printf '%s' "$RISPOSTA" | cut -f2)")"
TIPO_SERVER="$(pulisci "$(printf '%s' "$RISPOSTA" | cut -f3)")"
DURATA="$(pulisci "$(printf '%s' "$RISPOSTA" | cut -f4)")"
mv -n -- "$PARZIALE" "$FINALE"
[ ! -e "$PARZIALE" ] || { errore "$FINALE è comparso nel frattempo: non lo sovrascrivo."; rm -f -- "$PARZIALE"; exit 3; }

if [ ! -f "$PROV" ]; then
  {
    echo "# Provenienza dei file in \`scaricati/$NOME/\`"
    echo
    echo "Dati NON fidati: non si esegue niente dal loro interno. Gli archivi si aprono con"
    echo "\`03-infrastruttura/apri_archivio.py\` in una cartella nuova; i formati si leggono con librerie o con"
    echo "codice proprio. Una voce per file, aggiunta da \`03-infrastruttura/scarica.sh\`."
  } > "$PROV"
fi
{
  echo
  echo "## \`$FILE\`"
  echo
  echo "- indirizzo richiesto: <$(pulisci "$INDIRIZZO")>"
  echo "- indirizzo finale (dopo i rinvii): <$FINALE_URL>"
  echo "- ora dello scaricamento: $INIZIO (durata $DURATA s, risposta HTTP $CODICE)"
  echo "- dimensione: $DIM byte (tetto dichiarato: $TETTO byte)"
  echo "- sha256: \`$IMPRONTA\`"
  echo "- tipo rilevato dal contenuto: $TIPO (tipo dichiarato dal server: ${TIPO_SERVER:-nessuno})"
  echo "- licenza: $LICENZA"
} >> "$PROV"

echo "FATTO: $FINALE"
echo "  dimensione: $DIM byte   sha256: $IMPRONTA"
echo "  tipo rilevato: $TIPO   annotato in: $PROV"
case "$TIPO" in text/html*) echo "  AVVISO: il contenuto è una pagina HTML: forse il sito ha risposto con una pagina d'errore o d'accesso." >&2 ;; esac
[ "$LICENZA" != "DA COMPILARE" ] || echo "  AVVISO: licenza non indicata: compilala a mano in PROVENIENZA.md (il contratto la richiede)." >&2
exit 0
