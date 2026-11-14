# Effetti di meteo, fumo, fiammata e detriti sui sensori simulati

`sciame-sensori`, f15-lunga-portata/40-eventi/01-effetti, 15 novembre 2026 (orologio della macchina). File per il
simulatore: `effetti_eventi.json` (11 effetti, nomi dei sensori di `02-sensori/parametri_lunga_portata.json`, campi
`[valore, unità, fonte]`, coppie = `[nominale, prudente]`). Conti: `timeout 60 python3 -I conti.py` (esito in
`conti_esito.txt`). **Niente è validato: tutto è conto, scheda o ipotesi; nessun sensore fisico.** Solo osservazione,
monitoraggio e avviso.

## 1. Cambi di stato e regole violate

- **Previsioni** (`PREVISIONI.md`, scritte alle 00:12, conti eseguiti alle 00:14): sette, **tutte reggono**. P1 (P.838-3 a
  10 GHz: k = 0,01217, α = 1,2571) è un controllo di trascrizione, non indipendente: stessa tabella. P2 (77 GHz,
  25 mm/h: 11,4 dB/km contro «circa 10» della rassegna) e P3 (Kim, 905 nm, 0,5 km: 34,0 dB/km contro «circa 35»)
  confrontano due fonti diverse. P4: sfera di 2 cm = −35,0 dBsm.
- **Fonti: tre stati.** **A** = aperta e letta oggi: Nadeem e Leitgeb 2010 (leggi di Kruse e Kim), la rassegna
  arXiv:2112.08936, i coefficienti P.838-3 dalla pagina di itu-rpy. **S** = solo il riassunto del motore di ricerca,
  pagina non aperta: P.840, i requisiti FAA sui detriti a terra, le sezioni radar dei droni, le prove d'urto, i
  microbolometri, il fumo. **Ipotesi** = nessuna fonte. La consegna chiedeva «pagina aperta oggi»: per le fonti S
  **non è rispettata** e va detto a chi le cita.
- **Non aperte:** FAA AC 150/5220-24 (errore 403), la relazione FAA sul radar mobile (pagina vuota), l'esperimento a
  più sensori nel fumo di Ladstädter 2023 (file troppo grande). Non trovati: la legge di Carbonneau per la pioggia
  nell'ottico, un valore di P.840 a 77 GHz, studi con numero e massa dei frammenti di una collisione fra droni, tempi
  di rientro dell'esposizione automatica. Sono tutti «ipotesi» nel file.
- **Nessuna fonte per il radar nella fiammata** (né «nessun effetto», né plasma): **non verificato**, e così è scritto.
- 219 campi con fonte, 38 marcati ipotesi o non verificati; ma molti «conto» poggiano su ipotesi (soglie di
  contrasto, riferimento del radar a 0,01 m², Kl della nebbia): il numero sottostima.
- Il LiDAR spetta all'esperto hardware di LiDAR: qui solo propagazione e soglie, da fargli rivedere.

## 2. Meteo: leggi e portate

**Ottico (camere, LiDAR).** γ [dB/km] = (17/V) · (λ/550 nm)^(−q), V visibilità in km; q di Kim: 1,3 (6–50 km),
0,16V + 0,34 (1–6), V − 0,5 (0,5–1), **0 sotto 0,5 km** (fonte A). In nebbia la lunghezza d'onda non conta: 905 e
1550 nm, e nel modello anche il termico, perdono uguale. Per 4 e 10 µm la legge è **estrapolata** (ipotesi); il
caso prudente usa q = 0 sempre. **Radar in pioggia:** γ = k·R^α (P.838-3). **Radar in nebbia:** γ = Kl·M, con M =
0,05 g/m³ a ~300 m di visibilità e 0,5 g/m³ a ~50 m (S); Kl = 0,09 e 4 (dB/km)/(g/m³) a 9,4 e 77 GHz è ipotesi.

| dB/km, sola andata | pioggia 4 / 25 / 50 mm/h | nebbia V = 300 m / 50 m | neve forte |
|---|---|---|---|
| Radar 3 GHz | 0,001 / 0,007 / 0,017 | 0,001 / 0,005 (i) | trascurabile (i) |
| Radar 9,4 GHz | 0,055 / 0,59 / 1,44 | 0,004 / 0,045 (i) | 0,09 (i) |
| Radar 77 GHz | 3,1 / 11,4 / 18,8 | 0,2 / 2,0 (i) | ~6 (rassegna, A) |
| Ottico, 550–1550 nm | 2,7 / 9,3 / 14,8 (i) | 57 / 340 | 34–170 (V = 0,5–0,1 km) |

**Portata** (frazione di quella in aria limpida, nominale | prudente). Sensori attivi: R^n · 10^(2γR/10) = R₀^n,
n = 2 LiDAR su bersaglio esteso, n = 4 radar. Camere: R = 10·log(C₀/C_soglia)/γ; soglie ipotesi (EO: 0,5 e 2 % |
0,3 e 5 %; termica: trasmissione minima 0,1 | 0,3).

| Sensore (R₀) | foschia 4 \| 2 km | nebbia 300 \| 200 m | nebbia fitta 100 \| 50 m | pioggia 25 \| 50 mm/h | neve 500 \| 100 m |
|---|---|---|---|---|---|
| LiDAR tele 905 nm (320 m) | 0,85 \| 0,66 | 0,29 \| 0,23 (94 \| 75 m) | 0,15 \| 0,09 | 0,64 \| 0,55 | 0,38 \| 0,15 |
| LiDAR 1550 nm, ipotetico (320 m) | 0,90 \| 0,66 | 0,29 \| 0,23 | 0,15 \| 0,09 | 0,64 \| 0,41 | 0,38 \| 0,15 |
| Camera EO (2 km pratici) | 1,00 \| 0,46 | 0,12 \| 0,05 (247 \| 92 m) | 0,04 \| 0,01 | 0,75 \| 0,26 | 0,21 \| 0,02 |
| Termica onda media e lunga (1,2 km) | 1,00 \| 0,51 | 0,15 \| 0,05 (177 \| 62 m) | 0,05 \| 0,01 | 0,90 \| 0,29 | 0,25 \| 0,03 |
| Radar 77 GHz (300 m) | 1,00 | 0,99 | 0,97 \| 0,94 | 0,75 \| 0,65 | 0,91 \| 0,84 |
| Radar per droni, banda X (3100 m) | 1,00 | 1,00 | 0,99 \| 0,98 | 0,84 \| 0,70 | 0,98 \| 0,97 |
| Radar banda S, ipotetico (10 km) | 1,00 | 1,00 | 1,00 \| 0,99 | 0,99 \| 0,98 | 0,99 |

Tre cose da leggere nella tabella. **(a)** In nebbia e neve le camere e il LiDAR scendono a decine o poche centinaia
di metri; il radar quasi non se ne accorge. **(b)** Il vantaggio del termico vale solo in foschia (nominale); in
nebbia vera il modello non gliene dà: è la scelta prudente, non un fatto misurato qui. **(c)** La pioggia forte è
l'unica condizione che tocca il radar: −16 % | −30 % in banda X, −25 % | −35 % a 77 GHz.

**Falsi ritorni.** *Pioggia sul radar* (formula da manuale, ipotesi: η = π⁵·0,93·Z/λ⁴, Z = 200·R^1,6): in una cella
di 1° × 10° × 3 m (ipotesi) a 1 km la pioggia a 25 mm/h vale 0,068 m², cioè **6,8 volte un multirotore da 0,01 m²**;
a 3 km 61 volte. Senza filtro Doppler il drone è sommerso; il file dà 25 | 15 dB di cancellazione (ipotesi). È
l'effetto che pesa di più sul radar e non sta nell'attenuazione. *LiDAR:* gocce e spruzzi danno «fantasmi», i fiocchi
di neve falsi punti isolati, sotto 10 m di visibilità il blocco è quasi totale (rassegna, A); le frazioni nel file
(0,1–5 % dei punti) sono ipotesi.

## 3. Fumo e polveri

Modello: nube con profondità ottica nel visibile τ = 5 | 10 lungo la corda (ipotesi); τ(λ) = τ·550/λ per fuliggine
fine (ipotesi) | prudente: nessun vantaggio fino a 1550 nm, 0,5 a 4 µm, 0,2 a 10 µm (agglomerati, polvere). Camere:
exp(−τ); LiDAR: exp(−2τ). Unica evidenza trovata (S): nei grandi incendi la visibilità scende a decine di piedi,
l'infrarosso è attenuato dell'ordine di 1 per km, il radar molto meno.

| Oggetto dietro la nube | nominale | prudente |
|---|---|---|
| Camera EO | non osservato (T = 0,7 %) | non osservato |
| LiDAR 905 / 1550 nm | non osservato (0,2 % / 2,9 %) | non osservato |
| Termica onda media | osservato (T = 50 %) | **non osservato** |
| Termica onda lunga | osservato (T = 76 %) | **non osservato** (T = 13 %) |
| Radar (ogni banda) | osservato | osservato |

**Dimensioni e durata (ipotesi, ordini di grandezza):** due multirotori piccoli, raggio 3 | 10 m per 20 | 120 s;
avaria di un motore d'aereo, raggio 20 | 50 m per 60 | 300 s, scia di 300 | 1000 m. Regola per il simulatore: il
volume della nube e il cono d'ombra dietro sono «non osservato» per i sensori che non passano; il fronte della nube
dà al LiDAR ritorni veri di «qualcosa di opaco», non un falso allarme.

## 4. Fiammata e lampo

| Sensore | Effetto | Cecità oltre la sorgente | Fonte |
|---|---|---|---|
| Camera EO | saturazione (20 % \| 100 % del quadro: il campo è 2,7°), alone 2–5 volte la sorgente | 0,5 \| 2 s (rientro dell'esposizione) | effetto: A (rassegna); numeri: ipotesi |
| Termica | la fiamma supera la dinamica (~200 °C); immagine ferma < 0,5 s al cambio di guadagno; impronta residua | 1 \| 10 s | S; durate: ipotesi |
| LiDAR | area senza ritorni attorno alla sorgente (provato a 200 klx); cono cieco 1° \| 5° | 0 \| 1 s | effetto: A; numeri: ipotesi |
| Radar | nessun effetto modellato | 0 | **non verificato** |
| Cooperativi | la radio non è toccata; il mezzo danneggiato può tacere | — | 02-sensori |

Durata della sorgente (ipotesi): batteria al litio 2 | 10 s; fiammata di motore 0,5 | 3 s. **Come se ne accorge
(«salute del sensore», soglie ipotesi):** pixel al fondo scala > 5 % (termica 2 %); salto del livello medio > 50 %
fra due quadri (lampo); energia dei bordi dimezzata rispetto alla media di 10 s (nebbia, fumo, lente bagnata);
LiDAR: ritorni oltre 50 m calati del 30 %, o > 2 % dei raggi con ritorno sotto 20 m; radar: fondo salito di 6 dB.
Quando scatta, il sensore chiama `affidabilita_persa` di `movi_lp.py`: le sue celle tornano «non osservato», gli
avvisi restano; rientra dopo 10 quadri buoni **e** dopo aver riguardato. La salute accorcia la portata dichiarata,
non la allunga mai. Limite: usa gli stessi dati del sensore, quindi non vede un guasto che lascia un'immagine
plausibile.

## 5. Detriti

**In volo (ipotesi, salvo dove detto).** Collisione fra due multirotori di ~1 kg: 2 corpi di ~30 cm che cadono
quasi interi (S: in una prova a 383 km/h contro un'ala il drone «non si è frantumato»), 8 | 40 frammenti di
5–15 cm (eliche, bracci, batteria), 20 | 200 schegge sotto 5 cm. Avaria di motore: 10 | 100 pezzi di 5–50 cm; nessuna
distribuzione trovata (AC 20-128A, S, conta solo 676 eventi non contenuti). Caduta da 100 m (conto su ipotesi): corpo
5,9 s, braccio con motore 7,9 s, frammento d'elica 17,7 s, con 59–177 m di deriva a 10 m/s di vento.

**A quale distanza si vede un frammento** (nominale | prudente; `conti.py` § 6):

| Frammento | Sezione radar (metallo \| −10 dB) | Radar per droni | LiDAR tele | Camera EO, già puntata | Termica |
|---|---|---|---|---|---|
| 5 cm | 0,0020 \| 0,0002 m² (−27 dBsm) | 2,1 \| 1,2 km | 137 \| 115 m | 2,2 \| 0,5 km | 208 m \| 0 |
| 10 cm | 0,0079 \| 0,0008 m² | 2,9 \| 1,6 km | 193 \| 163 m | 4,3 \| 1,1 km | 417 m \| 0 |
| 30 cm | 0,071 \| 0,007 m² | 5,1 \| 2,8 km | 320 \| 226 m | 13 \| 3,3 km | 1250 m \| 0 |

Avvertenze: la sezione radar è quella di una sfera metallica (limite alto per plastica e carbonio, da cui i −10 dB,
ipotesi); il riferimento del radar (0,01 m² a 3100 m, Pd 0,5) è l'ipotesi di 02-sensori; un drone intero vale
0,02 m² in mediana e 0,004 nell'angolo peggiore (S, blog). Le distanze delle camere sono limiti geometrici (2 | 8
pixel), di giorno, con il campo di 2,7° già sul punto; la termica vede solo frammenti caldi. Il radar ha una
rivisita di 1 s e avvia una traccia in 2–3 giri: un corpo che cade in 6 s dà **3–6 misure**, un'elica ne dà 17 ma
è sotto soglia oltre ~1 km. Conclusione operativa: i frammenti non si seguono uno a uno; l'evento diventa un
**volume di possibile presenza** che cresce con (velocità relativa + vento)·t e scende fino al suolo.

**A terra («FOD»).** Requisiti FAA AC 150/5220-24 come li riporta una fonte secondaria (S; la circolare oggi dà
403): rilevare un cilindro metallico di 3,0 × 3,8 cm e una sfera di 4,3 cm, almeno 9 oggetti su 10 del gruppo di
prova, posizione entro 5 m, al più 1 falso allarme al giorno (3 senza conferma visiva); un radar fisso a onde
millimetriche vede il cilindro fino a ~1 km. Sistemi: radar fisso a ~94 GHz con camera (Tarsier, S), radar mobile su
veicolo (FOD Finder, S), ibrido sulle luci di bordo (FODetect) e solo ottico (iFerret) a memoria, non aperti. Ricerca
(S): sfera di 50 mm a ~660 m a 93 GHz; cilindro da −20 dBsm fino a 35 m a 76,5 GHz; un piccolo drone con camera
rileva il 96 % degli oggetti della circolare. **Nessun sensore a lunga portata di 02-sensori basta:** il radar del
movimento a terra ha celle di 3 × 15 m e non vede i detriti. Dopo un evento sopra una pista la striscia sotto il
volume di caduta resta «possibili detriti» fino a un'ispezione con un sensore capace.

## 6. Che cosa resta osservato, e con quale combinazione

| | Nebbia, neve | Pioggia forte | Fumo (dietro la nube) | Fiammata | Detriti in volo | Detriti a terra |
|---|---|---|---|---|---|---|
| Camera EO | no oltre ~0,1–0,25 km | sì, 0,75 \| 0,26 | **no** | **no**, sorgente + 0,5 \| 2 s | ≥ 5 cm se puntata | no (serve un sistema dedicato) |
| Termica | no oltre ~0,06–0,18 km | sì, 0,90 \| 0,29 | sì \| **no** | **no**, + 1 \| 10 s | solo se caldi | no |
| LiDAR | no oltre 30–95 m | sì, 0,64 \| 0,55 | **no** (vede il fronte) | no nel cono 1° \| 5° | sotto 140–320 m | no a lunga distanza |
| Radar 77 GHz | sì | sì, 0,75 \| 0,65 | sì | sì (non verificato) | portata corta | solo dedicato |
| Radar X o S | sì | sì (X 0,84 \| 0,70), con filtro Doppler | sì | sì (non verificato) | ≥ 5 cm entro 1–2 km | no |
| Cooperativi | sì, chi trasmette | sì | sì | sì | **no** (chi è rotto tace) | no |

**L'argomento per il multisensore.** Nessun sensore regge in tutte le colonne. Il radar tiene **esistenza, distanza
e velocità radiale** in nebbia, fumo e fiammata, ma non identifica, soffre la pioggia (ritorno di volume) e ha una
rivisita di 1 s. Le camere danno identità e conferma, e sono le prime a cadere. Radar + una camera (EO o termica) +
cooperativi lascia almeno «c'è qualcosa, qui» in ogni evento; ciò che si perde (identità, frammenti sotto 5 cm,
tutto ciò che sta dietro una nube per l'ottico, il suolo sotto una caduta) deve restare **«non osservato» con
l'avviso acceso**. Nessun effetto di questo modello dichiara libero un volume: possono solo togliere osservazione.

## 7. Stati proposti, proposte, e dopo

- **Sostenuto da un conto, non da una misura:** le portate della tabella del § 2; le distanze dei frammenti.
- **Non risolto:** il termico attraverso fumo e nebbia (nominale e prudente danno esiti opposti: lo deciderebbe una
  misura di trasmissione a 10 µm in fumo noto, per esempio l'esperimento di Ladstädter 2023, non aperto); il radar
  nella fiammata; numero e dimensione dei frammenti.
- **sensori-ev-1 (proposta):** nel video, la pioggia forte va mostrata come **perdita del drone piccolo sul radar**
  oltre 1–3 km, non come attenuazione. Previsione: con 15 dB di cancellazione il residuo a 3 km e 25 mm/h è
  0,019 m², sopra 0,01 m². La smentisce una scheda che dichiari la portata in pioggia con il filtro acceso.
- **sensori-ev-2 (proposta):** il simulatore usi sempre i valori **prudenti** per decidere «osservato» e i nominali
  solo per il disegno: un errore di modello così accende avvisi in più, mai in meno.
- **Dopo:** aprire le fonti S più pesanti (AC 150/5220-24, P.840, Ladstädter); far rivedere le righe del LiDAR
  all'esperto hardware di LiDAR; concordare con chi scrive il simulatore i nomi dei campi (qui: ipotesi mie, perché
  `10-simulatore` non esisteva ancora).
