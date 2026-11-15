# Prove del sistema a lunga portata (f15/11-prove)

`sciame-validazione`, 15-11-2026. **Tutto è simulazione** (simulatore `../10-simulatore/sim_lp.py`, schede di
02-sensori, moto dei dati pubblici di 01-dati): **niente è provato su un sensore fisico, niente è «validato».** Le
etichette di classe sono assegnate a mano dalla verità, perché il classificatore resta ai lavori futuri. Solo
osservazione e avviso.

## 0. In testa: cambi di stato e regole

- **Soglie scritte prima**, in `../10-simulatore/PREVISIONI.md` (2026-11-15T00:20:40). Ciò che ho notato dopo sta in § 5.
- **Il nucleo `movi_lp.py` non è stato modificato.** Lo provo in due modi. Nel modo **«interfaccia»** chiamo
  `mancato()` come dice la sua documentazione: per ogni traccia nel settore che non ha avuto un ritorno. Nel modo
  **«prudente»**, che è una mia proposta, `mancato()` si chiama solo se `avviso_spegnibile()` dice che **tutto**
  l'insieme di presenza è guardato libero.
- **Smentite principali:** P2 continuità (modo interfaccia), P3 precisione, P4 l'avviso contiene l'oggetto, P5 il
  libero sull'oggetto (A1 alta, S1), P6 falsi avvisi, P8 tempo di dichiarazione (A1, A2), P10 durata. Fra gli eventi:
  E1 ritardo e volume, E2 evento mai dichiarato, falsi eventi in E4 ed E5. Reggono P1 (salvo A2 min,
  A3, A4, S2), P7 (con una riserva sulla metrica), P9 e i semi.
- **Scarti dalla consegna.** Il modo prudente ha 50 passaggi, non 200. E1 ed E2 ne hanno 16 per configurazione,
  perché un passaggio con 60–100 frammenti costa 40–70 s; E3 ed E4 ne hanno 60, E5 300 a 5 m e 60 alle altre
  separazioni. La consegna di scenari_eventi.json chiedeva 1000 a 5 m.
  **P10 smentita: `rifai.sh` dura circa 35 minuti, non meno di 15.** Si misura in 642 s la parte principale, 494 s la
  prudente e 955 s gli eventi. Per stare nei 15 minuti: `sh rifai.sh 100 30 30 150 8 30`, non misurato.
- **Regole:** nessun file cancellato, niente rete, al più 8 processi di calcolo.

## 1. Come

- **Passaggi.** 200 per scenario e configurazione (modo interfaccia), 2400 in tutto. I semi sono
  `SeedSequence(20261115, spawn_key=(scenario, configurazione, passaggio))`: **2400 semi distinti e 2400 prime
  estrazioni distinte** (`risultati_lp_interfaccia.json`, campo `semi`). La verità ha una chiave sua ed è
  **appaiata** fra la configurazione minima e quella alta.
- **Cosa varia.** Comportamento del bersaglio a rotazione: nominale, rallenta (×0,3), si ferma 15 s, vira di 90°
  con a_lat della classe, torna indietro. Lo innesca l'ingresso nell'ombra del sensore principale; per il treno la
  virata è sostituita da «rallenta». Velocità × U(0,7; 1,2). Cooperazione presente, assente o intermittente, a
  rotazione. In A1 e A4 un passaggio su 7 ha il drone «C0» da 1,6·10⁻⁴ m². Un passaggio su 10 spegne per 15 s il
  sensore principale; un altro su 10 gli dà pioggia forte (radar) o abbagliamento (camera).
- **Configurazioni** («min» → «alta»):
  - **A1:** IRIS → IRIS + pannello a nord dell'edificio + camera EO + Remote ID.
  - **A2:** SCANTER → SCANTER + LiDAR AT128 su un secondo palo + ADS-B.
  - **A3:** radar d'aeroporto + ADS-B → in più IRIS, EO e Remote ID su un secondo sito a 2 km lungo il sentiero.
  - **A4:** radar 4D di bordo → radar 4D + AT128 + EO.
  - **S1:** radar 4D → radar 4D + AT128 + un secondo radar 4D sull'altro lato.
  - **S2:** Tele-15 → Tele-15 + radar 4D + AT128 sul lato opposto del binario.
- **Punto protetto per la tempestività** (ipotesi mia): il sito in A1, il mezzo in A2, l'aereo in A3, il portatore
  in A4, il punto di conflitto (0, 9) in S1, la testa della banchina (0, 12) in S2.
- **Regioni di previsione tarate su dati pubblici** (01-dati, livello 0,90). Si dividono **per scena**: le scene
  pari tarano, le dispari provano. Copertura sulla prova: multirotore 0,905–0,910 (n = 8155 per orizzonte), auto
  0,893–0,898, treno 0,878–0,898, aereo in avvicinamento 0,879–0,898. **Rullaggio 0,840–0,853**, sotto 0,90 con soli
  19 tratti: la regione del rullaggio è stretta.

## 2. Tavole (modo interfaccia, n = 200 per riga; [·] = Wilson 95 %)

**T1 — Tempestività e continuità.**

| Scen./conf. | d richiesta | traccia confermata a (mediana; p5) | avviso tempestivo | cicli nascosti senza regione | passaggi con ≥ 1 ciclo senza regione |
|---|---|---|---|---|---|
| A1 min | 806 | 949; 928 m | 200/200 [0,98; 1] | 1884/5676 = 0,33 [0,32; 0,34] | 64/200 [0,26; 0,39] |
| A1 alta | 806 | 963; 946 | 200/200 [0,98; 1] | 59/206 [0,23; 0,35] | 9/200 [0,02; 0,08] |
| A2 min | 147 | 125; 49 (confermata nel 54 %) | **50/200 [0,20; 0,31]** | 794/2368 [0,32; 0,35] | 14/200 |
| A2 alta | 147 | 303; 299 | 200/200 [0,98; 1] | 518/678 [0,73; 0,79] | 24/200 [0,08; 0,17] |
| A3 min | 3932 | mai (drone sotto 200 m) | **0/200 [0; 0,02]** | 13644/28063 [0,48; 0,49] | 67/200 |
| A3 alta | 3932 | 3432; 3391 | **0/200** (lo scenario parte a 2,5 km) | 119/23800 [0,004; 0,006] | 1/200 |
| A4 min | 126 | 209; 106 (confermata nel 57 %) | **100/200 [0,43; 0,57]** | 88/6675 [0,011; 0,016] | 3/200 |
| A4 alta | 126 | 207; 105 | **149/200 [0,68; 0,80]** | 180/2108 [0,07; 0,10] | 18/200 |
| S1 min | 67 | 106; 105 | 200/200 [0,98; 1] | 6737/11210 [0,59; 0,61] | 148/200 [0,68; 0,80] |
| S1 alta | 67 | 105; 93 | 200/200 | 5554/7528 [0,73; 0,75] | 126/200 |
| S2 min | 261 | 493; 490 | 186/200 [0,89; 0,96] | 1701/17531 [0,09; 0,10] | 28/200 |
| S2 alta | 261 | 493; 487 | 186/200 [0,89; 0,96] | 576/13075 [0,04; 0,05] | 62/200 |

**Nel modo prudente (n = 50) i cicli nascosti senza regione sono 0 in tutte e 12 le righe**
(`risultati_lp_prudente.json`: A1 min 0/1417, sup. 0,003; S1 min 0/2801; S1 alta 0/1885; A3 min 0/6963).
Tempestività: identica, salvo A4 min 32/50 e alta 43/50, S2 44/50 (campione diverso).

**T2 — Sicurezza.** Prima colonna: cicli nascosti con l'oggetto **fuori** dalla possibile presenza, o senza
avviso. Seconda: istanti in cui la cella dell'oggetto vero è «libera» (`stato_fuso`), contati ogni secondo.

| | fuori avviso: interfaccia | fuori avviso: prudente (n = 50) | «libero» sull'oggetto (interfaccia) |
|---|---|---|---|
| A1 min | 1894/5676 | **10/1417 [0,004; 0,013]** | 0/19494; C0 0/3306 |
| A1 alta | 59/206 | 0/50 | **436/19494 = 0,022 [0,020; 0,025]; C0 340/3306 = 0,10 [0,09; 0,11]** |
| A2 min / alta | 794/2368; 518/678 | 0/590; 0/173 | 0 su 18 000 per classe |
| A3 min / alta | 13644/28063; 158/23800 | 0/6963; 0/5950 | 0/27200 |
| A4 min / alta | 1023/6675; 223/2108 | **134/2025 = 0,066**; 2/573 | 0/9576; C0 0/1624 |
| S1 min / alta | 7061/11210; 5671/7528 | **141/2801 = 0,050; 75/1885 = 0,040** | **23/7800 = 0,003 [0,002; 0,004]; 30/7800** |
| S2 min / alta | 1917/17531; 1116/13075 | 52/4160; 24/3015 | 0/13400 |

**T3 — Precisione della zona dichiarata** (oggetto dentro la zona / zone dichiarate, al τ indicato; «z» = cicli
«previsto ampio», senza zona). Comportamento nominale e altri quattro insieme; modo interfaccia.

| | 2 s | 5 s | 10 s | 20 s |
|---|---|---|---|---|
| A1 min nominale / altri | 16/16; 44/47 | 29/30; 69/76 [0,82; 0,95] | 6/6; 52/55 | —; 39/39 |
| A3 min nominale / altri | **32/42 [0,61; 0,87]**; 92/124 | **30/42**; 105/144 [0,65; 0,80] | 25/36; 84/116 | 13/13; 36/36 |
| A3 alta altri | 208/220 [0,91; 0,97], z 198 | 146/148, z 100 | 130/130 | 75/75 |
| A4 min / alta altri | 3/10, z 253; 45/58 | 3/6, z 197; 33/36 | — | — |
| S1 min nominale / altri | **14/28; 29/91 [0,23; 0,42]** | **14/33; 25/99** | 7/11; 4/37 | — |
| S2 min nominale / altri | 40/42; 120/127 | 41/43; 123/128 | 40/42; 110/115 | 40/41; 100/108 |
| S2 alta nominale | 76/77 | 61/63 | 35/37 | **0/20 [0; 0,16]** |

**T4 — Altre misure (interfaccia).**

| | falsi avvisi (tracce confermate lontane > 200 m da ogni oggetto) per ora [sup. 95 %] | scambi d'identità (passaggi) | stessa identità al ritorno | perdita di un sensore: dichiarata; ritardo max | costo per ciclo: mediana; p95 peggiore |
|---|---|---|---|---|---|
| A1 min / alta | 3,8 [5,6]; **77,5** | 0/200; 0/200 | 128/200 = 0,64; 9/22 | 40/40; 3,5 s (giro 1 s); 3,6 s | 0,11; 4 ms / 10,2; 32 ms |
| A2 min / alta | 55; 91 | **87/200; 200/200** (metrica, § 3.6) | 12/37; 5/33 | 40/40; **5,3 s** (giro 1 s) | 0,13; 25 / 2,9; 14 |
| A3 min / alta | 23; 32 | 0/200 | — | 40/40; 13,2 s (giro 4 s) | 0,09; 3 / 5,4; 15 |
| A4 min / alta | **569; 672** | 0/200 | 5/34; 34/95 | 40/40; 1,1 s | 2,2; 10 / 4,1; 24 |
| S1 min / alta | **711; 1594** | 0/200 | 27/78 | 40/40; 1,0 s | 2,5; 14 / 11,1; **55** |
| S2 min / alta | 119; **909** | 0/200 | —; 29/123 | 20/20 e 40/40; 1,2 s | 0,5; 8 / 7,7; 36 |

## 3. Che cosa regge e che cosa cade

1. **Tempestività (P1).**
   - **Regge** con la configurazione alta in A1, A2 e S1: 200/200 [0,98; 1].
   - **Cade** in S2: 186/200 [0,89; 0,96], perché il treno «si ferma» o «torna indietro» prima di essere confermato
     nel 7 % dei casi.
   - **Cade** in A4 alta: 149/200 [0,68; 0,80]. Il radar 4D filtra il drone a velocità radiale piccola e il campo
     di 120° non copre il ritorno.
   - **Cade** in A2 min: 50/200 [0,20; 0,31]. Il radar di superficie da solo conferma tardi: mediana 125 m contro
     147.
   - **A3: 0/200 per costruzione.** Il drone parte a 2,5 km e ne servono 3,9.
   - In A3 min il radar d'aeroporto **non vede mai il drone** (quota minima 200 m). Questo è il caso «drone sotto
     la copertura», e il sistema lo dice solo se la configurazione lo dichiara.
   - Il drone C0 è tempestivo in A1 (29/29): IRIS lo vede entro circa 1 km e il sito è a 949 m.
2. **Continuità (P2): smentita nel modo interfaccia, regge nel modo prudente.**
   - In S1 min 148 passaggi su 200 perdono la regione durante l'ombra; in A1 min 64 su 200.
   - **Meccanismo**, dai diagnostici di `ins.eventi`: una sola passata mancata con Pd ≥ 0,99, valutata **nel punto
     previsto**, chiude la traccia («non più rilevata»). Il punto previsto esce dall'ombra prima dell'oggetto,
     perché ha la velocità vecchia; per lo stesso motivo una cella con il centro in vista ma l'oggetto in ombra
     conta come guardata.
   - È una **violazione del principio «l'avviso non si toglie se non guardando»** da parte dell'interfaccia di
     `mancato()`, che guarda un punto e non l'insieme.
   - Con la chiamata prudente si passa a **0 cicli su tutte le righe**: per esempio S1 min 0/2801, limite
     superiore 0,0014.
3. **L'avviso contiene l'oggetto nascosto (P4): smentita anche nel modo prudente**, in misura minore.
   - Restano A1 min 10/1417, A4 min 134/2025 = 0,066 [0,056; 0,078], S1 min 141/2801 = 0,050, S2 min 52/4160.
   - **Meccanismo**, visto in `MOVI_DIAG=1` su A1, passaggio 2: dopo l'ombra la porta della traccia è larga e
     accetta un **falso ritorno a 500 m**. La possibile presenza si ricentra lì e l'oggetto vero resta fuori.
   - Proposta in § 6.
4. **Il «libero» sull'oggetto (P5): smentita in A1 alta e in S1**, per due meccanismi che la regola del nucleo non
   vede.
   - **(a) S1, radar 4D:** il filtro Doppler toglie l'auto ferma o in moto trasversale, ma la griglia calcola la Pd
     come se la vedesse. Risultato: 23/7800 e 30/7800 istanti «liberi» su un'auto da 10 m², sopra la classe più
     piccola.
   - **(b) A1 alta, pannello a 10 Hz:** il ritorno, con σ = 3,25 m e 1°, cade nella cella vicina, e la cella vera
     senza ritorno è «libera». Risultato: 2,2 % per il drone nominale, 10 % per il C0.
   - Prevedevo violazioni solo per il C0 sotto la classe. **Il C0 da solo, col solo IRIS, non dà violazioni**
     (0/3306): con il giro di 1 s la finestra lato/v_max è più corta del giro e IRIS da solo **non dichiara quasi
     mai «libero»**. È prudente ma toglie informazione; la quota di celle libere non l'ho misurata (non verificato).
5. **Precisione (P3): smentita.**
   - **Regge** sui treni (S2 min 40/42 … 40/41) e in A3 alta (≥ 0,91).
   - **Cade** in A3 min nominale a 2 s: 32/42 [0,61; 0,87]. Il radar d'aeroporto a 4 s porta in zona un errore
     iniziale che la regione, tarata sullo stato vero, non contiene.
   - **Cade** in S1 a ogni τ (≤ 0,67): auto a 100 m con σ_az 0,3° e un comportamento di ombra breve; la zona del
     dato NGSIM (autostrada) non è quella di un incrocio.
   - **Cade** in S2 alta nominale a 20 s: 0/20. Il treno si ferma a fine corsa e la velocità costante lo porta
     oltre.
   - «Vira», «si ferma», «torna indietro» danno spesso «previsto ampio» (colonne z): non è un errore, è
     informazione in meno.
6. **Identità (P7).**
   - 0 scambi in A1, A3, A4, S1, S2 (0/200, sup. 0,019).
   - In **A2** persona e mezzo passano a 20–60 m l'uno dall'altra, e la mia associazione verità–traccia ha una
     porta di 60 m: i 200/200 scambi in alta sono in gran parte un **artefatto della metrica**. **Non risolto.** Lo
     decide una porta per classe di 3σ.
   - L'identità al ritorno è la stessa solo nel 15–64 % dei casi: il nucleo apre spesso una traccia nuova. È
     «presunta», come vuole la regola, ma **non va mostrata come continuità d'identità**.
7. **Falsi avvisi (P6): smentita.**
   - Sono 3,8 per ora con il solo IRIS e da 77 a 1594 per ora con radar 4D e LiDAR.
   - Il clutter uniforme (0,3 per quadro) a 5 Hz conferma tracce con M/N = 2/3 e una porta di velocità iniziale
     v_max/2 = 45 m/s.
   - **Sensibilità:** col valore del JSON (1 per quadro), su un passaggio di S1 alta, 117 tracce false contro 16.
     Su un solo passaggio è un'indicazione, non una misura.
8. **Perdita di un sensore (P8): smentita alla lettera.**
   - Dichiarata in 460 casi su 460 (Wilson [0,992; 1]).
   - Il ritardo arriva a 5,3 periodi per lo SCANTER (5,29 s con giro di 1 s) contro i 3 della soglia: si somma il
     silenzio dall'ultimo record (fino a 1 periodo), la latenza e il passo di uscita (0,5 s).
   - La dichiarazione per **pioggia** (fondo > +6 dB per 3 giri) arriva in ≤ 4,0 s.
9. **Costo (P9): regge.** Mediana ≤ 11 ms per ciclo in tutte le righe del modo interfaccia; il p95 peggiore è 55 ms
   (S1 alta, per le tracce false). Nel modo prudente la mediana arriva a 46 ms (S1 alta) e il p95 a 340 ms (A3 alta):
   **regge al limite, e solo in mediana.**

## 4. Eventi E1–E5 (`risultati_eventi.json`)

Strato eventi scritto da me in `eventi_lp.py` dalle regole di `regole_eventi.json`: stesso autore della prova, **non
indipendente**. Il volume V e l'impronta vengono da `frammenti.py` di 02-regole. «min» = solo il radar (E4: solo le
camere); «alta» = tutti i sensori dello scenario. [·] = Wilson 95 %.

| Misura (soglia scritta prima) | Esito |
|---|---|
| E1 evento entro 2,0 s (≥ 95 %) | min: dichiarato 11/16, entro 2 s **1/16 [0,01; 0,28]**, ritardo mediana 3,0 s (max 5,0); alta: **0/16 [0; 0,19]**. **Smentita** |
| E1 frammenti dentro V (≥ 0,999) | 35 960/36 660 = **0,981 [0,979; 0,982]**. **Smentita**: V parte da t_a, l'istante dichiarato, che arriva 3 s dopo l'urto vero |
| E1 celle «libere» nell'impronta | 0/9728 anche senza lo strato eventi (IRIS non dichiara libero, § 3.4). **Regge** |
| E2 camere non affidabili entro 3 cicli | 32/32, al più 3 cicli. **Regge** |
| E2 evento dichiarato, avviso al mezzo | **0/32 [0; 0,11]**: i frammenti (1,96·10⁻⁴ m²) non danno ritorni allo SCANTER e le camere sono abbagliate. L'avviso al mezzo **non parte**. **Smentita** |
| E3 portata utile = conto entro 5 % | uguale (drone 2801 m nebbia, 2000 m pioggia; aereo leggero 10 532 e 7523 m), ma **conto e nucleo usano la stessa formula: non è una prova indipendente**. Estensione reale del libero nella griglia: non misurata, **non verificato** |
| E3 celle libere oltre la portata utile | 0 su 4,2·10⁸ celle-ciclo. **Regge** |
| E3 «avviso non tempestivo» | mai necessario: R_utile ≥ d_avv (2000 ≥ 354; 7523 ≥ 1490) con i fattori prudenti di 01-effetti. **Non provata** |
| E3, E4 tracce perse senza avviso (0) | E3 0 su 1080 cicli nascosti; E4 0 su 900 (min) e 0 su 480 (alta). **Regge** |
| E4 eventi dichiarati (0) | min 0/60; alta **5/60 [0,04; 0,18]**: ritorni spuri presso la traccia scambiati per separazione. **Smentita** |
| E5 falsi eventi (0/1000 a 5 m) | 5 m: **1/300 [0,001; 0,019]**; 2 m: 0/60; 1 m: 2/60; 0,5 m: 0/60. **Smentita** (con 300 passaggi, non 1000); dove l'innesco cominci a scattare resta **non risolto** |

## 5. Che cosa cambia rispetto al corto raggio, dove il sistema cede, notato dopo

- **Cambia la grandezza che conta: non più i metri, ma i secondi di rivisita per la velocità.**
  - Con un giro di 4 s e 70 m/s l'oggetto si sposta di 280 m fra due illuminazioni.
  - Se la passata si data alla fine del giro, A3 dava celle «libere» sull'aereo (17 istanti per oggetto in un
    passaggio di prova). Datandola all'inizio del giro, scendono a 0/27 200.
  - **Notato dopo:** il nucleo non sa quando ogni cella è stata illuminata, e il chiamante deve dargli l'istante
    più vecchio.
- **Dove cede, in ordine di gravità.**
  - **(1)** L'avviso si spegne per una passata mancata in un punto: interfaccia di `mancato()`, § 3.2.
  - **(2)** Il «libero» ignora il filtro Doppler e lo spostamento del ritorno nella cella vicina (§ 3.4).
  - **(3)** Una misura falsa ricentra l'avviso (§ 3.3).
  - **(4)** Il drone sotto la copertura: il radar d'aeroporto non lo vede mai (A3 min). Il drone piccolo e lento per
    il radar 4D (A4) è filtrato dal Doppler.
  - **(5)** Il mezzo non cooperante: la tempestività non cambia fra presente, assente e intermittente in nessuno
    scenario (es. A2 alta 67/67, 67/67, 66/66). Qui i cooperativi non aiutano, ma non sono nemmeno serviti, perché i
    sensori non cooperativi bastavano. Non ho provato un caso in cui il cooperativo sia l'unico sensore.
  - **(6)** La rivisita lenta: precisione di A3 min.
  - **(7)** Virate e fermate: molti «previsto ampio» e la caduta di S2 alta a 20 s.
- **Notato dopo:** la camera orientata dal radar usa l'associazione vera (ottimista); la regione di S1 viene da
  dati di autostrada; nel controllo «libero» uso le stesse griglie del sistema, quindi la prova condivide con esso
  la geometria a celle, ma non la linea di vista esatta, che viene dal simulatore.

## 6. Stati proposti e proposte

- **Stati.**
  - «Il nucleo a lunga portata mantiene l'avviso durante l'occlusione»: **smentito** con l'interfaccia di
    `mancato()`; **sostenuto dai dati** (n = 50 per riga) con la chiamata prudente.
  - «Il libero non contiene oggetti di classe ammessa»: **smentito** per il radar 4D e per il pannello; **sostenuto
    dai dati** per IRIS, SCANTER, radar d'aeroporto e LiDAR.
  - «Simulatore conforme al suo modello»: **verificato** su V1–V6.
  - Tutto il resto: simulazione, nessun sensore fisico.
- **validazione-1, `mancato` sull'insieme.** Meccanismo: l'evidenza d'assenza conta solo se `avviso_spegnibile` è
  vero. Previsione: 0 cicli senza regione con n = 200. La smentisce un ciclo senza regione con oggetto nascosto.
- **validazione-2, cella ombra se un qualunque vertice è in ombra, e Pd zero sotto la soglia Doppler.** Previsione:
  «libero» sull'oggetto 0/7800 in S1. La smentisce un istante libero sull'auto.
- **validazione-3, porta dopo l'ombra limitata all'insieme raggiungibile più 3σ della misura, e conferma da due
  passate** prima di ricentrare. Previsione: fuori avviso ≤ 1/1000 in A1, A4, S1 nel modo prudente. La smentisce
  un caso.
- **Dopo:** rifare con 200 passaggi nel modo prudente, una prova su registrazioni pubbliche di rilevazioni (non ne
  esistono in 01-dati) e una revisione indipendente del simulatore.
