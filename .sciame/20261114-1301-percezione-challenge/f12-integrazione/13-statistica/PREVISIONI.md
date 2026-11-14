# PREVISIONI — controllo statistico delle prove nuove (sciame-statistico, f12)

Scritte alle **2026-11-14T18:09:41+01:00** (`date -Is`), prima di aprire un solo file grezzo di `02-prova-insieme/ris/` o di `03-libero/` e prima di
scrivere un programma mio. **Non cieche:** a quest'ora ho letto il contratto d'integrazione, `PROVA_INSIEME.md`,
`LIBERO_DELLA_CELLA.md`, i loro due `PREVISIONI.md`, `rifai.sh` della prova d'insieme e l'elenco dei file con le ore. Conosco
quindi le cifre dichiarate dagli autori; non conosco i file grezzi, i programmi, né V8, V7, VD (li leggo dopo).

| # | Misura | Regge se | Smentita se | Previsione mia |
|---|---|---|---|---|
| S1 | Ore: PREVISIONI.md di ciascuna prova più vecchio del primo file dei risultati (ora di modifica del file) | più vecchio | più recente o uguale | insieme: regge (17:51:12 contro 17:54 del fumo). libero: **non decidibile dall'ora** (il file è stato riscritto alle 17:59:43, dopo il lancio 1 delle 17:55:23) |
| S2 | Riconteggio mio dai file grezzi delle cifre principali (a1, a2, b cella peggiore per geometria e orizzonte, d, f; nuvole-1 = 0 violazioni su 9 000 + 9 000 fotogrammi; S2 = 3,0 m) | differenza 0 su ogni conteggio intero | almeno un conteggio diverso | regge (0 differenze); possibile una differenza di definizione sul denominatore di a1/a2 (23 402 e non 24 000) |
| S3a | Semi della prova d'insieme: coppie di semi vicini con flussi uguali a meno di uno spostamento fra -8 e +8, misurate da me sul generatore di `insieme.c` | 0 su almeno 1000 coppie | almeno 1 | regge (0) |
| S3b | Semi del banco del «libero»: lo stesso seme di rumore riusato fra condizioni diverse (numeri casuali comuni) | semi distinti per condizione | stesso seme in più condizioni | **cade**: prevedo semi riusati fra condizioni (i 15 000 fotogrammi non sono 15 000 estrazioni indipendenti); nessun difetto «spostato di uno» |
| S3c | Lancio 2 del «libero» con «semi nuovi»: frazione di righe identiche al lancio con i primi semi | sotto il 50 % delle righe con buchi o rumore | oltre il 90 % | regge (i semi sono davvero diversi) |
| S4 | Denominatore di (b): passaggi con il corpo tutto nascosto all'istante esatto; quota dei passaggi esclusi a 3 s | dichiarato e unico | due denominatori mescolati nella stessa cifra | l'esclusione a 3 s supera il 40 % dei passaggi in almeno una geometria (sopravvivenza selettiva: resta nascosto chi si ferma) |
| S5a | Celle di T e L (5 comportamenti x 3 orizzonti x 2 geometrie = 30) col limite inferiore di Wilson al 95 % sopra la soglia (0,90 a 1 e 2 s; 0,85 a 3 s), misura secondaria | 30 su 30 | meno di 30 | regge, 30 su 30 |
| S5b | Le stesse 30 celle con la correzione di Bonferroni (livello 0,05/30 per cella) | 30 su 30 | meno di 30 | regge 30 su 30, ma la cella peggiore a 2 s in L scende sotto 0,915 |
| S5c | D: celle sotto soglia, misura primaria a 1 s | — | — | 4 su 5 sotto 0,90, come dichiarato |
| S6 | nuvole-1: limite superiore al 95 % della quota di fotogrammi con violazione, contando le condizioni (non i fotogrammi) come unità | — | — | con 300 condizioni x 2 semi: «meno di 1 condizione su 100», non «2 fotogrammi su 10 000» |
| S7 | Numerosità dal vivo per distinguere 0,90 da 0,80 (una coda, 0,05, potenza 0,80), binomiale esatta | — | — | fra 70 e 110 passaggi; da 0,85: fra 300 e 450; in un'ora con due persone: fra 60 e 120 passaggi utili |
| S8 | Confronto con V8: cifra di D con corpo esteso sotto quella di V8 (0,922) | — | — | differenza attesa per il corpo esteso (non per i semi): la decide il braccio «puntiforme» se esiste nei file |

Esiti possibili: regge, smentita, non risolta. Ciò che noto dopo lo marco «notato dopo».

## Esiti (scritti alle 2026-11-14T18:17:47+01:00, dopo le prove; file accanto)

- **S1** insieme: **regge** (`PREVISIONI.md` 17:51:12,7; primo risultato, il fumo, 17:54:47; impronta `b60d31d0…` uguale a quella dichiarata; `ore_dei_file.txt`). Libero: **non risolta dall'ora del file**, come previsto (riscritto alle 17:59:43; lancio 1 alle 17:55:23); le due soglie però stanno nel contratto delle 17:43:55.
- **S2 regge**: 0 differenze sui conteggi interi delle due prove (`riconta_insieme.txt`, `riconta_libero.txt`). Due etichette, non conteggi: «217 861» sono i soli confermati (218 646 con i non confermati); «11 946 289 istanti» esclude i lanci con l'estraneo e il braccio «toglie» (in tutto 13 181 034, sempre 0 fuori da R100).
- **S3a regge**: 0 sovrapposizioni fra 437 400 flussi entro 39 passi; controllo positivo 39 000 su 39 000 (`semi_insieme.txt`).
- **S3b smentita (in bene)**: nel banco del «libero» i semi sono uno per condizione, 500 distinti su 500, 0 in comune fra i due lanci.
- **S3c regge**: righe identiche fra i due lanci 0,6–13,3 % con i buchi (33,7 % senza buchi).
- **S4 regge**: a 3 s resta nel denominatore il 55 % dei passaggi in T (29 % in «prosegue»), il 41 % in D, l'85 % in L. Denominatore unico per misura, dichiarato.
- **S5a regge** 30 su 30. **S5b regge** 30 su 30; L «torna» a 2 s scende a 0,914. **S5c regge**: in D 4 celle su 5 sotto 0,90 (5 su 5 con Bonferroni).
- **S6 regge**: 0 su 300 condizioni, limite 1,26 %; 0 su 10 scene, limite 27,8 %.
- **S7**: 0,90 contro 0,80: n = 94, **regge**. 0,90 contro 0,85: n = 296 (potenza 0,80), 401 (0,90): previsto 300–450, **smentita di 4 passaggi** al bordo basso. Passaggi in un'ora: **non risolta** (è una stima, nessuna misura).
- **S8 regge**: sugli stessi 400 semi in D il soggetto puntiforme dà 0,975 / 0,967 / 0,951, l'esteso 0,938 / 0,924 / 0,913 (`confronti.txt`).
- **Notato dopo** (non previsto): lo stesso camminatore (seme, comportamento, geometria) torna in tutti i lanci e in tutti i bracci (righe 101, 224 e 351 di `insieme.c`): 226 400 passaggi lanciati sono al più 70 400 camminatori distinti; i 24 000 di (a) sono 6 000. Nel «libero» a +0,5° e k = 0,0100 la distanza scende a 2,4 m. In (b) «chi svolta» sta sopra le cifre di V8 a 2 e 3 s.
