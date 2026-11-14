# PREVISIONI — f10, `22-avversario` (`sciame-avversario`)

Scritte alle **2026-11-14T17:34:54+01:00** (`date -Is`), dopo aver letto contratto, validazione, catena (codice), simulatore
(documento e firme), dati veri (documento), nucleo; **prima** di scrivere o lanciare qualunque mio script. Gli esiti
si aggiungono in fondo, senza toccare il testo qui sopra. Soglia di smentita = ciò che farebbe cadere l'attacco.

**A1 — posa (difetto che simulatore e catena condividono: la posa di `meta.json` è esatta per entrambi).**
Catena con inclinazione creduta 15° + e sulle sequenze simulate `d435i_nom__pavimento_vuoto` e `d435i_nom__scatola15_2p0m`.
- A1a. e = +1°: le celle «libero» calano del 5–20 % rispetto a e = 0. e = +2°: calano di almeno l'80 %.
- A1b. e = −2°: sul pavimento vuoto almeno 300 celle «occupato» in media per fotogramma (a e = 0: 19) e almeno una traccia confermata.
- A1c. e = +3°: almeno una cella dell'impronta della scatola di 15 cm (x ±0,075, z 2,00–2,15) è «libero» in almeno
  8 fotogrammi su 10; a e = 0 e a e = +2°: 0 fotogrammi. *Cade se* a +3° la scatola resta «occupato» o «non osservato» in più di 2 fotogrammi su 10.
- A1d. scena a mano senza rumore (848×480): scatola alta 12 cm a 2,5 m, e = +1,5°: la cella del suo fronte è «libero». *Cade se* non lo è.

**A2 — matrice a mano, posa esatta, ostacolo che non restituisce profondità (pixel a 0).**
- A2a. palo largo 3 cm a z = 2,05 m (pixel a 0): le celle che contengono il suo piede sono «libero» nel 100 % dei fotogrammi, 0 «occupato», 0 «in ombra».
- A2b. lastra 0,4 × 1,7 m a 0 che compare al fotogramma 3: celle della sua impronta e della sua ombra vera restano
  «libero» per esattamente 2 fotogrammi (età 1 e 2), almeno 20 celle; poi «non osservato»; mai «in ombra», nessuna traccia.
- A2c (ricerca). Con posa esatta e profondità valida NON mi aspetto di trovare un «libero» falso nella mappa
  (`pulita` e l'ombra prudente lo impediscono): se lo trovo è una sorpresa.

**A3 — due persone nella stessa ombra (scena a mano; nessuna sequenza la contiene).** Pannello 1 × 1,8 m a 1,8 m; B
è dietro dal primo fotogramma (mai tracciata); A entra da sinistra, si ferma nascosta; poi B esce a destra.
- All'uscita di B: evento «riaggancio» sull'identità di A; da lì A è «osservato» (≥ 5 fotogrammi) a meno di 0,3 m
  da B mentre A è nascosta a x = −0,25; le celle di «possibile presenza» scendono a 0 e la cella vera di A resta
  «in ombra» senza avviso. Nessun invariante violato (0 `InvarianteViolato`). *Cade se* esce «identità ambigua» o nasce una traccia nuova per B.
- A3b (codice ≠ testo). Il riaggancio dà «osservato» con una misura fuori dalla porta al 99 % (d2 > 9,21): l'invariante 3
  del testo («misura in porta») è controllato nel codice solo come «ha una misura». *Cade se* d2 ≤ 9,21 in questa scena.

**A4 — occlusore che si muove (scena a mano).** A entra dietro il pannello e si ferma; poi pannello e A si spostano
insieme a 0,5 m/s verso destra (A sempre nascosta).
- Evento «strato_finito: celle_libere» e chiusura della traccia di A a soggetto nascosto; almeno 10 fotogrammi con A
  nascosta e la sua cella fuori dalla «possibile presenza». *Cade se* lo strato segue il pannello o resta acceso fino alla fine.

**A5 — THÖR nelle condizioni della catena.** Stesso `kalman.py`, exp3, finestre come la validazione.
- A5a. σ = 6 cm (il solo dato vero, D415), ultime 5 misure tolte (0,33 s: il gruppo «tagliato» non aggiorna il
  filtro), q = 0,2: errore mediano a 1 s di buio **≥ 0,30 m** (validazione: 0,21). *Cade se* < 0,26.
- A5b. rincorsa di 4 misure (0,27 s: la garanzia vale «da 4 fotogrammi»), σ = 6 cm, q = 0,2: errore mediano a 1 s ≥ 0,45 m e raggio al 95 % ≥ 1,5 m.
- A5c. q = 0,1 («validazione-8», 0,945 a posteriori): in almeno una delle due condizioni sopra la copertura
  dell'ellisse al 90 % a 1 s esce da 0,90–0,97.
- A5d. Finestre con velocità sotto 0,3 m/s: meno del 15 % (THÖR quasi non contiene soste, cioè il caso b in cui la catena sbaglia di 4,2 m).

**A6 — il segno dell'errore dell'ombra è un'ipotesi del simulatore («ingrossamento 2 px», senza misura).** 10
sequenze `pannello_vuoto`-simili (a12 s00–s09 in memoria) con `bordo_ingrossamento_px` = 0.
- La mediana dell'errore scende di almeno 1,5 cm (da +6,2) e compare almeno un lato-sequenza con minimo < 0 cm
  (ombra più stretta della vera). *Cade se* il minimo resta ≥ +2 cm: allora «sempre verso il largo» non dipende da quell'ipotesi.

**A7 — verità del simulatore, tre fotogrammi a mano** (`d435i_nom__pannello_a12__s00`: uno visibile, uno a metà,
uno nascosto), con geometria mia (raggi su una capsula, pannello come rettangolo) e contando nell'immagine i pixel
alla profondità del soggetto. Previsione: la verità **regge** (scarto di `frazione_visibile` ≤ 0,05 nei tre; 0 pixel
del soggetto nel fotogramma nascosto, a meno della testa); spigoli dell'ombra a ±15,5°. *Smentita se* uno scarto > 0,10.

**A8 — soglia 40 fuori dalla geometria su cui è stata scelta** (a12, passaggi dispari, D435i nominale, in memoria).
- A8a. attore sulla linea z = 2,1 m (la soluzione dice «a non più di 2,3 m»): continuità pulita ≤ 5 su 10 (a 2,3 m: 13 su 15).
- A8b. stessa scena a 848×480 (la risoluzione del nucleo), soglia 40: continuità pulita ≤ 5 su 10; con soglia 160 (scalata per i pixel) ≥ 7 su 10.
  *Cadono se* la continuità resta ≥ 8 su 10.

**A9 — lettura dei numeri già prodotti (nessuna prova nuova):** su TUM, sola sequenza vera con posa, le celle «libero»
sono 58 di mediana su 5400: prevedo che meno del 5 % delle celle·fotogramma sia «libero» e che quindi l'ipotesi 1
sul vero poggi su un campione quasi vuoto.

## Aggiunta dopo l'esito di A6 (scritta alle 2026-11-14T17:39:10+01:00, prima della prova A6bis)

Visto dopo A6: la misura dell'errore d'ombra può valere solo +2,0 + 4,19·n cm, perché tutte le sequenze hanno lo
spigolo a ±15,52° (al 52 % della cella 15–16°). **A6bis** (nuova): pannello con lo spigolo a ±15,05° (mezza larghezza
0,484 m: lo spigolo copre il 5 % della colonna), 10 sequenze di 10 fotogrammi. Previsione: con soglia 40 almeno un
fotogramma-lato con errore < 0 (ombra più stretta: −0,2 cm o meno); con soglia 3 e ingrossamento 2 px nessuno.
*Cade se* con soglia 40 il minimo resta ≥ 0.

## Esiti (scritti alle 2026-11-14T17:41:41+01:00; cifre e file in ATTACCO_DATI.md e in `uscite/`)

| # | Esito | Cifra |
|---|---|---|
| A1a | **smentita nei numeri** | a +1° il «libero» non cala (100 %); a +2° cala del 37 %, non dell'80 % (nel simulato il rumore tiene 3 punti nella fascia); nella scena senza rumore a +2° cala del 75 % |
| A1b | **regge** | a −2°: 761 celle «occupato» per fotogramma, 42 tracce. Non previsto: già a −0,5° le tracce fantasma passano da 28 a 81, e a +0,5° scendono a 3 |
| A1c | **regge a +3°** (10 su 10), **smentita a +2°** (avevo scritto 0: sono 2 su 10; a +1°: 1 su 10; a +2,5°: 9 su 10) | e = 0: 0 su 10 |
| A1d | **regge**, e oltre | 12 cm a +1,5°: 7 celle su 7 «libero»; non previsto: 10 cm a +1,0° con tutto il resto normale (1630 celle libere) |
| A2a | **regge** | piede del palo «libero» 6 fotogrammi su 6 |
| A2b | **regge**, con una cosa non prevista | 2 fotogrammi di «libero» su impronta (11 celle) e ombra (62); poi 6 celle su 11 dell'impronta restano «libero» a regime (spicchio di suolo davanti) |
| A2c | **regge** | nessun «libero» falso trovato con posa esatta e profondità valida |
| A3 | **regge** | riaggancio dell'identità di A su B al fotogramma 27; A «osservato» 22 fotogrammi mentre è nascosta; 25 fotogrammi fuori dalla possibile presenza; 0 invarianti violati |
| A3b | **cade** | d2 = 0,165: la misura è in porta |
| A4 | **regge** | «strato_finito» al fotogramma 61; 21 fotogrammi nascosta e fuori dallo strato; 0 su «libero» |
| A5a | **regge** | 0,32 m (exp3), 0,31 (exp1) |
| A5b | **regge sull'errore** (0,52 m), **smentita sul raggio** (1,28 m, non ≥ 1,5) | |
| A5c | **cade** | q = 0,1 a 1 s: 0,963 e 0,913, dentro 0,90–0,97 |
| A5d | **smentita** | finestre lente 26,0 % (exp3), non < 15 %; «cammina e poi si ferma» 12 su 219 |
| A6 | **regge a metà** | mediana da +6,2 a +2,0 cm; nessun valore negativo (la seconda metà cade) |
| A6bis | **cade** come scritta (con l'ingrossamento del simulatore il minimo è +4,0); senza ingrossamento e con soglia 40: 63 fotogrammi-lato su 200 a −0,2 cm | |
| A7 | **regge** (la verità è giusta) | scarto massimo 0,010; 0 celle discordi su 100 nell'anello a 2,45 m |
| A8a | **regge** | 4 su 10 a 2,1 m (controllo a 2,3 m: 8 su 10) |
| A8b | **regge** | 848×480: soglia 40 → 0 su 10; soglia 160 → 10 su 10 |
| A9 | **regge** | TUM: 52 celle «libero» in media su 5400 (1,0 %) |
