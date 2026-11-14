# Verifica della decisione f7 (`sciame-validazione`, fase f3–f4)

14 novembre 2026, 17:03–17:20. Accanto: `PREVISIONI.md` (parti A–E, ciascuna con l'ora prima della prova che la decide), `vq3c.c`, `risultati_vq3c.txt`, `stato.md`. **Tutto è simulazione su camera ideale a sensore fermo, o riconteggio di file: nessun fotogramma vero.** Sigle come in `13-soluzione/DECISIONE.md` (D): T torneo, B banco; Q3c = `stato(p)`; N1 = griglia del nucleo.

## 0. In testa

**Cambi di stato proposti.** (1) «NO alla mappa voxel nelle 14 + 4 ore»: **regge**; la misura da cui dipende (Q3c sui punti, 0 falsi «libero» profondi) è rifatta con codice mio: **sostenuto dai dati, due autori**. (2) «Cella libera ⟺ `stato(centro)`» (D §1.3, PD1): **sostenuta dai dati come sicurezza (0 profondi), smentita come uscita** (misura mia, un autore): con il 5 % di buchi sparsi la distanza libera per settore cade da 3,0 a 1,4 m (§3). (3) Invariante 1 del nucleo: **smentito anche col mio codice** (58 fotogrammi su 90). (4) «438 → 0 punti falsi» (D §1.2, §1.5): **smentita sul file**: 438 → 14. (5) «Con 5 persone entra» (D §1.9): **non risolto**: è una somma di ore-persona; la fila di 38 ore non è spezzata da nessuna prova.

**Scostamenti e regole violate.** Previsioni non cieche (dichiarato in testa a ogni parte). `vq3c.c` modificato tre volte dopo aver visto un esito, ogni volta con la previsione scritta prima; i lanci precedenti sono conservati e le righe comuni sono identiche. Aperta una riga di `torneo.c` (stampa di S10), come annunciato. Due script di ricerca scritti nella cartella temporanea della sessione, fuori dalla cartella di consegna. Non lette le cartelle di f8 e f9. Le ore sono stime, **non verificate**.

## 1. Rilettura

**Cifre.** Ricontate 94 cifre di D sui file: **91 tornano** (fra le altre: 0 su 147, 97,1 %, 83,0 %, 0,48 e 6,24 ms in `risultati_scenB.txt`; 1 186 e 495 in `_a5c`; 44 su 87; 87,7 % in `_k106`; 14 448 su 22 240 in `_a3`; 537 in `_k105`; 1 444 su 1 460 in `_scenA`; 60, 146, 94/90/170 in `_pp`; 654 su 800 in `_a8`; 67 celle e 3 170 pixel in `_s10`; 200 e 153 su 200 in `_s11`; 1,39–1,76 e 1,54 MB in B; 138 230 in `01`, 5 553 in `06`, 22 % in `03`; 14 400 e 155 ms nel verdetto del nucleo). **Non tornano:** «438 → 0»: `risultati_a5.txt` dà N1 = 14 al fotogramma 60, con 13 di base; «tre fotogrammi, 2,46 MB»: in `12-prestazioni/banco.c` riga 325 sono due fotogrammi da 4 byte (tre: 3,69 MB). **A metà:** «da 11,9 cambi a 0»: 0,00 per direzione, 0,65 per settore (`SOLUZIONE_V2.md`, C9).

**Dove D afferma più dei file.**
1. *Prova 9, «regge: 0 libero subito».* Vale per Q3c sui punti; la griglia N1 nel file dà ancora 744 e 727 punti liberi nei due fotogrammi dopo la copertura (`risultati_a9.txt`).
2. *Prova 10.* D cita 0,29 ms, che è di Q1; Q3c ha massimo/mediana 2,09–2,13 in tre ripetizioni su tre (`risultati_a10.txt`), oltre la soglia 1,35 del torneo: sul rapporto è **smentita**, non «non risolta» (in assoluto 1,2 ms).
3. *Prova 3, «regge per costruzione».* Nessun file sulla struttura adottata; *prova 2:* Q3c non compare in `risultati_a2.txt` (segue da Q3 per inclusione); *prova 5:* I3 «non riprovata» (lo dice D; l'ho fatto io, §3).
4. *«Nessun beneficio del criterio è risultato suo».* Vero nella forma del contratto («rispetto al nucleo»). Sull'elenco di `promptMare.txt` §14 due voci sono **sostenute dai dati alla lettera**: meno memoria della densa (hash al 33–84 %, B §4.1) e prestazioni compatibili (p95 ≤ 12,8 ms con un raggio su 16, B §4.3). Non cambiano il verdetto (il risparmio è al più 1,54 MB e il nucleo usa 10 788 byte), ma D deve scriverlo.
5. *«97,1 % contro 83,0 %».* Stesso autore, stesso reticolo. Col mio reticolo Q3c rende 88,4–91,8 % (§3): il confronto vale dentro il torneo.
6. *Ore.* «Con 5 persone entra»: 70 − 58…60,5 lascia 9,5–12 ore-persona per integrazione, previsione (f8) e prove sull'hardware, e presuppone 38 ore in fila ridotte a 14 di orologio: non provato (D parte 3, punto 5, lo ammette; §1.9 no).
7. *S11.* D sostituisce `SOSTA_IN_OMBRA`; di «attraversamento» e «avvicinamento diretto» non dà un esito.

**Etichette.** «Provato» non è uno dei cinque stati: dove c'è un file va letto «sostenuto dai dati (simulazione, un autore)». Senza file che lo regga: riga «Griglia» (438 → 0, sopra); riga «Affidabilità persa» («scatta anche col rado»: T scrive «per definizione», la misura è solo del difetto).

## 2. Il criterio del contratto

| Punto | Esito | Prova |
|---|---|---|
| 1. Beneficio | Nessuno dei sette è proprio della mappa rispetto al nucleo; 1–3 li dà la lettura del fotogramma; 4 peggiora nel ciclo (fantasmi in 144 fotogrammi su 150, `_a4`); 5–6 vedi §1.4; 7 **non attaccato** | T §1–2; mia §3 |
| 2. Dieci prove | Tutte con un file per le candidate; sulla struttura adottata **intera** cinque sono parziali (2, 3, 5, 9, 10) e due smentite e dichiarate (6 posa, 8 vetro) | `11-torneo/risultati_*.txt` |
| 3. Costo | Misurato con media, p95, p99, massimo, a 10 e 5 cm, col comando | B §2. Non misurati: catena intera, linguaggio del prototipo |
| 4. Per prove | Sì: `07-rovesciatore` e il torneo. Scrutinio asimmetrico: Q3c aveva un autore e nessun attaccante | ridotto dal §3 |

## 3. La misura rifatta

**Quale.** Q3c: da lì dipendono il NO, l'invariante I3 e il «libero» delle celle. **Indipendenza:** condivido lo pseudocodice di D §1.3, la camera ideale e il modello che scrive; non il codice, le scene, il reticolo (208 000 punti a 5 cm), la verità. Copre i difetti del codice e delle scene del torneo, non quelli della specifica o del sensore vero. `gcc -O2 -o vq3c vq3c.c -lm && timeout 120 ./vq3c` (8 s, seme fisso); dieci condizioni da 90 fotogrammi.

| Previsione (scritta prima) | Esito |
|---|---|
| VB1: Q3c, 0 punti profondi ovunque | **regge**: 0; al bordo al più 144 punti |
| VB2: senza «pixel centrale valido», soggetto che non rimanda segnale | **regge**: 50 fotogrammi su 90 |
| VB3: resa ≥ 90 %; 80–92 % col 5 % sparso | **smentita in parte**: 88,4–91,8 %; 79,4–83,1 % |
| VB4 (= PD1): Q3c sulle celle, quota 0,10 m | **regge**: 0 profondi, resa 87,1 %. A 0,05 m la resa è **3,1 %**: il margine legge il pavimento come «occupato». D non scrive la quota |
| VB5 (= PD2): cambi per cella, 5 % sparso | **regge**: 2,04 al secondo (N1: 0,08); 3,72 col 10 %; 5,92 con chiazze al 30 % |
| VB6: N1 con la memoria, soggetto che non rimanda | **regge**: 58 fotogrammi su 90, 558 celle |
| VB7: regola dei settori (specializzazione §3.1) su Q3c, scena ferma, 5 % sparso | **regge**: mediana **1,4 m** su 3,0; «fino alla portata» 0,0 %; «sconosciuto» 44,4 %; N1 3,0 m e 100 % (180 settori-fotogramma) |

Conseguenza: PD1 e PD2 reggono alla lettera, ma la struttura adottata scambia un difetto di sicurezza con un'uscita inutilizzabile appena il sensore ha buchi radi: la regola dei settori si ferma alla prima cella non libera e Q3c chiede nove pixel validi attorno a un punto solo.

**`validazione-1`** (suolo visto ora, senza memoria): **smentita** sulla sicurezza, 32 fotogrammi su 90 (il rumore sposta punti del suolo dentro la cella coperta). **`validazione-2`, «impronta del suolo».** *Meccanismo:* tabella fissa pixel → cella toccata dal raggio e profondità attesa del suolo; cella libera ⟺ almeno un pixel dell'impronta è valido ora e legge quella profondità entro m(z), e la cella non è occupata né in ombra ora. Niente memoria. *Esito (VB9, scritta prima):* 0 profondi in tutte le condizioni; col 5 % sparso 3,0 m e 0 cambi; col 30 % sparso resa 83,0 % (Q3c: 8,0 %). *La smentisce:* un centro-cella profondo dato per libero; mediana sotto 2,7 m col 5 % di buchi veri. *Limiti:* un autore, 25 minuti di vita; non legge la quota; chiede il suolo tarato; un errore d'assetto oltre circa 1° le fa perdere il libero lontano (conto a mano: verso prudente).

## 4. Tre prove di cinque minuti sull'hardware

1. **Stanza ferma, 60 s, poi mano sul sensore.** Si registra: quota di pixel validi, forma dei buchi (radi o a chiazze), distanza libera per settore. *Smentita:* mediana sotto 2,5 m in un settore sgombro, o più di 3 cambi al secondo; «affidabilità persa» oltre 1 s dalla copertura, o una cella libera a sensore coperto.
2. **Soggetto scuro, 10 passaggi a 2 m su una riga di nastro.** *Smentita:* un fotogramma con una cella sotto i piedi data per libera. Dice anche quanti pixel del corpo sono validi.
3. **Pannello, 10 passaggi e 3 soste.** *Smentita:* almeno 100 pixel validi dell'attore sopra il pannello (pannello basso); una ricomparsa fuori dall'area mostrata; una riga «osservato» o «uscito» a soggetto nascosto; occlusione completa sotto 1 s.

Dieci esiti buoni su dieci dicono solo «tasso di fallimento sotto il 26 % al 95 %»; per il 5 % servono 59 passaggi.

## 5. Q2: la tabella frase → componente → momento

Undici righe, nessuna con una misura nella cella: c'è uno stato. **Con una misura nei file:** mobili e ostacoli (nucleo), identità al ritorno (14 400 passaggi), affidabilità (T, scenario A), registro (0 su 600, ma 16–52 % di eventi mancati), sicurezza (T; vetro smentito). **Coperte solo per lettura:** «orientamento assistito» (un'etichetta), «Intelligenza Artificiale» (niente, se si taglia l'etichetta), «aerospaziali», «ispezione», «oggetti». **Senza misura:** «feedback chiari e tempestivi» (e §3 dice che con Q3c sulle celle non lo sono), la previsione (in f8), «la scena continua a cambiare» insieme all'occlusione, la latenza (non risolta). **Atto 4:** col pannello largo 1 m l'occlusione completa dura 0,59 s a 1,4 m/s e 0,83 s a 1,0 m/s (conto mio): troppo poco per mostrare la continuità; serve un pannello di circa 2 m o un passo lento.

## 6. Stati, momento, continuità visiva

| Scelta | Stato che propongo | Ore; quando | Continuità |
|---|---|---|---|
| NO alla mappa voxel; NO a S10 | regge | dopo | non tocca (nel ciclo ostacola) |
| N1; affidabilità sui pixel; regioni dopo la copertura; frase con la quota | reggono come in D | 2–2,5; **14 ore** | la terza aiuta |
| «Libero» delle celle: `validazione-2` al posto di `stato(centro)` | sostenuto dai dati, un autore | circa 1 (stima mia); **14 ore**, se un secondo ruolo rilancia `vq3c` | aiuta: toglie la previsione solo dove il suolo è visto |
| `stato(p)` Q3c | sicurezza: sostenuto, due autori; resa: dipende dai buchi veri | 2–3; **14 ore solo se f8 la usa**, altrimenti 4 ore | aiuta; col 30 % di buchi ritaglia poco (resa 8 %), dal lato prudente |
| Registro con «come lo so» | logica controllata | 3–4; **14 ore** | aiuta |
| rec | un autore | 2–3; 4 ore | aiuta |
| Pannello largo 1 m | smentito per calcolo come prova di continuità | 0 | ostacola la demo |

**Dopo.** All'arbitro: i cinque cambi di stato del §0 e la scelta fra `stato(centro)` e `validazione-2`. A un secondo ruolo: rilanciare `vq3c` e attaccare `validazione-2`. Alla squadra, appena c'è un sensore: la prova 1 del §4, che decide fra buchi radi e chiazze.
