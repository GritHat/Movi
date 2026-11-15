# MoVi pitch v4 — storyboard del video completo (obiettivo 170 s, massimo 176 s)

Stile: fondo chiaro (cielo #CFE4FB → #F7FAFE), inchiostro blu notte #0B1F3A, accento blu #1F6FEB (ciò che MoVi dichiara),
verde acqua #00A389 (esiti), ambra #FF8A1F (avvisi). Illustrazioni vettoriali piatte: droni, aereo, auto, persone, satellite.
Una sola idea per scena, titoli grandi, nessun grafico di punti, nessun contatore che corre.
Riga fissa in basso a sinistra: «SIMULATED PROTOTYPE · ILLUSTRATION». Il tempo rallentato è scritto a schermo («time ×0.1»).
Voce: inglese, Kokoro `bm_george`, circa 2,3 parole al secondo. Circa 330 parole in tutto.

Le cifre vengono da `video/consegna/MoVi_registro_cifre_final.md` (chiave fra parentesi quadre). Tutte sono di simulazione.

| # | Tempo | Immagine | Voce (inglese) |
|---|---|---|---|
| 1 Aggancio | 0–10 s | Cielo chiaro. Un drone entra in una nuvola e sparisce. Titolo: «What you stop seeing is still there.» | "A drone flies into a cloud. For most systems, it is gone. But what you stop seeing is still there." |
| 2 Idea | 10–24 s | Attorno alla nuvola cresce piano una regione blu tratteggiata: «it can be anywhere in here». Tre pillole: «Declares where it can be», «Confidence fades with time», «Never says "clear" without looking». | "MoVi is a perception system for uncrewed vehicles. It keeps track of what it can no longer see: it declares a region where the object can be, with a confidence that fades with time. It never calls a place clear unless it has looked. And when it stops being reliable, it says so." |
| 3 Caso 1: volo veloce | 24–50 s | Un aereo in volo veloce (strisce di velocità), due droni accanto. Un motore si guasta: fumo, l'aereo devia. «time ×0.1». Le camere si oscurano; pillola «Cameras unreliable: declared within 1 s». La regione blu segue l'aereo. Numeri grandi: «60 of 60» [V-2], «10 s ahead · 60 of 60» [V-5]. | "First case: fast flight. Things happen in a fraction of a second, so we slow time down. An engine fails. Smoke covers the cameras. In sixty of sixty simulated runs MoVi declared its cameras unreliable within one second, and kept a region for every aircraft. And the proximity warning came at least ten seconds ahead, sixty times of sixty." |
| 4 Caso 2: scena eroe F7r | 50–95 s | Un drone (blu) segue un oggetto veloce; linea di vista tratteggiata. Due droni si scontrano in mezzo: lampo, fuoco, fumo, detriti. «time ×0.1». Etichette «CAMERAS · BLINDED», «RADAR · BLINDED». L'oggetto sparisce nel fumo: compare la regione blu «MoVi: the target is in here». Un frammento rosso va verso il drone: anello ambra, «WARNING SENT». Poi due numeri grandi: «59 of 59 — carrier warned before the first fragment (promising result · correction under test)» [F7R-C1-AVVISO]; «60 of 60 — target region kept; never called "clear" where the drone or a fragment was» [F7R-C1-LIBERO]. | "Second case. A drone follows a fast object. Right next to it, two drones collide: fire, smoke, debris. We slow time to one tenth. Cameras blinded. Radar blinded. MoVi does not guess, and it does not forget: it keeps the region where the target must be, and it warns its own drone at once. In simulation, with our latest correction, the warning arrived before the first fragment in fifty-nine runs of fifty-nine. The target's region was kept sixty times of sixty. And MoVi never called clear a place where the drone or a fragment was." |
| 5 Prove | 95–115 s | Titolo «Built on evidence, not on promises.» Quattro schede: «100+ pages of technical report · proofs and test results»; «400+ references studied · literature, maths, experiments»; «60/60 sensor failure declared within 1 second» [V-2]; «200/200 warned in time · long range» [LP-1]. | "Behind this there is a technical report of more than one hundred pages, with mathematical proofs and the results of every test. And a deep study: more than four hundred references, across the literature, the mathematics and the experiments. Every number you have seen comes from there." |
| 6 Scenari | 115–158 s | Sei tavole da 7 s, ciascuna con l'etichetta «POSSIBLE APPLICATION» e la stessa regione blu: (a) una persona non vedente e l'auto dietro l'angolo; (b) una macchina industriale che si ferma prima dell'operatore; (c) l'auto e il pedone dietro il furgone parcheggiato; (d) un'auto di pattuglia che non perde di vista l'auto seguita dietro un edificio; (e) un satellite e il frammento pericoloso nella nube di detriti; (f) un drone FPV fra pioggia e fumo. | "The same idea can protect people wherever sight is lost. A blind person, warned of the car they cannot see. A machine that stops before it reaches its operator. A car that remembers the pedestrian behind the parked van. A patrol that does not lose sight in a pursuit. A satellite that spots the dangerous fragment inside a cloud of debris. A fast drone that finds its way through rain and smoke. These are possible applications: one idea, many lives." |
| 7 Chiusura | 158–170 s | Marchio MoVi, frase «It keeps track of what it stops seeing.», logo SDMs, «THE BIG HACK 2026 · RITORNO AL FUTURO REMOTO · CITTÀ DELLA SCIENZA». | "MoVi. It keeps track of what it stops seeing. By SDMs, at The Big Hack twenty twenty-six." |

## Che cosa è simulato o illustrativo

- Tutte le immagini sono illustrazioni: nessuna ripresa, nessun dato per fotogramma. Lo dice la riga fissa a schermo.
- Tutte le cifre sono di simulazione. «59 of 59» è un risultato promettente, con la correzione ancora in prova: lo dice lo schermo.
- Gli scenari della scena 6 sono applicazioni possibili, non risultati: lo dice l'etichetta di ogni tavola.

## Non incluso

- L'indagine sui progetti di R&D del committente: in `documentazione/RIFERIMENTI.md` ci sono pagine e comunicati del committente fra i riferimenti, ma né lì né in `documentazione/STATO_PROGETTO.md` risulta un'indagine sui suoi progetti di R&D. Non è nel video.

## Il campione (62 s, muto, sottotitoli a schermo)

`sh video/progetto_v4/rendi.sh draft video/rendering/<nome>.mp4` rende `index.html` (HyperFrames, 24 fotogrammi al secondo).
Contiene: aggancio e idea (0–14 s), scena eroe F7r (14–36 s), prove (36–46 s), tre scenari (46–58 s), chiusura (58–62 s).
Mancano: caso 1, tre scenari, voce e musica.
