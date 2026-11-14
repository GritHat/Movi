# Previsioni di `sciame-avversario`, estensione f7, fase f4 (controprove sulla decisione)

Scritte alle **2026-11-14T17:10:28+01:00** (`date -Is`), PRIMA di ogni mio conto o script.
**Non sono cieche sul torneo:** a quest'ora ho letto il contratto dell'estensione, gli addendum, la traccia, `DECISIONE.md` con `PREVISIONI.md` e `conti.txt`, `TORNEO.md`, l'attacco alla specializzazione, il contratto di f8, le righe di `SOLUZIONE_V2.md` sui blocchi B1–B9 e sugli invarianti, e le funzioni `cast`, `render`, `q1m`, `q3`, `Nupdate` di `11-torneo/torneo.c` (per sapere che cosa NON condividere). Non ho ancora letto `TRIAGE.md`, `BENCHMARK_INDIPENDENTE.md` né le consegne 01–08 per intero (solo righe trovate con `grep` in 04).
**Codice:** tutto mio, in Python puro (`sim.py` e uno script per attacco), nessuna riga presa da `torneo.c`. Condivido con la decisione: il modello a foro (camera a 1,2 m, 15° in giù, 87° × 58°, 320 × 240), la legge del rumore k·z², il margine m(z) = 0,03 + 3·σ(z), la griglia 1° × 0,1 m fino a 3 m, lo pseudocodice del §1.3 letto da me. Niente vale per un sensore vero.

## AV1 — `stato(centro)` come fonte del «libero» delle celle (è la PD1 della decisione, più due variabili che la decisione non fissa)

La decisione scrive «cella libera <=> stato(centro)» senza dire a che quota sta il centro, e prova Q3c con il rumore 0,004·z².
Stanza vuota 6 × 4 × 3 m, 10 fotogrammi, celle con centro fra 1,3 e 3,0 m di distanza al suolo, dentro il campo. Resa = quota di queste celle (tutte davvero libere) date per «libero».
- quota del centro 0,00 m: resa **≤ 1 %** con qualunque rumore (un punto del suolo sta su una superficie: `leggi` dà OCCUPATO). *Smentita:* > 10 %.
- quota 0,10 m, k = 0,004: resa **≥ 80 %**. *Smentita:* < 60 % (cadrebbe anche l'utilità della PD1).
- quota 0,10 m, k = 0,0095 (stima mia per una stereo con 0,08 pixel di errore di disparità, base 50 mm, focale di 320 pixel su 87°: 169 pixel; da verificare sulla fonte): resa **≤ 30 %**, e nessuna cella libera oltre 1,8 m. *Smentita:* > 60 %.
- quota 0,30 m, k = 0,0095: resa **≥ 80 %**; ma una scatola alta 0,25 m (0,4 × 0,3 m a 2 m) ha **almeno 3 celle** col centro nella sua pianta date per LIBERO da `stato` (decide allora solo la riga «griglia <- pixel»). *Smentita:* 0 celle.
- corpo che non rimanda segnale (0,45 × 0,25 × 1,75 m a 2 m, pixel non validi), quota 0,10 m, k = 0,004: **0 celle** col centro nella pianta del corpo date per libere, in 10 fotogrammi (qui prevedo che la decisione REGGE). *Smentita:* una cella.

## AV2 — barra nella colonna: la regola letterale e la frase «quota verificata fino a 1,2 + 0,25·d»

Barra fra 1,40 e 1,50 m di quota, larga 1,2 m, profonda 0,10 m, a 2,0–2,1 m (il tetto del campo lì è 1,70 m: la barra è in vista).
- Lettura letterale «cella libera <=> stato(centro)» (centro a 0,10 m): **almeno 20 celle** con la barra nella colonna date per «libero», mentre la barra ha almeno 500 pixel validi. *Smentita:* 0 celle.
- Lettura «occupato dai pixel vince» (≥ 3 pixel con quota 0,07–2,0 m nella colonna): **0–3 celle** libere con la barra nella colonna.
- Con questa seconda lettura e «ombra oltre il primo ritorno»: **almeno 100 celle** di suolo davvero visto oltre la barra escono «in ombra» (perdita di libero, non di sicurezza).

## AV3 — senza fondale (un hangar: nessuna parete entro la portata valida)

Solo il suolo, portata valida 6 m (poi 10 m). Nella colonna sopra una cella a d = 2 m e a d = 3 m, la quota più alta a cui `stato(p)` dà LIBERO:
- portata 6 m: **≤ 0,9 m a 2 m** e **≤ 0,7 m a 3 m** (la frase d'uscita dichiara 1,70 e 1,95 m). Con 10 m: ≤ 1,05 e ≤ 0,95 m. *Smentita:* un LIBERO sopra 1,2 m a d = 2 m senza fondale.
- quota di pixel non validi nella scena vuota senza fondale: **30–50 %** (la decisione cita 32–44 % da altri ruoli).

## AV4 — la cassa da 1 m con la persona dietro (e la cassa dell'atto 2 della demo)

Cassa 0,8 × 0,3 × 1,0 m a 1,7–2,0 m; persona 0,45 × 0,25 × 1,75 m a 2,3 m, centrata dietro. 10 fotogrammi.
- La persona ha **≥ 1 500 pixel validi**; con la regola com'è scritta (primo ritorno = occupato, oltre = ombra, gruppo tagliato dall'ombra escluso) entra nel filtro in **0 fotogrammi su 10**. *Smentita:* ≥ 1 fotogramma.
- **Proposta `avversario-2`, «taglio dal basso».** Un gruppo oltre il primo ritorno si accetta se, alle righe d'immagine che occupa, i pixel subito a sinistra e subito a destra del gruppo sono validi e più lontani del gruppo (sfondo), non più vicini (occlusore) né non validi. Previsione: (a) persona dietro la cassa: accettata in **≥ 9 fotogrammi su 10**, errore del centro in pianta **≤ 0,10 m**; (b) persona tagliata di lato da un pannello alto 2 m (ne sporgono 0,15 m): **0 accettazioni su 10**; (c) persona dietro il pannello alto, del tutto nascosta: 0 gruppi. *Smentita della proposta:* (b) accettata anche una volta, oppure (a) sotto 9.

## AV5 — sensore coperto: «esci», «localizzata = no», identità (a ragionamento, più un conto in pianta)

- Alla lettera, nello pseudocodice un ciclo non in salute termina prima di «uscita» e prima della previsione: per una copertura di 2 s sono **30 cicli senza stima emessa** (criterio 1 del contratto di f8). *Smentita:* una riga del §1.3 che emette la previsione o l'uscita in quel ramo.
- Simulazione in pianta (mia): soggetto nascosto dietro l'occlusore A, sensore coperto 2 s, il soggetto passa a 1,2 m/s dietro l'occlusore B. Con la regola scritta («restano, localizzata = no») il soggetto è **fuori dalla regione in 60 fotogrammi su 60** dopo la copertura (è lo stesso numero del torneo: la bandierina non cambia le celle). Con la riga riscritta (regione := regione dilatata di v_max × durata della copertura + fascia, intersecata col non osservato): **0 su 60**. *Smentita della riscrittura:* ≥ 1.
- Nessuna riga della decisione rende «identità ambigua» il riaggancio dopo una copertura. *Smentita:* la riga c'è.

## AV6 — errore di posa: «`stato(p)` non chiede la posa» (§1.8) contro la prova 6

Trave a terra 0,12 m alta, 0,10 m profonda, larga 1 m, a 2,8 m; camera vera a 14° (o 16°), creduta a 15°.
- Con almeno uno dei due segni, **≥ 5 celle** col centro nella pianta della trave sono LIBERO per `stato(centro a 0,10 m)` e non occupate dai pixel (quota ricostruita sotto 0,07 m); con errore 0: **0**. *Smentita:* 0 celle con entrambi i segni.
- **Proposta `avversario-3`, controllo del piano nell'immagine (senza IMU):** la mediana della quota ricostruita dei pixel del suolo fra 2 e 3 m si scosta di **≥ 3 cm** con 1° d'errore e di **≤ 0,5 cm** con 0°: un controllo di salute da un'ora. *Smentita:* scarto < 1,5 cm a 1°.

## AV7 — ore: la somma sta, il calendario no (conto)

Dati dei file: blocchi del nucleo 3+6+6+5+9+4+3+6+12 = 54; catena B1→…→B8 = 38; sensore disponibile fra 5–6 ore (settimo addendum); accettazione sull'hardware «due persone, circa 2 h 40»; aggiunte f7 8–10,5.
- Messo il sensore all'ora 6 e l'accettazione in coda, alle 5 persone restano per **f8 più integrazione, prima dell'accettazione, ≤ 4 ore-persona** (la decisione ne dichiara 9,5–12). *Smentita:* ≥ 9,5.
- La catena B2→B8 (35 ore) deve stare in ≤ 11,4 ore d'orologio: servono **≥ 3 rami del tutto indipendenti**; nessun file prova che i quattro formati bastino.

## AV8 — il pannello (PD4 della decisione) e la frase «con un ostacolo più alto del sensore»

- PD4: pannello alto 1,5 m a 1,7 m, soggetto 1,75 m a 2,3 m: **≥ 100 pixel validi** della testa; pannello 1,70 m: **0**. (Prevedo che REGGE.)
- Pannello alto 1,30 m («più alto del sensore», che sta a 1,2 m): **≥ 800 pixel validi** del soggetto, che per la regola scritta non entra nel filtro: la frase dell'ambito (§2.1) è falsa fra 1,2 m e circa 1,65 m d'altezza dell'ostacolo. *Smentita:* 0 pixel con 1,30 m.

## AV9 — Q2: lettura frase per frase, registro e «oggetti», correzioni C1–C8 (lettura, `grep`)

- Nel testo dell'ambito (§2.1) mancano: «una persona sola» (C1), «al chiuso, fino a 3 m, camera a 1,2 m» (C8). Nello pseudocodice manca la riga di C2 (traccia che sparisce nell'anello cieco). Il tetto di C4 su d («non oltre la portata meno v_max × (età + latenza)») non c'è. *Smentita:* le parole ci sono.
- L'elenco delle righe del registro (§2.3) non ha nessun evento su un oggetto fermo: nell'atto 4 «un giurato posa una cassa in vista» il registro non scrive niente sulla cassa. *Smentita:* un evento «oggetto» nell'elenco.
- Tre verbi all'indicativo nell'ambito («monitora», «dà un avviso») affermano più di «è progettato per».

## Dove NON prevedo di trovare la rottura (lo dico prima)

Prove 1, 2, 3 del contratto (voxel non allocato, decadimento, rimozione dei blocchi) sull'architettura adottata: non c'è mappa né timer sul «libero»; le cerco nella sola forma che resta (memoria di 2 fotogrammi, epoca, regione per celle).

## AV10 — aggiunta alle 2026-11-14T17:20:23+01:00, dopo AV1–AV8 e prima del lancio che la decide

Visti AV2 e AV3 (la regola letterale libera 32,9 celle su 33 sotto una barra; senza fondale la quota letta libera è 0,55–0,95 m contro 1,70–1,95 dichiarati), provo la riga riscritta, **proposta `avversario-4`, «quota verificata per cella»**: cella libera ⇔ meno di 3 pixel-ostacolo (quota 0,07–2,0 m) nella cella ∧ non oltre il primo ritorno ∧ `stato(p)`==LIBERO a quota 0,20 m; quota verificata q_v = la più alta fra {0,2; 0,6; 1,0; 1,4; 1,8} m tale che `stato` è LIBERO a tutte le quote campionate fino a lei (5 letture per cella).
- Scene: barra di AV2, barra sottile 1,15–1,25 m (fra due campioni), scatola da 0,25 m e da 0,10 m, senza fondale; k = 0,004 e 0,0100; 10 valutazioni. **0 celle** libere con un ostacolo nella colonna sotto la loro q_v. *Smentita:* ≥ 1 cella-fotogramma.
- Resa del «libero» nella stanza vuota con k = 0,0100: **≥ 90 %**. *Smentita:* < 80 %.
- Senza fondale: q_v mediana a 2 m **≤ 0,6 m**, a 3 m **≤ 0,6 m** (dichiarate, non 1,70–1,95).

---

# Esiti (scritti alle 17:22 del 14 novembre 2026, dopo i lanci; i file `risultati_*.txt` sono accanto)

- **AV1.** Quota 0,00: resa 0,0 % di 1 391 celle (**regge**). Quota 0,10 e k = 0,004: 99,4 % (**regge**). Quota 0,10 e k = 0,0095: 15,2 % (**regge** sul ≤ 30 %); «nessuna cella libera oltre 1,8 m»: **smentita** (9,8 % fra 1,8 e 2,4 m; 1,0 % oltre). Quota 0,30: 100 %, e sopra la scatola da 0,25 m 11,0–15,3 celle su 33 date per libere da `stato` (**regge**); le ferma solo la riga dei pixel. Corpo che non rimanda segnale: 0 celle su 37 e 0 su 75, anche quando compare (**regge: qui la decisione tiene**); braccio senza clausola 37 e 75.
- **AV2.** Lettura letterale: 32,9 celle su 33 libere sotto la barra, vista da 1 404 pixel (**regge**). «Occupato vince»: 0,0 (**regge**). In ombra con suolo visto: 326,4 celle a fotogramma (**regge**).
- **AV3.** Portata 6 m: 0,75 m a 2 m e 0,55 m a 3 m; portata 10 m: 0,95 e 0,80 m; pixel non validi 44,6 % e 37,1 % (**reggono tutte**).
- **AV4.** Persona con 2 862 pixel validi, primo ritorno in 0 fotogrammi su 10 (**regge**). `avversario-2`: (a) 10 su 10, errore ≤ 0,007 m; (b) 0 su 10; (c) 0 (**reggono**).
- **AV5.** Nessuna riga emette l'uscita nel ramo «non salute» (**regge**, per lettura). Regola scritta: fuori regione 60 su 60 con T = 1 e 2 s; riscritta: 0 su 60, ma la regione è il 100 % del non osservato (**regge**). Nessuna riga sull'identità dopo una copertura (**regge**: «identità ambigua» compare una volta, nell'elenco del registro).
- **AV6.** Trave da 0,12 m con ±1°: 0 celle (**SMENTITA la mia previsione**: 3 × 3 e margine la tengono). Scarto del piano: ±3,5 cm a 1°, 0,0 a 0° (**regge**).
- **AV7.** Restano 1,5–4,0 ore-persona con 5 persone (**regge**); 3,1 rami indipendenti.
- **AV8.** 576 pixel con il pannello da 1,5 m, 0 con 1,65 e 1,70 m (**PD4 regge**); 1 604 pixel con 1,30 m (**regge**).
- **AV9.** «una persona sola», «fino a 3 m», «vuoto vicino», «portata meno», «oggetto fermo»: 0 occorrenze nella decisione; «al chiuso»: 1, nella demo e non nell'ambito (**regge**).
- **AV10.** 0 celle false in 16 combinazioni; resa 98,5 % con k = 0,0100; q_v mediana senza fondale 0,6 m a 2 e a 3 m (**reggono**). La previsione è stata scritta nello stesso comando che ha lanciato lo script (stessa ora al secondo): precede il lancio, ma di un istante.

## Notato dopo, senza previsione

1. AV1 con le tre curve di rumore del blocco B1 del nucleo (k = 0,00375 / 0,0100 / 0,0125): a quota 0,10 m resa 99,8 / 10,1 / 0,9 %; a 0,20 m 100 / 98,5 / 89,3 %.
2. AV1b: con k = 0,0095 e centro a 0,30 m, 2 celle-fotogramma su 330 sopra la scatola da 0,10 m sono libere per `stato` E non occupate dai pixel.
3. AV4: (a2) cassa da 0,5 m: 10 su 10, ma con k = 0,0095 la persona si fonde con la cassa (errore 0,18–0,27 m); (d) persona spostata: respinta (righe buone 51 %); (e) cassa più pannello di lato: respinta; (f) persona scura: nessun gruppo.
4. AV6: trave da 0,10 m con −1°: 21 celle su 21 libere per `stato`, 20,9 anche non occupate dai pixel; da 0,12 m con −2°: 21 e 21; da 0,15 m con −2°: 21 e 20,6. Col segno opposto: 0.
5. AV5: la riga «regione <- regione \ {celle col suolo libero ora da 3 fotogrammi}» non dice «oltre la fascia», come dice invece il nucleo: la fascia di 0,40 m (637 celle alla nascita) si consuma in 3 fotogrammi e resta il cuneo (288 celle).

## Registro dei difetti del mio banco

- AV4, giro 1 (`av4_giro1.py`, `risultati_av4_giro1.txt`): valutavo il gruppo più grande, che era la faccia della cassa (sta a cavallo di due celle: metà dei suoi pixel cade oltre il primo ritorno), non la persona. Corretto nel giro 2: componenti su tutte le celle-ostacolo, il soggetto è la componente entro 0,3 m dal vero. Le previsioni non sono state toccate.
- Fonte in rete per il rumore (guida del costruttore): non raggiunta (`getaddrinfo EAI_AGAIN`). Il valore k = 0,0095 resta una stima mia non verificata; uso come appoggio le curve scritte nel blocco B1 del nucleo.
- A fine lavoro ho lanciato `git status --short` (sola lettura) per controllare di non aver toccato file tracciati: la consegna dice «niente git». Nessun file fuori da questa cartella è stato scritto; il PDF di prova per contare le pagine (A4, corpo 10, margini 1,8 cm: 3 pagine) sta nello spazio temporaneo della sessione, non nel progetto.
