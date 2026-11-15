#!/usr/bin/env bash
# Mix voce + musica + ambiente con ducking, poi loudnorm a due passate (-14 LUFS, TP -1.5 dBTP).
# Uso: mix.sh VOCE.wav MUSICA AMBIENTE DURATA_S USCITA.wav [RITARDO_VOCE_MS=500]
set -euo pipefail
VOCE=$1; MUSICA=$2; AMB=$3; DUR=$4; OUT=$5; RIT=${6:-500}
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
FUORI=$(awk "BEGIN{print $DUR-3}")

# 1) premix: la voce comanda il compressore sulla musica (ducking), l'ambiente resta fisso
ffmpeg -hide_banner -loglevel error -y -i "$VOCE" -i "$MUSICA" -i "$AMB" -filter_complex "
[0:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=70,adelay=${RIT}:all=1,apad,atrim=0:${DUR},asplit=2[v][chiave];
[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:${DUR},volume=-14dB,afade=t=in:d=2,afade=t=out:st=${FUORI}:d=3[m];
[m][chiave]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=700:makeup=1[md];
[2:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:${DUR},volume=-26dB,afade=t=in:d=2,afade=t=out:st=${FUORI}:d=3[a];
[v][md][a]amix=inputs=3:normalize=0:duration=longest[mix]" -map "[mix]" -c:a pcm_s24le "$TMP/premix.wav"

# 2) prima passata: misura
ffmpeg -hide_banner -nostats -i "$TMP/premix.wav" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>"$TMP/p1.txt"
J=$(sed -n '/^{/,/^}/p' "$TMP/p1.txt")
g() { printf '%s' "$J" | sed -n "s/.*\"$1\" *: *\"\([^\"]*\)\".*/\1/p"; }
echo "misurato: I=$(g input_i) TP=$(g input_tp) LRA=$(g input_lra) soglia=$(g input_thresh) scarto=$(g target_offset)"

# 3) seconda passata: correzione lineare con i valori misurati, ricampionamento a 48 kHz
ffmpeg -hide_banner -loglevel error -y -i "$TMP/premix.wav" -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" -c:a pcm_s24le "$OUT"

# 4) verifica
ffmpeg -hide_banner -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|LRA:|Peak:)"
