# MoVi · ARCO NUOVO DEL VIDEO: volo ad alta velocità — `sciame-comunicazione`, f17-video/60-arco-volo

Cominciato il 2026-11-15T04:36:13+01:00 (`date -Is`). Previsioni scritte prima, alle 04:37:42, in `PREVISIONI.md`.
Accanto ci sono `voce_en_v3.txt` e `voce_it_v3.txt`, un paragrafo per scena nel formato di `kokoro_tts.py`. Sostituiscono
la v2 di `22-sintesi/` solo per l'arco. Il resto di PIANO_VIDEO (griglia, palette, regole d'onestà, QA) resta valido.

## 0. In testa: cambi di stato e regole

- **Scritture:** solo in questa cartella, con tre file nuovi e `PREVISIONI.md`. Nessun file cancellato, niente git,
  niente sudo, niente rete.
- **Indipendenza:** sono il ruolo che aveva scritto `10-messaggio`. Le cifre le ho prese dai verdetti 2C e FASE2. Ho
  ricalcolato solo gli intervalli di Wilson e le coperture per mezzo da `21-statistica/ridivisione`, con codice mio,
  sugli stessi record dell'autore.
- **Non disponibili alle 04:39:** `f19-volo/03-confidenza` e `04-scenari` sono vuote, `02-sensori-hw` ha solo le
  previsioni. Per questo la curva della confidenza, la latenza e gli scenari in volo restano **segnaposto**.
- **Da sapere subito (cambia ciò che si può dire):**
  1. Il 51/60 della collisione (E1 v3) viene da droni **sul sito**, a 15–21 m/s, non in volo veloce. A schermo va il
     dominio «E1 · site drones · sim.», finché `f19-volo/04-scenari` non lo rimisura a velocità di volo
     (segnaposto E1V).
  2. La fiammata con le camere accecate (E2) è **in rullaggio o in corsa di decollo**, non «in salita». La voce dice
     «in the climb» **solo se** `04-scenari` dà l'E2 in volo (variante al §3).
  3. Per gli aerei in volo l'avviso all'operatore di sito **non è tempestivo**: servono 3410 m, il «libero» arriva a
     2360 m (VERDETTO_FASE2 §1). È il limite che cambia il giudizio, e la voce lo dice nella scena 9.

## 1. Messaggio

- **In una frase (EN):** *When a fast aircraft or drone is lost from view, after a collision, a flash or smoke, MoVi
  does not go blank: it shows where the vehicle can be and how its confidence decays second by second, computed and
  checked on real flight trajectories.*
- **In una frase (IT):** *Quando un aereo o un drone veloce sparisce alla vista, dopo una collisione, una fiammata o il
  fumo, MoVi non si spegne: mostra dove il mezzo può essere e come la confidenza scende secondo per secondo, una curva
  calcolata e verificata su traiettorie di volo reali.*
- **Da ricordare se resta una sola immagine:** la zona che si allarga e, accanto, la curva che scende fino alla linea
  «I don't know».
- **In trenta secondi:** le scene 1, 6 e 9.
- **Pubblico:** una giuria mista. Ai non tecnici bastano la forma della curva e la linea del «non lo so». Ai tecnici
  servono la formula, la banda di Wilson e il dominio, a schermo in 22 px.
- **Tagline:** invariata, «Seen, not seen, unknown: declared for every track.»

## 2. Le nove scene (174 s; voce EN 326 parole, stimate a 125 parole al minuto)

Etichetta d'onestà come nel piano §2: `SIMULATION · …` solo se l'inquadratura è disegnata da un registro, altrimenti
`SCHEMATIC`.

| # | Tempo | Durata | Parole EN (stima) | Che cosa si vede | Componenti (nuovi in **grassetto**) | Dato · etichetta |
|---|---|---|---|---|---|---|
| 1 | 0:00–0:14 | 14 s | 26 (12,5 s) | Titolo 0–3 s. Due viste: **pianta** a sinistra e **quota** a destra (profilo distanza–altezza). Tre **tracce veloci** con scia: un ala fissa, un aereo in salita, due multirotori che convergono. A 0:09 le due tracce si toccano, la verità mostra il lampo piatto bianco e la nube grigia; tutti i glifi EO e IR si barrano insieme. Fermo sull'immagine al «now?» | TitoloMarchio, VeritaSim, PiantaArea, Sensori, Traccia, **VistaQuota**, **ScieVeloci**, FasceOnesta | anteprima di R-V4 (scena 6) e R-E1; SCHEMATIC finché non ci sono |
| 2 | 0:14–0:34 | 20 s | 38 (18,2 s) | Come la scena 2 del piano, accorciata: tre segni, `EMPTY` barrato. Niente fascia lunga | ScenaSchema, Traccia, Regione, PossibilePresenza | SCHEMATIC |
| 3 | 0:34–0:49 | 15 s | 28 (13,4 s) | Pianta e quota affiancate. I sensori si accendono uno alla volta; in quota si vedono i **ventagli in elevazione** e il buco sotto il fascio del radar. Riga a schermo: `sensors modelled from data sheets · state-of-the-art options: see technical annex` | PiantaArea, Sensori, VentaglioSettori, **VistaQuota** (settori in elevazione) | `parametri_lunga_portata.json` · SCHEMATIC |
| 4 | 0:49–1:10 | 21 s | 40 (19,2 s) | Le tracce dei due droni si uniscono in `UNRESOLVED TRACKS`; nessun impatto disegnato. `EVENT: CONTACT · INFERRED`, con sotto `inferred from: track merge + new returns`. Si apre il **volume dei detriti**: in pianta righe ocra con i raggi passati, in quota il **cono di caduta** fino al suolo, senza punti dentro. Contatore: `contact declared ≤ 2 s: 51 / 60 · 95 % [0.74; 0.92] · E1 · site drones · sim.` e `delay 1.2–1.8–2.3 s`. Raggio: `debris radius 3.1–4.5–5.3 km (60 runs, sim.)` | VolumeDetriti (+ sezione in quota), ConsoleTracce, Tabellone, **VistaQuota** | R-E1 da `lp_E1_v3`: evento SIMULATION, zona dei detriti solo SCHEMATIC (VERDETTO_2C §5; K-614) |
| 5 | 1:10–1:29 | 19 s | 35 (16,8 s) | Aereo: lampo piatto sul motore, `FLASH · schematic`; nube a puntini che copre la vista, `NOT OBSERVED · SMOKE (EO, IR)`. In console le **bande di affidabilità** corallo `RELIABILITY LOST · EO` e `· IR` entro 3 cicli; l'aereo `SEEN (RADAR ONLY)`; riga obbligatoria `radar response to flash: NOT VERIFIED`. Contatore `cameras declared unreliable ≤ 3 cycles: 30 / 30 · [0.89; 1] · optimistic trigger` | VeritaSim, Nube, BandaAffidabilita, ConsoleTracce, Sensori | R-E2 da `lp_E2_v3`: SIMULATION solo per le camere (VERDETTO_2C §5) |
| 6 | 1:29–1:54 | 25 s | 47 (22,6 s) | **Momento chiave.** Il radar perde l'aereo (o il drone ad ala fissa): `NOT SEEN · t s`. In pianta e in quota la zona si allarga con la scia del passato. Nel terzo destro il **grafico della confidenza nel tempo**: asse x 0–30 s, asse y 0–1; la curva **calcolata** è una linea piena; i punti **misurati sulle traiettorie pubbliche** a 2, 5, 10, 20 e 30 s hanno la loro banda di Wilson; una linea orizzontale tratteggiata alla soglia `[CIFRA-C0]`. Quando la curva la incrocia, la traccia passa a `WIDE ZONE · I DON'T KNOW` e il grafico segna `t* = [CIFRA-C1] s`. Riga di dominio: `public ADS-B and UAV logs · sensor noise simulated · samples correlated per trajectory` | Traccia, Regione, **VistaQuota**, **CurvaConfidenza**, FasceOnesta, ConsoleTracce | R-V4 (nuovo, §4) e la curva di `f19-volo/03-confidenza`; SIMULATION + `PUBLIC TRAJECTORIES` |
| 7 | 1:54–2:15 | 21 s | 39 (18,7 s) | **Barre della latenza**, dalla cattura all'avviso, impilate: rivisita del sensore, elaborazione, rete, reazione dell'operatore. Due righe: `laptop (measured)` e `dedicated hardware (estimated)`; il pezzo dell'elaborazione si accorcia di `[CIFRA-L3]×`, il resto no. Sotto, a 22 px: `analogy: [FONTE-HW] · estimate, not a measurement`. Poi una riga: `warning distance at 250 m/s: +[CIFRA-L4] m (calc.)` | **BarreLatenza**, Tabellone | `f19-volo/02-sensori-hw` · SCHEMATIC, `ESTIMATE` |
| 8 | 2:15–2:31 | 16 s | 30 (14,4 s) | Mosaico a tre riquadri, 5 s ciascuno: sito con drone dietro l'hangar e aereo in rullaggio (`200 / 200 · [0.98; 1] · sim.` per ciascuno); persona dietro un pannello (corto raggio); `presence warning for a blind person · does not replace a cane or guide dog` | ConsoleTracce, Regione, PossibilePresenza, FasceOnesta | `lp_A1_v3`, `lp_A2_v3`, registri corti · SIMULATION; per la persona nessuna cifra |
| 9 | 2:31–2:54 | 23 s | 43 (20,6 s) | 0–12 s: i limiti una riga alla volta. A destra la scala **«from prototype to deployed system»** su tre gradini: `state-of-the-art sensors` → `dedicated hardware` → `field trials on real sensors`, ciascuno con il suo «what it fixes». Dal secondo 12: simbolo SDMs, wordmark, tagline, `Observes and warns · no output is a command`, crediti, 0,5 s di nero | ScenaSchema, CatenaBlocchi (riusata come scala), TitoloMarchio, Crediti | verdetti · SCHEMATIC |

**Totale: 174 s** (fra 168 e 175). **Margine voce–scena:** da 1,5 a 2,4 s per scena. Il passo è quello stimato da
VOCE_GUIDA (125 parole al minuto con bm_george 1.0); il margine **non è misurato**: va rifatto sul `.tempi.json`.
Se una scena sfora, si taglia in quest'ordine, senza mai accelerare la voce:
1. scena 3, «seen from above and from the side» (lo mostra l'immagine);
2. scena 1, «A fixed-wing drone at speed.»;
3. scena 8, «people at short range» (resta a schermo).

Le scene 6 e 9 non si tagliano.

**Italiano** (351 parole, circa 156 s a 135 parole al minuto, non misurato): sforano le scene 7 (48 parole in 21 s) e
1. Si applicano subito i tagli 1 e 2. Nella scena 7 si toglie «costruiti per un solo compito».

## 3. Voce EN con l'IT accanto

| # | EN | IT |
|---|---|---|
| 1 | A fixed-wing drone at speed. An aircraft climbing out. Two drones collide. A flash, smoke, and every camera goes blind. What should the screen say now? | Un drone ad ala fissa, veloce. Un aereo in salita dopo il decollo. Due droni si scontrano. Una fiammata, il fumo, e ogni camera diventa cieca. Che cosa deve dire lo schermo, adesso? |
| 2 | MoVi declares what it has not observed. Three answers per track. I see it. I don't see it: here is where it can be. Or: I don't know. What it has not observed, it marks unverified, never empty. | MoVi dichiara ciò che non ha osservato. Tre risposte per ogni traccia. Lo vedo. Non lo vedo: ecco dove può essere. Oppure: non lo so. Ciò che non ha osservato lo segna non verificato, mai vuoto. |
| 3 | Radar, LiDAR, visible and thermal cameras, and what aircraft broadcast. All modelled from public data sheets, seen from above and from the side, each with its blind spots. | Radar, LiDAR, camere visibili e termiche, e ciò che trasmettono gli aerei. Tutto modellato dalle schede tecniche pubbliche, visto dall'alto e di lato, ciascuno con i suoi punti ciechi. |
| 4 | Two drones collide at speed. MoVi infers the contact from the tracks and new radar returns: in fifty-one of sixty simulated collisions, within two seconds. A debris zone opens, about four and a half kilometres in radius, never called empty. | Due droni si scontrano in velocità. MoVi deduce il contatto dalle tracce e dai nuovi ritorni radar: in cinquantuno collisioni simulate su sessanta, entro due secondi. Si apre una zona dei detriti di circa quattro chilometri e mezzo di raggio, mai detta vuota. |
| 5 | An engine fails in the climb: a flash, then smoke. The cameras go blind, and MoVi says so within three cycles, in every simulated run. In the model, the radar alone still holds the aircraft. | Un motore ha un'avaria in salita: una fiammata, poi il fumo. Le camere diventano cieche, e MoVi lo dice entro tre cicli, in ogni prova simulata. Nel modello, il solo radar tiene ancora l'aereo. |
| 6 | Now continuity is lost. MoVi keeps the track, shows where the aircraft can be, and how far to trust that zone, second by second. Computed, then checked on public flight trajectories: after [CIFRA-C1] seconds, confidence is [CIFRA-C2]. Below the line: I don't know. | Ora la continuità si perde. MoVi tiene la traccia, mostra dove l'aereo può essere e quanto fidarsi di quella zona, secondo per secondo. Calcolata, poi verificata su traiettorie di volo pubbliche: dopo [CIFRA-C1] secondi, la confidenza è [CIFRA-C2]. Sotto la linea: non lo so. |
| 7 | On a laptop, our processing takes [CIFRA-L1] per cycle. Chips built for one job, like those now serving language models far faster than GPUs, suggest [CIFRA-L2]: an estimate. Sensor and operator still dominate the delay. | Su un portatile, la nostra elaborazione richiede [CIFRA-L1] per ciclo. I chip costruiti per un solo compito, come quelli che oggi servono i modelli linguistici molto più in fretta delle GPU, fanno stimare [CIFRA-L2]: una stima. Il ritardo resta dominato da sensore e operatore. |
| 8 | Slower cases too: drones and taxiing aircraft, warned in time in two hundred of two hundred simulated runs each; people at short range; a warning aid for a blind person. | Anche i casi più lenti: droni e aerei in rullaggio, avvisati in tempo in duecento prove simulate su duecento, per ciascuno; persone a corto raggio; un aiuto di avviso per una persona non vedente. |
| 9 | The limits. Everything is simulated: no physical sensor, classes labelled by hand. Debris zones do not shrink by looking. For aircraft in flight, the warning still comes too late. Next: state-of-the-art sensors, dedicated hardware, field trials. MoVi. It observes and warns. By SDMs. | I limiti. È tutto simulato: nessun sensore fisico, classi etichettate a mano. Le zone dei detriti non si restringono guardando. Per gli aerei in volo, l'avviso arriva ancora troppo tardi. Poi: sensori allo stato dell'arte, hardware dedicato, prove sul campo. MoVi. Osserva e avvisa. Di SDMs. |

**Varianti obbligate dai dati:**
- Se `04-scenari` **non** dà E2 in volo, nella scena 5 si dice «An engine fails on the take-off run: a flash, then
  smoke.» / «Un motore ha un'avaria in corsa di decollo: una fiammata, poi il fumo.», e nella scena 1 «An aircraft on its
  take-off run.»
- Se E1V (la collisione a velocità di volo) arriva, nella scena 4 «in fifty-one of sixty» si sostituisce con la cifra
  nuova, **solo se** il limite inferiore di Wilson è almeno 0,70. Sotto 0,70 resta il 51/60 con il dominio «site drones».
- Se la latenza dedicata con hardware **e** sensore allo stato dell'arte rende tempestivo l'avviso in volo, per calcolo,
  nella scena 9 la frase diventa «For aircraft in flight, the warning still comes too late with today's sensors;
  faster ones close the gap, by calculation.» (+7 parole: si toglie allora il taglio 3). Altrimenti resta com'è.
- Se C1 o C2 non arrivano, la frase «Computed, then checked…» si riduce a «Computed from the motion model, and still to be
  checked.» La scena 6 perde i punti misurati e tiene solo la curva calcolata, con la scritta `NOT YET CHECKED ON DATA`.

## 4. Segnaposto (si riempiono o si tolgono prima di Kokoro; mai un aggettivo al posto di una cifra)

| Segnaposto | Misura che serve | Da chi | Stato atteso | Se manca |
|---|---|---|---|---|
| CIFRA-C0 | La soglia di confidenza sotto cui la traccia passa a «non lo so» (proposta: 0,90, cioè il livello del registro) | `f19-volo/03-confidenza` | regola di progetto | 0,90, scritto `design threshold` |
| CIFRA-C1 | Il tempo t* in cui la confidenza calcolata scende sotto C0, per classe (aereo in salita, ala fissa senza pilota), con le ipotesi del modello di moto | 03-confidenza | **calcolato** (forma chiusa o metodo) | la frase si riduce (§3) |
| CIFRA-C2 | La confidenza **misurata** a quell'orizzonte sulle traiettorie pubbliche: k/n, Wilson 95 %, con n delle traiettorie indipendenti dichiarato | 03-confidenza, con il riconto dell'arbitro | **su dati pubblici** (rumore del sensore simulato) | come C1 |
| Curva | La curva calcolata c(t) e i punti misurati a 2, 5, 10, 20, 30 s, per classe | 03-confidenza | calcolato e su dati pubblici | solo la curva calcolata, `NOT YET CHECKED ON DATA` |
| R-V4 | Il registro di una perdita di continuità in volo, con la zona e il campo `confidenza(t)` per riga | prototipo, `f19-volo/04-scenari` | simulazione | scena 6 SCHEMATIC, alimentata dalla sola curva |
| E1V | La collisione dichiarata entro 2 s a velocità di volo, k/n e Wilson | 04-scenari | simulazione | resta 51/60 con il dominio «site drones» |
| CIFRA-L1 | L'elaborazione per ciclo del modo lungo sul portatile, con la macchina, mediana e p99 | 02-sensori-hw (P1: fra 0,1 e 55 ms) | misurato (software) | si toglie la frase L1; resta la barra senza cifra |
| CIFRA-L2 / L3 | L'elaborazione per ciclo e il fattore su FPGA o ASIC, per analogia | 02-sensori-hw (P2: fra 10× e 100×) | **ipotesi / stima per analogia** | si toglie la frase; la barra dedicata non si disegna |
| FONTE-HW | La fonte pubblica dell'analogia: un acceleratore dedicato recente, con il fattore dichiarato dal produttore o misurato da terzi | 02-sensori-hw, con link | fonte | senza fonte, niente L2 |
| CIFRA-L4 | La distanza d'avviso guadagnata a 250 m/s con la catena dedicata (P5 di 02-sensori-hw) | 02-sensori-hw | calcolato | si toglie la riga |

**Candidati già nei file, da passare al riconto dell'arbitro e non ancora da usare.** Li ho ricalcolati io dalla
ridivisione: frazione dei casi in cui la zona tarata, a livello nominale 0,90, contiene il mezzo, con Wilson 95 %, su
dati pubblici con il rumore del sensore simulato. I casi dentro una stessa traiettoria sono correlati, quindi il vero
n è il numero delle traiettorie:
- **ala fissa senza pilota** (25 traiettorie): a 2 s 209/244 [0,81; 0,90], a 10 s 130/214 [0,54; 0,67], a 30 s 90/149
  [0,52; 0,68]. È una curva che scende, quindi la candidata naturale per la scena 6;
- **aereo in decollo** (15 traiettorie): a 2 s 105/123 [0,78; 0,91], a 30 s 82/107 [0,68; 0,84];
- **multirotore** (98 traiettorie): a 30 s 784/800 [0,97; 0,99].

Lo stesso file segna anche `fuori_avv` = 80/107 per il decollo a 30 s. Va capito che cosa conta (fonte:
`21-statistica/ridivisione/risultati_traiettorie.json`).

## 5. Componenti

- **Riusati** (COMPONENTI §2): Traccia, Regione, PossibilePresenza, VolumeDetriti, Nube, BandaAffidabilita,
  ConsoleTracce, VentaglioSettori, Tabellone, CatenaBlocchi, VeritaSim, FasceOnesta, ScenaSchema, TitoloMarchio,
  Sottotitoli. Valgono le correzioni di REVISIONE_VISIVA §3: `NOT COUNTED` sopra i sottotitoli, le etichette sopra le
  righe ocra.
- **Nuovi:**
  1. **`VistaQuota`**: profilo distanza–altezza, in scala comune con la pianta (tacca grafica), che riusa i
     proiettori. Disegna le tracce, la zona come intervallo verticale tratteggiato, i ventagli in elevazione, il cono
     di caduta dei detriti e la nube. Legge `tracce[].pos[2]` e `regione.quota_min/max` (campi da concordare con
     l'architetto).
  2. **`ScieVeloci`**: scia di 3 s dietro una traccia vista, con un'opacità che cala. Mai una scia nel futuro: il
     futuro è solo la zona tratteggiata.
  3. **`CurvaConfidenza`**: il grafico di 560×360 px. La curva calcolata è piena (#AEB8C5); i punti misurati sono
     cerchi vuoti con la barra di Wilson; la soglia C0 è tratteggiata; un cursore verticale segue il tempo della
     scena; a destra la scritta `t* = … s`. Legge `confidenza(t)` dal registro, oppure un JSON di `03-confidenza`.
     Niente ombre né riempimenti che suggeriscano una certezza.
  4. **`BarreLatenza`**: due barre impilate con i quattro segmenti etichettati. Il segmento stimato è a righe con la
     scritta `ESTIMATE`; la scala è lineare in ms. Se i rapporti sono di ordini di grandezza, si usa un riquadro
     d'ingrandimento sul segmento dell'elaborazione, non una scala logaritmica.
- **Palette:** invariata. La curva non usa tinte fra 90° e 160° (Q11).

## 6. Tabella «che cosa diciamo, con quale forza, con quale prova»

| Frase (EN, voce o schermo) | Forza | Stato | Prova |
|---|---|---|---|
| contact inferred within 2 s in 51 of 60 | incoraggiante: limite inferiore 0,74, sotto la soglia 0,90 del progetto | simulato (E1 v3, droni del sito) | VERDETTO_2C §1, `passaggi_v3.jsonl` |
| debris zone about 4.5 km in radius | misurato | simulato (3,1–4,5–5,3 km, 60 prove) | idem |
| never called empty | per regola, con la mappa non dichiarata | per costruzione e simulato | VERDETTO_2C §1, X5 |
| cameras declared blind within 3 cycles, every run | sostenuto: 30/30 [0,89; 1] (v3), 90 (v2) | simulato, con l'innesco ottimista | VERDETTO_2C §3 n. 8 |
| radar alone still holds the aircraft | solo nel modello | ipotesi del modello (`radar response to flash: NOT VERIFIED`) | piano §2, scena 6 |
| confidence curve, t*, measured points | calcolato più dati pubblici | in arrivo | 03-confidenza |
| processing on laptop / dedicated | misurato / stima per analogia | in arrivo | 02-sensori-hw |
| sensor and operator dominate the delay | atteso (P1 e P4 di 02-sensori-hw) | **ipotesi finché 02 non lo calcola**; se smentita, la frase si toglie | 02-sensori-hw |
| 200 of 200, drones and taxiing aircraft | sostenuto: [0,981; 1] ciascuno | simulato (A1 v3, A2 v2) | VERDETTO_2C §1, §3 n. 1–2 |
| for aircraft in flight, the warning still comes too late | limite | calcolato (3410 m contro 2360 m) | VERDETTO_FASE2 §1 |

**Da non dire** (VERDETTO_2C §4, ancora validi): validated, real time, certifiable, detect and avoid, «always», «zero
false alarms», «the footprint shrinks by looking», «warns only those in danger», il lessico d'ingaggio. Ho controllato
con grep la voce EN per 14 voci di quell'elenco: 0 occorrenze.

## 7. Domande attese, con risposte

1. *«51 su 60 non basta per la sicurezza.»* No, e lo diciamo: è un prototipo di un giorno, con il limite inferiore a
   0,74. Le nove prove fuori dai 2 s hanno un ritardo fino a 2,3 s, non sono mancate. Che cosa migliorare (e
   come) va scritto nell'allegato.
2. *«La curva è vera o disegnata?»* È calcolata dal modello di moto, e i punti sono misurati su traiettorie pubbliche,
   con il rumore del sensore simulato. Nessun sensore fisico.
3. *«Con un chip dedicato siete tempestivi in volo?»* La risposta onesta è la scena 7: si accorcia l'elaborazione, ma
   domina la rivisita del sensore; in volo serve anzitutto più portata. Cifre in arrivo da `02-sensori-hw`.
4. *«Chi prende le decisioni?»* L'operatore. MoVi osserva e avvisa, e nessuna uscita è un comando.

## 8. Stati delle previsioni (PREVISIONI.md)

- P1 **regge**: 326 parole, fra 280 e 330.
- P2 **regge**: 174 s.
- P3 **regge dopo una correzione**: la prima stesura aveva la scena 7 a 1,3 s di margine, poi ho tagliato due parole.
  Ora i margini vanno da 1,5 a 2,4 s. È stima, non misura.
- P4 **regge** sulla voce EN.
- P5 **regge**: 163 parole su 326 (50 %) stanno nelle scene 4–7.
- P6 **regge**: 16 s.

## 9. Che cosa propongo dopo

1. Appena `03-confidenza` consegna, riempire C0, C1, C2 e la curva. Una cifra entra solo con l'intervallo e il numero
   delle traiettorie indipendenti.
2. Mettere i segnaposto in `cifre.json` (v8, accanto alla v7) e generare la voce v3 con `kokoro_tts.py`. Poi
   ricontrollare i margini sul `.tempi.json`.
3. Costruire VistaQuota e CurvaConfidenza per primi, perché portano la scena chiave. BarreLatenza è semplice.
4. Chiedere all'arbitro un riconto indipendente dei candidati del §4 e chiarire `fuori_avv` sul decollo.
