# Previsioni dell'attacco alla versione 3 (sciame-avversario, f12, 10-attacco)

Scritte alle 2026-11-14T18:11:26+01:00, dopo aver letto il contratto d'integrazione, SOLUZIONE_V3.md, PROVA_INSIEME.md e
LIBERO_DELLA_CELLA.md (quindi NON cieche rispetto ai loro numeri), e PRIMA di aprire il codice e di lanciare qualsiasi prova mia.

| # | Attacco | Misura | Previsione | Soglia di smentita (del MIO attacco) |
|---|---|---|---|---|
| P1 | La regola del «libero» scritta nel §1.2 della V3 (un pixel valido dell'impronta; ripiego stato(centro a 0,20 m)) e' quella che la prova 03-libero rompe | rilancio di 03-libero/rifai.sh: fotogrammi con violazione per «V-018 un pixel» e per il ripiego | > 0 fotogrammi per entrambe (attesi circa 98 e 1732 su 7200); nuvole-1 a 0 | se «V-018 un pixel» da' 0 violazioni, l'attacco non rompe |
| P2 | La tolleranza di posa della V3 (1 grado all'avvio e nella salute) e' fuori dal dominio in cui nuvole-1 tiene (0,5 gradi) | celle libere dentro un corpo o con suolo nascosto con errore d'inclinazione +1 o -1 grado, regola nuvole-1 (PR4), banco 03-libero | almeno 1 cella in almeno 1 fotogramma | 0 celle a +-1 grado: l'attacco non rompe |
| P3 | Anello cieco: un oggetto alto 0,35 m e largo 0,30 m a 0,9 m dal sensore non e' visto, e il settore dice «suolo visto libero fino a d» con d oltre l'oggetto | programma mio sul modello di camera e sulla regola di 03-libero/libero.py: celle occupate sull'oggetto; d del settore centrale | 0 celle occupate; d = 3,0 m in almeno il 90 % dei fotogrammi (30 fotogrammi, k 0,004 e 0,010) | celle occupate > 0 oppure d <= 1,3 m («sconosciuto») in piu' del 10 % dei fotogrammi |
| P4 | Ostacolo sottile sospeso: barra orizzontale spessa 1 cm a quota 0,8 m, a 2,0 m, larga quanto il campo | stesso programma: quota dei settori-fotogramma (5 settori centrali x 30 fotogrammi) in cui nessuna cella del settore e' «occupato» a 1,9-2,1 m e d > 2,1 m | almeno il 30 % con k = 0,010; almeno il 10 % con k = 0,004; con 5 % di buchi sparsi almeno il 30 % | sotto il 5 % in tutte le condizioni: l'attacco non rompe |
| P5 | Il ripiego della V3 per il riaggancio («finche' C-C non e' passata: 0,40 m dall'ombra d'ingresso», N-C1) lascia cadere l'avviso con l'estraneo | banco 02-prova-insieme/insieme, lanci d_*_c1no, su semi MIEI se il programma lo permette, altrimenti rilettura dei file ris/ | identita' sbagliata in almeno il 40 % dei riagganci in tutte e tre le geometrie | sotto il 5 % in una geometria: li' il ripiego regge |
| P6 | La catena f10 che la squadra riuserebbe contraddice la V3 in almeno 4 regole di sicurezza con riga | lettura del codice (grep con numero di riga): memoria del «libero», stato «perso» o timer che chiude, rilascio dell'avviso, soglia di pixel, assenza del blocco salute | almeno 4 righe in contraddizione, di cui almeno 1 che toglie un avviso o crea un «libero» senza sguardo | meno di 2: l'attacco non rompe |
| P7 | «Rilascio cella per cella» (1.7) nel dominio dichiarato (sensore fermo, occlusore fermo) non rilascia mai nessuna cella: l'avviso finisce SOLO col riaggancio d'identita' | conto su griglia polare, geometria della demo: celle di R100 che possono essere «libero» ORA e stanno oltre 0,40 m dal cuneo | 0 celle (per costruzione): quindi I7 ha un solo ramo vivo, quello che l'estraneo rompe | > 0 celle rilasciabili a occlusore fermo |
| P8 | La cifra «100 % degli istanti dentro l'area d'avviso» (§7 punto 4) e' una tautologia: «nascosto» = centro nell'ombra vera, R100 = ombra stimata + 0,40 m | banco insieme: stessa misura con l'ombra stimata piu' stretta di 0,45 m (e=-0.45), n=400, geometria T | > 0 istanti fuori da R100; con e=-0.20 e e=-0.10 resta 0 | 0 fuori anche a -0,45 m: la misura non e' tautologica come dico |
| P9 | Formula della fascia (ultima riga di 1.7) contro il parametro: 0,20 + mezza larghezza (0,225) + 1,4 x (eta' 0,133 s + latenza 0,155 s) | conto | 0,83 m contro 0,40 m adottati: le due righe del blocco 1.7 non stanno insieme | la formula da' <= 0,40 m |

Stati possibili per ogni attacco: rompe / non rompe / non risolto. Cio' che noto dopo le prove va nel rapporto sotto «notato dopo».

## Aggiunte alle 2026-11-14T18:16:11+01:00 (dopo gli esiti di P1-P9, prima delle due prove nuove)

| # | Attacco | Misura | Previsione | Soglia di smentita |
|---|---|---|---|---|
| P10 | Copertura del sensore e ritorno (1.9): «regione <- (regione dilatata) ∩ non osservato», letta con il vocabolario della V3 («non osservato» = quarto stato, diverso da «in ombra») | conto sulla griglia di 03-libero, pannello di 1 m a 1,8 m: persona vista a sinistra, sensore coperto 2 s, la persona va dietro il pannello; al ritorno la sua cella sta nella regione? | lettura letterale: NO (la cella e' «in ombra», non «non osservato»): persona nascosta senza regione; lettura «non visto libero»: SI | la cella risulta nella regione anche con la lettura letterale |
| P11 | c7 (avviso per ogni traccia chiusa o non confermata entro 0,75 m da un'ombra) contro i fantasmi di F-403, con l'avviso senza tetto e il rilascio che a occlusore fermo non scatta (P7) | uscite di f10 gia' su disco (20-validazione/uscite/sim, sequenze nominali col pannello; catena f10 coi parametri del nucleo): tracce che finiscono senza entrare in ombra, con l'ultima posizione entro 0,75 m da una cella «in ombra» del fotogramma | mediana di almeno 3 per sequenza: altrettanti avvisi che nessuna regola della V3 puo' piu' spegnere | mediana 0 |

## Aggiunta alle 2026-11-14T18:17:25+01:00 (prima del lancio)

| # | Attacco | Misura | Previsione | Soglia di smentita |
|---|---|---|---|---|
| P12 | Il limite inferiore di 0,3 m/s (c5 com'e' scritta in 1.6) contro chi parte da fermo accanto all'ostacolo | banco insieme, semi miei (seme=31000000000), geometrie D e T, beh=8, n=800: quota «dentro la zona» a 1 s (R90 grezza e mostrata) con vmin=0.3, con vmin=0 e con c5b=1 | con c5 scritta: sotto 0,90 a 1 s in entrambe (attesa 0,70-0,80); senza c5 sotto 0,30; con «fermo negli ultimi 2 s» sopra 0,90 | con c5 scritta >= 0,90 a 1 s in entrambe: l'attacco non rompe |
