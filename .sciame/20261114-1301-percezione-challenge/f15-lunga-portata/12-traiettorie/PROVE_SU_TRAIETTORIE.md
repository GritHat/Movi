# Prove della previsione su traiettorie pubbliche reali, per classe (sciame-kalman, f15/12-traiettorie)

15 novembre 2026, 01:13–01:25 (orologio della macchina; la consegna dice 14). Previsioni scritte prima, alle **01:15:16**, in `PREVISIONI.md`.
Comando: `sh rifai.sh` (66 s di prove più 5 s di riassunto). Uscite: `risultati_traiettorie.json` (ogni caso), `riassunto.txt` e `riassunto.json` (le tabelle), `prove.log`.

## 0. In testa: limiti, cambi di stato, regole

- **Non è una prova di un sensore.** Il moto è reale (ADS-B, GNSS di bordo, telecamere NGSIM, GPS dei treni). Il rumore di misura è **simulato** dalle schede di `02-sensori/parametri_lunga_portata.json`. Le occlusioni sono **inserite a mano** (10 istanti a caso per tratto e per durata, seme 20261115 + D). C'è un solo oggetto per scena e **non c'è associazione**: si usa `Traccia` di `movi_lp.py`, non `Inseguitore`. Le posizioni dei sensori sono ipotesi: aerei σ 7,5 m isotropa a 1 s (SCANTER, valore «ipotesi» nella scheda); droni IRIS (σr 0,6 m, σaz 0,75°, σel 1°, 1 s) a 1,5 km; auto ARS 548 (σr 0,15 m, σaz 0,3° **ipotesi**, 0,1 s) a 100 m; treni Tele-15 (σr 0,02 m, σ 0,03°) a 300 m, al passo dei dati (3 s). Niente diventa «validato».
- **Metà e metà.** Divisione per tratto (seme 20261115). Su metà si tarano il fattore di Q e il raggio della zona al livello 0,90; **tutte le cifre qui sotto sono sulla sola metà di prova**. Nella prova i casi dello stesso tratto sono correlati. Per questo do due intervalli: Wilson sui casi e Wilson «conservativo», con n uguale al numero dei tratti.
- **Smentita K4 (la più grave).** L'insieme di possibile presenza, cioè l'avviso, calcolato con l'inviluppo di `aeroporto_e_droni` (v_max 90 m/s), **non contiene l'aereo vero** nel 28–41 % dei casi. Quei casi sono decolli, avvicinamenti e sorvoli reali a 160–247 m/s. Il principio regge (l'avviso non usa l'etichetta); è sbagliato il **valore** del limite di classe. La correzione è nel § 4.
- Smentite anche K1 (treni a 2 s), K3, K5 e K6 (aerei e treni), più metà di K7. Reggono K2 e K8. Dettagli nel § 3.
- **Eventi.** `40-eventi/01-effetti` e `02-regole` ci sono. Qui non eseguo E1–E5: li esegue il simulatore. Do però il **riscontro reale più vicino a E2 (avaria)**, cioè le 21 sequenze ALFA di prova con guasto indotto (§ 1), e la conferma della critica di 02-regole, riga 26: per E2 in decollo serve una classe nuova.
- Regole: nessuna violata, che io sappia. Nessun file cancellato o sovrascritto fuori dalla mia cartella, nessuna rete, niente git.

## 1. Risultati sulla metà di prova (zona al livello dichiarato 0,90)

La zona è una sfera centrata su p + vτ dall'ultima stima, con raggio r_D + 3(σp + σv τ). r_D è il quantile conforme tarato sulla metà di taratura. L'area è quella della sezione orizzontale, πr². «Fuori avviso» conta i casi in cui la verità sta fuori dall'insieme di possibile presenza.

| classe (tratti di prova; fattore di Q) | D (s) | casi | errore mediano / p90 (m) | dentro la zona: k/n, Wilson | Wilson conservativo | raggio mediano (m) | area mediana (km²) | fuori avviso |
|---|---|---|---|---|---|---|---|---|
| **aerei** (97; ×8) | 2 | 803 | 18,6 / 39,8 | 745/803 = 0,928 [0,908; 0,944] | [0,856; 0,964] | 44 | 0,006 | **223/803 = 0,278** |
| | 5 | 842 | 30,4 / 72,0 | 0,912 [0,891; 0,929] | [0,833; 0,950] | 71 | 0,016 | 0,348 |
| | 10 | 812 | 54,3 / 173 | 0,916 [0,895; 0,933] | [0,846; 0,958] | 170 | 0,091 | 0,390 |
| | 20 | 741 | 120 / 617 | 0,888 [0,863; 0,909] | [0,808; 0,935] | 557 | 0,97 | 0,348 |
| | 30 | 703 | 218 / 1194 | 0,905 [0,881; 0,924] | [0,831; 0,950] | 1109 | 3,86 | 0,407 |
| **droni** (122; ×0,25) | 2 | 1203 | 14,9 / 37,2 | 0,972 [0,961; 0,980] | [0,930; 0,992] | 44 | 0,006 | 1/1203 |
| | 5 | 1175 | 22,5 / 61,7 | 0,956 [0,942; 0,966] | [0,908; 0,982] | 57 | 0,010 | 0 |
| | 10 | 1137 | 38,4 / 123 | 0,924 [0,908; 0,938] | [0,866; 0,961] | 107 | 0,036 | 0 |
| | 20 | 1042 | 82,6 / 287 | 0,920 [0,902; 0,935] | [0,853; 0,954] | 239 | 0,18 | 0 |
| | 30 | 960 | 134 / 416 | 0,911 [0,892; 0,928] | [0,843; 0,948] | 355 | 0,40 | 0 |
| **auto** (79; ×1) | 2 | 766 | 2,6 / 6,4 | 0,941 [0,922; 0,956] | [0,860; 0,973] | 7,7 | 0,0002 | 0 |
| | 5 | 710 | 7,1 / 15,9 | 0,920 [0,897; 0,938] | [0,844; 0,965] | 18 | 0,001 | 0 |
| | 10 | 657 | 17,6 / 35,4 | 0,919 [0,896; 0,938] | [0,844; 0,965] | 38 | 0,005 | 0 |
| | 20 | 489 | 43,6 / 89,7 | 0,898 [0,868; 0,922] | [0,813; 0,948] | 87 | 0,024 | 0 |
| | 30 | 352 | 75,2 / 133 | 0,955 [0,927; 0,972] | [0,875; 0,980] | 155 | 0,076 | 0 |
| **treni** (56; ×1) | 2 (τ 3) | 372 | 40,3 / 193 | **0,836** [0,795; 0,870] | [0,722; 0,913] | 134 | 0,057 | 75/372 = 0,202 |
| | 5 (τ 6) | 538 | 67,1 / 306 | 0,885 [0,855; 0,909] | [0,785; 0,950] | 277 | 0,24 | 0,084 |
| | 10 (τ 11) | 529 | 106 / 436 | 0,877 [0,846; 0,902] | [0,764; 0,938] | 388 | 0,47 | 0,015 |
| | 20 | 516 | 175 / 666 | 0,901 [0,872; 0,924] | [0,785; 0,950] | 668 | 1,40 | 0 |
| | 30 | 505 | 292 / 1034 | 0,875 [0,844; 0,901] | [0,764; 0,938] | 944 | 2,80 | 0 |

Copertura **per tipo di tratto**, con D ≤ 10 s:

| | rettilineo | virata | accelerazione | arresto |
|---|---|---|---|---|
| aerei | 0,932 [0,920; 0,943] (n 1855) | **0,741** [0,673; 0,798] (185) | 0,916 [0,863; 0,949] (166) | 0,952 [0,918; 0,972] (251) |
| droni | 0,977 [0,968; 0,984] (1395) | **0,715** [0,669; 0,758] (390) | 0,977 [0,947; 0,990] (217) | 0,984 [0,977; 0,989] (1513) |
| auto | 0,964 [0,954; 0,973] (1515) | 2/3 (3) | **0,842** [0,811; 0,869] (609) | 2/6 (6) |
| treni | 0,855 [0,829; 0,877] (833) | 15/17 | **0,756** [0,701; 0,803] (266) | 1,000 [0,988; 1] (323) |

Per mezzo, a 10 s. Droni: multirotore 0,976 [0,964; 0,984] su 101 tratti; **ala fissa ALFA con guasto 0,656 [0,584; 0,721]** su 21 tratti (a 5 s 0,785 [0,722; 0,837]). Tutte le scene ALFA di prova hanno il guasto nel nome, quindi non c'è un confronto senza guasto. Aerei: decollo 0,860 [0,810; 0,899]; avvicinamento 0,904; aviazione generale 0,958; rullaggio 67/68. L'elicottero ha 8 casi su un solo tratto: non si dice niente.

«Previsto ampio» (zona > 0,8 × raggio dell'avviso) non scatta mai per aerei, droni e auto fino a 30 s. Per i treni scatta in 290 casi su 372 a 2 s e in 363 su 538 a 5 s. Lì la zona tarata è larga quanto l'avviso, perché il riferimento GPS è sporco (§ 3).

## 2. Profili di classe contro i dati (tutti i 704 tratti; `riassunto.txt`, ultima sezione)

| tipo | classe usata (`regole_lunga_portata.json`) | v massima del tratto: mediana / massimo | tratti oltre v_max | lettura |
|---|---|---|---|---|
| aereo in decollo | aereo_linea_avvicinamento, 90 m/s | 165,9 / 204,6 | 55/55 [0,935; 1] | **smentito**: serve un «aereo in decollo e salita», v_max ≥ 210 m/s |
| aereo in avvicinamento | idem | 157,9 / 195,3 | 48/49 [0,893; 0,996] | **smentito** (sotto 3000 m; Zenodo è lisciato, ma le velocità reggono, cfr. 01-dati § 3.2) |
| sorvolo | idem | 241,7 / 247,6 | 6/6 [0,61; 1] | smentito: in crociera, fuori contesto |
| aviazione generale | aereo_leggero, 70 m/s | 59,3 / 137,7 | 5/60 [0,036; 0,181] | **corretto in parte**: v_max ≈ 140 |
| rullaggio | aereo_rullaggio, 15,4 (= f14) | 10,7 / 16,0 | 2/19 [0,029; 0,314] | non risolto (19 tratti): v_max 16–17 |
| ala fissa senza pilota | drone_ala_fissa, 40 | 22,2 / 28,2 | 0/47 [0; 0,076] | **confermato** (largo) |
| multirotore | multirotore_piccolo, 19 (= f14 multirotore_lento) | 9,5 / 14,2 | 0/196 [0; 0,019] | confermato **per questo mezzo** (voli programmati) |
| auto (autostrada) | auto_autostrada, 36,1; f14 auto_strada_urbana, 13,9 | 16,9 / 27,8 | 0/154; f14: 114/154 [0,666; 0,803] | f14 smentito fuori dal suo contesto; autostrada confermata |
| treno in linea | treno_alta_velocita, 83,3; f14 treno_banchina, 16,7 | 37,6 / 73,9 | 0/111; f14: 95/111 [0,779; 0,909] | idem; il massimo del GPS non è affidabile (01-dati § 3.3) |

Le accelerazioni sono stimate come p99 di |dv/dt| a partire da una velocità già derivata. Superano a_max per i multirotori (88 tratti su 196 oltre 6,9 m/s²), i treni (108 su 111 oltre 0,5) e gli aerei (p99 mediano 7–12 m/s²). Per aerei e treni è quasi certamente rumore della doppia derivazione e del passo di 3–5 s, non moto vero: **non risolto**. Lo deciderebbe un'accelerazione misurata a bordo (IMU), che questi dati non danno. Per i multirotori il valore è plausibile ma **non verificato**. Le virate (01-dati, statistiche.json) mostrano che l'ala fissa vira molto (p95 24,5 °/s). È la causa principale della copertura 0,66 dell'ala fissa a 10 s.

## 3. Le previsioni (scritte alle 01:15:16) e gli esiti

| # | esito | numeri |
|---|---|---|
| K1 copertura ≥ 0,85 fino a 10 s | **smentita** solo per i treni a 2 s | 0,836 [0,795; 0,870]; le altre celle con D ≤ 10 s vanno da 0,912 a 0,972 |
| K2 copertura più bassa in virata e in arresto | **regge** per la virata (−0,19 aerei, −0,26 droni rispetto al rettilineo); **non** per l'arresto (0,95–1,00) | tabella del § 1 |
| K3 ordine aerei > droni > auto > treni a 10 s | **smentita** | treni 106 > aerei 54 > droni 38 > auto 18 m |
| K4 avviso al 100 % | **smentita** per aerei (0,28–0,41), treni (0,20 a 2 s) e droni (1 caso: ALFA, 141 m in 2 s a 20 m/s, cioè un salto nei dati, non verificato) | § 1 |
| K5 ala fissa con il rapporto errore/(vτ) più alto a 5 s | **smentita** | multirotore 1,11 (v0 basse: il rapporto è inadatto), rullaggio 0,64, ala fissa 0,57 |
| K6 NIS medio in [1,5; 6] | regge per droni 3,08 e auto 3,30; **smentita** per aerei 7,28 e treni 142 449 | n 19 565 / 46 644 / 30 306 / 9002 |
| K7 profili superati | regge per aereo_linea (103/104) e per f14; **smentita** per drone_ala_fissa (0/47) | § 2 |
| K8 meno di 10 min | **regge** | 66 s |

Notato dopo, non previsto. (a) Per gli aerei il fattore di Q scelto (×8) sta al **bordo** della griglia, e per i droni anche (×0,25). Il NIS degli aerei (7,28) dice che il filtro è troppo sicuro: servono Q più grande o un R più largo del valore di scheda per l'ADS-B interpolato. Il filtro dei droni ha un solo q per multirotore e ala fissa. (b) Treni: il NIS di 142 449 dice che il LiDAR di scheda (16 cm a 300 m) è molto più preciso della **verità** GPS (salti, doppioni, 01-dati § 3.3). Il filtro crede alle misure, e la zona assorbe l'errore della verità. Per i treni questa è una prova del riferimento, non del filtro: **non risolto**. Lo deciderebbe un riferimento ferroviario migliore, o R portato al rumore del GPS. (c) La taratura conforme unica per classe dà la copertura marginale, ma **non la copertura condizionata** al tratto: in virata e per l'ala fissa con guasto si scende a 0,66–0,74.

## 4. Stati proposti, frase più forte, che cosa non si può dire

- «Su traiettorie reali la zona al 0,90 tarata su metà dei tratti copre circa il 0,90 sull'altra metà»: **sostenuto dai dati** per aerei, droni e auto (D 2–30 s). Per i treni è sotto (0,84–0,90).
- «L'avviso contiene sempre il mezzo»: **smentito** per gli aerei con i valori attuali. Il principio non cambia; vanno corretti `v_max` e `a_max` dell'inviluppo.
- Profili: aereo_linea (90 m/s) **smentito**; aereo_leggero corretto a circa 140 m/s; drone_ala_fissa, multirotore e auto_autostrada **sostenuti dai dati**; f14 auto_strada_urbana e treno_banchina **smentiti fuori dal loro contesto**.

**Frasi più forti che restano vere.** k è il limite inferiore di Wilson con n = tratti, preso come minimo fino a t e arrotondato per difetto, in decimi.
- **Aerei:** su tracciati pubblici reali di 97 aerei (avvicinamento, decollo, rullaggio, aviazione generale), la zona dichiarata contiene il mezzo in almeno **8 casi su 10 fino a 30 s**. Con l'inviluppo attuale, però, l'avviso **non** lo contiene in 3–4 casi su 10. Finché `v_max` non è corretto, la frase sull'avviso non si può dire.
- **Droni:** su 122 droni reali (101 multirotori, 21 ali fisse con guasto), almeno **9 su 10 fino a 5 s** e **8 su 10 fino a 30 s**. Per l'ala fissa con guasto si scende a **5 su 10 a 10 s** con Wilson sui casi ([0,584; 0,721]); con n = 21 tratti il limite inferiore è circa 0,45, cioè **4 su 10**.
- **Auto:** su 79 auto reali (US-101 congestionata), almeno **8 su 10 fino a 30 s**, con zona di 38 m di raggio a 10 s.
- **Treni:** su 56 treni reali, almeno **7 su 10 fino a 30 s**, con zona di 0,4–0,9 km. La frase vale con un riferimento GPS sporco.

**Che cosa non si può dire.** Non è una prova di un sensore: il rumore è di scheda, la geometria è inventata, non ci sono falsi allarmi, mancati rilevamenti né associazione. Le occlusioni sono inserite a mano e non vengono da ostacoli veri. La verità è di bordo, interpolata (Zenodo, passo di 3–5 s) o sporca (treni). Il sottoinsieme è piccolo per elicottero (1 tratto), sorvolo (4) e camion e moto. Nessuna frase vale fuori da questi luoghi (Atlanta, LHR-ZRH, Pittsburgh, US-101, Finlandia), da questi mezzi e da queste giornate.

**Proposte (sigla kalman-).**
- **kalman-1**: classi «aereo in decollo e salita» e «aereo in avvicinamento» con v_max di 210–250 m/s (dai dati, più un margine), e a_max da verificare. Previsione: «fuori avviso» degli aerei scende da 0,28–0,41 a meno di 0,01. La smentisce il rifacimento con più di 1 caso su 100 fuori.
- **kalman-2**: taratura condizionata al modello IMM dominante (virata contro rettilineo), oppure una zona a cuneo lungo la rotta. Previsione: in virata la copertura sale a ≥ 0,85 con un'area media non più del doppio. La smentisce una copertura in virata sotto 0,85.
- **kalman-3**: per i treni, R pari al rumore del GPS (σ 5–10 m) o un riferimento migliore. Previsione: NIS fra 1,5 e 6 e copertura ≥ 0,88 a 2 s. La smentisce un NIS ancora oltre 20.

**Dopo:** rifare con kalman-1 nelle regole (`04-moto`), allargare la griglia di Q per aerei e droni, e separare il q di multirotore e ala fissa.
