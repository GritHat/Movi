# Verdetto dell'estensione f8 — la continuità visiva (`sciame-arbitro`, fase f5)

**In testa.** Lavoro dalle 17:29 alle 17:42 del 14 novembre 2026 (`date -Is`). Lunghezza: quattro pagine fitte (circa 3140 parole, 6 % più del triage); con un'impaginazione larga sfora, e lo dichiaro. **Verdetto.** Q3: il nucleo versione 2 **non rispetta** l'imperativo. Q4: le modifiche (`13-soluzione/MODIFICHE_CONTINUITA.md`, qui **M**) lo fanno rispettare **in simulazione, a sensore fermo, con la maschera d'ombra esatta**, dentro un dominio dichiarato (§2.1); fuori ci sono **controesempi certificati**. **Non «adottabile» nel senso della pipeline; adottabile come progetto di prototipo** con le correzioni c1–c8. **Cambi di stato.** (1) §5.5 del mio verdetto del nucleo («la previsione vale circa mezzo secondo… la continuità la porta l'avviso»): **sostituita**. (2) §5.4, «stessa identità al ritorno, 100 %»: **non regge con C6** in due codici indipendenti di f8, banco e controprove (K-218). (3) C-EST com'è scritta: **smentita**. (4) «Con 4 persone ci sta con `sd-0`» (M §2.11): **smentita** con le correzioni (58,5–62,75 ore-persona contro 56 [arb.]). (5) «Tre conti che non coincidono» (M, O1): è **una definizione**. (6) «9 su 10 fino a 1 s in ogni prova» (`15-statistica` §4): **smentita** dalle controprove. **Scostamenti.** `PREVISIONI.md` è scritto dopo la lettura dei documenti, cieco solo rispetto al riconteggio; due script sono nati dopo (`riconta_semi.py`, `semi_altri.py`); nessun simulatore rieseguito; di `SOLUZIONE_V2.md` letti §1–§3; f9 non letta. **Regole violate:** nessuna che io sappia. Le **ore** sono stime degli autori, **non verificate**; le somme sono mie [arb.]. Tutto è **simulazione o conto**: nessun fotogramma vero.

**Cifre ricontate sui file** (`riconta_verdetto.txt`, 29 gruppi; `riconta_semi.txt`): **tornano tutte**; nel testo portano **(R)**. Fra queste: i vuoti del nucleo e di `sd-1`, i due denominatori (86/92 = 86/98; 101/105 = 101/119), i riagganci, C-EST, le controprove, le celle a semi riparati, R100. **Note di lettura:** (a) i «2 in D» di C-EST (banco §4) sono passaggi con un vuoto, non con cicli «perso» (0); (b) le 15,5 ore di M sono l'estremo basso della sua tabella (15,5–19,5); (c) 19 / 38 / 33 % vale sui cinque comportamenti sul percorso. Tre numeri con «/» = geometrie D (demo, pannello 1 m) / T / L (pannello 2 m). «Sul percorso» = prosegue, rallenta, si ferma, torna, sosta lunga.

## 1. Q3 — il nucleo versione 2 rispettava l'imperativo? No

| Parte | Esito | Prova |
|---|---|---|
| Previsione mostrata (strato 2, «metà dell'ombra», «perso» assorbente) | **non rispettato** | regione nel 19 / 38 / 33 % dei cicli senza osservazione; un vuoto in 1958 / 1991 / 1999 passaggi su 1958 / 2000 / 2000; in demo «previsto» 0,67 s, spento prima della ricomparsa in 332 transiti su 355 (R; `11-misure/risultati/prova_*_pd09.tsv`); cinque codici (F-201) |
| Precisione dichiarata (cerchio del filtro) | **non rispettato** | a 2 s contiene il soggetto nello 0,00–0,06; chi torna 0,29–0,77; il «50 %» contiene 0,63–0,85 (triage, F-202) |
| Centro della previsione; incertezza controllata | **in parte** | il centro batte «fermo», ma sta su suolo visto libero nel 22 % dei cicli (banco §2); la regione è limitata, ma oltre soglia sparisce |
| Ingresso nell'ombra (B5) | **non rispettato**, ed è sicurezza | soggetto nascosto senza traccia pendente in 87 passaggi su 2800; 499 su 600 con l'ombra stimata a −20 cm (`12-torneo` §2) |
| Avviso «possibile presenza» (strato 1); invarianti 1–5 e 7 | **rispettato** | contiene il nascosto nel 100 % (R) |
| Accettazione (R3, H9), profili d'uso, demo, documento | **non rispettato** o in parte | H9 misura l'identità, non la copertura; «si riduce a un istante»; atto 4 «per un attimo» (triage §1) |

## 2. Q4 — le modifiche lo fanno rispettare? Controllo per controllo

| Controllo | Stato (pipeline) | Per costruzione | Sostenuto dai dati in simulazione | Dove cade |
|---|---|---|---|---|
| **1. Continuità** | **dimostrazione condizionata** (premessa: la traccia è entrata nell'ombra) più **evidenza sperimentale**; **controesempio certificato** all'ingresso e al riaggancio | il pavimento (senza celle, la regione è tutto il «non visto libero» dell'ombra); «perso» non è più uno stato | 0 passaggi con un vuoto su 2716 / 2800 / 2798 e, a semi riparati, su 13 638 / 5600 / 5597; 0 nelle controprove (R) | traccia chiusa prima dell'ombra: 9 su 2800; **130 su 1581** con rilevamento 0,7 e corpo esteso (R). Riaggancio composto: 102/273, 306/397, 250/332 (R). «Identità ambigua» assorbente: 0 riagganci su 66 e su 100; 87 / 117 / 95 pendenti (R). Il punto arretra nel 18 / 4 / 3,5 % dei «prosegue» (R), 29 / 13,5 / 15 % nelle controprove: soglia 5 % |
| **2. Efficacia** | **evidenza sperimentale** (tre geometrie, miscela «squadra») | — | errore mediano del punto in T 0,18 / 0,39 / 0,60 m a 1 / 2 / 3 s, contro 0,97 / 1,53 / 1,64 di «fermo» (M §2.2, banco §2; non ricontati); mai oltre 1,22 volte la base migliore | in «ampio» la croce sbaglia quanto un segno fisso (0,45 contro 0,41 m); chi parte da fermo |
| **3. Precisione valutata in modo realistico** | **evidenza sperimentale nel dominio**; **controesempi certificati** fuori; **questione aperta** sul sensore | — | `sd-1`, semi riparati: limite inferiore di Wilson sopra 0,90 in **45 celle su 45** fino a 2 s (peggiore 826/879, limite 0,922) e sopra 0,85 in 60 su 60 fino a 3 s (R); una geometria mai tarata; larghezza riportata | §2.1 |
| **4. Incertezza controllata** | **dimostrazione condizionata** (maschere ricalcolate a ogni ciclo; «libero» giusto) | regione ⊆ ombra + fascia; R90 ⊆ R100; oltre soglia cambia segno, non sparisce | 0 cicli di R90 su visto libero oltre la fascia, 0 fuori da R100 (R) | dentro la fascia di 0,20 m tocca celle viste libere nel 92–100 % dei cicli; il punto su «libero» dopo il quinto ciclo: 13 / 0 / 23 cicli (R); soglia dell'80 % e orizzonte di 3 s scelti dopo i dati |
| **5. Sicurezza conservata** | **dimostrazione condizionata** per i tre principi; **evidenza** per lo strato 1; **controesempio** ereditato (K-016); due **questioni aperte** | nessun predittore scrive «osservato» o «libero»; R100 è lo strato 1; la previsione accende l'avviso e non lo toglie | 0 nascosti fuori da R100 su 175 802 istanti e 156 celle di controprova (R), anche a −20 cm e con 6° d'imbardata | secondo soggetto: identità sbagliata e avviso rilasciato in 193 casi su 193 (banco) e in 347 su 357 (torneo, R). Aperte: c1 contro l'estraneo (K-219); la chiusura «fuori dall'area osservata», mai eseguita. Il disco pieno senza misura: per costruzione, **non misurato** |
| **6. Costo e portabilità** | **evidenza sperimentale** per il costo; portabilità: **questione aperta**, con un **controesempio** in moto | interfaccia unica (celle, punto, età, livello, stato) | C: 0,6–1,4 ms al 95º percentile con dieci tracce; Python puro: 5,3 ms, 6,2 al 95º (R); limite 6,7; macchina condivisa | 120 tracce pendenti: 5,4 ms in C. In moto, con 1° e 2° di tremolio d'imbardata, R90 scende a 0,76 e 0,56 a 2 s; ausilio indossato: niente provato |

### 2.1 Il dominio della cifra di precisione, e dove cede

Dominio: sensore e ostacolo fermi, un soggetto per ombra visto almeno 4 fotogrammi, ingresso fra 0,3 e 1,8 m/s, sul percorso, rumore misurato, libreria dei percorsi dello stesso tipo di camminatore. **In nessuna prova la libreria viene da un generatore e i passaggi da un altro** (`15-statistica` §4). Fuori (`14-attacco/ris`, `15-statistica/ris`):

| Che cosa cambia | Quota dentro la regione a 1 / 2 / 3 s |
|---|---|
| chi svolta; chi esce dal lato lontano | 0,86–0,94 / 0,54–0,70 / 0,38–0,52; 0,77–0,92 / 0,32–0,67 / 0,13–0,47 (R): lo copre solo l'avviso |
| ombra stimata più stretta di 10 e di 20 cm, corpo esteso, rilevamento 0,7 | 0,46 / 0,37 e 0,37 / 0,28 a 1 / 2 s (R); con il soggetto puntiforme 0,99 / 0,95: **il banco non lo vede** |
| parte da fermo accanto al pannello | 0,11 / 0,16 / 0,26 (R) |
| camminatori meno regolari della libreria, ombra larga | 0,944 / 0,835 / 0,801 (R); libreria di 30 calmi su vivaci: 0,73 a 2 s |
| rumore 4 / 9 / 16 cm non rimisurato | 0,44; rimisurato 0,87 |
| oltre 3 s | a 5 s 0,787 in D (174/221, R): nessuna cifra dichiarata |

Nessuna candidata tiene il livello 50 %. Il «100 %» dell'avviso vale per costruzione più conteggio, non come taratura.

## 3. Contraddizioni

| K | Stato dopo banco, torneo, controprove e analisi |
|---|---|
| K-201, K-206 | **risolte contro C-EST**: cicli «perso» in 374 e 1312 passaggi su 2000 (T), 1976 e 1987 (L); «sosta» a 3 s 0,72 e 0,53 (T), 0,14 e 0,00 (L) (R) |
| K-202 | **aperta nel numero**: «metà» spegne tutto in demo; l'80 % è scelto dopo i dati e in demo scatta a 1,00 s, prima della ricomparsa in 269 «prosegue» su 273 (R) |
| K-203, K-204, K-205, K-208 | **risolte in simulazione**: il punto ibrido con attesa non è peggiore di «fermo» (in «ampio» niente croce, c8); il deterministico tiene con area minore; un solo livello, detto «almeno» |
| K-207, K-209 | la taratura si trasferisce fra geometrie, non fra rumori né fra camminatori; K-209 di fatto «pavimento con la larghezza accanto», scelta formale al coordinatore |
| K-210 | **risolta contro S2 com'è scritta**: dopo una sosta improvvisa l'errore passa da 0,040 a 0,178 m; il segno pieno compensato cade nell'ombra in 393 passaggi su 400 senza C6 (`12-torneo/ris/a17_s2.txt`) |
| K-211, K-212 | chiuse: 0,67 s (R); apparente |
| **K-213** (O1, O2 di M) | **risolta**: banco e M usano denominatori diversi (R); si adotta «nascosti dentro l'area osservata», chi esce dall'area a parte |
| **K-214** copertura a 5 s: ≥ 0,905 contro 0,73–0,80 | **aperta**: nessuna cifra oltre 3 s |
| **K-215** (O4) ombra stimata stretta | **controesempio in simulazione**; c3 non provata; decide il sensore |
| **K-216** (O3) velocità tripla dentro la porta: 5,5 % contro 72 %. **K-217** (O5) C-EST in demo: regge nel banco (transito dominante in 1 passaggio su 200), non nel torneo (174 su 202) | **aperte**, senza effetto sull'esito: la porta vale come segnale; C-EST cade in T e L nei due codici |
| **K-218** identità al ritorno «100 %» (nucleo) contro 0,37–0,99 con C6 | **aperta**: c1 provata dopo, sugli stessi semi (275/277, 398/399, 332/338) |
| **K-219** c1 allarga il riaggancio ↔ estraneo (K-016) | **aperta, sicurezza**: mai provate insieme |
| **K-220** M1 entra subito (meno scoperti) ↔ false entrate (4,7 a passaggio da fermi in vista) | **aperta**: c4 le porta da 92 a 7 passaggi su 400, gli scoperti restano 131; c7 non provata |
| **K-221** «30 camminate» ↔ 200 percorsi ↔ due persone a tre andature | «30» **smentita** (0,88 e 0,82 a 2 e 3 s); il numero è aperto |
| **K-222** «9 su 10 a 1 s in ogni prova» ↔ 0,37 e 0,11 a 1 s | **risolta**: vale nel dominio del §2.1 |
| **K-223** intervalli di banco e M | **risolta**: i semi contigui di `gen.h` danno lo stesso flusso spostato di uno (rifatto da me: 1000 su 1000); intervalli stretti di 1,3–2,5 volte, stime confermate a semi riparati; `torneo.c` e `att.c` ne sono esenti (`semi_altri.txt`) |

**Effetto sul verdetto del nucleo.** K-004 chiusa come regola («metà» cade), aperta come numero (K-202). K-014: M1 la riduce in simulazione (499 → 16 su 600); aperta sul sensore. K-015 intatta. K-016 **non riparata**. K-017 cambia forma: il costo di C6 su chi torna sparisce (0,935–0,977 a 3 s, R), ma C6 fa cadere il riaggancio del nucleo (K-218) e non scatta con l'ombra stimata stretta (K-215). K-018: la riga è scritta in M1, mai eseguita. **Le nove condizioni:** la 1 (filtri spenti) diventa premessa anche della previsione, che usa il «libero» [arb., deduzione non provata]; la 2 prende il limite inferiore di 0,3 m/s; la 3 resta, e in quella geometria la previsione localizza per circa 1 s; la 4 è rafforzata (controllo 6); la 5 e la 6 valgono anche per la previsione; la 7 si allunga (§5); la 8 è scritta ma non provata; la 9 diventa «solo in simulazione, a sensore fermo, soggetto puntiforme salvo le controprove». **Decima, nuova:** un solo livello dichiarato, con il dominio e con «previsto ampio».

## 4. Correzioni obbligate, in ordine

**Già nelle modifiche:** riga d'ingresso (M1); «perso» → «previsto ampio» e chiusure motivate (M2); R100 = strato 1; maschere a ogni ciclo; pavimento; un solo livello; porta (M7); S2 riscritta; C6 come presupposto.

**Da fare nel passo d'integrazione** (prima la sicurezza):
1. **c7**: una traccia chiusa o non confermata con l'ultima misura entro 0,75 m da un'ombra accende l'avviso. *Non provata.*
2. **c1** riaggancio riscritto, e **prima** la prova contro l'estraneo (K-219).
3. **c2**: le pendenti ambigue di un'ombra diventano un solo avviso e non bloccano il riaggancio.
4. **c4**: entrata dopo due cicli senza misura.
5. **c3**: «gruppo tagliato» definito sull'immagine. *Non provata; col sensore.* Finché manca, la cifra vale «con la maschera esatta».
6. **c5**: sotto 0,3 m/s subito «ampio» (porta 0,22 a 0,65 a 1 s: non basta; «fermo negli ultimi 2 s»: non provata).
7. **c6** «visto in parte» a contorno pieno; **c8** soglia sulle sole celle d'ombra e, in «ampio», niente croce.
8. `statistico-3`: un denominatore e la regola di Wilson (cadono O1, O2 e «non superata per un millesimo» di M §2.8). `statistico-5`: «almeno 9 su 10» fino a 2 s, «almeno 8 su 10» fino a 3 s, poi «ampio». `statistico-4`: il tabellone conta la persona dentro la regione a 1 e a 2 s, non «la prima misura entro 0,40 m».
9. La chiusura «fuori dall'area osservata» non toglie l'avviso [arb.: richiesta, da provare].
10. Nel raffinamento: **c9** e `statistico-6` (circa 200 percorsi, due persone, tre andature). Dopo: c10; `statistico-7` prima di ogni nuovo lancio del banco.

**Manca la prova d'insieme:** c1–c5 sono provate una per una, dopo, sugli stessi semi: indizi, non conferme.

## 5. Adottabile? Che cosa entra, a quali condizioni

**Adottabile come progetto di prototipo, non come sistema validato.**

| Componente | Ore-persona | Fascia |
|---|---|---|
| M1 + c4 + c7; M2 + c2; M7 + c1; c5 | 5 | **indispensabile nelle 14 ore** (sicurezza e continuità) |
| M3: interfaccia «insieme di celle», `sd-0`, pavimento, punto ibrido | 2 | **14 ore**, per primo |
| M5 + c6 + c8 (disegno); M6 con le righe dello statistico (occlusione virtuale, tabellone «dentro k su n») | 7,5–9,5 | **14 ore**: è la «valutazione realistica» |
| c3; M8 (rumore misurato, libreria, due righe da 50 camminate) | 3–4 | **14 ore**, all'arrivo del sensore |
| M4: `sd-1` dietro la stessa interfaccia | 3–5 | **14 ore con 5 persone**; altrimenti raffinamento |
| c9, righe restanti del tabellone, S2 riscritta | 3–4 | **4 ore di raffinamento** |
| C-001, C-002, S3 e S4 di C-EST, c10, sensore in moto, due soggetti per ombra, battito sonoro | 5–8 l'uno | **dopo l'hackathon** |

**Bilancio [arb.]:** nucleo tagliato 37 (taglio di M) + continuità 15,5–19,5 + integrazione 4 + correzioni 4,25–5,25 + statistico 0,75–2 = **61,5–67,75** ore-persona; 58,5–62,75 con il solo `sd-0`. In 14 ore: **5 persone** 70, ci sta con 2–8,5 ore di margine; **4 persone** 56, **non ci sta** nemmeno con il solo `sd-0`; **3 persone** 42, mancano 16,5–20,75. Il settimo addendum dice cinque persone, e sensori non prima di 5–6 ore. **Non verificato:** il percorso critico in ore d'orologio (il nucleo aveva 38 ore in fila).

**`sd-0` o `sd-1`.** Le prove non sono pari: `sd-0` tiene 0,85 in 60 celle su 60 ma 0,90 solo in 37 su 45 fino a 2 s, e da 2 s occupa 0,8–1,7 volte l'ombra (R): dice «è dietro», non «dove». `sd-1` occupa 0,06–0,36 dell'ombra in T e L fino a 3 s (R). Nella demo sono vicini: 0,72 contro 1,13 a 1 s, poi tutta l'ombra.

**C-EST:** S3 e S4 non entrano. Di S5 entrano il contorno pieno solo con una misura, l'inviluppo tratteggiato ritagliato e l'età; non «conf Z%» (senza definizione) né la regione che sparisce. S2 entra riscritta, nel raffinamento; gli attacchi 1, 2 e 5 come prove.

**Non si può dichiarare:** «tarato» o «validato»; «90 %» senza dominio; un livello 50 %; una localizzazione «per tutta l'occlusione» nella demo; una cifra oltre 3 s; qualunque cifra in moto o indossato; «l'ellisse al 95 % è coerente»; che il riaggancio regga con due soggetti.

## 6. Affermazioni convergenti per la giuria

1. **Finché una persona seguita è dietro un ostacolo, lo schermo mostra a ogni fotogramma un segno e una zona tratteggiata dove può essere: non sparisce più.** *Per costruzione, e 0 passaggi con un'interruzione su circa 8300 simulati (e su 24 800 a semi riparati); prima erano quasi tutti. Cede se il sistema perde la persona prima dell'ostacolo: 9 su 2800; 8 su 100 con rilevamenti scarsi. `13-soluzione/ris`, `15-statistica/ris`, `14-attacco/ris`.*
2. **Precisione: in simulazione, a sensore fermo, chi resta sul proprio percorso (prosegue, rallenta, si ferma, torna indietro) sta dentro la zona in almeno 9 casi su 10 fino a 2 secondi senza essere visto, e in almeno 85 su 100 fino a 3; poi il sistema dice «previsto ampio».** *Sostenuto dai dati in simulazione: 45 combinazioni su 45, tre disposizioni, una mai usata per la taratura. `15-statistica/ris/semi_*.tsv`.*
3. **Dove cede, detto prima:** chi svolta o si allontana (3–7 su 10 a 2 s) è coperto solo dall'avviso; con il bordo dell'ombra stimato male di 10–20 cm la cifra scende a 3–5 su 10; chi parte da fermo accanto all'ostacolo, 1–3 su 10; camminatori diversi da quelli della taratura, 8 su 10. *Controesempi in simulazione. `14-attacco/ris`, `15-statistica/ris`.*
4. **La zona non sta mai su suolo che il sensore vede libero in quel momento (oltre un margine di 20 cm) e sta sempre dentro l'avviso.** *Per costruzione; 0 casi ricontati. `11-misure/risultati`.*
5. **La previsione non tocca l'avviso di «possibile presenza»: la persona nascosta era dentro l'area d'avviso nel 100 % dei casi, anche quando la zona stretta sbagliava.** *Per costruzione; 0 fuori su oltre 170 000 istanti simulati. Limite: un solo soggetto per ombra.*
6. **Con un'ombra larga la zona è stretta (da meno di un decimo a un terzo dell'ombra, fino a 3 s); nella demo, con il pannello da 1 m, localizza per circa 1 s e poi dice «è ancora dietro».** *Simulazione. `15-statistica/ris`, `14-attacco/ris/base_D.txt`.*
7. **La soluzione a due ipotesi della preproposta esterna, com'è scritta, non regge fuori dalla demo: fra 2 e 3 s smette di mostrare la zona in una quota dei passaggi che va da 2 su 10 a quasi tutti, e la sua ellisse al 95 % contiene la ricomparsa in 0–7 casi su 10 invece di 9. Ne teniamo le regole di disegno e gli attacchi.** *Controesempio in simulazione, due letture, due codici indipendenti. `11-misure/risultati`, `12-torneo/ris`.*
8. **Il calcolo costa circa 1 ms per ciclo con dieci oggetti in C (6 ms in Python), su CPU. Nessuna di queste cifre viene da una camera vera: sul sensore vale il tabellone, «dentro k su n».** *Misura su CPU condivisa; il resto non verificato.*

## 7. Da non dire, prossima prova, decisioni dell'utente

**Da non dire:** l'elenco del §5; in più «prevede dove sarà», «continuità garantita» senza il limite dell'ingresso, «la preproposta è stata adottata», «30 prove bastano» (27 su 30 dice «fra 0,74 e 0,97»).

**Prossima prova che cambia la decisione.** *In simulazione, subito:* gli attacchi 1–5 rifatti con c1–c5 e c7 **insieme**, su semi nuovi, da un'altra istanza, con l'estraneo contro c1 e il corpo esteso a −10 cm: se la regione resta sotto 0,85 a 1 s, la cifra del punto 2 si dichiara solo «con la maschera esatta». *Sul sensore, per primi:* l'errore della maschera al bordo del pannello e la distanza della prima misura valida dall'ombra (decidono K-215 e K-218); poi due righe da 50 occlusioni virtuali.

**Decisioni dell'utente.**
1. **`sd-1` nelle 14 ore o nel raffinamento**; e, con meno di cinque persone, che cosa si taglia ancora dal nucleo.
2. **La demo:** pannello da 1 m (previsione localizzata per circa 1 s, poi «è dietro»), oppure un'ombra più larga, dove la zona stretta si vede per 2–3 s.
3. **La cifra a schermo e nel documento:** «almeno 9 su 10 fino a 2 s» dalla simulazione, con i suoi limiti, oppure solo il contatore misurato sull'installazione.

**Rifare** (in `16-verdetto`): `timeout 120 python3 riconta_verdetto.py > riconta_verdetto.txt`; lo stesso per `riconta_semi.py` e `semi_altri.py`.

Controfirma: arbitro
