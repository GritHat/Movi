# MoVi · PIANO DEL VIDEO (unico e vincolante) — `sciame-videomaker`, f17-video/22-sintesi

Cominciato il 2026-11-15T00:34:05+01:00 (`date -Is`). Sintesi convergente delle tre proposte (`10-messaggio`, `11-marketing`,
`12-regia`) con la lettura (`20-lettura/LETTURA.md`) e l'attacco (`21-attacco/ATTACCO_VIDEO.md`). Da qui in poi le tre
proposte valgono solo dove questo piano le richiama. Accanto: `voce_en_v2.txt` e `voce_it_v2.txt` (il testo del §3, un
paragrafo per scena, nel formato di `kokoro_tts.py`).

## 0. Cambi di stato e regole

- **Scritture:** questo file, `voce_en_v2.txt` e `voce_it_v2.txt` in `22-sintesi/`. In `video/marchio/` ho scritto **solo
  file nuovi**: `sdms_{logo,simbolo}{,_mono,_mono_scuro}_v3.svg` (anello interno tolto), le stesse in `_v3b` (zona
  ellittica) e `tavola_controllo_v3.png`. Nessun file cancellato o sovrascritto (`cp -n`). Niente git, niente sudo, niente
  rete. Una copia di lavoro della tavola sta nella scratchpad.
- **Controlli fatti:** `xmllint` sui 12 SVG nuovi: 0 errori. Resa con `rsvg-convert` a 168 px e a 32 px; tavola guardata.
  Verde (tinta 90–160°, saturazione > 0,3): **0 pixel** sulla tavola v3. Parole della voce contate con `awk` (§3).
- **Previsioni:** quelle sui segnaposto sono dell'attacco (§3 dell'attacco, scritte alle 00:44 prima del verdetto) e qui si
  adottano senza cambiarle. Le mie scelte sul logo sono un'osservazione fatta dopo aver guardato la tavola, non una previsione.
- **Indipendenza:** sono lo stesso ruolo che ha scritto la proposta di regia `12-regia`. Ho corretto quella proposta
  seguendo critiche altrui, ma non posso vedere i suoi difetti che né la lettura né l'attacco hanno visto. Serve Q29.
- **Non letti:** la proposta `.tex` v1.0 e l'allegato (il nucleo a corto raggio mi arriva dalle istruzioni e dalle
  proposte); di `ISTRUZIONI_VIDEO_UTENTE.md` ho letto §3, §4, §5, §6, §7, §8 e §11, non §1, §2, §9, §10 e §12.
  `30-verdetto/` alle 00:38 **non esiste**.
- **Da dire all'utente:**
  1. Il nome «MoVi» somiglia a «MōVI» (Freefly, stabilizzatori di camera anche per droni). Lo stato del marchio **non è
     verificato** (attacco, 22).
  2. «Napoli» nei titoli non è verificato.
  3. La pronuncia di «MoVi» resta `[DA FORNIRE]`. La grafia «Movee» per Kokoro non è provata.

## 1. Messaggio, tagline, titoli (scelti)

- **Messaggio (EN):** *MoVi declares what it has not observed: for every tracked aircraft or drone it says "I see it", "I
  don't see it: here is where it can be" or "I don't know", marks what it has not observed as unverified, never empty,
  and says when it can no longer be trusted. Everything here is simulated from public data sheets.*
- **Messaggio (IT):** *MoVi dichiara ciò che non ha osservato: di ogni aereo o drone seguito dice «lo vedo», «non lo vedo:
  ecco dove può essere» oppure «non lo so»; ciò che non ha osservato lo segna non verificato, mai vuoto; e dice quando
  non ci si può più fidare di lui. Tutto qui è simulato dalle schede tecniche pubbliche.*
- **Tagline:** **"Seen, not seen, unknown: declared for every track."** / «Visto, non visto, non so: dichiarato per ogni
  traccia.»
  - È la T1 di K corretta come chiede l'attacco (correzione 2): via «always», via «unseen» (lettura 15), «per ogni traccia»
    al posto dell'universale.
  - Stato: **per regola (C)**, per il formato del registro, che dà uno stato a ogni traccia in ogni riga (`valida_riga`).
  - Non vale per gli oggetti mai rilevati (attacco, 1): per loro il video dice «non verificato» sulle celle, mai «non lo so».
- **Frase chiusa in voce sul «vuoto»:** solo nella scena 2, nella forma «What it has not observed, it marks unverified,
  never empty».
  - Le formule «…unless it has looked» non si usano: sono smentite come formulate (attacco, 2).
  - «Libero» a schermo compare solo come `OBSERVED EMPTY · class · to d m`, e solo dove il registro lo dichiara.
- **Titolo di apertura, 0:00–0:03, sovrapposto al piano d'insieme della scena 1:**
  - wordmark MoVi alto 120 px;
  - sotto, Inter 600 da 44 px: «A prototype that declares what it has not observed» (9 parole);
  - riga JB Mono da 24 px: `SDMs · The Big Hack 2026 · simulation and schematics only`.

  Entra nei 12 s della scena 1 (attacco, 12), mentre la voce comincia a 0:00.
- **Titolo del file e del caricamento:** «MoVi: a prototype that declares what it has not observed (SDMs, The Big Hack
  2026)».
- **Titoli di coda, dentro la scena 9, 3 righe** (lettura, 7):
  1. `MoVi · Team SDMs`;
  2. i cinque nomi su due righe;
  3. `Voice: synthetic (Kokoro) · music, fonts, sources: see description`.

  I crediti completi vanno nella descrizione (§8). Il cartello dei limiti di K si toglie: lo sostituisce la scena 7.

## 2. Le scene (172 s)

Scaletta unica: quella di M, riconciliata con R e allungata di 1 s nella scena 2.

L'etichetta d'onestà sta **in alto a destra, per tutta la scena**, e la stampa il componente `FasceOnesta`
(`creativo-videomaker-2`, reso obbligatorio):
- `SIMULATION · SENSORS MODELLED FROM DATASHEETS` **solo se l'inquadratura è disegnata da un registro**;
- `SCHEMATIC` in tutti gli altri casi.

Le scene 4–6 restano Schematic finché non c'è il registro (§7): la voce non cambia. Le parole sono quelle inglesi di
`voce_en_v2.txt`; ogni cifra conta 3 parole.

| # | Inizio–fine | Durata | Parole | Inquadratura | Componenti | Dati | Richiesta della traccia | Dicitura d'onestà |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:00–0:12 | 12 s | 22 | Verità a tutto schermo: piazzale, hangar, due multirotori, aereo in rullaggio. Titolo 0:00–0:03. A 0:05 la verità si restringe nel suo pannello (0,5 s, lineare). Un drone passa dietro l'hangar: a sinistra il bordo lo «mangia»; al centro il disco diventa anello con zona tratteggiata, `NOT SEEN · 0.8 s` che sale | VeritaSim, PiantaArea, Sensori, Traccia, Regione, ConsoleTracce, FasceOnesta, TitoloMarchio | registro `lp_V1_piazzale` (§7, R1) | Monitoraggio in ambienti aerospaziali; interruzioni della visibilità | SIMULATION, se c'è R1; altrimenti SCHEMATIC |
| 2 | 0:12–0:39 | 27 s | 52 | Fondo scuro, tre segni grandi sullo stesso drone: disco `SEEN`, anello e tratteggio `NOT SEEN · 1.2 s`, ombra intera a righe `WIDE ZONE`. Sotto ciascuno, in piccolo: «I see it», «here is where it can be», «I don't know». Poi l'ombra a puntini `UNVERIFIED ZONE`; la parola EMPTY compare sopra e viene **barrata**. Infine la fascia `POSSIBLE PRESENCE`, che resta | ScenaSchema, Traccia, Regione, PossibilePresenza | nessuno (illustrazione) | Distinguere osservato e incerto; sicurezza delle indicazioni | SCHEMATIC |
| 3 | 0:39–0:55 | 16 s | 27 | Pianta del sito: tutti i sensori **a terra, fermi**, con i glifi che si accendono uno alla volta e ognuno con la sua ombra. Un multirotore piccolo resta fuori dalla portata del radar: `observed for an aircraft · not for a small drone`. A schermo, non in voce: «Silent transponder: proves nothing» | PiantaArea, Sensori, VentaglioSettori, ScenaSchema | intestazione `sensori` di un registro lungo, se c'è; altrimenti `parametri_lunga_portata.json` | Rilevare elementi mobili e ostacoli | SCHEMATIC |
| 4 | 0:55–1:16 | 21 s | 40 | Tavola a tre viste. **Nebbia E3(a), 0–7 s:** il ventaglio di scheda resta come tratteggio fantasma, quello utile si ritrae; `USEFUL RANGE REDUCED · EO · IR`; `LA1 · NON-COOPERATIVE`. **Pioggia E3(b), 7–11 s:** stesso schema, multirotore, `HEAVY RAIN`, e `WARNING NOT TIMELY · small multirotor` solo se il registro lo dà. **Di nuovo E3(a)+(c), 11–21 s:** `NO REDUNDANCY`, poi la banda `RELIABILITY LOST · RADAR · injected fault`; la traccia di LA1 diventa `NOT SEEN · X s` con il tubo che cresce e `WARNING NOT TIMELY · all classes`. 1 s di silenzio di musica all'ingresso della banda | VeritaSim, PiantaArea, Sensori, Traccia, Regione, BandaAffidabilita, ConsoleTracce, FasceDominio, FasceOnesta | registri R3a, R3b, R3c (§7) | Perdita di affidabilità; feedback tempestivi; meteo | SIMULATION · E3, se c'è il registro; fascia del dominio `scenario E3 written by hand · fault injected 20 s` |
| 5 | 1:16–1:38 | 22 s | 40 | Tavola a tre viste (fotogramma A v3). Le tracce si fondono in `UNRESOLVED TRACKS` (non è un evento). A sinistra le due sagome si toccano; al centro **nessun impatto disegnato**, ma `EVENT: CONTACT · INFERRED` con, piccolo, `inferred from: track merge + new returns`. Nasce il volume a righe ocra, con gli anelli dei raggi passati e l'impronta a trattini, **senza punti dentro**. DroneA → `WIDE ZONE`; droneB a terra → `NOT SEEN · X s`. Persona `SEEN` dentro l'impronta, in console `WARNING TO OPERATOR · PERSON IN FOOTPRINT`. Dopo il 20° s del registro: `×4 · time compressed`. Fine: `UNVERIFIED · POSSIBLE DEBRIS · clears by inspection` | come la 4, più VolumeDetriti, ZonaNonVerificata | R1E (E1); a parte, in un riquadro di 3 s, R5 (E5: «close pass: no event») | Interruzioni della visibilità; detriti; tempestività | SIMULATION · E1, se c'è il registro |
| 6 | 1:38–1:58 | 20 s | 38 | Tavola a tre viste (fotogramma B v3). Nella verità, sul motore, un'**area bianca piatta senza punte**, `FLASH (3 s) · schematic`; l'aereo resta intatto; il fumo è una macchia grigia piatta. Nella pianta i glifi EO e IR sono barrati e le loro coperture diventano **settori interi** a contorno grigio tratteggiato, `EO, IR · NOT COUNTED`; il corallo compare solo nelle bande della console. Aereo `SEEN (RADAR ONLY)`; riga obbligatoria `radar response to flash: NOT VERIFIED`. `EVENT: SEPARATION · INFERRED`, con `inferred from: new radar returns behind the aircraft`. Nube `NOT OBSERVED · SMOKE (EO, IR)`; pista a valle `UNVERIFIED · POSSIBLE DEBRIS`; in console `WARNING TO OPERATOR · UNVERIFIED ZONE ON VEHICLE PATH`. 1 s di silenzio all'ingresso delle bande | come la 5, più Nube | R2E (E2) | Visibilità estremamente limitata; perdita di affidabilità; detriti | SIMULATION · E2, se c'è il registro |
| 7 | 1:58–2:28 | 30 s | 56 | Fondo scuro. I limiti, una riga alla volta (≤ 16 parole per schermata). A destra la catena a blocchi: sensori → celle → tracce → regole → uscite, con la classificazione di lato, tratteggiata, «required · hand labels». Sotto, i contatori con la loro origine | CatenaBlocchi, Tabellone, ScenaSchema | verdetto (§3.2) | Prototipo; efficienza; continuità | SCHEMATIC; i contatori portano `in simulation` |
| 8 | 2:28–2:39 | 11 s | 19 | Ponte visivo: la console della scena 6 si rimpicciolisce e diventa la scena a corto raggio (persona dietro un pannello, camera di profondità), con anello, zona e `POSSIBLE PRESENCE`. Riga a schermo: «Same core: presence warning for a blind person · does not replace a cane or guide dog» | ConsoleTracce, Regione, PossibilePresenza, FasceOnesta | registri corti `passa_dietro_e_ricompare`, `resta_dietro` | Accessibilità; continuità | SIMULATION · IDEAL SENSOR (dal registro), **nessuna cifra** |
| 9 | 2:39–2:52 | 13 s | 20 | Il simbolo SDMs v3b si anima (1,5 s, guida §7); wordmark MoVi; tagline; `Observes and warns · no output is a command`; tre righe di coda; 0,5 s di nero | TitoloMarchio, Crediti | nessuno | — | nessuna (titoli) |

**Totale: 172 s, 314 parole in inglese** (conteggio `awk` sul file, segnaposto esclusi; con le cifre, circa 318).

**Tempo della voce, stimato e non misurato.** A 129 parole al minuto (bm_george a 1.0) la voce fa circa 146 s. Le pause
fra le frasi non sono contate.
- La scena 2 è la più stretta: 52 parole in 27 s.
- La scena 7 regge: 56 parole in 30 s.
- Se la voce misurata con `.tempi.json` sfora, si taglia in quest'ordine, senza mai accelerare:
  1. nella scena 2, «MoVi declares what it has not observed» (resta il titolo a schermo);
  2. nella scena 6, «Downstream: possible debris, unverified» (passa a schermo);
  3. nella scena 5, «Then they touch» (lo dice l'immagine).

  La scena 7 non si taglia mai.

**Italiano:** 339 parole, circa 151 s con im_nicola. Si applicano subito i tagli 1 e 2. Non verificato finché non si genera
l'audio.

**Copertura della traccia:**

| Richiesta | Scene |
|---|---|
| Rilevare elementi mobili e ostacoli | 1, 3 |
| Interruzioni della visibilità | 1, 4, 5, 6 |
| Osservato e incerto | 2, 5 |
| Feedback tempestivi | 4, 5 |
| Perdita di affidabilità | 4, 6 |
| Sicurezza delle indicazioni | 2, 5 |
| Latenza ed efficienza | 7 (S7) |
| Ambiti aerospaziale e industriale | 1, 3 |
| Accessibilità | 8 |

**Testo a schermo fisso per scena** (≤ 16 parole per schermata, etichette di stato escluse):

- **Scena 3:** «Small drone, radar: [CIFRA-S2] by calculation · cross-section 0.01 m² assumed · ground clutter not modelled».
- **Scena 4:** «EO, multirotor, dense fog: [CIFRA-S3] (calc.)». La cifra sta accanto al cuneo, non su una linea lunga.
  Nella pioggia: «heavy rain: [CIFRA-S3b] (calc.)».
- **Scena 5:**
  - «Debris volume: by construction it never shrinks»;
  - se c'è V3, «Free cells inside footprint: [CIFRA-V3] · in simulation».
- **Scena 6:** «radar response to flash: NOT VERIFIED» (obbligatoria).
- **Scena 7:** le righe dei limiti; poi V1 e S7 (§3.2).

## 3. Il testo della voce (definitivo) e i segnaposto

`voce_en_v2.txt` e `voce_it_v2.txt` sono la fonte unica. I sottotitoli EN e IT si **generano da questi testi** con i tempi
di `.tempi.json`, non si scrivono a parte (Q20). I segnaposto fra parentesi quadre si riempiono o si tolgono **prima** di
mandare i file a Kokoro.

### 3.1 Inglese con l'italiano accanto

| # | EN (voce, bm_george) | IT (im_nicola) |
|---|---|---|
| 1 | An apron. A hangar. Two inspection drones. An aircraft taxiing. One drone slips behind the hangar. What should the screen say now? | Un piazzale. Un hangar. Due droni d'ispezione. Un aereo in rullaggio. Un drone scivola dietro l'hangar. Che cosa deve dire lo schermo, adesso? |
| 2 | MoVi declares what it has not observed. For every tracked object, one of three answers. I see it. I don't see it: here is where it can be. Or: I don't know. What it has not observed, it marks unverified, never empty. A possible-presence warning stays on until a sensor looks again. | MoVi dichiara ciò che non ha osservato. Per ogni oggetto seguito, una di tre risposte. Lo vedo. Non lo vedo: ecco dove può essere. Oppure: non lo so. Ciò che non ha osservato lo segna non verificato, mai vuoto. Un avviso di possibile presenza resta acceso finché un sensore non torna a guardare. |
| 3 | Radar, LiDAR, visible and thermal cameras, and what aircraft and drones broadcast. All simulated from public data sheets. Each sensor has blind spots, and MoVi draws them. | Radar, LiDAR, camere visibili e termiche, e ciò che trasmettono aerei e droni. Tutto simulato dalle schede tecniche pubbliche. Ogni sensore ha i suoi punti ciechi, e MoVi li disegna. |
| 4 | Fog, then heavy rain. By calculation, the cameras' reach collapses, and MoVi declares it, per sensor. Only the radar is left: no redundancy. If the radar also fails, a fault we inject, reliability is lost: warnings would come too late. | Nebbia, poi pioggia forte. Per calcolo, la portata delle camere crolla, e MoVi lo dichiara, sensore per sensore. Resta solo il radar: ridondanza assente. Se cade anche il radar, un guasto che introduciamo noi, l'affidabilità è persa: gli avvisi arriverebbero troppo tardi. |
| 5 | Two drones fly close. Too close to separate: unresolved tracks. Then they touch. Event: contact, inferred. A possible-debris volume opens, and never shrinks on its own. The operator is warned: a person is underneath. The ground stays unverified until inspected. | Due droni volano vicini. Troppo vicini per separarli: tracce non risolte. Poi si toccano. Evento: contatto, dedotto. Si apre un volume di possibili detriti, che non si restringe mai da solo. L'operatore riceve l'avviso: sotto c'è una persona. Il suolo resta non verificato finché non è ispezionato. |
| 6 | An engine fails on the take-off run, with a flash. The flash blinds the cameras: MoVi marks them unreliable. In the model, the radar alone still sees the aircraft. Behind the smoke: not observed. Downstream: possible debris, unverified. | Un motore ha un'avaria in corsa di decollo, con una fiammata. La fiammata acceca le camere: MoVi le dichiara non affidabili. Nel modello, il solo radar vede ancora l'aereo. Dietro il fumo: non osservato. A valle: possibili detriti, non verificato. |
| 7 | First, the limits. Everything you saw is simulated from public data sheets: no physical sensor. Object classes are labelled by hand. [STATO-1] The full chain has not yet run end to end. Total delay is not measured. What holds: written rules decide, not a trained model. [CIFRA-V2] In simulation, hidden objects left without a warning: [k] of [n]. | Prima, i limiti. Tutto ciò che avete visto è simulato dalle schede tecniche pubbliche: nessun sensore fisico. Le classi degli oggetti sono etichettate a mano. [STATO-1] La catena intera non è ancora stata eseguita dall'inizio alla fine. Il ritardo totale non è misurato. Che cosa regge: decidono regole scritte, non un modello addestrato. [CIFRA-V2] In simulazione, oggetti nascosti rimasti senza avviso: [k] su [n]. |
| 8 | The core comes from our short-range version: a person behind an obstacle, a depth camera, the same three answers. | Il nucleo viene dalla nostra versione a corto raggio: una persona dietro un ostacolo, una camera di profondità, le stesse tre risposte. |
| 9 | MoVi. Seen, not seen, unknown: declared for every track. It observes and warns. No output is a command. By SDMs. | MoVi. Visto, non visto, non so: dichiarato per ogni traccia. Osserva e avvisa. Nessuna uscita è un comando. Di SDMs. |

**Varianti obbligate dai dati:**
- Senza la classe «corsa di decollo» (`scene-dinamiche-3`), nella scena 6 si dice «An engine fails while the aircraft
  taxis, with a flash.» / «Un motore ha un'avaria mentre l'aereo rulla, con una fiammata.» (E2 ha `aereo_rullaggio`.)
- Se STATO-1 diventa «sì», la frase si sostituisce con «The full chain has run end to end, in simulation only.» / «La
  catena intera è stata eseguita dall'inizio alla fine, solo in simulazione.»

**Correzioni dell'attacco, tutte applicate:**
- 1: «tracked», «marks unverified»;
- 2: via «unless it has looked»; la tagline corretta;
- 3: «In the model…»; il sottotitolo uguale alla voce, generato dalla voce;
- 4: «a fault we inject»;
- 5: avvisi solo all'operatore, e nella scena 6 tolti dalla voce;
- 6: V1 fuori dalla voce, V2 senza «lost»;
- 7: il lessico del §4;
- 8–10: fotogrammi e glifi (§4);
- 11: la musica (§8);
- 12: la scaletta (§2);
- 13: QA e conflitti (§9).

### 3.2 I segnaposto

Regola: se una cifra non arriva, **si toglie la frase**. Non la si sostituisce con un aggettivo, e una soglia non prende mai
il posto di un risultato. Le misure «di soglia» delle schede `misure` diventano cifre solo se il verdetto le **misura**.

| Segnaposto | Misura | Scenario | Sensore | Dove la prende il verdetto | Dove va | Se manca |
|---|---|---|---|---|---|---|
| STATO-1 | La catena intera (sensori simulati → regole EV → uscite → registro) è stata eseguita? | E1–E4 | tutti | dichiarazione del verdetto su `movi_lp.py` con EV-A…E realizzate (`REGOLE_E_SCENARI_EVENTI.md`, righe 23–24) | voce, 7 | resta «not yet» (oggi è così) |
| CIFRA-V2 | Oggetti nascosti rimasti senza avviso, k su n, con n dichiarato | E1–E4, `misure.tracce_perse_senza_avviso` | radar, EO, IR, LiDAR | conteggio dei registri E1–E4 con EV | voce, 7 | **Variante B** (attacco, §3), **solo a schermo**: «Tracks with no declared state: [k] of [n] frames · format check» (da `valida_riga` sui registri che esistono, con il dominio). Se non c'è neppure questa, la frase si toglie e la scena 7 tiene i limiti a schermo 4 s in più |
| CIFRA-V1 | Campioni (frammento, istante) dentro V(τ), k su n, nel dominio `v_t ≥ v_t,min, \|u\| ≤ Δv` | E1, E2, `misure.quota_frammenti_dentro_V` | — (modello dei frammenti) | verdetto §E1/E2. Candidato «0 fuori su 1 131 692» (`40-eventi/02-regole` §3), stesso autore del generatore | **solo a schermo**, 7: «Own fragment model: [k] of [n] samples inside the volume · within model assumptions» | si toglie; resta la proprietà «by construction it never shrinks» (scena 5) |
| CIFRA-V3 | Celle «libere» dentro l'impronta, k su n cicli | E1, `misure.celle_libere_dentro_impronta` | tutti | registro E1 con EV-E | schermo, 5 | si toglie |
| CIFRA-S2 | Distanza di primo rilevamento di un multirotore piccolo | calcolo, non scenario | radar del sito | `02-sensori/SENSORI_LUNGA_PORTATA.md` §2 (candidato 3,1 km per 0,01 m²), confermato dal verdetto | schermo, 3 | si toglie la riga |
| CIFRA-S3 / S3b | Portata utile, per calcolo, con nebbia fitta e con pioggia forte | E3(a), E3(b), `misure.portata_utile_dichiarata` | camera EO, multirotore | EV-D, `conti_eventi_esito.txt` (candidati 23 m e 526 m), con la misura «uguale al conto entro il 5 %» | schermo, 4 | si toglie la cifra; resta la geometria del registro |
| CIFRA-S7 | Tempo di calcolo per ciclo del modo lungo, con la macchina | E1–E4 | — | misura su `movi_lp.py` | schermo, 7: «[S7] per cycle · laptop · simulated scenes · total delay not measured» | si toglie; la cifra a corto raggio (6 ms) **non** si sposta qui |
| CIFRA-S1 | Copertura della zona al livello 0,90, per classe e orizzonte, con il dominio | `lp_A1`/`lp_A2` | — | verdetto, solo se è misurata su tracce di classe aereo o drone | schermo, 1, su una riga a parte, **mai** accanto alla zona | si toglie: il candidato 0,8703 misura il generatore |
| S4, S5, S6 | Ritardo dell'evento; falsi eventi in E5; cicli fino ad «affidabilità persa» | E1, E5, E2 | — | solo se il verdetto le **misura** | schermo, 5 e 6 | **tolte**. Previsione dell'attacco: non arrivano |
| STATO-2 | Ritardo totale | — | — | — | voce, 7 («not measured») | resta così |

## 4. Il sistema visivo (definitivo)

**Griglia:** 1920 × 1080, margini di 96 e 54 px; tavola a tre viste ferma, come in R §2.1.

| Zona | Rettangolo | Contenuto |
|---|---|---|
| Fascia alta | 0–124 | scena e richiesta della traccia a sinistra; etichetta d'onestà a destra |
| SIMULATED TRUTH | x 96–576 | — |
| AS MoVi DECLARES IT | x 600–1384 | — |
| OPERATOR CONSOLE | x 1408–1824 | — |
| Fascia del dominio | y 862–900 | — |
| Sottotitoli | y 940–1080 | — |

**Console ridotta:** 3 righe di stato e una riga d'evento; le righe secondarie compaiono solo quando la voce le cita
(lettura, 13).

**Palette** (fondo #0B0F17, pannello #121826, bordi #24344A, testo #E8EDF2 e #AEB8C5). Nessuna tinta fra 90° e 160°.

| Ruolo | Colore | Uso esclusivo |
|---|---|---|
| Visto | ciano #3DD6E8 | disco della traccia, `SEEN` |
| Non visto | ambra #F5A524 | anello, zona tratteggiata, `WIDE ZONE`, `UNRESOLVED TRACKS` (**solo oggetti**) |
| Avviso | ocra #C7841A **sempre con righe a 45°** | `POSSIBLE PRESENCE`, volume e impronta dei detriti. Si distingue dall'ambra per la trama e la parola, non per il colore (lettura, 16) |
| Sensore degradato | #AEB8C5, bordo tratteggiato | `USEFUL RANGE REDUCED`, `NO REDUNDANCY` (non più l'ambra) |
| Affidabilità persa | corallo #FF6B6B, testo #0B0F17 | **solo** bande della console e banda di sistema di 120 px; sulla pianta i sensori guasti sono settori interi a contorno grigio tratteggiato, `NOT COUNTED` |
| Non osservato, non verificato | puntini #8A97A8, nube #6B7686 + parola | `UNVERIFIED ZONE`, `NOT OBSERVED · cause (sensors)` |
| Cooperativi | viola #A99CFF | glifo quadrato ADS-B o identificazione remota |
| Posizione vera | bianco #E8EDF2 | solo nel pannello della verità e nel segno di verifica alla ricomparsa (regola 7 delle nove) |

**Lessico unico.** Vale in voce, a schermo e nei sottotitoli. Sostituisce le tabelle di M §6, R §2.2 e K.

| Registro | Schermo (EN) | Italiano | Forma |
|---|---|---|---|
| `vista` | `SEEN · ID` / `SEEN (RADAR ONLY)` | vista (solo radar) | disco pieno |
| `vista_in_parte` | `PARTLY SEEN` | vista in parte | disco a metà |
| `in_conferma` | `CONFIRMING` | in conferma | disco vuoto sottile |
| `non_vista` + regione | `NOT SEEN · 2.4 s` | non vista da 2,4 s | anello + zona tratteggiata al 18 %, mai una sagoma |
| `previsto_ampio` | `WIDE ZONE` | previsto ampio | righe su tutta la regione, anello al centro, nessun punto |
| `ricomparsa` | `SEEN AGAIN · IDENTITY ASSUMED` | ricomparsa, identità presunta | disco + «?» per 2 s |
| `identita: ambigua` | `UNRESOLVED TRACKS` | tracce non risolte | due anelli uniti da un tratteggio |
| `possibile_presenza` | `POSSIBLE PRESENCE` | possibile presenza | contorno a righe ocra |
| celle `zona_non_verificata` | `UNVERIFIED ZONE` | zona non verificata | puntini |
| detriti a terra (EV-E) | `UNVERIFIED · POSSIBLE DEBRIS` | non verificato · possibili detriti | puntini + impronta |
| volume V(τ) | `POSSIBLE DEBRIS` | possibili detriti | righe ocra, anelli dei raggi passati, **nessun punto** salvo `RADAR RETURNS` dal registro (quadratini grigi) |
| nube | `NOT OBSERVED · SMOKE (EO, IR)` / `· FOG` | non osservato · fumo | puntini fitti + contorno a trattini |
| `visto_libero_fino_a` | `OBSERVED EMPTY · class · to d m` | visto vuoto · classe · fino a d m | cella tenue #24344A, solo nel fotogramma corrente |
| `affidabilita_persa` | `RELIABILITY LOST · sensor · cause` | affidabilità persa | banda corallo |
| portata ridotta | `USEFUL RANGE REDUCED · sensor` | portata utile ridotta | ventaglio fantasma + utile |
| — | `NO REDUNDANCY`, `WARNING NOT TIMELY · class` | ridondanza assente; avviso non tempestivo | banda grigia |
| `eventi[]` | `EVENT: CONTACT · INFERRED` / `EVENT: SEPARATION · INFERRED` (o `OBSERVED`) + `inferred from: …` | evento: contatto / separazione (dedotto) | riga di console |
| avvisi all'operatore | `WARNING TO OPERATOR · …` | avviso all'operatore | riga di console |
| ispezione | `INSPECTED BY OPERATOR` | ispezionata da operatore | (non c'è negli scenari: non compare) |

**Termini vietati** (Q9): FREE, CLEAR, PREDICTED o PREDICTION, LOST come stato, GONE (anche fra virgolette), probable,
target, threat, engage, intercept, lock, hostile, test range, validated, certified, compliant, guaranteed, detect and avoid,
real-time.

Il campo `"bersaglio"` di `scenari_eventi.json` non affiora mai: si scrive «warning area».

**Eccezione registrata:** nel video non si dice «no engagement or pointing function» (lettura, 12). Il perimetro si dice
«Observes and warns · no output is a command». La formula L8 resta nella descrizione e nella relazione.

**Glifi dei sensori** (grigi, salvo i cooperativi):

| Sensore | Glifo |
|---|---|
| radar | piccolo cerchio pieno grigio con un arco (attacco, 10; mai cerchio con punto) |
| EO | triangolo vuoto |
| IR | triangolo pieno al 50 % |
| LiDAR | rombo |
| cooperativi | quadrato viola |

**Tipografia:**
- Inter (OFL) per i titoli, da 38 a 96 px, e per i sottotitoli, Inter 600 da 40 px.
- JetBrains Mono **Bold** (700, perché il 600 non c'è in locale) per le etichette di stato, da 28 px in su, e per la console.
- JetBrains Mono Regular, da 20 a 22 px, solo per le righe di fonte e di dominio.
- Font da file locale, mai dalla rete.

**Movimento:**
- I cambi di stato sono istantanei (0–2 fotogrammi).
- Regioni, volumi e coperture crescono come dice il registro, senza easing aggiunto.
- Camera ferma nelle scene di dati; un carrello lento (≤ 5 % al secondo) solo nelle scene 2, 3 e 7.
- Tempi di scenario reali; dove si comprime il tempo, la fascia lo dice (`×4 · time compressed`).
- Tagli netti fra le scene. Le uniche transizioni motivate sono:
  - il restringimento della verità nella scena 1;
  - il ponte della console nella scena 8;
  - la dissolvenza al nero alla fine.

**Divieti grafici:**
- niente verde, spunte, frecce «vai», semafori;
- niente bagliori, particelle, scansioni, mirini, reticoli, coni puntati su un aereo;
- niente stelle a punte per la fiammata;
- niente fuoco realistico, sangue, vittime, volti, loghi di terzi, livree;
- aerei e droni solo come sagome piatte grigie.

**Fotogrammi da rifare come `_v3`, accanto alle v2:**
- **A:** via i punti bianchi dalla pianta; «A · PREDICTED» diventa `A · WIDE ZONE`; via `never "gone"`.
- **B:** fiammata piatta senza punte; settori interi grigi; «EO · RELIABILITY LOST» dentro la banda.
- **C:** «23 m (calc.)» accanto al cuneo; `LA1 · NON-COOPERATIVE`.
- **Su tutti e tre:** l'etichetta `SCHEMATIC · STYLE FRAME` al posto della coppia contraddittoria «SIMULATION / values
  schematic» (attacco, 21).

## 5. Il marchio

- **Wordmark MoVi (`movi_wordmark*.svg`, v2): approvato.** La «o» è l'anello tratteggiato, il punto della «i» è il disco
  ciano. Si legge da 32 px in su.
- **Simbolo SDMs: corretto.** Ho applicato la correzione obbligata 10 dell'attacco (via l'anello interno, che con quello
  esterno faceva un bersaglio a cerchi). La tavola `video/marchio/tavola_controllo_v3.png` (v2, v3, v3b a 168 e a 32 px)
  mostra però che il **v3**, cioè il disco accanto a un anello di 8 trattini, si legge come una **rotellina di
  caricamento**: è il rischio già visto dalla lettura (giurato esterno). Per questo:
  - **approvato per il video: `sdms_logo_v3b.svg` e `sdms_simbolo_v3b.svg`** (con le versioni `_mono` e `_mono_scuro`).
    Il disco ciano sta accanto a una **zona ellittica** tratteggiata ambra (rx 33, ry 26, 8 trattini al 60 %), vuota: non
    è un cerchio, non è concentrica a niente, e ripete la forma delle zone del video, che sono regioni e non anelli;
  - `_v3` (cerchio vuoto) resta come alternativa, se il test la preferisce; `_v2` (con l'anello interno) **non si usa**;
  - verde: 0 pixel. `xmllint`: 0 errori.
- **Test dei cinque secondi** (K §7 con l'aggiunta dell'attacco), su 5 persone fuori dal gruppo, v3b e v3 in ordine alterno.
  Due domande: «che cosa vuol dire?» e «ti ricorda un mirino o un caricamento?».
  - *Previsione:* per v3b, al più 1 su 5 dice «mirino» o «caricamento».
  - *Smentita:* 2 o più su 5. In quel caso si passa alla sola parola «SDMs» con il disco.
  - Esito: **non eseguito**.
- **SDMs** non si scioglie: la sigla non si spiega a schermo, per decisione presa qui (lettura, 15). Se la squadra vuole
  spiegarla, va nella descrizione.
- **Anteriorità del marchio:** non verificata (attacco, 23).
- **`GUIDA_MARCHIO.md`** non l'ho modificata: la v3b va aggiunta al §2 della guida, come versione nuova, da chi la mantiene.

## 6. I componenti (HyperFrames 0.9.48, via A di `STRUMENTI.md` §2)

**Interfaccia comune.** Ogni componente è una funzione pura `draw(riga, intest, opz)`.
- `riga = registro[floor(t·30 + 1e-6)]`: si tiene l'ultimo stato, gli stati non si interpolano.
- `intest` è la riga 1 del registro.
- `opz = {scala_m_px, origine, pannello, lingua}`.

I dati arrivano come `assets/data/<scena>.js` (`window.__REG = {fps, intest, righe}`), prodotti dal `.jsonl` con
`genera_stati.mjs`. Ci sono una composizione per scena (`compositions/sNN_*.html`) e il testo a schermo in
`testi/schermo_{en,it}.json`, per chiave, separato dalle scene: la versione italiana non tocca le immagini.

| # | Componente | Legge | Disegna |
|---|---|---|---|
| 1 | `PiantaArea` | `intest.ostacoli`, `aree`, `griglie` | aree, hangar, scala grafica |
| 2 | `Sensori` | `intest.sensori` (id, tipo, pos, portata di scheda, campo); `riga.sensori[].salute, causa`, `portata_utile_m{classe}`\* | glifi; copertura piena, fantasma, oppure settore grigio `NOT COUNTED` |
| 3 | `Traccia` | `tracce[]`: id, classe, `origine_etichetta`, `stato`, `non_vista_da_s`, `identita`, pos | disco, anello, «?»; `ID · STATE · X s` |
| 4 | `Regione` | `tracce[].regione` (cerchio, poligono, settore_anulare, celle) | tratteggio al 18 %, oppure righe per `previsto_ampio` |
| 5 | `PossibilePresenza` | `avvisi[]` | contorno a righe ocra + parola |
| 6 | `VolumeDetriti` | `volumi[]`\*: evento, `t_a`, `tau`, forma, quota, `impronta`; `ritorni[]`\* | righe ocra, anelli dei raggi passati, impronta; quadratini `RADAR RETURNS` solo dal registro |
| 7 | `Nube` | `nubi[]`\*: id, forma, `opaca_per[]`; `celle.per_sensore` con `causa`\* | puntini fitti + parola con i sensori |
| 8 | `BandaAffidabilita` | `sensori[].salute, causa, eta`; `affidabilita` | bande in console; banda di sistema |
| 9 | `ConsoleTracce` | `tracce[]`, `eventi[]` (t, tipo, `come_lo_so`, `indizi`\*), `avvisi_operatore[]`\* | 3 righe di stato + 1 riga d'evento |
| 10 | `VentaglioSettori` | `settori[]` | settori a tre livelli |
| 11 | `ZonaNonVerificata` | `celle` (`rle`, causa) | puntini; si tolgono solo all'evento `ispezione` |
| 12 | `Tabellone` | contatori del verdetto (k, n, origine, dominio) | contatore con l'origine sotto |
| 13 | `CatenaBlocchi` | `dichiarazioni.regole` | blocchi; quelli spenti tratteggiati, «in design» |
| 14 | `VeritaSim` | `verita` (oggetti, classe, pos, visibile), eventi dello scenario (`durata_sorgente_s`) | sagome grigie, fiammata piatta, fumo piatto, pioggia e nebbia come velo |
| 15 | `FasceOnesta` | `dichiarazioni` di **ogni riga** | `SIMULATION · …` solo se c'è la riga, altrimenti `SCHEMATIC`; il dominio in basso; `×N` |
| 16 | `ScenaSchema` | `testi/schermo_*.json` | segni grandi delle scene 2, 3 e 7 |
| 17 | `TitoloMarchio` | SVG di `video/marchio/` (v3b, wordmark v2) | titolo, animazione del simbolo, chiusura |
| 18 | `Sottotitoli` | `.srt` EN e IT da `.tempi.json` | fascia bassa (oppure impressi con libass) |

\* = campo **proposto**, che oggi non c'è nel registro (`ARCHITETTURA.md` §3: «il formato basta al modo lungo: non
risolto»). Finché manca, il componente non disegna niente, e l'inquadratura va `SCHEMATIC`.

## 7. I registri da chiedere al prototipo (quando è pronto)

**Formato:** `registro.jsonl` del modo `lungo`, a 30 righe al secondo (o ricampionato con «tieni l'ultimo»), validato da
`valida_riga`, con `verita` piena e `dichiarazioni` in ogni riga.

| Id | Scena del video | Scenario e condizione | Finestra | Oggetti | Campi richiesti oltre al formato attuale |
|---|---|---|---|---|---|
| R1 | 1 | **`lp_V1_piazzale`**: `lp_A2` (hangar, aereo in rullaggio, mezzo, persona) con due multirotori da `lp_A1`, uno dei quali passa dietro l'hangar. E1 ed E2 **non hanno ostacoli**, quindi non bastano | 0–12 s | 2 multirotori, aereo, mezzo, persona | nessuno |
| R3a | 4 | E3(a), nebbia fitta, aereo leggero non cooperante | 0–40 s | leggero1 | `sensori[].portata_utile_m{classe}`, `copertura`, `ridondanza`, `avviso_tempestivo{classe}` |
| R3b | 4 | E3(b), pioggia forte, multirotore | 3–5 s utili | drone3 | come R3a |
| R3c | 4 | E3(a)+(c), guasto del radar 100–120 s, nebbia | 95–125 s | leggero1 | come R3a; la regione a tubo |
| R1E | 5 | E1 nominale (seme dichiarato), con EV-A ed EV-E | 10–90 s (×4 dopo i 20 s) | droneA, droneB, persona1 | `volumi[]`, `impronta`, `eventi[].indizi`, `avvisi_operatore[]`, `ritorni[]`, `celle.causa` |
| R5 | 5 (riquadro) | E5, separazione di 5 m | 10–20 s | droneA, droneB | come R1E |
| R2E | 6 | E2 nominale, con EV-A, EV-B, EV-C ed EV-E (se c'è, con la corsa di decollo) | 12–40 s | aereo1, mezzo1 | `nubi[]`, `celle.per_sensore.causa`, `volumi[]`, `avvisi_operatore[]` |
| R4 | riserva | E4(a) ed E4(b), colonna di fumo | 15–25 s | drone4 | `nubi[]` |
| Rc | 8 | corto raggio: `passa_dietro_e_ricompare`, `resta_dietro` (esistono già) | intera | persona | nessuno |

Dal verdetto servono anche: STATO-1, i contatori del §3.2 con origine e dominio, e l'impronta della configurazione di ogni
registro (per Q14 e Q28).

## 8. Audio e licenze

- **Voce:** Kokoro-82M, `bm_george`, `--velocita 1.0 --pausa-frase 0.35 --pausa-paragrafo 0.8`; poi `im_nicola` sulla
  stessa immagine.
  - Kokoro è sotto Apache-2.0 (`STRUMENTI.md` §3.5). La licenza dei file delle voci la registra §3.5, che **non ho letto
    per intero**: va ricontrollata in Q22.
  - Prima del montaggio si misura con `.tempi.json` e con `asr_controllo.py`.
  - Nessuna voce di persona reale.
- **Musica:** **il tappeto sintetico** `00-strumenti/audio/uscite/tappeto_180s.wav` (numpy, seme 7, senza diritti di
  terzi, senza attribuzione: attacco, 11).
  - Se dopo l'ascolto si sceglie «Dreams Become Real» di MacLeod (CC BY 4.0), l'attribuzione va in un cartello di 2 s da
    ≤ 16 parole («Music: "Dreams Become Real", Kevin MacLeod, incompetech.com, CC BY 4.0»), nel `.srt` della
    descrizione e in Q22.
  - Bartmann e «Ossuary» sono esclusi.
- **Ambiente:** fruscio d'aria generato con ffmpeg a −26 dB. Nessun motore registrato, nessun «boom» alla fiammata né alla
  collisione, nessuna sirena.
- **Suoni:** nessun suono legato agli stati e nessuna altezza legata all'incertezza. Unica eccezione: 1 s di silenzio di
  musica e ambiente all'ingresso di `RELIABILITY LOST`, nelle scene 4 e 6.
- **Mix:** `mix.sh` (musica −14 dB con sidechain), loudnorm a due passate a **−14 LUFS**, picco vero ≤ −1,5 dBTP
  (≤ −1,0 per il regolamento interno); un limitatore prima, per restare in modalità lineare (avvertenza di
  `STRUMENTI.md` §5.2).
- **Esportazione:** H.264 High, yuv420p, CRF 18, 30 fps, AAC 48 kHz, `faststart`, una sola codifica finale (resa
  HyperFrames `--quality delivery` o in PNG).
- **Licenze da registrare in Q22:**

  | Materiale | Licenza | Nota |
  |---|---|---|
  | Inter | OFL 1.1 | — |
  | JetBrains Mono | OFL 1.1 | — |
  | HyperFrames | Apache-2.0 | — |
  | GSAP | GreenSock Standard License | gratuito, non libero |
  | Kokoro | Apache-2.0 | — |
  | tappeto | opera del gruppo | — |
  | marchio | opera originale del gruppo | — |
  | modelli dei sensori | schede tecniche pubbliche | i nomi commerciali solo nella relazione, mai a schermo |

## 9. Controllo qualità (adattato da ISTRUZIONI §11)

Il video si consegna solo con tutte le voci superate. Il rapporto `MoVi_QA_video_v1.md` riporta per ogni voce l'esito, il
metodo e la prova. Le voci contrassegnate † cambiano per il nuovo caso; le altre restano come nelle istruzioni.

| # | Controllo | Criterio |
|---|---|---|
| Q1 | Durata (`ffprobe`) | fra 165,0 e 175,0 s (regolamento: < 240 s) |
| Q2 | Parole della voce | ≤ 340, in EN e in IT |
| Q3 | Ritmo | ≤ 135 parole al minuto per scena, su `.tempi.json` |
| Q4 | Testo a schermo | ≤ 16 parole per schermata, etichette di stato escluse |
| Q5 † | Cifre | ognuna dal verdetto (§3.2), con origine («in simulation», «by calculation», «assumed») e dominio |
| Q6 † | Cifre escluse | nessuna cifra fuori dal §3.2; nessuna soglia presentata come risultato; nessuna cifra della v1.0 a corto raggio fuori dalla scena 8 (dove non ce n'è nessuna) |
| Q7 † | Domini | V1 e S1 mai senza dominio; S1 mai accanto a una zona |
| Q8 † | Limiti | in voce: simulato, nessun sensore fisico, etichette a mano, catena (STATO-1), ritardo non misurato, «in the model» per il radar. A schermo: tempi di reazione ipotizzati, fuori dal modello (frammenti più veloci), radar e fiammata non verificati, sensori a terra e fermi, avviso solo all'operatore |
| Q9 † | Termini vietati | lessico del §4, ricerca sul `.srt` EN e IT e sul testo a schermo; zero occorrenze. Eccezioni scritte: nessuna (la formula L8 non è nel video) |
| Q10 † | Nomi degli stati | solo quelli della tabella del §4; nessun PREDICTED, FREE, CLEAR, LOST, GONE |
| Q11 | Niente verde | un fotogramma al secondo; nessuna area > 50 px con tinta 90–160° e saturazione > 30 % |
| Q12 † | «Vuoto» | `OBSERVED EMPTY` solo dove il registro lo dice; mai dentro un'impronta, una nube o oltre la portata utile |
| Q13 † | Etichette d'onestà | per tutta la durata; `SIMULATION` solo nelle inquadrature con un registro (controllo automatico su `FasceOnesta`) |
| Q14 † | Fedeltà ai registri | scene 1 e 4–6 e 8, un fotogramma al secondo confrontato con R1…Rc: stati, ID, età, regioni, volumi, bande |
| Q15 † | Disegno dell'incertezza | le nove regole; in più: nessun punto dentro il volume dei detriti nella pianta; nessun cono o settore puntato su un aereo |
| Q16 † | Etichetta del sensore | scena 8 `IDEAL SENSOR`; scene 4–6 il sensore che dichiara (`RADAR ONLY`, `EO, IR · NOT COUNTED`) |
| Q17 | Segnali sonori | nessuno |
| Q18 | Loudness | −14 LUFS ± 1; picco ≤ −1,0 dBTP |
| Q19 | Formato | 1920 × 1080, 30 fps, yuv420p, H.264, AAC 48 kHz |
| Q20 † | Sottotitoli | `.srt` EN e IT generati dalla voce, identici al testo detto; scarto ≤ 200 ms; 2 righe da 42 caratteri |
| Q21 | Margini | nessun testo fuori dalla griglia di sicurezza |
| Q22 † | Licenze | §8, compresa la licenza dei file delle voci Kokoro |
| Q23 † | Volti e persone | solo sagome; niente sangue né vittime |
| Q24 | Segnaposto | zero `[CIFRA`, `[STATO`, `[DA FORNIRE` nel video, nel `.srt` e nei file dati a Kokoro |
| Q25 | Committente | nessun riferimento |
| Q26 † | Decisioni | le scelte di questo piano registrate (tagline, lessico, logo v3b, musica, posizione dell'etichetta) |
| Q27 † | Conflitti, con la scelta e chi l'ha fatta | (a) «drone», «aircraft», «fly» ammessi **solo per gli oggetti osservati**; i sensori sono sempre a terra e fermi; nessun sensore a bordo (regole 15, 24, 25); (b) l'avviso «diretto al conducente» di `scenari_eventi.json` E2 diventa nel video «avviso all'operatore»; (c) l'etichetta d'onestà sta in alto a destra, non in basso; (d) JB Mono 700 invece di 600; (e) il titolo dentro la scena 1. Scelte del videomaker in sintesi, autorizzate dall'addendum 13 |
| Q28 † | Versione unica | tutte le cifre da un solo verdetto, con l'impronta della configurazione |
| Q29 | Revisione indipendente | le quattro domande, più «la fiammata o la collisione sembrano spettacolo?» |
| Q30 † | Funzioni tagliate | nessuna funzione assente dai registri in voce o a schermo; le regole EV non eseguite si dicono «not yet run» |
| Q31 † | Piattaforme | nessun sensore su un drone o su un aereo; se compare A4: «analysis only, not simulated» |
| Q32 † | Fonti esterne | nessun nome commerciale di sensore o di sistema a schermo; il coasting citato come principio solo nella relazione |
| Q33 † (nuova) | Lessico d'ingaggio, nelle immagini | nessun mirino, reticolo, cerchio concentrico attorno a un oggetto, cono rosso puntato; controllo a vista sul fotogramma più denso di ogni scena |
| Q34 † (nuova) | Tempo compresso | ogni tratto non in tempo reale porta `×N · time compressed` |

## 10. Stati proposti

| Enunciato | Stato |
|---|---|
| Voce EN entro le 340 parole | **Verificato** sul file: 314 parole, più circa 4 per le cifre |
| La voce entra nei tempi delle scene | **Non risolto**: lo decide `.tempi.json` di bm_george |
| Il simbolo SDMs v3 sembra un caricamento | **Sostenuto** dalla sola mia visione della tavola v3; la lettura aveva visto lo stesso rischio |
| Il simbolo SDMs v3b non sembra né un mirino né un caricamento | **Non risolto**: lo decide il test dei cinque secondi |
| Senza verde | **Verificato** sui file del marchio (tavola v3: 0 pixel); sul video non ancora |
| Le scene 4–6 possono essere SIMULATION | **Non risolto**: mancano i campi \* e le regole EV in `movi_lp.py` |

## 11. Che cosa propongo dopo

1. Il videomaker rifà i fotogrammi A, B e C come `_v3` con il §4.
2. Si genera la voce guida EN dai file `voce_*_v2.txt` con segnaposto neutri (frasi delle cifre tolte), solo per misurare i
   tempi, e si monta un animatic a 960 × 540.
3. L'architetto aggiunge i campi \* al registro (§6) e produce R1 e R1E. Senza quei registri, le scene 1 e 4–6 escono
   `SCHEMATIC`.
4. Il marketing esegue il test del logo (§5) e aggiorna `GUIDA_MARCHIO.md` con la v3b.
5. All'arrivo del verdetto si applica il §3.2 senza riaprire il copione. Poi il lettore critico ripassa Q9, Q10, Q15 e Q33
   sul montaggio.
