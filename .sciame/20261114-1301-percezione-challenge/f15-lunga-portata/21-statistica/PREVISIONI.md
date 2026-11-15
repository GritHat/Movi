# PREVISIONI (sciame-statistico, f15/21-statistica)

Scritte il **2026-11-15T01:22:30+01:00** (`date -Is`), dopo aver letto i due rapporti ma PRIMA di aprire i file grezzi con codice e di ricalcolare qualunque cifra.

| # | previsione | misura | smentita se |
|---|---|---|---|
| Q1 | Le soglie dei due rapporti sono state scritte prima delle prove | ora in PREVISIONI.md vs mtime dei programmi e dei risultati | un programma di prova o un risultato ha mtime anteriore all'ora delle previsioni |
| Q2 | I semi della prova LP sono distinti (2400/2400) | ricontati dal JSON | il JSON non riporta i semi per passaggio (allora: non verificabile, «non risolto») o ci sono doppioni |
| Q3 | I Wilson ricalcolati coincidono con quelli riportati entro ±0,01 | k/n del rapporto e dei JSON | uno scarto > 0,01 su un intervallo |
| Q4 | Nelle traiettorie la copertura ricalcolata PER MEZZO (media per tratto, n = tratti) dà un limite inferiore più basso del Wilson sui casi; per gli aerei a 10 s resta ≥ 0,80 | bootstrap per tratto, 2000 ricampionamenti | limite inferiore bootstrap < 0,80 per aerei a 10 s |
| Q5 | Taratura e prova sono separate per tratto (nessun tratto in entrambe) | id dei tratti nei due insiemi | intersezione non vuota |
| Q6 | I tratti non coincidono con i mezzi distinti per almeno una classe (più tratti dello stesso volo/veicolo) | conteggio id di mezzo, se ricavabile dai nomi delle scene | ogni tratto ha un mezzo diverso in tutte le classi (allora tratti = mezzi) |
| Q7 | Con la correzione di Bonferroni sulle 12 righe (o 20 celle), le affermazioni «in tutti gli scenari/celle» basate su 0/n o n/n restano vere solo in forma più debole | limite Clopper-Pearson/Wilson a 1-0,05/m | — (è un conto, non una previsione falsificabile; la registro per non scegliere dopo) |

## Aggiunta, scritta il **2026-11-15T01:25:07+01:00**, dopo il primo conto (controllo_esito.txt) e PRIMA della ridivisione

Il primo conto ha mostrato che la divisione per scena mette lo stesso mezzo nelle due metà (aerei 32 voli su 77, auto 37 veicoli su 51, treni 29 su 33, droni 7 voli su 118). Rifaccio la prova di 12-traiettorie con il loro codice, non modificato, sostituendo solo `dividi` con una divisione per mezzo (aerei: numero di volo o ICAO; droni: volo; auto: veicolo; treni: numero del treno), stesso seme, uscite nella mia cartella.

| # | previsione | smentita se |
|---|---|---|
| Q8 | La copertura sulla prova cambia di al più 0,03 rispetto alla divisione per scena in ogni classe × D | uno scarto > 0,03 in una cella |
| Q9 | La quota «fuori avviso» degli aerei resta ≥ 0,2 a ogni D (dipende da v_max, non dalla divisione) | una cella sotto 0,2 |
