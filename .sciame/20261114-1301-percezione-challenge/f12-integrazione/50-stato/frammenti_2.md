@@@ S4_1_NUOVE
#### 4.1.10 f7 — verdetto sulla mappa voxel e sulla traccia (17:27–17:43)

`f7-estensione/16-verdetto/VERDETTO_ESTENSIONE.md`. Tutto è simulazione o conto su camera ideale ferma. L'arbitro ha fatto 66 controlli su cifre del torneo, dell'attacco e della verifica, cercate nei file dei risultati: tornano tutti; restano sbagliate due cifre della decisione («438 → 0»: sul file 438 → 14). Ha rilanciato tre programmi altrui con uscite identiche: è lo stesso codice, copre solo la trascrizione. File giudicati: `f7-estensione/13-soluzione/DECISIONE.md`, `f7-estensione/14-attacco/CONTROPROVE_DECISIONE.md`, `f7-estensione/15-verifica/VERIFICA_DECISIONE.md`, `f7-estensione/11-torneo/TORNEO.md`. Cifre: §4.6, righe N29–N32; esito: §5.2.

#### 4.1.11 f8 — verdetto sulla continuità visiva (17:29–17:42)

`f8-continuita/16-verdetto/VERDETTO_CONTINUITA.md`. Simulazione o conto, a sensore fermo, soggetto puntiforme salvo le controprove. L'arbitro ha ricontato 29 gruppi di cifre sui file: tornano tutte; nessun simulatore rieseguito. File giudicati: `f8-continuita/13-soluzione/MODIFICHE_CONTINUITA.md`, `f8-continuita/14-attacco/CONTROPROVE_MODIFICHE.md`, `f8-continuita/15-statistica/ANALISI.md`, `f8-continuita/11-misure/BANCO_DI_PROVA.md`, `f8-continuita/12-torneo/TORNEO.md`. Un difetto di metodo trovato e chiuso: i semi contigui del generatore davano lo stesso flusso spostato di uno; gli intervalli erano stretti di 1,3–2,5 volte, le stime sono confermate a semi riparati (K-223). Cifre: §4.6, righe N33–N34; esito: §5.3.

#### 4.1.12 f10 — verdetto sui dati pubblici e sull'hardware simulato (17:43–17:52)

`f10-dati/23-verdetto/VERDETTO_DATI.md`; contributi: `f10-dati/10-catena/CATENA.md`, `f10-dati/11-simulatore/SIMULATORE.md`, `f10-dati/12-dati-veri/DATI_VERI.md`, `f10-dati/20-validazione/VALIDAZIONE_DATI.md`, `f10-dati/21-statistica/ANALISI_DATI.md`, la cartella `f10-dati/22-avversario/`. È il primo tentativo su profondità realistica: profondità **simulata dalle schede tecniche** di tre camere e tracce pubbliche di persone; nessun sensore della squadra. L'arbitro ha ricontato le cifre sui file con un programma suo (`f10-dati/23-verdetto/riconta_arbitro.py`): tornano tutte; due etichette non tornano, i conteggi sì («135 sequenze, filtri spenti» sono 131 più 4 con i filtri; i «45 al bordo in 1 sequenza» stanno in 2). Cifre: §4.6, righe N14, N21–N28; esito: §5.5.

#### 4.1.13 f12 — le prove del passo d'integrazione (17:47–18:33)

Tutte simulazione, un autore ciascuna; l'arbitro le ha ricontate sui file dei risultati in VI ([ric.]), senza rieseguire i simulatori: vede errori di somma e di denominatore, non un difetto dentro i programmi.

| Prova | File e ora | Che cosa prova | Indipendenza dichiarata |
|---|---|---|---|
| Prova d'insieme della continuità (controllo C-C) | `f12-integrazione/02-prova-insieme/PROVA_INSIEME.md`, 17:47–18:09 | M1–M8 con c1, c2, c3, c4, c5, c7 insieme, su semi nuovi, con l'estraneo e l'ombra stimata stretta; 75 lanci, 241 s | il codice è ricomposto, non riscritto: `insieme.c` è il codice dell'avversario di f8 con 33 sostituzioni; sensore ideale; previsioni non cieche; c6 e c8 non sono nell'insieme |
| «Libero» della cella (controllo C-D) | `f12-integrazione/03-libero/LIBERO_DELLA_CELLA.md`, 17:47–18:08 | V-017, V-018 e la regola `nuvole-1` sullo stesso banco: 10 scene, 300 condizioni, buchi sparsi e a chiazze | camera ideale ferma; regola scelta dopo il primo lancio; un autore |
| Identità su profondità simulata | `f12-integrazione/06-identita/IDENTITA_SU_PROFONDITA.md`, 17:53–18:18 | F-401, F-402, F-408, F-409 su una copia della catena di riferimento, a 424 e a 848 px, con l'estraneo | la correzione che passa («tracciamento-1») è scelta dopo aver visto i dati |
| Controprova dell'identità | `f12-integrazione/07-controprova-identita/CONTROPROVA_IDENTITA.md`, 18:18–18:33 | replica su semi mai usati e attacchi al dominio | le cifre dell'autore si rifanno identiche; stessa catena |

Le critiche dello stesso passo: l'attacco alla versione 3 (`f12-integrazione/10-attacco/ATTACCO_V3.md`, 18:09–18:21: controesempi alla regola del «libero» della prima stesura e alla posa «entro 1°»); la completezza (`f12-integrazione/11-completezza/COMPLETEZZA.md`: sulla prima stesura 149 voci, di cui 120 conformi, 12 escluse col motivo, 15 non conformi, 2 mancanti, e 13 incoerenze fra regole); il piano rifatto (`f12-integrazione/12-piano-rifatto/PIANO_RIFATTO.md`); il controllo statistico (`f12-integrazione/13-statistica/CONTROLLO_PROVE.md`: i conteggi delle due prove tornano tutti; cambiano tre diciture). Cifre: §4.6.

#### 4.1.14 f13 — i ricalcoli dei fascicoli dell'allegato tecnico (17:59–18:15)

Sei specialisti hanno rifatto da zero dimostrazioni, conti e riconteggi (cartelle `f13-allegato/01-dimostrazioni/` … `f13-allegato/06-bibliografia/`). Le discordanze fra i ricalcoli e i file sono in `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md`: §4.7 e §5.8. I simulatori altrui non sono stati rieseguiti: «ricontato» vuol dire somme e intervalli rifatti dalle righe grezze. Due regole violate per errore e dichiarate (un `git status` in sola lettura; un file di lavoro scritto nella cartella temporanea condivisa).

#### 4.1.15 f14 — la valutazione breve su classificazione e profili (18:31–18:55)

Contratto `f14-classificazione/CONTRATTO_CLASSIFICAZIONE.md` (domanda Q9, criteri L-1…L-6); tre proposte (`f14-classificazione/01-profili/PROFILI.md`, `f14-classificazione/02-uso/USO_DELLA_CLASSE.md`, `f14-classificazione/03-classificatore/CLASSIFICATORE.md`); un attacco (`f14-classificazione/10-attacco/ATTACCO_CLASSIFICAZIONE.md`); il blocco (`f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md`). Solo conti e simulazioni brevi: niente sensore, niente catena, nessun modello eseguito. Cifre: §4.6, riga N36; esito: §5.9.

#### 4.1.16 f12 — i riconteggi dell'arbitro nel verdetto d'integrazione (18:55–19:09)

`f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md`, con cinque programmi di riconteggio accanto (sola lettura di txt, json e jsonl; nessun codice altrui importato). Le otto previsioni dell'arbitro, scritte alle 18:56, reggono tutte: «ho trovato ciò che mi aspettavo: motivo di prudenza». **Lette e non ricontate:** 29 scoperti su 95 399, le cifre di K-215, il costo in millisecondi, le cifre dell'attacco e del blocco di classificazione, THÖR. Dal riconteggio vengono due cambi di stato nuovi, che nessun ruolo aveva visto (§5.6, cambi 9 e 10).

@@@ S4_3_NOTA
> **Versione 3.** La tabella qui sotto è lo stato delle contraddizioni **dopo il verdetto del nucleo**. Lo stato alla chiusura della convocazione, con le contraddizioni nate in f7, f8, f10 e f12, è nel §4.8; lo stato dei requisiti nel riquadro del §1.3.

@@@ S4_5_NOTA
> **Versione 3: che cosa è stato toccato nel frattempo, e che cosa resta.** *Toccato, in simulazione:* la maschera d'ombra e il «libero» da una profondità **simulata dalle schede** (f10; non da un sensore); i rilevamenti falsi e i pixel a mezz'aria ai bordi (F-401, F-403); le correzioni della continuità tutte insieme (c1–c5 e c7: prova d'insieme), ma non c6 e c8; l'occlusore più basso del sensore (K-102, K-110: il sistema perde chi è ancora in vista); pedoni veri solo come tracce di cattura del moto (THÖR). *Resta non toccato:* ogni sensore vero; la versione 3 eseguita come insieme; la continuità su profondità; il rilascio dell'avviso; le regole per settori, il registro e la misura sul posto; due persone, occlusore mobile, sensore in moto; ogni classe diversa da «persona a piedi»; il classificatore; qualunque prova con persone. *Metodo:* manca una rilettura indipendente della versione 3 finale e del blocco di classificazione; l'audit delle ipotesi nascoste non è rifatto sulla versione 3 (`f5/CHIUSURA.md`, §4). L'ultimo capoverso qui sotto («Estensioni in corso») è **superato da** §4.1.10–§4.1.16.

@@@ S4_6_7_8
### 4.6 Le cifre nuove della versione 3

Ogni riga porta il file, la numerosità e l'intervallo dove i file lo danno. Stati con le marche della legenda; [SIM] vale a sensore fermo; «scheda» = profondità simulata dalle schede tecniche (f10); «ideale» = camera o sensore ideale. [ric.] = ricontato dall'arbitro in VI. Il redattore non ha ricontato niente. Tre numeri con «/» = geometrie D / T / L.

| # | Cifra | Valore (N o intervallo) | Stato | File |
|---|---|---|---|---|
| N1 | Continuità: passaggi con un ciclo senza regione dopo l'ingresso in ombra | 0 su 23 402 nascosti; 6 000 camminatori distinti: meno di 6,4 su 10 000; 0 su 217 861 lanciati | [COSTR] più [SIM] ideale [f12][ric.] | `f12-integrazione/02-prova-insieme/ris/TABELLE.txt`; ST; VI §3 |
| N2 | Persona dentro la regione, ostacolo largo 2 m, bordo noto, sul percorso | Wilson sopra 0,90 fino a 2 s e sopra 0,85 a 3 s in 30 celle su 30; limiti peggiori 0,921 e 0,899; 608–2 359 casi per cella | [SIM] ideale [f12][ric.] | PI §2; ST §2 |
| N3 | Lo stesso, pannello da 1 m, corpo esteso | 942 su 1045 a 1 s, limite 0,882; 0,87 sulle cinque celle; oltre 1 s «ampio» nel 92 % degli istanti | [SMENT] la soglia 0,90 [ric.] | PI; ST |
| N4 | Passaggi scoperti (traccia chiusa prima dell'ombra) | 24 su 23 402 con c7; 928 senza (3,97 %) | [SIM] ideale [ric.]; «0 scoperti» [SMENT] | PI |
| N5 | Estraneo con c1: prende l'identità e l'avviso cade | 3 027 su 3 041 / 3 493 su 3 616 / 3 239 su 3 546 | controesempio certificato [ric.] | PI; VI cambio 2 |
| N6 | Riaggancio sul percorso (c1 e C6) | 10 711 su 10 757 / 9 228 su 9 240 / 6 772 su 6 967 | [SIM] ideale [ric.] | PI; VI §4 |
| N7 | Bordo dell'ombra stimato, non noto | 0,30–0,46 a 1 s senza c3; 0,74–0,80 col bordo riconosciuto 8 cicli su 10 | controesempio [f12] (letto) | PI; V3 §1.6 |
| N8 | Chi svolta o esce dal lato lontano | 0,57–0,86 a 2–3 s (in V8: 0,13–0,52 a 3 s; differenza non spiegata) | controesempio [f12] | PI; ST; VI §4 |
| N9 | H-501, celle libere sopra un ostacolo | 0 su 300 condizioni (9 000 fotogrammi), due lanci; limite superiore per condizione 1,3 %; attacco: 0 su 7 200, 0 su 900, 0 su 9 000 entro ±0,5° | [VER] sull'insieme dichiarato, [SIM] ideale [ric.] | `f12-integrazione/03-libero/banco.json`; AT P1 |
| N10 | Candidate del contratto per il «libero» | V-017: 301 fotogrammi su 9 000 con una violazione; V-018 a un pixel: 1 130 | controesempi [ric.] | LC; VI C-D |
| N11 | Posa sbagliata di 1° | 150 e 145 fotogrammi con una cella libera sopra un corpo; 10 cm a 2,55 m «libero» in 7 celle su 7 | controesempio [ric.]; F-404 | LC; AT P2; VD §3 |
| N12 | Distanza libera per settore (mediana) | 3,0 m col 5 % di buchi sparsi a errore 0; 2,4 m a +0,5° con rumore al limite; 2,2 m con chiazze al 5 % | [SIM] ideale [ric.]; soglia 2,7 m non tenuta dentro il dominio | LC; VI C-D |
| N13 | Resa del libero vero con `nuvole-1` | 86,8 % senza buchi e col 5 % sparso; 62,6 % col 30 % sparso; 78,3 % e 45,4 % con chiazze | [SIM] ideale [f12] (letto) | LC; V3 §1.2 |
| N14 | Identità al ritorno, parametri del nucleo | 0 passaggi su 90 [0–4,1 %]; con soglia 40: 41 su 45 [79,3–96,5 %], a una risoluzione | [SMENT] su scheda | VD §1, H-404 |
| N15 | Identità al ritorno con H-502 | 176 su 180 [94,4–99,1 %] a 424 px; 174 su 180 [92,9–98,5 %] a 848 px; criterio 28 su 30: 27 in un caso | [SIM] scheda, come tasso, dominio stretto [ric.] | CI; VI cambio 6 |
| N16 | Lo stesso, fuori dominio | 0, 2, 0 su 10 (oltre 2,6 m, bambino, rumore limite); 6 su 10 a +0,5°; 0 e 1 su 10 a 0,3 m dal pannello; estraneo 19 su 20 | controesempi [ric.] (0,3 m: letto) | CI; ID |
| N17 | F-409: centro nascosto «in ombra senza avviso» | 0 fotogrammi su 4 324 (424 px) e 0 su 4 325 (848 px), contro 180 e 271 di partenza; replica 0 su 3 608; 334 fotogrammi oltre 3 m | [SIM] scheda [ric.] | ID; CI; VI cambio 7 |
| N18 | Continuità su profondità: stato della traccia a persona nascosta | «previsto» 1 568 e «perso» 2 983 su 4 552 (424 px); 1 584 e 2 968 su 4 553 (848 px); 44 e 43 passaggi su 140 senza vuoti | fatto nuovo dell'arbitro [ric.] | VI cambio 9 |
| N19 | Rilascio dell'avviso tolto il pannello | acceso 2 s dopo in 10 prove su 10, anche nella catena di partenza; 117 celle, 95 «libero» per la mappa | controesempio; causa non diagnosticata | CI; VI cambio 10 |
| N20 | Avviso dietro un occlusore fermo | non si spegne in 140 passaggi su 140; 0 celle rilasciabili su 808 | costo dichiarato [f12] | ID; AT P7 |
| N21 | «Libero» nell'ombra vera, catena di f10 | 0 su 2 907 032 celle·fotogramma (3 149 352 con la definizione dell'arbitro); 3 forme d'ombra; per sequenza 0 su 131 (limite superiore 2,9 %). Su sequenze nuove: 5 su 3 992 186 | [SIM] scheda, posa esatta; le 5: [NR] | VD §1; CI; VI cambio 8 |
| N22 | Pannello fermo «in movimento» | 79 passaggi su 90 [79,4–93,0 %] coi gruppi del nucleo; 0 su 140 con H-502; fuori dominio 7 su 10 | [SMENT] la cifra 0,0–0,2 %; [SIM] scheda [ric.] | VD H-405; VI cambio 10 |
| N23 | Tracce fantasma sul pavimento vuoto | 28 in 2 s (D435i; D455: 0); 3 a +0,5° e 81 a −0,5°; 7–66 per passaggio | [SIM] scheda | VD F-403, K-406 |
| N24 | Errore del bordo d'ombra | +2,0 / +6,2 / +14,6 cm (minimo, mediana, massimo), 115 sequenze su 115; al limite 0 su 8, da −65 a +73 cm | [SIM] scheda al nominale; [SMENT] al limite | VD H-402 |
| N25 | Filtro su pedoni veri (THÖR, cattura del moto) | q = 0,2: 0,977 / 1,000 / 1,000 a 1 / 2 / 3 s, 219 tratti, 9 persone; secondo codice 0,982 / 0,995 / 1,000 | sostenuto dai dati (non una camera) | VD §1; DF stima D6 |
| N26 | Costo di calcolo | 6,35 ms di media su 9 152 cicli simulati, 4 oltre 66 ms; 81 ms su una registrazione vera con 254 tracce confermate in 21 s; 3,0 e 7,5 ms con gli interruttori | [SIM]; un filo di un portatile, non la scheda di bordo | VD H-406; V3 §7 |
| N27 | Centro nascosto, parametri del nucleo | 2 939 fotogrammi su 3 038 nell'avviso, 99 senza avviso, 0 «libero» | [SIM] scheda | VD |
| N28 | Regione a velocità costante sulla catena di f10 | 36 passaggi su 46 coi parametri di partenza; 83 su 90 nella variante a soglia 40 | [SIM] scheda; attribuzione corretta da DF | DF statistica 3 |
| N29 | Varianti voxel | lettura a due stati: 80 505 falsi «libero» su 146 901; decadimento: 830 fotogrammi su 897; sensore coperto: 71 006 punti «libero» per sempre | controesempio certificato [SIM] ideale | V7 §1 |
| N30 | Lettura del fotogramma corrente: punti profondi dati per liberi; resa | 0 in 147 + 87 + 87 fotogrammi e in 10 condizioni × 90 fotogrammi (208 000 punti); resa 97,1 % con conferma su tre fotogrammi, 61,1 % a un solo fotogramma | [SIM] ideale, due autori | V7 §1; DF costo 2 |
| N31 | «Libero» ricordato per 3 fotogrammi (invariante 1 del nucleo) | 1 186 punti del suolo sotto un corpo che non rimanda segnale; 58 fotogrammi su 90 | controesempio, due programmi | V7 §0 |
| N32 | Vetro | 654 punti della lastra su 800 dati per liberi a 2,0 m; 600 su 800 a 1,5 m | [SMENT], limite dichiarato | V7; DF costo 5 |
| N33 | Nucleo versione 2, previsione mostrata | regione nel 19 / 38 / 33 % dei cicli senza osservazione; un vuoto in 1 958 / 1 991 / 1 999 passaggi su 1 958 / 2 000 / 2 000 | imperativo non rispettato [SIM] | V8 §1 |
| N34 | sd-1, soggetto puntiforme | 45 celle su 45 sopra 0,90 fino a 2 s (peggiore 826 su 879, limite 0,922) | [SIM]; superata da N2 e N3 col corpo esteso | V8 §2; VI cambio 1 |
| N35 | Velocità coperta dalla fascia di 0,40 m | 1,13 m/s (0,40 m / 0,355 s); 0,56 m/s con 20 cm d'errore di bordo | [CONTO], latenza stimata | DF dimostrazioni D4; VI §3 |
| N36 | Classi e profili | avviso tempestivo fino a 1,44 m/s; 3 classi su 15 a velocità tipica, 0 a velocità massima; I15: 0 violazioni su 20 000, due volte; regola scartata 0,353 e 0,791 | [CONTO]; [SIM] sulla sola fascia (letto) | BL §6–§7 |
| N37 | Piano: minimo intero entro l'ora 14 | 0,428 [0,421; 0,435] (stime dell'autore, modello leggero); 0,039 [0,036; 0,042] (secondo ruolo, modello medio); 0,005 nel duro | [STIMA] simulata, non misura | `f12-integrazione/21-piano-finale/risultati_variante_c2.txt` |
| N38 | Piano: punti protetti nel programma all'ora 14 | 0,99 / 0,82 / 0,47 nei tre modelli | [STIMA] simulata | PIA §9 |
| N39 | Registro degli eventi | 0 violazioni su 600 scene; eventi mancati nel 16–52 % delle scene; scomparse spurie 12,5 % | logica controllata dal suo autore | V7 §2 |
| N40 | c7 su profondità coi parametri del nucleo | tracce finite entro 0,75 m da un'ombra: mediana 20 per sequenza di 3 s | controesempio [f12] | AT P11 |
| N41 | Scoperti con l'avviso davvero acceso | 29 passaggi su 95 399 con la maschera esatta; 2 / 15 / 1 704 / 1 979 su 2 000 con l'ombra stimata più stretta di 0,10 / 0,20 / 0,45 / 0,60 m | [SIM] ideale (letto, non ricontato) | V3 §1.7 |

### 4.7 Cifre corrette dai ricalcoli dei fascicoli (f13)

Regola usata: dove il fascicolo sa derivare la cifra e la derivazione è scritta, vale la cifra derivata; altrimenti si riportano entrambe con la condizione di ciascuna. Fonte unica: `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md`. Nessuna discordanza rovescia una conclusione.

| Dove, in questo documento | Com'era scritto | Che cosa dice il ricalcolo | Che cosa vale ora |
|---|---|---|---|
| sintesi della versione 2; §1.3, R3; §2.2, B5 | «400 su 400: limite inferiore 99,25 %» | è Clopper-Pearson unilaterale al 95 %; con Wilson al 95 % è 99,05 % | entrambe, col nome dell'intervallo; la cifra è comunque superata (N14) |
| §2.2, B3 | «2000 su 2000: limite inferiore 99,85 %» | limite unilaterale esatto; Wilson al 95 %: 99,81 % | entrambe, col nome |
| §2.2, B3 | soglia «mobile» 5·σ·√2 | il codice che ha dato 100 / 85,9 / 26,6 % usa 5·σ·√(2/m), m = 3; la forma letterale darebbe 0 % da 3 m | 5·σ·√(2/m), m = 3 |
| §2.3, invariante 1 del nucleo | «0,33 m, meno della fascia» | vero per la sola età; con la latenza 0,72 m a 2,5 m/s | già segnato smentito; resta |
| §2.2, B8; cap. 7 | la fascia copre «circa 1,4 m/s» (1,39) | conta solo età e latenza (0,288 s); con la tenuta, 0,355 s: 1,13 m/s; 0,56 con 20 cm d'errore di bordo. L'altro conto dei file, 1,85 m/s, con la latenza di 0,155 s dà 1,80 | 1,13 m/s (0,56), conto riconosciuto dall'arbitro |
| §4.2, riga 1 | Fisher: det/traccia² = 5·10⁻¹⁷ | è lo zero in virgola mobile; il valore esatto è 0 | «determinante esattamente 0» |
| §2.1; sintesi | «il filtro viene dopo l'associazione» | esatto solo per l'aggiornamento; la previsione precede l'associazione | forma corretta |
| §2.2, B1; §3.4 | geometria (suolo, testa, quota del disco, focale, Gemini) | sette righe | tabella del §3.10 |
| §2.2, B5 | «2 riagganci sbagliati su 1200» | nel file sono 2 su 2400 | 2 su 2400 nel file; 2 su 1200 nel verdetto del nucleo |
| §1.5; §4.2 | accelerazione: σ ≈ 66 m/s² a 30 Hz | giusta per uno scarto di posizione di 3 cm, che è un valore assunto; con 1,5 cm (curva nominale a 2 m) viene 33 m/s² | 66 m/s² «con 3 cm assunti» |
| §5.2 | octree «2,2–3,9 volte» su 18 configurazioni; «da 1,4 a 3,9» | le configurazioni sono 20; senza potatura 2,2–3,8, con potatura 2,3–3,9; tabella a blocchi 1,39–1,76 | le tre cifre distinte |
| §5.2; verdetti | rese 97,1 %, 79–88 %, 8 % della «lettura del solo fotogramma corrente» | sono della lettura con conferma su tre fotogrammi; a un fotogramma 61,1 %, 55,7–57,9 %, 3,6 % | entrambe, col nome della lettura |
| §4.6, N28 | «regione 83 su 90» | variante a soglia 40; coi parametri di partenza 36 su 46 | entrambe |
| §2.2, B5 | previsione in Python: 5,3 ms, 6,2 al 95° percentile | rilanciata su macchina carica: 15,9 ms al 95° percentile | entrambe: 6,2 nei file, 15,9 al rilancio |
| §4.6, N26 | «254 tracce» | sono le confermate in 21,3 s; presenti insieme: mediana 152, massimo 259 | precisato |
| §3.6 | soglie Q1–Q5 sul moto | interpolazione su griglie rade; un tasso scambiato per un angolo | §3.10 |
| §8.3, §8.4; §10.1, riquadro 6, j | distanza di separazione da norma, C = 0,85 m | le norme non sono state lette (la pagina di ISO 13855 non è raggiungibile) | **non citabile** |
| §5.3 | il cerchio «a 2 s contiene il soggetto nello 0,00–0,06» | è la copertura della regione emessa dalla regola «metà dell'ombra», sul comportamento «prosegue»; chi si ferma, nel cerchio non spento, è coperto 0,86–0,94 | frase nel senso dei file |
| §4.6, N25 | THÖR | due codici: 0,977 / 1,000 / 1,000 e 0,982 / 0,995 / 1,000 | entrambe |

Il fascicolo di bibliografia cambia lo stato di alcune fonti (da «verificata in parte» a «verificata per il dato indicato»: fra le altre `thor` e `tum-rgbd`, di cui trova la licenza CC BY 4.0) e segnala che i file di esempio RealSense sono fatti con hardware di pre-produzione: l'elenco dei riferimenti lo recepisce in un documento separato (`f12-integrazione/51-riferimenti/RIFERIMENTI.md`, in scrittura alle 19:20, non letto).

### 4.8 Contraddizioni e ipotesi alla chiusura

Fonte: VI, §4; `f5/CHIUSURA.md`, §2. «Chiusa» vuol dire chiusa **in simulazione**.

| Gruppo | K# | Stato alla chiusura | Prova che decide |
|---|---|---|---|
| Chiuse in simulazione | K-218, K-220 (sul banco ideale); K-222, K-223, K-213; K-401, K-402, K-405; K-018; K-501 (vale «previsto / previsto ampio»); K-502 (vale «suolo visto libero da 1,3 m a d m»); K-201, K-206, K-203…K-205, K-208, K-210…K-212 (V8); K-102, K-103, K-104, K-105 (V7) | chiuse | — |
| Decise dall'arbitro | K-508 (nelle 14 ore la fascia resta 0,40 m, con la riga fissa che dice che cosa copre); K-509 («drone», «UAV», «in volo» restano vietate come capacità; classi e portatori si nominano solo come «profilo configurato, non provato») | decise | — |
| Aperte su regole adottate: conclusione riformulata nel dominio | **K-505** (rilascio dell'avviso) | adottata la sola metà di sicurezza | diagnosi sul seme 301, poi il blocco `rotto` di `f12-integrazione/07-controprova-identita/attacco.py` |
| | **K-219, K-016** (identità ed estraneo) | identità «presunta», un soggetto per ombra; l'avviso non ne dipende | braccio «estraneo» di `f12-integrazione/02-prova-insieme/insieme.c` con lo strato che resta: 0 rilasci |
| | **K-504** (c2 «la pendente più recente» contro «con più pendenti: ambigua») | c2 con identità presunta | sessione di 120 passaggi sulla catena di ID |
| | **K-506, K-514** (c2 e c7 contro i fantasmi; la prova d'ingresso del rumore, com'è scritta, non può passare coi gruppi del nucleo) | la prova si esegue nella configurazione che si vuole accendere | pavimento vuoto e pannello fermo, 30 s, sulle sequenze di f10 |
| | **K-403** (3 pixel nella mappa contro soglie per l'identità) | soglie solo sui gruppi; tasso, non criterio | 90 passaggi per cella; poi il sensore |
| | **K-215, K-404** (precisione contro ombra stimata) | il livello si dichiara solo «col bordo noto» | quota dei cicli col bordo riconosciuto, sul sensore |
| | **K-014, K-107** («libero» nell'ombra vera; impronta contro fotogramma vero) | la conclusione è H-501 su camera ideale | H-501 sulle sequenze di f10; pannello sul suolo segnato, 150 fotogrammi |
| | **K-015** (velocità coperta) | 1,13 m/s dichiarati | latenza al 95° percentile |
| | **K-017** (C6 obbligata contro il suo costo; non nominata nella versione 3) | C6 resta | caso fuori dalla geometria del catalogo |
| | **K-109** (dopo una copertura le regioni si dilatano sul non visto libero) | conto, non riprovato | coperture di 1 e 2 s sulla catena |
| | **K-515** (i testi della versione 3, del piano e dello schermo contro il blocco di classificazione) | vale il blocco; i tre testi vanno fusi | ricerca testuale di «classific» nei tre file |
| All'utente | **K-503** (chi toglie l'avviso residuo), **K-507** («fondamentale» contro «fuori dalle 14 ore»), **K-111** (larghezza del pannello) | decisioni | cap. 7 |
| Aperte, senza effetto sulle conclusioni adottate | K-003 (q resta 0,2), K-004, K-007, K-101, K-106, K-108 (decide il minuto 60), K-110, K-202, K-214, K-216, K-217, K-221, K-301…K-308, K-406, K-407, K-510…K-513 | aperte | VI, §4 |

**Ipotesi** (VI, §4). H-012, riformulata nella versione 3: provata **solo in simulazione, a sensore fermo**, clausola per clausola (continuità; precisione dichiarata; sicurezza), nel senso del contratto d'integrazione; nel senso più stretto dei verdetti precedenti (correttezza verificata sul dominio d'uso) **nessuna ipotesi è provata** (`f5/CHIUSURA.md`, §1). H-501: da testare sul vero. H-502: da testare, dietro interruttore. H-503: adottata, da testare il rilascio. H-504 (avviso che scade col tempo): aperta, contro la priorità 2: decide l'utente. H-505: adottata come specifica, da testare I15 sulla catena. Soglia proporzionale per cella (F-401 e F-412 come proposte): smentita.

**Previsioni risolte e non risolte:** `f5/CHIUSURA.md`, §3. Non risolte, con la prova: continuità su profondità; causa dei 24 scoperti; rilascio dell'avviso; errore del bordo d'ombra e «libero» nell'ombra vera sul sensore; rumore del centro con la distanza; latenza; chi svolta (0,57–0,70 contro 0,13–0,52); la regola delle etichette sulla catena; quale lettura del piano vale.

---

@@@ S5_TESTA
## 5. Le valutazioni chiuse dopo il nucleo: f7–f10, l'integrazione f12, f13 e f14

> **Versione 3.** Il titolo era «Valutazioni in corso: le estensioni f7–f10». **Tutte le valutazioni sono chiuse.** Ciò che segue resta simulazione, conto o lettura di schede, a sensore fermo: «chiuso» non vuol dire «validato».

### 5.0 Gli esiti in una tabella

| Valutazione | Domanda | Verdetto dell'arbitro | Esito in una riga | Qui |
|---|---|---|---|---|
| f7, mappa voxel e traccia | Q1, Q2 | V7, `f7-estensione/16-verdetto/VERDETTO_ESTENSIONE.md`, 17:43 | **no** alla mappa voxel nelle 14 + 4 ore e alle tre fasce; «libero» letto nel solo fotogramma; correzioni a–h; struttura a tre assi; registro degli eventi | §5.2 |
| f8, continuità visiva | Q3, Q4 | V8, `f8-continuita/16-verdetto/VERDETTO_CONTINUITA.md`, 17:42 | il nucleo versione 2 **non rispetta** l'imperativo; le modifiche M1–M8 con c1–c8 lo fanno rispettare in simulazione dentro un dominio dichiarato | §5.3 |
| f9, preproposta esterna | Q5 | V9, `f9-preproposta/13-verdetto/VERDETTO_PREPROPOSTA.md`, 16:37 | strategie approvate in forma corretta o respinte; piano a 14 ore simulato (già nella versione 2) | §5.4 |
| f10, dati pubblici e hardware simulato | Q6 | VD, `f10-dati/23-verdetto/VERDETTO_DATI.md`, 17:52 | nessuna ipotesi validata sul sensore; due cifre del nucleo cadono, una si corregge, due reggono in un dominio più stretto; tredici difetti | §5.5 |
| f12, integrazione | Q7 | VI, `f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md`, 19:09; chiusura `f5/CHIUSURA.md` | versione 3 adottabile come progetto di prototipo, non come sistema validato; esito della convocazione: chiuso | §5.6 |
| f13, allegato tecnico | nono addendum | nessun verdetto: fascicoli e discordanze | i ricalcoli correggono cifre e diciture, nessuna conclusione rovesciata | §5.8; §4.7 |
| f14, classificazione e profili | Q9 | giudicata dentro VI (H-505, K-507…K-513, K-515) | requisito incluso come specifica; classificatore richiesto, non realizzato, non valutato | §5.9 |

**Fotografia delle 16:13 (versione 2), superata dalla tabella qui sopra per lo stato.**

@@@ S5_1_NOTA
> **Versione 3.** La tabella qui sotto dice che cosa era consegnato alle 16:13: la colonna «Ancora vuoto» è **superata**; tutte le caselle sono state riempite e giudicate (§5.0).

@@@ S5_2_ESITO
> **Versione 3 — esito: verdetto V7** (`f7-estensione/16-verdetto/VERDETTO_ESTENSIONE.md`). Il testo sotto il riquadro è la fotografia preliminare della versione 2: dove differisce, vale il riquadro.
> - **Q1, la mappa voxel: la decisione NO regge**, per le 14 e per le 4 ore. «A sensore fermo una mappa non sa più della storia dei fotogrammi» è una deduzione, non una dimostrazione scritta. Stato: evidenza sperimentale in simulazione. Tre dei sei benefici attesi li dà la lettura del fotogramma corrente; le varianti voxel che ricordano o deducono un «libero» cadono ciascuna in almeno una prova di sicurezza (§4.6, N29). Le strutture sparse risparmiano al più 1,54 MB e costano 1,39–1,76 volte il tempo. Con il sensore in moto la domanda resta aperta (non attaccata).
> - **S10, tre fasce di quota: NO** come sostituto e come passaggio automatico. La premessa è un errore di lettura (1,09 m è una distanza, non un'altezza); 32 celle «libere» sopra una scatola di 10 cm che il nucleo vede; resa 30,6 %, e 0,0 % col 5 % di buchi sparsi. Ne resta il principio «libero solo fin dove si è letto».
> - **Cambi di stato.** «Cella libera = `stato(centro)`»: controesempio in simulazione. «Quota verificata fino a 1,2 + 0,25·d»: da «dimostrato» a smentita. **Invariante 1 del nucleo («libero» ricordato per 3 fotogrammi): controesempio in simulazione, due programmi** (§4.6, N31): «nessun "libero" falso in dodici attacchi» non vale più come frase generale. «Con 5 persone entra»: questione aperta (K-108).
> - **Le correzioni obbligate a–h**, tutte riprese nella versione 3: (a) il «libero» della cella → `nuvole-1` (B2); (b) «suolo visto libero fino a d», una quota solo se letta (B7); (c) con il sensore non in salute le tracce continuano in previsione (B8); (d) la traccia che sparisce nel vuoto vicino (B5); (e) controllo dell'inclinazione nella salute (B8); (f) casse fuori dalla linea dell'attore, e dichiarare l'ostacolo più basso di 1,65 m (B9); (g) la prova della copertura regge per la lettura del fotogramma, non per la griglia; (h) «provato» si legga «sostenuto dai dati, simulazione, un autore».
> - **Q2, la traccia della challenge: regge la struttura a tre assi** (applicazione, portatore del sensore, uscita), verificata come mappa, senza misure; «un giurato esterno capisce» è non verificato. «Monitoraggio di attività» lo copre solo il registro degli eventi (B10). S11: riformulare; «sosta in ombra» è smentita come nome di evento.
> - **Demo:** pannello alto almeno 1,7 m (poi 1,8 m con VD), a 1,7–1,9 m dal sensore; largo 1 m nasconde l'attore per 0,54–0,90 s a 1,0–1,4 m/s: poco per mostrare la continuità (K-111, decisione dell'utente).
> - **Contraddizioni:** K-102 decisa (il cuneo nasconde chi si vede dietro un ostacolo basso), K-103 e K-104 risolte, K-105 decisa (mai «via libera»), K-106 decisa in simulazione e aperta sul vero; nuove K-107…K-111 (§4.8). Le candidate V-002, V-003, V-012 della fotografia non entrano come tali: al loro posto la lettura del fotogramma e `nuvole-1`; V-016, V-017, V-019, T-008 nelle 4 ore, se un secondo autore le conferma.

@@@ S5_3_ESITO
> **Versione 3 — esito: verdetto V8** (`f8-continuita/16-verdetto/VERDETTO_CONTINUITA.md`). Il testo sotto il riquadro è la fotografia preliminare: dove differisce, vale il riquadro.
> - **Q3: il nucleo versione 2 non rispetta l'imperativo.** La previsione mostrata esce nel 19 / 38 / 33 % dei cicli senza osservazione; c'è un vuoto in quasi tutti i passaggi (§4.6, N33); in demo «previsto» dura 0,67 s. La precisione dichiarata col cerchio del filtro non regge. L'ingresso nell'ombra del nucleo lascia il soggetto nascosto senza traccia pendente in 87 passaggi su 2 800 (499 su 600 con l'ombra stimata a −20 cm): è sicurezza. Restano rispettati l'avviso e gli invarianti 1–5 e 7 del nucleo.
> - **Q4: le modifiche M1–M8 lo fanno rispettare in simulazione, a sensore fermo, con la maschera d'ombra esatta, dentro un dominio dichiarato**; fuori ci sono controesempi certificati. Dominio: sensore e ostacolo fermi, un soggetto per ombra visto almeno 4 fotogrammi, ingresso fra 0,3 e 1,8 m/s, sul percorso, rumore misurato, libreria dei percorsi dello stesso tipo di camminatore. Adottabile come progetto di prototipo, con le correzioni c1–c8.
> - **Cambi di stato sul verdetto del nucleo.** §5.5 di VN («la previsione vale circa mezzo secondo; la continuità la porta l'avviso»): **sostituita**. §5.4 di VN («stessa identità al ritorno, 100 %»): non regge con C6 in due codici (K-218). C-EST, la soluzione a due ipotesi della preproposta: smentita com'è scritta. «Con 4 persone ci sta»: smentita.
> - **Il predittore scelto.** sd-0 (ripiego, per primo) e sd-1 (principale) dietro la stessa interfaccia. sd-1 occupa 0,06–0,36 dell'ombra con un ostacolo largo, fino a 3 s; nella demo, con il pannello da 1 m, localizza per circa 1 s e poi dice «è ancora dietro». Nessuna candidata tiene il livello 50 %: un solo livello, detto «almeno». Nessuna cifra oltre 3 s (K-214).
> - **Dove cede** (§2.1 del verdetto): chi svolta o esce dal lato lontano; ombra stimata più stretta di 10–20 cm col corpo esteso; chi parte da fermo; camminatori meno regolari della libreria (0,944 / 0,835 / 0,801); rumore non rimisurato.
> - **Che cosa ha aggiunto il passo d'integrazione** (prova d'insieme; VI): la continuità regge anche con le correzioni insieme (§4.6, N1); la cifra «9 su 10 fino a 2 s» regge con l'ostacolo da 2 m ed è smentita col pannello da 1 m e il corpo esteso (N2, N3); c7 è sostenuta (N4); c1 contro l'estraneo è un controesempio certificato (N5).
> - **Le domande all'utente della fotografia.** Livelli e soglia del «previsto ampio» (K-202): un solo livello; soglia 80 % e orizzonte 3 s, scelti dopo i dati, aperta nel numero. Se il punto può spegnersi quando l'area resta (K-203): in «ampio» nessun punto e nessuna croce (c8). «Solo schermo o anche suono»: nessun verdetto lo decide; resta all'utente.

@@@ S5_4_ESITO
> **Versione 3 — che cosa i verdetti successivi hanno deciso sui «pareri» di V9.** Per S2–S5, S10 e S11 l'arbitro di f9 dava un parere, in attesa di f8 e di f7. Ora: **S3 e S4 (due ipotesi con pesi) non entrano**; di S5 entrano il contorno pieno solo con una misura, l'inviluppo tratteggiato ritagliato e l'età, non «conf Z %» né la regione che sparisce; S2 entra riscritta, nel raffinamento, solo sull'uscita (V8, §5; K-210). **S10: no** (V7, §1). **S11: riformulare** come registro degli eventi (V7, §2). Due punti di «che cosa entra nella soluzione integrata», nel testo qui sotto, sono **superati**: il punto (3), previsione «in tre gradi», da «previsto / previsto ampio» più l'evento «non ricomparso da n s» (K-501: vale V8); il punto (5), dicitura «nessun ostacolo osservato fino a d metri», da «suolo visto libero da 1,3 m a d m» (K-502: vale V7). «Per fare posto cade per prima l'etichetta della rete»: superato dal decimo addendum (cap. 7, decisione 1). Il piano a 14 ore di V9, §1 bis («il minimo chiude entro l'ora 14»): **non provato e tolto come obiettivo** (VI, cambio 12; §6.3).

@@@ S5_5_ESITO
> **Versione 3 — esito: verdetto VD** (`f10-dati/23-verdetto/VERDETTO_DATI.md`). **Nessuna delle sei ipotesi è validata sul sensore della squadra, che non esiste ancora.** Il «da sciogliere 4» qui sotto è sciolto: 162 sequenze simulate (9 152 fotogrammi) e 8 sequenze vere (3 510 fotogrammi) sono state elaborate dalla catena di riferimento.
>
> | H# | Prima (verdetto del nucleo) | Dopo (VD, §1) |
> |---|---|---|
> | H-401, «libero» da una profondità | argomento per costruzione; K-014 non decidibile | **confermata su profondità simulata da scheda, solo a posa esatta e con ostacoli che restituiscono profondità**; su registrazioni vere non decidibile |
> | H-402, errore del bordo d'ombra | ±20 cm assunti | confermata su simulata al nominale (+2,0…+14,6 cm); **smentita al limite**; sul vero non decidibile |
> | H-403, rumore del centro con la distanza | curva nominale; K-007 aperta | **non decidibile** |
> | H-404, previsione durante l'occlusione | identità 100 %; q = 0,2 | (a) identità: **smentita com'è** (0 su 90), corretta con una soglia più alta scelta dopo i dati (41 su 45); (b) q **corretto** verso 0,05–0,1 sui pedoni veri; (c) su profondità vera non decidibile |
> | H-405, mobili e ostacoli | «mobile» 100 % a 2 m; muro mobile 0,0–0,2 % | ostacoli fermi: confermata su simulata; falsi «in movimento»: **smentita** (79 su 90) |
> | H-406, costo per ciclo | questione aperta | confermata su simulata (6,35 ms); **smentita su una registrazione vera affollata** (81 ms) |
>
> - **Tredici difetti, ingressi obbligati per la soluzione integrata** (F-401…F-413), e dove stanno nella versione 3: F-401 (la persona si fonde col pannello) e F-412 (soglie di punti assolute) → gruppi per picco dietro interruttore, mai la soglia per cella (B3); F-402 (il riaggancio accetta gruppi tagliati e l'occlusore) → interruttore del riaggancio (B5); F-403 (fantasmi del pavimento) → prova d'ingresso del rumore (B1); F-404 (posa sbagliata) → prova d'ingresso della posa (B1); F-405 (ostacolo che non restituisce profondità) e F-410 (ostacolo sospeso) → limiti dichiarati (B2); F-406 (filtri del costruttore) → condizione 3; F-407 («libero» per memoria su una cella che era occupata) → nessuna memoria (B2); F-408 (filtro fermo dopo un riaggancio tagliato) → ripartenza dalla misura (B4); F-409 (lo strato si spegne al riaggancio) → l'avviso resta (B5); F-411 (regione che non informa) → q resta 0,2, regione di f8 (B4, B5); F-413 (il vuoto vicino è una striscia) → B1 e §3.10.
> - **Contraddizioni nuove** K-401…K-407 (§4.8) e le nove condizioni riviste (§2.4).
> - **Per la giuria** (VD, §5): sei affermazioni; due sono state riscritte dal verdetto d'integrazione: «0 su 2,9 milioni» vale «sulle sequenze di partenza» (su sequenze nuove 5 celle·fotogramma, non risolto), e «si recupera correggendo una soglia (41 su 45)» è superata dal tasso di 176 su 180 nel dominio stretto (VI, cambi 6 e 8). Le frasi da non dire: §8.10.
> - **La «prossima prova senza sensore»** chiesta da VD è stata eseguita in f12 (prova e controprova sull'identità: §4.1.13).
> - **Decisioni dell'utente poste da VD:** telefono con profondità e inventario; ammettere `http://` per il solo archivio di Friburgo; che cosa promettere sull'identità (cap. 7).

@@@ S5_6_7_8_9
### 5.6 Il passo d'integrazione f12 e la chiusura

Contratto: `f12-integrazione/CONTRATTO_INTEGRAZIONE.md` (domanda Q7, cinque priorità, sette controlli C-A…C-G). Verdetto: `f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md` (VI). Chiusura: `f5/CHIUSURA.md`. **Verdetto in una frase:** la versione 3 è adottabile come progetto di prototipo, non come sistema validato; in simulazione rispetta la continuità visiva e conserva la sicurezza delle indicazioni dentro un dominio che dichiara; è una specifica composta, mai eseguita come insieme, e sulla sola catena che gira su profondità la continuità non c'è ancora.

**I sette controlli** (VI, §1).

| Controllo | Esito | Perché |
|---|---|---|
| C-A, completezza | **regge in parte** | sulla prima stesura 149 voci: 120 conformi, 12 escluse col motivo, 15 non conformi, 2 mancanti; la finale dichiara applicate le correzioni e ne lascia 11 col motivo, ma **nessun ruolo diverso dall'autore l'ha ricontrollata**. F-401…F-413 e K-401…K-407 stanno tutti nella versione 3 o nella sua tabella. Restano: K-017 non nominata; il decimo addendum con 0 occorrenze di «classific» nella versione 3, nella tabella, nel piano e nello schermo (sta solo nel blocco) |
| C-B, coerenza | **regge in parte** | le 13 incoerenze risultano corrette per lettura; restano K-514, K-515 e K-017 |
| C-C, continuità insieme | **regge in parte** | 0 vuoti su 23 402 (regge); scoperti 24 (cade la soglia 0); regione: T e L 15 celle su 15 ciascuna, D cade; ombra stretta: cade senza c3; estraneo: cade con c1. Indipendenza parziale |
| C-D, «libero» della cella | **regge in parte** | le due candidate del contratto cadono; regge H-501 (0 su 9 000, due volte); la mediana scende a 2,4 e a 2,2 m dentro il dominio |
| C-E, piano | **regge in parte** | piano per persona e per ora, con la simulazione dell'autore e il rifacimento del secondo ruolo; mancano i compiti della classificazione e la correzione del rilascio; è scritto prima della controprova |
| C-F, chiusura | **regge, con riformulazioni** | `f5/CHIUSURA.md` |
| C-G, documento | **non regge oggi** | alla data del verdetto il testo di due pagine era la versione 0.8 delle 17:54, che precede la versione 3 finale, la controprova e il blocco; nessun lettore senza contesto l'ha letto. Dopo il verdetto è comparsa una nuova stesura (`f12-integrazione/40-documento/TESTO_DUE_PAGINE.md`, 19:19): **qui ne è letta solo l'intestazione; non è vagliata dall'arbitro** |

**I dodici cambi di stato di VI**, per esteso.

1. V8, §6, «almeno 9 su 10 fino a 2 s»: da «sostenuta in 45 celle su 45» a **regge con l'ostacolo largo 2 m, smentita con il pannello da 1 m e il corpo esteso**.
2. K-219 (c1 contro l'estraneo): da «aperta» a **controesempio certificato**; conseguenza: l'avviso non dipende più dall'identità.
3. c7: da «non provata» a **sostenuta dai dati in simulazione**; «0 scoperti» smentito.
4. K-107 («libero» della cella): da «aperta» a **decisa in simulazione, aperta sul vero**.
5. Condizione 4 del nucleo (posa): da «meno di 1°» a **meno di 0,5° più la prova d'ingresso**.
6. Identità al ritorno: resta **smentita coi parametri del nucleo**; con H-502 **sostenuta come tasso in un dominio stretto**; criterio di VD non superato.
7. F-409 (l'avviso resta dopo il riaggancio): da «non provata» a **sostenuta dai dati in simulazione**.
8. «0 su 2,9 milioni» di VD: vale per le sequenze di f10; su sequenze nuove 5 celle·fotogramma: **non risolto**.
9. **Nuovo:** su profondità simulata da scheda la continuità **non è mai stata eseguita** («perso» in 2 983 fotogrammi su 4 552).
10. **Nuovo:** il difetto «tolto il pannello l'avviso resta acceso» c'è anche nella catena di partenza; «il pannello non è mai in movimento» vale solo nel dominio.
11. VN, §5.6, «la rete mette solo l'etichetta»: **superata** dal decimo addendum; classificatore richiesto, non realizzato, non valutato.
12. V9, §1 bis, «il minimo chiude entro l'ora 14»: **non provato e tolto come obiettivo** (0,04–0,43).

**La chiusura** (`f5/CHIUSURA.md`). Le tre condizioni della pipeline: (1) almeno una ipotesi provata: sì, H-012 riformulata e H-501, **solo in simulazione, a sensore fermo**; (2) nessuna contraddizione aperta su una conclusione adottata: sì, **dopo sei riformulazioni** (continuità: vale sul banco a sensore ideale; «l'avviso finisce solo guardando»: adottata la sola metà di sicurezza; identità: «presunta, un soggetto per ombra»; precisione: «col bordo noto»; «libero» nell'ombra vera: H-501 su camera ideale; velocità coperta: 1,13 m/s); (3) ogni previsione risolta o dichiarata non risolta: sì. **Esito: chiuso.** Chiusa è la domanda di progetto, non una domanda sul sensore: chi chiede «provata sul dominio d'uso» deve leggere la chiusura come «non chiuso». Delle quattro verifiche dei risultati fondanti **manca** una rilettura indipendente della versione 3 finale e del blocco di classificazione, e l'audit non è rifatto sulla versione 3.

**Regole violate dichiarate dall'arbitro:** la lunghezza del verdetto (sei pagine contro cinque); V7, V8 e V9 non riletti per intero; un `git --version` lanciato per errore.

> **Testo della versione 2, superato:** «Alla data [il passo d'integrazione] non ha cartella né contratto». Le dipendenze che elencava (S3 e S4 dal banco di f8; S10 e S11 da f7; il predittore di f8 innestato in f10; le ore sulle 14 + 4) sono risolte, salvo una: **il predittore di f8 non è innestato nella catena di f10** (cambio 9).

### 5.7 Che cosa cambia qui alla prossima valutazione

I cinque punti della versione 2 («che cosa cambia qui alla chiusura di ogni estensione»: f7, f8, f9, f10, integrazione) sono **superati**: fatti in questa versione (righe 3 (a)–(i) del registro delle modifiche), salvo due cose che non esistono ancora: le «ore vere» del piano (tutte le ore restano stime), e la correzione della portata dichiarata (resta «3 m, scelta, da misurare», con «suolo visto libero» fino a 2,6 m al più). Le prossime valutazioni attese, e i paragrafi che toccano:

- **Innesto di regione e «previsto ampio» nella catena su profondità** (soglia: 0 cicli senza regione): riga 4 della sintesi; §2.2, B5 (1.6); §4.6, N18; condizione 10.
- **Diagnosi e correzione del rilascio dell'avviso** (K-505): §2.2, B5 (1.7); invariante I7; cap. 7, decisione 2.
- **Braccio «estraneo» con l'avviso che resta** (0 rilasci): §4.8, K-219.
- **H-501 sulle sequenze di f10 e un secondo autore:** §2.2, B2; §4.8, K-014 e K-107.
- **Prova differenziale di I15 sulla catena:** §2.2, B6; §5.9.
- **Fusione del blocco di classificazione nei testi della versione 3, del piano e dello schermo** (K-515), e nuova lettura del documento di due pagine (C-G).
- **Inventario dei sensori e prima ora con un sensore** (le tre misure): cap. 3; riga 1 della sintesi; tutte le righe [NV-HW].
- **Minuto 60 dell'hackathon:** sceglie la lettura del piano (§6.3).
- **Decisioni dell'utente** (cap. 7): ognuna cambia la sintesi e il paragrafo indicato.
- **Elenco dei riferimenti:** le fonti nuove dell'appendice B e le correzioni del riquadro 6 del §10.1.

### 5.8 f13 — le discordanze dei fascicoli dell'allegato tecnico

Il nono addendum chiede un allegato tecnico per una commissione esterna. Sei specialisti hanno rifatto conti e riconteggi (dimostrazioni, geometria, stima, statistica, costo, bibliografia); le discordanze sono raccolte in `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md` e sono ingressi della versione 3 e del verdetto d'integrazione. **Nessuna rovescia una conclusione.** Le cifre corrette sono nel §4.7 e nel §3.10. Gli enunciati che reggono solo in forma più debole:

- **«La previsione non tocca l'avviso»**: falsa alla lettera; vale la monotonia (la previsione accende l'avviso e non lo restringe), e l'area d'avviso realizzata, nel nucleo, si chiudeva anche per riaggancio: è lì che entrava l'ipotesi «un solo soggetto per ombra».
- **«Ciò che non è visto non è mai libero»** e **«ciò che è dichiarato libero è libero»** sono due enunciati: il secondo vale solo sui raggi verso il suolo e solo all'acquisizione.
- **«La regione non sta su suolo visto libero oltre la fascia»**: nel codice è ottenuta con un peso; lo «0 cicli» è misurato, non garantito dalla sola regola.
- **La dimostrazione di «ciò che non è valutato non è libero»** per la lettura del fotogramma è scritta dall'autore del fascicolo di costo a partire dal verdetto di f7: «va riletta da un secondo ruolo».
- **Conti nuovi dei fascicoli**, non presenti nei file dello sciame e da vagliare: la velocità coperta con i tre termini (1,13 m/s, riconosciuta dall'arbitro); la regione esatta del campo (20,5 %); un 95° percentile della latenza «a voci costanti» (170 ms: citato nel fascicolo di geometria, non letto qui).

I capitoli e l'unione dell'allegato (`f13-allegato/11-capitolo/` … `f13-allegato/20-unione/`) sono in corso e non sono letti qui.

### 5.9 f14 — classificazione su più classi e profilo di chi porta il sensore

**Il requisito** (decimo addendum, `ADDENDUM_UTENTE.md`): dato, non si ridiscute; si giudica come è incluso. Contratto: `f14-classificazione/CONTRATTO_CLASSIFICAZIONE.md` (domanda Q9, criteri L-1…L-6).

**L'attacco** (`f14-classificazione/10-attacco/ATTACCO_CLASSIFICAZIONE.md`). «L'etichetta non restringe mai l'avviso» è **smentita in due proposte su tre** e in un punto della terza: regge solo nella forma «massimo che non torna indietro, con pavimento = inviluppo del sito». «Limite del dominio 2,25 m/s»: smentito per conto, manca il tempo di conferma; i documenti davano tre cifre per la stessa grandezza (2,25; 2,11 o 1,76; 1,44 m/s). Le otto correzioni obbligate dell'attacco sono applicate nel blocco.

**Il blocco** (`f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md`): è **parte della soluzione versione 3**. Contenuto: §2.2, B6 (blocco nuovo 1.13); modifiche ai blocchi esistenti (riquadri di B1, B4, B5, B7, B10, B11); invarianti I15–I20 (§2.3); tabella del dominio per classe e profili del portatore (§8.10); frasi per i documenti e frasi da non dire (§8.10); compiti CL1–CL4 (§6.3).

**Stati** (VI, §2, cambio 11, condizione 16). Classificatore: **richiesto, non realizzato, non valutato**. La regola di sicurezza sulle etichette (I15): per costruzione, provata sulla sola fascia, **questione aperta sulla catena**. Dominio «tempestivo fino a 1,44 m/s»: per conto. Ogni classe diversa da «persona a piedi» e il sensore in moto: **non provato**. H-505: adottata come specifica.

**Aperte** (K-507…K-513; VI, §4): «fondamentale» contro «nelle 14 ore la classe non entra in fascia, filtro e previsione» (K-507: decide l'utente); fascia a un solo valore contro fascia di scenario (K-508: decisa, resta 0,40 m nelle 14 ore); le parole (K-509: decisa); tempo di reazione di una persona non vedente, senza fonte (K-510); il margine del conto (K-511: lo decide la latenza misurata); treno e aereo non etichettabili (K-512); lo scenario dichiarato male (K-513). In più K-515: il blocco non è fuso nei testi della versione 3, del piano e dello schermo.

@@@ S6_TESTA
> **Versione 3.** **Il piano che vale è nel §6.3** (`f12-integrazione/21-piano-finale/PIANO_14_4.md`). I §6.1 e §6.2 restano come storia e come registro: il bilancio per blocchi, la tabella delle tappe a 24 ore e il ricalcolo dell'arbitro di f9 sono **superati come calendario** dal §6.3; la frase dell'arbitro di f9 «il minimo chiude entro l'ora 14» è tolta come obiettivo (VI, cambio 12). Tutte le ore restano stime mai misurate.

@@@ S6_2_V3

> **Versione 3: che cosa cambia nel registro dei rischi.** Riga 1 (filtri della camera): confermato in simulazione, col sensore coperto e i filtri accesi restano 989–995 celle «libero» per altri 3 fotogrammi (F-406). Riga 2 (fascia e latenza): da «margine zero a 1,4 m/s» a «copre 1,13 m/s, dichiarati» (K-015). Riga 6 (ciclo): misurati 6,35 ms di media in numpy su scene simulate e 81 ms su una registrazione vera affollata (VD); in C la griglia polare costa 0,03–0,6 ms e la matrice densa 45–67 ms con tutti i raggi, 102 ms in Python puro (V7, §1); la scheda di bordo non è misurata. Riga 7 (pannello): da «≥ 1,5 × 1 m» a «alto 1,8 m» (VD; VI, condizione 14). Riga 8 (secondo soggetto): l'identità passa all'estraneo ma **l'avviso resta** (H-503). Riga 9 (rilevamenti mancati vicino all'ombra): c7 dietro la prova d'ingresso; scoperti 24 su 23 402 con c7, 3,97 % senza. Riga 10 (continuità costruita tardi): sd-0 per primo; regione nel programma al gelo dell'ora 12 con probabilità 0,97 / 0,71 nelle due letture. Riga 11 (estensioni che chiudono tardi): superata, tutte chiuse. Riga 13 (dati pubblici): il simulatore è ottimistico sui buchi (K-407). Riga 14 (parole): elenco delle frasi da non dire nel §8.10. Rischi nuovi:
>
> | # | Rischio | Cifra e fonte | Contromisura |
> |--|---|---|---|
> | 15 | La continuità non regge sulla catena su profondità | «perso» in 2 983 fotogrammi su 4 552 (VI, cambio 9) | innesto di regione e «previsto ampio», poi il conteggio: 0 cicli senza regione, prima della demo |
> | 16 | L'avviso residuo non si spegne tolto l'ostacolo | 10 prove su 10 (K-505) | diagnosi e correzione fra le prime prove; altrimenti dichiarare «si toglie riavviando» |
> | 17 | Posa sbagliata: un ostacolo basso esce «libero» | 7 celle su 7 a +1° (F-404) | prova d'ingresso della posa prima di ogni fotogramma vero; tolleranza sotto 0,5° |
> | 18 | La correzione dell'identità cade fuori dal suo dominio | 0–6 passaggi su 10 fuori dominio (CI) | interruttore spento di norma; schermo «identità in correzione»; l'avviso non dipende dall'identità |
> | 19 | c7 accende avvisi che niente spegne | mediana 20 per sequenza di 3 s coi parametri del nucleo (AT, P11) | c7 solo dopo la prova d'ingresso del rumore |
> | 20 | I testi che la squadra legge non contengono la classificazione | 0 occorrenze di «classific» nella versione 3, nel piano, nello schermo (K-515) | fusione dei testi prima dell'ora 0; riga fissa «nessun modello di classificazione in esecuzione» |
> | 21 | I compiti della classificazione mangiano il minimo | 2,5 ore date a chi fa lo schermo portano il minimo da 0,428 a 0,195 (BL, §10) | compiti dopo i punti protetti; decisione 1 dell'utente |
> | 22 | La catena di riferimento contraddice la versione 3 | 8 righe (V3, §6) | correggerle prima di riusarla; i due banchi a ogni fusione |
> | 23 | Una persona manca | con 4 persone il minimo scende a 0,09 / 0,004 (PIA, §7) | tagli dall'ora 0 |

@@@ S6_3
### 6.3 Il piano finale a 14 + 4 ore (versione 3)

Fonte: `f12-integrazione/21-piano-finale/PIANO_14_4.md` (18:23–18:32), con il rifacimento del secondo ruolo (`f12-integrazione/12-piano-rifatto/PIANO_RIFATTO.md`) e il giudizio di VI, §6. **Tutte le durate sono stime, non misure; il calendario è stato ridisegnato due volte dopo aver visto i numeri (dichiarato).**

**Che cosa si promette: una scala con gelo all'ora 12, non «il minimo chiuso entro l'ora 14».** Ordine d'ingresso nel programma comune (il «tronco»): ① «libero» dal solo fotogramma → ② avviso che non cade per sola identità → ③ regione disegnata per tutta l'occlusione → ④ identità corretta → ⑤ stati senza vuoti → ⑥ sensore non in salute. **Protetti, mai tagliati:** ①–④, lo scheletro di punta a punta, il tabellone base. Ciò che non è entrato resta dietro il suo interruttore, spento, e lo schermo lo nomina.

**La «valutazione preliminare» chiusa all'ora 14** (PIA, §1): (1) il tabellone sul programma gelato, con sensore simulato e verità esatta, una riga per passaggio, semi non usati per tarare: righe di sicurezza (celle «libero» con un ostacolo sotto; nascosti fuori dall'avviso; avvisi caduti senza aver guardato: soglia 0) e righe di continuità (passaggi con un vuoto; persona dentro la regione a 1, 2, 3 s come «k su n»); (2) una riga su persone vere (tracce THÖR); (3) se mancano le righe della regione, la tabella della prova d'insieme, dichiarata «banco di progetto, non il prototipo»; (4) se arriva un sensore, le tre misure del §3.10; (5) la demo in riproduzione dichiarata e il video di ripiego.

**Chi fa che cosa** (profili ipotizzati; nessuna persona della squadra è stata sentita). P1 mappa e sicurezza («libero», avviso che resta, salute del sensore); P2 previsione (sd-0 dietro l'interfaccia, stati e chiusure); P3 schermo e documento (lettore, scheletro, regione tratteggiata, diciture); P4 misura (simulatore, inventario, tabellone); P5 tronco, identità, sensori (banco di regressione, correzione sui gruppi, ingresso in ombra, controllo all'avvio). Il calendario ora per ora e la prima ora minuto per minuto sono in PIA, §3 e §8.

| Quando | Punto di controllo | Se no |
|---|---|---|
| **minuto 60** | minuto in cui la quinta macchina ha le 25 prove verdi e una sequenza che scorre: **è la misura che sceglie la lettura** | entro 60 minuti vale la lettura dell'autore; fra 60 e 90 quella del secondo ruolo; oltre 90 si taglia subito |
| ora 5 | banco di regressione chiuso, inventario spedito, «libero» avviato | nessuna modifica entra senza il banco |
| ora 5–6 | ramo del sensore deciso (tabella del §3.10) | — |
| ora 8 | scheletro di punta a punta | chi fa l'identità lo chiude con chi fa lo schermo |
| ora 9 | primo tabellone base | — |
| ora 10 | la regione esce a ogni ciclo | chi fa il tronco affianca chi fa la previsione; taglio 10 (stati e ingresso in ombra dietro interruttore); le righe della regione restano sul predittore che la catena ha già |
| **ora 12** | **gelo:** entra solo ciò che passa il banco | ciò che manca sta spento e nominato |
| 13:15–14:00 | prova generale registrata, a tempo chiuso | la demo si fa con ciò che c'è, dichiarato |
| ora 16 | gelo finale | ciò che non è nel programma esce dalla demo e va in «limiti» |
| 17:15, ora 18 | seconda prova generale; consegna | — |

**Ordine dei tagli** (PIA, §5): 1 etichetta «persona» (non si comincia); 2 zone; 3 profilo sonoro (resta un suono); 4 sd-1; 5 registro; 6 tabella delle regole estesa; 7 sequenze pubbliche descrittive; 8 latenza ridotta a una riga del tabellone; 9 diciture ridotte; 10 stati e ingresso in ombra dietro interruttore; 11 controllo all'avvio solo in riproduzione (mai con fotogrammi di un sensore vero). **Il taglio 1 è superato dal decimo addendum:** vale il blocco di classificazione (K-515).

**Probabilità, fra due letture delle stesse stime** (20 000 estrazioni; cifre lette nei file del piano, programma non rieseguito né dall'arbitro né qui).

| Stime, modello | Minimo intero entro l'ora 14 | entro l'ora 16 | Punti protetti nel programma alle ore 12 / 14 / 16 |
|---|---|---|---|
| dell'autore, leggero | **0,428** [0,421; 0,435] | 0,71 | 0,96 / **0,99** / 1,00 |
| dell'autore, medio | 0,108 | 0,31 | 0,85 / 0,95 / 0,99 |
| dell'autore, duro | 0,016 | 0,06 | 0,54 / 0,73 / 0,86 |
| del secondo ruolo, leggero | 0,214 | 0,48 | 0,84 / 0,95 / 0,99 |
| del secondo ruolo, medio | **0,039** [0,036; 0,042] | 0,15 | 0,59 / **0,82** / 0,93 |
| del secondo ruolo, duro | 0,005 | 0,03 | 0,26 / 0,47 / 0,66 |

Nessuna media: la lettura la sceglie il minuto 60. Nella lettura prudente il minimo intero chiude oltre l'ora 18 (mediana 19,6): all'ora 18 si consegna la scala. Decide la coda (prima corsa di tutto insieme e tabellone), non un compito di sviluppo. Con 4 persone: 0,09 / 0,004. Preparare l'ambiente prima dell'ora 0 vale +0,03…+0,08 sul minimo e +0,16 sui punti protetti al gelo nella lettura prudente; se il regolamento lo ammetta è **non verificato**.

**Se arriva un sensore** (ora 5–6). Camera di profondità densa: registra e spedisce, niente flusso dal vivo; prima di ogni fotogramma il controllo all'avvio; poi le tre misure; 30 passaggi non permettono «9 su 10» (30 su 30 dà un limite di 0,886); allestimento con pannello alto 1,8 m e largo 2 m, persona a 0,5 m dal pannello. Solo altro (telefono con LiDAR, webcam): dati o video di verità, non demo. Niente: il piano non cambia.

**Le riserve dell'arbitro** (VI, §6; C-E). (1) Il piano **non ha i compiti della classificazione**. Il blocco li definisce: CL1, scenario e portatore nella configurazione, dichiarazioni d'avvio e riga fissa (1,0 ora stimata, nelle 14 ore, a chi fa la misura); CL2, campi dell'etichetta sulla traccia, copione o tasti, testo sotto la traccia, registro (1,5 ore, nelle 4 ore); CL3, errori iniettati e prova differenziale di I15 (1,5 ore, dopo); CL4, fascia di scenario e librerie per classe (dopo l'hackathon). (2) Non ha la correzione del rilascio dell'avviso (K-505). (3) È scritto prima della controprova sull'identità: il punto protetto ④ poggia su una correzione che fuori dominio cade; se i due cancelli non passano, resta spento e dichiarato.

**Stati** (PIA, §11). «Minimo entro l'ora 14»: non provato (0,04–0,43, stime). «Punti protetti nel programma all'ora 14»: sostenuto solo da una simulazione di stime (0,82–0,99), con il calendario scelto dopo. «Con 4 persone non ci sta»: sostenuto. K-108 resta aperta: la decide il minuto 60.

---

@@@ S7_V3
> **Versione 3: le decisioni aperte alla chiusura.** Le prime tre vengono dal verdetto d'integrazione (VI, §9; `f5/CHIUSURA.md`, §6), con la raccomandazione dell'arbitro.
>
> | # | Decisione | Opzioni | Raccomandazione dell'arbitro · stato |
> |--|---|---|---|
> | I | **La classificazione nelle 18 ore** (K-507) | (a) dichiarata sulla riga fissa e nei documenti, più scenario e portatore nella configurazione nelle 14 ore (CL1) e le etichette a mano nelle 4 ore (CL2): prezzo di CL1 non stimato, nessuno sui punti protetti; (b) CL1 e CL2 dentro le 14 ore: il minimo scende da 0,43 a 0,20–0,26 nella lettura favorevole; (c) nessun codice, solo la dichiarazione: il requisito «etichette a mano nelle prove» non è mostrato | **(a)** · aperta |
> | II | **Chi toglie l'avviso residuo** (K-503, K-505, H-504) | (a) solo lo sguardo: dietro un ostacolo fermo resta acceso e, finché il rilascio non è corretto, si toglie riavviando; (b) l'avviso scade dopo T secondi: schermo più pulito, ma una persona ferma oltre T esce senza avviso, contro la priorità 2; (c) lo azzera l'operatore: stessa obiezione | **(a)**, con la correzione del rilascio fra le prime prove · aperta. Con (b) la clausola di sicurezza dell'ipotesi chiusa andrebbe riscritta |
> | III | **Che cosa si promette e che cosa si prepara** | (a) la scala col gelo all'ora 12, l'identità «presunta, in correzione», l'ambiente pronto sulle cinque macchine prima dell'ora 0 (se il regolamento lo ammette: non verificato) e subito la domanda su telefono con profondità, sensore e pannello di 1,8 × 2 m; (b) promettere il minimo chiuso all'ora 14: probabilità 0,04–0,43 | **(a)** · aperta |
> | IV | **Telefono e inventario** (VD, §6) | chiedere ora ai cinque se c'è un iPhone Pro o un iPad Pro (profondità vera subito), e dire se il sensore di casa può arrivare in sala | senza, la demo è una riproduzione dichiarata · aperta |
> | V | **Dati con occlusioni lunghe** (VD, §6) | ammettere `http://` per il solo archivio di Friburgo (2,81 GB), che lo scaricamento a regola ha rifiutato | aperta; quanti tratti nascosti lunghi contenga: non verificato |
> | VI | **Larghezza del pannello della demo** (K-111; V7; V8) | 1 m (previsione localizzata per circa 1 s, poi «è ancora dietro»; nessuna cifra oltre 1 s) oppure circa 2 m (la zona stretta si vede per 2–3 s; 0,45 s di vista per lato a 1,0 m/s) | la versione 3 scrive 1 m per la demo; il piano chiede 2 m se arriva un sensore · aperta |
>
> **Che ne è delle undici decisioni della tabella qui sotto.**
>
> | # | Da … a … | Chi lo decide |
> |--|---|---|
> | 1 | resta **aperta**; si aggiungono la tabella di decisione per l'inventario (§3.10) e la domanda sul telefono (IV) | VD |
> | 2 | resta **aperta**: nessun file letto dice da quando contano le 14 ore; il piano conta in «ora 0 … ora 18» | — |
> | 3 | da «sensore fermo; moto e ausilio indossato non verificati» a **dicitura unica** della condizione 1 (§2.4) | VD; VI |
> | 4 | da «circa 1,4 m/s o fascia più larga» a **fascia 0,40 m con 1,13 m/s dichiarati** nelle 14 ore (K-508, decisa dall'arbitro); la latenza misurata rifà la fascia | VI |
> | 5 | da «etichetta, sensori laterali, mappe memorizzate» all'**ordine dei tagli** del §6.3; il taglio dell'etichetta è superato dal decimo addendum → decisione I | PIA; VI |
> | 6 | livelli: da «ipotesi 50 e 90 %» a **un solo livello dichiarato**, «almeno 9 su 10» fino a 2 s e «almeno 85 su 100» fino a 3 s, solo nel dominio; nessun livello 50 %; soglia dell'«ampio» 80 % e 3 s (K-202, aperta nel numero). Sicurezza come vincolo: confermata (priorità 2 del contratto d'integrazione). «Solo schermo o anche suono»: **aperta**. Demo con ombra più larga → decisione VI | V8; VI |
> | 7 | resta **aperta**; l'ambito si dice con la struttura a tre assi (§8.10) | V7 |
> | 8 | restano **aperte** montaggio, linguaggio, macchina; 360°: no | — |
> | 9 | resta **non verificato**; si aggiunge: se si può preparare l'ambiente prima dell'ora 0 (III) | VI |
> | 10 | da «non scritto» a **definita nel piano** (§6.3, «valutazione preliminare»); che cosa si promette → decisione III | PIA; VI |
> | 11 | da «aperta» a **l'operatore ferma solo la ripetizione del suono**; le celle le toglie lo sguardo (K-503); resta all'utente come decisione II | V3 §1.7; VI |

@@@ S8_10
### 8.10 Aggiornamento alla versione 3: tre assi, profili, classi, frasi

**La struttura a tre assi** (V7, §2; verificata come mappa, senza misure): **applicazione** (monitoraggio di attività e oggetti; avviso di presenza), **portatore del sensore** (supporto fisso; veicolo senza equipaggio **fermo** alla stessa quota), **uscita** (schermo e registro; segnali sonori). La traccia della challenge non nomina veicoli: ogni frase che nomina il veicolo contiene «fermo» o «non provato».

**I due profili d'uso** (V3, §3). **A:** monitoraggio di un varco o di un'area di lavoro; uscita su schermo e registro; il messaggio per settori verso un autopilota è progetto, mai generato; da dire: «al chiuso, fino a 3 m, camera a 1,2 m: a un'altra quota i numeri cambiano». **B:** avviso di presenza per una persona non vedente **ferma** (non «orientamento»); segnali sonori di 0,3 s, frase a stato stabile; alla perdita di affidabilità la persona si ferma e torna al bastone; da dire: «per chi cammina non è provato niente»; non è un dispositivo medico (se vi rientri: non verificato). In nessuno dei due profili qualcosa è provato oltre il nucleo comune; quattro regole su nove del nucleo sono identiche nei due profili. Le correzioni C1–C8 dell'attacco alla specializzazione (§8.5) entrano nella versione 3; **restano non provate esse stesse** (V7, §4).

**La frase della prova** (V3, §3). «Al calcolatore, a camera ferma, con una persona alla volta e un ostacolo fermo largo 2 metri che la nasconde per intero, lo schermo ha mostrato a ogni fotogramma una zona dove poteva essere; finché restava nascosta e sul proprio percorso, la persona era dentro in almeno 9 casi su 10 fino a 2 secondi e in almeno 85 su 100 fino a 3, con il bordo dell'ombra noto esattamente. Con il pannello da 1 metro della demo: circa 9 su 10 a 1 secondo (limite 0,87), poi lo schermo dice "è dietro l'ostacolo" senza un livello. Provato su profondità simulata dalle schede tecniche e su tracce pubbliche di persone; mai su un sensore nostro. Dove cede lo diciamo prima.» Le sedici affermazioni convergenti per il documento di due pagine, ciascuna con stato e file, sono in VI, §7.

**Classi e dominio** (BL, §2 e §6; valori di `f14-classificazione/01-profili/classi.json`). Camera ferma, portata 3 m, stazione fissa con tempo di reazione di 1,0 s (ipotesi), avvicinamento frontale: **l'avviso è tempestivo, per conto, fino a 1,44 m/s**; oltre 7,1 m/s i 3 m si percorrono in meno del tempo di conferma più la latenza (0,42 s) e l'avviso uscirebbe dopo il contatto.

| Classe | Velocità tipica / massima (m/s) | Dentro i 3 m? | Portata che servirebbe (m) |
|---|---|---|---|
| persona a piedi | 1,4 / 2,5 | **sì a passo normale** (6 cm di margine); no a passo svelto | 4,5 |
| veicolo a guida automatica | 1,0 / 2,0 | sì a velocità tipica (mai simulato); no alla massima | 3,8 |
| aereo al traino | 1,4 / 4,2 | a velocità tipica per conto; non etichettabile dal sensore | 7 |
| trattore di piazzale | 1,7 / 8,3 | no | 3,4–13 |
| carrello elevatore | 2,2 / 4,5 | no | 4–7,5 |
| persona di corsa; auto in area di lavoro | 3,0 / 8,0; 2,8 / 8,3 | no; alla massima dopo il contatto | 13 |
| bicicletta; monopattino; treno in manovra | 4,3 / 8,3; 4,2 / 5,6; 4,2 / 8,3 | no | 9–13 |
| tram a una fermata | 5,6 / 13,9 | no | 9–21 |
| auto, strada urbana | 8,3 / 13,9 | no: dopo il contatto già a velocità tipica | 13–21 |
| aereo in rullaggio | 9,0 / 15,4 | no: dopo il contatto | 14–23 |
| treno in arrivo in banchina | 11,0 / 16,7 | no: dopo il contatto | 17–25 |
| multirotore in volo lento | 3,0 / 19,0 | no; la mappa del suolo non lo rappresenta | 5–28, e un altro sensore |

Solo 9 velocità su 30 hanno una fonte aperta da chi ha scritto la tabella; accelerazioni e frenate sono quasi tutte ipotesi; le fonti sono di terza mano e le norme primarie non sono lette (elenco «fonti nuove da registrare», appendice B). Una camera di profondità da 3 m non è il sensore delle classi veloci (BL, §6).

**Profili di chi porta il sensore** (BL, §3; esempi, per conto). Velocità coperta a sensore fermo, a 3 m: veicolo terrestre senza equipaggio con arresto automatico 2,84 m/s (reazione 0,3 s, ipotesi); lo stesso con operatore remoto 0,92; persona non vedente 1,07 m/s, **sotto il passo normale** (reazione 1,5 s: ipotesi, nessuna fonte); stazione fissa con persona vicina 1,44. **Ogni cifra con il sensore in moto è un conto fuori dal dominio provato.**

**Frasi per i documenti** (BL, §9). «Il sistema prevede un classificatore su più classi (persone, veicoli di tipo diverso, altri ostacoli in movimento), ciascuna con velocità, accelerazione e gradi di libertà, e un profilo fisso di chi porta il sensore. Qui nessun modello è in esecuzione: le etichette le mettiamo a mano. La classe può solo allargare un avviso e dare forma alla regione prevista; "libero" e la chiusura di un avviso non la leggono.»

**Da non dire** (elenchi completi: V3, §3; SCH, §6; BL, §9; VI, §7; VD, §5; V7, §6; V8, §7). In breve: «validato», «via libera», «garantito», «conforme a», «tarato»; «bassa latenza», «15 Hz» come prestazione; «perso»; «sosta», «è uscito»; «prevede dove sarà»; «9 su 10» senza «ostacolo largo, bordo noto, sul percorso», o col pannello da 1 m; «continuità provata» senza «al calcolatore, su sensore ideale»; «l'avviso si spegne quando rivede il suolo» (non provato); «0 su 2,9 milioni» senza «sulle sequenze di partenza»; «identità mantenuta al 100 %», «il criterio sull'identità è superato»; «mai libero dove c'è un ostacolo» senza «a posa nota e se l'ostacolo risponde»; «mappa 3D», «voxel», «360°»; «massa e accelerazione stimate»; «riconosce», «classifica», «gestisce veicoli, treni, aerei»; una percentuale di fiducia; «drone», «UAV», «in volo» come capacità (si nominano solo come «profilo configurato, non provato»: K-509); «orientamento» per chi cammina; «dispositivo medico»; una distanza di separazione da una norma (le norme non sono state lette); «chiuso» letto come «validato».

**Norme (§8.4).** Resta «ispirato a», mai «conforme a». ISO 13855 e il margine C = 0,85 m restano **non citabili** (DF; §10.3). Il blocco di classificazione usa nel suo conto un margine di 0,95 m, «il margine del conto già consegnato nel fascicolo di geometria»: è un parametro del conto, non una cifra di norma (K-511).

---

@@@ S9_2_RIGHE
| 17:27–17:43 | **verdetti dell'arbitro su f8 (17:42) e su f7 (17:43)**: il nucleo non rispetta la continuità, le modifiche sì in simulazione; no alla mappa voxel | `f8-continuita/16-verdetto/VERDETTO_CONTINUITA.md`; `f7-estensione/16-verdetto/VERDETTO_ESTENSIONE.md` |
| 17:43–17:52 | **verdetto dell'arbitro su f10**: identità al ritorno smentita su profondità realistica; F-401…F-413. PDF v0.7 (dopo i tre verdetti) e v0.8 (dopo il verdetto sui dati; 17:54 secondo VI): `proposta/VERSIONI.md`, radice | `f10-dati/23-verdetto/VERDETTO_DATI.md` |
| 17:47–18:22 | f12, prima fase: prima stesura della versione 3, prova d'insieme, «libero» della cella, piano e schermo; poi attacco, completezza, piano rifatto, controllo statistico; prova sull'identità (18:18) | `f12-integrazione/01-soluzione/` … `f12-integrazione/13-statistica/` |
| 17:59–18:15 | f13: sei fascicoli dell'allegato tecnico e le loro discordanze (nono addendum) | `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md` |
| 18:23–18:40 | f12, fase di correzione: **soluzione versione 3 finale** (18:38), piano finale (18:32), schermo e demo finali (18:40); controprova sull'identità (18:33) | `f12-integrazione/20-finale/SOLUZIONE_V3.md`; `f12-integrazione/21-piano-finale/PIANO_14_4.md`; `f12-integrazione/22-schermo-finale/SCHERMO_E_DEMO.md` |
| 18:31–18:55 | decimo addendum; f14: tre proposte, attacco, **blocco di classificazione** (18:55) | `f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md` |
| 18:55–19:09 | **verdetto d'integrazione e chiusura della convocazione**: «Esito: chiuso» | `f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md`; `f5/CHIUSURA.md` |
| 19:19–{HM} | nuova stesura del testo di due pagine (19:19, non vagliata); versione 3 di questo documento | `f12-integrazione/40-documento/TESTO_DUE_PAGINE.md`; `f12-integrazione/50-stato/STATO_PROGETTO.md` |
@@@ S10_3
### 10.3 Stato dei punti dopo le valutazioni chiuse

**I sei riquadri del §10.1.**

| Riquadro | Stato alla versione 3 | Chi lo decide |
|---|---|---|
| 1, C1–C11 o C1–C12 | **aperto**: nessun verdetto letto fissa la numerazione; la versione 3 cita le correzioni del nucleo per nome | — |
| 2, meccanismo di K-014 | **sciolto in parte**: su profondità simulata il «libero» falso con dati validi non compare a posa esatta; i filtri accesi tengono vivo il «libero» (F-406): sono due anelli diversi, tutti e due con una cifra. Sul sensore resta aperto | VD, §2 |
| 3, pannello della demo | **sciolto come progetto**: alto 1,8 m, largo 1 m, a 1,8 m dal sensore, attore a 2,3 m. Resta la larghezza (K-111) e resta da correggere il PDF, se scrive ancora 1,5 m (non verificato: il PDF non è letto qui) | VD; V7; VI, condizione 14 |
| 4, dati pubblici di f10 | **sciolto**: 8 sequenze vere e 3 510 fotogrammi elaborati; nessuna prova sul «libero» o sull'identità con dati veri | VD |
| 5, f6 e le «prove nuove» | **sciolto in parte**: V7, §4, dice che cosa della specializzazione entra e che cosa resta non provato; f6 non ha un verdetto suo; i suoi conti sul moto sono corretti dal fascicolo di geometria (§3.10) | V7; DF |
| 6, correzioni dell'elenco dei riferimenti | (b) latenza: **confermata** da DF, geometria 8; (j) ISO 13855 e C = 0,85 m: **confermata**, non citabile; (o) le ipotesi senza fonte restano tali, e si aggiunge il tempo di reazione di una persona non vedente (K-510). Le altre, (c)–(i), (k)–(n): **nessun verdetto letto le decide**; restano segnate in riga | DF; V3, §3 |

**I punti non applicati di `f11-documentazione/finale/CORREZIONI_APPLICATE.md`, §2.** Punto 8 (integrare i file di f7, f8 e f10): **fatto in questa versione**, dai verdetti. Punto 6 (correzioni b–o dell'elenco): due confermate, come sopra. Punto 7 (cambi di stato formali): quelli toccati dai verdetti sono scritti nei riquadri «Versione 3»; gli altri restano proposte. Punti 1–5 e 9–12 (file fuori cartella, seconda marca nel §4.2, controllo automatico, ordine del §9.2, numero dei commit, frasi fra «» del cap. 8, orari degli addendum, PDF): **non toccati**, per gli stessi motivi di allora.

**Discordanze nuove fra file, non sciolte.** (1) Chi svolta: 0,57–0,70 nella prova d'insieme contro 0,13–0,52 in V8; lo decide lo stesso lancio col corpo puntiforme. (2) Le 5 celle·fotogramma «libero» nell'ombra vera su sequenze nuove: catena o bordo della maschera di verità. (3) Larghezza del pannello: 1 m nella versione 3, 2 m nel piano per il ramo del sensore. (4) Il taglio 1 del piano («etichetta persona») contro il blocco di classificazione (K-515). (5) Il copione dello schermo dice «9 su 10 fino a 2 secondi» senza le condizioni (VI, C-G). (6) Due focali nei file (§3.10).

---

@@@ GLOSSARIO_RIGHE
| **estraneo** | un secondo soggetto mai visto che esce dalla stessa ombra (K-016, K-219) |
| **fascia di guardia (w)** | 0,40 m attorno al cuneo; copre 1,13 m/s (§2.2, B5). La **fascia di ritaglio**, 0,20 m, sta dentro w e riguarda solo la regione R90 |
| **gelo** | l'ora dopo la quale nel programma comune entra solo ciò che passa il banco di regressione (ora 12; gelo finale all'ora 16) (§6.3) |
| **interruttore** | opzione del programma, spenta di norma, dietro cui sta una regola non ancora provata abbastanza; la riga fissa dello schermo nomina quelle spente |
| **maschera** | il «non visto libero»: tutto ciò che nel fotogramma non è «libero» |
| **`nuvole-1` (H-501)** | la regola del «libero» della cella dal solo fotogramma: metà dell'impronta della cella e delle 8 vicine legge il suolo (§2.2, B2) |
| **occlusione virtuale** | prova in cui una copia della catena riceve le misure con un cuneo cancellato a programma, mentre la persona resta visibile e fa da verità (§2.2, B11) |
| **passaggio scoperto** | passaggio in cui la traccia è chiusa prima dell'ombra e l'avviso non nasce |
| **possibile presenza fresca / residua** | l'avviso con una traccia in previsione / l'avviso rimasto dopo un riaggancio, senza traccia (§2.2, B5) |
| **previsto ampio** | lo stato in cui il sistema dice «non so dove, ma è dietro l'ostacolo o fuori area»: tutta la maschera del cuneo, tratteggiata, senza punto; sostituisce «perso» |
| **profondità simulata da scheda** | immagini di profondità generate dal simulatore di f10 con i parametri delle schede tecniche di tre camere; non è un sensore |
| **R90, R100** | la regione prevista al livello dichiarato; l'area d'avviso (cuneo più w). Sempre R90 ⊆ R100 |
| **scenario** | l'insieme delle classi ammesse nel sito, dichiarato all'avvio: fissa l'ampiezza dell'avviso (§2.2, B6) |
| **sd-0, sd-1** | i due predittori: il ripiego (disco a velocità costante, senza cifre) e il principale (percorsi registrati, con il livello) |
| **tabellone** | la tabella delle misure a schermo, una riga per passaggio, «k su n» con l'intervallo (§2.2, B11) |
| **tronco; scala; piolo** | il programma comune in cui entrano le regole; l'ordine d'ingresso; ciascuna delle sei regole in ordine (§6.3) |
| **versione 3** | la soluzione dopo i cinque verdetti e il passo d'integrazione, con il blocco di classificazione (cap. 2) |
@@@ REGISTRO_RIGHE
| 3 (a) | 14 novembre 2026, {HM} | verdetto dell'arbitro su f8, continuità visiva (`f8-continuita/16-verdetto/VERDETTO_CONTINUITA.md`, 17:42) | continuità: da «il nucleo non la rispetta [prel.]» a «il nucleo versione 2 non la rispetta; le modifiche M1–M8 con c1–c8 la fanno rispettare in simulazione nel dominio dichiarato»; «perso» → «previsto ampio»; «la continuità la porta l'avviso» → sostituita; identità «100 %» → non regge con C6 (K-218); §5.3, §2.2 B5, §2.3 (I10) |
| 3 (b) | idem | verdetto dell'arbitro su f7, mappa voxel e traccia (`f7-estensione/16-verdetto/VERDETTO_ESTENSIONE.md`, 17:43) | mappa voxel e tre fasce: da «in valutazione» a «no»; «libero» da «uno degli ultimi 3 fotogrammi» a «solo fotogramma corrente» (invariante 1 del nucleo: controesempio); pannello da «almeno 1,5 m» a «almeno 1,7 m»; tre assi; registro degli eventi (B10); §5.2, §2.2 B2, B7, B8 |
| 3 (c) | idem | verdetto dell'arbitro su f10, dati pubblici e hardware simulato (`f10-dati/23-verdetto/VERDETTO_DATI.md`, 17:52) | identità al ritorno: da «100 %, almeno 99,25 %» a «smentita su profondità realistica (0 su 90)»; muro «mobile»: da «0,0–0,2 %» a «smentita (79 su 90)»; q: da «risolta a 0,2» a «corretto verso 0,05–0,1» (resta 0,2); K-014: da «non decidibile» a «sostenuta in simulazione a posa esatta»; pannello 1,8 m; posa nota; F-401…F-413; K-401…K-407; §5.5, §2.2, §2.4, §3.10 |
| 3 (d) | idem | prove di f12: prova d'insieme, «libero» della cella, identità e controprova (17:47–18:33) | cifre nuove N1–N20 (§4.6); c7 da «non provata» a «sostenuta»; K-219 da «aperta» a «controesempio certificato»; K-107 da «aperta» a «decisa in simulazione»; «9 su 10 fino a 2 s»: regge con l'ostacolo da 2 m, smentita col pannello da 1 m; identità con H-502: tasso in un dominio stretto |
| 3 (e) | idem | critiche di f12: attacco, completezza, piano rifatto, controllo statistico (18:09–18:23) | posa da «meno di 1°» a «meno di 0,5°»; «1,7 su 10 000» → «meno di 6,4 su 10 000»; `nuvole-1` «verificato sull'insieme dichiarato»; «minimo entro l'ora 14» smentito come obiettivo |
| 3 (f) | idem | soluzione versione 3 finale, piano finale, schermo e demo finali (18:32–18:40) | cap. 2 riscritto per riquadri: tredici blocchi, venti invarianti; §6.3 nuovo (scala con gelo all'ora 12); B9 e §3.10 (demo e prime misure) |
| 3 (g) | idem | discordanze dei fascicoli dell'allegato tecnico, f13 (18:15) | §4.7 e §3.10: velocità coperta da «circa 1,4» a 1,13 m/s; soglia «mobile» 5·σ·√(2/m); 99,25 % e 99,85 % nominati (Wilson: 99,05 % e 99,81 %); testa a 2,01 m per 1,70 m; suolo a ±44° 1,71–1,73 m; rese della lettura a un fotogramma; «83 su 90» e 15,9 ms attribuiti; C = 0,85 m non citabile |
| 3 (h) | idem | decimo addendum e blocco di classificazione, f14 (18:55) | B6: da «etichetta persona / non persona, a lato; primo taglio» a «classificatore su più classi, richiesto, non realizzato, non valutato»; invarianti I15–I20; scenario e portatore; dominio 1,44 m/s; §5.9, §8.10; decisione I |
| 3 (i) | idem | verdetto d'integrazione e chiusura della convocazione (`f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md`; `f5/CHIUSURA.md`, 19:09) | sintesi e «stato in dieci righe» riscritti; cap. 5 da «valutazioni in corso» a «valutazioni chiuse»; §5.6 con i sette controlli e i dodici cambi di stato; due cambi nuovi (continuità non eseguita su profondità; rilascio dell'avviso); diciotto condizioni (§2.4); §4.8; cap. 7 con tre decisioni nuove; legenda, indice, glossario, appendici aggiornati |
| 4 | *(da scrivere)* | *attese: innesto della continuità nella catena su profondità; correzione del rilascio dell'avviso; prova differenziale di I15; fusione del blocco di classificazione nei testi; inventario dei sensori e le tre prime misure; minuto 60; decisioni I–VI dell'utente; nuovo elenco dei riferimenti* | *si veda il §5.7* |
@@@ APP_A_V3
**Versione 3 (riquadri «Versione 3» di tutti i capitoli; §3.10, §4.1.10–§4.1.16, §4.6–§4.8, cap. 5, §6.3, cap. 7, §8.10, §10.3)** — scritta da [red.] nel passo d'integrazione. **Per intero:** `f12-integrazione/CONTRATTO_INTEGRAZIONE.md`; `f12-integrazione/30-arbitro/VERDETTO_INTEGRAZIONE.md`; `f5/CHIUSURA.md`; `f7-estensione/16-verdetto/VERDETTO_ESTENSIONE.md`; `f8-continuita/16-verdetto/VERDETTO_CONTINUITA.md`; `f10-dati/23-verdetto/VERDETTO_DATI.md`; `f12-integrazione/20-finale/SOLUZIONE_V3.md`; `f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md`; `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md`; `f12-integrazione/21-piano-finale/PIANO_14_4.md`; `ADDENDUM_UTENTE.md` (nono e decimo addendum); `documentazione/STATO_PROGETTO.md` (radice del progetto: la versione 2, in gran parte). **Solo la testa** (cambi di stato, scostamenti): `f12-integrazione/02-prova-insieme/PROVA_INSIEME.md`; `f12-integrazione/03-libero/LIBERO_DELLA_CELLA.md`; `f12-integrazione/06-identita/IDENTITA_SU_PROFONDITA.md`; `f12-integrazione/07-controprova-identita/CONTROPROVA_IDENTITA.md`; `f12-integrazione/10-attacco/ATTACCO_V3.md`; `f12-integrazione/11-completezza/COMPLETEZZA.md`; `f12-integrazione/12-piano-rifatto/PIANO_RIFATTO.md`; `f12-integrazione/13-statistica/CONTROLLO_PROVE.md`; `f12-integrazione/22-schermo-finale/SCHERMO_E_DEMO.md` (testa e §1); `f14-classificazione/10-attacco/ATTACCO_CLASSIFICAZIONE.md`; `f14-classificazione/CONTRATTO_CLASSIFICAZIONE.md`; `f11-documentazione/finale/CORREZIONI_APPLICATE.md` (§2); `f12-integrazione/40-documento/TESTO_DUE_PAGINE.md` (intestazione). **Citati e non aperti:** `f14-classificazione/01-profili/PROFILI.md`, `f14-classificazione/02-uso/USO_DELLA_CLASSE.md`, `f14-classificazione/03-classificatore/CLASSIFICATORE.md`; i fascicoli di f13; i file che V7, V8 e VD giudicano (`f7-estensione/13-soluzione/DECISIONE.md` e gli altri del §4.1.10; i cinque del §4.1.11; i cinque del §4.1.12); `f10-dati/04-embedded/INVENTARIO_E_DECISIONE.md` e `f10-dati/03-infrastruttura/AMBIENTE.md` (attraverso VD); `f12-integrazione/20-finale/TABELLA_CORREZIONI.md`; `f12-integrazione/51-riferimenti/RIFERIMENTI.md`; `f6-specializzazione/` (già fonte del cap. 8 nella versione 2); `RIFERIMENTI.md` di `documentazione/` (radice: usato solo per le chiavi già presenti qui). **Nessuna simulazione eseguita, nessuna cifra ricontata, rete non usata.** Di ogni file letto solo in testa le cifre sono riportate come le riportano VI e la versione 3.

@@@ APP_B_V3
**Fonti nuove da registrare (versione 3).** Le fonti qui sotto compaiono nei file integrati in questa versione e **non sono nell'elenco dei riferimenti** con cui questo documento è allineato (`RIFERIMENTI.md` di `documentazione/`, radice del progetto: nessuna voce trovata con una ricerca testuale). Le chiavi sono **provvisorie**: le definitive le assegna il curatore delle fonti. Nessuna è stata aperta da [red.]; la lettura è quella dichiarata dal file che le cita. Un nuovo elenco dei riferimenti è in scrittura (`f12-integrazione/51-riferimenti/RIFERIMENTI.md`, 19:20): non letto.

| Chiave provvisoria | Che cos'è | Link | Citata da · lettura dichiarata | Usata qui |
|---|---|---|---|---|
| `[red3-velocita-cammino]` | Wikipedia, «Preferred walking speed» | https://en.wikipedia.org/wiki/Preferred_walking_speed | BL §2 · pagina aperta da chi ha scritto la tabella dei profili, riaperta dall'attacco | §8.10, velocità della persona a piedi |
| `[red3-bohannon1997]` | Bohannon 1997, PMID 9143432 (riassunto) | https://europepmc.org/article/MED/9143432 | BL §2 · riassunto | §8.10 |
| `[red3-distanza-frenata]` | Wikipedia, «Braking distance» | https://en.wikipedia.org/wiki/Braking_distance | BL §2 · pagina aperta | §8.10, frenata di auto e furgone |
| `[red3-distanza-arresto]` | Wikipedia, «Stopping sight distance» | https://en.wikipedia.org/wiki/Stopping_sight_distance | BL §2 · pagina aperta | §8.10 |
| `[red3-rullaggio]` | Wikipedia, «Taxiing» | https://en.wikipedia.org/wiki/Taxiing | BL §2 · pagina aperta, riaperta dall'attacco | §8.10, aereo in rullaggio |
| `[red3-freno-emergenza-treno]` | Wikipedia, «Emergency brake (train)» | https://en.wikipedia.org/wiki/Emergency_brake_(train) | BL §2 · pagina aperta, riaperta dall'attacco | §8.10, treno |
| `[red3-bicicletta]` | Wikipedia, «Bicycle performance» | https://en.wikipedia.org/wiki/Bicycle_performance | BL §2 · pagina aperta, riaperta dall'attacco | §8.10 |
| `[red3-monopattino]` | Wikipedia in italiano, «Monopattino elettrico» | https://it.wikipedia.org/wiki/Monopattino_elettrico | BL §2 · pagina aperta | §8.10 |
| `[red3-regole-aeroporto]` | regole di sicurezza del traffico di un aeroporto, PDF, 2016 | https://www.munich-airport.de/_b/0000000000000008368639bb5e302e6f/traffic-safety-rules-2016.pdf | BL §2 · pagina aperta | §8.10, trattore di piazzale |
| `[red3-scheda-veicolo-automatico]` | scheda tecnica di un veicolo a guida automatica, PDF | https://www.hartfiel.com/wp-content/uploads/2024/04/MiR250-Specs.pdf | BL §2 · pagina aperta | §8.10 |
| `[red3-a320]` | Wikipedia, «Airbus A320 family» | https://en.wikipedia.org/wiki/Airbus_A320_family | BL §2 · pagina aperta | §8.10, ingombro dell'aereo |

**Da cercare, non lette da nessun ruolo** (BL, §2; DF, bibliografia): ISO 3691-4; ISO 13855 (la pagina dell'ente ha risposto con un rifiuto); regolamento UE 2019/945; una fonte per il tempo di reazione di una persona non vedente a un avviso sonoro (K-510). **Chiavi nuove dell'allegato tecnico:** il fascicolo di bibliografia cita 4 chiavi nuove e 19 chiavi dell'elenco che mancano in `documentazione/riferimenti.bib` (radice del progetto); stanno in `f13-allegato/06-bibliografia/allegato.bib` (non letto).

@@@ APP_C_V3
**La versione 3 (passo d'integrazione f12).** Scritta da `sciame-redattore` [red.] il 14 novembre 2026, partendo dalla versione 2 e applicando a una sua copia i frammenti di `f12-integrazione/50-stato/frammenti_1.md` e `frammenti_2.md` con il programma `componi_v3.py` (ogni punto d'innesto deve comparire una volta sola nella versione 2, altrimenti il programma si ferma). Si rifà con `python3 -I -B componi_v3.py` nella cartella. **Che cosa ho fatto oltre a leggere:** niente simulazioni, niente riconteggi; solo i controlli testuali di `controlla.py`, con le previsioni scritte prima (`PREVISIONI.md`, 19:20:52). **Esiti dei controlli:** nel file `MODIFICHE.md`, in fondo. **Indipendenza:** condivido con tutti i ruoli il modello linguistico e i file; non ho verificato nessuna cifra: ogni cifra nuova vale quanto il file da cui viene, e porta lo stato che le dà l'arbitro. **Scostamenti.** (1) Otto ingressi della consegna sono letti solo in testa e tre non sono aperti (appendice A): le loro cifre passano per il verdetto d'integrazione e per la versione 3. (2) Il testo ereditato dalla versione 2 non è riscritto riga per riga: resta sotto i riquadri «Versione 3», con le righe superate nominate nel riquadro; chi legge un paragrafo deve leggere prima il riquadro. (3) Le tabelle del §4.2 e dell'appendice B non sono aggiornate riga per riga: le correzioni stanno nel §4.7 e nelle «fonti nuove da registrare». (4) Lunghezza: la consegna vieta di togliere contenuto ancora vero; il documento cresce. (5) Rete non usata; nessuna fonte riaperta. Regole violate: nessuna che io sappia (niente git, niente sudo, scritture solo in `f12-integrazione/50-stato/`).

