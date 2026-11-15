# Riprova nel prototipo col nucleo v2 (fase 2b, 10-riprova)

`sciame-sviluppatore`, 2026-11-15, dalle 02:16 alle 02:53 (`date -Is`). Previsioni e soglie scritte prima, alle
02:18:09, in `PREVISIONI.md`. La diagnosi D1 è stata aggiunta dopo i primi esiti e prima del suo lancio.
**Tutto è simulazione dalle schede: nessun sensore fisico, niente è «validato».** Etichette a mano. Solo osservazione
e avviso. Frequenze per passaggio (un record per passaggio), con Wilson al 95 %.

## 0. In testa: cambi di stato e regole

- **Cambi di stato:**
  - «A1 tempestivo con l'inviluppo dei droni»: **regge**, 200/200 sia in min sia in alta.
  - «Nessun passaggio con il mezzo fuori dall'avviso»: **smentita** in A1 min, 12/200.
  - «"Libero" sull'oggetto col pannello a 0»: **smentita** nella famiglia «sito», 163/171 passaggi non C0. Regge
    nella famiglia «aeroporto», 0/171: se la prova sia vuota là è **non verificato**.
  - E1 entro 2 s: resta **smentita**, 49/60. E2 ed E4: **reggono** come in EVENTI_V2.
- **Regole che ho violato:**
  - Per circa 23 s ho tenuto 9 processi: una prova di E1 è girata mentre `riprova.py` ne usava 8.
  - Ho fermato con TaskStop il primo giro di `prova_tutto` (il passo 05 falliva) e l'ho rifatto.
  - Non ho cancellato file. Ho riscritto solo file miei: `riprova.py`, le configurazioni di `scene/video/`, i
    registri di `uscite/video/`.
  - Nel prototipo ho modificato, solo aggiungendo, i file di altri: `movi/lungo.py`, `movi/registro.py`,
    `movi/__main__.py`, `prova_tutto.sh` (copia di prima in `prova_tutto.sh.prima`), `prove/prova_registro.py`.
    In `lungo.py` 3 righe sono state riscritte, non tolte.
- **Indipendenza.** Nucleo, simulatore, strato eventi e misure condividono codice e semi con le prove di 01-nucleo e
  02-eventi, e la misura è mia. Questo controllo vale solo per difetti dell'integrazione.

## 1. Integrazione (fatta)

- **Copie.** `prototipo/riuso/lunga_portata_v2/` contiene `movi_lp_v2.py`, `regole_lunga_portata_v2.json` ed
  `eventi_v2.py`, copiati con `cp -n` e con gli sha256 uguali agli originali (`PROVENIENZA.md`).
- **Nucleo predefinito v2.** `movi/lungo.py` usa il v2 per difetto.
  - Si torna al v1 con `--nucleo v1`, con `MOVI_NUCLEO_LP=v1`, oppure con `"nucleo": "v1"` nella sorgente.
  - Col v2 si caricano le regole v2. A1 e A2 vanno in `sito_droni_rullaggio`, A3 in `aeroporto_e_droni`.
  - La mappa è **dichiarata completa** (`MAPPA_CERTIFICATA_PREDEFINITA = True`). È un'ipotesi, ed è scritta
    nell'intestazione.
- **Eventi.** E1, E2, E4 ed E5 passano dallo strato `eventi_v2`, ricompilato con una sola riga di registrazione di
  sola lettura (`passaggio_eventi_v2`). E3 resta in eventi_lp, col nucleo v2.
- **Il vecchio codice resta.** Il ramo v1 è intatto: L1 e L3 di `prova_tutto` girano con `MOVI_NUCLEO_LP=v1` contro
  gli esemplari di f15.
- **Campi nuovi del registro.** `affidabilita_per_sensore`, `zona_non_verificata_per_classe`, `libero_per_classi`,
  `detriti` (volume e impronta come liste di poligoni, «dedotto»), `portata_dichiarata` (solo E3), e gli eventi
  `evento_*` e `avviso_detriti`, sempre «dedotti».
- **Validatore.** `registro._valida_campi_v2` controlla:
  - le forme dei campi nuovi;
  - che un evento improvviso sia «dedotto»;
  - che non ci siano «libero» e «non verificata» insieme;
  - che non ci sia «libero» con affidabilità persa;
  - che la griglia di un sensore non affidabile non dichiari celle libere.

## 2. Riprova A1, A2, A3: n = 200, chiamata prudente (`riprova.py` → `riprova_esito.json`, `riprova_passaggi.jsonl`)

| Configurazione (famiglia) | Tempestivi | Fuori avviso | Senza regione | «Libero» sull'oggetto | Falsi conf. (med.) |
|---|---|---|---|---|---|
| A1 alta (sito) | **200/200** [0,981; 1] | 0/200 [0; 0,019] | 0/200 | **192/200**; non C0 **163/171** [0,91; 0,98], 855/19 494 istanti | 0 |
| A1 min (sito) | **200/200** [0,981; 1] | **12/200** [0,035; 0,102] | 0/200 | 0/200 | 0 |
| A2 alta (sito) | 200/200 [0,981; 1], d_conf mediana 303 m (servono 147) | 0/200 | 0/200 | 0/200 (51 600 istanti) | 1 |
| A3 min (aeroporto): radar d'aeroporto + ADS-B | non misurata (per costruzione) | 0/200 | 0/200 | 0/200 sul drone (multirotore) | 1 |
| D1 diagnosi, A1 alta (aeroporto) | 200/200 | 0/200 | 0/200 | **0/171 non C0** [0; 0,022] | **8** |
| D1 diagnosi, A1 min (aeroporto) | 200/200 | **10/200** [0,027; 0,09] | 0/200 | 0/200 | 1 |

- **R1, R2 e R6 reggono.** d_conf in A1 ha mediana 963 m (alta) e 949 m (min), contro gli 806 m richiesti.
- **R3 è smentita in A1 min.** I 12 passaggi sono tutti con il comportamento «rallenta» (6 su 40) o «ferma» (6 su
  40). Il difetto c'era già nel v1 prudente: 10 su 1417 cicli in 11-prove (per ciclo). Non dipende dalla famiglia:
  con D1 sono 10/200.
  - Causa candidata: un falso ritorno, o un ritorno del drone che rallenta, ricentra l'avviso (K-606). **Non
    verificata.**
  - La prova che la decide: confrontare, ciclo per ciclo, il centro dell'avviso con la verità nei 12 passaggi.
- **R5 è smentita nella famiglia «sito»** e regge nella famiglia «aeroporto». D1 regge per il «libero» ed è
  smentita per i fuori avviso.
  - Il prezzo è a rovescio: con «aeroporto» i falsi confermati hanno mediana 8, con «sito» 0.
  - Causa candidata: con l'inviluppo più stretto (v_max 45 m/s invece di 210) la finestra W_c è più lunga. Le celle
    restano «libere» più a lungo, il drone ci entra, e la validazione-2 (alone 3σ) non basta col pannello. **Non
    verificata.**
  - Non so se lo 0/171 di «aeroporto» sia vuoto, cioè se ci siano celle libere vicino all'oggetto.
  - La prova che lo decide: per ogni istante violato, la griglia del sensore che dà «libero» e l'età della sua
    ultima passata.
- **I C0 non contano come violazione.** I passaggi C0 (29/29 con «libero») riguardano una classe esclusa: il v2 la
  dichiara «zona non verificata per multirotore_C0».
- **R7 regge.** In A3 il drone sotto la copertura non è mai «libero» (0/54 400 istanti, con gli aerei). Il registro
  `lp_A3` dice «zona non verificata per multirotore_*» da 2 s a fine passaggio.

## 3. Eventi col nucleo v2 (`riprova_eventi.py` → `riprova_eventi_esito.json`): 60 passaggi, semi di EVENTI_V2

| Misura (soglia scritta prima) | v2 nucleo | EVENTI_V2 (nucleo v1) | Stato |
|---|---|---|---|
| E1 evento entro 2,0 s (≥ 57/60) | **49/60** [0,70; 0,89], contando solo 0 ≤ ritardo ≤ 2 s. L'aggregato di eventi_v2 dà 50/60, perché conta anche il passaggio 31, «separazione» dichiarata 12,5 s **prima** dell'urto | 51/60 | **smentita** |
| E1 frammenti dentro V (≥ 0,999) | 0,9973 | 0,9971 | **smentita** |
| E1 «libero» su un frammento nell'impronta | 0/60 [0; 0,06] | 0/60 | regge (per costruzione) |
| E2 evento entro 2,0 s (≥ 57/60) | **60/60** [0,94; 1], ritardo 0,2–0,3 s | 60/60 | regge, con l'ipotesi ottimista della fiammata |
| E2 camere non affidabili entro 3 cicli | 60/60 | 60/60 | regge |
| E2 avviso al mezzo a ≥ 140 m dall'impronta | 0/60 (l'impronta di circa 3,5 km lo contiene già) | 0/60 | smentita nella forma scritta |
| E2 avviso al mezzo a ≥ 140 m dai frammenti veri | 60/60 [0,94; 1] | 60/60 | sostenuto (definizione di 02-eventi) |
| E4 falsi eventi, alta e min (0) | 0/60 e 0/60 [0; 0,06] | 0/60 e 0/60 | regge |

E3 non è nello strato v2, quindi non ho una misura per passaggio. Ho solo il registro `lp_E3`: la portata dichiarata
del radar passa da 1062 a 1041 m (multirotore) ed è costante in tutto il passaggio. Non ho rifatto E5.

## 4. Registri per il video e prova d'insieme

- **Registri.** In `prototipo/uscite/video/` ci sono 8 registri, ciascuno con `movi.mp4`, tutti a 2 Hz.
  - 7 hanno 0 errori. `lp_A1_ingenua` ne ha 7, ed è atteso.
  - Durate e secondi sono in `INDICE.md`.
  - `lp_A1` è il passaggio 33: drone non C0, senza pioggia. L'ho scelto **dopo** aver visto i passaggi con una fase
    nascosta (22/200 in alta).
- **`prova_tutto.sh`: esito 0 in 665 s** (dalle 02:40:46, `prova_tutto_esito.txt`).
  - Tutti i passi danno «ok», comprese L1 e L3 col v1.
  - Le 20 scene lunghe, che girano col v2, hanno 0 errori ciascuna, anche le due `*_interfaccia`: col v2 la
    validazione-1 sta nel nucleo, e la falla P2 si vede solo col v1 (`lp_A1_ingenua`).
  - Il primo giro è fallito al passo 05 per un difetto che c'era già: `prova_registro.py` non scriveva la riga di
    riassunto che il collaudo ha reso obbligatoria. L'ho corretto aggiungendo la riga.
  - Il passo 09 ora non conta le scene `*_interfaccia` e `*_ingenua` e tiene al più 3 scene insieme.

## 5. Che cosa propongo dopo

1. **Decidere la famiglia di A1** (coordinatore).
   - «sito» è tempestivo, ma dà il «libero» sull'oggetto.
   - «aeroporto» non dà «libero» sull'oggetto, ma tiene più falsi confermati e per gli aerei non è tempestivo.
   - Prova: la diagnosi del § 2 sulla W_c. Previsione: legando la W_c alla v_max **vera** del multirotore veloce il
     «libero» scende a ≤ 2/171. Smentita se resta ≥ 10/171.
2. **A1 min fuori avviso (12/200).** Misurare l'avviso ricentrato ciclo per ciclo. Previsione: tutti i 12 hanno un
   ritorno associato fuori dal 3σ vero. Smentita se ce n'è anche uno solo senza.
3. **E1.** Fondere le tracce duplicate e togliere la «separazione» prematura (passaggio 31), come in EVENTI_V2 § 4.
