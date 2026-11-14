# Previsioni del redattore sul testo finale delle due pagine (`sciame-redattore`, f12, 43-documento-finale)

Scritte alle 2026-11-14T19:28:08+01:00 (`date -Is`), dopo aver letto il contratto, la prima stesura, CIFRE.md, le due letture e il verdetto d'integrazione, **prima** di scrivere il testo finale e di lanciare `controlla.sh`. Misura: lo script `controlla.sh` di questa cartella (copia di quello di `40-documento/`, stesso autore del testo: vale per conteggi e ricerche testuali, non per il contenuto).

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| F1 | Il testo finale non si allunga rispetto alla prima stesura | `wc -w`: corpo, schema, tabelle, riquadro | corpo > 1279, oppure somma delle quattro parti > 2025 |
| F2 | Nessuna frase «da non dire» fuori dalle eccezioni già dichiarate (titoli degli scarti «voxel», «360°», «massa e accelerazione»; «100 %» dentro un intervallo; «al chiuso») | elenco di ricerca di `controlla.sh`, più «sempre», «mai dato», «si spegne quando» | una occorrenza fuori dalle eccezioni |
| F3 | Ogni cifra del testo ha la sua riga in CIFRE.md | punto 5 di `controlla.sh` | una cifra mancante |
| F4 | Il discorso da un minuto sta in 130 parole e non porta cifre assenti dal documento | `wc -w` sul blocco; confronto delle cifre | > 130 parole, o una cifra non presente nel testo |
| F5 | Le correzioni dei lettori applicate sono almeno 17 su 23 (10 dell'esterno, 13 del tecnico) | conteggio nella sezione (a) | meno di 17 |

Esiti: in fondo, scritti dopo i controlli.

## Esiti (scritti alle 2026-11-14T19:39:58+01:00, dopo `sh controlla.sh`; uscita in `esito_controlli.txt`)

- **F1 regge, al limite.** Corpo 1255 (soglia 1279); somma delle quattro parti 2025 (soglia: più di 2025). Tabelle 348 contro 333, riquadro 249 contro 241 e schema 173 contro 172: cresciuti, compensati dal corpo. Notato dopo: per starci ho tolto il punto sui tracciati pubblici di 9 persone, la seconda frase del sottotitolo, i chilometri all'ora e le domande aperte del §10.
- **F2 regge.** Occorrenze trovate: «voxel», «360°», «massa e accelerazione» (titoli degli scarti), «38–100 %» (intervallo), «al chiuso» (una volta), «sempre» in «è sempre "presunto"» (forma di VI, affermazione 11). Nessuna fuori dalle eccezioni. «9 su 10»: una occorrenza, col dominio nella stessa frase.
- **F3 regge.** 62 cifre distinte nel testo, 0 mancanti in CIFRE.md (il controllo è testuale: dice che la cifra compare nella tabella, non che la riga sia giusta).
- **F4 regge, al limite.** 130 parole (conteggio per spazi, in Python); cifre: due metri, nove su dieci, due secondi, tutte nel §3.
- **F5 regge.** 19 correzioni su 23 applicate, alcune in parte; 4 non applicate (E9, T5, T7, T9), più mezza E7 e la parte di E2 sulle frecce.

Non verificato: la lettura del testo finale da parte di un lettore senza contesto (C-G); la resa su due pagine A4 (non impaginato da me).
