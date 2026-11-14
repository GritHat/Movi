# Controllo statistico delle due prove nuove (C-C e C-D) — `sciame-statistico`, f12

Lavoro dalle 18:08:59 alle 18:22 del 14 novembre 2026 (`date -Is`). **Tutto ciò che ho controllato è simulazione: niente diventa «validato».** Accanto, in `f12-integrazione/13-statistica/`: `PREVISIONI.md` (18:09:41, prima di aprire un file grezzo; esiti in coda), i programmi `riconta_insieme.py`, `semi_insieme.py`, `riconta_libero.py`, `confronti.py`, `dettagli.py`, `potenza.py`, `confronta_tabelle.py`, le loro uscite `.txt` con lo stesso nome, `ore_dei_file.txt`, `rifai.sh` (rifà tutto in meno di un minuto). Sigle: **PI** = `02-prova-insieme/PROVA_INSIEME.md`; **LC** = `03-libero/LIBERO_DELLA_CELLA.md`. D / T / L = geometrie di PI (D: demo, pannello largo 1 m; T e L: 2 m).

## 0. In testa

**Cambi di stato proposti.** Nessuna cifra cambia stato rispetto a PI e LC: i conteggi tornano tutti. Cambiano tre **diciture**: (1) «0 vuoti, limite superiore 1,7 su 10 000» diventa «**meno di 6,4 su 10 000**» (6 000 camminatori distinti, non 23 402 prove indipendenti); (2) in D «almeno 88 su 100 a 1 s» diventa «**almeno 87 su 100**» (cinque celle guardate insieme); (3) per `nuvole-1` «meno di 2 fotogrammi su 10 000» **non è una frequenza**: lo stato giusto è «**verificato sull'insieme dichiarato**» (10 scene, 300 condizioni, due lanci), non «sostenuto come quota».

**Regole e scostamenti miei.** Previsioni non cieche: avevo già letto PI, LC e le loro previsioni. Due conti brevi fatti con il `python3` di sistema (sola libreria standard), poi rifatti con l'interprete di f10. Nessuna scrittura fuori dalla cartella; niente git, rete, sudo. **Letti solo in parte:** V7 (righe su K-107, V-017, V-018), V8 (§2, §2.1), VD (tutti i paragrafi, righe lunghe troncate). **Non aperti:** V9, VN, l'audit, f6. Lunghezza al limite delle tre pagine (circa 2 700 parole, in buona parte tabelle). **Prova sull'identità:** `06-identita/IDENTITA_SU_PROFONDITA.md` è comparsa alle 18:17:45, a lavoro quasi finito: ne ho letto il §0–§2, **non l'ho ricontata**; la controprova `07-controprova-identita/` **non è ancora consegnata**.

**Indipendenza.** Condivido con PI e LC i file grezzi (righe «R» di `ris/*.txt`; `banco*.json`), la specifica e il modello linguistico; non gli script di lettura. Vedo errori di somma, di denominatore e d'intervallo; **non vedo** un errore dentro `insieme.c` o `banco_libero.py`, che non ho rieseguito.

## 1. I controlli da 1 a 5 (il 6 è al §4, il 7 al §5)

| Controllo | Prova d'insieme (C-C) | «Libero» della cella (C-D) |
|---|---|---|
| **1. Soglie scritte prima?** | **Sì.** `PREVISIONI.md` 17:51:12,7; primo risultato (fumo) 17:54:47; impronta `b60d31d0…` come dichiarata. PI scrive «17:51:24»: 12 s di differenza nel testo, senza effetto. Soglie già nel contratto (17:43:55) | **Soglie sì; ordine del file non dimostrabile.** S1 e S2 stanno nel contratto (17:43:55). Il file è stato riscritto alle 17:59:43, dopo il lancio 1 (17:55:23): l'ora non prova niente. Indizio a favore: `banco_lancio1.json` ha solo le 5 regole di partenza. Le varianti prudenti nascono **dopo** il lancio 1 (dichiarato) |
| **2. Riconteggio** | **0 differenze** su 300 righe di 75 file: 0 vuoti; scoperti 24 su 23 402 (17 confermati + 7 non confermati); le 72 celle di (b), confrontate a macchina con `ris/TABELLE.txt` (`confronta_tabelle.txt`); estraneo 3027/3041, 3493/3616, 3239/3546; riaggancio 10 711/10 757, 9228/9240, 6772/6967; le quattro righe della tabella di K-215 | **0 differenze** su 4 500 + 4 500 righe: V-017 770 (527) / 835 / 238 / 163 fotogrammi; V-018 un pixel 533 (20) / 98; metà impronta 6 (3) / 6; `nuvole-1` 0 su 9 000 + 9 000; S2 3,0 / 3,0 m; rese 86,8 / 62,6 / 78,3 / 45,4 % |
| **3. Semi** | **Nessun flusso spostato** (il difetto di K-223): 0 stati comuni fra 437 400 flussi (ogni seme × comportamento × geometria × ruolo, più la libreria) entro 39 passi; il mio controllo positivo ne trova 39 000 su 39 000. Correlazione fra semi vicini +0,0005 e −0,0015 (errore tipo 0,002). **Ma i semi si riusano fra i lanci** (critica 1) | **Indipendenti:** un seme per condizione, 500 distinti su 500, 0 in comune fra i due lanci; con i buchi le righe identiche fra i lanci sono lo 0,6–13 % |
| **4. Denominatori** | Uno per misura, dichiarato: (a) confermati + non confermati = 23 402 su 24 000 (598 mai nascosti, esclusi). (b) passaggi **ancora tutti nascosti** all'istante: a 3 s il 55 % in T (29 % in «prosegue»), 41 % in D, 85 % in L. Esclusi e tenuti «a parte» **prima** dei dati: chi svolta, chi esce lontano, chi parte da fermo (3 comportamenti su 8). Tre totali diversi sotto «tutti i lanci» (critica 2) | 7 200 fotogrammi = 240 condizioni (16 combinazioni × 5 buchi × 3 errori); 9 000 = 300 condizioni con le due scene in più. S2: 270 settori-fotogramma, ma solo 9 settori su 17 vedono il suolo da 1,3 m. Escluso dalla soglia: ±1° (misurato a parte) |
| **5. Intervalli** | §2 | §3 |

## 2. Prova d'insieme: intervalli e confronti multipli

Limite inferiore di Wilson al 95 %; fra parentesi lo stesso con la correzione di Bonferroni su 30 celle (z = 3,14). «Primaria» = solo gli istanti in cui lo schermo dice «previsto»; «secondaria» = tutti gli istanti nascosti (confrontabile con f8). File: `riconta_insieme.txt`.

| Geometria | Celle sopra soglia (5 comportamenti × 3 orizzonti) | Cella peggiore fino a 2 s | Cella peggiore a 3 s |
|---|---|---|---|
| T | 15 su 15, anche con Bonferroni, entrambe le misure | secondaria 1222/1265: 0,955 (0,946) | secondaria 666/698: 0,936 (0,922) |
| L | 15 su 15, anche con Bonferroni, entrambe le misure | secondaria 2125/2279: 0,921 (0,914); primaria 1995/2112: 0,934 (0,927) | secondaria 1754/1922: 0,899 (0,890); primaria 0,909 (0,900) |
| D | primaria a 1 s: **1 su 5** sopra 0,90 (0 su 5 con Bonferroni); a 2 e 3 s nessuna cella arriva a 400 casi. Secondaria: 5 su 5 a 1 s, 4 su 5 a 2 s (3 con Bonferroni), 4 su 5 a 3 s | primaria 1 s 942/1045: 0,882 (0,869; su 5 celle 0,875). Secondaria 2 s 1257/1388: 0,889 | secondaria 845/984: 0,836 |

- **«In tutte le celle» regge in T e L** (30 su 30) anche dopo la correzione. Stato: sostenuto dai dati in simulazione.
- **Scoperti con c7:** rilevamento 0,9, corpo esteso 1 su 5 704, limite superiore 0,99 per mille: «meno di 1 su 1000» regge **al bordo**. Rilevamento 0,7, corpo esteso 17 su 5 704: 1,9–4,8 per mille: PI scrive «circa 2 su 1000», la forma vera è «**fino a 5 su 1000**» (`dettagli.txt`).
- **Estraneo con c1:** 0,992–0,997 / 0,960–0,971 / 0,904–0,922; casi decisi 3041, 3616, 3546 su 4000 (gli altri: estraneo mai visto o traccia non pendente).

**Confronto con V8 (§2, §2.1).** *Coincidono:* 0 vuoti; scoperti senza c7 con rilevamento 0,7 e corpo esteso, 506/5704 = 8,9 % contro 130/1581 = 8,2 %; K-215 a −10 cm, 0,464 e 0,361 contro 0,46 e 0,37; T e L, cella peggiore 0,921 contro 0,922. *Differenza attesa, e l'ho misurata:* la caduta in D viene dal **corpo esteso**, non dai semi. Sugli stessi 400 semi per comportamento, in D il soggetto puntiforme (quello di f8) dà 0,975 / 0,967 / 0,951 a 1 / 2 / 3 s, l'esteso 0,938 / 0,924 / 0,913; in T e L i due corpi coincidono entro 0,01 (`confronti.txt`). *Differenza attesa:* scoperti con rilevamento 0,9 più alti di V8 (0,6–0,7 % contro 0,3 %) perché PI conta anche i non confermati (i soli confermati: 27 su 5 691 e 7 su 5 968, cioè 0,5 e 0,1 %); riaggancio 0,97–0,999 contro 0,37–0,77 di V8 perché ora ci sono c1 e c2 (lettura mia della riga di V8, non ricontata). *Segnale, non spiegato:* chi svolta e chi esce lontano, in T e L, a 3 s stanno a 0,57–0,70, sopra lo 0,13–0,52 di V8 (a 2 s L dà 0,79 contro al più 0,70): **non risolto**; lo decide lo stesso lancio con il corpo puntiforme. È dal lato buono e riguarda casi tenuti «a parte»: non tocca la cifra dichiarata.

## 3. «Libero» della cella: che cosa dice lo zero

`nuvole-1`: 0 violazioni su 9 000 fotogrammi, due volte. I fotogrammi di una condizione hanno la stessa scena e cambiano solo rumore e buchi. Il limite superiore al 95 % dipende dall'unità (`riconta_libero.txt`): per fotogramma 0,43 per mille (**non indipendenti**); per condizione, 0 su 300, **1,3 %**; per scena, 0 su 10, 28 %. Le scene non sono un campione: sono scelte dagli autori. Quindi: **verificato su 300 condizioni dichiarate, due lanci, un autore**; regola scelta fra quattro **dopo** il lancio 1; i semi nuovi rifanno il rumore, non le scene.

- **S2:** 3,0 / 3,0 m col 5 % di buchi sparsi, a errore 0. La mediana è al tetto della scala (3,0 m su 3,0): l'intervallo non si calcola dai file, che non salvano la distribuzione (**non verificato**). Dentro il dominio di S1, a +0,5° e k = 0,0100, la distanza è **2,4 m**, sotto soglia; col 30 % di buchi 1,5 m.
- **A −1°:** 150 e 145 fotogrammi su 300 con violazione sulla scatola lontana (tornano); le celle sono 798 e 759 contando anche il suolo nascosto (LC ne scrive 503 e 455: presumo le sole «dentro», non verificato).
- **Confronto con V7:** *coincidono* V-017 senza buchi (0 su 1 440 fotogrammi), V-018 a 3,0 m col 5 % e a 1,5 m con chiazze al 30 %, `stato(centro)` a 1,3 m (V7: 1,4). *Differenza attesa:* le cadute di V-017 stanno tutte nelle chiazze (113 celle dentro un corpo con il 5 %, 657 con il 30 %; 0 con i buchi sparsi), condizione che V7 dichiarava «mai provata». Cambi al secondo di V-018 con chiazze al 30 %: 4,97 contro 4,55, altro autore e altro banco.

## 4. Che cosa si può scrivere per la giuria

**Precisione, forma più forte che resta vera.** «In simulazione, con un ostacolo largo 2 m, sensore fermo e una persona alla volta che prosegue, rallenta, si ferma o torna indietro, la persona nascosta sta dentro la zona prevista in **almeno 9 casi su 10 fino a 2 secondi** dall'ultima misura, e in **almeno 85 su 100 fino a 3 secondi**, finché resta nascosta. Vale in 30 casi di prova su 30, con il bordo dell'ombra noto esattamente; non è misurato su un sensore.» Numeri: 12 000 passaggi per geometria, da 608 a 2 359 per cella, limiti peggiori 0,921 e 0,899.
Per la demo con il pannello da 1 m: «a 1 secondo circa 9 su 10 (limite 0,87); dopo, lo schermo dice "è dietro l'ostacolo" e non dichiara un livello».

**«Libero».** «Il sistema dice "suolo visto libero fino a d" solo dove, in quel fotogramma, almeno metà dei punti della cella e di tutte le celle vicine leggono il suolo. In simulazione, con camera ferma e inclinazione nota entro mezzo grado, la regola non ha mai dato per libera una cella con un ostacolo sopra: 300 condizioni, 9 000 fotogrammi, due volte. Con il 5 % di misure mancanti vede libero fino a 3 m; con molte mancanti dice "sconosciuto".»

**Non si può scrivere.** «9 su 10» senza «ostacolo largo, bordo noto, sul percorso»; una cifra in D oltre 1 s; una cifra per chi svolta (0,58–0,79 a 2–3 s) o parte da fermo; «9 su 10» con il bordo stimato (con c3 che manca 2 cicli su 10: 0,74–0,80 a 1 s in T e L); «zero casi su 218 000 passaggi» (i camminatori distinti sono al più 70 400); «2 su 10 000» per il libero; «mai libero» senza «a posa nota»; «2,7 m» su un sensore (modello al limite: 2,2 m, LC); l'identità al ritorno come cifra (§6).

## 5. Quante prove dal vivo (`potenza.txt`, binomiale esatta, una coda, livello 0,05)

| Scopo | Passaggi | Regola del tabellone | Potenza |
|---|---|---|---|
| escludere 0,80 se il vero è 0,90 | **94** (100) | dentro almeno 82 su 94 (87 su 100) | 0,86 (0,88) |
| escludere 0,85 se il vero è 0,90 | **296**; 401 | almeno 262 su 296; 353 su 401 | 0,83; 0,92 |
| escludere 0,85 se il vero è 0,95 | 68 | almeno 63 su 68 | 0,80 |
| scrivere «almeno 9 su 10» (limite di Wilson ≥ 0,90) | 100 | almeno 96 su 100 | 0,44 se il vero è 0,95; 0,82 se è 0,97 |
| 30 passaggi (prova 3 di VD) | 30 | 30 su 30 dà un limite di 0,886 | non può dire «9 su 10» |

**In un'ora con due persone che camminano** (stima mia, **non misurata**: 25–35 s a passaggio con il ritorno, le due persone alternate, un terzo che annota): 90–120 passaggi utili. Bastano per «più di 8 su 10» con potenza 0,86; **non bastano** per distinguere 0,90 da 0,85 (servono 3–4 ore). «Almeno 9 su 10» dal vivo riesce solo se il vero è 0,97 o più. Condizioni: tutti i passaggi nel dominio dichiarato e contati prima di guardare l'esito; 1 s e 2 s si leggono sullo stesso passaggio; divisi per comportamento (20 l'uno) non dicono niente (20 su 20: limite 0,84). Con l'occlusione virtuale del piano (D2) l'unità resta la camminata, non il pannello virtuale.

## 6. Che cosa aggiungono o tolgono i dati veri (VD) e la prova sull'identità

1. **Aggiungono** il moto di pedoni veri (THÖR, 219 tratti, 9 persone): copertura 0,977 / 1,000 / 1,000 a 1 / 2 / 3 s con q = 0,2. È lo stesso ordine di grandezza, ma con cattura del moto e misure buone fino all'ultimo: non conferma lo «0,90» della libreria `sd-1`.
2. **Tolgono** il trasporto delle cifre di PI su profondità: lì la regione contiene la persona in 83 passaggi su 90 (limite 0,848), una sola traccia pendente è falsa (7–66 fantasmi per passaggio), i buchi veri sono il 24–34 %, regime in cui `nuvole-1` scende a 1,5 m e dice «sconosciuto» in quasi metà dei settori; a 1° d'errore di posa il «libero» cade in VD (F-404) come in LC.
3. **Identità al ritorno:** il riaggancio 0,97–0,999 di PI vale per un sensore che dà un punto pulito. Su profondità: 0 su 90 (VD); con la correzione «tracciamento-1», scelta dopo i dati, 88 su 90 a 424 px e 88 su 90 a 848 px nella geometria del catalogo, 0–1 su 10 fuori (letto, non ricontato; controprova non consegnata). Resta «**in correzione**».

## 7. Critiche numerate

1. **Riuso dei semi fra lanci e bracci** (non è K-223, è un altro difetto). Il seme è 7 000 000 000 + 1 000 003·s con s da 0 in ogni lancio (`insieme.c`, righe 101, 224, 351): lo stesso camminatore, con lo stesso rumore, torna in tutti i lanci. 226 400 passaggi lanciati sono al più 70 400 camminatori distinti; i 24 000 di (a) sono 6 000 × 4 bracci. I confronti a coppie (con e senza c7, con e senza c1) ne guadagnano; i totali no. *Stato: verificato per lettura del codice; l'effetto sugli intervalli non è misurato (i file non hanno una riga per passaggio).*
2. **Tre totali sotto «tutti i lanci»:** 217 861 (confermati), 194 861 (senza l'estraneo), 11 946 289 istanti (senza estraneo e senza «toglie»; con tutti 13 181 034, sempre 0 fuori da R100). Nel documento va un totale solo.
3. **La cifra a 3 s parla di chi è ancora nascosto** (in T «prosegue»: 698 passaggi su 2 400), e **c3 usa il bordo vero**: la frase per la giuria porta «finché resta nascosta» e «bordo noto».
4. **`nuvole-1` ha un solo autore e nasce dopo il lancio 1:** serve il secondo autore su scene non sue (già chiesto da LC §4).

## 8. Dopo

Nel registro del tabellone, una riga per passaggio (numero, comportamento, dentro o fuori a 1, 2, 3 s): gli intervalli si rifanno per camminatore. Rilanciare (b) con il corpo puntiforme (D a 4000 semi; «chi svolta» nei due corpi): chiude il segnale del §2. Sul sensore, prima di ogni cifra: la quota di cicli in cui il bordo si riconosce (c3) e la quota di pixel dell'impronta dentro il margine (i 2,7 m).
