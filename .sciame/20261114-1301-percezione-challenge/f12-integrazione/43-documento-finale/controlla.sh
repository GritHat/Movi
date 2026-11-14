#!/bin/sh
# Controlli del redattore sul testo FINALE delle due pagine. Uso: sh controlla.sh   (dalla cartella 43-documento-finale)
# Copia di 40-documento/controlla.sh: controlla solo la parte prima di «FINE DEL TESTO»; cinque ricerche in più.
# Indipendenza: stesso autore del testo; vale per conteggi e ricerche testuali, non per il giudizio sul contenuto.
awk '/^<!-- FINE DEL TESTO -->/{exit} {print}' TESTO_DUE_PAGINE.md > .solo_testo.md
T=.solo_testo.md; C=CIFRE.md
echo "== 1. Parole (wc -w)"
echo "file intero:        $(wc -w < $T)"
awk '/^<!--/{h=1} h{print} /^-->/{h=0}' $T | wc -w | sed 's/^/intestazione:       /'
awk '/^```/{f=!f; next} f' $T | wc -w | sed 's/^/schema:             /'
grep '^|' $T | grep -v '^|---' | wc -w | sed 's/^/tabelle:            /'
grep '^>' $T | wc -w | sed 's/^/riquadro limiti:    /'
awk '/^<!--/{h=1} /^```/{f=!f; next} !h && !f && !/^\|/ && !/^>/ {print} /^-->/{h=0}' $T | wc -w | sed 's/^/corpo:              /'
echo "== 2. Righe delle tabelle (senza intestazione)"
awk '/^\|---/{n++; r[n]=0; next} /^\|/{ if(n>0 && prev ~ /^\|/) r[n]++ } {prev=$0} END{for(i=1;i<=n;i++) print "tabella " i ": " r[i] " righe"}' $T
echo "== 3. Frasi da non dire (V3 §3, SCH §6, BL §9, verdetto d'integrazione §7): occorrenze nel testo, senza l'intestazione"
awk '/^<!--/{h=1} !h{print} /^-->/{h=0}' $T > /dev/null
for f in 'validat' 'via libera' 'nessun ostacolo osservato' 'garanti' 'certificat' 'conforme a' 'tarato' 'bassa latenza' '\bperso\b' '\bsosta\b' 'si è fermato' 'è uscito' 'prevede dove sarà' 'livello 50' 'confidenza' 'ellisse' '30 prove' '218 000' '2 su 10 000' '2,7 m' 'mappa 3D' 'voxel' 'ostacoli bassi' 'vetro è risolto' '360°' 'massa e accelerazione' 'drone' '\bUAV\b' 'in volo' 'in movimento' 'detect and avoid' 'ACAS' 'TA/RA' 'bird' 'minaccia' 'preallarme' 'ispezion' 'orientamento' 'dispositivo medico' 'Intelligenza Artificiale' 'dal vivo' '100 %' 'soglia 40' '15 Hz' '0,2 m' 'in cinque ci sta' 'preproposta' '0,85 m' 'riconosc' '\bclassifica\b' 'distingue\b' 'gestisce' 'copre i veicoli' '1,4 m/s' '2,9 milioni' 'mai dato per mobile' 'criterio' 'continuità provata' 'si spegne quando' 'avviso utile' 'profilo migliore' 'accuratezza' 'fiducia' 'provato su carrelli' 'chiuso' 'sempre' 'mai dato' 'funzione di sicurezza' 'per prudenza' 'registrat'; do
  n=$(awk '/^<!--/{h=1} !h{print} /^-->/{h=0}' $T | grep -i -c -- "$f")
  [ "$n" != "0" ] && { echo "TROVATA «$f»: $n riga/righe"; awk '/^<!--/{h=1} !h{print} /^-->/{h=0}' $T | grep -i -o -- ".\{0,45\}$f.\{0,45\}" | sed 's/^/     … /'; }
done
echo "(fine elenco: ciò che non compare ha 0 occorrenze)"
echo "== 4. «9 su 10»: ogni occorrenza col suo contesto"
grep -o '.\{0,160\}9 casi su 10.\{0,60\}\|.\{0,160\}9 su 10.\{0,60\}' $T
echo "== 5. Cifre del testo che mancano in CIFRE.md"
python3 -I - <<'PY'
import re
rx=re.compile(r'\d+(?:[  ]\d{3})*(?:,\d+)?')
t=open('.solo_testo.md',encoding='utf-8').read()
t=re.sub(r'<!--.*?-->','',t,flags=re.S)
t=re.sub(r'(?m)^## \d+ · ','## ',t)          # numeri di sezione
t=re.sub(r'(?m)^\d+\. ','',t)                 # numeri d'elenco
t=re.sub(r'\bB\d\b','',t)                     # sigle dei blocchi dello schema
t=re.sub(r'\(\d\) ','',t)                     # numeri degli atti della demo
c=open('CIFRE.md',encoding='utf-8').read()
a=set(rx.findall(t)); b=set(rx.findall(c))
m=sorted(a-b)
print('cifre distinte nel testo:',len(a),'· mancanti in CIFRE.md:',len(m),m)
PY
