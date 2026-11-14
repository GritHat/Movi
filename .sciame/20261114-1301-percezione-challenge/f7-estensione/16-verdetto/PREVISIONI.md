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

## Esiti (scritti alle 2026-11-14T17:43:20+01:00, dopo le prove)

| # | Esito | Prova |
|---|---|---|
| PA1 | **regge**: 66 controlli (ciascuno su una o più cifre) su 66 tornano dai file dei risultati; oltre a questi restano sbagliate in `DECISIONE.md` le due cifre già segnalate dalla verifica | `python3 -I -B riconta_arbitro.py` → `riconta_arbitro.txt` |
| PA2 | **regge**: `risultati_a5.txt` dà N0 = 438 e N1 = 14 al fotogramma 60, con 13 al fotogramma 59 | stesso script |
| PA3 | **regge**: uscita identica riga per riga (202 righe; 7,4 s) | `gcc -O2 -o rifatti/vq3c ../15-verifica/vq3c.c -lm && (cd rifatti && timeout 120 ./vq3c > rifatto_vq3c.txt)`; `diff` vuoto. Stesso codice: copre solo la trascrizione |
| PA4 | **regge**: `av10.py` e `av4.py` lanciati con `python3 -I -B` e uscita nella mia cartella: `diff` vuoto con i file dell'avversario (16 righe con 0 celle; 0 su 10 per la regola scritta) | `rifatti/rifatto_av10.txt`, `rifatti/rifatto_av4.txt`. Niente scritto nella cartella dell'avversario |
| PA5 | **regge**: con 5 persone 1,5–4,0 ore-persona (conto dell'avversario, rifatto), 6,5–8,0 nella mia variante; con 4 da −2,0 a −9,8; con 3 da −16,0 a −21,2. Il conto «semplice» della decisione (9,5–12) torna anch'esso: i due conti differiscono per l'ipotesi sul calendario, non per un errore | `conti_arbitro.txt`. Le ore sono stime altrui, non verificate |
| PA6 | **regge**: 0,76–0,90 s a 1,0 m/s (0,54–0,64 s a 1,4 m/s), secondo la distanza del pannello (1,7–1,9 m) | `conti_arbitro.txt` |
| PA7 | **regge**: il tetto è 1,2 + 0,2493·d; a 2,3 m 1,773 m (previsto 1,77–1,78); a 1,7–1,9 m 1,624–1,674 m (previsto 1,62–1,68: dentro) | `conti_arbitro.txt` |
| PA8 | **regge**: le tre fasce, la soglia di 45 ms e `SOSTA_IN_OMBRA` sono nel file; in più, notato dopo: la riga 18 dà 30 ms e scrive «ostacoli bassi (< 1,1 m)», che conferma l'errore di lettura distanza/altezza | `grep` su `prepropostaEsterna.md` |
| PA9 | **regge**: 0 occorrenze di uncrewed, drone, UAV, voxel, 3D, veicol, volo | `grep -ci` su `regole_challenge.md` |
| PA10 | **regge**: torneo, decisione, attacco e verifica dichiarano in testa «simulazione» e «nessun fotogramma vero»; il banco dichiara «non la scheda di bordo» | `grep` sulle intestazioni |

**Notato dopo, senza previsione.** (1) Nel file della verifica, con chiazze al 30 % l'«impronta del suolo» (V-018) scende a una mediana di 1,5 m per settore e a 4,55 cambi al secondo: la verifica riporta solo il caso sparso. (2) «Tre fotogrammi, 2,46 MB»: `12-prestazioni/banco.c`, riga 325, alloca quattro piani a 16 bit di 640 × 480 (2 457 600 byte). (3) Un comando di shell ha stampato un errore innocuo (`echo ====` in zsh); nessun effetto sui file.

**Lunghezza del verdetto.** Quattro pagine: `pandoc VERDETTO_ESTENSIONE.md -o x.pdf --pdf-engine=xelatex -V geometry:a4paper,margin=1.8cm -V fontsize=10pt` (PDF scritto nella cartella temporanea della sessione, non nel progetto).
