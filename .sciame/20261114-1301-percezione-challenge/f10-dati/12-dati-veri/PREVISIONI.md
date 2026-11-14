# Previsioni di sciame-dati (f10, dati veri) — scritte PRIMA di ogni scaricamento e di ogni lettura dei dati

Ora di scrittura: 2026-11-14T16:15:46+01:00 (`date -Is`). A quest'ora ho letto solo: il contratto, DATI_PUBBLICI.md del ricercatore,
AMBIENTE.md e formato_sequenza.md dell'infrastruttura, l'intestazione di scarica.sh e di apri_archivio.py.
Nessun file dei dati è stato scaricato né aperto. Esiti possibili: regge, smentita, non risolta.

| N. | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| D1 | L'archivio TUM fr3/walking_static si scarica intero con scarica.sh | byte del file | diverso da 474 074 105, oppure uscita diversa da 0 |
| D2 | TUM: circa 745 immagini di profondità 640×480 a 16 bit (24,83 s a 30 Hz) | numero di PNG in depth/, forma, tipo | meno di 600 o più di 900; forma o tipo diversi |
| D3 | TUM: quota di pixel validi per fotogramma, mediana fra 60 % e 95 % (luce strutturata, ombre di parallasse) | mediana sulla sequenza | fuori da [60 %, 95 %] |
| D4 | TUM: profondità mediana dei pixel validi fra 1,5 e 4,0 m; nessun valore valido sotto 0,4 m | mediana e minimo in mm | mediana fuori da [1500, 4000]; oltre lo 0,1 % dei validi sotto 400 mm |
| D5 | TUM: la frequenza reale dei tempi è 30 Hz ± 2 e ci sono salti (intervalli oltre 50 ms) in meno del 5 % dei fotogrammi | mediana e quota degli intervalli | mediana fuori da [28, 32] Hz; salti ≥ 5 % |
| D6 | THÖR: i due file sono a 100 Hz, oltre 30 000 righe l'uno, con almeno 9 corpi rigidi; le posizioni mancanti (cattura persa) superano il 5 % per almeno un corpo | righe, colonne, quota di mancanti | frequenza ≠ 100 Hz; meno di 30 000 righe; meno di 9 corpi; nessun corpo con mancanti > 5 % |
| D7 | THÖR: la velocità mediana dei corpi in moto sta fra 0,6 e 1,6 m/s (pedoni al chiuso) | mediana delle velocità sopra 0,2 m/s | fuori da [0,6; 1,6] m/s |
| D8 | Friburgo: l'archivio (2 805 714 553 byte) si completa in al più 5 rilanci da 10 minuti | numero di rilanci, byte | più di 5 rilanci o dimensione diversa |
| D9 | Friburgo: oltre 3000 immagini di profondità 640×480 da tre camere, valori grezzi a 11 bit (tutti ≤ 2047 dopo l'eventuale scambio dei byte) | conteggio, massimo | meno di 3000; valori oltre 2047 in più dell'1 % dei pixel |
| D10 | Friburgo: almeno 20 identità annotate e almeno 10 tratti con visibilità 0 (nascosto) seguiti da una ricomparsa della stessa identità | conteggio sulle annotazioni | meno di 20 identità o meno di 10 tratti nascosti con ricomparsa |
| D11 | Friburgo: dopo la conversione in millimetri la profondità mediana dentro i riquadri delle persone visibili sta fra 1 e 8 m | mediana in mm | fuori da [1000, 8000] |
| D12 | Bag RealSense: profondità 16UC1 già in millimetri (unità 0,001 m), quota di validi mediana fra 70 % e 99 % | codifica, mediana dei validi | codifica diversa; mediana fuori |
| D13 | Tutte le sequenze convertite passano `controlla_sequenza.py --tutti` con 0 errori | codice d'uscita | un errore in una qualsiasi |
| D14 | scaricati/ resta sotto 6 GB (previsti circa 4,1 GB con gli archivi TUM aperti) | `du -sb` | oltre 6 000 000 000 byte |
| D15 | Nessuna delle fonti scaricabili dà la posizione metrica vera delle persone nel riferimento della camera di profondità: «verita.json» con x, z veri si potrà scrivere solo per THÖR (che non ha profondità) | campi presenti nelle annotazioni | una fonte con profondità e posizioni metriche vere delle persone |

Ciò che noterò dopo va in fondo a questo file, in una sezione separata «Notato dopo», con l'ora.

## Esiti (scritti alle 2026-11-14T16:28:30+01:00, dopo le prove)

| N. | Esito | Misura (prova) |
|---|---|---|
| D1 | regge | 474 074 105 byte, uscita 0 (`registro_scaricamenti.txt`, `scaricati/tum_fr3_walking_static/PROVENIENZA.md`) |
| D2 | regge | 723 immagini uint16 480×640 (`converti_tum.py`) |
| D3 | **smentita** | mediana dei pixel validi 58,8 % (min 49,4 %, max 72,7 %): sotto la soglia del 60 % (`statistiche.json`) |
| D4 | regge | mediana delle mediane 2958 mm; nessun valore valido sotto 400 mm su un campione (minimo 697 mm) |
| D5 | regge | 31,0 Hz mediana; intervalli oltre 1,5 volte la mediana (48 ms): 3,9 %; massimo 68,2 ms |
| D6 | regge | 100 Hz; 33 897 e 31 507 righe; 9 caschi con dati (Helmet_1 sempre assente); mancanti dal 24 % all'87 % per casco |
| D7 | regge | 0,98 e 0,99 m/s |
| D8 | **non risolta** | Friburgo risponde solo in `http://`; `scarica.sh` ammette solo `https://` (curl 7 sulla porta 443): non scaricato |
| D9, D10, D11 | **non risolte** | dipendono da Friburgo, non scaricato. La prova che le decide: scaricare l'archivio (serve ammettere `http://`) |
| D12 | **smentita** | codifica «mono16» (non «16UC1»); unità 0,001 m in due file su tre, 0,000125 m nel terzo, che è un SR300 a luce codificata e non uno stereo attivo; validi mediana 58,0 % (stands_still), 61,4 % (stairs), 90,5 % (structured): due su tre sotto il 70 % |
| D13 | smentita alla prima esecuzione, regge dopo la correzione | prima: 9 + 3 errori in due sequenze Princeton, per un errore MIO nel convertitore (indici della verità ripetuti); dopo: 0 errori in 8 sequenze su 8 (`esito_controlli.txt`). Con `--rigoroso` tre falliscono per avvisi veri (tempi irregolari, valori oltre 20 m) |
| D14 | regge | 4 170 220 504 byte (`du -sb scaricati`), di cui 1,72 GB di archivi aperti |
| D15 | regge | nessuna fonte con profondità dà posizioni metriche vere delle persone: solo riquadri (Princeton, DepthTrack) o niente (TUM, RealSense) |

## Notato dopo (non era previsto)

- 16:21 — `structured.bag` non è della classe del sensore della squadra (SR300, luce codificata).
- 16:22 — `stands_still.bag` guarda un piano a 0,35 m: utile per il rumore nel tempo, non per le distanze d'interesse.
- 16:25 — nelle righe «NaN» di Princeton la quinta colonna ripete l'ultimo numero visibile (causa del mio errore in D13).
- 16:26 — sul piano di stands_still i valori sono lungo l'asse ottico (scarto 1,08 mm) e non lungo il raggio (32,6 mm).
- 16:28 — la posizione derivata dal riquadro salta a ridosso dell'occlusione (new_ex_occ4: z = 6,72 m al fotogramma 27, 3,37 m al 31).
- 16:26 — DepthTrack: 19 % dei pixel validi oltre 10 m e scarto nel tempo mediano di 275 mm sui pixel sempre validi: rumore lontano dello stereo o camera in moto, non distinguibili da qui.
