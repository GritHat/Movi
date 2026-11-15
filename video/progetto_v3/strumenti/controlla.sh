#!/bin/sh
# Controlli sul file reso: ffprobe, un'istantanea ogni N secondi (cartella nuova), conteggio del verde (Q11).
# Uso: sh strumenti/controlla.sh <video.mp4> <cartella_istantanee_nuova> [ogni_s=10]
set -eu
V=${1:?video}; O=${2:?cartella}; N=${3:-10}
[ -e "$O" ] && { echo "esiste già: $O"; exit 3; }
mkdir -p "$O"
ffprobe -v error -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate,nb_frames:format=duration,size -of default=nw=1 "$V" | tee "$O/ffprobe.txt"
timeout 300 ffmpeg -v error -i "$V" -vf "fps=1/$N" "$O/t_%03d.png"
# Q11: pixel con tinta 90–160° e saturazione > 0,3 (un fotogramma al secondo, ridotto a 480x270)
timeout 600 ffmpeg -v error -i "$V" -vf "fps=1,scale=480:270" -f rawvideo -pix_fmt rgb24 - | python3 -I -c '
import sys, colorsys
W, H = 480, 270; n = W * H * 3; f = 0; peggiore = 0
while True:
    b = sys.stdin.buffer.read(n)
    if len(b) < n: break
    v = 0
    for i in range(0, n, 3):
        h, s, l = colorsys.rgb_to_hls(b[i] / 255, b[i + 1] / 255, b[i + 2] / 255)
        if 90 <= h * 360 <= 160 and s > 0.3 and 0.1 < l < 0.95: v += 1
    peggiore = max(peggiore, v); f += 1
print(f"Q11 verde: {f} fotogrammi, massimo {peggiore} pixel verdi in un fotogramma (480x270)")' | tee -a "$O/ffprobe.txt"
