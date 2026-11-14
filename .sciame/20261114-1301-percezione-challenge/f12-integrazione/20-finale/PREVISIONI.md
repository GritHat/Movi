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
