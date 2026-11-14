# ANALISI_DATI — f10, `21-statistica` (`sciame-statistico`), 14 novembre 2026, 17:28–17:45

Percorsi relativi a `f10-dati/21-statistica/`. Codice mio: `ricalcolo_sim.py`, `ricalcolo_thor.py`, `rigenera_fermi.py`,
`analisi_fermi.py`, `confronto_profondita.py`, `controlli_brevi.py`; uscite in `tabelle/`; si rifà con
`../ambiente/venv/bin/python -I -B <script>`. Previsioni S1–S9 in `PREVISIONI.md` (17:29:04, prima di aprire le uscite grezze).

## 0. Cambi di stato, scostamenti, regole violate

- **Le cifre della validazione tornano**: su oltre 30 ricalcolate, 3 non tornano come scritte (§1). Nessun conteggio cambia.
- **«La regione dichiarata copre il 100 %» (simulato, soglia 40): corretta.** La mediana è 1,00, ma in **7 passaggi su
  90** la verità esce dalla regione al 90 %; in 4 di a05 non ci entra mai (errore 2,3–2,9 m).
- **Rumore del centro, persona ferma a 2 m, soglie del nucleo: la mediana (0,34 cm) inganna.** La distribuzione è
  bimodale: 8 semi su 20 stanno a 3,7–4,4 cm, sopra la curva nominale (1,5 cm).
- **Il simulatore non somiglia alle registrazioni vere nei buchi** (21–39 punti di pixel validi in più del vero); nel
  rumore sta entro un fattore 2 dell'unico D435 (§5).
- *Scostamenti.* (a) Conoscevo le cifre della validazione prima delle previsioni (è il compito). (b) Il rumore del
  centro da fermi **non è un ricalcolo**: i valori per seme non sono conservati; l'ho **replicato** con 60 sequenze
  nuove, importando simulatore e catena in sola lettura. (c) La mia tolleranza S5 (±0,02) era più stretta del rumore
  di Monte Carlo. (d) La variante «maschera a 2,4 m» del bordo è scritta dopo le previsioni.
- **Violata:** per alcuni secondi due processi insieme (il ricalcolo THÖR mentre la replica girava in sottofondo).
  Niente rete, git, sudo, GPU; `f7`–`f9` non lette; scritto solo qui; dati scaricati letti con `allow_pickle=False`.
- *Indipendenza.* Condivido con la validazione le uscite della catena, la verità del simulatore, le definizioni e il
  modello linguistico; non il codice di misura né il filtro (THÖR: filtro mio, per asse).

## 1. Che cosa torna (unità: la sequenza o il passaggio; Wilson al 95 %)

| Misura | Validazione | Ricalcolo mio | |
|---|---|---|---|
| K-014, «libero» in celle tutte in ombra | 0 su 2 907 032, «135 sequenze, filtri spenti» | 0 su 2 841 026 in **131** sequenze senza filtri + 0 su 66 006 in **4 con i filtri**; con la mia definizione a 9 punti 0 su 2 741 202 (130 sequenze); sulla maschera polare della verità 0 su 3 137 390 | torna; **l'etichetta no** |
| lo stesso, soglia 40 | 2 (45 al bordo), 1 sequenza | 2 (45), `scatola15_2p0m`, 1 cella, 2 fotogrammi | torna |
| Bordo d'ombra, nominale | mediana +6,2; da +2,0 a +14,6 cm; 103 su 103; 3742 fotogrammi | identico; limite: da −65 a +73 (nucleo), 8 su 8 (soglia 40) | torna |
| Continuità pulita | 0 su 90; dispari 41 su 45; 28 / 24 / 28 su 30 | identico (pari 39 su 45) | torna |
| Centro nascosto in «possibile presenza» | 2939 su 3038 (nucleo); 328 / 793 / 1917 (soglia 40) | identico; 99 «in ombra senza avviso», 0 «libero» | torna |
| Pannello «si muove» | 79 su 90; 5 su 90 | identico | torna |
| Errore per tempo nascosto (soglia 40) | a12 0,08 / 0,11 / 0,12; b … 3,78 m | identico | torna |
| Copertura della regione al 90 % | «mediana 1,00 in ogni caso» | mediana 1,00; **media per passaggio 1,000 / 0,867 / 0,956** | fuorviante |
| THÖR, q = 0,2, exp3 | 0,977 / 1,000 / 1,000 | 0,982 / 0,995 / 1,000 | torna |
| THÖR, q = 0,05, exp3 | 0,795 / 0,804 / 0,831 | 0,836 / 0,822 / 0,840 | **a 1 s no** (seme: 0,790–0,836 su 20 semi) |
| Centro, persona ferma (nucleo) | 0,36 / 0,99 / 1,25 cm | replica 0,34 / 0,84 / 1,18 | compatibile |

Non ricalcolati (**non verificati da me**): celle per stato sul pavimento vuoto, tracce fantasma, sensore coperto,
vetro, tabella degli ostacoli, persone lente, TUM, costo (ipotesi 6).

## 2. Critiche, ciascuna con la prova

1. **«2,9 milioni di celle» sono 3 geometrie d'ombra.** 128 sequenze su 130 hanno lo stesso pannello (330 celle), una
   la cassa (438), una la scatola (6): `tabelle/sim_sim.txt`. Per generalizzare l'unità è la geometria (N = 3), non
   la cella·fotogramma. Per sequenza: 0 su 131, limite superiore 2,9 %.
2. **La misura del bordo ha quattro valori possibili.** Un grado a 2,4 m vale 4,2 cm: +2,0 (17,3 %), +6,2 (82,3 %),
   +10,4, +14,6. «+2,0» è il minimo che la griglia può dare senza perdere una colonna. Con soglia 40 è +2,0 nel 100 % dei fotogrammi. Sinistra e destra: +5,2 e +5,8 cm.
3. **La regione dichiarata, per passaggio.** Verità sempre dentro l'ellisse al 90 % (soglia 40): a12 30 su 30
   (88,6–100 %), a05 **26 su 30** (70,3–94,7 %), b **27 su 30** (74,4–96,5 %); in tutto 83 su 90 (84,8–96,2 %). In a05
   `s04`, `s15`, `s18`, `s28` la copertura è 0,00 dal primo fotogramma nascosto. Con i parametri del nucleo solo 46
   passaggi su 90 hanno una previsione.
4. **L'errore «0,08–0,12 m» è contro la superficie misurata, non contro la persona.** Senza togliere lo scarto
   (−16 cm, stimato sullo stesso passaggio) l'errore contro il centro vero è 0,22 / 0,26 / 0,26 m in a12. In b, oltre
   3 s: 3,78 m (3,55–3,86), p90 4,6 m all'uscita dall'ombra.
5. **Persona ferma a 2 m, soglie del nucleo.** Semi ordinati: dodici fra 0,17 e 0,39 cm, otto fra 3,69 e 4,44 cm
   (`tabelle/controlli_brevi.txt`): 8 su 20 (21,9–61,3 %) sopra la curva nominale. L'intervallo della mediana è
   0,24–3,81 cm. A 3 m: 0 su 20 sopra la nominale (0,84 cm; 0,68–1,02); a 4 m 2 su 20. Con soglia 40 tutti sotto 1 cm.
   Falsi «si muove»: 0 su 20 a ogni distanza (0–16,1 %), replicato con semi nuovi.
6. **THÖR: 219 tratti, ma 9 persone.** L'intervallo per persona (q = 0,05, 2 s: 0,76–0,89) è 1,27 volte quello ingenuo
   sui tratti; la copertura per persona va da 0,43 a 1,00. Con la stessa regola scritta, q esce 0,05 su exp1 e **0,1 su
   exp3**: il valore tarato dipende dalla registrazione.
7. **Il criterio «28 su 30» non può mostrare il 90 %.** 28 su 30 ha limite inferiore 78,7 %, 41 su 45 ha 79,3 %; per
   escludere a una coda (5 %) una continuità sotto il 90 % servono 29 successi su 29 (0,9^29 = 0,047).

## 3. Soglie scritte prima, scelte dopo i dati, taratura e prova

Le soglie V1–V21 sono scritte alle 16:48, prima delle corse; V22–V24 e la regola di q prima delle loro prove. Gli
esiti sfavorevoli sono riportati (V7, V12, V18, V23 smentite). La correzione della misura
dell'identità (dichiarata) va nel verso **più severo**: con la definizione originale la soglia 40 darebbe 89 su 90, con
quella corretta 80 su 90. **Taratura e prova:** soglia 40 scelta sui passaggi pari (39 su 45) e provata sui dispari
(41 su 45), che entrano dall'altro lato: dati separati, ma generati dallo stesso simulatore e dalla stessa scena; la
scelta sta fuori dalla regola scritta (dichiarato). q: exp1 per tarare, exp3 per provare; **stessi nove caschi, stesso
giorno** (13:35 e 14:47 del 22 febbraio 2019, `meta.json`): separati per registrazione, non per persona (identità dei
partecipanti: non verificata). Scelte dopo i dati **non dichiarate** in §0 della validazione:
1. V8 al limite: per la soglia scritta è **smentita** (0 sequenze su 8 entro ±20 cm), riportata come «non decidibile».
   Sulla maschera a 2,4 m lo scarto è sempre verso il largo (da +6 a +144 cm).
2. «135 sequenze, filtri spenti» comprende le 4 con i filtri.
3. Il rumore vero «5,8–6,8 cm» è la migliore di tre varianti della stessa sequenza (parametri del nucleo: 15,8–28,5
   cm; soglia scalata senza vincolo: 19 fotogrammi utili); «rollio vincolato» e «soglia scalata» non stanno nelle previsioni V20–V21.
4. Le soglie «scalate» (91, 121, 362) sono 40 per il rapporto dei pixel: derivano da un valore fuori regola.
Nessuna sequenza simulata esclusa; le vere sono troncate o sottocampionate a 51–320 cicli (dichiarato).

## 4. Quante sequenze vere, e che cosa si può dire

Otto sequenze con profondità vera, 3510 fotogrammi; 5 con una persona, **una sola con stereo attivo e una persona**
(DepthTrack, D415), **una sola con la posa nota** (TUM, Kinect), nessuna con la posa della squadra. Tratti nascosti: 5
in 3 sequenze (0,03–0,70 s); identità decidibile in **2 tratti di 0,03–0,10 s di una sequenza**. Verità indipendente
della posizione o dell'ombra: nessuna. **In una riga: su profondità vera la continuità durante l'occlusione non è
provata — 2 tratti su 2 con la soglia scalata (34–100 %), 0 su 2 con i parametri del nucleo (0–66 %), N = 1 sequenza,
occlusioni non più lunghe della memoria della mappa (3 fotogrammi).** K-014: N = 0 sequenze con l'ombra vera. Rumore del
centro: N = 1 sequenza (288 fotogrammi correlati, moto del corpo incluso).

## 5. Profondità simulata contro vera (`tabelle/confronto_profondita.txt`, stesso codice, primi 60 fotogrammi)

| | Simulato D435i nominale / limite | D435 vero (`stairs`) | D415 vero (DepthTrack) | Kinect (TUM) |
|---|---|---|---|---|
| Pixel validi | 96,9 % / 85,5 % | 61,0 % | 76,1 % | 70,9 % |
| Buchi dove la scena sta fra 0,5 e 3 m | 1,7 % / 7,8 % | 34,4 % (×20; ×4,4) | 24,1 % (×14; ×3,1) | 6,3 % |
| Pixel validi solo a tratti | 26 % / 56 % | 71 % | 65 % | 27 % |
| Buchi di bordo (quota dei pixel) | 1,0 % / 6,4 % | 5,8 % | 10,7 % | 4,1 % |
| Larghezza mediana a 848 px | 6 px / 8 px | 34 px | 5 px (p90 28) | 11 px |
| Buco a sinistra dell'oggetto vicino | 75 % / 56 % | 51 % | 54 % | 73 % |
| Rumore nel tempo a 2–3 m | 26 mm / 91 mm | 21 mm (0,83 del nominale) | 43 mm (1,6) | 13 mm |
| lo stesso a 1–2 m, riportato con z² | — | 1,45 del nominale | 4,3 (limite superiore) | — |

Punto fermo: `stands_still` (D435i, piano a 0,35 m), scarto nel tempo 0,36 mm, ricalcolato; il modello dà 0,28 mm a 848
px e 0,37 mm riportato a 640 px (rapporto 1,29 e 0,97), ma a una distanza fuori dal campo di lavoro. **Lettura:** nel
rumore il vero sta fra nominale e limite; nei buchi il vero è **oltre il limite** (3–4 volte); l'asimmetria della banda
stereo del simulatore non si vede nelle due sequenze stereo. *Che cosa non dice:* nessuna coppia ha la stessa scena; con la
camera in moto il rumore vero è un limite superiore. Conseguenza: le cifre al nominale (identità, fantasmi, «libero» al 95–100 %) sono ottimistiche sui buchi.

## 6. Ipotesi → che cosa si può affermare

| Ipotesi | Affermazione | Dati | Incertezza | Stato |
|---|---|---|---|---|
| 1 «Libero» | nessun «libero» dentro l'ombra vera con i parametri del nucleo; un controesempio se l'ostacolo non è rilevato | simulato, 131 sequenze, **3 geometrie**, 3 profili | per sequenza 0–2,9 %; per geometria non stimabile | sostenuta in simulazione; sul vero **non risolta** (N = 0) |
| 2 Bordo d'ombra | errore da +2 a +15 cm, mai verso lo stretto, al nominale | simulato, 115 sequenze, un pannello a 1,8 m | sequenze con un fotogramma sotto zero: 0–3,2 %; risoluzione 4,2 cm | sostenuta al nominale; al limite **smentita** la soglia ±20 cm (verso largo) |
| 3 Rumore del centro | fermo: 0,3 / 0,8 / 1,2 cm di mediana; a 2 m il 40 % dei semi a circa 4 cm | simulato, 20 semi per distanza (replica) | 2 m: 22–61 % sopra la nominale; vero: 1 sequenza, descrittivo | K-007 **non risolta** |
| 4a Continuità simulata | 0 su 90 con la catena com'è; 41 su 45 con soglia 40; verità nella regione in 83 su 90 | simulato D435i nominale | 0–4,1 %; 79,3–96,5 %; 84,8–96,2 %; al limite 0 su 6 (0–39 %) | smentita com'è; sostenuta con soglia 40 al nominale |
| 4b Moto di pedoni veri | q = 0,2 copre 0,98–1,00 (prudente); q = 0,1: 0,92–0,95; q = 0,05: 0,82–0,84; errore mediano 0,22 / 0,44 / 0,73 m a 1 / 2 / 3 s | THÖR exp3, **9 persone**, 219 tratti, caschi, occlusione inventata | per persona: 0,96–1,00; 0,86–0,98; 0,76–0,91; errore 0,19–0,25 / 0,37–0,55 / 0,62–0,92 | sostenuta dai dati (solo il modello del moto) |
| 4c Continuità su profondità vera | niente | 1 sequenza, 2 tratti ≤ 0,10 s | 34–100 % | **non risolta** |
| 5 Fermi detti «mobili» | pannello «si muove» in 79 su 90; 5 su 90 con soglia 40 | simulato | 79,4–93,0 %; 2,4–12,4 % (il 10 % non è escluso) | smentita com'è; con soglia 40 compatibile, non mostrata |

## 7. Proposte e che cosa dopo

- **statistico-1.** Riportare ogni copertura come quota di **passaggi** con la verità sempre dentro, non come mediana.
  *Meccanismo:* i fallimenti sono interi passaggi (velocità d'ingresso sbagliata), non fotogrammi sparsi. *Previsione:* sul sensore della squadra, 30 passaggi a 0,5 m/s danno meno di 27 su 30. *La smentisce:* 27 o più.
- **statistico-2.** Il banco d'ingresso (validazione-9) con numerosità che decide: 30 passaggi per caso, criterio 29
  su 30 (limite inferiore 83 %), e **almeno 5 geometrie d'occlusore** per K-014 (pannello a due distanze, cassa,
  scatola, persona). *Meccanismo:* oggi il limite superiore vale per un pannello solo. *La smentisce:* una cella «libero» in ombra in una qualunque.
- **statistico-3.** Portare il simulatore ai buchi veri prima di fidarsi del nominale: 25–35 % di pixel senza dato fra
  0,5 e 3 m, validi a tratti. *Meccanismo:* fusioni e fantasmi nascono dai pixel mancanti e misti. *Previsione:* la continuità con soglia 40 scende sotto 36 su 45. *La smentisce:* 36 o più.
- **statistico-4.** Tarare q su THÖR con «togline una persona» e una terza registrazione (exp2). *Meccanismo:* la
  persona è l'unità. *Previsione:* q fra 0,05 e 0,1, copertura 0,85–0,97 in almeno 8 persone su 9. *La smentisce:* meno di 8.

Dopo: decide il sensore della squadra. Da misurare per primi: pixel validi sul pavimento fra 2 e 3 m, 30 s di
pavimento vuoto, 30 passaggi dietro il pannello con un metro a terra.
