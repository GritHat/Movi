# Previsioni dell'arbitro, verdetto dell'estensione f7 (fase f5)

Scritte alle 2026-11-14T17:27:15+01:00 (`date -Is`), **prima** di ogni riconteggio, rilancio o conto mio. Non sono cieche: ho già letto il contratto dell'estensione, gli addendum, `13-soluzione/DECISIONE.md`, `14-attacco/CONTROPROVE_DECISIONE.md`, `15-verifica/VERIFICA_DECISIONE.md`, `11-torneo/TORNEO.md`, `10-triage/TRIAGE.md`, il verdetto del nucleo e l'attacco alla specializzazione. Non ho ancora aperto nessun `risultati_*.txt` né lanciato niente.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| PA1 | Le cifre che porterò nel verdetto, prese da torneo, attacco e verifica, tornano dai file `risultati_*.txt` | riconteggio con `grep` e script miei, almeno 25 cifre | più di 2 cifre che non tornano (oltre alle 2 già segnalate dalla verifica: «438 → 0» e «2,46 MB per tre fotogrammi») |
| PA2 | «438 → 0» non torna: il file dà N1 = 14 (come dice la verifica), non 0 | `11-torneo/risultati_a5.txt` | il file dà 0 |
| PA3 | Il rilancio di `15-verifica/vq3c.c` (compilato in una cartella mia) ridà gli stessi conteggi di `risultati_vq3c.txt`: 0 punti profondi per Q3c in tutte le condizioni; 58 fotogrammi su 90 per N1; mediana 1,4 m per VB7 | diff dei conteggi (non dei tempi) | un conteggio diverso |
| PA4 | Il rilancio di `14-attacco/rifai.sh` NON lo faccio se scrive nella cartella dell'avversario; se riesco a lanciare i suoi script con uscita nella mia cartella, AV10 ridà 0 celle in 16 combinazioni e AV4 0 fotogrammi su 10 | conteggi | un conteggio diverso |
| PA5 | Il conto delle ore dell'avversario (AV7: 1,5–4,0 ore-persona restanti con 5 persone) è rifacibile dai numeri scritti nei file (70 ore-persona, 35 in fila B2…B8, 2 h 40 in due per l'accettazione, aggiunte f7 8–10,5): il mio conto dà un margine fra 0 e 6 ore-persona con 5 persone e negativo con 4 e con 3 | conto mio (`conti_arbitro.py`) | margine con 5 persone sopra 8 ore-persona, o positivo con 4 |
| PA6 | La durata dell'occlusione completa col pannello largo 1 m a 1,7–1,9 m e attore a 2,3 m è sotto 1 s a 1,0 m/s (la verifica dice 0,83 s) | conto geometrico mio | oltre 1,2 s |
| PA7 | Il tetto del campo a distanza d è 1,2 + 0,25·d (camera a 1,2 m, 15° in giù, 58° verticali): a 2,3 m dà 1,77–1,78 m; a 1,7–1,9 m dà 1,62–1,68 m | conto mio | scarto oltre 3 cm |
| PA8 | In `prepropostaEsterna.md` S10 nomina le tre fasce 0,15–0,60 / 0,60–1,60 / oltre 1,60 m e la soglia di 45 ms; S11 nomina otto stati fra cui la sosta in ombra | `grep` | una delle due assente |
| PA9 | Nella traccia (`regole_challenge.md`) non compaiono «uncrewed», «drone», «UAV», «voxel», «3D» | `grep -ci` | una occorrenza |
| PA10 | Nessuno dei file f7 che cito contiene una misura su fotogrammi veri (tutte le prove sono simulazione o conto) | `grep` di «nessun fotogramma vero» o equivalente nelle intestazioni di 11, 13, 14, 15 | una prova su camera vera |

Esiti: in coda a questo file, dopo le prove, con l'ora.
