# Previsioni dell'arbitro (triage f7) — scritte PRIMA di leggere le otto consegne

Ora di scrittura: 2026-11-14T15:42:18+01:00. A quest'ora ho letto solo: la consegna, la traccia, il contratto dell'estensione, gli addendum, promptMare.txt. Non ho ancora aperto nessuna CONSEGNA.md né i loro risultati.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| P1 | Le otto consegne ci sono, cominciano con il canarino della propria corsia e nessun canarino compare nei file dell'altra corsia. | `head -1` di ogni CONSEGNA.md; `grep -rl` dei due canarini sulle otto cartelle. | Una consegna mancante, una prima riga diversa, o un solo file con il canarino dell'altra corsia. |
| P2 | La regione 6 × 4 × 3 m ha 72 000 voxel a 0,10 m e 576 000 a 0,05 m (calcolo a mano: 60·40·30 e 120·80·60). I ruoli che danno il conteggio alla stessa risoluzione danno questi numeri. | Conteggi nei file dei ruoli, ricalcolati da me. | Un ruolo che dà un numero diverso per la stessa regione e la stessa risoluzione senza dichiarare una regione diversa. |
| P3 | Le misure del costo del lancio dei raggi di «ottimizzazione» e di «tempo-reale» divergono di oltre un fattore due su almeno una configurazione confrontabile (stessa risoluzione, stessa struttura). | Rapporto fra i tempi per ciclo riportati nei due file di risultati, a parità dichiarata di risoluzione e di struttura. | Tutte le coppie confrontabili entro un fattore due. |
| P4 | Almeno una contraddizione fra corsia A e corsia B sulla necessità della mappa voxel (la B, con il rovesciatore, dice «non necessaria»; almeno un ruolo della A dice «sì condizionato»). | Lettura delle decisioni proposte nelle otto consegne. | Tutte e otto le consegne propongono la stessa decisione per Q1. |
| P5 | Almeno due ruoli hanno proposto in modo indipendente le fasce di quota per cella; nessuno ha provato esattamente le tre fasce di S10 (0,15–0,60; 0,60–1,60; oltre 1,60 m), perché il quinto addendum è arrivato dopo. | Ricerca di «fasc», «2,5D», «colonn» nelle consegne e nei sorgenti. | Meno di due ruoli, oppure un ruolo con le soglie esatte di S10 provate. |
| P6 | Rifacendo un conteggio deterministico di almeno due ruoli con il loro comando, i numeri tornano identici; i tempi tornano entro un fattore due. | Rilancio dei comandi «per rifare» (al più due minuti l'uno, uno alla volta). | Un conteggio deterministico diverso, o un tempo oltre il fattore due. |
| P7 | Nessun ruolo dichiara il vetro risolto e nessun ruolo dichiara provata la piattaforma in moto. | Lettura. | Una consegna che lo dichiara. |

Esiti: in fondo a questo file, dopo le prove, in una sezione separata «Dopo».

---

## Seconda tornata — scritta alle 2026-11-14T15:51:47+01:00, DOPO la lettura delle otto consegne e PRIMA di ogni mio rilancio

Nota di provenienza. La tabella P1–P7 qui sopra era già in questa cartella quando ho cominciato (inizio di questa sessione: 2026-11-14T15:47:33+01:00; il file porta la data 15:42): l'ha scritta un lancio precedente dello stesso ruolo, che non ha lasciato altro. Io l'ho letta prima di aprire le consegne e la adotto senza cambiarla; non posso però certificare di persona che cosa quel lancio avesse già letto. P1–P5 e P7 si decidono per lettura; P6 con i rilanci qui sotto.

Le previsioni A1–A8 le scrivo sapendo già che cosa dicono le consegne (non sono cieche rispetto ai testi), ma senza aver rilanciato nessun programma né ricalcolato niente dai file dei risultati, salvo due divisioni a mente dichiarate in A1.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| A1 | Fra «ottimizzazione» e «tempo-reale» nessuna coppia DAVVERO confrontabile (stessa struttura, stessa risoluzione, stessi raggi liberi, stessa regola sui colpi) diverge oltre un fattore due. La coppia «19 200 raggi a 10 cm» (2,79 contro 5,5 ms: 1,97) non è confrontabile perché il banco di «tempo-reale» tratta comunque i colpi a piena risoluzione (campo colpi/fot=68722 anche con k=4). Tolto quel costo fisso, il costo per passo di raggio dei due banchi a 5 cm sta entro 1,3 volte. (Già fatto a mente prima di scrivere: 5,23 ms / 1,9 M passi e (8,0 − 3,69) ms / 1,56 M passi.) | Script mio `confronto.py` sui file `risultati_*.txt` dei due ruoli. | Una coppia confrontabile oltre 2; oppure costo per passo oltre 1,3 volte. |
| A2 | Ricompilando nella MIA cartella i due `banco.c` e rilanciando, i conteggi deterministici tornano identici ai file: blocchi 116 (10 cm) e 736 (5 cm) nella scena vuota in entrambi; somma di controllo `db445d28f708d362` per densa e hash a 10 cm, scena rada, 160×120 («ottimizzazione»); passi/fot=33310236 per D 5 cm k=1 («tempo-reale»). I tempi tornano entro un fattore due. | Rilancio, uno alla volta, `timeout 120`. | Un conteggio diverso; un tempo oltre 2 volte. |
| A3 | `verifica_strati.py` (matematico), lancio senza argomenti: 0 falsi liberi per la regola Π e 138 230 celle-fotogramma per la griglia di Bayes, 45 829 per la regola nucleo-simile. | Rilancio (18 s dichiarati). | Una cifra diversa. |
| A4 | `eventi.py` (requisiti): 0 «osservato» a soggetto nascosto e 0 uscite false; braccio ingenuo fallito 200 su 200; B1 con 103 scene su 200. | Rilancio. | Una cifra diversa. |
| A5 | `sim3d scene` (nuvole-punti) ricompilato: stesse cifre di `risultati_scene.txt` salvo le righe dei tempi. `rovescia analisi` (rovesciatore): identico a `risultati_analisi.txt`. | `diff`. | Una riga non di tempo diversa. |
| A6 | Nessun sorgente delle otto cartelle prova le soglie esatte di S10 (0,15 / 0,60 / 1,60 m). | `grep` di 0.60 e 1.60 (e 0,60 / 1,60) nei sorgenti e nelle consegne. | Un sorgente con quelle soglie come fasce di quota. |
| A7 | Calcolo a mano sulle tre fasce di S10 con il montaggio del nucleo (1,2 m, 15° in basso, 58° verticali: bordo alto a +14°, bordo basso a −44°): la fascia media (fino a 1,60 m) è vista per intero solo da 1,60 m di distanza; la fascia alta, se ha un tetto a 2,0 m, solo da 3,21 m, cioè MAI dentro la griglia di 3 m; la quota 0,15 m è vista da 1,09 m. Quindi S10 alla lettera («libero solo se tutte le fasce pertinenti sono osservate e libere»), con la fascia alta pertinente, dà zero celle «libero» entro 3 m con il montaggio orizzontale. Le misure dei ruoli sulla colonna intera (ottimizzazione: 0–3 caselle su 270; creativo: 7 celle su 570) sono coerenti. | Conto in `confronto.py` (tangenti) e ricerca delle due cifre nei file. | Distanze diverse di oltre 2 cm; oppure un file dei ruoli che mostra più del 5 % di celle con la colonna 0,1–2 m vista per intero entro 3 m con montaggio orizzontale. |
| A8 | Nella traccia (`regole_challenge.md`) le radici uncrewed, drone, UAV, veicol, volo, voxel, 3D compaiono 0 volte; in `promptMare.txt` «UAV» o «drone» compaiono 12 volte. | `grep -ci` / `grep -oi | wc -l`. | Un conteggio diverso. |

---

## Dopo (esiti, scritti alle 2026-11-14T15:59:57+01:00)

| # | Esito | Prova |
|---|---|---|
| P1 | **regge** | Otto consegne presenti; prima riga: canarino A in 01–06, canarino B in 07–08; `grep -rl` del canarino A in 07 e 08: nessun file; del canarino B in 01–06: nessun file; in tutto 6 + 2 occorrenze, solo nelle otto `CONSEGNA.md`. |
| P2 | **regge** | 72 000 e 576 000 in matematico, ottimizzazione, tempo-reale, esperto-dominio, rovesciatore; 576 000 in nuvole-punti e creativo; `confronto.py` (3). La memoria cambia solo con i byte per voxel dichiarati (1, 2, 4, 8, 12). |
| P3 | **smentita** | Coppie confrontabili (tutti i 307 200 raggi): 1,16 (densa 5 cm), 1,27 (densa 10 cm), 1,44 (hash 5 cm), 1,57 (hash 10 cm). Nessuna oltre due. La coppia a 1,95 (19 200 raggi liberi, 10 cm) non è confrontabile: vedi A1. |
| P4 | **regge alla lettera**, ma la sostanza converge | «SÌ condizionato» a uno strato denso in affiancamento (ottimizzazione, esperto-dominio) contro «NO per la prima demo» (nuvole-punti, creativo) e «SÌ condizionato alla sola lettura 3D» (rovesciatore). Nessuno degli otto sostiene la mappa sparsa e probabilistica come garanzia. |
| P5 | **regge** | Fasce o profilo di quota proposti da ottimizzazione (D), nuvole-punti (B4, B8, P), rovesciatore (fasce da 5 cm lette), creativo (sagoma). Nessuno con le soglie di S10 (A6). |
| P6 | **regge** | Sette ruoli rifatti (tutti salvo creativo): conteggi identici; tempi entro 1,44 volte (il caso più largo: DDA V5 di nuvole-punti, 214–227 ms contro 307 del file). File in `rifatti/`. |
| P7 | **regge** | Vetro «non risolto» o «non provato» in matematico, nuvole-punti, esperto-dominio, rovesciatore, creativo; nessuna consegna dichiara provata la piattaforma in moto. |
| A1 | **regge** | `confronto.txt` (1c, 1d): costo per passo 2,76 ns (ottimizzazione) contro 2,77 marginali (tempo-reale) a 5 cm, 2,93 contro 3,14 a 10 cm; costo fisso dei colpi a piena risoluzione 2,2–2,3 ms. |
| A2 | **regge** | `rifatti/rifatto_ott.txt`: somma db445d28f708d362 (densa e hash, 10 cm), blocchi 116 e 736, tempi 2,81 / 3,40 / 5,31 / 7,11 ms contro 2,79 / 3,37 / 5,23 / 7,03; tetto: caselle occupate 21 e 29, libere 0. `rifatti/rifatto_tr.txt`: passi 33 310 236, 88,96 ms contro 88,53; 5,46 contro 5,43. Nota: il primo tentativo (15:52:35) ha passato gli argomenti come uno solo, nessuna misura. |
| A3 | **regge** | `rifatti/rifatto_matematico.txt` identico a `risultati.txt` (diff vuoto): Π 0; nucleo-simile 45 829; Bayes 138 230. |
| A4 | **regge** | `rifatti/rifatto_requisiti.txt`: stesse cifre; `diff_requisiti.txt` mostra solo l'ordine delle chiavi in tre righe (insiemi non ordinati). |
| A5 | **regge** | `diff_nuvole.txt`: solo le righe dei tempi (e una riga d'intestazione); `diff_rov.txt`: vuoto. |
| A6 | **regge** | `grep -E '0[.,]60|1[.,]60'` nei sorgenti e nelle consegne: solo coordinate di una barra, un conteggio di voxel, 0,59–0,60 ms. |
| A7 | **regge** (calcolo; non è una misura di S10) | `confronto.txt` (2): 1,60 m visto da 1,60 m; 2,00 m da 3,21 m; 0,15 m da 1,09 m. Colonna intera entro 3 m: 0–3 caselle su 270 (ottimizzazione), 7 celle su 570 (creativo), nessuna (rovesciatore). |
| A8 | **regge** | 0 per le sette radici nella traccia; 12 occorrenze di UAV o drone in `promptMare.txt`. |

**Notato dopo, senza previsione.** (1) `risultati_scene.txt` di nuvole-punti contiene anche la variante **B4** (quattro fasce da 0,5 m), non riportata nella sua consegna: libero a torto 0 litri nelle cinque scene, nascosto a torto 0–384 litri, resa 71,1–78,2 % (B8: 83,7–88,4 %). È la misura più vicina alle tre fasce di S10. (2) Lo stesso file dà il costo della costruzione delle fasce B4 + B8: 121–140 ms (11 655 420 visite), non riportato nella consegna; ottimizzazione misura per la sua struttura a colonne di bit 1,66 ms con 19 200 raggi e 26,0 con 307 200. (3) I banchi «diretti» costano 4,9–7,7 ns per passo di raggio (nuvole-punti, esperto-dominio, rovesciatore), quelli di ottimizzazione e tempo-reale 2,5–3,1: stessa macchina, oltre il fattore due. (4) Il sovraccosto dell'hash per passo è 0,16–0,55 ns (rovesciatore), 0,16–0,52 (ottimizzazione), 0,94–1,32 (tempo-reale): il disaccordo sui rapporti (1,03–1,13 contro 1,2–1,5) viene dalla base diversa.
