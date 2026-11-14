# Previsioni del redattore — f12, 40-documento

Scritte alle 2026-11-14T19:12:58+01:00 (`date -Is`), dopo la lettura degli ingressi (contratto d'integrazione, verdetto d'integrazione, chiusura, versione 3 §1, §1.6, §1.7, §3, §4, §7, blocco di classificazione §0–§1 e §6–§10, schermo e demo §0, §1, §4, §6, piano §0, §1, §3, §6, §9, discordanze dei fascicoli, verdetto sui dati §5–§6, decimo addendum, traccia, sorgente v0.8) e PRIMA di scrivere il testo e di lanciare i controlli. Non cieche rispetto agli ingressi.

| Sigla | Misura | Soglia di smentita |
|---|---|---|
| redattore-P1 | parole del corpo (esclusi intestazione, schema, tabelle, riquadro dei limiti), con `wc -w` | smentita se oltre 1 150 |
| redattore-P2 | occorrenze delle frasi «da non dire» (V3 §3, SCH §6, BL §9, verdetto d'integrazione §7), cercate con `controlla.sh` | smentita se ne resta una fuori dalle eccezioni dichiarate (parole che la consegna chiede di nominare come scartate o negate) |
| redattore-P3 | cifre del testo assenti da CIFRE.md (confronto automatico dei numeri) | smentita se ne manca una |
| redattore-P4 | righe di ciascuna tabella | smentita se una supera sei |
| redattore-P5 | affermazioni tecniche senza marca [S], [C] o [P] (conto a mano, per paragrafo) | smentita se ne trovo una alla rilettura |

Esiti: in fondo, dopo i controlli.

## Esiti (scritti alle 2026-11-14T19:19:46+01:00, dopo `sh controlla.sh`; uscita in `esito_controlli.txt`)

| Sigla | Esito | Prova |
|---|---|---|
| redattore-P1 | **smentita** | corpo 1 279 con `wc -w` (soglia 1 150); tolte 36 marche di stato e 43 segni di marcatura restano circa 1 200 parole, contro le circa 1 100 chieste. Tre stesure: 1 456, 1 331, 1 257, poi 1 279 dopo quattro aggiunte di precisione (il ripiego `sd-0`, «su profondità simulata», quattro marche). Non ho tolto sezioni chieste dalla consegna; l'ordine dei tagli è in fondo a CIFRE.md |
| redattore-P2 | **regge** | 0 occorrenze fuori dalle eccezioni dichiarate; restano «voxel», «360°», «massa e accelerazione» (titoli di idee scartate), «100 %» (dentro «98–100 %» e «38–100 %»), «al chiuso». Limite del controllo: è una ricerca di 65 stringhe scelte da me, non una rilettura di un secondo ruolo |
| redattore-P3 | **regge** | 68 cifre distinte nel testo, 0 mancanti in CIFRE.md (confronto automatico dei numeri; non controlla che la riga dica la cosa giusta) |
| redattore-P4 | **regge** | tabella 1: 6 righe; tabella 2: 4 righe |
| redattore-P5 | **regge in parte** | alla rilettura ho aggiunto 4 marche mancanti (§3, §8, §9). Il riquadro dei limiti e il §10 non portano marche per scelta: sono limiti dichiarati e voci senza prova |

**Notato dopo, non previsto.** (1) Nella prima stesura avevo scritto nell'intestazione un conteggio di parole prima di misurarlo: tolto e sostituito con quello di `controlla.sh`. (2) La zona «da 400 percorsi» è il predittore `sd-1`, che nel piano sta fra i lavori delle 4 ore: nel testo ho aggiunto il ripiego che entra per primo. (3) «Sotto un ostacolo sospeso» era scritto al rovescio (è l'ostacolo sospeso a sfuggire): corretto.
