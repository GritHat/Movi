#!/bin/sh
# MoVi video FINALE = v3d (copia di genera_versione_italiana_v3c.sh, che resta): correzioni QA_V3C D1, D2, D4 e REVISIONE_V3C C1, C3-C6;
# se VOCE_ESISTENTE=<cartella con voce_it.wav e voce_it.wav.tempi.json> riusa quella voce (stesso testo voce_it_v3c.txt) invece di rigenerarla.
# Derivato da: MoVi video v3c (copia di genera_versione_italiana_v3.sh, che resta), versione italiana: F7 col radar accecato e la correzione c1; voce im_nicola (Kokoro, velocita' 1,0, mai accelerata), rimontaggio delle scene
# sui tempi della voce italiana, sottotitoli italiani impressi (e .srt), mix a -14 LUFS, codifica finale.
# Le scritte a schermo dei pannelli restano in inglese (le cifre sono le stesse, da cifre_v3d.json).
# Non cancella e non sovrascrive niente: si ferma se un'uscita esiste.
# Uso: sh genera_versione_italiana_final.sh [draft|standard|high|delivery] [etichetta]
#   draft (predefinito) -> rendering/MoVi_pitch_IT_v3d_<etichetta>.mp4 ; delivery -> consegna/MoVi_pitch_IT_final.mp4
set -eu
Q=${1:-draft}; ET=${2:-draft}
V=$(cd "$(dirname "$0")/.." && pwd); R=$(dirname "$V")
S="$R/.sciame/20261114-1301-percezione-challenge/f17-video/00-strumenti/voce"
P="$V/progetto_v3"
VO="${VOCE_ESISTENTE:-$V/voce/uscite/it_v3d_$ET}"
TJ="tempi/scene_v3d_it_$ET.js"
IMM="$V/rendering/MoVi_pitch_IT_v3d_${ET}_immagine.mp4"
if [ "$Q" = delivery ]; then OUT="$V/consegna/MoVi_pitch_IT_final.mp4"; else OUT="$V/rendering/MoVi_pitch_IT_v3d_$ET.mp4"; fi
W="$V/rendering/audio_MoVi_pitch_IT_v3d_$ET"
[ -n "${VOCE_ESISTENTE:-}" ] || { [ -e "$VO" ] && { echo "esiste gia': $VO"; exit 3; }; }
for f in "$P/$TJ" "$IMM" "$OUT" "$W"; do [ -e "$f" ] && { echo "esiste gia': $f (usa un'altra etichetta)"; exit 3; }; done
# 1. voce italiana (pausa fra frasi 0,05 s: im_nicola lascia ~0,3-0,45 s di coda; fra paragrafi 0,7 s, > 0,6 s per le scene)
if [ -z "${VOCE_ESISTENTE:-}" ]; then mkdir -p "$VO"
timeout 900 "$S/venv-kokoro/bin/python" -I "$S/script/kokoro_tts.py" --testo "$V/voce/testi/voce_it_v3c.txt" \
  --voce im_nicola --lingua it --velocita 1.0 --pausa-frase 0.05 --pausa-paragrafo 0.7 --uscita "$VO/voce_it.wav" | tee "$VO/genera.log"; fi
cd "$P"
# 2. scene e sottotitoli italiani sui tempi della voce; si ferma (codice 4) se il totale supera 176,0 s
python3 -I strumenti/costruisci_v3d.py "$VO/voce_it.wav" "$TJ" --max 176.0
# 3. index.html (la versione precedente va in versioni/) e immagine
python3 -I strumenti/monta_v3d.py "$TJ" it
timeout 900 sh strumenti/rendi_finale.sh "$Q" "$IMM"
# 4. silenzio di musica all'urto di F7 (stessa regola dell'inglese), mix e codifica finale
SIL=$(python3 -I -c "import json;t=json.load(open('${TJ%.js}.json'));s=[x for x in t['scene'] if x['id']=='s8'][0];fr=json.load(open(t['voce']+'.tempi.json'));p=[x for x in fr if x['inizio']>=s['voce_wav_da']-1e-6];print(round(s['inizio']+s['voce_da']+p[1]['inizio']-p[0]['inizio']+0.4,3))")
CRF=18; [ "$Q" = draft ] && CRF=23
timeout 1500 python3 -I strumenti/audio_finale.py "$IMM" "$OUT" "$W" "${TJ%.js}.json" "$VO/voce_it.wav" --silenzi "$SIL" --crf "$CRF"
cp -n "${TJ%.js}.srt" "${OUT%.mp4}_impressi.srt"   # come nella v3c: 20 code sovrapposte di ~0,2 s; il .srt da consegnare e' MoVi_pitch_IT_final.srt
# 5. torna all'inglese: index.html della versione inglese (la versione italiana resta in versioni/)
python3 -I strumenti/monta_v3d.py tempi/scene_v3d_en.js en
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,sample_rate -of default=nw=1 "$OUT"
echo "uscita: $OUT"
