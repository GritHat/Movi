# Consegna — `nuvole-punti-f9` — strategia S10 (mappa a tre fasce di quota)

Lavoro dalle 2026-11-14T15:38:52 alle 15:55 (`date -Is`). Cartella: `f9-preproposta/08-nuvole-punti/`. Per rifare: `sh rifai.sh` (tre lanci, ognuno sotto i 30 s).

## In testa: scostamenti e regole violate

- **Ore scritte a mente.** In `PREVISIONI.md` avevo scritto «15:44» e «15:52» senza leggerle da `date -Is`; la seconda era sbagliata. Corrette nel file con le ore vere (15:42:29–15:45:20). Le previsioni restano anteriori al primo lancio (15:48:09).
- **Aggiunte dopo il primo lancio** (quindi *notate dopo*, non previste): la variante «per differenze» **F3d**, la misura del volume dentro il cuneo d'ombra, il profilo con franco 1,8 m, la spazzata della distanza, il montaggio verticale. Il primo lancio è conservato in `risultati_1.txt` (`fasce_v1.c`).
- **Che cosa è la prova.** Un simulatore mio in C (`fasce.c`): camera ideale 87°×58°, 640×480, a 1,2 m, inclinata di 15°, scatole e pareti, un fotogramma. **Nessun fotogramma vero.** Mappe e verità usano lo stesso lancio di raggi: un errore di geometria sarebbe comune. Controllo a parte: il conto a mano (1,24 / 1,09 / 2,41 m) coincide con la spazzata (scatola a 0,90 m: 0 pixel; a 0,95 m: 114). Con il nucleo condivido la specifica del montaggio e il modello linguistico, non il codice. Rete non usata: nessuna fonte esterna aperta.
- Non ho letto le altre cartelle di f9, né f7 e f8 (solo i contratti).

## 1. Verdetto proposto su S10

**Approvata con correzioni**, in tre parti distinte.

| Parte | Verdetto | Prova |
|---|---|---|
| Tre fasce di quota per cella, con «libero» solo se le fasce del profilo sono osservate e libere | **approvata con correzioni** (le sei del §4). Stato: sostenuta dai dati **in simulazione**; da provare sull'hardware (lettera P del documento) | con la regola stretta: 0 celle «libero» sopra un solido in 15 scene (13 senza rumore, 2 con); con la regola come scritta: falsi «libero» in 4 scene mirate su 4 |
| «Chiude il buco sotto 1,1 m», «copertura completa degli ostacoli bassi» | **respinta** | scena C: la scatola di 15 cm a 0,8 m ha **0 pixel** in ogni mappa, voxel compreso |
| Passaggio automatico alla voxel (scheda grafica, o ciclo ≤ 45 ms) | **respinta come automatismo**; la voxel resta un'opzione scelta all'avvio, da provare sull'hardware | la voxel a 10 cm gira in 23 ms su un filo di CPU e non aggiunge sicurezza; la sua regola abituale dà più «libero» sul non visto delle tre fasce corrette |

## 2. I numeri

Dominio: 0,3–3 m, 87 settori da 1°, quota 0–2 m; parete di fondo a 4,5 m; senza rumore. **N-cuneo** = nucleo alla lettera (tutto in ombra oltre il primo ritorno); **N-cella** = nucleo con «libero» dove il suolo si rivede (audit, ipotesi 5); **F3-lett** = tre fasce come scritte (0,15–0,60 / 0,60–1,60 / 1,60–2,00 m; osservata = un raggio la attraversa); **F3-corr** = versione del §4; **V10** = voxel cartesiano a 10 cm con la regola abituale (libero = un raggio lo attraversa); **V10p** = voxel cilindrico a 10 cm con la regola stretta. Profili: BMA (0–2 m), BM (0–1,6 m), M (0,6–1,6 m). File: `risultati_2.txt`.

| Misura | N-cuneo | N-cella | F3-lett | F3-corr | V10 | V10p |
|---|---|---|---|---|---|---|
| **C**, scatola 15 cm a 0,8 m (0 pixel): celle dell'impronta «libero», BM (su 22) | 0 | 0 | **22** | 0 | 0 | 0 |
| **B**, sbarra a quota 1,8 m a 2 m (0 pixel): celle sotto «libero», BMA (su 53) | **53** | **53** | **53** | 0 | 0 | 0 |
| **A**, persona accovacciata dietro la cassa (0 pixel): impronta «libero», BMA e BM (su 48) | 0 | 0 | 0 | 0 | 0 | 0 |
| idem, profilo M (mezzo a quota del busto) | 0 | 0 | **48** | 0 | 0 | 0 |
| **A**, persona in piedi (10 354 pixel): celle «occupato» / «nascosto» | 0 / 48 | 13 / 35 | 13 / 35 | 13 / 35 | 13 / 35 | 13 / 35 |
| **A**, vuoto visto dichiarato nascosto nel cuneo (litri; visti 1595 su 3484) | 1595 | 1088 | 0 | 1317 | 163 | 236 |
| **D**, gradino di 10 cm: celle «libero», BM (su 182) | 0 | 0 | **182** | 0 | 0 | 0 |
| **T**, tavolo: «libero» BM su colonne non viste per intero (m²) | 0,87 | **1,84** | 2,87 | 0,25 | 0,61 | 0,00 |
| Stanza vuota: «libero» BMA / BM / franco 1,8 m (m²) | 5,48 / 5,48 / 5,48 | uguale | 4,34 / 6,51 / 4,34 | **0** / 4,86 / **0** | 0,21 / 5,22 / 2,83 | 0 / 4,62 / 1,97 |
| Stanza vuota: «libero» su volume mai visto (litri, su 2719) | 1525 | 1525 | 1471 | 7 | 306 | 2 |
| Stanza vuota: vuoto visto dichiarato nascosto (litri, su 10 810) | 1368 | 1368 | 27 | **2531** | 27 | 298 |
| Senza pareti entro la portata: «libero» BM (m²) | 5,48 | 5,48 | 6,51 | **0** | 0 | 0 |
| Tempo per fotogramma, mediana di 200 (ms) | 0,25 | — | 28,1 | 28,6; **1,11** per differenze | 23,4 | 32,8 |
| Memoria (kB) | 13 | 13 | 125 | 64 + 1867 di tabelle fisse | 220 | 791 |

Con rumore (σ = 1,5 cm a 2 m, 2 % di pixel non validi, seme 20261114) gli esiti sulle impronte non cambiano: persona nascosta 0 «libero» su 48, gradino 182 «occupato» su 182 per F3-corr; F3-lett resta a 182 «libero» sul gradino.

## 3. Critiche

1. **Il limite «1,09 m» è una distanza, e le fasce non lo toccano.** (1,2 − 0,15) / tan(15° + 29°) = 1,087 m: sotto quella distanza la cima di un oggetto di 15 cm sta sotto il bordo inferiore del campo. Scena C: 0 pixel. Nessuna struttura dati crea pixel. Lo chiude solo il montaggio o un sensore in basso: camera ruotata di 90° (58°×87°): la stessa scatola ha 4684 pixel, suolo visto da 0,74 m (`risultati_verticale.txt`); il costo è il campo orizzontale (58°).
2. **Scritta com'è, la regola peggiora il nucleo.** «Osservata» non è definita. Se basta un raggio, la scatola a 0,8 m risulta «libero» (22 celle su 22: i raggi passano sopra, fra 0,28 e 0,60 m), cosa che il nucleo non fa. Richiedere anche il suolo (F3-lett+suolo) corregge solo questa scena: restano la sbarra (53 su 53), il gradino (182 su 182) e il profilo M (48 su 48).
3. **La fascia bassa da 0,15 m apre un buco che il nucleo non ha.** Il nucleo chiama ostacolo ciò che supera 0,07 m. Fra 0,07 e 0,15 m la preproposta «filtra il pavimento»: un gradino di 10 cm è «libero» su tutta l'impronta (0,67 m²), con e senza rumore. Anche l'ostacolo di riferimento del nucleo, alto esattamente 15 cm, senza rumore finisce nel pavimento (scena C2 e braccio di controllo P8: «libero» con 5938 pixel sopra). Alla soglia decide il rumore.
4. **La fascia alta non è mai osservata dentro la griglia.** Con questo montaggio la quota 2,0 m è coperta per intero solo da 3,21 m, la 1,8 m da 2,41 m, la 1,6 m da 1,60 m. Con la regola stretta e una fascia alta fino a 2 m, **nessuna cella è «libero» per un pedone** (0 m² su 5,48). «> 1,60 m» senza tetto, come scritto, non è mai osservabile. È il prezzo vero: le tre fasce non danno più copertura, dicono dove la copertura manca. Con la camera in verticale il «libero» BMA torna a 3,25 m² e la sbarra a 2 m si vede (51 celle occupate su 53).
5. **Senza un ritorno dietro, un raggio non prova nulla.** In un capannone o all'aperto, dove i raggi sopra l'orizzonte non tornano, la fascia media (che arriva a 1,6 m, sopra il sensore) non è mai osservata: 0 m² di «libero». Vale anche per la voxel. Nella sala della demo servono pareti entro la portata valida.
6. **«Sostituto su CPU della voxel» parte da una premessa non misurata.** Su un filo di un Ryzen AI 9 HX 370 la voxel densa a 10 cm (3 × 6 × 2 m) costa 23 ms a piena risoluzione. E le tre fasce, se «osservata» si calcola seguendo ogni raggio, costano **quanto la voxel** (28,6 ms): il costo è il tracciamento, non il numero di strati. Diventano economiche (1,11 ms) solo sfruttando che in griglia polare ogni pixel ha azimut e pendenza fissi (§4, punto 5).
7. **La voxel non aggiunge sicurezza, aggiunge quota.** Falsi «libero» su solidi: 0 per entrambe. Con la regola abituale la voxel mette «libero» su 306 litri mai visti (voxel di bordo visti a metà), contro 7 delle fasce corrette. Il guadagno è d'informazione: nel cuneo dietro la cassa il vuoto visto buttato via scende da 1317 a 236 litri (su 1595), e un franco di 1,8 m ottiene 1,97 m² di «libero» dove le fasce ne danno 0. Lo stesso si ottiene ridisegnando la fascia alta sul franco del profilo.
8. **Il passaggio automatico cambia ciò che è «libero» senza una nuova osservazione** (0 → 0,21 m² BMA passando a V10) e può farlo a metà di un'occlusione. Contrasta con il principio che un cambio di configurazione non tocca gli avvisi. Una mappa sola nel percorso critico, scelta all'avvio.
9. **Che cosa le fasce chiudono davvero.** (a) Il cuneo «fino al bordo della portata» del nucleo, falso con occlusori bassi: dietro un gradino il 90 % del volume dichiarato in ombra è vuoto visto, dietro una scatola di 30 cm l'87 %, dietro la cassa di 1 m il 46 %. (b) La correzione proposta dall'audit (N-cella) non è sicura sotto e dietro un tavolo: il suolo si vede sotto il piano, ma fra 0,3 e 0,7 m resta una lama d'ombra (1,84 m² di «libero» su colonne non viste). (c) Per la continuità visiva: una persona in piedi dietro la cassa di 1 m è vista (10 354 pixel), ma il nucleo alla lettera la tiene «in ombra» in 48 celle su 48; con le fasce resta «osservata» e l'inseguitore non la perde.

## 4. La versione corretta (`nuvole-punti-f9-1`)

1. Fasce **0,07–0,60 / 0,60–1,60 / 1,60–franco del profilo** (1,8 o 2,0 m, dichiarato): la prima parte dalla soglia del nucleo.
2. Fascia **occupata osservata**: almeno K ritorni dentro. **Osservata libera**: tutti i raggi che per geometria la attraversano in quella cella hanno un ritorno valido oltre la cella (tolleranza dichiarata sui pixel non validi), e per geometria coprono tutta la sua altezza (maschera fissa del montaggio). **In ombra**: un ritorno più vicino ferma almeno un raggio che l'attraverserebbe. Altrimenti **non osservata**.
3. Cella «libero» per un profilo: suolo visto (invariante 1 del nucleo) **e** tutte le fasce del profilo osservate libere. Un profilo in quota (sola fascia media) non richiede il suolo.
4. All'avvio si dichiara, dalla maschera, da quale distanza ogni fascia è osservabile. La «possibile presenza» resta uno strato a parte e sopravvive a ogni cambio di mappa.
5. Calcolo per differenze: per ogni pixel e fascia l'intervallo di corone attraversato è precalcolato; per fotogramma due incrementi per pixel e fascia. In 13 scene senza rumore dà le stesse classi della versione che segue i raggi (0 celle diverse su 2349, quattro profili); con rumore differisce in 54–86 celle (più «libero», 0 m² sopra solidi).
6. Nessun passaggio automatico alla voxel. Nel documento: «a meno di 1,1 m **di distanza dal sensore**».

**La smentisce:** una cella «libero» sopra un solido su fotogrammi veri (sbarra a 1,8 m, scatola a 0,8 m, gradino di 10 cm, persona accovacciata dietro una cassa).

## 5. Dove la preproposta ha letto male

- «Copertura verticale (< 1,1 m)», «buco sotto 1,1 m», «ostacoli bassi (< 1,1 m)»: legge come **quota** una **distanza**. Il v0.5 lo favorisce: scrive «sotto 1,1 m gli ostacoli bassi non si vedono» senza dire «di distanza» (sez. 4 e riquadro dei limiti).
- Il v0.5 (sez. 7) chiede se la voxel chiuderebbe «ostacoli sospesi, ostacoli più bassi del sensore»: sono altri due limiti, non l'anello cieco vicino. La preproposta li fonde.
- «Senza far crollare il ciclo sotto 15 Hz in assenza di GPU»: il v0.5 non contiene nessuna misura del costo della voxel.

## 6. Costo

Calcolo: 1,11 ms per fotogramma contro 0,25 (mediana, un filo, tempi indicativi; esclusi lettura e deproiezione dal formato della camera); 64 kB più 1,9 MB di tabelle fisse. Ore: **circa 5** oltre le 6 del blocco B2 (tabelle 1, ciclo e regola 2, uscita per profilo 1, prova su registrazioni 1): stima mia, non verificata. Si tolgono dall'etichetta (B6, 4 ore). Variante minima da 1 ora: solo la maschera fissa e la frase d'avvio «sopra questa quota, a questa distanza, non vedo».

## 7. Esiti delle previsioni (scritte prima)

Reggono: P1, P2bis, P3, P4 (46 %; −17 % le fasce, −90 % la voxel; con la metrica aggiunta dopo), P9. **Smentite in parte:** P2 (V10 dà 0,21 m² di «libero» BMA, non 0); P5 (N-cuneo: 31 celle occupate e 151 in ombra, non il 90 % occupate); P6 (le fasce a raggi costano 114 volte il nucleo, non al più 2; per differenze 4,4); P7 (0,09–0,16 m² anche per le altre mappe, non 0: 19 celle su 31 non le ho spiegate); P8 (F3-lett non vede la scatola pur con 5938 pixel: critica 3).

## 8. Non verificato, e che cosa propongo dopo

Non verificato: tutto ciò che dipende dal sensore vero (pixel misti ai bordi, banda senza dato accanto all'ombra, quota di ritorni validi sopra l'orizzonte nella sala, riflessi del suolo); più fotogrammi insieme alla regola dei tre fotogrammi; sensore in moto; la regione 6 × 4 × 3 m di f7; i tempi sulla macchina dell'hackathon; le ore.

Prova che decide, nella prima ora con l'hardware (10 minuti): sala vuota, poi sbarra a 1,8 m, scatola a 0,8 m, gradino di 10 cm. Si contano le celle «libero» per profilo e si confronta la maschera fissa con il campo vero. In parallelo va deciso il montaggio verticale (`nuvole-punti-f9-2`): previsione, «libero» per il pedone da 0 a circa 3 m² e scatola a 0,8 m vista; lo smentisce un campo di 58° che taglia l'attore dell'atto 3.
