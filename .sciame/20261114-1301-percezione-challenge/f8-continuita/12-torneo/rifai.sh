#!/bin/sh
# Rifa tutte le prove del torneo f8 (sciame-avversario). Un lancio alla volta, ognuno con timeout 120. Semi fissati.
# Uso: sh rifai.sh [gruppo]   (gruppi: tar base est fuori sens tar2 inganno; senza argomento: tutti)
cd "$(dirname "$0")" || exit 1
G=${1:-tutti}
T="timeout 120 ./torneo"
TAB=tab_D.txt,tab_T.txt,tab_P.txt
run() { out=$1; shift; echo ">> $out: $*"; $T "$@" > "ris/$out" 2> "ris/$out.err" || echo "ESITO NON ZERO: $out"; [ -s "ris/$out.err" ] || rm -f "ris/$out.err"; }
mkdir -p ris
gcc -O2 -o torneo torneo.c -lm 2>/dev/null || exit 1
if [ "$G" = tutti ] || [ "$G" = tar ]; then   # taratura: semi 1000-1199, solo D e T
  $T -scene T -cal tab_T.txt -n 200 -seed 1000; $T -scene D -cal tab_D.txt -n 200 -seed 1000
  $T -scene T -cal tab_P.txt -n 400 -seed 1000 -beh 0 -vlo 1.15 -vhi 1.45
fi
if [ "$G" = tutti ] || [ "$G" = base ]; then  # avv-5, 15, 18, 19, 20 (e attacco 5 su «prosegue»)
  run base_T.txt -scene T -n 400 -seed 9000 -tab $TAB
  run base_D.txt -scene D -n 400 -seed 9000 -tab $TAB
  run base_L.txt -scene L -n 400 -seed 9000 -tab $TAB
  run base_T_liscia.txt -scene T -n 200 -seed 9000 -tab $TAB -smooth1
fi
if [ "$G" = tutti ] || [ "$G" = est ]; then   # avv-1 (attacco 1), avv-2
  run a1_T.txt -scene T -beh 13 -vlo 1.2 -vhi 1.2 -n 200 -seed 9000 -tab $TAB
  run a1_D.txt -scene D -beh 13 -vlo 1.2 -vhi 1.2 -n 200 -seed 9000 -tab $TAB
fi
if [ "$G" = tutti ] || [ "$G" = fuori ]; then # avv-6, 7, 8, 9, 16 e casi fuori dal modello
  run a6_sosta30_T.txt -scene T -beh 7 -cap 460 -n 100 -seed 9000 -tab $TAB
  run a6_sosta30_D.txt -scene D -beh 7 -cap 460 -n 100 -seed 9000 -tab $TAB
  run a7_corsa_L.txt -scene L -beh 0,2 -vlo 3.0 -vhi 3.0 -n 200 -seed 9000 -tab $TAB
  run a7_corsa_D.txt -scene D -beh 0,2 -vlo 3.0 -vhi 3.0 -n 200 -seed 9000 -tab $TAB
  run a8_estraneo_T.txt -scene T -beh 6 -stranger -n 400 -seed 9000 -tab $TAB
  run a9_altri_T.txt -scene T -beh 9,10,11,12 -n 200 -seed 9000 -tab $TAB
  run a16_segue_T.txt -scene T -beh 0 -follow -vlo 0.5 -vhi 1.0 -n 100 -seed 9000 -tab $TAB
  run a16_segue_congela_T.txt -scene T -beh 0 -follow -freeze -vlo 0.5 -vhi 1.0 -n 100 -seed 9000 -tab $TAB
  run a16_via_congela_T.txt -scene T -beh 6 -vp 0.4 -freeze -n 100 -seed 9000 -tab $TAB
  run a16_via_T.txt -scene T -beh 6 -vp 0.4 -n 100 -seed 9000 -tab $TAB
fi
if [ "$G" = tutti ] || [ "$G" = sens ]; then  # avv-10, 11, 12, 13
  run a10_dw-20_T.txt -scene T -beh 0,2,8 -dw -0.2 -n 200 -seed 9000 -tab $TAB
  run a10_dw-30_T.txt -scene T -beh 0,2,8 -dw -0.3 -n 200 -seed 9000 -tab $TAB
  run a10_dw+20_T.txt -scene T -beh 0,2,8 -dw 0.2 -n 200 -seed 9000 -tab $TAB
  run a10_dw-20_D.txt -scene D -beh 0,2,8 -dw -0.2 -n 200 -seed 9000 -tab $TAB
  run a10_dw-30_D.txt -scene D -beh 0,2,8 -dw -0.3 -n 200 -seed 9000 -tab $TAB
  run a10_dw-20_fix_T.txt -scene T -beh 0,2,8 -dw -0.2 -fixentry -n 200 -seed 9000 -tab $TAB
  run a7_corsa_fix_L.txt -scene L -beh 0,2 -vlo 3.0 -vhi 3.0 -fixentry -n 200 -seed 9000 -tab $TAB
  run a21_base_fix2_T.txt -scene T -n 400 -seed 9000 -fixentry2 -tab $TAB
  run a21_dw-20_fix2_T.txt -scene T -beh 0,2,8 -dw -0.2 -fixentry2 -n 200 -seed 9000 -tab $TAB
  run a21_corsa_fix2_L.txt -scene L -beh 0,2 -vlo 3.0 -vhi 3.0 -fixentry2 -n 200 -seed 9000 -tab $TAB
  run a21_pd07_fix2_T.txt -scene T -beh 0,2,3 -pd 0.7 -fixentry2 -n 200 -seed 9000 -tab $TAB
  run a21_vuoto0.7_fix2_D.txt -scene D -beh 0 -vlo 1.2 -vhi 1.2 -drop 0.7 -fixentry2 -n 200 -seed 9000 -tab $TAB
  run a11_pd07_T.txt -scene T -beh 0,2,3 -pd 0.7 -n 200 -seed 9000 -tab $TAB
  run a11_pd07_fix_T.txt -scene T -beh 0,2,3 -pd 0.7 -fixentry -n 200 -seed 9000 -tab $TAB
  run a11_miss8_T.txt -scene T -beh 0,2,3 -miss 8 -n 200 -seed 9000 -tab $TAB
  run a11_base_fix_T.txt -scene T -n 400 -seed 9000 -fixentry -tab $TAB
  for d in 0.5 0.7 0.9 1.2; do run a12_vuoto${d}_D.txt -scene D -beh 0 -vlo 1.2 -vhi 1.2 -drop $d -n 200 -seed 9000 -tab $TAB; done
  run a12_vuoto0.7_fix_D.txt -scene D -beh 0 -vlo 1.2 -vhi 1.2 -drop 0.7 -fixentry -n 200 -seed 9000 -tab $TAB
  run a13_corpo_c6no_T.txt -scene T -beh 0,2 -body 0.45 -c6 0 -n 200 -seed 9000 -tab $TAB
  run a13_corpo_c6si_T.txt -scene T -beh 0,2 -body 0.45 -n 200 -seed 9000 -tab $TAB
  run a13_corpo_c6no_D.txt -scene D -beh 0,2 -body 0.45 -c6 0 -n 200 -seed 9000 -tab $TAB
fi
if [ "$G" = tutti ] || [ "$G" = tar2 ]; then  # avv-14: spostamento della distribuzione
  run a14_shift_T.txt -scene T -beh 0,2,3 -vlo 0.7 -vhi 0.9 -mix 0.68,0,0.20,0.12 -n 400 -seed 9000 -tab $TAB
  run a14_nominale_T.txt -scene T -beh 0 -vlo 1.15 -vhi 1.45 -mix 1 -n 400 -seed 9000 -tab $TAB
fi
echo fatto
