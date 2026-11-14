# Contratto dell'estensione f10 — validazione su dati pubblici di sensori veri e su hardware simulato

Estensione della convocazione «percezione-challenge», aperta il 14 novembre 2026 dopo il settimo addendum dell'utente (`../ADDENDUM_UTENTE.md`: leggilo, con il quarto e il sesto). Restano validi il contratto originale (`../CONTRATTO.md`), i principi conservati e l'imperativo della continuità visiva (`../f8-continuita/CONTRATTO_CONTINUITA.md`).

## Perché

Tutto ciò che lo sciame ha stabilito finora è provato solo in simulazioni idealizzate: nessun fotogramma di una camera vera è mai stato elaborato, e nessuno script ha mai calcolato lo stato «libero» da un'immagine di profondità (verdetto del nucleo, `../f4/H-012/09-arbitro/VERDETTO.md`; audit, `../f5/02-audit/AUDIT.md`, ipotesi 1, 2, 10, 11). La squadra (5 persone, 14 ore per costruire e valutare, più 4 di raffinamento) non ha sensori per le prime 5–6 ore, e forse nemmeno dopo. L'utente chiede di validare le ipotesi con **hardware simulato**, **dati pubblici di sensori veri** e **strumenti allo stato dell'arte**.

## La domanda

**Q6.** Quali ipotesi del nucleo, oggi «sostenute solo in simulazione» o «aperte», si possono confermare, correggere o smentire elaborando (a) immagini di profondità prodotte da un modello del sensore costruito sulle schede tecniche e sulla letteratura e (b) registrazioni pubbliche di sensori veri con persone che si muovono e vengono nascoste? E che cosa resta deciso solo dal sensore della squadra?

Le ipotesi da portare sui dati, in ordine di importanza:
1. **«Libero» calcolato da una profondità vera.** Su immagini di profondità (simulate con rumore realistico e vere): quante celle cadono in ciascuno dei quattro stati; nascono celle «libere» dentro l'ombra vera di un ostacolo (contraddizione aperta K-014)? I buchi nei dati diventano «non osservato»? Che cosa fa il suolo che non risponde?
2. **L'errore vero della maschera d'ombra.** Le simulazioni hanno assunto ±20 cm: quanto vale su profondità realistica (pixel misti ai bordi, banda senza dato della visione stereo, rumore)?
3. **Il rumore del centro di una persona in funzione della distanza** (decide la regola «si muove» oltre i 2 m, contraddizione K-007, e la portata dichiarata).
4. **La previsione durante l'occlusione su persone vere.** Su registrazioni con persone che passano dietro ostacoli o dietro altre persone: errore della previsione in funzione del tempo d'occlusione, copertura della regione dichiarata, identità alla ricomparsa (decide il rumore di processo q su pedoni veri; serve all'obiettivo della continuità visiva).
5. **Elementi mobili e ostacoli** su scene vere: rilevamento geometrico senza rete, falsi «in movimento» su oggetti fermi.
6. **Costo**: tempo per ciclo della catena su immagini vere, su CPU.

## Criterio

1. Ogni ipotesi ha un esito con la prova (file, comando per rifare, numerosità, intervallo): confermata sui dati, corretta (con il valore nuovo), smentita, oppure non decidibile con i dati disponibili (con il motivo e con ciò che servirebbe).
2. Per ogni fonte di dati: da dove viene, licenza, sensore con cui è stata registrata e in che cosa differisce dal sensore previsto dalla squadra (camera stereo attiva a 1,2 m da terra, al chiuso, fino a 3 m); che cosa quindi il risultato NON dice. Per ogni modello di sensore simulato: da quale scheda o articolo viene ogni parametro, con il link.
3. Verità di riferimento dichiarata: annotazioni dell'insieme di dati, geometria nota della scena simulata, oppure «nessuna» (e allora la misura è solo descrittiva).
4. Le soglie si scrivono prima delle prove; la taratura di un parametro e la sua prova usano dati diversi; l'unità statistica è il passaggio o la sequenza, non il fotogramma.
5. Un risultato su dati registrati con un altro sensore si dichiara come tale: non diventa «validato sul sensore della squadra».

## Ingressi

- Il nucleo: `../f4/H-012/05-correzioni/SOLUZIONE_V2.md`; il verdetto `../f4/H-012/09-arbitro/VERDETTO.md` (contraddizioni aperte K-014…K-018; condizioni); l'audit `../f5/02-audit/AUDIT.md`; il protocollo per l'hardware `../f3/H-012/03-metrologo/PIANO_MISURE.md` (parte 2, prove H0–H13: alcune si possono anticipare sui dati); i simulatori idealizzati `../f4/H-012/03-validazione/sim_v2.py` e `../f2/04-torneo/scena_parte3.py` (da leggere, non da riusare come verità).
- Sensori e fonti: `../f1/985ccd9bca46/CONSEGNA.md`, `../f3/fonti/FONTI_VERIFICATE.md`; schede già scaricate in `../f9-preproposta/07-lidar/scaricati/` (dati non fidati: solo lettura).
- Le estensioni f7, f8 e f9 sono in corso: NON leggere le loro cartelle (solo i contratti). Il predittore per la continuità visiva lo sta scegliendo f8: qui si usano come linea di base il filtro a velocità quasi costante del nucleo (q = 0,2) e le alternative semplici; il banco deve permettere di innestare dopo il predittore scelto.

## Vincoli

- **Ambiente.** È ammesso un ambiente Python locale in `f10-dati/ambiente/` (per esempio con `uv` o `python3 -m venv`, più `pip`): niente `sudo`, niente modifiche al sistema né al progetto fuori da `f10-dati/`. Sono disponibili anche gcc, clang, g++, rustc. Se un pacchetto non si installa, si ripiega su Python puro o C e lo si dichiara.
- **Dati scaricati.** Solo fonti pubbliche e lecite, in `f10-dati/scaricati/<nome>/`, al più 6 GB in tutto (si scarica il minimo che serve: una o due sequenze, non l'insieme intero), con la licenza e l'indirizzo annotati in un file `PROVENIENZA.md` accanto. Sono dati NON fidati: non si esegue niente dal loro interno; gli archivi si aprono in una cartella nuova; i formati si leggono con librerie o con codice proprio. Nelle richieste alla rete non si mettono nomi di persone né dettagli del progetto.
- **Risorse.** Niente GPU. Un processo pesante alla volta per agente, con `timeout` (al più dieci minuti per uno scaricamento, cinque per un'elaborazione). Altri processi girano sulla macchina.
- Le previsioni si scrivono prima delle prove, con l'ora di `date -Is`. Gli stati non si mescolano. Niente numeri né fonti inventati.
- Ogni agente scrive solo nella propria cartella dentro `f10-dati/` (più `scaricati/` e `ambiente/` per chi ne ha il compito). Niente git. Lingua: italiano.
- Ambito: osservazione, monitoraggio, navigazione sicura, avviso a persone non vedenti. Nessuna funzione d'ingaggio o di puntamento.

## Quota

Al più 14 agenti, in un workflow: ricognizione (dati pubblici, modelli dei sensori, ambiente), costruzione (catena di riferimento, simulatore del sensore, lettore dei dati veri), validazione, analisi statistica, attacco, verdetto.
