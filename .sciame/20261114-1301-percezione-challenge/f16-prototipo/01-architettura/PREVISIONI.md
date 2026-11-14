# PREVISIONI — sciame-architetto, f16-prototipo/01-architettura

Scritte alle 2026-11-15T00:02:02+01:00 (da `date -Is`), PRIMA di copiare il codice e di lanciare qualsiasi prova.
Nota sull'ora: la consegna dice «oggi è il 14 novembre 2026»; l'orologio della macchina segna già il 15 (dopo mezzanotte).

Tutto è simulazione: nessuna di queste prove tocca un sensore fisico; nessuna rende «validato» alcunché.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| arch-P1 | La catena con le correzioni (f12/06-identita/catena), copiata senza modifiche in `prototipo/movi/riuso/catena`, passa le sue prove dal nuovo posto. | `python -I -B prove.py` nella copia: codice d'uscita e confronto con `esito_prove.txt` dell'origine | Smentita se il codice d'uscita non è 0, o se una riga diversa dai tempi (P16) differisce dall'originale |
| arch-P2 | Lo scheletro del pacchetto si importa tutto e la riga di comando risponde. | `python -I -m movi --help` e importazione di ogni modulo `movi.*` | Smentita se un modulo non si importa o l'uscita non è 0 |
| arch-P3 | Il banco in C del predittore (insieme.c) si compila nella copia e gira da solo, senza file di taratura esterni. | `gcc -O2 … -lm` e `timeout 60 ./insieme prova geo=T n=40 …` | Smentita se non compila, se esce ≠ 0 o se supera 60 s |
| arch-P4 | Il formato unico del registro basta al modo a corto raggio: ogni riga d'uscita della catena su una sequenza simulata con persona e pannello si converte e supera la validazione dello schema. | sequenza `d435i_nom__pannello_a12__s00`: righe non valide su N | Smentita se anche una sola riga non è valida (k > 0 su N); con 0 su N riporto il limite superiore di Wilson al 95 % |
| arch-P5 | Il nucleo del predittore da portare in Python (mpos, pred_init, smooth, hdr, pred_step di insieme.c) sta sotto le 150 righe di C: il porto è fattibile da uno sviluppatore in meno di un'ora. | conteggio delle righe fra «sd-1» e `dist_reg` in insieme.c | Smentita se ≥ 150 righe (allora: chiamare il C come processo) |
| arch-P6 | `sh prova_tutto.sh` nello stato di scheletro (prove del codice riusato + convalida del registro) finisce in meno di 5 minuti. | `time` | Smentita se ≥ 300 s |

Indipendenza: le prove P1 e P3 condividono con ciò che controllano il codice e l'autore originale (sono le prove di chi l'ha scritto): mostrano solo che la copia non ha rotto niente. P4 condivide con lo schema l'autore (io): trova gli errori di forma, non quelli di significato.

## Esiti (scritti DOPO le prove, 15-11-2026, fra le 00:06 e le 00:09)

Comando unico: `cd prototipo && sh prova_tutto.sh` (uscite in `prototipo/uscite/*.txt`); per P4 anche
`python -I -B prove/prova_registro.py <sequenza>` su altre quattro sequenze.

| # | Esito | Prova |
|---|---|---|
| arch-P1 | **Non risolta al primo lancio, regge al secondo e al terzo.** Primo lancio: uscita 1, fallisce la sola `test_p16_costo` (prova di tempo: p95 19,71 ms). Nello stesso minuto la stessa prova fallisce anche sull'ORIGINALE lanciato sul posto (uscita 1, p95 6,02 ms) con il carico della macchina a 28 (`uptime`): è il carico, non la copia. Secondo e terzo lancio: 25 prove, OK, uscita 0; le righe diverse dall'originale sono solo i tempi (P14, P16) e le due righe d'intestazione. | `uscite/01_prove_catena.txt`; `diff` con `riuso/catena/esito_prove.txt` |
| arch-P2 | **Smentita al primo lancio, poi corretta.** Con `-I` la cartella corrente non è nel percorso: `python -I -m movi` dà «No module named movi». Correzione: lanciatore `movi.sh` che aggiunge la cartella in modo esplicito. Dopo: 15 moduli importati, uscita 0. | `uscite/03_importa.txt` |
| arch-P3 | **Regge.** Compila senza errori; `insieme prova geo=T n=40 beh=01236 …` finisce (tutto `prova_tutto.sh`: 20–27 s). Nessun file esterno richiesto. | `uscite/02_banco_c.txt` |
| arch-P4 | **Smentita al primo lancio (difetto dell'adattatore, non dello schema), poi regge.** Primo lancio: `KeyError: 'affidabilita_persa'`: la catena ha uno stato di traccia che non avevo letto (`inseguimento.py` riga 218). Aggiunto alla tabella degli stati (→ «previsto ampio»). Dopo: righe non valide 0 su 47 (Wilson 95 %: 0–7,6 %) su `pannello_a12__s00`; 0 su 30, 0 su 80, 0 su 45, 0 su 84 sulle altre quattro (in tutto 0 su 286: 0–1,3 %). | `uscite/04_registro_corto.txt`, `uscite/05_convalida.txt` |
| arch-P5 | **Regge.** 43 righe di C (righe 162–205 di `insieme.c`); in più servono `traj` e `build_lib` (righe 100–142 e 299–304) per la libreria dei percorsi. | `awk` sul file |
| arch-P6 | **Regge nello stato di scheletro.** 27 s, 20 s, 24 s nei tre lanci. Con le scene costruite il tempo va rimisurato. | `time sh prova_tutto.sh` |

## Notato DOPO, non previsto

1. **Senza le correzioni di f12 il pavimento vuoto simulato genera tracce fantasma**: su `d435i_nom__pavimento_vuoto` (30 fotogrammi) 66 nascite e 28 conferme con `Parametri()` di base; 0 nascite e 0 avvisi con i sette campi «correzioni f12» accesi. Per questo `correzioni_f12` parte ACCESO nel prototipo. (Un lancio per braccio: è un'osservazione, non una frequenza.)
2. **Su `pannello_a12__s00` con le correzioni accese non c'è nessun evento «riaggancio»**: la persona che ricompare nasce come traccia nuova con 8 eventi «identità ambigua». La scena «passa dietro e ricompare» oggi mostrerebbe «identità ambigua», non «ricomparso · identità presunta». Un riaggancio si vede senza correzioni su `cassa_persona__s00` (1 evento). Da decidere da chi costruisce: quale sequenza e quali regole per la scena, senza ritoccare il risultato.
3. La consegna dava `f15-lunga-portata/03-scenari/scenari.json` come «in arrivo»: alle 00:05 c'era già (scenari A1, A2, A3, A4 «solo analisi», S1, S2) e c'era `04-moto/movi_lp.py` (596 righe). Sono file ancora in lavorazione di altri ruoli: letti come dati, da rileggere.
