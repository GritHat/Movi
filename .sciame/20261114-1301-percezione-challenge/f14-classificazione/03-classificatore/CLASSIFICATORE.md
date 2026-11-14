# Il componente classificatore: specifica, stato dell'arte, protocollo con etichette a mano — f14, `03-classificatore` (`sciame-ml`)

14 novembre 2026, lavoro dalle 18:33 alle 18:40 (`date -Is`). Accanto: `PREVISIONI.md` (18:34:17, prima della rete e dello script), `oracolo_degradato.py` (numpy, seme 20261114), `esito_oracolo.txt` (la sua uscita, 18:35:22).

## 0. In testa

**Cambi di stato proposti** (li assegna l'arbitro): `ml-1` «con la regola *solo allarga* un'etichetta non porta mai la velocità usata sotto la linea di base»: **per costruzione**, esercitata 0 volte su 480 000 conteggi; `ml-2` «la regola ingenua (la classe decide la velocità) restringe l'avviso anche con etichette giuste»: **sostenuta dai dati in simulazione** (59 % delle tracce); `ml-3` «COCO copre 9 tipi della tassonomia, non carrello elevatore, tram, multirotore, carrozzina»: **verificato** sull'elenco letto oggi; `ml-4` «un modello pronto basta per queste classi a 3 m su questo sensore»: **non risolto** (nessun modello eseguito); `ml-5` «l'etichetta arriva in tempo per le classi veloci entro 3 m»: **smentito per conto** (§5, RC-3).
**Regole violate:** nessuna che io sappia (niente git, sudo; scritture solo in questa cartella; nelle richieste in rete nessun nome né dettaglio del progetto). **Scostamenti.** (a) L'ambiente chiede di non scrivere file di rapporto: la consegna chiede questo file, e ho seguito la consegna. (b) Lo strumento di rete ha salvato da sé il PDF di TIDE nella cartella della sessione, fuori dalla mia: letto come dato (pagine 3–6), niente eseguito. (c) Della soluzione finale ho letto §0, 1.6, 1.7, 1.10, §2, §3; non i fascicoli f13 né i verdetti f8 e f10: le loro cifre le prendo dalla soluzione e **non le ho ricontate**. (d) Le velocità per classe dello script sono **ipotesi mie** di lavoro: i profili veri li fissa un altro ruolo (L-2).
**Indipendenza.** Script, matrici, velocità e regola hanno un solo autore (io); lo script non esegue la catena vera (`insieme.c`, mappa, avviso): vale solo per la grandezza «velocità massima usata».

## 1. Tassonomia e regola di ripiego

| Categoria | Tipi (fra parentesi quadre: c'è in COCO) |
|---|---|
| persona | pedone [person]; persona su carrozzina; persona con ausilio o carico |
| veicolo terrestre | bicicletta [bicycle]; motociclo [motorcycle]; auto [car]; furgone e camion [truck]; autobus [bus]; carrello elevatore; transpallet; veicolo a guida automatica; mezzo di piazzale (trattore, carrello bagagli, nastro) |
| veicolo ferroviario | treno [train]; tram; mezzo di manovra |
| aeromobile | aereo a terra, in rullaggio o trainato [airplane]; elicottero a terra; multirotore; ala fissa senza equipaggio |
| oggetto mobile generico | carrello a mano; porta, cancello, barriera; carico sospeso; animale; oggetto che rotola o cade |
| non classificato | — |

**Ripiego.** Vale il tipo se p(tipo) ≥ τ; altrimenti la categoria se la somma dei suoi tipi ≥ τ; altrimenti «non classificato» (τ = 0,7: **ipotesi**, da tarare). **Regola dell'involucro:** il profilo cinematico di una categoria è il caso peggiore dei suoi tipi (velocità e accelerazione massime, unione dei gradi di libertà); quello di «non classificato» è il caso peggiore delle classi ammesse dalla configurazione del sito. Così salire nella gerarchia allarga sempre e non restringe mai. I gradi di libertà vincolati (binario, raggio di sterzata) non restringono mai R100.

## 2. Interfaccia

- **Ingressi, per traccia:** ritagli di profondità (e RGB, se il sensore lo dà: **non deciso**) degli ultimi fotogrammi con la maschera del gruppo; dimensioni metriche del gruppo e marca «tagliato»; storia della traccia (posizioni, velocità del filtro, massima osservata, cambi di direzione); stato di visibilità; salute del sensore.
- **Uscite:** distribuzione sui tipi; `classe` dopo il ripiego e suo `livello` (tipo, categoria, non classificato); `fiducia` con la marca «tarata sì/no»; `origine` ∈ {**a mano**, **simulata** (matrice e ritardo), **modello** (nome, versione)}; `età` dell'etichetta; `coerenza cinematica` (regge / violata); `fuori distribuzione`.
- **Frequenza:** asincrono, 1–2 Hz per traccia o a evento (traccia confermata, riaggancio, coerenza violata). Il ciclo a 15 Hz non aspetta mai. **L'etichetta è una proprietà della traccia, non del fotogramma**: ha un'isteresi, durante l'occlusione resta con la sua età («etichetta di 2,3 s fa»), al riaggancio con identità «presunta» è presunta anch'essa e non passa attraverso un'identità ambigua.
- **Finché l'etichetta non c'è:** la traccia è «non classificato», con l'involucro del sito. La catena lavora come la versione 3 di oggi, che non usa etichette.
- **Clausole di sicurezza del contratto** (I5 e I7 restano come sono):
  - **C-1** il classificatore scrive solo `classe`: non scrive «libero», non rilascia un avviso, non abbassa un livello;
  - **C-2, «solo allarga»:** ogni grandezza che dimensiona un avviso vale max(valore di base del sito, valore peggiore fra le classi con probabilità ≥ ε); un'etichetta allarga o lascia com'è;
  - **C-3, coerenza a un solo verso:** velocità o dimensioni osservate oltre il profilo della classe degradano l'etichetta verso la categoria o «non classificato»; la cinematica può smentire un'etichetta «lenta», mai confermarla per restringere;
  - **C-4** occupato, ombra e avviso nascono dalla geometria: un oggetto che il classificatore non vede esiste lo stesso per la mappa.
- **Livello dichiarato di 1.6:** i 400 percorsi registrati sono di pedoni. Per ogni classe diversa da «persona» propongo predittore sd-0 con la velocità della classe e **nessuna cifra**.

## 3. Stato dell'arte (pagine aperte oggi, 14-11-2026, salvo dove è detto)

| Tema | Fonte e link | Che cosa ho letto | Stato |
|---|---|---|---|
| Classi COCO | [coco.yaml di Ultralytics](https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/datasets/coco.yaml) | 80 nomi: 0 person, 1 bicycle, 2 car, 3 motorcycle, 4 airplane, 5 bus, 6 train, 7 truck, 8 boat…; assenti forklift, tram, drone, scooter, wheelchair | verificato su quel file (non sull'articolo di COCO) |
| RF-DETR | [deposito](https://github.com/roboflow/rf-detr) | codice Apache-2.0; rilevamento N, S, M, L Apache-2.0; Atto, Femto, Pico, XL, 2XL sotto PML 1.0; N: 48,4 AP, 30,5 M di parametri, 384 px, 2,3 ms; S: 53,0 AP, 3,5 ms; latenze su NVIDIA T4, TensorRT, FP16 | letto; **nessuna latenza su CPU dichiarata** |
| YOLO26 | [deposito](https://github.com/ultralytics/ultralytics) | AGPL-3.0 oppure licenza aziendale; YOLO26n 640 px: 40,9 mAP, 38,9 ± 0,7 ms CPU ONNX, 2,4 M; YOLO26s: 48,6 mAP, 87,2 ms, 9,5 M; CPU non nominata nella tabella (istanza EC2 P4d) | letto; sul portatile della squadra **non verificato** |
| Carrello elevatore | [LOCO](https://github.com/tum-fml/loco) | 37 988 immagini, 5 593 annotate, 152 421 annotazioni; classi: forklift, pallet truck, pallet, small load carrier, stillage; CC0-1.0; ICMLA 2020 | letto; RGB, non profondità |
| Mezzi di piazzale | [Apron Dataset](https://github.com/apronai/apron-dataset) | 43 categorie fini; dati **a richiesta**, uso non commerciale; ACCV 2022 Workshops, pp. 147–163 | letto il deposito; numero d'immagini non letto |
| Guida automatica, tram, multirotore | solo risultati di ricerca (insiemi su Roboflow, uno lidar di magazzino) | niente aperto | **non verificato** |
| Sola profondità | [Gupta et al. 2014](https://arxiv.org/abs/1407.5736); [PointNet, Qi et al. 2016](https://arxiv.org/abs/1612.00593) | riassunti: la profondità codificata come disparità, altezza dal suolo e angolo con la gravità; una rete che legge direttamente la nuvola di punti | esistono i metodi; su queste classi a 3 m **non verificato** |
| Cinematica | [Ristic, Gordon, Bessell 2004](https://doi.org/10.1016/j.inffus.2003.08.002), Information Fusion 5(1), 15–21; [Chiu et al. 2020](https://arxiv.org/abs/2001.05673); [arXiv 2410.13616](https://arxiv.org/html/2410.13616) (Kyrkou e un coautore) | del primo solo il registro Crossref; del secondo il riassunto (Kalman con covarianze dalle statistiche dei dati, distanza di Mahalanobis); del terzo il §V-B2: camion confusi col fondo nel 35 %, con autobus 10 %, con auto 12 %; con la differenza fra fotogrammi la confusione camion→autobus sale al 30 % | il filone esiste; contenuto del primo e parametri per classe del secondo **non verificati**; il terzo è su riprese aeree, altro dominio |
| Taratura e fuori distribuzione | [Guo et al. 2017](https://arxiv.org/abs/1706.04599); [Hendrycks e Gimpel 2016](https://arxiv.org/abs/1610.02136); `kuzucu2024` in `documentazione/RIFERIMENTI.md` [49] | riassunti: le reti moderne sono tarate male, la scala di temperatura funziona; la probabilità massima come linea di base. Il terzo non riaperto: lo dà verificato il curatore | letti i riassunti |
| Errori dei rilevatori | [TIDE, Bolya et al. 2020](https://arxiv.org/abs/2008.08115) | PDF, pp. 3–6: sei tipi (classificazione, localizzazione, entrambi, doppione, fondo, mancato) | letto; i valori per rilevatore **non letti** |

**Che cosa ne segue.** Un rilevatore pronto su COCO dà 9 tipi su circa 25 e chiede l'RGB; per carrello e piazzale servono dati dedicati, per il resto non ho trovato niente di verificato. Il movimento aiuta a trovare l'oggetto ma può aumentare la confusione fra classi che si muovono allo stesso modo (un solo lavoro, altro dominio): la cinematica va usata come controllo di coerenza (C-3), non come prova della classe.

## 4. Che cosa vuol dire «simulato», e il protocollo

- **(a) Oracolo, «A MANO»:** l'operatore della prova assegna la classe alla traccia da un copione della scena o da tastiera.
- **(b) Oracolo degradato, «SIMULATA · matrice · ritardo»:** la stessa etichetta passa da una matrice di confusione dichiarata e da un ritardo dichiarato, con seme fisso. Misura la sensibilità del sistema, non un classificatore.
- **(c) Modello vero, «MODELLO»:** non realizzato; questa origine nel prototipo non compare mai.

**Misure.** M-1 copertura della regione di previsione per classe (istanti nascosti con la posizione vera dentro R90, limite di Wilson): dati veri ci sono solo per «persona»; per le altre classi le traiettorie sarebbero sintetiche dal profilo, cioè **ipotesi**. M-2 sicurezza dell'avviso: cicli in cui l'avviso con etichette è più stretto di quello senza (soglia 0), e passaggi con la posizione vera fuori da R100, per classe vera × classe assegnata. M-3 tempo fino alla prima etichetta, dal quarto ciclo della traccia: in (a) è il tempo dell'operatore, e si dichiara tale. M-4 cambi d'etichetta per traccia (al più un evento sonoro).
**Matrici.** Identità; uniforme al 10 %; «strutturata» (errori dentro la categoria; una sola riga ha un appiglio pubblicato, il camion di arXiv 2410.13616); «avversa» (ogni classe veloce diventa «persona» 2 volte su 10). **Tutte ipotesi dichiarate**: non ho trovato una matrice pubblicata fra classi COCO; la via giusta è misurarla su COCO val2017 con un rilevatore pronto (non fatto: 1–2 ore).
**Quante prove.** Al calcolatore 10 000 tracce per braccio (con 0 eventi il limite superiore al 95 % è 3 su 10 000). Al banco 30 passaggi per classe mostrata, in (a) e in (b) con la matrice avversa: con 0 eventi su 30 il limite è 10 %, quindi il banco mostra la regola, non la misura.

**Che cosa ho eseguito** (24 bracci = 4 matrici × ritardi 0, 0,5 e 2 s × linea di base 1,4 e 4,0 m/s; 7 classi con velocità **ipotetiche**):

| Regola | Tracce sotto la linea di base | Tracce sotto la velocità vera della classe (matrici con errori) |
|---|---|---|
| ingenua: la classe decide | 0 con base 1,4; **5 561–6 916 su 10 000 con base 4,0, di cui 5 928–5 984 con etichette tutte giuste** | 228–1 035 su 10 000 |
| solo allarga, etichetta secca | **0 in 24 bracci** | 160–1 004 su 10 000 |
| solo allarga, classi con probabilità ≥ 0,02 | **0 in 24 bracci** | 0 con la matrice avversa; 88–259 con le altre |

Il conto analitico per la regola ingenua (2,4 %, 5,8 %, 10,0 %) torna con i conteggi. **Limiti:** lo «0» è la proprietà di un massimo, non una misura del sistema. Il ritardo non sposta il conteggio per traccia (tutte durano più di 2 s): per conto, la quota di vita senza etichetta è 10 % con 0,5 s e 40 % con 2 s (r · ln 5 / 8). Con base 1,4 m/s tutte le 7 classi ipotizzate la superano: senza etichetta nessuna è coperta.
**Due cose che ne escono.** (1) «Solo allarga» protegge la linea di base, non la classe: una classe veloce etichettata «lenta» resta coperta quanto oggi, cioè poco. Solo una linea di base del sito pari alla classe più veloce ammessa azzera il caso, al prezzo di avvisi sempre larghi: è una scelta di configurazione, non del classificatore. (2) Con l'errore uniforme al 10 % e i treni al 2 % delle tracce, l'etichetta «treno» è giusta solo nel 52 % dei casi (0,018 / 0,0343): il requisito va scritto sulla precisione di ogni etichetta, non sull'accuratezza.

## 5. Requisiti per il classificatore futuro (nei documenti: «richiesto»; le soglie sono **ipotesi**)

- **RC-1 classi:** la tassonomia di §1, almeno a livello di categoria, con «non classificato» come uscita vera.
- **RC-2 fiducia tarata:** errore di taratura atteso ≤ 0,05 per classe, su dati dello stesso sito tenuti da parte; senza taratura la fiducia non si mostra.
- **RC-3 tempo fino alla prima etichetta:** ≤ 0,5 s dalla conferma della traccia. Conto: 3 m di portata si attraversano in 1,67 s a 1,8 m/s, in 0,75 s a 4 m/s, in 0,21 s a 14 m/s; la conferma chiede 4 cicli a 15 Hz, cioè 0,27 s. A 14 m/s l'oggetto ha attraversato la portata prima di essere una traccia; a 4 m/s l'etichetta arriva a cosa fatta. Per le classi veloci, in questo dominio, protegge la configurazione del sito e non l'etichetta.
- **RC-4 errori tollerati, asimmetrici:** innocui gli scambi fra profili uguali (auto e furgone, treno e tram) e da lento a veloce (costo: avvisi più larghi; ≤ 10 %). Non innocui: da veloce a lento (P(classe vera più veloce | etichetta lenta) ≤ 1 %) e da libero a vincolato (una persona o un multirotore etichettati «su binario»).
- **RC-5 fuori distribuzione:** un tipo mai visto esce «non classificato»; quota di oggetti ignoti con un'etichetta sicura ≤ 5 %. La probabilità massima è solo la linea di base; C-3 è la seconda barriera.
- **RC-6 stabilità:** al più un cambio d'etichetta ogni 2 s per traccia; nessuna etichetta nuova su un gruppo «tagliato».
- **RC-7 valutazione senza fughe:** partizioni per sito e per sequenza, mai per fotogramma (i fotogrammi della stessa traccia stanno tutti da una parte); prova su un sito mai visto; risultati per classe con intervalli e con la linea di base «sempre non classificato».

## 6. Schermo e frasi

**A schermo.** Sotto la traccia, in piccolo e grigio, dopo lo stato di visibilità: «persona · a mano»; «veicolo, tipo incerto · simulata»; «non classificato». La classe non cambia mai forma né colore del segno (quelli dicono osservato o previsto) e non è mai verde. **Nessuna percentuale**: in (a) e (b) sarebbe inventata, e «confidenza Z %» è già fra le frasi vietate. Riga fissa, sempre visibile: «CLASSIFICATORE SIMULATO · etichette assegnate a mano» (in (b): «· errori iniettati, matrice X, ritardo r s»). Il segnale di 0,3 s non dice la classe; la frase a stato stabile può dirla con l'origine.

**La frase vera.** «Il sistema richiede un classificatore su più classi e tipologie (persone, veicoli di tipo diverso, altri ostacoli in movimento) consapevole della velocità e dei gradi di libertà di ogni classe. In questo prototipo il classificatore è simulato: le etichette che vedete sono assegnate a mano da noi. In una seconda prova le sporchiamo apposta con errori dichiarati, per mostrare che un'etichetta sbagliata non toglie e non restringe un avviso. Nessun modello di classificazione è stato addestrato né valutato.»

**Da non dire.** «Riconosce auto, treni e aerei»; «classifica i veicoli»; «il modello distingue»; «accuratezza del X %» o qualunque percentuale di fiducia; «classificatore provato» o «validato»; «funziona con qualunque veicolo»; «a prova d'errore di classificazione» (vale contro la linea di base, non contro la classe vera); «provato su carrelli, treni, aerei» (nessuna traiettoria né sensore); «copre i treni» o altre classi veloci entro 3 m.

## 7. Ore (stime mie, non misurate)

Ore di una persona. (a) Campi `classe`, `origine`, `età` sulla traccia, copione o tasti, testo e riga fissa a schermo: 2, più 0,5 di prova. (b) Funzione di degradazione, matrici, ritardo, registro, bracci rifatti: 1,5. «Solo allarga» sulla tabella dei profili (se L-2 la consegna) e asserzione «avviso con etichette ⊇ avviso senza»: 1,5. **Minimo per la demo, solo (a): 2,5 ore. Tutto: 5,5 ore.**

## 8. Esiti delle previsioni e che cosa propongo dopo

`ml-P1` **regge** (9 su 9 presenti, 5 su 5 assenti). `ml-P2` **regge per YOLO, smentita in parte per RF-DETR**: i tre modelli più piccoli e i due più grandi sono sotto PML 1.0. `ml-P3`: la prima metà **regge** (LOCO); la seconda è **smentita** (l'Apron Dataset è uscito alla prima ricerca; a richiesta e non commerciale). `ml-P4` **regge** per l'esistenza; il contenuto di Ristic et al. non è letto. `ml-P5`: «solo allarga = 0» **regge**; «ingenua > 0 con ogni matrice con errori» è **smentita** nei 9 bracci con base 1,4 m/s (nessuna classe ipotizzata è più lenta): era scritta male. *Notato dopo:* con base 4,0 la regola ingenua restringe anche con la matrice identità. `ml-P6` **regge** (160–1 004 su 10 000 nei 18 bracci con errori).

**Dopo.** (1) L'arbitro decida la linea di base del sito: bassa con etichette che allargano, oppure pari alla classe più veloce ammessa. (2) Innestare `degrada()` nel banco vero e misurare M-2 sull'avviso, non sulla sola velocità. (3) Misurare una matrice vera su COCO val2017 con un rilevatore sotto Apache-2.0. (4) Chiedere allo statistico il numero di passaggi per M-1 per classe.
