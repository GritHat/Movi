# PIANO_14_4 — 14 + 4 ore, cinque persone (`sciame-pianificatore`, f12, controllo C-E), 14 novembre 2026

Lavoro dalle 17:47 alle 18:00 (`date -Is`); circa 3 700 parole, in gran parte tabelle: al limite delle cinque pagine. Cartella: `f12-integrazione/04-piano/`. Programma: `piano_mc.py`; uscite:
`risultati_primo_lancio.txt`, `risultati_piano_mc.txt`; previsioni ed esiti: `PREVISIONI.md`. Si rifà con
`timeout 300 ../../f10-dati/ambiente/venv/bin/python -I -B piano_mc.py` (1 s).

## 0. In testa: cambi di stato, regole violate

- **«Con 5 persone ci sta, con 2–8,5 ore di margine» (V8 §5, bilancio in ore-persona): non regge come frase sul
  calendario.** Il bilancio torna anche a me (44,5 ore-persona probabili per il minimo, 57 con le aggiunte, su 70), ma
  decide la fila, non la somma. **Stato: sostenuto solo da una simulazione di stime mie** (20 000 estrazioni, tre semi):
  il minimo dimostrabile intero chiude entro l'ora 14 nel **0,29** dei casi [0,288; 0,300]; con i tagli scritti al §4 nel
  **0,46** [0,453; 0,467]; con 4 persone 0,08 e 0,28; col compito più lungo a una persona sola 0,18 e 0,29.
- **K-108 (le ore che restano): resta aperta**, con un dato in più: col riuso della catena di f10 le ore-persona
  bastano; non basta il percorso in fila (mediana della fine: ora 15,5 intero, 14,25 con i tagli).
- **Mie previsioni cadute: 4 su 9** (S-1: avevo previsto 0,45–0,80 per il primo piano, è uscito 0,016; S-3; S-6;
  poi S-8: 0,46 contro ≥ 0,60); S-4 regge in parte; R-1, R-2, R-3 (le prove sul riuso) reggono. Il piano consigliato (TC) è stato **ridisegnato dopo il primo esito**, senza toccare
  le stime dei compiti: va letto come scelto dopo.
- **Regola violata per errore:** un `git status --short` in sola lettura. Nessuna scrittura fuori cartella (gli
  eseguibili di prova sono nella cartella temporanea della sessione). Rete, sudo, GPU: non usati.
- **Tutte le durate sono stime, non misure.** Nessuna persona della squadra è stata sentita; i profili sono ipotesi.
  *Indipendenza:* stime, modello e programma hanno lo stesso autore; le ancore sono le ore dei verdetti V7 §1, V8 §5, V9.

## 1. Che cosa si riusa (misurato sul codice), e quanto costa rileggerlo

| Materiale | Che cosa ho misurato | Rilettura e adattamento (ore: ott./prob./pess.) | Rischio |
|---|---|---|---|
| Catena in Python, `f10-dati/10-catena` | 1 280 righe in 10 moduli, 590 di prove; **25 prove su 25 in 4,7 s rilanciate da me** (`prova_R1_catena.txt`); solo numpy; 2,5 ms a ciclo (CATENA §3) | rilettura A1 + B1: 1,5 / 2,5 / 5; l'adattamento sono A2, A3, B2, B3 | **alto.** Realizza il nucleo v2: ha ancora la memoria di 3 fotogrammi (da togliere, V7 a). **Preliminare (f10, senza verdetto):** identità alla ricomparsa 0 su 90 su profondità realistica, pannello detto «si muove» 79 su 90, soglia 40 che a 848×480 dà 0 su 10 |
| Simulatore, `11-simulatore` | 1 831 righe, numpy e scipy; 164 sequenze su disco (1,8 GB); controlli non rilanciati (scrivono nella loro cartella): **non verificato da me** | a scatola chiusa, con le misure di `20-validazione` (`misura_passaggi.py`, `banco_thor.py`): D1 1 / 1,5 / 3 | medio: rumore oltre 60° e pixel misti sono ipotesi (VALIDAZIONE §1) |
| Sequenze vere, `12-dati-veri` | 8 sequenze (2,0 GB), 901 righe di convertitori, formato rispettato (`esito_controlli.txt`) | D4 0,75 / 1,5 / 3 | solo descrittivo: posa ignota (salvo TUM), nessuna verità con persone |
| Predittori e banco in C, `f8/13-soluzione`, `11-misure` | `comp.c` 635 righe dense (50,6 kB), `banco.c` 599, `gen.h` 188; **compila senza errori** (`prova_R2_comp.txt`) | non è un modulo: `step_sd` e `step_c004` si riscrivono in Python dietro «insieme di celle» (dentro B2 e B4) | medio: traduzione di codice denso; controprova: stessa regione su 3 passaggi a seme uguale |
| Registro degli eventi, `f7/04-requisiti/eventi.py` | 418 righe, Python puro, **gira, uscita 0** (`prova_R3_eventi.txt`); estrattore di 99 righe, 50,5 µs a ciclo con 20 tracce | E3 2 / 3 / 5 (i nomi degli stati cambiano) | basso; è il primo taglio |
| Registratore e controllo del formato, `04-embedded`, `03-infrastruttura` | `registra_sequenza.py`, `controlla_sequenza.py`; mai collegato un dispositivo (INVENTARIO, in testa) | dentro E1 ed E4 | alto sul sensore vero: non provato |

Senza questo riuso vale il piano di V9 con 5 persone: «catena vera (innesto)» chiusa in 14 ore nello 0,0 % dei casi,
«continuità sul simulatore» nel 7,3–7,7 % (77,4 % col compito N5 spezzato, ipotesi dell'arbitro): `risultati_piano_14h.txt`
e `risultati_piano_14h_spezzato.txt` in `f9-preproposta/13-verdetto/`.

## 2. «Valutazione preliminare» chiusa all'ora 14 (proposta)

1. **Sul sensore simulato (verità esatta):** il tabellone M6 su almeno 90 passaggi con semi non usati per tarare:
   passaggi con un vuoto dopo l'ingresso in ombra (soglia 0); nascosti fuori dall'area d'avviso (0); persona dentro la
   regione a 1, 2, 3 s come «k su n» con l'intervallo di Wilson (soglie di C-C: 0,90; 0,90; 0,85, nel dominio
   dichiarato); celle «libere» con un ostacolo sotto (0); avvisi rilasciati senza aver guardato (0); tempo per ciclo
   e latenza in riproduzione a 15 Hz. Se una soglia cade, si mostra la cifra trovata.
2. **Su sequenze pubbliche di sensori veri:** copertura delle regioni sulle traiettorie di pedoni veri (THÖR, con
   l'occlusione virtuale); sulle 8 sequenze convertite solo conteggi descrittivi: invarianti violati, tempo per
   ciclo, quota di pixel validi. Nessuna cifra di precisione: manca la verità.
3. **Se arriva un sensore, la prima ora di misure:** tre pareti (errore di distanza), pavimento vuoto (residuo,
   pixel validi), `passa_dietro` con 10 passaggi: errore della maschera al bordo del pannello e distanza della prima
   misura valida dall'ombra (decidono K-215 e K-218). Si dichiara «una installazione, n = 10».
4. **La demo** del §8 in riproduzione, dichiarata come tale, e il video di ripiego.

**Minimo dimostrabile (MD):** punti 1 e 4, con dentro sicurezza (A2, A3) e continuità (B2, B3a, B3b). Il «minimo
intero» ha anche il punto 2 e la tabella delle regole; «con i tagli» li rimanda a dopo l'ora 14. **Per le 4 ore:** c9, le righe restanti del tabellone, S2 riscritta (V8 §5: 3–4 ore), `sd-1` se
non è entrato, il registro, le due righe da 50 occlusioni virtuali sul sensore (M8), i secondi autori di V-016,
V-017, V-019, T-008, il documento.

## 3. Compiti, stime a tre punti, chi, criterio «fatto»

Profili **ipotizzati**: P1 percezione e geometria; P2 tracciamento e previsione; P3 interfaccia e documento; P4 dati
e statistica; P5 sistema, sensori e secondo sviluppatore del tracciamento. Chi registra a casa non è contato fra i
cinque: **non verificato**. Ore di lavoro (ottimista / probabile / pessimista); «*» = fuori dal minimo; «°» = nel minimo intero, cade con i tagli.

| Id | Compito (origine) | Ore | Chi | Dopo | «Fatto» quando |
|---|---|---|---|---|---|
| K0 | Avvio: ambiente, 25 prove, lettura della versione 3, formato delle uscite | 0,5 / 0,75 / 1,5 | tutti | — | 25 prove verdi su ogni macchina |
| A1 | Rilettura di mappa, geometria, gruppi, ciclo | 0,5 / 1 / 2 | P1 | K0 | sa cambiare una soglia e rifare le prove |
| A2 | «Libero» nel solo fotogramma corrente; affidabilità persa sui pixel validi (V7 a, §1) | 1 / 1,5 / 3 | P1 | A1 | 0 celle libere sotto un ostacolo sulle scene di C-D; prove verdi |
| A3 | Sensore non in salute (c), C2 (d), controllo del piano (e) | 1,5 / 2,5 / 5 | P1 | A2 | su `azzeramento_progressivo` nessun «libero», tracce «dedotto, sensore non affidabile» |
| B1 | Rilettura di inseguimento, presenza, Kalman e dei predittori in C | 1 / 1,5 / 3 | P2 | K0 | elenco scritto dei punti dove entrano M1–M7 |
| B2 | M3: interfaccia «insieme di celle», `sd-0`, pavimento, punto ibrido | 1,5 / 2 / 4 | P2 | B1 | la regione esce a ogni ciclo nel file per fotogramma |
| B3a | M1 + c4 + c7; M2 + c2: ingresso in ombra, stati, chiusure | 2 / 3 / 5,5 | P2 | B2 | 0 passaggi con un vuoto su 30 di fumo |
| B3b | M7 + c1 con la prova dell'estraneo (K-219); c5 | 2 / 3 / 5,5 | P5 | B2, E2 | con l'estraneo nessun avviso rilasciato senza averlo visto |
| C1 | Riproduttore e schermo: quattro stati, tracce, età | 2 / 3 / 6 | P3 | K0 | una sequenza simulata scorre a 15 Hz |
| C2 | M5 + c6 + c8: contorno pieno solo con misura, inviluppo tratteggiato, contatore | 2 / 2,5 / 5 | P3 | C1 | osservato e dedotto si distinguono a colpo d'occhio |
| C3a | «Affidabilità persa» a schermo e un suono | 0,5 / 1 / 2 | P3 | C2 | scatta su `azzeramento_progressivo` |
| C3b° | Tabella delle regole ridotta | 1 / 1,5 / 3 | P1 | A3 | ogni stato ha una riga e un messaggio |
| D1 | Rilettura del simulatore e delle misure di f10; scelta delle sequenze | 1 / 1,5 / 3 | P4 | K0 | elenco delle sequenze e dei semi tenuti da parte |
| D2 | M6: occlusione virtuale, registro per ciclo, tabellone «dentro k su n» | 3 / 4,5 / 8 | P4 | D1 | il tabellone gira da solo sul tronco e stampa le righe del §2.1 |
| D4° | Corsa sulle sequenze pubbliche | 0,75 / 1,5 / 3 | P4 | D2, B2, A2 | tabella descrittiva e copertura su THÖR |
| E1 | Modulo d'inventario e istruzioni di registrazione all'utente; sorgente da cartella | 0,75 / 1,5 / 3 | P5 | K0 | spedito entro l'ora 3 |
| E2 | Banco di regressione (prove più 6 sequenze di fumo) e riproduzione a 15 Hz | 1 / 1,5 / 3 | P5 | E1 | un comando, meno di 2 minuti, usato da tutti a ogni modifica |
| PI | Prova d'insieme sul tronco | 0,5 / 1 / 2 | P2 + P5 | A2, A3, B3a, B3b, C2, E2 | regressione verde con tutte le regole accese |
| TAB | Corsa finale del tabellone e lettura | 0,5 / 1 / 2 | P4 | PI, D2 | tabella con n e intervalli, firmata con la versione |
| LAT | Latenza e cicli al secondo in riproduzione | 0,5 / 1 / 2 | P5 | PI | due numeri con il metodo |
| PG | Prova generale, registrata come video di ripiego | 0,75 a tempo chiuso | tutti | TAB, LAT, C3a | la demo scorre due volte senza interventi |
| A4* | Robustezza su profondità realistica: soglie per risoluzione, pannello che «si muove» | 1,5 / 3 / 6 | P1 | A3 | le cifre d'identità dichiarate come trovate |
| B4* | M4: `sd-1` dietro la stessa interfaccia | 3 / 4 / 7 | P2 o P1 | PI | stessa prova di B2 |
| E3* | Registro degli eventi | 2 / 3 / 5 | P3 | C3a | gli eventi di una sequenza coincidono col copione |
| E4* | Prima ora col sensore (ramo A); M8 e c3 | 1,5 / 2,5 / 5 | P4 (P5) | registrazioni | §2.3 |

**Percorso critico (ore d'orologio, mediane della simulazione con i tagli):** K0 0–1,0 → B1 –3,05 → B2 –5,8 → B3a
–9,7 (accanto B3b 6,2–10,1) → PI 11,1–12,05 → TAB 12,3–13,5 → PG 13,5–14,25. Sta sul percorso critico: TAB nel 96 %
dei casi, PI 84 %, B1 e B2 51 %, B3a 33 %, B3b 35 %, lo schermo (C1, C2) 19 %, il tabellone (D1, D2) 12 %.

## 4. Calendario per persona e per ora (mediane; ogni cella è l'ora che finisce a quel numero)

| Ora | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|
| 1 | K0 | K0 | K0 | K0 | K0 |
| 2 | A1 | B1 | C1 | D1 | E1 |
| 3 | A1 → A2 | B1 | C1 | D1 | E1 (inventario spedito) |
| 4 | A2 | B2 | C1 | D2 | E2 |
| 5 | A2 → A3 | B2 | C1 | D2 | E2 |
| 6 | A3 | B2 | C2 | D2 | scelta del ramo (§6); prova dell'estraneo preparata |
| 7 | A3 | B3a | C2 | D2 | B3b |
| 8 | A3 → C3b° | B3a | C2 | D2 | B3b |
| 9 | C3b° | B3a | C2 | D2 → primo tabellone sul tronco | B3b |
| 10 | A4* | B3a | C3a | D4° (ramo A: E4*) | B3b |
| 11 | A4* | aiuto a B3b, difetti del primo tabellone | scaletta, E3* | D4° (ramo A: E4*) | B3b |
| 12 | A4* → **gelo del tronco** | PI | E3* | tabellone di prova | PI |
| 13 | solo difetti bloccanti | solo difetti bloccanti | diapositive | TAB | LAT |
| 14 | PG | PG | PG | TAB → PG | PG |
| 15 | ciò che è rimasto fuori (ordine del §5) | B3 rimasto, poi B4* | E3*, S2 riscritta | righe restanti, M8 | sensore, c3 |
| 16 | come sopra → **gelo finale** | come sopra | come sopra | come sopra | come sopra |
| 17 | regressione, difetti bloccanti | regressione | documento | tabellone finale | latenza finale, video |
| 18 | prova generale 2, consegna | idem | idem | idem | idem |

Le pause sono dentro le mediane (efficienza d'orologio 0,78–0,96); vanno sfalsate, mai P2 e P5 insieme dopo l'ora 6.

## 5. Punti di controllo: regola scritta prima

Ordine dei tagli (continuità e sicurezza non si toccano): **1** etichetta «persona» (non si comincia); **2** zone;
**3** profilo sonoro (resta un suono); **4** `sd-1` (B4) al raffinamento; **5** registro (E3) al raffinamento;
**6** tabella delle regole estesa (C3b); **7** sequenze pubbliche (D4) dopo l'ora 14; **8** A4 a tempo chiuso, cifre
«come trovate»; **9** di A3 restano il ramo «sensore non in salute» e l'affidabilità sui pixel validi, (d) ed (e)
al raffinamento. Mai: A2, B2, B3a, B3b, il disegno osservato/dedotto, «affidabilità persa», il tabellone sul simulato.

| Ora | Si guarda | Se no (probabilità dal modello) |
|---|---|---|
| 2 | K0 chiuso entro 1 h 15; riletture avviate. **La misura che corregge le stime:** (fine di K0 + rilettura B1) / 2,25 h | rapporto sotto 1,2: P(MD) 0,75; 1,2–1,5: 0,50; 1,5–1,8: 0,24; **oltre 1,8: 0,04 → tagli 4–7 subito** e tutte le stime si moltiplicano per il rapporto |
| 5 | A2 ed E2 chiusi (0,40 dei casi) | 0,32 contro 0,67: tagli 4–6; P4 passa il primo tabellone a dopo B2 |
| 8 | B2, C1, A3 chiusi (0,82) | 0,06 contro 0,55: tagli 4–9 tutti; chi è libero affianca B3a o B3b (in coppia, stessa tastiera) |
| 11 | B3a, B3b, C2, D2 chiusi (0,42) | 0,08 contro 0,98: **la demo dell'ora 14 mostra il tronco com'è**; la regola mancante è nominata sullo schermo e nel tabellone; entra fra 14 e 16 |
| 12 | gelo del tronco; PI entro 12,5 (0,57) | senza PI entro 12,5: P(MD) 0,003 → TAB sulla versione gelata, niente modifiche |
| 14 | PG fatta, tabella firmata | la demo si fa comunque (tempo chiuso) con ciò che c'è, dichiarato |
| 16 | gelo finale | ciò che non è nel tronco esce dalla demo e va in «limiti» |
| 18 | consegna | — |

Con il gelo all'ora 12, continuità e sicurezza (A2, A3 ridotto, B2, B3a, B3b) sono tutte nel tronco nel **0,70** dei
casi; all'ora 14 nel 0,88; all'ora 16 nel 0,96. Manca più spesso B3a (0,21) o B3b (0,22).

## 6. I rami all'ora 5–6 (tabella di `f10-dati/04-embedded/INVENTARIO_E_DECISIONE.md`)

- **A. Arriva una camera di profondità densa** (prima scelta RealSense D4xx, poi Orbbec, OAK-D Pro, L515, Kinect v1).
  Il sensore resta a casa: si **registra e si spedisce** (dieci minuti del §4 dell'inventario; circa 1,4 GB, banda
  non verificata), niente flusso dal vivo. P4 fa E4 nelle finestre libere (ore 10–11 e dopo TAB); D4 passa a dopo
  l'ora 14. Costo sul minimo: P(MD) 0,44 contro 0,46. La prima ora col sensore chiude prima della prova generale
  nel 0,47 dei casi, e insieme al minimo entro l'ora 14 nel **0,16**: è più probabile che finisca fra 14 e 16.
  Kinect v2 e Azure Kinect: solo raffinamento (1–4 ore, può fallire).
- **B. Arriva solo altro.** Telefono con LiDAR: profondità registrata, 15 minuti, come dati e non come demo (stesso
  costo di A ridotto). Webcam: video di verità dietro il pannello. Telemetro: metro delle prove. LiDAR 2D, radar,
  ultrasuoni, moduli a microcontrollore: nessuna integrazione nelle 14 ore.
- **C. Non arriva niente.** Il piano non cambia: simulato e pubbliche; il §2.3 resta vuoto e si dichiara.

In tutti e tre la demo è una riproduzione; dal vivo solo con un sensore in sala (INVENTARIO §3).

## 7. Rischi e contromisure

| Rischio | Segnale | Contromisura |
|---|---|---|
| Il riuso va peggio del previsto (riletture × 2, correzioni × 1,5): P(MD) da 0,46 a 0,05 | rapporto dell'ora 2 oltre 1,5 | tagli 4–9 all'ora 2; non riscrivere: correggere dentro la catena con le 25 prove |
| Sottostima comune (tutte le durate × 1,2: −0,31) | lo stesso rapporto | la regola dell'ora 2 moltiplica tutte le stime |
| La coda finale (PI, TAB, PG: +1 h l'una toglie 0,17–0,20) | PI non chiusa all'ora 12,5 | tabellone acceso dall'ora 9, gelo all'ora 12, prova generale a tempo chiuso |
| B3a o B3b in ritardo (dividerlo vale +0,11) | ora 8, ora 11 | coppia sulla regola rimasta; interfaccia fra le due metà fissata in B2 |
| La catena cade sulla profondità realistica (f10, preliminare) | primo tabellone, ora 9 | A4 a tempo chiuso; cifre «come trovate», con la risoluzione; la possibile presenza non dipende dall'identità |
| Avvio lento (K0 preparato prima dell'ora 0: +0,13) | ora 1 h 15 | ambiente e lettura della versione 3 prima dell'ora 0, se il regolamento lo ammette: **non verificato** |
| Il sensore a casa non registra o non spedisce | ora 7 senza file | resta il ramo C; nessuna attesa: E4 è fuori dal minimo |
| Una persona manca (4 persone: 0,28 con i tagli, 0,08 senza) | — | tagli 4–9 dall'ora 0; il banco di regressione passa a P3 |
| Una frase «da non dire» in demo | prova generale | scaletta scritta con l'elenco dei verdetti accanto |

## 8. Simulazione delle durate: modello, esiti, che cosa li muove

Triangolari sulle stime del §3; ore di lavoro = base × fattore di squadra (lognormale, σ 0,12) × fattore della persona
(σ 0,20), a media 1: correlazione 0,55 fra due compiti della stessa persona, 0,13 fra persone diverse (stampata);
ore d'orologio = lavoro / efficienza (triangolare 0,78–0,88–0,96); code fisse per persona; compiti fuori dal minimo
solo nelle finestre libere. Non modellati: stanchezza nelle ore 14–18, persone che si scambiano i compiti, guasti.

| Caso (20 000 estrazioni; Wilson al 95 % entro ± 0,007) | P(MD entro l'ora 14) | Mediana / 80° percentile della fine |
|---|---|---|
| Primo piano, integrazione tutta insieme, B3 a uno / diviso | 0,016 / 0,022 | 21,1 / 24,9 h |
| **TC-5**, minimo intero | **0,29** | 15,5 / 18,1 h |
| **TC-5 con i tagli scritti** | **0,46** (entro l'ora 15: 0,62; 16: 0,75) | 14,25 / 16,5 h |
| TC-5 con B3 a una persona, intero / con i tagli | 0,18 / 0,29 | 16,7 / 19,8 h |
| TC con 4 persone, intero / con i tagli | 0,08 / 0,28 | 18,4 / 21,8 h |
| Altri due semi (TC-5; con i tagli) | 0,289–0,296; 0,459–0,462 | — |

**Che cosa muove di più** (TC-5 con i tagli): il riuso che va male −0,41; tutte le durate × 0,8 / × 1,2: +0,39 /
−0,31; pause al minimo +0,20; un'ora in più su PG, PI, TAB, K0: da −0,20 a −0,17; su B1 o B2 −0,10; su A1 o A2 0,00.
Correlazione di rango con l'ora di fine: fattore di squadra +0,58, P2 +0,37, P5 +0,23, P1 +0,02. **Lettura:** conta la
velocità comune e la catena della continuità (P2, P5), non la mappa. Un secondo ruolo deve rifarla con ipotesi sue (C-E).

## 9. La demo

- **Ora 14 (5 minuti, in riproduzione dichiarata, stessa catena):** (1) pavimento vuoto: «libero» solo dove si vede,
  il resto «non osservato»; (2) passaggio dietro il pannello: contorno pieno → inviluppo tratteggiato con l'età e
  l'avviso → riaggancio; (3) sosta dietro: la regione si allarga, «è dietro», l'avviso resta finché non si guarda;
  (4) sensore coperto: «affidabilità persa»; (5) il tabellone: k su n con gli intervalli, il dominio, i limiti, e che
  cosa è simulato. Se è arrivato il sensore: un passaggio vero, «una installazione».
- **Ora 18:** la stessa scaletta, più ciò che è entrato fra 14 e 16 (nominato), le misure sul sensore se ci sono, il
  video di ripiego pronto. Mai: «validato», «tarato», «90 %» senza dominio, «prevede dove sarà» (V8 §5 e §7).

## 10. Stati proposti e che cosa propongo dopo

- «Il minimo dimostrabile chiude in 14 ore con 5 persone»: **non provato**; nel mio modello 0,29–0,46. Lo decide la
  misura dell'ora 2 (rapporto fra durata vera e stima di K0 e della prima rilettura).
- «Con 4 persone non ci sta» (V8): **sostenuto** dalla simulazione (0,08; 0,28 con i tagli).
- «Dividere il compito più lungo aiuta»: **sostenuto** solo nel piano a integrazione continua (+0,11); nel primo
  piano no (+0,006): là la fila stava dopo.
- **Decisioni dell'utente:** accettare i tagli 4–9 dall'ora 0 (0,46) o tentare il piano intero (0,29); preparare K0
  prima dell'ora 0; chi registra a casa. **Dopo:** il secondo ruolo rifà la simulazione; l'arbitro assegna gli stati.
