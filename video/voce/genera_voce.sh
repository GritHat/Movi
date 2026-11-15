#!/usr/bin/env bash
# Rigenera TUTTA la voce di MoVi da testo e cifre.json, in locale, senza rete e senza cancellare file.
# Uso: video/voce/genera_voce.sh <en|it> [velocita] [etichetta]
#   en: bm_george, en-gb, velocità predefinita 1.0     it: im_nicola, it, velocità predefinita 1.0
# Ingressi: video/voce/testi/voce_<l>_v3.modello.txt (un paragrafo per scena, {{CHIAVE}} per le frasi con cifre)
#           video/progetto/cifre.json (unica fonte delle cifre; 'pronuncia' per le grafie date a Kokoro)
# Uscite (in video/voce/uscite/<etichetta>/, cartella nuova; se esiste, se ne crea una con l'ora):
#   voce_<l>_detto.txt (testo esatto = sottotitoli), voce_<l>_kokoro.txt, voce_<l>.wav, voce_<l>.wav.tempi.json
#   (grafia vera, campo «scena»), voce_<l>_scenaN.wav, misure.txt
set -euo pipefail
export LC_ALL=C
L="${1:?lingua en|it}"; VEL="${2:-1.0}"; ET="${3:-${L}_v${VEL}}"
QUI="$(cd "$(dirname "$0")" && pwd)"
R="$(cd "$QUI/../.." && pwd)"
V="$R/.sciame/20261114-1301-percezione-challenge/f17-video/00-strumenti/voce"
CIFRE="$R/video/progetto/cifre.json"
case "$L" in
  en) VOCE=bm_george; LING=en-gb; PF=0.35; PP=0.8 ;;
  # im_nicola lascia circa 0,3-0,45 s di coda non rifilata per frase (misurato con silencedetect, v4): pause date più corte
  it) VOCE=im_nicola; LING=it; PF=0.05; PP=0.45 ;;
  *) echo "lingua: en o it" >&2; exit 2 ;;
esac
PIANO="12,27,16,21,22,20,30,11,13"   # durate del PIANO_VIDEO.md §2
OUT="$QUI/uscite/$ET"
[ -e "$OUT" ] && OUT="$OUT.$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"
PY="$V/venv-kokoro/bin/python"
"$PY" -I "$QUI/script/voce_util.py" compila "$L" "$QUI/testi/voce_${L}_v3.modello.txt" "$CIFRE" \
  "$OUT/voce_${L}_detto.txt" "$OUT/voce_${L}_kokoro.txt" | tee "$OUT/misure.txt"
cp -n "$CIFRE" "$OUT/cifre_usate.json"
timeout 600 "$PY" "$V/script/kokoro_tts.py" --testo "$OUT/voce_${L}_kokoro.txt" --voce "$VOCE" --lingua "$LING" \
  --velocita "$VEL" --pausa-frase "$PF" --pausa-paragrafo "$PP" --uscita "$OUT/voce_${L}_grezza.wav" | tee -a "$OUT/misure.txt"
# tempi con la grafia vera (MoVi, SDMs) e la scena di ogni frase
"$PY" -I "$QUI/script/voce_util.py" tempi "$OUT/voce_${L}_grezza.wav.tempi.json" "$OUT/voce_${L}_detto.txt" "$OUT/voce_${L}.wav.tempi.json"
cp -n "$OUT/voce_${L}_grezza.wav" "$OUT/voce_${L}.wav"
N=$(wc -w < "$OUT/voce_${L}_detto.txt")
bash "$V/script/misura.sh" "$OUT/voce_${L}.wav" "$N" | tee -a "$OUT/misure.txt"
# picchi, tagli e silenzi: campioni saturi già in misura.sh; qui silenzi > 1,0 s (anomali: la pausa più lunga voluta è 0,8 s)
ffmpeg -hide_banner -nostats -i "$OUT/voce_${L}.wav" -af silencedetect=noise=-45dB:d=1.0 -f null - 2>&1 \
  | grep -E "silence_(start|end)" | sed 's/^/silenzio>1s: /' | tee -a "$OUT/misure.txt" || echo "silenzi > 1,0 s: nessuno" | tee -a "$OUT/misure.txt"
"$PY" -I "$QUI/script/voce_util.py" scene "$OUT/voce_${L}.wav" "$OUT/voce_${L}.wav.tempi.json" "$OUT" "voce_${L}" "$PIANO" \
  | tee -a "$OUT/misure.txt"
echo "uscita: $OUT"
