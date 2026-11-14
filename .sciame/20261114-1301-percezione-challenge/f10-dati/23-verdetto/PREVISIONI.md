# Previsioni dell'arbitro — verdetto dell'estensione f10

## Blocco A — scritto alle 2026-11-14T17:43:49+01:00, dopo aver letto SOLO il contratto (CONTRATTO_DATI.md) e prima di aprire i contributi e i file dei risultati

Che cosa condivido con ciò che controllo: il modello (stesso modello linguistico degli altri ruoli), la specifica (il contratto). Non condivido il codice dei riconteggi (script miei, in questa cartella) né l'autore dei rapporti.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| A1 | Le cifre dei rapporti tornano dai file dei risultati | riconteggio con script miei di almeno 8 cifre, lette dai file di dati (csv/json), non dai rapporti | smentita se 2 o più cifre su quelle ricontate differiscono oltre l'arrotondamento dichiarato; non risolta se meno di 8 cifre sono ricontabili da file |
| A2 | Almeno una delle sei ipotesi finisce «non decidibile con i dati disponibili» | numero di ipotesi con quello stato nel verdetto | smentita se tutte e sei ricevono un esito confermata/corretta/smentita |
| A3 | Nessuna ipotesi risulta provata con il sensore della squadra (non esiste) | numero di prove su un sensore fisico della squadra | smentita se un contributo riporta una misura su un sensore della squadra |
| A4 | L'errore della maschera d'ombra su profondità realistica NON conferma i ±20 cm assunti dal nucleo senza correzione | stato dell'ipotesi 2 | smentita se l'ipotesi 2 risulta «confermata» con il valore ±20 cm invariato su simulato e su vero |
| A5 | I contributi contengono almeno una contraddizione fra loro su una cifra o su uno stato | numero di K nuove | smentita se zero contraddizioni dopo il controllo incrociato |
| A6 | L'avversario (22) abbassa lo stato di almeno un'affermazione della validazione (20) | confronto degli stati | smentita se nessuna affermazione cambia stato dopo l'attacco |

Gli esiti si scrivono in fondo a questo file, in un blocco separato, dopo le prove.

## Blocco B — esiti, scritti alle 2026-11-14T17:49:19+01:00, dopo i riconteggi (`riconta_arbitro.py`, uscita in `riconteggio.txt`)

| # | Esito | Prova |
|---|---|---|
| A1 | **regge** | 14 gruppi di cifre ricontati (C1–C12, C15), 0 differenze oltre l'arrotondamento. Due etichette non tornano, i conteggi sì: «135 sequenze, filtri spenti» sono 131 senza filtri più 4 con i filtri; i «45 al bordo in 1 sequenza» (soglia 40) stanno in 2 sequenze (36 in `scatola15_2p0m`, 9 in `azzeramento_progressivo`) |
| A2 | **regge** | ipotesi 3 e parte 4c non decidibili; 1, 2 e 5 non decidibili sulle registrazioni vere |
| A3 | **regge** | nessun contributo riporta una misura su un sensore della squadra; nessun dispositivo collegato (`04-embedded`) |
| A4 | **non risolta** | al nominale simulato i ±20 cm sono confermati senza correzione (115 su 115); al limite la soglia scritta è smentita (0 su 8); sul vero non decidibile. La mia soglia di smentita chiedeva «simulato e vero»: non scatta, ma la previsione nella sostanza non è confermata |
| A5 | **regge** | sette contraddizioni fra contributi (K-019…K-025 nel verdetto) |
| A6 | **regge** | K-014 ristretta a «posa esatta e ostacoli che rispondono»; «il nascosto non esce mai dalla possibile presenza» smentita fuori dal caso provato; «41 su 45» da riformulare |

**Notato dopo, non previsto.** (a) Con i bordi spenti nel simulatore la fusione persona–pannello scende da 10 su 10 a 1 su 10, ma la continuità resta 0 su 10 (`20-validazione/uscite/mem_coperto_bordi.txt`): la fusione non è l'unica causa. (b) Controllo C16, definito dopo aver letto `misura_ostacoli.txt`: 0 celle «libero» con il centro sotto l'impronta di un ostacolo fisso su 61 192 celle·fotogramma (il vetro non è nella maschera polare della verità: non lo copre).
