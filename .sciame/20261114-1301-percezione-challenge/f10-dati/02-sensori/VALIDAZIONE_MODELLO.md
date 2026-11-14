# Come validare il modello del sensore contro registrazioni vere — f10, `02-sensori`

Allegato di `MODELLO_SENSORE.md` (sezione 5). I valori attesi vengono da `parametri_sensori.json`; le soglie sono scritte qui prima di ogni prova (14 novembre 2026). Verità di riferimento: la geometria della scena dove è nota (parete piana, bordo verticale a distanza misurata), altrimenti «nessuna» e la statistica è solo descrittiva. Una registrazione fatta con un altro esemplare o un altro modello tara il modello di QUEL sensore, non di quello della squadra.

Si confrontano le stesse statistiche sul simulato e sul vero, per sequenza (non per fotogramma); la taratura dei parametri I e la prova usano sequenze diverse.

| Statistica | Come si misura | Atteso dal modello | Il modello è smentito se |
|---|---|---|---|
| Quota di pixel validi | per fotogramma, sull'intero e sull'80 % centrale; mediana e 5°–95° percentile | 90–99 % al chiuso (ipotesi) | differenza > 5 punti |
| Banda al bordo sinistro | colonne iniziali senza dato per riga, contro fx·B/z | formula + margine 0–25 px | fuori dall'intervallo |
| Rumore su piano | residuo dal piano su parete e suolo, per fasce di 0,5 m; s = σ·fx·B/z² | s fra nominale/1,5 e limite; suolo < 3× parete (P12) | s fuori; suolo ≥ 3× |
| Rumore temporale | scarto per pixel su 30 fotogrammi fermi, diviso lo spaziale | 0,5–0,7 | < 0,3 o > 0,9 |
| Correlazione spaziale | autocorrelazione del residuo | lunghezza > 1 px | rumore bianco |
| Banda d'occlusione | tratto senza dato a sinistra e a destra dei bordi verticali, contro fx·B·(1/z₁ − 1/z₂) | sinistra = formula ± 3 px; destra 0–3 px | simmetrica (P11) |
| Instabilità dei bordi | scarto nel tempo della colonna del bordo di un oggetto fermo | fra 1,5 px e 4,3 cm | fuori |
| Buchi per materiale e persistenza | quota valida su abiti scuri, capelli, pavimento lucido; P(buco a t+1 dato buco a t) | tabella dei buchi | serve a **tarare** le ipotesi I |
| Quantizzazione | passi nell'istogramma della profondità di una parete lontana | 1/32 px | passo diverso: si corregge |
| Filtri nella registrazione | riempimento al 100 %, scie dietro chi si muove | assenti | registrazione filtrata: non usarla per i buchi |
| Tempo | `FRAME − SENSOR`, `ARRIVAL − BACKEND`, intervallo fra fotogrammi | 70 ms; 33,3 ms ± 5 | — |

**Registrazioni pubbliche di D4xx verificate oggi (esistono, non scaricate):** `stairs.bag` (D435 di pre-produzione, 409 MB) e `d435i_sample_data.zip` (472 MB), elencate in `doc/sample-data.md` di librealsense come dati «uncompressed and unfiltered». Non contengono persone nascoste da ostacoli: servono a tarare il sensore, non a provare la previsione.
