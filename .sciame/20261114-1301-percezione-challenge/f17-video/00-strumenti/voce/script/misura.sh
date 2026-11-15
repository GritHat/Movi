#!/usr/bin/env bash
# Misure oggettive di un WAV: durata, parole/min, picco, RMS, LUFS, campioni saturi, silenzi > 0,6 s, silenzio in testa e in coda.
export LC_ALL=C
# Uso: script/misura.sh <file.wav> <numero_parole>
f="$1"; n="$2"
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
fmt=$(ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate,channels,codec_name -of csv=p=0 "$f")
st=$(ffmpeg -hide_banner -nostats -i "$f" -af astats=measure_perchannel=none -f null - 2>&1)
pk=$(echo "$st" | awk '/Peak level dB/{print $NF}'); rms=$(echo "$st" | awk '/RMS level dB/{print $NF}')
dc=$(echo "$st" | awk '/DC offset/{print $NF}')
clip=$(ffmpeg -v error -i "$f" -f s16le - | python3 -I -c "
import sys,array;a=array.array('h');a.frombytes(sys.stdin.buffer.read());print(sum(1 for x in a if abs(x)>=32767))")
lufs=$(ffmpeg -hide_banner -nostats -i "$f" -af ebur128=peak=true -f null - 2>&1 | awk '/Integrated loudness/{f=1} f&&/I:/{print $2; exit}')
sil=$(ffmpeg -hide_banner -nostats -i "$f" -af silencedetect=noise=-45dB:d=0.05 -f null - 2>&1 | grep -E "silence_(start|end)")
testa=$(echo "$sil" | awk '/silence_start: 0($|[^.0-9])|silence_start: 0\.0*$/{g=1} g&&/silence_end/{print $5; exit}')
coda=$(echo "$sil" | awk -v d="$d" '/silence_start/{s=$5} END{print d-s}')
lunghi=$(echo "$sil" | awk '/silence_duration/{if($8>0.6)c++} END{print c+0}')
maxint=$(echo "$sil" | awk -v t="${testa:-0}" '/silence_end/{if($5!=t && $8>m)m=$8} END{print m+0}')
wpm=$(awk -v n="$n" -v d="$d" 'BEGIN{printf "%.0f", n/d*60}')
printf "%s | %s | %.2f s | %s p/min | picco %s dBFS | RMS %s dB | %s LUFS | saturi %s | DC %s | testa %s s | coda %.2f s | pausa interna max %.2f s | silenzi>0,6 s: %s\n" "$(basename "$f")" "$fmt" "$d" "$wpm" "$pk" "$rms" "$lufs" "$clip" "$dc" "${testa:-0}" "$coda" "$maxint" "$lunghi"
