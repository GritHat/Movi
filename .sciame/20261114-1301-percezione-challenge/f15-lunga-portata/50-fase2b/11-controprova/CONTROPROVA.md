# Controprova delle correzioni (fase 2b, 11-controprova)

`sciame-avversario`, 2026-11-15, dalle 02:52 alle 03:00 (`date -Is`). Previsioni e soglie scritte prima, alle
02:52:54, in `PREVISIONI.md`. **Tutto è simulazione dalle schede: nessun sensore fisico, niente è «validato».**
Etichette a mano; solo osservazione e avviso. Frequenze per passaggio, Wilson al 95 % (codice mio).

## 0. In testa: cambi di stato e regole

- **Nuovo controesempio (forte), E1.** L'impronta dei detriti col nucleo v2 ha raggio **≥ 10 km in 20 passaggi su 30**
  [0,49; 0,81], mediana **59 km**, massimo 74 km. Copre tutto il sito, avvisa 73–108 tracce per passaggio (tutte), e
  nel codice non c'è modo di toglierla: la regola dice «finché non è ispezionata», ma `eventi_v2.py` non ha
  l'ispezione. Ne risulta un avviso perpetuo che non dice niente. Anche i dati dell'autore lo mostrano
  (`10-riprova/riprova_eventi_passaggi.jsonl`: E1 mediana 46 km, 36/60 ≥ 10 km). RIPROVA non lo dice, e il video
  `lp_E1` (passaggio 0, 4,5 km) non è rappresentativo.
- **Nuovo controesempio nel video centrale.** In `lp_A1` ci sono celle «libero» per i multirotori **dentro l'avviso**
  del drone nascosto: 4 fotogrammi (46,0–47,5 s) e 56 celle-fotogramma, a 29–34 m dal drone vero, con celle da 39 m.
- **Restano smentite:** «libero» sull'oggetto col pannello (A1 alta, famiglia sito: 85/85 non C0), A1 min fuori avviso
  (9/100), E1 entro 2 s (24/30).
- **Regge:** X1 (dentro l'ipotesi 25 m/s²), X4 (n_eff = 1), X6 per il C0, E2 entro 2 s, E4 ed E5 senza falsi eventi.
- **Regole.** Non ho cancellato né sovrascritto file di altri. Ho scritto solo in questa cartella. Niente rete, git o
  sudo. Al più 7 processi Python (6 figli e il padre).
- **Indipendenza.** I miei programmi (`cp_*.py`, `valida_video.py`) chiamano lo stesso simulatore, lo stesso nucleo v2
  e la stessa funzione di misura per passaggio (`prove_lp.passaggio`, `eventi_v2.passaggio`) usati dall'autore. Sono
  miei i semi (indici 5000+ e 7000+, contro 0–199 e 0–59), le aggregazioni, i Wilson, le integrazioni di X1, X5 e il
  validatore video, che legge solo i registri. Vale per difetti di semi, di aggregazione e del registro, **non** per
  difetti della misura condivisa.

## 1. Misure rifatte (semi miei)

| Misura | Esito mio | RIPROVA | Stato |
|---|---|---|---|
| A1 alta, tempestivi (`cp_A.py`) | 100/100 [0,963; 1] | 200/200 | regge |
| A1 min, tempestivi | 100/100 [0,963; 1] | 200/200 | regge |
| A1 min, passaggi con il mezzo fuori dall'avviso | **9/100** [0,048; 0,162]: 6/20 «rallenta», 3/20 «ferma» | 12/200 | **smentita**, si ripete |
| A1 alta, «libero» sull'oggetto (pannello, sito), non C0 | **85/85** [0,957; 1] | 163/171 | **smentita**, si ripete |
| A1 min, «libero» sull'oggetto | 0/85 [0; 0,043] | 0/200 | regge |
| A4 alta (radar 4D + AT128 + EO), «libero» sull'oggetto | 0/85 [0; 0,043] (il Doppler ha portata 0: per costruzione) | — | regge |
| A4 alta, tempestivi / fuori avviso | 95/100 [0,888; 0,978] / **9/100** [0,048; 0,162] | — | il fuori avviso resta |
| E1, evento con 0 ≤ ritardo ≤ 2 s (`cp_E.py`) | **24/30** [0,627; 0,905]; 1/30 «separazione» 11,5 s prima | 49/60 | **smentita** (soglia 0,95) |
| E1, «libero» su un frammento nell'impronta | 0/30 [0; 0,114] | 0/60 | regge |
| E2, evento entro 2 s / mezzo avvisato | 30/30 [0,886; 1] / 30/30 | 60/60 | regge, ma l'impronta contiene il mezzo di 3,2–3,5 km |
| E4 alta e min, E5 a 5 m: falsi eventi | 0/30 ciascuno [0; 0,114] | 0/60 | regge |

Previsioni: la 1 regge, le 2 e 3 reggono (i difetti restano), la 4 è **smentita** (0/85 invece di ≥ 1), la 5 regge,
le 6 e 8 reggono, la 7 è **smentita** (§ 2).

## 2. Attacchi e controesempi nuovi

1. **X1, il drone che scatta da fermo** (`cp_X.py`, spostamento integrato a passi di 1 ms). Con 22 e 30 m/s² fino a
   45 m/s il drone resta dentro l'insieme in entrambe le famiglie: **regge**. Fuori dall'ipotesi, con 25 m/s² fino a
   60 m/s, esce nella famiglia sito da τ = 8 s (408 m contro 374 m) e a 30 s (1728 contro 1364). Vale solo se nel
   sito esistono droni da corsa oltre i 45 m/s: ipotesi da dichiarare.
2. **X3.** Distanza d'avviso dell'operatore: 770 m nella famiglia sito, 3410 m nella famiglia aeroporto (v_max 210).
   È il limite dichiarato, coerente con l'ADDENDUM.
3. **X4.** n_eff vale 1 per 5 passate (ρ = 1): **corretta**, in modo prudente.
4. **X5, l'edificio non in pianta, riaperto dal prototipo** (`cp_X5b.py`). `movi/lungo.py:74` imposta
   `MAPPA_CERTIFICATA_PREDEFINITA = True`. Con un edificio vero non in pianta, il punto dietro risulta **«libero»** a
   75, 125, 175, 275 e 475 m. Con l'edificio in pianta è «in ombra». Con la mappa non certificata è «non osservato».
   La validazione-3 (`sfondo_misurato`) non è chiamata né da `prove_lp.py` né da `lungo.py` (grep: nessuna
   occorrenza). La correzione esiste nel nucleo, ma il prototipo la scavalca: va detto come ipotesi forte.
5. **X6, le classi non dichiarate.** Nella famiglia sito (il caso centrale) `aereo_leggero` (70 m/s), `elicottero`
   (80 m/s), le auto e i pedoni non sono né ammessi né esclusi: il registro di `lp_A1` dichiara «zona non verificata»
   solo per `multirotore_C0` e `aereo_in_volo`. Un elicottero sul sito non entra nell'inviluppo (45 m/s) e non è
   dichiarato. Per il C0 la correzione regge.
6. **Impronta dei detriti in E1 (nuovo, causa nel codice).** In `eventi_v2.apri_evento` c'è
   `r0 = … + 0.5 * a_max * (t_b - t_a) ** 2`. Qui a_max = 25 m/s², l'a_max del multirotore veloce introdotto dalla
   correzione 1, e `t_a` viene da una traccia d'origine vista per l'ultima volta a 1,5–4,5 s, cioè 12–15 s prima
   dell'urto. Ne viene r0 ≈ 2–3 km, e un'impronta di 44–74 km. Lo stesso calcolo col nucleo v1 (a_max 6,9) dava una
   mediana di 16,5 km (`02-eventi/passaggi_v2.jsonl`). La correzione 1 moltiplica un difetto che c'era già
   (tracce vecchie o duplicate fra le origini). Ne seguono **un falso di inutilità** e **un avviso perpetuo**.
7. **Validatore video** (`valida_video.py` → `valida_video_esito.json`; `cp_video_dettaglio.py`). Ricostruisce le
   celle come le disegna `mostra_lungo` e controlla tre cose: il «libero» dentro gli avvisi e dentro il volume o
   l'impronta dei detriti; i conteggi mostrati contro `celle.conteggi`; gli stati dichiarati.
   - `lp_A1`: **56** celle-fotogramma «libero» dentro l'avviso #4, a 29–34 m dal drone vero, che si trova in una cella
     «non osservato».
   - Gli altri 7 registri: 0. Nessun «libero» dentro l'impronta di E1 ed E2.
   - In tutti gli 8 registri, nei primi 2–3 fotogrammi le celle mostrate (576 «non osservato») non coincidono con
     `conteggi` vuoto. È nel verso prudente, ma lo stato mostrato non è quello scritto.
   - **Plausibile, non verificato:** la griglia è calcolata «ogni 2 s (fra due: l'ultima)». Fra 45,0 e 48,5 s il
     `rle` è identico, quindi il «libero» mostrato può avere fino a 2 s, mentre il drone si muove a circa 15 m/s.
   - Il visore non disegna né `detriti` né `zona_non_verificata_per_classe`. Uno stato del registro non è mostrato.

## 3. Stati proposti

- «Avviso detriti al mezzo in pista» (E2): **sostenuto** nella forma debole. Avvisa tutti, perché l'impronta
  contiene il sito.
- «L'avviso dei detriti è utile»: **smentito** in E1, 20/30 ≥ 10 km.
- «Mai "libero" dentro l'avviso»: **smentito** nel registro `lp_A1`.
- «"Libero" con il pannello sull'oggetto»: resta **smentito**.
- X5 nel prototipo: **smentito** con la mappa dichiarata completa.

## 4. Proposte (`avversario-1…4`)

- **avversario-1.** In `apri_evento`, `t_a` vale solo per le origini viste entro 2 s; le altre si escludono. In più
  r0 ≤ v_max·(t_b − t_a).
  - Previsione: mediana di R_imp in E1 ≤ 5 km, con ritardo invariato.
  - Smentita se resta ≥ 10 km in ≥ 5/30.
- **avversario-2.** Un'ispezione dell'impronta, con lo stesso criterio di `avviso_spegnibile`, e la dichiarazione
  dell'area non ispezionata.
  - Smentita se dopo 60 s di vista piena l'impronta non si riduce in nessun passaggio.
- **avversario-3.** Il «libero» dentro un avviso attivo non si mostra (o si mostra «libero per ⟨classi⟩, avviso
  attivo»). La griglia si ricalcola a ogni fotogramma.
  - Smentita se il validatore trova ancora celle dentro gli avvisi.
- **avversario-4.** La famiglia sito dichiara in `classi_escluse` tutte le classi non ammesse (elicottero, aereo
  leggero, pedone, auto).

## 5. Dopo

Rifare E1 con avversario-1 (n = 60, semi 7000+), poi il validatore su un `lp_E1` scelto a caso fra i passaggi.
Programmi ed esiti in questa cartella: `cp_A.py`, `cp_E.py`, `cp_X.py`, `cp_X5.py`, `cp_X5b.py`,
`valida_video.py`, `cp_video_dettaglio.py`, e i rispettivi `*_esito.*` e `*_passaggi.jsonl`.
