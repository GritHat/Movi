# MoVi pitch v3c: registro delle cifre a schermo

Fonte: `video/progetto_v3/cifre_v3c.json` (blocco del verdetto finale §8 + chiavi F7R-C1-* dai rapporti c1). Ogni cifra a schermo ha intervallo e stato. Tutto simulato.

| chiave | a schermo | stato | fonte |
|---|---|---|---|
| `C-TAR-1-2` | 1–2 s: 0.89 (655/733) [0.87; 0.91] · cases correlated | su dati pubblici, sensore simulato | f20/02-taratura/TARATURA.md §3; f20/10-attacco/riconto_taratura.txt |
| `C-TAR-BANDA` | 0.85–0.89 from 1 to 30 s · 21–30 s: 0.85 [0.81; 0.88] · 89.5% of cases from 4 flights of one route | su dati pubblici, sensore simulato; 89.5% of cases from 4 flights of one route | f20/10-attacco/ATTACCO_FINALE.md §4 |
| `C-TAR-VIRATA` | in turns: 0.73 (161/221) [0.67; 0.78] · limit | su dati pubblici; limite | f20/02-taratura/TARATURA.md §3 |
| `F7R-C1-AVVISO` | fix under test · carrier warned before the first fragment, radar and cameras blinded: 59/59 [0.939; 1] · without 0/59 [0; 0.061] · same seeds · sim. | simulato; sostenuto dai dati; strada promettente, non adottata come risultato definitivo | f20/05-scorta/correzione_f7r/CORREZIONE.md; verifica/VERIFICA.md (confronto appaiato, costo.txt, attacco F7c) |
| `F7R-C1-FALSI` | limit · false warnings if the radar saturates for another cause: 11/200 [0.031; 0.096] · sim. | simulato; robustezza smentita sotto interferenza | f20/05-scorta/correzione_f7r/CORREZIONE.md; verifica/VERIFICA.md (confronto appaiato, costo.txt, attacco F7c) |
| `F7R-C1-LIBERO` | with the fix: 'clear' on the tracked drone or a fragment 0/60 [0; 0.060] · region kept 60/60 [0.940; 1] · sim. | simulato | f20/05-scorta/correzione_f7r/CORREZIONE.md; verifica/VERIFICA.md (confronto appaiato, costo.txt, attacco F7c) |
| `F7R-C1-LOC` | limit · warning not localised: conservative sphere up to 565 m, median 8 s | simulato; limite | f20/05-scorta/correzione_f7r/CORREZIONE.md; verifica/VERIFICA.md (confronto appaiato, costo.txt, attacco F7c) |
| `F7R-C1-RIACQ` | limit · reacquisition within 2 s below the 51/60 threshold: ahead 49/60 [0.701; 0.894] · in a turn 40/60 [0.541; 0.773] | simulato; P2 smentita (limite) | f20/05-scorta/correzione_f7r/CORREZIONE.md; verifica/VERIFICA.md (confronto appaiato, costo.txt, attacco F7c) |
| `HW-CALC` | dedicated processing estimated 0.08–1.2 ms (estimate by analogy, not a measurement); the sensor revisit dominates | ipotesi (analogia) | f19-volo/02-sensori-hw/latenza.json; VERDETTO_VOLO K-707 |
| `LP-1` | warned in time: 200/200 [0.981; 1] · sim. | simulato | f15-lunga-portata/60-fase2c/02-verdetto/VERDETTO_2C.md |
| `LP-4` | warned in time with three fused sensors: 200/200 [0.981; 1] · sim. | simulato | VERDETTO_2C |
| `V-1` | never 'clear' where the object or a fragment was · F6 0/200 [0; 0.019] · other cells 0/60 [0; 0.060] · sim. | simulato | f19-volo/10-prove/passaggi_volo_v3i.jsonl; f20/01-contatto/valutazione_v4c.jsonl; f20/20-verdetto/riconto_finale.txt |
| `V-10` | optics blinded: every track keeps a region · 60/60 [0.940; 1] · identity PRESUMED · sim. | simulato | VERDETTO_VOLO §2.1 V-10 |
| `V-11-PROVA` | contact rule under test: 57/60 [0.863; 0.983] · false events in a 39 m near miss (F5) 2/60 [0.009; 0.114] · not adopted | simulato (regola in prova, limite) | f20/01-contatto/CONTATTO.md §2; riconto_finale.txt |
| `V-2` | event inferred, cameras declared unreliable within 1 s: 60/60 [0.940; 1] · optimistic trigger · sim. | simulato (innesco ottimista) | VERDETTO_FINALE §2.1 V-2; riconto_finale.txt F4 |
| `V-3` | low-energy debris inside the declared volume: 58/60 [0.886; 0.991] · sim. | simulato | VERDETTO_VOLO §2.1 V-3 |
| `V-5` | proximity warning at least 10 s ahead: 60/60 [0.940; 1] · 10 s threshold set after · sim. | simulato | VERDETTO_VOLO §2.1 V-5 |
| `V-6` | true position and fragments inside the region: 60/60 [0.940; 1] · 939/939 samples · sim. | simulato | VERDETTO_VOLO §2.1 V-6 |

Numeri a schermo senza chiave (letti dal registro della simulazione, per fotogramma): t, raggio della regione del drone seguito, raggio della sfera prudente (`registro_F7r_c1_totale.jsonl`, idx 0, seme 20261124, att), confidenza calcolata nel modello.

