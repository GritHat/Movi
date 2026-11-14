# Previsioni dell'arbitro — f8, fase f5 (verdetto della continuità visiva)

Scritte alle **2026-11-14T17:29:27+01:00** (`date -Is`), **dopo** la lettura dei sette documenti d'ingresso (contratto, triage, banco, torneo, modifiche, controprove, analisi), del verdetto del nucleo e degli addendum, e **prima** di aprire un qualunque file dei risultati (`*.tsv`, `ris/*.txt`, `TABELLE*.txt`) e di scrivere lo script di riconteggio. Sono quindi cieche solo rispetto al riconteggio, non rispetto ai documenti.

Misura: per ogni cifra, il valore che esce dal file dei risultati con un mio script (`riconta_verdetto.py`), confrontato con quello scritto nel documento. «Torna» = identico al conteggio, o entro l'ultima cifra scritta per le quote.

| # | Previsione | Soglia di smentita |
|---|---|---|
| P-v-1 | Almeno 12 cifre ricontate, e tornano tutte | una sola che non torna (smentita: lo dico in testa e non uso la cifra com'è scritta) |
| P-v-2 | La spiegazione dello statistico su O1 è giusta: nella stessa cella («prosegue», 3 s, D) il banco dà 86/92 con il denominatore «dentro l'area osservata» e 86/98 con «tutti i nascosti»; la soluzione dà 101/105 e 101/119 | un numeratore diverso fra le due definizioni nello stesso file, o denominatori diversi da quelli scritti |
| P-v-3 | Nei file della soluzione (`13-soluzione/ris/prova_*.tsv`) il riaggancio dei «prosegue» è 212/331, 336/345, 207/232 (D / T / L), come dice l'avversario: la soluzione aveva il difetto nei propri dati | conteggi diversi di più di un'unità |
| P-v-4 | `15-statistica/ris/prova_semi.txt` mostra 1000 uguali su 1000 (flussi dei semi contigui spostati di un numero) | meno di 1000 |
| P-v-5 | Passaggi con un vuoto per il nucleo (L0), banco: 1958 / 1991 / 1999; per `sd-1`: 0 / 0 / 0 su 2716 / 2800 / 2798 | un valore diverso |
| P-v-6 | C-EST su «sosta» a 3 s (banco): 0,72 e 0,53 in T, 0,14 e 0,00 in L | uno scarto oltre 0,01 |
| P-v-7 | Attacco 5 su C-EST (banco, «prosegue»): A 0,28 / 0,30 / 0,00; B 0,997 / 0,71 / 0,00 | uno scarto oltre 0,01 |
| P-v-8 | Controprova «tutto insieme» (`14-attacco/ris/tutto_T.txt`): 136/364 a 1 s e 43/152 a 2 s su «prosegue» | conteggi diversi |
| P-v-9 | Sessione con la regola 2 (`sess_*`): pendenti alla fine 87 / 117 / 95; riagganci 0 su 66 e 0 su 100 dopo la prima «ambigua» | conteggi diversi |
| P-v-10 | Somma delle ore delle correzioni c1–c8 (fascia «14 ore»): fra 4,25 e 5,25 ore-persona, cioè «circa 5» torna | somma fuori da 4–5,5 |
| P-v-11 | Bilancio: 37 + 15,5 + 4 = 56,5 torna; con le correzioni dell'attacco (circa 5) e le due righe da 50 camminate (circa 2) si arriva a 62–64 ore-persona: sta in 70 (5 persone), **non** in 56 (4 persone) senza il ripiego `sd-0`, non in 42 (3 persone) | somma che sta in 56 con `sd-1`, o che non sta in 70 |
| P-v-12 | R100 (strato 1) contiene il nascosto nel 100 % in ogni file che ricontrollo (0 passaggi fuori) | un passaggio fuori |
| P-v-13 | Il mio giudizio finale, scritto prima del riconteggio: il nucleo V2 **non** rispetta l'imperativo (controlli 1, 3; in parte 2 e 4); le modifiche lo fanno rispettare **in simulazione, a sensore fermo, con maschera esatta**, con il controllo 3 valido «sul percorso fino a 2 s» e **controesempi certificati** fuori da quel dominio (maschera a −10/−20 cm con corpo esteso; chi parte da fermo; camminatori diversi dalla libreria; sensore in moto); adottabile come progetto di prototipo con le correzioni c1–c8, non come sistema validato | il riconteggio mostra che una delle cifre portanti (0 vuoti; ≥ 0,90 fino a 2 s; R100 al 100 %) non torna |

Esiti: in coda, dopo il riconteggio.

## Esiti (dopo il riconteggio; `riconta_verdetto.txt`, `riconta_semi.txt`, `semi_altri.txt`)

| # | Esito | Numero |
|---|---|---|
| P-v-1 | **regge** | 29 gruppi di cifre su 29 tornano; quattro note di lettura, nessuna cifra sbagliata (vedi il verdetto, in testa) |
| P-v-2 | **regge** | banco: in90 = 86, n = 98, fuori griglia 6 → 86/92 e 86/98; soluzione: 101, 119, 14 → 101/105 e 101/119 |
| P-v-3 | **regge** | 212/331, 336/345, 207/232 |
| P-v-4 | **regge** | 1000 su 1000 nel file; rifatto da me in Python dalle righe 25–40 di `gen.h`: 1000 su 1000 |
| P-v-5 | **regge** | 1958 / 1991 / 1999 (cinque comportamenti sul percorso); `sd-1` 0 su 2716 / 2800 / 2798 |
| P-v-6 | **regge** | T 282/393 = 0,718 e 209/393 = 0,532; L 54/399 = 0,135 e 0/399 |
| P-v-7 | **regge** | A 100/355, 104/343, 0/240; B 354/355, 245/343, 0/240 |
| P-v-8 | **regge** | 136/364 e 43/152 |
| P-v-9 | **regge** | D (1; 0 su 66; 87), T (4; 0 su 100; 117), L 95 |
| P-v-10 | **regge** | 4,25–5,25 ore-persona |
| P-v-11 | **regge alla lettera, ma con una smentita notata dopo** | 56,5 torna; con le correzioni 61,5–67,75 con `sd-1` (sta in 70). Notato dopo: nemmeno con il solo `sd-0` sta in 56 (58,5–62,75): la mia frase lasciava intendere di sì |
| P-v-12 | **regge** | 0 fuori da R100 su 35 780 istanti distinti nel banco (572 480 righe-campione, perché ogni istante è contato per 16 predittori), 35 891 nella soluzione, 104 131 a semi riparati: 175 802 in tutto; più 156 celle delle controprove |
| P-v-13 | **regge** | le tre cifre portanti tornano; il giudizio resta quello scritto prima |

**Notato dopo (non previsto prima).** (a) `semi_altri.py`: il difetto dei semi di `gen.h` non tocca `torneo.c` né `att.c` (0 numeri in comune su 20 000 fra semi contigui). (b) `riconta_semi.py`: con i semi riparati 45 celle su 45 fino a 2 s hanno il limite inferiore di Wilson sopra 0,90 con i due denominatori; per `sd-0` sono 37 su 45. (c) Il riaggancio del nucleo nel banco, «prosegue»: 252/355, 340/343, 219/240 (D / T / L). Queste tre letture non hanno una previsione scritta prima: valgono come riconteggi, non come conferme di una previsione.
