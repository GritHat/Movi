#!/bin/sh
# Rilancia i banchi di sicurezza e di costo della previsione (copie dei sorgenti d'origine, compilate qui).
# Un processo alla volta, ognuno sotto timeout. Uso: sh rilancia_sicurezza.sh [nucleo]
cd "$(dirname "$0")" || exit 1
C=${1:-2}; U=uscite; mkdir -p $U
echo "# inizio $(date -Is) nucleo=$C carico=$(cut -d' ' -f1-3 /proc/loadavg)" > $U/registro_sicurezza.txt
( cd banco_lettura && gcc -O2 -o vq3c vq3c.c -lm && gcc -O2 -o torneo torneo.c -lm ) || exit 1
( cd banco_sicurezza && gcc -O2 -Wno-misleading-indentation -o banco banco.c -lm -lpthread ) || exit 1
( cd banco_previsione && gcc -O2 -Wall -Wno-misleading-indentation -o att att.c -lm ) || exit 1
timeout 120 taskset -c $C banco_lettura/vq3c > $U/lettura_vq3c.txt 2>&1 || echo "FALLITO vq3c" >> $U/registro_sicurezza.txt
for t in statica s10 a2 a3 a9 a5c scenB a10; do
  timeout 120 taskset -c $C banco_lettura/torneo $t > $U/torneo_$t.txt 2>&1 || echo "FALLITO torneo $t" >> $U/registro_sicurezza.txt
done
( timeout 120 taskset -c $C banco_lettura/torneo k106 ; timeout 120 taskset -c $C banco_lettura/torneo k106 3c ) > $U/torneo_k106.txt 2>&1
timeout 120 taskset -c $C banco_sicurezza/banco sicurezza tipica 5 4 > $U/sicurezza_tipica_5_4.txt 2>&1 || echo "FALLITO sicurezza" >> $U/registro_sicurezza.txt
timeout 120 taskset -c $C banco_sicurezza/banco vecchi 5 Q > $U/vecchi_5_Q.txt 2>&1 || echo "FALLITO vecchi" >> $U/registro_sicurezza.txt
for n in 1 10 60 120; do timeout 120 taskset -c $C banco_previsione/att tempo geo=T n=$n | tail -1; done > $U/previsione_C.txt 2>&1
PYTHONDONTWRITEBYTECODE=1 timeout 120 taskset -c $C python3 -I banco_previsione/tempo_py.py > $U/previsione_py.txt 2>&1 || echo "FALLITO tempo_py" >> $U/registro_sicurezza.txt
timeout 120 taskset -c $C python3 -I -B banco_strutture/py_puro.py > $U/strutture_py_puro.txt 2>&1 || echo "FALLITO py_puro" >> $U/registro_sicurezza.txt
echo "# fine $(date -Is) carico=$(cut -d' ' -f1-3 /proc/loadavg)" >> $U/registro_sicurezza.txt
