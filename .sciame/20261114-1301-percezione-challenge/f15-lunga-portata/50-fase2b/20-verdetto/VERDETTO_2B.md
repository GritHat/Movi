# Verdetto rapido sulle correzioni (fase 2b)

`sciame-arbitro`, 2026-11-15, dalle 02:59 alle 03:15 circa (`date -Is`). Previsioni e soglie scritte prima dei riconti
alle 02:59, in `PREVISIONI.md`. Riconto: `riconto_2b.py` → `riconto_2b_esito.txt` (in questa cartella), che rilegge i
record per passaggio di `10-riprova`, `11-controprova` e `02-eventi` e ricalcola i Wilson al 95 % con codice mio.
**Tutto è simulazione dalle schede: nessun sensore fisico, niente è «validato».** Etichette a mano. Solo osservazione
e avviso. Indipendenza: il riconto condivide con gli autori i file di esito e le definizioni dei campi
(`libero_viol`, `fuori_avviso`, `ritardo_evento_s`). Controlla solo l'aggregazione, non la misura.

**Previsioni del riconto.** 1, 2, 3 e 6 **reggono**: ogni k/n e ogni Wilson ritrovato è uguale a quello di RIPROVA e
CONTROPROVA. La 4 regge per RIPROVA (49/60) e CONTROPROVA (24/30). La 5 regge sui conteggi (36/60 e 20/30 ≥ 10 km),
ma le mediane non tornano (K-610). **Non ricontato, adottato col rinvio al file:** i casi costruiti di 01-nucleo
(`prove_v2_esito.json`), cp_X, cp_X5b, il validatore video (`11-controprova/valida_video_esito.json`) e `prova_tutto`.

## 1. Cambi di stato rispetto a VERDETTO_FASE2

**Regole violate dagli altri** (dai loro rapporti): 9 processi per circa 23 s (RIPROVA) e per la durata della misura
(EVENTI_V2). RIPROVA ha modificato, aggiungendo, file del prototipo di altri (`lungo.py`, `registro.py`,
`__main__.py`, `prova_tutto.sh`, `prova_registro.py`), con la copia di prima per uno solo: se la consegna lo
permettesse è **non verificato**. Nessuno dichiara cancellazioni. Io ho scritto solo in `20-verdetto`.

**Le otto correzioni.**

| # | Correzione | Applicata? | Esito |
|---|---|---|---|
| 1 | inviluppo (210 m/s; `multirotore_veloce` 45 m/s e 25 m/s², ipotesi) | **sì**, nel nucleo v2 | regge su X1 e X2 costruiti e su cp_X fino a 45 m/s. Oltre l'ipotesi (60 m/s) il drone esce dall'avviso a 8 s. **Effetto avverso:** l'impronta dei detriti di E1 esplode (§ 1, eventi) |
| 2 | passate correlate (n_eff = 1) | **sì** | regge (X4); il «libero» del multirotore scende a 877 m |
| 3 | mappa come ingresso di sicurezza | **nel nucleo sì** (predefinito non certificato) | **scavalcata nel prototipo**: `lungo.py:74` mette `MAPPA_CERTIFICATA_PREDEFINITA = True`, e la validazione-3 non è mai chiamata. X5 è **riaperto**: dietro un edificio non in pianta il punto risulta «libero» (cp_X5b) |
| 4 | «libero per ⟨classi⟩», C0 escluso | **sì** | regge per il C0. **Residuo:** nella famiglia «sito» elicottero, aereo leggero, auto e pedoni non sono né ammessi né esclusi (X6, CONTROPROVA § 2.5) |
| 5 | validazione-1 e 2 nel nucleo | **sì** | la validazione-1 regge (0 passaggi senza regione su 200 per ogni riga). Validazione-2: il Doppler regge per costruzione (A4: 0/85). **Col pannello è smentita nella famiglia sito** (sotto) |
| 6 | disturbo strutturato | no | — |
| 7 | occlusioni vicino agli ostacoli | no (la divisione per mezzo era già fatta) | — |
| 8 | rivisita IRIS (K-604) | no | non risolto |

**A1, A2, A3 col nucleo v2** (riprova n = 200 per riga, controprova n = 100; per passaggio; ricontati):

- **A1, tempestività nell'inviluppo dei droni: regge.** Alta e min: 200/200 [0,981; 1]. Controprova: 100/100
  [0,963; 1]. La previsione di VERDETTO_FASE2 § 9 (≥ 190/200) regge.
- **A1, «mai il mezzo fuori dall'avviso»: smentita in min.** 12/200 [0,035; 0,102] (6 «rallenta», 6 «ferma") e 9/100
  [0,048; 0,162] in controprova. In alta 0/200, ma solo 22 passaggi su 200 hanno una fase nascosta. La smentita
  scritta prima («un solo passaggio fuori avviso») è raggiunta. La causa (ricentramento, K-606) è **non verificata**.
- **A1, «libero» sull'oggetto col pannello, famiglia sito: smentita, ed è peggiorata.** Passaggi non C0: 163/171
  [0,910; 0,976] e 85/85 [0,957; 1]. Era 7/40 col v1 nel pilota. Nella famiglia «aeroporto» (D1): 0/171
  [0; 0,022], ma con 8 falsi confermati di mediana (contro 0), e con l'operatore non avvisato in tempo per gli aerei.
  Se la prova sia vuota là è **non verificato**.
- **A2, rullaggio: regge.** 200/200 tempestivi; 0/200 fuori avviso, 0/200 senza regione, 0/200 «libero»
  sull'oggetto. Solo 34/200 passaggi hanno una fase nascosta.
- **A3: regge come limite.** 0/200 «libero» sul drone sotto la copertura. La tempestività resta non misurata per
  costruzione.
- **Aerei in volo:** il nucleo v2 calcola e scrive «avviso non tempestivo» (3410 m > 877 m). È sostenuto su un caso
  costruito ed è coerente con l'ADDENDUM.
- **A4:** 95/100 tempestivi [0,888; 0,978], 9/100 fuori avviso: il difetto del v1 resta.

**Eventi** (strato `eventi_v2`; riprova col nucleo v2, n = 60; controprova n = 30):

- **E1 entro 2 s: resta smentito, ma da 1/16 sale a 49/60 [0,701; 0,894]** (controprova 24/30 [0,627; 0,905]). I
  ritardi vanno da 1,2 a 2,2 s. Frammenti dentro V: 0,9973, smentito contro ≥ 0,999. «Libero» su un frammento: 0/60
  passaggi [0; 0,06], ma **per costruzione**.
  - **Controesempio nuovo:** l'impronta ha raggio ≥ 10 km in 36/60 passaggi [0,474; 0,714] (20/30 in controprova),
    con mediana 42 km e massimo 74 km. L'ispezione non c'è: l'avviso resta perpetuo, su tutte le 69–119 tracce.
    Col nucleo v1 la mediana era 16 km (stessi 36/60 ≥ 10 km). La correzione 1 moltiplica il difetto, che non crea.
- **E2: da smentito (0/32) a sostenuto in forma debole.**
  - Evento dedotto in 60/60 [0,94; 1] (0,2–0,3 s), **solo con l'innesco ottimista**: la saturazione è presa dal punto
    vero.
  - Camere dichiarate non affidabili: 60/60.
  - Mezzo avvisato a ≥ 140 m dai frammenti veri: 60/60. Dall'impronta: 0/60, perché l'impronta di circa 3,5 km
    contiene già il mezzo. L'avviso è giusto, ma non discrimina.
- **E3:** invariato, non rifatto per passaggio col v2, non indipendente. Nel registro `lp_E3` la portata passa da
  1062 a 1041 m.
- **E4 ed E5: da smentiti a reggono.** E4: 0/60 + 0/60 (v2) e 0/30 + 0/30. E5: 0/300 [0; 0,013] col nucleo v1 e
  0/30 col v2. Il passaggio 31 di E1 dà però una «separazione» falsa 12,5 s prima dell'urto (1/60).

**Contraddizioni nuove.**

| K | Contrasto | Vale | Prova |
|---|---|---|---|
| K-609 | EVENTI_V2 «E1 51/60» | **50/60** con 0 ≤ ritardo ≤ 2 s: il 51° è il passaggio 31, a −12,5 s | `riconto_2b_esito.txt` |
| K-610 | CONTROPROVA «mediana 46 km» (riprova) e «59 km» (cp) | ricontate **42,1 km** e **57,0 km**; i conteggi ≥ 10 km tornano | idem; la causa dello scarto è non verificata |
| K-611 | RIPROVA «`lp_A1` 0 errori» contro CONTROPROVA «56 celle libere nell'avviso» | **tutti e due veri**: il validatore del registro non controlla il «libero» dentro l'avviso, e il record del passaggio 33 (sito) ha `libero_viol` multirotore = 2 | `riprova_passaggi.jsonl`, idx 33 |
| K-612 | nucleo «mappa non certificata per difetto» contro prototipo `True` | nel prototipo **vale `True`**: X5 riaperto | cp_X5b |
| K-613 | famiglia sito (tempestiva, «libero» sull'oggetto) contro aeroporto (nessun «libero», più falsi, non tempestiva per gli aerei) | **decisione del coordinatore** | RIPROVA § 2 |

## 2. Affermazioni convergenti (aggiornate, al più dodici)

1. **(Caso centrale: sito sorvegliato, droni)** «In simulazione da scheda, un drone a 15–21 m/s che sparisce dietro
   un edificio del sito è stato annunciato in tempo all'operatore (gli servono 806 m, la traccia era confermata a
   circa 950 m) in 200 passaggi su 200 e in altri 100 su 100 con semi nuovi. L'avviso di possibile presenza l'ha
   contenuto per tutta l'ombra in 188 passaggi su 200; nei 12 in cui il drone rallenta o si ferma l'avviso l'ha perso
   per qualche ciclo, e lo diciamo.» · S (Pd ipotetica) · `10-riprova/riprova_passaggi.jsonl`, `11-controprova/cp_A_*`.
2. **(Caso centrale: rullaggio)** «Un aereo in rullaggio nascosto da un hangar, con radar di superficie, LiDAR e
   ADS-B: avviso in tempo in 200 passaggi su 200, mai fuori dall'avviso, mai "libero" sull'aereo. Col solo radar era
   in tempo in 50 su 200: un sensore solo non basta.» · S · riprova A2; 11-prove (v1) per il solo radar.
3. **(Aerei in volo, limite)** «Per gli aerei in volo (fino a 210 m/s) l'avviso non arriva in tempo all'operatore di
   sito (servono 3,4 km, il "libero" arriva a 0,88 km), e MoVi lo scrive in ogni uscita: "avviso non tempestivo".» ·
   S, caso costruito · `01-nucleo/prove_v2_esito.json`.
4. «Un radar d'aeroporto non vede un drone sotto la sua copertura. MoVi non lo chiama mai "libero" (0 passaggi su
   200) e scrive "zona non verificata per i multirotori".» · S, e per costruzione · riprova A3, registro `lp_A3`.
5. «L'avviso si spegne solo dopo aver guardato tutta la zona dove il mezzo può essere, oppure quando lo si rivede. La
   regola ingenua lo spegneva in 564 passaggi su 2400; ora è nel nucleo, e 0 passaggi su 200 restano senza regione.»
   · S · 11-prove (v1), riprova.
6. «Il limite di velocità copre i droni veloci fino a 45 m/s (ipotesi, senza fonte) e gli aerei fino a 210 m/s. Le
   passate correlate non sommano la probabilità di vedere: il "libero" per un drone scende a circa 0,9 km.» · S, casi
   costruiti · `01-nucleo`, cp_X.
7. «Quando un sensore cade, o una fiammata o la pioggia lo accecano, MoVi lo dice: camere dichiarate non affidabili
   entro 3 cicli in 90 passaggi simulati su 90.» · S · riprova E2 e cp_E. Il 460/460 entro 5,3 s è del v1 e non è
   rifatto.
8. «Fumo, detriti in pista e passaggi ravvicinati non hanno prodotto falsi eventi improvvisi (0 su 120 e 0 su 60 col
   fumo, 0 su 300 e 0 su 30 a 5 m).» · S · `02-eventi`, riprova, cp_E.
9. **(Eventi improvvisi, forma che regge)** «Dopo una collisione fra droni MoVi deduce l'evento in 1,2–2,2 s (entro 2 s
   in 49 passaggi su 60), e non chiama mai "libero" dove possono cadere i frammenti. Ma oggi la zona dei detriti è
   enorme (in 36 passaggi su 60 più di 10 km), non si riduce, e l'avviso non distingue chi è in pericolo.» · S, e X
   come utilità · riprova_eventi, cp_E.
10. «"Libero" vale solo per le classi dichiarate: i droni sotto i 250 g sono "zona non verificata".» · S · riprova (C0).
11. «Il nome della classe non spegne l'avviso.» · per costruzione; 228/228 cicli in un passaggio col **v1**, non
    rifatto col v2.
12. **(Limite)** «Il "libero" può essere falso: col pannello radar, nella configurazione del sito, quasi tutti i
    passaggi (163 su 171) hanno istanti con "libero" sul drone; un edificio non in mappa apre un "libero" falso se la
    mappa è dichiarata completa, come fa oggi il prototipo.» · X · riprova, cp_X5b.

Il prototipo: `prova_tutto.sh` dà esito 0 in 665 s; le 20 scene col v2 hanno 0 errori; L1 e L3 sono riprodotte col
v1. È verificato, non ricontato, e non indipendente (stesso codice).

## 3. Da non dire

- Restano dalla fase 2: «validato» (e i suoi equivalenti), «in tempo reale», «certificabile», «detect and avoid»,
  «rileva droni a N km», «zero falsi allarmi», «122 droni», il lessico d'ingaggio e quello della scheda IRIS, le
  cifre di tempestività per A3.
- **Nuove o aggiornate:**
  - «avviso tempestivo per gli aerei in volo»;
  - «l'avviso contiene sempre il drone» (12/200);
  - «MoVi non dichiara mai libero ciò che non ha osservato», senza le condizioni (classi, mappa certificata, e
    smentito col pannello nel sito);
  - «dichiara le collisioni entro 2 s» e «sempre»;
  - «individua chi è minacciato dai detriti» o «zona dei detriti precisa»;
  - «rileva la fiammata» come capacità del sensore: l'innesco è ottimista;
  - «tutte le correzioni sono applicate» (6, 7 e 8 no; la 3 è scavalcata dal prototipo);
  - le mediane di CONTROPROVA (46 e 59 km);
  - «E1 51/60».

## 4. Limiti da dire per primi

1. Nessun sensore fisico; le Pd, i falsi allarmi e le latenze sono ipotesi. Lo stesso vale per i 45 m/s e i
   25 m/s² del drone veloce.
2. Gli aerei in volo sono fuori dal caso centrale: per loro l'avviso non è tempestivo, ed è dichiarato.
3. Il «libero» è falso col pannello nella configurazione del sito (163/171), e con una mappa dichiarata completa ma
   sbagliata (prototipo).
4. L'avviso perde il drone che rallenta o si ferma in circa 6 % dei passaggi (12/200).
5. Gli eventi improvvisi sono dedotti, entro 2 s in 49/60. La zona dei detriti copre il sito e non si riduce; la
   fiammata è rilevata con un'ipotesi ottimista.
6. Un solo multirotore e un solo ala fissa reali nelle traiettorie (fase 2, invariato).

## 5. Le scene del video (`prototipo/uscite/video/INDICE.md`)

| Scena | Verdetto | Motivo |
|---|---|---|
| `lp_A1` | **solo «Schematic»** | Registro valido (0 errori), ma non coerente con le prove: il record del passaggio 33 ha 2 istanti «libero» sul drone; ci sono 56 celle-fotogramma «libero» dentro l'avviso proprio nel momento centrale (46–47,5 s); e il passaggio è scelto dopo. Diventa «Simulation» rigenerato con avversario-3 e con il validatore a 0, oppure nella famiglia aeroporto (K-613) |
| `lp_A1_ingenua` | **«Simulation»**, come contrasto e con la scritta «regola ingenua (v1)» | i 7 errori sono attesi, e coerenti con 564/2400 |
| `lp_A2` | **«Simulation»** | 0 errori, validatore a 0, coerente con 200/200 |
| `lp_A3` | **«Simulation»** | La scritta «zona non verificata per i droni» va presa dal campo del registro, perché il visore non la disegna. Nessuna cifra di tempestività |
| `lp_E1` | **solo «Schematic»** | Il passaggio 0 (impronta di 4,5 km) non è rappresentativo (mediana 42 km); il visore non disegna i detriti; E1 è smentito entro 2 s |
| `lp_E2` | **«Simulation» solo per le camere dichiarate non affidabili**; i detriti e l'avviso al mezzo solo «Schematic» | l'innesco è ottimista e l'impronta contiene il mezzo |
| `lp_E3` | **«Simulation»** | la riduzione è piccola (1062 → 1041 m) e non indipendente: va detto |
| `lp_E4` | **«Simulation»** | nessun falso evento, coerente con 0/60 e 0/30 |

Per tutte le scene: nei primi 2–3 fotogrammi le celle mostrate (576 «non osservato») non corrispondono ai `conteggi`
vuoti. L'errore va nel verso prudente, ma va corretto o tagliato. La griglia mostrata può avere fino a 2 s
(plausibile, non verificato).

## 6. Che cosa resta aperto

1. **K-613 (decisione del coordinatore):** la famiglia di A1. Prova: legare la W_c alla v_max vera. Previsione di
   RIPROVA: ≤ 2/171; smentita se ≥ 10/171.
2. Il fuori avviso in A1 min (12/200): misurare il centro dell'avviso ciclo per ciclo nei 12 passaggi.
3. Togliere `True` dalla mappa nel prototipo, oppure chiamare la validazione-3: rifare cp_X5b.
4. E1: avversario-1 (t_a solo da origini recenti), fusione dei duplicati, ispezione dell'impronta (avversario-2).
   Previsione: mediana ≤ 5 km; smentita se ≥ 10 km in ≥ 5/30.
5. Lo strato eventi col nucleo v2 per E3 ed E5 per passaggio, e la fiammata col rilevamento nel simulatore più un
   caso avversario (sole o riflesso).
6. Le correzioni 6–8 e X6 nella famiglia sito (avversario-4).
7. Rifare `lp_A1` e `lp_E1` scelti a caso, con il validatore di CONTROPROVA.
