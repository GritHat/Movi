# Previsioni — f12, `20-finale` (`sciame-scene-dinamiche`), versione 3 finale

Scritte alle 2026-11-14T18:24:21+01:00 (`date -Is`), dopo aver letto contratto, prima stesura, le quattro critiche, le due prove, il verdetto dei dati, le discordanze dei fascicoli e la prova sull'identità; **prima** di scrivere il documento finale e prima dei controlli sotto. Non sono cieche rispetto a quei testi. Non eseguo simulazioni nuove: le sole prove mie sono controlli testuali sul documento che consegno.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| F1 | Ogni correzione obbligata delle quattro critiche (ATTACCO §4: 12; COMPLETEZZA §5: 11; PIANO_RIFATTO §6: 8; CONTROLLO_PROVE §0 e §7: 3 diciture + 4 critiche) ha una riga nella tabella finale con «applicata» o «non applicata» e il motivo | `controlla_finale.sh`: conta le sigle AT-1…AT-12, CO-1…CO-11, PR-1…PR-8, ST-1…ST-7 in `TABELLA_CORREZIONI.md` | una sigla con 0 occorrenze |
| F2 | I difetti F-401…F-413 e le K-003, K-216, K-305, K-404, K-406, K-016, K-214, K-108, K-219 compaiono tutti nel documento finale | `grep -c` per sigla in `SOLUZIONE_V3.md` | una sigla con 0 occorrenze |
| F3 | Nessuna frase «da non dire» compare fuori dal paragrafo che le elenca: in particolare «nessun ostacolo osservato», «100 % degli istanti», «finisce solo guardando» senza il limite accanto | `grep -n` sulle tre stringhe | un'occorrenza fuori dall'elenco o dalla riga che la dichiara caduta |
| F4 | Il documento non rimanda alla prima stesura per una regola (autosufficienza): la stringa «01-soluzione» compare solo nel §8–§9 (che cosa è cambiato) e nell'intestazione | `grep -n 01-soluzione` | un'occorrenza dentro §1–§7 |
| F5 | Lunghezza entro dodici pagine fitte: al più 9 500 parole (stima mia: circa 800 parole a pagina fitta con tabelle) | `wc -w` | oltre 9 500 parole |
| F6 | Alla consegna `07-controprova-identita/CONTROPROVA_IDENTITA.md` non esiste ancora (alle 18:23 c'era solo il codice) | `ls` a fine lavoro | il file esiste: in quel caso lo leggo e lo applico, o dichiaro che cosa non ho fatto in tempo a leggere |

Esiti: in coda, dopo i controlli.

## Esiti (scritti alle 2026-11-14T18:38:36+01:00, dopo i controlli; comando: `sh controlla_finale.sh`, uscita in `esito_controlli.txt`)

- **F1: regge.** 45 sigle (AT-1…AT-12, CO-1…CO-11, PR-1…PR-8, ST-1…ST-7, più CI-1…CI-7 aggiunte dopo) hanno ciascuna una riga con «applicata» o «non applicata»: 0 difetti. Il controllo vede che la riga c'è, non che la correzione sia giusta: questo lo decide un altro ruolo.
- **F2: regge.** 0 sigle mancanti nel documento (F-401…F-413, le K nominate, `logico-K1`, `sd-K7`, `sd-K8`).
- **F3: regge.** «Nessun ostacolo osservato», «100 % degli istanti» e «via libera» compaiono solo nell'elenco «non si dice mai» e nelle righe che le dichiarano escluse o cadute; «solo guardando» compare in I7 e nel §3 con il limite accanto («con l'occlusore fermo non finisce»). Letto a occhio sulle righe stampate: non è un controllo sul senso.
- **F4: regge.** 0 occorrenze di «01-soluzione» nel documento.
- **F5: SMENTITA.** 13 237 parole contro la soglia di 9 500; impaginato: 23 pagine a corpo 10 con margini di 2 cm, 14 a corpo 8 con margini di 1,5 cm (`pandoc` con XeLaTeX; la prima stesura a corpo 10 ne fa 12). Il limite di dodici pagine fitte **non è rispettato**: dichiarato in testa al documento, con ciò che si taglia per primo.
- **F6: SMENTITA.** `CONTROPROVA_IDENTITA.md` è comparsa alle 18:33:47, a stesura finita. L'ho letta per intero e applicata con 24 ritocchi (`applica_controprova.py`) e con il §15 della tabella.

**Notato dopo, non previsto.** (1) La controprova rompe una mia affermazione della stesura («l'avviso finisce quando l'ostacolo è tolto»): nel codice di `06-identita` non finisce (10 prove su 10); l'ho scritto come difetto aperto (`sd-K8`). (2) Togliere le righe «Incorpora:» con un'espressione regolare ha portato via anche una frase vera di 1.3 (il ripiego di «mobile»): rimessa a mano. (3) Un primo conto delle pagine era sbagliato (33 pagine: le opzioni di impaginazione non arrivavano a `pandoc`): rifatto.

**File di questa cartella.** `SOLUZIONE_V3.md` (consegna); `TABELLA_CORREZIONI.md`; `fai_tabella.py` con `coda_tabella.md` (rifanno la tabella dalla prima stesura); `applica_controprova.py` e `accorcia.py` (ritocchi già applicati: non si rilanciano); `controlla_finale.sh` ed `esito_controlli.txt`.
