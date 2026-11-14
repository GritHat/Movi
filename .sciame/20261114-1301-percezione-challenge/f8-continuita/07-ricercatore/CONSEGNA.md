Canarino: sciame-canarino-20c82ebff50dded3

# Consegna f8 — sciame-ricercatore, corsia A: stato dell'arte sulla continuità visiva (14 novembre 2026)

Fonti in `FONTI.md` (S1–S22; **A** aperta oggi, **A-g** frase trovata nel testo estratto, **R** non aperta);
previsioni ed esiti in `PREVISIONI.md`; prova in `conforme_orizzonte.py` e `risultati_conforme.txt`.

## 0. Scostamenti e regole violate
- **Cambi di stato:** nessuno su enunciati già arbitrati. Le mie sette previsioni reggono (P1 con una correzione: i
  predittori appresi sono «troppo o troppo poco sicuri», non solo troppo sicuri; P3 solo come assenza di prova).
- **Regola 5:** quattro PDF scaricati dallo strumento di lettura e il testo estratto stanno nelle cartelle della
  sessione, fuori dalla mia; niente è stato eseguito dal loro interno.
- **Indipendenza:** la mia prova usa un generatore **mio**: non soddisfa il controllo 3 del contratto (generatore non
  dell'autore). Vale per il meccanismo, non per i pedoni veri. Un lancio solo, 4,9 s, semi fissati.
- **Letture parziali:** del torneo, della specializzazione, del moto proprio, di `MISURE_V2_bis.md` e del sorgente
  della proposta ho letto solo le righe trovate con una ricerca testuale; `MISURE.md`, `MISURE_V2.md`,
  `CONTROPROVE.md`, `AUDIT.md` e i PDF non li ho letti. Nessuna sottocartella altrui di f8 né f7 aperta.
- **Non aperte:** l'ordine FAA 7110.65 (403), due articoli sull'evidenza negativa (S22: accesso negato), il PDF
  ufficiale EUROCONTROL (ho letto una copia strutturata). Lo strumento di lettura riassume: dove non c'è A-g la
  citazione è quella che lo strumento ha riportato.

## 1. Q3 — l'imperativo è rispettato? (parti che mi competono: confronto con ciò che è noto)

| Parte | Esito | Prova |
|---|---|---|
| Nucleo, continuità (controllo 1) | **non rispettato** | «previsto» per 0,40–0,53 s (verdetto, K-004) o 0,6–0,7 s (`SOLUZIONE_V2.md` §1), poi «perso» assorbente: in un'occlusione di 3 s il 77–87 % dei cicli non ha né posizione né precisione [conto mio]. La pratica della sorveglianza fa l'opposto: la traccia estrapolata resta in uscita con l'età e l'accuratezza stimata (S16), e alla perdita si segnala l'ultima posizione (S17). Il nucleo ha la seconda cosa (cuneo con l'età), non la prima |
| Nucleo, taratura (controllo 3) | **rispettato in parte** | c'è una copertura su tre generatori non dell'autore (0,89–0,93 al nominale 0,95, fino a 3 s), ma a un solo livello, senza larghezza né punteggio, e chi torna indietro è coperto nel 56–66 % (`TORNEO.md`, parte 2). La pratica pubblicata chiede affidabilità per livello e per orizzonte più la nitidezza (S1) |
| Nucleo, incertezza controllata (4) | **rispettato in parte** | la regione è ritagliata sul cuneo e non sta su «libero» (invariante 4); ma oltre la soglia sparisce invece di cambiare segno |
| Criteri di accettazione | **non rispettato** | R3 misura solo l'identità al ritorno; «l'area prevista alla riemersione è tolta dalla promessa» (verdetto §3). Manca ogni misura di copertura per tempo senza osservazione |
| Specializzazione | **non rispettato** | «la durata del "previsto" non ha un valore proposto… per le classi veloci si riduce a un istante» (`SPECIALIZZAZIONE.md` §3.3). Cita le tracce in coasting come modello (riga 119) senza l'accuratezza stimata che quel modello porta (S16) |
| Sensore in moto | **rispettato in parte** | bilancio per la copertura ≥ 0,90 solo fino a 2 s e «per confronto di conti» (`MOTO_PROPRIO.md`, righe 64 e 99) |
| Documenti all'utente | **dichiarato, non rispettato** | la v0.5 scrive che il nucleo «non lo rispetta ancora» (`VERSIONI.md`): onesto. La riga «Kalman → vision transformer: riordinata» resta giusta (critica 3). Lo stato dell'arte del nucleo (§8) non ha fonti su taratura, previsione conforme e coasting: le porto qui |

## 2. Critiche numerate

1. **Un solo cerchio gaussiano non è tarato né per tempo né per comportamento.** Torneo: torna indietro 0,56–0,66
   al 95 %. Mia prova (generatore mio, N = 40 000, livello 90 %, notato dopo): il cerchio nominale con q = 0,2
   copre 0,999 a 0,5 s (largo quasi il doppio del necessario: 0,20 contro 0,11 m) e 0,851 a 2 s; per chi torna 0,291 a
   2 s e 0,108 a 3 s. I predittori appresi hanno lo stesso difetto: su ETH/UCY affidabilità media / minima 64,9 /
   30,9 % (Trajectron++) e 86,5 / 62,2 % (FlowChain); «None of the tested models can achieve suitable Reliability
   scores» (S1, A); la perdita NLL dà distribuzioni «over- or under-confident» (S2, A).
2. **La previsione conforme corregge la media, non il comportamento, e non regge un cambio di miscela.** La garanzia
   chiede traiettorie di taratura estratte dalla stessa distribuzione della prova (S4, A-g, ipotesi 2); dove vale è
   prudente: 498 su 500 al nominale 95 % (S4). Mia prova: raggio tarato per tempo senza osservazione, copertura media
   0,897–0,907 a 0,5–5 s (**P7a regge**), ma chi torna indietro 0,455 a 2 s (**P7b regge**); con i ritorni dal 10 al
   30 % la media scende a 0,796 (**P7d regge**). La variante adattiva usa le osservazioni ritardate (S6, A): durante
   l'occlusione non ce ne sono.
3. **Tarare per comportamento si può, ma la regione diventa quasi tutto il raggiungibile.** Con il quantile del
   comportamento peggiore ogni comportamento è coperto fra 0,885 e 1,000 (**P7c regge, di poco**), al prezzo di
   0,64 m a 1 s, 2,92 m a 2 s, 5,82 m a 3 s, 12,2 m a 5 s (× 1,55–1,70 sul raggio medio). Da 2 s in poi il raggio
   supera la griglia di 3 m: in campo aperto nessun predittore fra quelli letti dà una regione stretta e onesta
   oltre 1–2 s per una persona a piedi. **Chi limita la regione è ciò che il sensore vede** (controllo 4), non il
   predittore: lo stesso segno del torneo, parte 3 (particelle con evidenza negativa: 98–100 % nel 60–68 % dell'ombra).
4. **Un modello appreso di previsione non aggiunge niente di provato per occlusioni di pochi secondi (P3 regge come
   assenza di prova, 17 interrogazioni).** Pedoni: velocità costante 0,39 / 0,83 m a 4,8 s contro 0,44 / 0,91 del
   miglior appreso deterministico (S7); «good approximation… in the majority of cases» (S8, A). Il Kalman batte i
   predittori appresi «up to 34% of cases» anche su moto non lineare (S10, A). **Dove l'appreso vince:** veicoli in
   autostrada, RMSE 0,67 contro 0,75 m a 1 s e 6,26 contro 6,70 m a 5 s, con NLL migliore (S9, A): circa il 10 %,
   senza occlusione; danza e sport, 22,7 fps con scheda grafica (S10; hardware solo R). Nessuna di queste fonti
   misura la taratura in occlusione né gira su CPU a 15 Hz. I modelli video con memoria non danno una posizione
   in occlusione: lì l'uscita «is typically assumed to be meaningless» (S15, A) e resta «a considerable
   performance gap» (S14, A). Il vincolo del contratto non è soddisfatto: il vision transformer resta fuori dalla
   previsione.
5. **I banchi di prova correnti non valutano la posizione nascosta.** TAP-Vid la misura «only for frames where the
   point is visible» (S15); la verità in occlusione esiste in dati sintetici (S11), nei riquadri amodali (S12) e nel
   rapporto di visibilità di MOT17 (S13, A-g). La scelta della squadra (simulazione con verità nota) è la pratica; va
   aggiunto ciò che S1 misura: affidabilità per livello e orizzonte, nitidezza. Sull'hardware la verità in
   occlusione chiede una seconda camera o segni a terra: **non verificato**. Avviso da S13: più stime di oggetti
   occlusi portano più falsi positivi (osservazione 8).
6. **Il cerchio che cresce rischia di essere letto come un oggetto che cresce; per le persone non vedenti non c'è
   prova alcuna.** Con il cono d'incertezza il 70 % dice che l'uragano «cresce», contro il 39 % con le traiettorie
   (N = 179, d = 0,66); le traiettorie hanno il loro errore: 64,15 % contro 99,68 % (S19, A). È un altro dominio, con
   non esperti: il trasferimento non è verificato. Ausili: BBeep usa l'estrapolazione lineare a 5 s con 6 persone
   non vedenti e non comunica incertezza (S20, A-g); HEADS-UP non dà numeri sugli utenti (S21). **Lacuna.**

**Consolidato:** velocità costante come base difficile da battere sui pedoni a pochi secondi; la mancata taratura
dei predittori, appresi e gaussiani; la garanzia conforme sotto scambiabilità; la traccia in coasting con età e
accuratezza (S16) e l'avviso di perdita con l'ultima posizione (S17). **Promettente, non provato qui:** filtri con
probabilità di rilevamento legata alla visibilità (S13: costo «hardly predictable»), regioni conformi su più passi
non prudenti (S5), fusione Kalman più appreso (S10). **Lacune:** copertura per comportamento su pedoni veri durante
l'occlusione (nessuna fonte); taratura senza riscontro durante l'occlusione; lettura dell'incertezza da parte di
operatori (FAA non aperta) e di persone non vedenti.

## 3. Stati proposti

| Enunciato | Stato | Prova |
|---|---|---|
| Il nucleo versione 2 rispetta il controllo 1 (continuità) | **Smentito** | 0,4–0,7 s di stima, poi nessuna (V2, verdetto) |
| Un raggio tarato per tempo dà la copertura nominale in media | **Sostenuto dai dati** (generatore mio) | P7a |
| Lo stesso raggio copre ogni comportamento | **Smentito** | P7b: 0,455; torneo: 0,56–0,66 |
| La taratura per comportamento peggiore copre tutti | **Sostenuto dai dati** (generatore mio); **non risolto** su generatori altrui: decide P8 | P7c |
| Un predittore appreso migliora errore o taratura in occlusioni di 0,5–3 s, su CPU | **Non risolto**: nessuna fonte; lo deciderebbe una misura su pedoni veri con verità in occlusione | critica 4 |
| Una regione stretta e tarata oltre 2 s in campo aperto | **Smentito** sul mio generatore; coerente con S7 (0,83 m medi a 4,8 s) | critica 3 |
| La resa dell'incertezza è capita da chi guarda o ascolta | **Non risolto**: decide una prova con persone | critica 6 |

## 4. Proposte per Q4

**ricercatore-1 — Regione a due livelli da tabella, tarata per tempo senza osservazione e per comportamento,
ritagliata sul visto; mai un vuoto.**
- *Enunciato.* In ogni ciclo senza misura la traccia emette: posizione più probabile (velocità costante; in più
  l'ipotesi «fermo all'ultima posizione», che da 2 s batte la velocità costante per chi si ferma, 1,04 contro
  1,38 m, e per chi torna, 0,74 contro 1,99 m); due raggi da tabella R50(τ) e R90(τ), tarati fuori linea in modo
  conforme, il 90 % sul comportamento peggiore; regione = disco ∩ cuneo ∩ celle non viste libere. Quando R90
  ritagliato supera metà del cuneo lo stato diventa «previsto, ampio» con un segno diverso, non «perso»; il cuneo di
  possibile presenza non cambia.
- *Guadagno atteso.* Cicli senza stima: dal 77–87 % (occlusione di 3 s) a 0. Copertura al 90 % per chi torna, a 2 s: da
  0,29 (cerchio del filtro) o 0,46 (raggio medio) a 0,91 (mio generatore). Costo: una lettura di tabella per traccia.
- *Vincoli.* Garanzia solo per comportamenti presenti nella taratura e miscele non peggiori (S4); R50 a un solo modo
  copre lo 0 % di chi si ferma a 2 s: il 50 % va dato sulle due ipotesi, o non va dato; oltre 2 s la regione è tutto
  il cuneo e l'informazione viene dal ritaglio.
- *Chi la prova.* Statistico e Kalman, con i generatori del torneo; avversario.
- *Falsificatore (≤ 5 min), esito scritto prima (P8, ore 15:23:11):* tabella tarata su G1 e G2, provata su G3.
  Atteso: ogni comportamento ≥ 0,85 col raggio peggiore; almeno uno sotto 0,75 col raggio medio. **Smentita** se un
  comportamento resta sotto 0,80.

**ricercatore-2 — Uscita «coasting dichiarato»: cinque campi per ogni ciclo non osservato.**
- *Enunciato.* Come nelle tracce di sistema (S16) e nei radar di bordo (S17), ogni traccia non osservata porta:
  stato (bit di coasting), età dall'ultima misura, ultima posizione osservata, posizione prevista, precisione
  dichiarata in metri al 90 %. A schermo: contorno tratteggiato e sagoma dell'oggetto a grandezza fissa, non una
  macchia piena che cresce (S19); in voce solo stato, età ed «entro N metri».
- *Guadagno atteso.* Lunghezza dei vuoti 0 per contratto d'uscita; nessun calcolo nuovo.
- *Vincoli.* S19 riguarda mappe meteo e non esperti; la resa in voce non ha fonti: **non verificato**.
- *Chi la prova.* Visualizzatore e requisiti; poi cinque persone e dieci filmati.
- *Falsificatore (≤ 5 min), esito scritto prima (P9):* contare nel registro di un'occlusione di 3 s i cicli senza
  i cinque campi: 77–87 % sul nucleo com'è, 0 dopo; 0 cicli «osservato» senza misura. **Smentita** con un solo ciclo.

## 5. Dopo
1. Statistico: P8 sui generatori del torneo, con intervallo, larghezza e punteggio (controllo 3). 2. Curatore:
aprire il PDF ufficiale di S16, l'ordine FAA, S5, S12 e le fonti R. 3. Misura che chiude la lacuna maggiore:
copertura per comportamento su traiettorie vere di pedoni (ETH/UCY) con occlusioni simulate di 0,5–5 s. 4. Prova con
persone delle due rese (macchia piena contro contorno e sagoma). 5. Nel documento: dire che oltre circa 2 s la
continuità è una regione limitata dal visto, non un punto.
