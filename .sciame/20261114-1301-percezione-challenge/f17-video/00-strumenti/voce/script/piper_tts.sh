#!/usr/bin/env bash
# Testo -> WAV 48 kHz mono 16 bit con Piper.
# Uso: script/piper_tts.sh <voce> <testo.txt> <uscita.wav> [length_scale=1.0] [pausa_frase_s=0.35]
# length_scale > 1 rallenta (1.1 = circa il 10 % più lento). Ogni riga del file è un enunciato.
set -euo pipefail
QUI="$(cd "$(dirname "$0")/.." && pwd)"
VOCE="$1"; TESTO="$2"; USCITA="$3"; LS="${4:-1.0}"; PAUSA="${5:-0.35}"
TMP="$(mktemp --suffix=.wav)"
"$QUI/venv-piper/bin/piper" -m "$QUI/modelli/piper/$VOCE.onnx" -i "$TESTO" -f "$TMP" \
  --length-scale "$LS" --sentence-silence "$PAUSA"
ffmpeg -v error -y -i "$TMP" -af "volume=-3dB,adelay=150:all=1,apad=pad_dur=0.15,aresample=48000:resampler=soxr:precision=28" \
  -ar 48000 -ac 1 -c:a pcm_s16le "$USCITA"
rm -f "$TMP"
