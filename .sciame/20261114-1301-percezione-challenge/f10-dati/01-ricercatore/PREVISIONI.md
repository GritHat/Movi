# Previsioni del ricercatore (f10, ricognizione dei dati pubblici)

Scritte alle 2026-11-14T15:58:48+01:00, PRIMA di ogni richiesta alla rete (finora ho letto solo il contratto, l'addendum e le righe sul sensore in SOLUZIONE_V2.md, CONSEGNA.md e FONTI_VERIFICATE.md). Vengono dalla mia memoria degli insiemi di dati: sono ipotesi, non fatti.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| P1 | La pagina dell'insieme «RGB-D People» di Friburgo (Spinello e Arras, 3 Kinect in un atrio) risponde ancora e l'archivio si scarica senza registrazione | codice HTTP della pagina e dell'archivio | pagina o archivio non 200 |
| P2 | L'insieme «Kinect Tracking Precision» (Padova) NON risponde più all'indirizzo originale (pagina personale dell'autore) | codice HTTP | la pagina e almeno un file rispondono 200 |
| P3 | Gli insiemi di pedoni RGB-D dell'EPFL (LAB e CORRIDOR, Kinect v2) rispondono e si scaricano senza modulo | codice HTTP della pagina e di un archivio | pagina non 200, oppure modulo obbligatorio |
| P4 | TUM RGB-D: la sequenza freiburg3_walking_xyz (o walking_static) si scarica con un indirizzo diretto .tgz, dimensione fra 0,3 e 1,0 GB | Content-Length dell'intestazione | non 200, o dimensione fuori intervallo |
| P5 | Princeton Tracking Benchmark: il sito originale non risponde o non offre più i dati | codice HTTP | sito e archivio rispondono 200 |
| P6 | I file di esempio .bag del costruttore per la classe D400 (stereo attivo) sono ancora pubblici con indirizzo diretto, e nessuno ha una verità di riferimento sulle persone | codice HTTP, lettura della pagina | nessun file raggiungibile, oppure un file con posizioni annotate di persone |
| P7 | NESSUN insieme pubblico soddisfa insieme tutte le condizioni: camera a stereo attivo, ferma, a circa 1,2 m, inclinata in basso, profondità grezza, parametri, posizioni vere delle persone per fotogramma anche durante l'occlusione | tabella di confronto | ne trovo uno che le soddisfa tutte |
| P8 | Entro 6 GB si riescono a scegliere tre fonti che insieme toccano le ipotesi 1–5 del contratto (la 6, il costo, la decide qualunque sequenza) | somma dei Content-Length | somma > 6 GB, oppure un'ipotesi fra 1 e 5 senza alcuna fonte |
| P9 | Almeno due candidati richiedono registrazione o modulo (ostacolo) | lettura delle pagine | zero o uno |
| P10 | Per il LiDAR 2D con persone esiste almeno un insieme annotato scaricabile senza modulo (DROW o FROG); per i sensori a tempo di volo multizona (classe VL53L5CX/L7CX/L8CX) NON trovo alcun insieme pubblico con persone e verità di riferimento | ricerca e codici HTTP | LiDAR: nessuno raggiungibile; ToF multizona: ne trovo uno con verità |
| P11 | DepthTrack (camera a stereo attivo della classe D400) è su un archivio pubblico con file separati per sequenza, senza registrazione | codice HTTP e elenco dei file | non raggiungibile, o un solo archivio > 6 GB |

Esiti (regge / smentita / non risolta): scritti in fondo a DATI_PUBBLICI.md, dopo le prove.
