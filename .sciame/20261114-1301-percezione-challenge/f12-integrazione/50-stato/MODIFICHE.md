# Modifiche alla versione 3 di `STATO_PROGETTO.md` — f12, `50-stato` (`sciame-redattore`)

Lavoro dalle 2026-11-14T19:20:07+01:00 alle 2026-11-14T19:40:22+01:00 (`date -Is`). File consegnato: `f12-integrazione/50-stato/STATO_PROGETTO.md` (2 387 righe, circa 78 000 parole; la versione 2 ne aveva 1 692 e circa 51 000). Accanto: `PREVISIONI.md` (19:20:52, prima della stesura e dei controlli), `STATO_V2_copia.md` (la copia della versione 2 su cui ho lavorato), `frammenti_1.md` e `frammenti_2.md` (tutto il testo nuovo), `componi_v3.py` (applica i frammenti alla copia: ogni punto d'innesto deve comparire una volta sola, altrimenti si ferma), `controlla.py` e `esito_controlli.txt`. Si rifà con `python3 -I -B componi_v3.py && python3 -I -B controlla.py`. L'originale `documentazione/STATO_PROGETTO.md` non è toccato.

## 0. In testa: cambi di stato, regole violate, scostamenti

- **Cambi di stato proposti da me: nessuno.** Non ho eseguito simulazioni né ricontato cifre. Ogni stato è quello dei sei verdetti dell'arbitro; ogni cifra nuova viene dal file citato. Niente è diventato «validato».
- **Scostamento principale dalla consegna.** Letti **per intero**: contratto d'integrazione, verdetto d'integrazione, chiusura, V7, V8, VD, soluzione versione 3 finale, blocco di classificazione, discordanze dei fascicoli, piano finale, nono e decimo addendum. Letti **solo in testa** (cambi di stato e scostamenti): prova d'insieme, «libero» della cella, identità su profondità, controprova, attacco alla versione 3, completezza, piano rifatto, controllo statistico, schermo finale (testa e §1), attacco alla classificazione, contratto di f14, il §2 delle correzioni di f11. **Non aperti:** `PROFILI.md`, `USO_DELLA_CLASSE.md`, `CLASSIFICATORE.md`, i sei fascicoli di f13, i file citati da V7 e V8, la tabella delle correzioni della versione 3; non riaperti VN, V9, l'audit, f6, la versione 2 della soluzione (già fonti della versione 2 di questo documento). Le cifre dei file non letti per intero passano per il verdetto d'integrazione e per la versione 3, che li citano riga per riga: un errore di trascrizione di quei due file passerebbe anche qui.
- **Il testo ereditato non è riscritto riga per riga.** Ogni paragrafo toccato ha in testa un riquadro «Versione 3» (regola, parametri, stato della prova, limiti, che cosa è superato); il testo della versione 2 resta sotto. È la via che conserva tutto il contenuto ancora vero, ma chi legge un blocco deve leggere prima il riquadro. Le tabelle del §4.2 (56 righe) e dell'appendice B non sono aggiornate riga per riga: le correzioni stanno nel §4.7 e in «fonti nuove da registrare».
- **Regole.** Scritto solo in questa cartella. Niente git, niente sudo, niente rete. Usato il `python3` di sistema (sola libreria standard: numpy non serve) e, per quattro ritocchi ai miei frammenti, `sed` e uno script. Previsioni scritte prima, non cieche rispetto ai testi letti. Tempo: circa 20 minuti sui 40.
- **Regola dell'ambiente non seguita, per scelta:** l'ambiente sconsiglia i file di rapporto; la consegna chiede questo file e `PREVISIONI.md`, e ho seguito la consegna.

## 1. Che cosa ho cambiato, capitolo per capitolo

| Dove | Che cosa |
|---|---|
| Testa | riga della versione; il riquadro «niente è provato sull'hardware» riscritto (la frase «nessun fotogramma di una camera vera…» non era più vera alla lettera dopo f10: ora «di una camera della squadra», con la frase vecchia citata come superata); «che cosa fotografa» e «che cosa ho letto»; i due riquadri della versione 2 ridotti a tre righe «superato da …», conservando i punti su f9 e f11; regola 6 aggiunta a «come si aggiorna» |
| Sintesi | riscritta: sistema, **stato in dieci righe**, stabilito, aperto, prossima prova, decisioni; in coda il riquadro con i cambi rispetto alla sintesi della versione 2 |
| Legenda | marca [prel.] ridefinita; marche nuove [f12] e [ric.]; paragrafo delle sigle nate dopo la versione 2; quattro omonimi nuovi |
| Indice | riscritto |
| Cap. 1 | riquadri nei §1.1, §1.2, §1.3 (tabella dello stato di R1–R8), §1.4; stato «chiusa» nelle righe 3, 4, 5, 7 della tabella degli addendum; righe 9 e 10 nuove; tre celle del §1.5 estese |
| Cap. 2 | titolo; riquadro d'apertura; schema della versione 3 e tabella B1–B11 ↔ blocchi 1.1–1.13; un riquadro «Versione 3» per ciascuno di B1–B9; B6 rinominato «Classificazione e profili»; blocchi nuovi B10 (registro degli eventi) e B11 (misura della precisione sul posto); §2.3 con i venti invarianti; §2.4 con le diciotto condizioni e la tabella «le nove condizioni del nucleo, com'erano e come sono» |
| Cap. 3 | nota nel §3.1; §3.10 nuovo (geometria corretta, sensore simulato, tabella per l'inventario, tre prime misure, che cosa la squadra ha già) |
| Cap. 4 | §4.1.10–§4.1.16 nuovi (f7, f8, f10, prove di f12, f13, f14, riconteggi dell'arbitro); note nei §4.2, §4.3, §4.5; §4.6 (41 cifre nuove con file, numerosità, intervallo, stato); §4.7 (20 cifre corrette dai fascicoli); §4.8 (contraddizioni, ipotesi e previsioni alla chiusura) |
| Cap. 5 | titolo da «valutazioni in corso» a «valutazioni chiuse»; §5.0 (esiti in una tabella); riquadri d'esito nei §5.2, §5.3, §5.4, §5.5; §5.6 riscritto (sette controlli, dodici cambi di stato, chiusura); §5.7 riscritto; §5.8 (f13) e §5.9 (f14) nuovi |
| Cap. 6 | riquadro d'apertura; §6.1 rinominato; aggiornamento del registro dei rischi con nove rischi nuovi (15–23); §6.3 nuovo, il piano finale |
| Cap. 7 | sei decisioni aperte alla chiusura (I–VI); tabella «che ne è delle undici decisioni» |
| Cap. 8 | §8.10 nuovo (tre assi, profili, frase della prova, classi e dominio, portatori, frasi da dire e da non dire, norme) |
| Cap. 9 | otto righe nuove nella cronologia |
| Cap. 10 | §10.3 nuovo (stato dei sei riquadri, dei punti non applicati di f11, sei discordanze nuove) |
| Glossario | 17 voci nuove; 13 voci della versione 2 estese con «Versione 3: …»; ordine alfabetico rifatto |
| Registro | nove righe, 3 (a)–3 (i), una per valutazione integrata; riga 4 «da scrivere» |
| Appendici | A: file letti per la versione 3; B: undici fonti nuove con chiave provvisoria `[red3-…]` e le fonti da cercare; C: provenienza e controlli della versione 3 |

I cambi di stato per esteso («da … a …», con il file) stanno nei riquadri e, raccolti, nel registro delle modifiche (righe 3 (a)–(i)) e nel §5.6.

## 2. Critiche e dubbi di contenuto per gli autori (non corretti da me: non cambio le affermazioni)

1. **Due diciture per la stessa cifra.** Pannello da 1 m: «almeno 87 su 100 a 1 s» (verdetto d'integrazione, condizione 11; versione 3, §1.6) e «circa 9 su 10 a 1 secondo (limite 0,87)» (frase della prova, versione 3, §3). Prova: ricerca delle due stringhe nei due file. Ne serve una.
2. **Larghezza del pannello.** La versione 3 scrive 1 m per la demo (§7); il piano chiede 2 m se arriva un sensore (§6). Nel documento l'ho messa fra le decisioni dell'utente (VI) e fra le discordanze (§10.3).
3. **Due margini.** Le discordanze dei fascicoli dicono che C = 0,85 m da norma non è citabile; il blocco di classificazione usa C = 0,95 m «già consegnato nel fascicolo di geometria». Non ho aperto il fascicolo: la relazione fra i due valori è **non verificata**.
4. **«1,69 m a ±44°»** resta scritto nel verdetto dei dati (F-413); col campo di 58° il fascicolo di geometria dà 1,71–1,73 m. Ho riportato entrambe con la condizione.
5. **Il blocco di classificazione non è fuso** nei testi della versione 3, del piano e dello schermo (K-515): la versione 3 dice ancora che la rete è facoltativa e il piano la mette al taglio 1. Nel documento vale il blocco, come chiede il coordinatore.
6. **Il copione dello schermo** dice «9 su 10 fino a 2 secondi» senza «bordo noto» e «sul proprio percorso» (verdetto d'integrazione, C-G): riportato, non corretto.
7. **Limiti peggiori della precisione:** il verdetto d'integrazione dà due coppie (0,955 e 0,921 fino a 2 s; 0,936 e 0,899 a 3 s), la versione 3 «0,921 e 0,899». Ho scritto i due peggiori, come la versione 3; chi vuole le due geometrie le trova nel verdetto.
8. **Il PDF** scrive ancora «pannello alto almeno 1,5 m»? Non verificato: non ho letto il PDF né la nuova stesura delle due pagine (solo l'intestazione).

## 3. Stati che propongo

Nessuno nuovo. Per il documento: «versione 3 consegnata; non riletta da un secondo ruolo».

## 4. Proposte

- **redattore-1.** *Meccanismo:* alla prossima versione fondere riquadro e testo ereditato, blocco per blocco, partendo da B5 e B2, e rifare il §4.2 riga per riga con una colonna «stato alla versione N». *Previsione:* il documento scende sotto 60 000 parole senza perdere cifre. *La smentisce:* un numero distinto della versione 3 assente nella versione 4 senza una riga «superato da».
- **redattore-2.** *Meccanismo:* una verifica avversaria di questa versione, come le tre di f11, su un campione di 60 cifre nuove contro i file grezzi. *Previsione:* almeno 57 su 60 coincidono. *La smentisce:* 4 o più cifre diverse.

## 5. Esiti delle previsioni (`PREVISIONI.md`; uscita in `esito_controlli.txt`)

| # | Esito | Misura |
|---|---|---|
| R1, percorsi | **regge** | 1 428 citazioni di percorsi; 0 percorsi nuovi mancanti. Restano 28 nomi con cartella relativa già presenti nella versione 2 (per esempio `sez-a/SEZIONE.md`, relativo a `f11-documentazione/`): seguono la convenzione della legenda, non li ho toccati |
| R2, tabelle | **regge** | 76 tabelle, 0 con colonne diverse o senza riga di separazione |
| R3, contenuto non tolto | **smentita com'era scritta** | 79 righe della versione 2 non compaiono identiche (soglia: 60). *Notato dopo, con una misura aggiunta:* 25 sono righe estese in coda (il testo c'è ancora), 54 sono tolte o riscritte: testa, sintesi, indice, legenda, titoli, §5.6, §5.7, riga 3 del registro. Per ognuna c'è il testo nuovo o una riga «superato da …» |
| R4, frasi da non dire | **regge** | 10 righe con «validat», «via libera», «garantit» fuori da virgolette, lette una per una: 6 sono negazioni («non come sistema validato», «nessuna ipotesi è validata», «non garantiti dalla sola regola»), 3 sono testo ereditato su altro (semafori acustici, un'autorizzazione societaria, «invalidato»), 1 è la negazione ripetuta nel §5.8. Nessun uso affermativo |
| R5, ingressi citati | **regge** | 38 percorsi d'ingresso della consegna, 0 non citati |

*Indipendenza dei controlli:* il programma è mio e controlla solo la forma (percorsi, tabelle, righe, parole); non dice niente sulla correttezza delle cifre.

## 6. Che cosa propongo dopo

Una rilettura da parte di un ruolo diverso (lettore critico) dei riquadri «Versione 3» di B2 e B5 e del §4.6 contro i file grezzi; la registrazione delle undici fonti nuove nell'elenco dei riferimenti; la copia di questo file in `documentazione/`, che spetta al coordinatore.
