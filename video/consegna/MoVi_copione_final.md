# MoVi pitch FINAL (v3d): copione (EN, con la traduzione italiana)

**Voce e tempi identici alla v3c** (stessa voce `voce_en_v3c.txt` / `voce_it_v3c.txt`, stessi tempi; EN 174,379 s, IT 170,469 s). Cambia solo ciò che è a schermo:
- s1, dalla domanda (9,9 s EN): riga «not observed ≠ clear» (REVISIONE_V3C C6);
- s7: tolte le sigle «C-TAR», «min. progressive», «Wilson» («95 % intervals per case»); etichetta «fixed zone at last sighting · 150 m» dentro il pannello (C4, C5);
- s5: «false events in a 39 m near miss with optics blinded 2/60 [0.009; 0.114]» senza «(F5)»;
- s8 F7: le tre righe di limite c1 (49/60 e 40/60; 565 m, mediana 8 s; 11/200) compaiono subito dopo 59/59 e restano fino alla fine della scena (QA_V3C D2); barra «position confidence, tracked drone (computed in the model)» con «identity: …» dal registro (C3); pianta allargata a 560 m perché il drone seguito resti nel pannello e la sua etichetta non copra quella del portatore (D4);
- s9: «LP-1 · S · simulation» e «LP-4 · S · simulation» diventano «simulation»;
- s10 LIMITS: la riga di prima di c1 («debris warning to the carrier not reliable») è sostituita da tre righe: «radar blinded: carrier warned only with a fix under test (sim.)», «that fix: warning not localised; reacquisition still partial», «that fix: false warnings 11/200 [0.031; 0.096] (sim.)» (QA_V3C D1, REVISIONE_V3C C1).

Segue il copione v3c, invariato per voce e sottotitoli.

---

# MoVi pitch v3c: copione (EN, con la traduzione italiana)

Durata del montaggio 174.379 s; file `video/consegna/MoVi_pitch_EN_v3c.mp4` (ffprobe 174,379 s). Voce Kokoro bm_george, velocità 1,0 (mai accelerata). Generato da `video/voce/testi/voce_en_v3c.txt` e `video/progetto_v3/tempi/scene_v3c_r2_en.json`. Tutto simulato: nessun sensore fisico.

## s1 · 0.0–13.3 s · Fast flight: drones on a collision course

- Etichetta: sim

| tempo | voce (EN) | sottotitolo IT |
|---|---|---|
| 3.0 | Fast aircraft and drones: a collision, an in-flight failure, a flash that blinds the cameras. | Aerei e droni veloci: una collisione, un'avaria in volo, un lampo che acceca le camere. |
| 9.9 | When the view is lost, what should the screen say? | Quando la vista si perde, che cosa deve dire lo schermo? |

## s2 · 13.3–26.1 s · Three answers per track

- Etichetta: schema

| tempo | voce (EN) | sottotitolo IT |
|---|---|---|
| 13.8 | MoVi declares what it has not observed. | MoVi dichiara ciò che non ha osservato. |
| 17.3 | Three answers per track. | Tre risposte per traccia. |
| 19.5 | I see it. | Lo vedo. |
| 20.9 | I don't see it, but here is where it can be. | Non lo vedo, ma ecco dove può essere. |
| 24.0 | Or: I don't know. | Oppure: non lo so. |

## s3 · 26.1–34.7 s · F1 · aircraft on approach, non-cooperative drone

- Etichetta: sim
- A schermo: «never 'clear' where the object or a fragment was · F6 0/200 [0; 0.019] · other cells 0/60 [0; 0.060] · sim.» (chiave `V-1`)

| tempo | voce (EN) | sottotitolo IT |
|---|---|---|
| 26.6 | In six flight scenarios with the core, MoVi never said clear where an aircraft, a drone or a fragment was. | In sei scenari di volo con il nucleo, MoVi non ha mai detto libero dove c'era un aereo, un drone o un frammento. |

## s4 · 34.7–56.0 s · F4 · failure with low-energy debris, 135 m/s

- Etichetta: sim
- A schermo: «event inferred, cameras declared unreliable within 1 s: 60/60 [0.940; 1] · optimistic trigger · sim.» (chiave `V-2`)
- A schermo: «low-energy debris inside the declared volume: 58/60 [0.886; 0.991] · sim.» (chiave `V-3`)

| tempo | voce (EN) | sottotitolo IT |
|---|---|---|
| 35.2 | An aircraft fails in flight at a hundred and thirty-five metres per second. | Un aereo va in avaria in volo a centotrentacinque metri al secondo. |
| 40.7 | MoVi infers the event and declares the cameras unreliable within one second, in sixty of sixty simulated runs. | MoVi deduce l'evento e dichiara le camere non affidabili entro un secondo, in sessanta prove simulate su sessanta. |
| 49.7 | Low-energy debris stays inside the declared volume in fifty-eight of sixty. | I detriti a bassa energia restano nel volume dichiarato in cinquantotto su sessanta. |

## s5 · 56.0–74.1 s · F3 · fast drones colliding at 40 and 35 m/s

- Etichetta: sim
- A schermo: «proximity warning at least 10 s ahead: 60/60 [0.940; 1] · 10 s threshold set after · sim.» (chiave `V-5`)
- A schermo: «true position and fragments inside the region: 60/60 [0.940; 1] · 939/939 samples · sim.» (chiave `V-6`)
- A schermo: «contact rule under test: 57/60 [0.863; 0.983] · false events in a 39 m near miss (F5) 2/60 [0.009; 0.114] · not adopted» (chiave `V-11-PROVA`)

| tempo | voce (EN) | sottotitolo IT |
|---|---|---|
| 56.5 | Two fast drones collide. | Due droni veloci si scontrano. |
| 58.8 | MoVi warns of the close pass at least ten seconds ahead, in sixty of sixty runs. | MoVi avvisa del passaggio ravvicinato almeno dieci secondi prima, in sessanta prove su sessanta. |
| 65.0 | The collision is not yet declared as an event, but the region is kept: the fragments stayed inside it in sixty of sixty runs. | La collisione non è ancora dichiarata come evento, ma la regione resta: i frammenti vi sono rimasti in sessanta prove su sessanta. |

## s6 · 74.1–83.8 s · F5 · a flash blinds every optical sensor

- Etichetta: sim
- A schermo: «optics blinded: every track keeps a region · 60/60 [0.940; 1] · identity PRESUMED · sim.» (chiave `V-10`)

| tempo | voce (EN) | sottotitolo IT |
|---|---|---|
| 74.6 | A flash blinds every optical sensor. | Un lampo acceca tutti i sensori ottici. |
| 77.8 | Radar alone keeps a region for every track, and identity is presumed. | Il solo radar mantiene una regione per ogni traccia, e l'identità è presunta. |

## s7 · 83.8–110.2 s · When continuity is lost: confidence over time

- Etichetta: SCHEMATIC + PUBLIC TRAJECTORIES|curve computed in the model · points: public flight tracks, simulated sensor
- A schermo: «in turns: 0.73 (161/221) [0.67; 0.78] · limit» (chiave `C-TAR-VIRATA`)

| tempo | voce (EN) | sottotitolo IT |
|---|---|---|
| 84.6 | When continuity is lost, MoVi computes, in the motion model, how confidence falls, and grows the region to keep nine chances in ten. | Quando la continuità si perde, MoVi calcola, nel modello del moto, come cala la confidenza, e fa crescere la regione per tenere nove probabilità su dieci. |
| 94.5 | On public flight tracks, with a simulated sensor, the region held the aircraft eighty-five to eighty-nine times in a hundred, below nine in ten, mostly one route. | Su traiettorie di volo pubbliche, con un sensore simulato, la regione ha contenuto l'aereo da ottantacinque a ottantanove volte su cento, sotto nove su dieci, soprattutto su una rotta. |
| 105.8 | In turns, seventy-three: a declared limit. | In virata, settantatré: un limite dichiarato. |

## s8 · 110.2–140.0 s · F7 · on board a moving drone: a collision nearby, radar blinded

- Etichetta: sim
- A schermo: «radar and cameras saturated together: both declared unreliable · log readout»
- A schermo: «fix under test · carrier warned before the first fragment, radar and cameras blinded: 59/59 [0.939; 1] · without 0/59 [0; 0.061] · same seeds · sim.» (chiave `F7R-C1-AVVISO`)
- A schermo: «with the fix: 'clear' on the tracked drone or a fragment 0/60 [0; 0.060] · region kept 60/60 [0.940; 1] · sim.» (chiave `F7R-C1-LIBERO`)
- A schermo: «limit · reacquisition within 2 s below the 51/60 threshold: ahead 49/60 [0.701; 0.894] · in a turn 40/60 [0.541; 0.773]» (chiave `F7R-C1-RIACQ`)
- A schermo: «limit · warning not localised: conservative sphere up to 565 m, median 8 s» (chiave `F7R-C1-LOC`)
- A schermo: «limit · false warnings if the radar saturates for another cause: 11/200 [0.031; 0.096] · sim.» (chiave `F7R-C1-FALSI`)

| tempo | voce (EN) | sottotitolo IT |
|---|---|---|
| 111.7 | Now MoVi rides on a drone, keeping the track of a fast drone ahead. | Ora MoVi è a bordo di un drone e mantiene la traccia di un drone veloce più avanti. |
| 116.8 | Nearby, two drones collide: flash, smoke, debris. | Accanto, due droni si scontrano: lampo, fumo, detriti. |
| 120.9 | Radar and cameras are blinded together. | Radar e camere si accecano insieme. |
| 124.2 | With a fix under test, MoVi warns the carrier at once, before the first fragment, in fifty-nine of fifty-nine runs, against none without it. | Con una correzione in prova, MoVi avvisa subito il portatore, prima del primo frammento, in cinquantanove prove su cinquantanove, contro nessuna senza. |
| 134.2 | A promising path: the warning does not say where. | Una strada promettente: l'avviso non dice dove. |

## s9 · 140.0–152.0 s · Also: the site with taxiing aircraft and drones, and other uses

- Etichetta: SIMULATION (site) · SCHEMATIC (short range)|Simulated · state-of-the-art sensor parameters assumed · no physical sensor

| tempo | voce (EN) | sottotitolo IT |
|---|---|---|
| 140.5 | The same approach works on a site: a drone behind a building, warned in time in two hundred of two hundred runs. | Lo stesso approccio funziona in un sito: un drone dietro un edificio, avvisato in tempo in duecento prove su duecento. |
| 148.1 | And at short range: people, cars, trains. | E a corto raggio: persone, auto, treni. |

## s10 · 152.0–174.4 s · Limits, and what comes next

- Etichetta: SCHEMATIC · ESTIMATE|limits from the verdicts · hardware figure is an estimate by analogy

| tempo | voce (EN) | sottotitolo IT |
|---|---|---|
| 152.5 | The limits: everything is simulated, with no physical sensor, and classes are labelled by hand. | I limiti: tutto è simulato, senza sensori fisici, e le classi sono etichettate a mano. |
| 159.2 | Next: a contact rule for fast collisions, state-of-the-art sensors, dedicated hardware, field trials. | Poi: una regola di contatto per le collisioni veloci, sensori allo stato dell'arte, hardware dedicato, prove sul campo. |
| 166.7 | MoVi observes and warns. | MoVi osserva e avvisa. |
| 169.5 | By SDMs. | Di SDMs. |

