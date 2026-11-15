# Sensori allo stato dell'arte e hardware dedicato per il volo veloce

`sciame-tempo-reale`, f19-volo/02-sensori-hw, 15-11-2026. File: `parametri_volo.json`, `latenza.json` (prodotto da
`latenza.py`), `PREVISIONI.md` (scritte alle 04:36:33, prima delle fonti e dei conti).

## 0. In testa: stati e regole

- **Nessuna misura su hardware.** Le sole misure sono quelle del prototipo in Python (f15/11-prove). Tutto il resto è
  **calcolato** da **ipotesi** o da **fonti**. Delle fonti, ne ho **aperte oggi** solo tre: heise (Taalas), il blog
  Cerebras, le diapositive CERN sul filtro di Kalman su FPGA. EchoShield, ASR-11, CM202A, SupIR, AC 90-48 e il CFAR su
  FPGA vengono da **riassunti di ricerca**: i PDF hanno dato 404 o 403. Sono segnati «NON APERTA» nel JSON e vanno
  aperti prima di citarli nel documento tecnico.
- Non ho violato regole: niente cancellazioni, niente git, scritture solo in questa cartella e nello scratchpad.
- In questo compito non entrano prove ripetute, quindi nessun intervallo di Wilson. Gli intervalli sono [minimo;
  massimo] delle ipotesi per stadio, sommati nel caso peggiore.

## 1. Sensori per il volo veloce (dettagli e fonti in `parametri_volo.json`)

| sensore | rivisita | portata | che cosa non vede | stato |
|---|---|---|---|---|
| Radar a scansione elettronica, classe Echodyne EchoShield (banda Ku) | 0,1 s (10 Hz in traccia) | traccia tipica: Cessna 2,5 km, Matrice 600 1,4 km, Phantom 4 1,0 km; strumentata 30 km | fuori dai 130×90° del pannello; dietro detriti densi; i primi 0,3–0,5 s di una traccia nuova | fonte non aperta (dati del produttore, di parte) |
| AESA multifunzione con rivisita programmata | 0,025 s (40 Hz sul bersaglio) | 5 km su un aereo leggero | i settori in ricerca; con molti bersagli (detriti) la rivisita di ciascuno cala | **ipotesi**: nessun esemplare con scheda |
| Radar di avvicinamento ASR-11 (banda S) | 4,8 s | 111 km (60 NM) | 1,2 km di percorso fra due giri a 250 m/s; bassa quota; droni piccoli | fonte non aperta |
| ADS-B 1090ES | 0,5 s (1 s è il minimo di legge) | portata radio | chi non trasmette, i detriti, l'avionica danneggiata (resta l'ultimo dato, vecchio); latenza fino a 2,0 s | 1 s e 2,0 s: fonte aperta (14 CFR 91.227); 0,5 s: non aperta |
| Identificazione remota (droni) | 1 s | portata radio | droni non conformi, detriti | fonte aperta (14 CFR 89.310) |
| Multilaterazione | 1 s, σ di 30 m | — | chi non trasmette | ipotesi |
| Torretta EO/MWIR, classe CM202A con ottica SupIR | 30 Hz; brandeggio a 150°/s | rilevamento oltre 25 km con ΔT di 2 °C (alle condizioni del produttore) | fuori dal campo stretto (1,7°, cioè 74 m a 2,5 km); fumo, nebbia e fiammata (il MWIR si acceca); il mosso durante il brandeggio | fonte non aperta |
| LiDAR a campo stretto, Livox Tele-15 | 10 Hz | 500 m | oltre 500 m; fumo | fonte aperta in f15 |
| Sensore passivo a radiofrequenza | 0,5 s, 3° | — | droni autonomi che non trasmettono, detriti, aerei | ipotesi |

**Lettura per gli eventi impulsivi.** In un evento con collisione, detriti o fiammata:

- ADS-B e identificazione remota perdono proprio l'oggetto colpito, cioè l'ultimo dato smette di arrivare.
- L'EO/IR si acceca nella fiammata.
- Resta il radar, che però ha da seguire molti più bersagli.

Con una schiera attiva il costo è la rivisita: i bersagli da seguire si moltiplicano per i frammenti, e il tempo di
fascio dato a ciascuno cala. Ne segue una regola da mettere nel nucleo (**ipotesi**, da provare nel simulatore):

- quando la rivisita di un oggetto supera 0,1 s, il suo stato passa a «non osservato»;
- intanto la zona di possibile presenza si allarga di v·T + a·T²/2, come in `tra_due_rivisite`.

## 2. Bilancio della latenza dalla cattura all'avviso (`latenza.json`)

I valori sono in ms, nel caso peggiore, con la traccia a 10 Hz. Fra parentesi, il caso a 40 Hz.

| stadio | CPU generica | GPU | dedicato (FPGA o ASIC) | origine |
|---|---|---|---|---|
| età della misura (attesa della rivisita) | 0–100 (0–25) | uguale | uguale | fonte EchoShield; 40 Hz è un'ipotesi |
| acquisizione (integrazione coerente) | 5–20 | 5–20 | 5–20 | ipotesi; non dipende dal calcolo |
| trasferimento dei dati grezzi | 0,5–2 | 0,6–2,5 | 0,001–0,01 (in linea) | ipotesi |
| elaborazione del segnale (fasci, FFT distanza-Doppler, CFAR) | 5–20 | 1–3 | 0,05–0,5 | ipotesi; per l'FPGA, il CFAR in 10 cicli a 100 MHz (fonte non aperta) |
| estrazione dei plot | 0,5–2 | 0,2–1 | 0,01–0,1 | ipotesi |
| associazione, filtro a più regimi, previsione, regione, regole | **0,09–55** | 0,05–5 | 0,01–0,5 | CPU: **misura del prototipo** (Python: mediana 0,09–11 ms, p95 peggiore 55 ms, modo interfaccia); il resto è ipotesi |
| uscita verso una macchina / verso un operatore | 0,1–1 / 17–50 | uguale | 0,01–0,1 / 17–50 | ipotesi (lo schermo va a 60 Hz) |
| **per aggiornamento, verso una macchina** | 11–200 (11–125) | 7–133 (7–58) | 5–121 (**5–46**) | calcolato |
| conferma di una traccia nuova (3 rivisite su 5) | +300–500 (+75–125) | uguale | uguale | ipotesi; è un costo del **sensore** |
| **primo avviso, verso una macchina** | 311–700 (86–250) | 307–633 (82–183) | 305–621 (**80–171**) | calcolato |

Il modo prudente del prototipo (p95 di 340 ms, misurato) porta la CPU a 534 ms per aggiornamento e a 1,03 s per il
primo avviso.

**Analogia con l'hardware dedicato, e quanto se ne può prendere.**

- **Chip per i modelli linguistici.** Su Llama 3.1 8B, Taalas HC1 dichiara circa 17 000 token/s per utente, contro i
  circa 230 di una H200: 74 volte. Cerebras ne fa circa 1936 (8,4 volte; il produttore dichiara 20 volte). Fonti:
  heise (21-02-2026) e il blog Cerebras, **aperte oggi**. Sono dati del produttore: una prova indipendente dà 14 357
  token/s, da riassunto di ricerca. Il motivo del guadagno è che la decodifica è **limitata dalla memoria**: portare i
  pesi sul chip toglie il viaggio verso la memoria esterna.
- **Dove l'analogia vale.** Vale per l'**elaborazione del segnale radar**, che è un flusso di dati grezzi limitato
  dalla banda. Su un FPGA in linea col convertitore i dati non passano dalla memoria del calcolatore, e il fattore
  prudente sulla CPU va da 10 a 100 volte. Ho usato 40 volte nel caso peggiore (da 20 a 0,5 ms) e 6 volte sulla GPU.
- **Dove l'analogia non vale.** Non vale per il **filtro e l'associazione**. Sono pochi oggetti, con uno stato
  piccolo e un calcolo limitato dai tempi di contorno. Il CERN misura un passo di Kalman su FPGA in circa 725 ns,
  contro circa 250 ns su CPU: «So far, no speedup!» (diapositive **aperte oggi**). Il guadagno vero viene da un'altra
  parte: dal passaggio dal Python al codice compilato (10–100 volte, **ipotesi**), e dal **determinismo** del caso
  peggiore, perché su un FPGA il 99° percentile coincide con il massimo.

Un ASIC fatto apposta per tutta la catena, analogo all'HC1, toglierebbe al più i circa 75 ms di calcolo della colonna
CPU. La rivisita e la conferma resterebbero dove sono.

**La conclusione** (calcolata):

- Con la traccia a 10 Hz, l'hardware dedicato porta il primo avviso da 0,70 a 0,62 s: guadagna circa 80 ms.
- Portare la rivisita da 10 a 40 Hz lo porta da 0,62 a 0,17 s: guadagna circa 450 ms.
- **La leva è il sensore, cioè la rivisita e la conferma, non il calcolo.** Fa eccezione il modo prudente del
  prototipo: lì il calcolo pesa (p95 di 340 ms), e il codice compilato o un FPGA servono a tenerlo sotto i 0,5 ms con un
  massimo garantito.

## 3. Quando l'avviso è tempestivo

La formula è d_min = v · (L_primo avviso + t_risposta + ritardo del mezzo), con v la velocità verso un punto fermo.
In un incontro frontale fra due mezzi le velocità si sommano.

I tempi di risposta e i ritardi usati sono questi:

- **Umano senza ausilio: 12,5 s.** È il totale della tabella 1 dell'AC 90-48D (fonte non aperta).
- **Umano con un avviso che dà la direzione: 5,4 s.** È calcolato dalla stessa tabella: 1,0 s per riconoscere, 4,0 s
  per decidere, 0,4 s per i muscoli. I 5,0 s per «capire la rotta di collisione» li fa il sistema.
- **Umano addestrato con una procedura fissa: 1,5 s** (**ipotesi**, fra 0,75 e 2,5 s).
- **Ritardo del mezzo:** 2,0 s per l'aereo (dalla tabella) e 0,5 s per il drone (**ipotesi**).

La distanza minima è in metri. Le sigle delle colonne sono queste:

- **CPU:** CPU a 10 Hz, primo avviso in 0,75 s.
- **D10:** hardware dedicato a 10 Hz, 0,62 s.
- **D40:** hardware dedicato a 40 Hz, 0,17 s.

| mezzo, v | umano senza ausilio, CPU | umano con direzione, CPU / D10 | umano addestrato, D10 | macchina, CPU / D10 / D40 | catena su (catena + umano addestrato) |
|---|---|---|---|---|---|
| aereo 70 m/s | 1067 | 570 / 561 | 288 | 192 / 183 / 152 | 15 % |
| aereo 120 m/s | 1830 | 978 / 963 | 495 | 330 / 315 / 261 | 15 % |
| aereo 180 m/s | 2745 | 1467 / 1444 | 742 | 495 / 472 / 391 | 15 % |
| aereo 250 m/s | **3812** | **2037 / 2005** | 1030 | 687 / 655 / **543** | 15 % |
| drone 20 m/s | 275 | 133 / 130 | 52 | 25 / 22 / 13 | 24 % |
| drone 45 m/s | 619 | 299 / 293 | 118 | 56 / 50 / 30 | 24 % |
| drone 70 m/s | 962 | 465 / 456 | 183 | 87 / 78 / 47 | 24 % |
| drone 90 m/s | **1237** | 598 / 587 | 236 | 112 / 101 / 60 | 24 % |

**Lettura**, tutta calcolata da fonti e ipotesi:

1. **Domina l'umano.** La differenza fra un umano senza ausilio e una macchina, a 250 m/s, vale 3,1 km. L'hardware
   dedicato, sulla stessa colonna, ne toglie 32 m.
2. **Aerei a 250 m/s.**
   - Con il radar di classe EchoShield (traccia tipica 2,5 km su un Cessna), l'avviso è tempestivo per una macchina
     (0,55–0,69 km) e per un operatore addestrato (1,03 km).
   - Per un umano avvisato con la direzione (2,0 km) è al limite: deve restare entro la portata compresa la conferma.
   - Per un umano senza ausilio (3,8 km) non è tempestivo.
   - L'ASR-11 ha la portata (111 km), ma la conferma richiede 9,6–14,4 s, cioè 2,4–3,6 km di percorso. Va bene per
     un aereo lontano, non per un evento improvviso vicino.
3. **Droni a 90 m/s.** Con il Phantom 4 tracciato a 1,0 km, l'avviso è tempestivo per l'umano con la direzione
   (0,59 km) e non lo è per l'umano senza ausilio (1,24 km).
4. **Che cosa non è contato.** La geometria della manovra di scansamento e la distanza di frenata: qui c'è solo il
   ritardo del mezzo. Le distanze sono quindi un **limite inferiore** del bisogno.

## 4. Gli esiti delle previsioni

| previsione | esito |
|---|---|
| P1 | **Regge** a 10 Hz: il calcolo pesa dal 32 al 40 % nel caso peggiore. **Smentita** a 40 Hz verso una macchina (63 %) e nel modo prudente. |
| P2 | **Non risolta.** L'analogia dà da 8 a 74 volte per i carichi limitati dalla memoria, ma per il filtro su FPGA il CERN dà 0,34 volte. Lo deciderebbe una misura del nucleo compilato e del CFAR su una scheda FPGA. |
| P3 | **Regge**: 5–46 ms per aggiornamento a 40 Hz, 5–121 ms a 10 Hz, entrambi dentro la soglia fra 10 e 200 ms. |
| P4 | **Mista.** Il rapporto fra il tempo umano e la catena va da 31 (umano con direzione, dedicato a 40 Hz) a 2,4 (umano addestrato, dedicato a 10 Hz): il secondo è sotto 5, quindi lì è smentita. |
| P5 | **Non risolta.** A 250 m/s la differenza fra l'umano addestrato e la macchina è 375 m: sopra la soglia di smentita (300 m), sotto i 500 previsti. Con l'umano con direzione la differenza è 1,35 km. |

## 5. Proposte

- **tempo-reale-1.** Rivisita come stato: oltre 0,1 s senza misura, l'oggetto diventa «non osservato» e la zona
  cresce come v·T + a·T²/2.
  - **Meccanismo:** dopo un evento con detriti, la schiera attiva si satura.
  - **Previsione:** nel simulatore, con 20 frammenti e un tempo di fascio fisso, la quota di passi falsamente
    «osservati» va a zero.
  - **Smentita se** cresce la frazione di frammenti non contenuti nella zona.
- **tempo-reale-2.** Da dire nel video e nel documento: «il calcolo dedicato garantisce un caso peggiore
  sotto il millisecondo; la tempestività la fanno la rivisita del sensore e chi riceve l'avviso».
  - **Smentita da** una misura del nucleo compilato con un p99 sopra i 5 ms.
- **Dopo:**
  1. aprire i PDF segnati «NON APERTA», o sostituirli con fonti apribili;
  2. compilare il nucleo e misurarne mediana, p99 e massimo sulla macchina;
  3. provare tempo-reale-1 nel simulatore degli eventi E1–E5.
