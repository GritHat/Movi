# Soluzione unica, versione 3 — f12, `01-soluzione` (`sciame-scene-dinamiche`, responsabile del nucleo)

14 novembre 2026, dalle 17:47:52 (`date -Is`). Accanto: `TABELLA_CORREZIONI.md` (una riga per correzione obbligata, con il paragrafo di questo documento), `PREVISIONI.md`, `controlla_sigle.sh`.

## 0. In testa

**Che cos'è.** Il nucleo versione 2 con dentro le correzioni approvate dai quattro verdetti dell'arbitro e dall'attacco alla specializzazione. Fonti: **N** `f4/H-012/05-correzioni/SOLUZIONE_V2.md`; **VN** `f4/H-012/09-arbitro/VERDETTO.md`; **AU** `f5/02-audit/AUDIT.md`; **V7** `f7-estensione/16-verdetto/VERDETTO_ESTENSIONE.md` (**A7** il suo attacco, `14-attacco/CONTROPROVE_DECISIONE.md`); **V8** `f8-continuita/16-verdetto/VERDETTO_CONTINUITA.md` (**M** `13-soluzione/MODIFICHE_CONTINUITA.md`, **A8** `14-attacco/CONTROPROVE_MODIFICHE.md`); **V9** `f9-preproposta/13-verdetto/VERDETTO_PREPROPOSTA.md`; **AS** `f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md`; **f10** `f10-dati/` (`10-catena/CATENA.md`, `20-validazione/VALIDAZIONE_DATI.md`, `21-statistica/ANALISI_DATI.md`, `22-avversario/ATTACCO_DATI.md`). Sigle: condizioni **1–9** di VN e **decima** di V8; **a–h** di V7; **M1–M8**, **c1–c10**, `statistico-3…7` di V8; **S1–S12** di V9; **C1–C8** di AS; le correzioni interne del nucleo sono «N-C#».

**Stato.** Tutto è simulazione, conto o lettura di schede tecniche, **a sensore fermo**: nessun fotogramma di una camera vera è passato da una prova vagliata dall'arbitro. È un **progetto di prototipo**. Ogni stato è quello del verdetto citato; non ho eseguito simulazioni nuove e non ho rifatto i conti (**non verificati da me**: valgono i riconteggi dell'arbitro). Le regole sono provate una per una o a gruppi, **mai tutte insieme**: la prova d'insieme (criteri C-C e C-D del contratto) spetta ad altri ruoli.

**f10 e la marca [prel.].** Alle 17:50 il verdetto di f10 non esisteva (`ls`); è comparso alle 17:52, mentre scrivevo, e l'ho letto alle 18:02: **V10** = `f10-dati/23-verdetto/VERDETTO_DATI.md`. V10 riconta e conferma le cifre di f10 che cito, e ne fissa lo stato: **profondità simulata dalle schede tecniche o tracce pubbliche di persone, mai un sensore della squadra**. La marca **[prel.]** resta su ogni cifra di f10 e si legge così. V10 cambia tre stati del nucleo (identità al ritorno «100 %»: **smentita** su profondità realistica; muro «mobile» 0,0–0,2 %: **smentita**; q = 0,2: **corretto** verso 0,05–0,1) e consegna i difetti F-401…F-413: stanno nei blocchi e nella tabella (§8 di `TABELLA_CORREZIONI.md`). Le loro correzioni sono **non provate**: qui non diventano regole.

**Cambi di stato proposti da me:** nessuno. **Scelte fra verdetti in disaccordo:** tutte nel §5. **Regole violate:** nessuna che io sappia. **Scostamenti:** la prima stesura era di 15 pagine a corpo 10 e l'ho accorciata; V10 è entrato a stesura finita, con ritocchi e non con una riscrittura; letti per intero N, V7, V8, V9, V10, M, AS e il contratto d'integrazione; di VN, AU, A7, A8, f10 e della specializzazione le parti citate; non aperti `TORNEO.md`, `BANCO_DI_PROVA.md`, `DECISIONE.md`, `MOTO_PROPRIO.md`, `CONTRATTO.md`, `STATO_PROGETTO.md`, `RIFERIMENTI.md`, gli addendum. Idee nuove: nessuna.

## 1. Schema a blocchi

```
[1 sorgente + controllo all'avvio] -> [2 mappa polare a 4 stati] -> [3 gruppi, «tagliato», «mobile»]
 -> [4 associazione + Kalman] -> [5 ciclo di vita, ingresso nell'ombra] -> [6 previsione R90] [7 avviso R100] [8 riaggancio]
[9 salute del sensore] --scavalca tutto--> [10 regole -> schermo e suoni]   [11 registro eventi]   [12 precisione sul posto]
```
Ciclo a 15 Hz su flusso a 30 fps. Tre assi separati (V7 §2): **applicazione**, **portatore del sensore** (supporto fisso; veicolo senza equipaggio **fermo**), **uscita**. La rete che mette l'etichetta «persona» è facoltativa, asincrona, non decide niente, ed è la prima cosa che si taglia (V8 §5, V9 §5).

Convenzioni. «Fotogramma» = fotogramma elaborato; 3 fotogrammi = 0,2 s; le soglie valgono **in secondi** (cond. 2, AU 7). «Cuneo» = ombra dell'occlusore in cui una traccia è entrata. **R100** = cuneo più 0,40 m: è l'avviso. **R90** = regione prevista al livello dichiarato. Parametri: *scelto* = fissato a tavolino; *tarato* = ricavato da dati, qui sempre simulati.

### 1.1 Sorgente e controllo all'avvio

**Entra:** flusso di profondità (ordine di preferenza dei sensori in `f10-dati/04-embedded/INVENTARIO_E_DECISIONE.md` [prel.]), oppure una cartella nel formato di `f10-dati/CONTRATTO_DATI.md`, oppure il simulatore. **Esce:** fotogramma con marca di cattura e contatore; la **configurazione dichiarata**, che viaggia in ogni uscita.
```
all'avvio, a scena vuota e ferma:
  spegni i filtri della camera (persistenza, riempimento dei buchi)
  autoverifica: mano sul sensore -> pixel validi < 10 % entro 3 fotogrammi, altrimenti NON PARTE
  stampa risoluzione e campo del flusso usato; posa dalla taratura, confrontata col metro: oltre 1° NON PARTE
  tara la quota di pixel validi; conta le celle che ricevono suolo = zona valutata
  dichiara una volta: vuoto vicino (suolo solo da 1,24 m), fuori campo, oltre portata, quote non viste
  configurazione <- {sensore, risoluzione, posa, profilo, predittore, moduli}: in esercizio NON cambia
```
**Parametri.** Quota 1,2 m e inclinazione 15° (N; scelti). 30 fps, 15 Hz (N; scelti). Portata 3 m (N; scelta: «dove il rumore radiale resta ≤ 5 cm», da misurare). Autoverifica 10 % in 3 fotogrammi (VN cond. 1; scelta). Tolleranza d'inclinazione 1° (AS C7, A7; conto geometrico: il requisito a 3 m è 1,02°).
**Stato.** Non provato su hardware. [prel.] Con i filtri accesi e il sensore coperto restano 989–995 celle «libero» per altri 3 fotogrammi; con 1° d'errore d'inclinazione un ostacolo di 10 cm a 2,55 m esce «libero» (stesso verso in A7: 21 celle su 21 a 2,8 m); il piano stimato dai primi fotogrammi sbaglia di 5° su una sequenza vera: per questo la posa viene dalla taratura. **Incorpora:** cond. 1, 4, 9; AU 1, 9, 11; (e); S1 minima; S10 minima (frase d'avvio); C7, C8; F-404, F-406, F-413. Prima misura col sensore secondo V10 §6 (soglie scritte, mai eseguita): 30 s di pavimento vuoto, 0 tracce confermate; un oggetto di 10 cm a 2,5 m esce «occupato» (F-403, F-404).

### 1.2 Mappa e «libero» della cella

**Entra:** profondità, posa. **Esce:** griglia polare, quattro stati per cella (**libero, occupato osservato, in ombra, non osservato**); la maschera del «non visto libero» (tutto ciò che non è «libero»), rifatta a ogni ciclo.
```
per ogni cella, a OGNI fotogramma, senza memoria:
  occupato      <- almeno 3 pixel validi con quota fra 0,07 e 2,0 m
  in ombra      <- la cella sta oltre il primo ritorno del suo azimut
  libero        <- non occupato, non in ombra, e un pixel dell'impronta della cella è valido ORA
                   e legge la profondità attesa del suolo entro la tolleranza        [V-018]
                   ripiego: stato(centro della cella a quota 0,20 m) == LIBERO
  non osservato <- tutto il resto (buco, fuori campo, oltre portata, vuoto vicino, 1–2 pixel)
occupato e ombra del fotogramma vincono; nessun «libero» ricordato, dedotto o dato da un timer
per settore: «suolo visto libero fino a d m»; una quota si dichiara solo se LETTA (V-017, 4 ore)
```
**Parametri.** Cella 1° × 0,1 m fino a 3 m (N; scelta). Quota d'ostacolo 0,07–2,0 m (N; scelta). Pixel minimi 3 (A7 §3.1; scelto; [prel.] dipende dalla risoluzione: `sd-K4`). Memoria 0 fotogrammi (V7). Tolleranza del suolo: quella di `vq3c.c`; la catena f10 usa 5 cm [prel.]; da rimisurare.
**Stato.** Sicurezza **sostenuta dai dati in simulazione, camera ideale ferma, due autori**: 0 punti oltre 5 cm dentro un corpo dati per liberi, anche se il corpo non rimanda segnale (V7 §5.8). Prezzo: resa del libero vero 79–88 % col 5 % di buchi, 8 % col 30 %. La regola del nucleo («libero» ricordato per 3 fotogrammi) è un **controesempio in simulazione, due programmi**, ed esce. **K-107 aperta.** [prel.] 0 celle «libero» dentro l'ombra vera su 2 907 032 celle·fotogramma, a posa esatta, su tre geometrie, con la catena f10 che ha ancora la memoria: non è una prova di questa regola. Controesempi: vetro (V7); palo e lastra che non rimandano segnale [prel.]. **Incorpora:** (a), (b), (g); cond. 7; AU 2, 6, 11; il principio di S10.

### 1.3 Gruppi e regola «mobile»

**Entra:** celle occupate, immagine. **Esce:** gruppi con centro, larghezza, marca «tagliato», «mobile» sì / no / non valutabile.
```
gruppo   <- celle occupate connesse; centro = media dei punti
tagliato <- in immagine il gruppo confina con un bordo di profondità più vicino (c3);
            senza sensore: accanto, nello stesso anello, c'è l'ombra di un gruppo più vicino
tagliato => non aggiorna il filtro, non entra in «mobile», non fa nascere tracce;
            si disegna a contorno pieno, «visto in parte», senza velocità (N-C6, c6)
mobile   <- spostamento fra due misure distanti al più 1 s (finestra che cresce), ciascuna media
            di 3 fotogrammi, > 5·σ(z)·√2 lungo un asse; la χ² si registra a fianco
```
**Parametri.** σ(z) 1,5 / 3,4 / 6,0 cm a 2 / 3 / 4 m (N, documento del costruttore; **da misurare**, M8). Finestra e media (N-C8, N-V1; scelte). Soglia 5·σ·√2 (N; scelta).
**Stato.** A 2 m **sostenuta in simulazione** (100 %, N = 2000); oltre, **non risolta** (K-007). c3, c6: **non provate**. [prel.] Su profondità realistica il pannello fermo è «mobile» in 79 passaggi su 90 e la persona si fonde col pannello in 90 su 90; l'unico rumore vero, descrittivo, è 5,8–6,8 cm sotto 3 m. V10: N-C6 da sola **non basta** (K-017 aggravata; F-401, F-412); la correzione proposta, soglia di pixel proporzionale, è **non provata** (`sd-K4`). **Incorpora:** cond. 5; c3, c6. Ripiego: «mobile» dalla velocità del filtro (AU 8).

### 1.4 Associazione e filtro

Kalman a velocità quasi costante su [x, y, vx, vy]; porta al 99 %; ungherese con priorità alle confermate (ripiego: una traccia, al più vicino); conferma 3 su 5. **Entrano solo gruppi non tagliati.** **Parametri.** q = 0,2 m²/s³ (N; scelto; V10 lo dà per **corretto** verso 0,05–0,1 su tracce di 9 pedoni veri [prel.]: 0,2 è prudente, copre 0,98–1,00; resta 0,2 finché 0,1 non è provato su dati nuovi: decisione 3 di V10). q **non** si tara sulle innovazioni alla ricomparsa: premierebbe gli scambi (F-409). R(z) dal rumore misurato (M8; da tarare sul posto). **Stato.** Il cerchio del filtro **non è** la precisione dichiarata: a 2 s contiene il soggetto nello 0,00–0,06 dei casi (V8 §1); la dà il blocco 1.6. L'identità con due tracce pendenti non si dà mai (74 % di scambi, N). Massa e accelerazione non si stimano. **Incorpora:** cond. 6; M8.

### 1.5 Ciclo di vita della traccia e ingresso nell'ombra

**Esce:** lo stato della traccia: **osservato**, **visto in parte**, **non confermato**, **previsto**, **previsto ampio**; oppure una chiusura col motivo. **«Perso» non è più uno stato** (M2; VN §5.5 è sostituita).
```
traccia confermata (vista almeno 4 fotogrammi), senza misura non tagliata nel ciclo:
  occl <- ombra di un occlusore che NON è il gruppo della traccia              (K-018, cond. 8)
  gruppo tagliato ora                                    -> ENTRATA subito               (c4)
  senza misura da 2 cicli e (ultima misura a < 0,40 m da occl,
       o punto previsto in occl o entro 0,40 m)           -> ENTRATA                 (M1, c4)
  ultima misura a < 0,40 m dal vuoto vicino o dal bordo del campo
       -> avviso sul non osservato entro la fascia; niente «suolo libero» lì finché non è rivista (C2, d)
  altrimenti: «non confermato» con l'età per 0,2 s, poi chiusa «non più rilevato»
traccia chiusa o non confermata, ultima misura entro 0,75 m da un'ombra -> accende l'avviso (c7)
ENTRATA -> partono 1.6 e 1.7.   Chiusure in ombra, elenco chiuso: (1) riagganciata; (2) identità ambigua;
  (3) ombra vista libera; (4) affidabilità persa; (5) fuori dall'area osservata. Nessun timer chiude.
```
**Parametri.** 0,40 m (N, M1; scelto). 2 cicli (c4; scelto dopo una prova sugli stessi semi). 0,75 m (c7; scelto, non provato). 4 fotogrammi (N; tarato in simulazione: con 3 la traccia manca nel 27,1 % dei casi, con 4 nel 5,2 %).
**Stato.** M1 **sostenuta in simulazione**: nascosti senza traccia pendente 87 → 9 passaggi su 2800; 499 → 16 su 600 con l'ombra stimata 20 cm stretta. c4: false entrate 92 → 7 su 400. c7, C2, (d): **non provate**. **Controesempio:** traccia chiusa prima dell'ombra in 130 passaggi su 1581 con rilevamento 0,7 e corpo esteso. **K-220 aperta.** **Incorpora:** M1, M2, c4, c7; cond. 6, 8; AU 4; C2; (d).

### 1.6 Previsione durante l'occlusione

**Entra (interfaccia unica, M3):** stato della traccia all'ultima misura; maschera del «non visto libero» a ogni ciclo. **Esce a ogni ciclo, fino a una chiusura:** celle di R90, punto, età, livello, stato.
```
sd-0 (ripiego, PER PRIMO): disco a velocità costante, raggio da tabella, ritagliato
sd-1 (principale): 400 percorsi registrati trapiantati su punto e velocità d'ingresso; 200 proseguono,
   200 si fermano a un istante uniforme; un membro su una cella vista libera oltre 0,20 m dall'ombra
   pesa un decimo a ogni ciclo; R90 = celle più dense fino al 90 %, dopo 3 passate di lisciatura
pavimento: nessuna cella -> R90 = tutto il non visto libero dell'ombra, stato «ampio»
sempre: R90 ⊆ R100; R90 mai su «libero» oltre 0,20 m; l'evidenza negativa restringe solo R90
punto: quello del filtro finché sta su celle non viste libere; altrimenti fermo 8 cicli, poi verso
   il baricentro dei membri non visti liberi, al più 0,167 m per ciclo
livello: «almeno 9 su 10» fino a 2 s senza osservazione; «almeno 8 su 10» fino a 3 s; poi «ampio»
PREVISTO AMPIO se: R90 > 80 % delle celle d'ombra, o pavimento, o > 3 s, o ingresso < 0,3 m/s,
   o profondità / posa degradate. In «ampio»: tutto il non visto libero dell'ombra, tratteggiato,
   NESSUN punto, «PREVISTO AMPIO · dietro l'ostacolo o fuori area · da Y s».  Mai sparisce.
```
**Parametri.** 400 membri, 200 / 200 (M; scelti). Fascia di ritaglio 0,20 m (M; scelta). Livello 90 %, uno solo (V8; scelto: nessuna candidata tiene il 50 %). Lisciatura 3 (M; **tarata in simulazione**: con una 0,78–0,83). Soglia 80 % e orizzonte 3 s (M, c8; **scelti dopo i dati**: K-202). 0,3 m/s (c5; scelto: a 1 s dà 0,65, non basta). Punto: 8 cicli, 0,167 m (M; scelti). Libreria: almeno 200 percorsi, due persone, tre andature (c9, `statistico-6`; **aperto**, K-221: «30 camminate» smentita).
**Stato.** *Continuità:* **dimostrazione condizionata** (premessa: la traccia è entrata) più **evidenza in simulazione**: 0 passaggi con un ciclo senza regione su 2716 / 2800 / 2798 e, a semi riparati, su 13 638 / 5600 / 5597. *Precisione:* **sostenuta dai dati in simulazione nel dominio del §7**, con sd-1, maschera d'ombra esatta e soggetto puntiforme: limite inferiore di Wilson sopra 0,90 in 45 celle su 45 fino a 2 s, sopra 0,85 in 60 su 60 fino a 3 s. sd-0: 0,85 in 60 su 60, 0,90 solo in 37 su 45, e da 2 s è grande quanto l'ombra. *Punto:* errore mediano 0,18 / 0,39 / 0,60 m a 1 / 2 / 3 s; arretra nel 18 / 4 / 3,5 % dei «prosegue»; su «libero» dopo il quinto ciclo in 13 / 0 / 23 cicli (soglia 0: **non superata**). Fuori dominio: **controesempi** (§7). [prel.] Il predittore di f8 non è innestato nella catena f10: su profondità realistica R90 non è mai stata misurata. **Incorpora:** M2, M3, M4; c5, c8; `statistico-5`; decima condizione; S3 (una ipotesi), S4a.

### 1.7 Avviso di «possibile presenza»

```
R100 <- cuneo dell'occlusore d'ingresso, tagliato alla griglia, più 0,40 m; con la sua età; nessun tetto di tempo
la previsione ACCENDE l'avviso e non lo toglie mai; le chiusure (2), (4), (5) non lo tolgono
rilascio cella per cella: «libero» nel fotogramma per 3 fotogrammi di fila E oltre la fascia; oppure riaggancio
più pendenti ambigue nella stessa ombra -> UN avviso con contatore ed età, senza predittore (c2)
un'ombra in cui non è entrato nessuno resta «in ombra»: mai «libero», mai avviso
con la latenza misurata: fascia >= 0,20 m + mezza larghezza + v_max·(età + latenza)   (cond. 2, C4)
```
**Parametri.** Fascia 0,40 m (N; scelta): onesta **fino a 1,4 m/s**, classe «persona», con 155 ms di latenza stimata, a margine zero. Rilascio 3 fotogrammi oltre la fascia (N, A7 §3.3; scelto).
**Stato.** **Per costruzione** più conteggio: 0 nascosti fuori da R100 su 175 802 istanti e 156 celle di controprova, anche con l'ombra a −20 cm (V8 §2). **Controesempi:** un secondo soggetto dalla stessa ombra prende l'identità e spegne l'avviso (193 su 193; 347 su 357: K-016, **non riparata**); 13 passaggi su 4800 con un rilevamento mancato su dieci e ombra a −20 cm (VN). [prel.] Su profondità realistica, parametri del nucleo: centro nascosto nell'avviso in 2939 fotogrammi su 3038, «in ombra senza avviso» in 99, mai «libero»; occlusore che si muove: 21 fotogrammi fuori. Costo: l'avviso copre il 28,2 % del libero visto (N §5). **Incorpora:** cond. 2, 6; N-C4, N-C5; c2; C4; V8 §4.9.

### 1.8 Riaggancio

```
candidato <- la prima misura NON tagliata (c1)
RIAGGANCIA (stessa identità; chiude previsione e avviso) se è entro 0,40 m da R90 (M7), entro 0,75 m
   dall'ombra d'ingresso (c1; in demo senza il margine dalla portata) e la traccia è la pendente più recente (c2)
   -- finché la prova C-C contro l'estraneo non è passata: 0,40 m dall'ombra d'ingresso (N-C1) --
altrimenti «identità ambigua»: traccia nuova; la vecchia resta «previsto ampio»; l'avviso resta
dopo un'affidabilità persa ogni riaggancio è «identità ambigua» (V7 c)
alla ricomparsa: scarto fra punto e prima misura a schermo per 0,5 s, in centimetri
```
**Stato.** c1: 398 su 399, 332 su 338, 275 su 277 nelle tre geometrie, **provata dopo, sugli stessi semi: indizio**; **mai contro l'estraneo** (K-219, sicurezza). Senza c1 il riaggancio cade (102 su 273, 306 su 397, 250 su 332) e l'identità «100 %» del nucleo non regge con N-C6 (K-218). [prel.] Su profondità realistica il riaggancio prende un fantasma dello spigolo a soggetto nascosto (F-402) e «una sola traccia pendente» è falsa (7–66 tracce fantasma per passaggio, F-403): escludere il gruppo dell'occlusore è la correzione proposta, **non provata**; il riaggancio parte sempre da una misura non tagliata, così il filtro riparte da una misura piena (F-408). Prova senza sensore di V10 §6: identità almeno 28 su 30 **e** scatola di 15 cm a 2 m vista almeno 9 volte su 10; se cade, l'identità al ritorno resta smentita anche in simulazione. **Incorpora:** M7, c1, c2; N-C1; cond. 3.

### 1.9 Salute del sensore e «affidabilità persa»

```
NON IN SALUTE se: nessun fotogramma nuovo per 0,13 s o tre identici; pixel validi sotto metà della taratura
   per 0,2 s (contati sui PIXEL); IMU oltre 0,5° o 5°/s; inclinazione del suolo fuori di 1° dalla taratura da fermo
allora: griglia tutta «non osservato»; tracce in previsione, «ampio, non aggiornata · sensore non affidabile»;
        il ciclo ESCE COMUNQUE, col segnale dedicato
al ritorno dopo T s: regione <- (regione dilatata di v_max·T + fascia) ∩ non osservato; riagganci «ambigui»
```
**Parametri.** 0,13 s (N; scelto; da rifissare dopo 60 s di conteggio a vuoto e sotto carico, AU 7). Metà della taratura per 0,2 s (N-C10, V7; scelto). IMU (N; scelto; **solo profilo fermo**, cond. 4). Piano 1° ((e), C7; conto, non provato).
**Stato.** N-C10: segnale in 0,13 s, 0 falsi in 60 s, **in simulazione, rumore dell'IMU ipotizzato**. Il conteggio sui pixel non è misurato (il difetto sì: 1444 celle «note» su 1460 col 10 % di pixel validi). Il ramo (c): conto in pianta, 0 fotogrammi fuori su 60, **non riprovato** (K-109). **Incorpora:** (c), (e); cond. 4; C7; AU 7.

### 1.10 Tabella di regole e uscite

Regole scritte, non apprese. **Nessuna uscita è un comando.**
```
fuori scala, scavalca tutto: «AFFIDABILITÀ PERSA»
per settore della zona valutata, il livello più alto fra:
   «attenzione»                    <- mobile in avvicinamento (detto per primo), poi occupato a d m
   «zona non verificata»           <- possibile presenza, previsto, in ombra, buco prima della portata
   «suolo visto libero fino a d m» <- solo celle «libero» fino a d; d <= portata − 0,40 m
per traccia, la forma prima del colore, mai verde: disco pieno = osservato; contorno pieno = visto in parte;
   anello vuoto + regione tratteggiata = previsto; sola regione tratteggiata = previsto ampio
etichetta: «PREVISTO · almeno 9 su 10 qui dentro · larga X,X m · non visto da Y,Y s»; età MISURATA, mai «0 ms»
sotto tutto: il cuneo di possibile presenza con l'età
suono: un segnale di 0,3 s per cambio di stato; la frase solo a stato stabile
nelle 4 ore, solo etichetta: «avvicinamento diretto» (S6, S7): nessun numero abbassa un livello
```
**Stato.** Regole di progetto; il messaggio per settori **non è mai stato generato** (AS §3). L'ordine «mobile per primo» è quello del nucleo (N-C3: 100 / 100 / 99,5 % in simulazione); la tabella riscritta **non è provata** (K-306…K-308). Latenza: **non risolta** (155 ms stimati contro 150). Nessuna persona ha visto lo schermo o ascoltato un suono. **Incorpora:** N-C3, N-C11; M5, c6, c8; S2 (età subito; compensazione nelle 4 ore, sulla sola uscita, mai in ombra), S5, S8 riscritta; (b); C2, C4; A7 §3.10.

### 1.11 Registro degli eventi

Una riga per evento: ora, identità, evento, **come lo so** (osservato | dedotto), età, settore, configurazione. Eventi: *ingresso*; *scomparsa dietro l'ostacolo*; *non ricomparso da n s* (dedotto); *ricomparsa* (riagganciata | identità ambigua); *affidabilità persa* e *tornata*. Mai «sosta» o «uscito»: non si distinguono (V9 F-307). Nessun evento nasce da un peso. «Oggetto fermo comparso o rimosso» (T-008): 4 ore, con un secondo autore. **Stato.** Logica controllata dal suo autore (0 violazioni su 600 scene), eventi mancati nel 16–52 % delle scene, scomparse spurie nel 12,5 %; **mai provato sul nucleo** (V7 §2). È la sola copertura di «monitoraggio di attività». **Incorpora:** S11 riformulata; V7 §5.12.

### 1.12 Misura della precisione sul posto

```
occlusione virtuale: una COPIA della catena riceve le misure con un cuneo cancellato a programma;
   la persona resta visibile alla catena vera e fa da verità a ogni ciclo
tabellone: la persona è DENTRO la regione a 1 s e a 2 s? -> «dentro k su n» + intervallo di Wilson;
   denominatore: nascosti dentro l'area osservata; chi esce dall'area a parte
scheda: 4 comportamenti × 30 passaggi, camminatori diversi dalla taratura;
   per cella: >= 28 regge; <= 23 smentita; altrimenti altri 30 e >= 54 su 60
a schermo: «27 su 30: fra 0,74 e 0,97»; la parola «tarato» non si usa
```
**Stato.** **Mai eseguita**; non rende il corpo tagliato dal bordo. È la «valutazione realistica della precisione»: senza, a schermo va solo la cifra di simulazione col suo dominio. L'identità al ritorno resta misurata a parte (criterio a due stadi di N); la misura H9 esce. [prel.] 28 su 30 ha limite inferiore 78,7 %: non mostra il 90 %. **Incorpora:** M6, M8; `statistico-3`, `-4`, `-6`; c9.

## 2. Invarianti, rinumerati

| # | Invariante | Stato | Controllo che lo esercita |
|---|---|---|---|
| I1 | «Libero» esiste solo nel fotogramma corrente, dove il suolo è letto ora; non si ricorda, non si deduce (sostituisce l'1 del nucleo) | sostenuto dai dati in simulazione, due autori; K-107 aperta | asserzione nella mappa; prova C-D; al sensore: «libero» dentro l'ombra vera del pannello (soglia 0) |
| I2 | Buco, fuori campo, oltre portata, vuoto vicino, ombra, sensore non in salute: mai «libero» | dimostrazione condizionata (profondità valida = giusta; superfici che rimandano; assetto entro 1°) | asserzione; mano sul sensore |
| I3 | Disco pieno solo con una misura non tagliata in porta nel ciclo; una previsione non esce come osservazione. Vale in un solo verso | per costruzione, non misurato; [prel.] 8 passaggi su 90 con «osservato» a soggetto nascosto, parametri del nucleo | dischi pieni a soggetto nascosto nell'occlusione virtuale (soglia 0) |
| I4 | R90 ⊆ R100; R90 mai su «libero» oltre 0,20 m; l'avviso mai su «libero» oltre 0,40 m | dimostrazione condizionata; 0 casi ricontati | asserzione a ogni ciclo |
| I5 | Nessun timer, modello appreso, peso o conferma dell'operatore produce un «libero», toglie un avviso o abbassa un livello | per costruzione | lettura del codice: «libero» si scrive solo in 1.2, il rilascio solo in 1.7 e 1.8 |
| I6 | L'evidenza negativa vale dove la profondità è valida ora, restringe solo R90, mai R100 | per costruzione | asserzione; sosta di 30 s |
| I7 | L'avviso finisce solo guardando: riaggancio (1.8) o celle viste libere 3 fotogrammi di fila oltre la fascia | sostenuto in simulazione; controesempi: secondo soggetto, occlusore mobile | prova C-C; atto «si ferma dietro» |
| I8 | Ogni uscita porta contatore, età, livello, configurazione, «come lo so» | per costruzione | schema della riga per ciclo |
| I9 | Niente massa né accelerazione; punto e regione previsti escono solo col loro stato | dimostrato nel modello del punto materiale (massa); due calcoli (accelerazione) | schema d'uscita |
| I10 | **Continuità:** per ogni traccia confermata entrata in un'ombra, a ogni ciclo fino a una chiusura, escono regione, età, livello e (fuori da «ampio») un punto | dimostrazione condizionata più 0 vuoti su circa 8300 passaggi; controesempio all'ingresso | cicli senza regione (soglia 0); prova C-C |
| I11 | Configurazione fissata all'avvio; mappa e griglia non cambiano in esercizio | regola di progetto | la configurazione in ogni riga |
| I12 | Il livello più basso è «suolo visto libero fino a d m», d ≤ portata − 0,40 m | regola di progetto | ricerca nelle stringhe d'uscita |
| I13 | Non parte se l'autoverifica fallisce; non in salute, il ciclo esce comunque | non provato | avvio coi filtri accesi; coperture di 1 e 2 s |
| I14 | Ogni evento dice se è osservato o dedotto; nessuno afferma una sosta o un'uscita | logica controllata dal suo autore | oracolo di `eventi.py` rifatto sul nucleo |

Cadono: la riga «0,33 m, meno della fascia» (**smentita**: 0,72 m con la latenza, VN §0) e «perso assorbente».

## 3. Contratto d'uscita comune e i due profili

**Comune, non cambia mai.** Di ogni cosa seguita il sistema dice se **la vede**, se **non la vede ma prevede dove può essere** (con il livello), o se **non lo sa** («previsto ampio: dietro l'ostacolo o fuori area»). Di ogni cella: libero, occupato, in ombra, non osservato; **«non osservato» non diventa mai «libero»**. La **possibile presenza** finisce solo guardando. **Affidabilità persa** è un segnale a parte. Identiche nei due profili anche quattro regole su nove del nucleo (3, 6, 7, 9); le altre cinque prendono un termine del profilo (AS C5).

**Parole.** «Osservato», «visto in parte», «previsto», «previsto ampio», «possibile presenza», «non ricomparso da n s», «identità ambigua», «suolo visto libero fino a d m», «attenzione», «zona non verificata», «affidabilità persa».

**Non si dice mai.** «Via libera»; «validato», «garantito», «certificato», «tarato»; «bassa latenza»; «perso»; «sosta», «si è fermato», «è uscito»; «prevede dove sarà»; «90 %» senza dominio, un livello 50 %, una cifra oltre 3 s, in moto o indossato; «± X,XX m», «confidenza Z %»; una quota calcolata e non letta; «mappa 3D», «voxel», «copre gli ostacoli bassi»; «360°»; «massa e accelerazione stimate»; «segue chi passa dietro un ostacolo» senza «che lo nasconde per intero»; «drone», «in volo», «in movimento», «ACAS», «minaccia», «preallarme laterale»; «orientamento» per chi cammina; «dispositivo medico»; «Intelligenza Artificiale» se l'etichetta è tagliata; «dal vivo» prima che giri; «identità mantenuta al 100 %»; «mai libero dove c'è un ostacolo» senza «a posa nota e se l'ostacolo risponde»; «15 Hz» ed «errore di 0,2 m a 1 s» come prestazioni misurate (15 Hz è il ciclo di progetto) (V7 §6, V8 §5 e §7, V9 §6, V10 §5).

| | A: monitoraggio di un varco o di un'area di lavoro | B: avviso di presenza per una persona non vedente **ferma** |
|---|---|---|
| Portatore | supporto fisso, o veicolo senza equipaggio **fermo** alla stessa quota | lo stesso treppiede, accanto alla persona |
| Uscita | schermo, registro; messaggio per settori verso un autopilota: **progetto, mai generato** | segnali sonori di 0,3 s; frase a stato stabile |
| Alla perdita di affidabilità | segnale a schermo; settori «zona non verificata»; ultimo quadro con l'età | segnale dedicato; la persona si ferma e torna al bastone |
| Provato oltre il nucleo | niente | niente (nessuna prova con persone) |
| Da dire | «al chiuso o all'ombra, fino a 3 m, camera a 1,2 m: a un'altra quota i numeri cambiano» (C8) | «per chi cammina non è provato niente» (C6); non è un dispositivo medico (se vi rientri: **non verificato**) |

Frase della prova (C1, aggiornata): «Al calcolatore, con una persona sola e un ostacolo fermo che la nasconde per intero, lo schermo ha mostrato a ogni fotogramma una zona dove poteva essere, e la persona era dentro in almeno 9 casi su 10 fino a 2 secondi, se restava sul proprio percorso. Dove cede lo diciamo prima.»

## 4. Che cosa è escluso, e perché

| Escluso | Perché (fonte) | Destino |
|---|---|---|
| Mappa a voxel, in ogni variante | a sensore fermo non dà niente più del fotogramma corrente; ogni variante che ricorda o deduce un «libero» cade (80 505 falsi «libero» su 146 901) (V7 §1) | dopo, in moto |
| Tre fasce di quota (S10) come sostituto; passaggio automatico | errore di lettura (1,09 m è una distanza); 32 celle «libere» sopra una scatola di 10 cm (V7, V9) | resta il principio |
| «Libero» ricordato per 3 fotogrammi; `stato(centro)` | 58 fotogrammi su 90; 32,9 celle su 33 «libere» sotto una barra (V7 §0) | sostituiti da 1.2 |
| Cerchio del filtro spento a «metà del cuneo»; «perso» assorbente | un vuoto in 1958 / 1991 / 1999 passaggi su circa 2000 (V8 §1) | sostituiti da 1.6 |
| Due ipotesi con pesi a ogni ciclo (S3 seconda, S4b); soglia 0,8 m (S4c) | sosta falsa nel 38–100 % dei transiti; fra 2 e 3 s la zona sparisce (V9, V8 §6.7) | dopo |
| «± X,XX m \| conf Z %»; livello 50 %; cifre oltre 3 s | «± σ» contiene il 39,3 %; nessuna candidata tiene il 50 % (V9 S5, V8) | — |
| Selettore completo (S1) | 200 cambi in 10 minuti; fa nascere «libero» sul 13,8–57,0 % della zona (V9) | resta il controllo all'avvio |
| «Probabilità d'intrusione» (S6); rotta convergente come modulo (S7) | scende quando il dato peggiora; S7 è S6 (V9) | etichetta, 4 ore |
| Livelli della preproposta com'erano (S8) | attesa in 900 fotogrammi su 900 a stanza vuota (V9) | riscritti in 1.10 |
| Sensori laterali come «preallarme» (S9); «360°» | 0,07 s di margine; coprono 180°; l'hardware manca (V9, VN §5.8) | dopo |
| «Taglio garantito» (S12) | 0 estrazioni su 4000 (V9) | piano a tappe |
| Compensazione della latenza sul segno pieno o in ombra (S2 com'era) | dopo una sosta l'errore va da 0,04 a 0,18 m (V8 K-210) | sola uscita, 4 ore |
| c10; `statistico-7`; particelle; due soggetti per ombra; sensore in moto; battito sonoro | non provati o fuori tempo (V8 §5) | dopo |
| V-016, V-017, V-019, T-008 | un autore ciascuna (V7 §1) | 4 ore, se confermate |
| Pannello da 0,5 m; seconda persona dietro il pannello | contenimento 14,2–16,5 %; scambio 2400 su 2400 (N, VN) | fuori dalla demo |
| Massa e accelerazione | non osservabili (VN §5.7) | mai |

**Correzioni proposte da f10 e non adottate, perché non provate** (V10 §3): soglia di pixel proporzionale ai pixel attesi per cella (F-401, F-412); l'avviso che resta al riaggancio finché le celle non sono viste libere (F-409); il filtro che riparte da una misura tagliata (F-408); q = 0,1 (F-411). Entrano solo dopo la prova senza sensore di V10 §6 o la prova C-C.

## 5. Contraddizioni aperte su regole adottate

`sd-K#` sono identificativi provvisori. Quando: **S** simulazione subito; **H** primo sensore; **D** dopo.

| K | I due enunciati | Regola adottata, e da chi | Prova che decide |
|---|---|---|---|
| `sd-K1` | V9: previsione «in tre gradi» ↔ V8: «previsto / previsto ampio», un livello | **V8** (V9 dà un parere e rimanda a f8). Il terzo grado è l'evento «non ricomparso da n s» | S: banco di f8 col registro: quante volte l'evento esce col segno ancora «previsto» |
| `sd-K2` | V9: «nessun ostacolo osservato fino a d metri» ↔ V7: «suolo visto libero fino a d» | **V7**: afferma solo il suolo ([prel.] sotto un ostacolo sospeso a 2,06 m il suolo è «libero» nel 97,5 %) | D: lettura con tre persone |
| `sd-K3` | c2: le pendenti ambigue «le azzera l'operatore» ↔ priorità 2; decisione 3 di V9 | **l'operatore ferma la ripetizione; le celle d'avviso le toglie solo lo sguardo** | decisione dell'utente |
| `sd-K4` (tocca K-403, K-017) | V7: «occupato» con 3 pixel ↔ V10 [prel.]: con 3 l'identità tiene in 0 passaggi su 90; con 40 (a 424×240) in 41 su 45, ma si perde la scatola di 15 cm | **3 pixel** (prima la sicurezza) | S: prova di V10 §6 a 424 e 848 pixel (≥ 28 su 30 e scatola ≥ 9 su 10); H: prova d'ingresso |
| `sd-K5` = K-109 | M2: con affidabilità persa la regione «si congela» ↔ V7 (c): si dilata | **V7** (congelata: fuori regione in 60 fotogrammi su 60) | S: coperture di 1 e 2 s sul nucleo intero |
| `sd-K6` | M2: chiusura «fuori dall'area osservata» ↔ V8 §4.9: non toglie l'avviso | **V8 §4.9** | S: mai eseguita |
| K-107 | «libero»: V-018 (impronta) ↔ V-017 (quota letta) | **V-018**; V-017 nelle 4 ore | S: C-D (0 celle libere con un ostacolo sotto; mediana ≥ 2,7 m) |
| K-106 | buchi radi o a chiazze (a chiazze al 30 %: 1,5 m, 4,55 cambi al secondo) | senza memoria comunque | H: stanza ferma per 60 s |
| K-202 | «ampio» a metà ↔ all'80 % (scelto dopo i dati) | **80 %, 3 s** (V8, c8) | S: semi nuovi; H: 2 righe da 50 occlusioni virtuali |
| K-215 | precisione ↔ ombra stretta di 10–20 cm con corpo esteso (0,46 / 0,37) | cifra dichiarata **«con la maschera esatta»** | S: C-C a −10 cm; H: errore al bordo ([prel.] da +2 a +15 cm, verso il largo) |
| K-218, K-219 | identità «100 %» ↔ 0,37–0,99 con N-C6; c1 ↔ l'estraneo | N-C6 resta; c1 **solo dopo** la prova contro l'estraneo | S: C-C; H: distanza della prima misura dall'ombra |
| K-220 | M1 subito ↔ c4 dopo 2 cicli | **M1 + c4 + c7** (V8 §4) | S: C-C |
| K-110 | N-C6 ↔ continuità dietro un ostacolo più basso di 1,65 m | **N-C6**; la demo lo evita e lo dichiara | D: V-019 con un secondo autore |
| K-111 | pannello di 1 m ↔ occlusione lunga | 1 m a passo lento più il pannello virtuale | decisione dell'utente |
| K-221 | 30 camminate ↔ 200 percorsi | **almeno 200** (c9) | H: `statistico-6` |
| K-306…K-308 | ordine e soglie dei livelli | ordine del nucleo; nessuna «richiesta» | S, H, D (prove di V9 §3) |
| K-015, K-007, K-014 | velocità coperta; «mobile»; «libero» nell'ombra vera | 1,4 m/s; spostamento; I1 e I2 | H: latenza, rumore, pannello sul nastro |
| K-016, K-214, K-108 | secondo soggetto; oltre 3 s; ore | limiti dichiarati; piano di un altro ruolo | D |

Decise dall'adozione, con il residuo detto: «libero» ricordato per 3 fotogrammi (nucleo) ↔ senza memoria (V7): vale V7, resta K-106; nomi dei livelli di V9 ↔ segni di V8: sono due assi (per settore e per traccia, in 1.10), restano `sd-K2` e K-306…K-308; croce in «ampio» (M5) ↔ niente croce (c8): vale c8; pannello alto 1,5 m (VN) ↔ 1,7 m (V7) ↔ 1,8 m proposto da V10: almeno 1,7 m, 1,8 m se c'è (più alto non toglie niente); fascia 0,40 m (V9 S4a) ↔ 0,20 m (M): due fasce, la seconda dentro la prima; K-302, K-303, K-304: la seconda ipotesi non entra, livello 90 %.

## 6. Codice dello sciame riusabile

Tutto è **scritto da un agente, non riletto da una persona**. Percorsi sotto `.sciame/20261114-1301-percezione-challenge/`, presenti su disco (`ls` delle 17:50).

| Che cosa | Percorso | Avvertenze |
|---|---|---|
| Catena di riferimento, Python con numpy (blocchi 1.1–1.8) | `f10-dati/10-catena/` (`catena.py`, `mappa.py`, `gruppi.py`, `kalman.py`, `inseguimento.py`, `presenza.py`, `parametri.py`, `prove.py`) | [prel.] 25 prove su 25 su scene a mano dello stesso autore; V10: punto di partenza, con i difetti F-401…F-413. **Da correggere:** ha la memoria del «libero», «perso», il riaggancio del nucleo, soglie di pixel assolute; l'invariante 3 controlla «ha una misura», non «in porta»; dopo un riaggancio con misura tagliata il filtro non si muove (fino a 5,00 m). Mancano 1.9–1.12 |
| Interprete | `f10-dati/ambiente/venv/bin/python` (`03-infrastruttura/AMBIENTE.md`) | [prel.] |
| Simulatore del sensore, scene, sequenze | `f10-dati/11-simulatore/` (`simsens.py`, `catalogo.py`, `sequenze/`) | [prel.] la verità regge a un controllo a mano; ha meno buchi del vero (21–39 punti) |
| Formato, controllo, registrazione | `f10-dati/CONTRATTO_DATI.md`, `03-infrastruttura/controlla_sequenza.py`, `04-embedded/registra_sequenza.py` | [prel.] nessun dispositivo mai collegato |
| Innesto del predittore | `f10-dati/20-validazione/comune.py` (`PredittoreCheRegistra`) | [prel.] oggi a velocità costante |
| sd-0, sd-1, pavimento, punto, in C | `f8-continuita/13-soluzione/comp.c` | soggetto puntiforme; da riscrivere in Python (5,3 ms per ciclo, V8) |
| Banco, generatore, torneo, controprove | `f8-continuita/11-misure/banco.c`, `gen.h`; `12-torneo/torneo.c`; `14-attacco/att.c` | prima di un nuovo lancio usare `15-statistica/codice_semi/gen.h` (`statistico-7`) |
| «Impronta del suolo»; quota letta; taglio dal basso | `f7-estensione/15-verifica/vq3c.c`; `14-attacco/av10.py`, `av4.py` | un autore ciascuna |
| Registro degli eventi | `f7-estensione/04-requisiti/eventi.py` | lavora su un nucleo ridotto; rinominare l'evento della sosta |

## 7. Dominio dichiarato e limiti

**La forma più forte che resta vera.** *In simulazione, a sensore fermo, con una camera di profondità a 1,2 m da terra inclinata di 15°, al chiuso, fino a 3 m, con una persona sola vista per almeno 4 fotogrammi che passa dietro un ostacolo fermo che la nasconde per intero, entrando fra 0,3 e 1,8 m/s e restando sul proprio percorso (prosegue, rallenta, si ferma, torna), con la maschera d'ombra esatta, il soggetto puntiforme, il rumore misurato e una libreria di percorsi dello stesso tipo di camminatore:*
1. a ogni fotogramma lo schermo mostra una zona tratteggiata dove la persona può essere, distinta da «osservato»: 0 passaggi con un'interruzione su circa 8300 (24 800 a semi riparati);
2. la persona è dentro la zona in almeno 9 casi su 10 fino a 2 s e in almeno 85 su 100 fino a 3 s (limite inferiore di Wilson; tre disposizioni, una mai usata per la taratura); poi il sistema dice «previsto ampio»;
3. la zona non sta su suolo visto libero in quell'istante oltre 20 cm di margine, e sta sempre dentro l'avviso;
4. la persona nascosta è dentro l'area d'avviso nel 100 % degli istanti simulati (oltre 170 000), anche quando la zona stretta sbaglia; nessun timer toglie l'avviso;
5. ciò che non è letto in quell'istante non è dato per libero: regola per costruzione, sostenuta in simulazione, mai esercitata su immagini vere.

**Dove cede, detto prima** (controesempi in simulazione, V8 §2.1; quota dentro la zona a 1 / 2 / 3 s):

| Che cosa cambia | Effetto |
|---|---|
| chi svolta; chi esce dal lato lontano | 0,86–0,94 / 0,54–0,70 / 0,38–0,52; 0,77–0,92 / 0,32–0,67 / 0,13–0,47: lo copre solo l'avviso |
| ombra stimata stretta di 10–20 cm, corpo esteso, rilevamento 0,7 | 0,46 / 0,37 e 0,37 / 0,28 a 1 / 2 s |
| chi parte da fermo accanto all'ostacolo | 0,11 / 0,16 / 0,26 (0,65 a 1 s con c5) |
| camminatori meno regolari; libreria di 30 calmi su vivaci | 0,944 / 0,835 / 0,801; 0,73 a 2 s |
| rumore non rimisurato; oltre 3 s | 0,44; nessuna cifra (a 5 s 0,787 in demo) |
| la persona è persa prima dell'ostacolo | 9 passaggi su 2800; 130 su 1581 con rilevamenti scarsi e corpo esteso |
| una seconda persona, mai vista, esce dalla stessa ombra | scambiata sempre (193 su 193); l'avviso si spegne |
| pannello della demo, largo 1 m | la zona localizza per circa 1 s, poi dice «è ancora dietro» |

**Limiti.** Non vede il vetro (654 punti della lastra su 800 dati per liberi) né ciò che non rimanda segnale [prel.]. Non vede: il suolo a meno di 1,24 m; un ostacolo di 15 cm a meno di 1,09 m **di distanza dal sensore**; un oggetto alla quota della testa a meno di 2,41 m; ciò che è più basso di 0,4–0,7 m e più vicino di 0,8–0,5 m. Dietro un ostacolo più basso di circa 1,65 m perde chi è ancora in vista. Occlusore mobile, due soggetti per ombra, sensore in moto, ausilio indossato, sole, pavimento lucido, classi diverse da «persona»: **non provati**, o con controesempio (in moto, con 1° e 2° di tremolio d'imbardata, 0,76 e 0,56 a 2 s). La fascia è onesta fino a 1,4 m/s: di corsa no. La latenza non è misurata. Costo della previsione: circa 1 ms per ciclo in C e 6 ms in Python con dieci tracce, su un portatile; [prel.] catena intera 1–6 ms su scene pulite, 81 ms di media su una scena vera con 254 tracce.

**[prel.] Che cosa aggiunge f10, col verdetto V10.** Su profondità simulata dalle schede, con i parametri del nucleo, l'identità al ritorno **non tiene** (0 passaggi su 90: fusione col pannello, fantasmi sul pavimento; smentita) e il pannello fermo è «mobile» in 79 passaggi su 90 (smentita); «libero» nell'ombra vera: 0 su 2,9 milioni di controlli, a posa nota e con ostacoli che rimandano segnale, su tre forme d'ombra. Altri limiti da V10: un ostacolo sospeso vicino non è visto e sotto è «libero» (F-410); il simulatore ha meno buchi del vero, quindi le cifre al nominale sono ottimistiche (K-407). Sui dati veri: solo il modello del moto. **Gruppi, soglia di pixel e riaggancio (1.2, 1.3, 1.8) sono i primi punti da provare**; col sensore, le tre misure di V10 §6: pavimento vuoto e posa; pannello sul suolo segnato col nastro; 30 passaggi con un metro a terra e la mano sul sensore.

**Geometria della demo** (cond. 3, V7 §2, C3, (f), V10): pannello alto almeno 1,7 m (1,8 m se c'è), largo 1 m, a 1,7–1,9 m dal sensore; attore sulla linea a non più di 2,3 m, a passo lento; **una sola persona dietro il pannello**; casse fuori dalla linea dell'attore; al chiuso. Da dire per primi: «provato al calcolatore, su profondità simulata dalle schede tecniche e su tracce pubbliche di persone, a sensore fermo, con una persona sola; mai su un sensore nostro».
