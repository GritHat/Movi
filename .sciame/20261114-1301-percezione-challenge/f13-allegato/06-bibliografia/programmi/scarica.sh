#!/usr/bin/env bash
# Riapre in rete i registri bibliografici delle voci da alzare e delle voci nuove.
# Solo identificativi pubblici nelle richieste; il materiale va in scaricati/ (dato non fidato, mai eseguito).
set -u
qui="$(cd "$(dirname "$0")/.." && pwd)"
ua="curatore-bibliografia/1.0"
esito="$qui/scaricati/esito_richieste.tsv"
: > "$esito"
prendi() { # nome url cartella
  local f="$qui/scaricati/$3/$1"
  local c
  c=$(curl -sS -L --max-time 25 --max-filesize 3000000 -A "$ua" -o "$f" -w '%{http_code}' "$2" 2>/dev/null) || c="errore:$c"
  printf '%s\t%s\t%s\t%s\n' "$(date -Is)" "$1" "$c" "$2" >> "$esito"
}
while IFS=$'\t' read -r nome doi; do
  [ -z "$nome" ] && continue
  prendi "$nome.json" "https://api.crossref.org/works/$doi" crossref
  sleep 0.4
done <<'DOI'
kalman1960	10.1115/1.3662552
kuhn1955	10.1002/nav.3800020109
clopper1934	10.1093/biomet/26.4.404
hornung2013	10.1007/s10514-012-9321-0
luiten2021	10.1007/s11263-020-01375-2
zhang2022	10.1007/978-3-031-20047-2_1
thor	10.1109/LRA.2020.2965416
tum-rgbd	10.1109/IROS.2012.6385773
koch2007	10.1016/j.inffus.2005.09.002
wyffels2015	10.1109/TRO.2015.2409413
nguyen2012	10.1109/3DIMPVT.2012.84
moras2011	10.1109/ICRA.2011.5980298
guibas1999	10.1142/S0218195999000273
krejci2026	10.1109/TAES.2026.3676431
hetzel2024	10.1007/978-3-031-91585-7_9
barber2021	10.1093/imaiai/iaaa017
ahn2019	10.1109/URAI.2019.8768489
nuova-wilson1927	10.1080/01621459.1927.10502953
nuova-brown2001	10.1214/ss/1009213286
nuova-barshalom2001	10.1002/0471221279
nuova-elfes1989	10.1109/2.30720
nuova-vovk2005	10.1007/b106715
nuova-bernardin2008	10.1155/2008/246309
DOI
prendi "arxiv_gruppo.xml" "https://export.arxiv.org/api/query?id_list=2106.00170,1903.04684,2110.06864,2009.07736,2511.20239,2410.06905,2001.04134,2201.11924&max_results=10" arxiv
prendi "zenodo_thor.json" "https://zenodo.org/api/records/3382145" pagine
prendi "librealsense_sample-data.md" "https://raw.githubusercontent.com/IntelRealSense/librealsense/master/doc/sample-data.md" pagine
prendi "tum_rgbd_pagina.html" "https://cvg.cit.tum.de/data/datasets/rgbd-dataset" pagine
prendi "tum_rgbd_download.html" "https://cvg.cit.tum.de/data/datasets/rgbd-dataset/download" pagine
prendi "neurips_gibbs.html" "https://proceedings.neurips.cc/paper/2021/hash/0d441de75945e5acbc865406fc9a2559-Abstract.html" pagine
cat "$esito"
