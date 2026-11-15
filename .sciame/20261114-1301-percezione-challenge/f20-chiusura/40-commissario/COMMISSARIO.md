# Lettura da commissario esterno: documento tecnico v3 e proposta v3.0 (`sciame-lettore`)

Scritto il 15-11-2026, dalle 06:56 alle 07:05 circa (`date -Is`).

**File letti.**
- `allegato_tecnico/allegato_tecnico.pdf`: 108 pagine, del 15-11 alle 06:48.
- `proposta/proposta_sciame.pdf`: 2 pagine, del 15-11 alle 06:41.
- Per il confronto: `f20-chiusura/20-verdetto/VERDETTO_FINALE.md`, `ADDENDUM_UTENTE.md` (fino all'esito di c1, verso le
  06:50) e `05-scorta/correzione_f7r/CORREZIONE.md` con `verifica/VERIFICA.md`.

**Come cito le pagine.** «p. N» è la pagina del PDF; la pagina stampata è N − 1. «r. k» è la k-esima riga di testo
non vuota estratta da `pdftotext -layout`, quindi è approssimata: per ritrovare il punto, conta la citazione fra
virgolette.

## 0. In testa: cambi di stato e regole

**Regole.**
- Ho scritto solo in questa cartella e nello scratchpad.
- Niente cancellazioni né sovrascritture, niente git, rete o sudo.
- Python con `-I` dal venv indicato.

**Indipendenza.** Condivido con gli autori solo i due PDF e i rapporti dello sciame che ho letto per il confronto.
- Non ho rieseguito le simulazioni.
- Ho ricontato a mano con la formula di Wilson 60 cifre dei due documenti: **tutte coincidono**, da 39/60 [0,524;
  0,758] fino a 655/733 [0,869; 0,914].
- Ho rifatto a mano:
  - la dimostrazione di σ²(τ), del lemma di convessità, di C₂ e C₃, di k₀,₉ (2,146 e 2,500), del tempo di soglia
    t_C (proposizione 10.7 (i)–(iii)), del contenimento (10.9) e del cammino massimo L(τ) (10.10);
  - l'esempio numerico del § 10.6.3 (10,7 s; 9,6 s; 17/39/91/238/427 m);
  - la tabella 55 del drone seguito per A (C = 0,84 e 0,62, r₀,₉ = 33,6 e 46,2 m, t(C < 0,9) = 1,35 s, con q = 80);
  - le distanze 3312, 2005, 543 e 1058 m.

  **Le dimostrazioni sono corrette** nei modelli dichiarati.

**Ciò che non copro.** La fisica e il modello dei sensori, e il contenuto delle fonti esterne.

**Che cosa ho capito dopo la prima lettura** (parafrasi).
- MoVi non dice mai «libero» su ciò che non vede, e in volo veloce tiene una regione dove l'oggetto può essere.
- Ne dichiara la confidenza nel tempo con una formula chiusa, tarata su tracce ADS-B.
- A bordo di un drone tiene la traccia attraverso una collisione vicina. Se il radar è accecato, però, l'avviso dei
  detriti non funziona.
- La collisione veloce non viene riconosciuta come evento.
- Tutto è simulato.

Il messaggio arriva, ed è onesto. Le cifre dei due documenti coincidono fra loro e con il § 2 del verdetto finale. I
difetti sono in **ciò che manca** (la correzione c1), in **qualche contraddizione interna** e in **due punti della
confidenza che possono fuorviare**.

**Riferimenti rotti.** Nessun «??» in nessuno dei due PDF (`grep` su tutto il testo estratto).

**Frasi del § 7 del verdetto.** Nessuna è presente (`grep` di: validato, 16 aerei, 130×90, 90-48D citata come fonte,
14 357, 3812, 1237, «99 %» di confidenza, «tarata» senza condizione, tempo reale, certificabile, detect and avoid,
insegue, intercetta, istantaneo). «Validato» compare solo come «niente è validato».

## 1. Difetti, dal più grave

**D-1 (grave: manca un risultato deciso).** La correzione c1 del radar accecato non c'è in nessuno dei due documenti.
- L'addendum 19 dice: «Documento tecnico e proposta riportano F7, F7r e c1 con limiti e migliorie».
- I documenti invece dicono che l'avviso «crolla (0 su 59)»:
  - proposta p. 1, r. 15 e r. 73;
  - allegato p. 11 (tab. 2), p. 64 (V5), p. 87 (F7r) e p. 95 (conclusioni).
- In più la tab. 58 (p. 92, riga «F7: radar non accecato») presenta come «Prossimo» proprio la miglioria già provata.
- Un commissario che vede il video con la «strada promettente» e poi legge «crolla» crede a una contraddizione.
- Prova che manca nei documenti (CORREZIONE.md e VERIFICA.md):
  - avviso prima del frammento entro 10 m: cella totale da 0/59 a **59/59 [0,939; 1]** (McNemar appaiato p = 3,5·10⁻¹⁸),
    davanti/att 51/51 [0,930; 1], vira/att 58/58 [0,938; 1];
  - continuità 60/60 in ogni cella; «libero» 0;
  - identità spurie non dichiarate da 1/60 a 0/60.
- Limiti:
  - riacquisizione entro 2 s in davanti/att 49/60 [0,701; 0,894], sotto la soglia di 51/60;
  - vira/att 40/60 [0,541; 0,773];
  - l'avviso non localizza: è una sfera prudente fino a 565 m, accesa per una mediana di 8 s;
  - **11/200 [0,031; 0,096] falsi avvisi** se il radar satura per un'altra causa.

**Correzione.**
- Allegato p. 87, dopo «…con il radar cieco non è affidabile.», aggiungere il paragrafo: «*Correzione provata (c1).*
  Alla saturazione congiunta di radar e camere il sistema dichiara subito un "evento vicino non localizzato" con un
  volume prudente attorno al portatore, dentro il quale non dice mai "libero". Su semi nuovi, con confronto appaiato
  [S]:
  - l'avviso prima del frammento entro 10 m passa nella cella totale da 0/59 a 59/59 [0,939; 1], davanti a 51/51
    [0,930; 1] e in virata a 58/58 [0,938; 1];
  - continuità 60/60, "libero" 0, falsi avvisi nel controllo 0/200 [0; 0,019].

  Limiti:
  - l'avviso non localizza l'evento (sfera fino a 565 m, accesa per una mediana di 8 s);
  - se il radar satura per un'altra causa i falsi avvisi sono 11/200 [0,031; 0,096];
  - la riacquisizione entro 2 s resta sotto soglia, 49/60 [0,701; 0,894].

  È una strada promettente, non adottata.»
- Tab. 58, p. 92: lo «Stato» diventa «c1 applicata in simulazione: avviso 59/59 nella cella totale; falsi 11/200 con
  saturazione radar d'altra causa. Prossimo: localizzare l'avviso (direzione del lampo, Doppler); soglia: falsi ≤ 0,05
  con avviso ≥ 0,9».
- Tab. 2 (p. 11), V5 (p. 64), conclusioni (p. 95): «fino a 0/59 [0; 0,061]; con la correzione c1 59/59 [0,939; 1], ma
  non localizzato e con 11/200 falsi avvisi».
- Proposta p. 1, r. 15: «…l'avviso al portatore crolla (0 su 59 nel caso peggiore); una correzione in prova lo riporta
  a 59 su 59 [0,939; 1], ma non localizza l'evento e dà 11 falsi avvisi su 200 se il radar satura per altra causa L».
- Proposta p. 1, r. 73: lo stesso, in forma breve.

**D-2 (grave: contraddizione interna).** «Nessuna prova con il sensore in moto», contro F7.
- p. 14, r. 9 (§ 1.7): «nessuna prova è stata fatta con il sensore in moto o indossato».
- p. 94, r. 48: «Il sensore in moto è trattato solo come analisi dei requisiti».
- Le due frasi negano il § 10.7, cioè F7, che è parte del caso centrale.

**Correzione.**
- p. 14: «a corto raggio nessuna prova è stata fatta con il sensore in moto o indossato; a lunga portata il sensore a
  bordo di un drone in moto è simulato nello scenario del § 10.7».
- p. 94: «A corto raggio il sensore in moto è trattato solo come analisi dei requisiti (§ 8.11); il sensore in moto a
  lunga portata è simulato in § 10.7».

**D-3 (medio-grave: può fuorviare sulla base matematica).** La formula mostrata non è quella con cui è misurata la
copertura.
- La (32) e la proposta (p. 1, r. 56) mostrano C = 1 − exp(−r²/2σ²) con r₀,₉ = 2,146σ: è il caso a un regime, nel
  piano.
- La copertura della tab. 52 e della proposta (0,85–0,89; 0,73) è misurata in altro modo:
  - sulla **sfera in 3D** («u = C della sfera», p. 82; `curva_video.py` r. 48: «sfera 3D»);
  - con la **miscela** di regimi;
  - con la **ricalibrazione isotonica**.
- Il lettore crede che 2,146σ dia lo 0,89.

**Correzione.**
- p. 83, r. 19, dopo «verificata numericamente»: «La (32) è scritta per un solo regime nel piano. La copertura della
  tabella 52 è misurata sulla sfera (k₀,₉ = 2,500), con la miscela della proposizione 10.8 e la ricalibrazione
  isotonica: la cifra viene dalla catena intera, non dalla sola (32)».
- Proposta § 3: «(caso a un regime nel piano; la copertura in tabella è misurata in 3D, con la miscela e la
  ricalibrazione)».

**D-4 (medio: può fuorviare su che cosa copre la regione).** σ_rif = 20 m gonfia la regione per l'errore della
verità ADS-B.
- La copertura dichiarata è quindi quella della **posizione ADS-B**, non della posizione vera.
- Con un sensore e una verità diversi, σ_rif va rimisurato.

**Correzione.** p. 83, punto 1, aggiungere: «la copertura è misurata rispetto alla posizione ADS-B; con un'altra verità
di riferimento σ_rif va rifissato (tappa 2 del § 11.2)».

**D-5 (medio: tre cifre diverse per la stessa cosa).** Copertura sui 43 aerei del sito.
- Le tre cifre:
  - tab. 4 (p. 13, r. 65): «circa 9 su 10 da 2 a 30 s (… estremo inferiore ≥ 0,88)»;
  - § 10.9 (p. 90, r. 20): «circa 0,93–0,95»;
  - conclusioni (p. 95, r. 27): «circa 9 casi su 10 fino a 30 s».
- Nessuna ha un intervallo per passaggio.
- Accanto c'è 0,71 → 0,89 sugli aerei della taratura. Il commissario non capisce quale sia la cifra vera, né perché
  sia diversa.

**Correzione.** Usare ovunque la cifra di § 9.6, con il suo intervallo, e la frase «con l'inviluppo di 90 m/s; è un
esperimento diverso dalla taratura del § 10.6.8 (zona d'avviso, non regione al 90 %)».

**D-6 (medio: troppo forte).** Proposta p. 2, r. 32 (tabella «I requisiti della traccia»).
- Dice: «regione mantenuta dopo urto, cecità e collisione vicina, 60 su 60 per cella simulata S».
- È falso in tre celle:
  - F7 davanti/att 59/60;
  - F7r totale/att 59/60;
  - col radar rotante F1/att 39/60.

**Correzione.** «regione mantenuta dopo urto, cecità e collisione vicina: 59–60 su 60 per cella col radar a scansione
elettronica o a 360° S; col radar rotante a 1 Hz 39 su 60 L».

**D-7 (medio: il lettore inciampa).** Proposta p. 1, r. 42 contro § 5.
- La r. 42 dice «Nessun falso evento nelle quasi collisioni a 40 m».
- Il § 5 dice «falsi eventi in un quasi incrocio a 39 m, 2 su 60».
- Sembra una contraddizione: la differenza (nucleo adottato contro regola in prova) non è detta nella r. 42.

**Correzione.** r. 42: «S Col nucleo adottato, nessun falso evento…». Lo stesso nella tab. 49 (p. 77), già scritto
«(nucleo adottato)»: va bene così.

**D-8 (medio: riferimenti al modo di lavorare).**
- Proposta p. 1, r. 4, intestazione: «fase 4: volo ad alta velocità; con documento tecnico» (`proposta_sciame.tex`
  r. 28, `\statodoc`). «Fase 4» è l'organizzazione interna del lavoro.
  - Correzione: «volo ad alta velocità; con documento tecnico».
- Bibliografia, pp. 106–108: le voci portano note di lavoro, non bibliografiche:
  - «Aperta il 15-11-2026: …» con citazioni;
  - «IEEE Xplore non restituisce contenuto», «PMC chiede un controllo del browser», «MDPI 403»;
  - «risultato di ricerca: 11-5-2025»;
  - «lette solo le accuratezze».

  Correzione: ridurle a «consultata il 15-11-2026; testo intero non consultato» oppure «dato del produttore».

Non ho trovato nomi dello sciame, di fasi, di ruoli né di percorsi `.sciame` nel testo (`grep` su fase, sciame,
addendum, arbitro, coordinatore, verdetto, f1x-, K-, F-8xx, v3i e v4c).

**D-9 (medio: riproducibilità).** Appendice B, p. 99: «I programmi, nella cartella di lavoro delle prove del progetto,
sono: …».
- Il percorso non è dato, e i file stanno in una cartella nascosta di lavoro.
- Un revisore non li trova.

**Correzione.** Copiare i programmi in `prototipo/prove/volo/` (copia, senza spostare) e scrivere quel percorso.

**D-10 (medio-basso: parametri mancanti).** p. 87, r. 42, tabella 55.
- Per B manca σ₀ᵥ. Dai valori della tabella lo ricavo a circa 4,6 m²/s (non verificato); con σ₀ᵥ = 0 non si rifà
  la riga.
- Mancano anche q = 80 m²/s³ e l'accelerazione dell'insieme di presenza, che dai numeri vale a = 10 m/s².
- La tabella è [C], ma non si ricalcola.

**Correzione.** «A: σ₀ = 3,05 m, σ₀ᵥ = 13,6 m²/s, σᵥ = 6,84 m/s; B: σ₀ = 1,26 m, σ₀ᵥ = ‹valore dal file›, σᵥ = 5,17
m/s; q = 80 m²/s³ per asse; insieme di presenza r₀ + 3σᵥτ + aτ²/2 con a = 10 m/s²». Il valore va preso da
`05-scorta/curva_F7.json`.

**D-11 (basso: una costante non spiegata).** p. 90, r. 3: «250·(0,75+12,5) = 3312 m».
- Il primo avviso su CPU della tab. 57 è 0,70 s, non 0,75.

**Correzione.** Dire da dove viene 0,75 s, oppure usare 0,70 (dà 3300 m). In quel caso va cambiato anche «3312» nella
proposta e nel § 6 del verdetto: decide l'arbitro.

**D-12 (basso: incongruenze di lettura).**
- (a) p. 6, r. 20: τ è «latenza dall'evento all'uscita», ma nel § 10 τ è il tempo dall'ultima misura. Aggiungere al
  blocco del § 10 dei simboli: «τ (§10): tempo dall'ultima misura».
- (b) p. 81, r. 35: «76 piccole violazioni» non ha denominatore, e accanto c'è «45 su 1440» (p. 83). Correzione: «76 su
  ‹N› passi dei registri simulati (altro insieme dai 1440 della taratura)».
- (c) Proposta § 3, ultima frase: «C scende da 1,00 a 0,62 a 2 s» vale solo con il radar frontale; col radar a 360° è
  0,73. Aggiungere «(radar frontale)».
- (d) Proposta § 4: «20 su 20 [0,839; 1]» sta sotto la classe S, ma il limite inferiore è sotto 0,90. Scrivere
  «(robustezza, 20 per cella)».
- (e) Proposta § 4: il volume dei detriti è dato solo in campioni (correlati). Aggiungere «60 su 60 passaggi [0,940; 1]
  per geometria, radar a 360°».
- (f) Proposta § 2: «Sei scenari simulati con sensori allo stato dell'arte» comprende anche il radar rotante a 1 Hz.
  Scrivere «con sensori di classe attuale (radar a scansione elettronica e radar rotante)».
- (g) Proposta § 3, riga «prima della taratura»: 0,96 e 0,905 senza intervallo. Scrivere «(stime)» o mettere
  l'intervallo.
- (h) Sommario, p. 2, r. 12: «contenimento dimostrato per velocità fino a 210 m/s». Aggiungere «se l'errore iniziale è
  entro r₀», come fa il testo a p. 82.

**D-13 (basso: refusi).**
- «s.d..» con il punto doppio: voci [7], [8], [10], [12], [78], [79], [84], [85], [87].
- «RealSense.Post-processing» senza spazio: voce [12].
- «Metadati Crossref verificati il 15-11-2026 .» con lo spazio prima del punto: voce [101].
- «Il 89,5 %» va scritto «L'89,5 %»: p. 83 (`11_volo_alta_velocita.tex` r. 324) e tab. 2 a p. 11
  (`01_introduzione.tex` r. 104, «il 89,5 %»).
- La «pregola» a p. 64 è un artefatto dell'estrazione del testo (la radice di una formula), non un refuso: da non
  correggere.

**D-14 (struttura, nessuna correzione obbligata).**
- Il caso centrale comincia a p. 74 su 108.
- La tab. 1 dei requisiti (p. 8) è tutta a corto raggio, e il sommario dedica più righe al corto raggio che al volo.
- Proposta (facoltativa): una tabella «requisiti della sfida → volo veloce» nel § 1.2, uguale al § 8 della proposta, e
  il sommario che comincia dal volo.

## 2. Stati che propongo

- Dimostrazioni del § 10 (proposizioni 10.3, 10.6, 10.7, 10.9 e 10.10, lemma 10.4): **dimostrato** nel modello
  dichiarato, ricontrollato.
- Cifre: **coerenti** fra allegato, proposta e verdetto finale § 2, salvo c1 (D-1). Wilson **verificato** su 60
  conteggi.
- La copertura 0,85–0,89 resta **I su dati pubblici**, con le condizioni D-3 e D-4.
- Video EN v3: 173,856 s (ffprobe), dentro il limite di 176 s. Non contiene c1, come i documenti. Il resto del video
  **non l'ho verificato**.

## 3. Che cosa propongo dopo

- Applicare D-1, D-2, D-6, D-7 e la prima parte di D-8 (sono testo, pochi minuti), poi ricompilare con versioni nuove
  accanto.
- D-3 e D-4: due frasi.
- D-5 e D-10: chiedono di aprire `f15…/VERDETTO_2C.md` e `curva_F7.json`.

**Che cosa manca in questa lettura.**
- Non ho letto riga per riga i capitoli 2–9 né le appendici: solo `grep` e i punti citati.
- Non ho controllato i riferimenti incrociati (§, tabella, proposizione) uno per uno: ho cercato solo «??».
