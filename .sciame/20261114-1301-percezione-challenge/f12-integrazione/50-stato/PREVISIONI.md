# Previsioni del redattore (f12, 50-stato) — scritte prima dei controlli

Ora: 2026-11-14T19:20:52+01:00 (`date -Is`). Scritte dopo aver letto il contratto d'integrazione, il verdetto d'integrazione, la chiusura, la soluzione versione 3, il verdetto dei dati e le discordanze dei fascicoli; prima di scrivere la versione 3 del documento di stato e prima di ogni controllo. Non sono cieche rispetto a quei testi.

Le mie sole prove sono controlli testuali sul file consegnato (`STATO_PROGETTO.md` in questa cartella). Non eseguo simulazioni e non riconto cifre: ogni cifra viene dal file citato.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| R1 | Nessun percorso citato fra accenti gravi nel documento manca sul disco | programma `controlla.py`: percorsi che finiscono in un'estensione nota o in «/», risolti rispetto alla cartella della convocazione, alla radice del progetto o alla cartella del file citato subito prima | 1 o più percorsi **nuovi** (introdotti dalla versione 3) inesistenti. I percorsi mancanti già nella versione 2 si contano a parte e si elencano |
| R2 | Nessuna tabella rotta | per ogni blocco di righe che iniziano con «\|»: stesso numero di colonne in tutte le righe, riga di separazione presente come seconda riga | 1 o più tabelle con colonne diverse o senza separatore |
| R3 | Il contenuto della versione 2 non è tolto | righe della versione 2 assenti nella versione 3 | più di 60 righe tolte o riscritte (attese: testa, sintesi, indice, §5.1, §5.6, §5.7, registro); ognuna deve avere una sostituzione o una riga «superato da …» |
| R4 | Nessuna frase «da non dire» usata come affermazione | ricerca di «validato», «via libera», «garantit» fuori da virgolette o da negazioni, lette a mano | 1 o più usi affermativi |
| R5 | Tutti gli ingressi obbligati sono citati almeno una volta | ricerca dei 22 percorsi d'ingresso della consegna | 1 o più mancanti |

Esiti: in fondo a `MODIFICHE.md`.
