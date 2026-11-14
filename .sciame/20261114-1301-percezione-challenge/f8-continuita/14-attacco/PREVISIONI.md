# Previsioni dell'attacco alle modifiche — `sciame-avversario`, f8, fase f4

Scritte alle **2026-11-14T16:58:37+01:00** (`date -Is`), prima di scrivere una riga del mio simulatore (`att.c`) e prima di ogni lancio.

**Che cosa avevo già visto quando le ho scritte** (va tolto dal loro valore di previsione): `MODIFICHE_CONTINUITA.md`, `BANCO_DI_PROVA.md`, `TORNEO.md`, `SOLUZIONE_V2.md`, il contratto, il codice `13-soluzione/comp.c` e `gen.h` (letti per intero), e le righe `G` dei file `13-soluzione/ris/prova_{D,T,L}.tsv`, da cui ho letto il campo `C1_riaggancio` (su «prosegue»: D 212/331, T 336/345, L 207/232). La P-av-1 quindi non è cieca sul verso in D.

**Modello della prova (mio, dichiarato prima).** Sensore fermo all'origine, pannello fermo, geometrie D / T / L delle modifiche. Corpo = disco di raggio 0,225 m (0,45 m di larghezza); la misura è il baricentro della parte visibile (fuori dal cuneo VERO) più 5 cm per asse; il gruppo c'è se è visibile almeno il 15 % del disco. **C6 sulla maschera stimata:** il gruppo è «tagliato» se un suo punto visibile sta entro una cella (0,10 m) dall'ombra STIMATA; braccio di sensibilità a 0,05 m e con il soggetto puntiforme a 0,22 m (l'emulazione del banco). Ciclo di vita com'è scritto in M1 e M2 (§2.5–2.6): senza misura, «entrata» se l'ultima misura è a meno di 0,40 m dall'ombra stimata oppure se il punto previsto è in ombra o entro 0,40 m; altrimenti 3 fotogrammi e chiusura. Riaggancio: regola «Ritorno» del nucleo (misura entro 0,40 m dall'ombra d'ingresso, a più di 0,40 m da portata e bordi del campo, una sola pendente) E porta M7 (entro 0,40 m da R90). `sd-1` com'è scritto: 400 membri, peso × 0,1 cumulato su celle viste libere oltre la fascia di 0,20 m, 3 lisciature, 90 % per scenario, pavimento, «ampio» oltre l'80 % dell'ombra o oltre 3 s (letto come agganciato: «da lì»). Generatore di traiettorie mio (decelerazioni costanti, ondulazione del passo, curva a velocità angolare costante), diverso da `gen.h`. Unità: il passaggio. τ = tempo dall'ultima misura accettata.

| # | Attacco | Previsione (misura e soglia) | La smentisce |
|---|---|---|---|
| P-av-1 | Riaggancio composto (nucleo ∧ M7) con corpo esteso e C6 a una cella, rilevamento 0,9, «prosegue» | quota delle ricomparse riagganciate con la stessa identità: D ≤ 0,70, T ≤ 0,85, L ≤ 0,85 | ≥ 0,95 in tutte e tre |
| P-av-2 | Stato assorbente: sessione di 120 passaggi (30 × prosegue, rallenta, sosta, torna, mescolati), regola 2 del §2.5 com'è scritta | la prima «identità ambigua» arriva entro i primi 15 passaggi in D e in T; dopo, 0 riagganci; tracce «previsto ampio» pendenti alla fine ≥ 100 (D) e ≥ 80 (T) | pendenti alla fine ≤ 5 |
| P-av-3 | Tutto insieme (A-sd-1, A-sd-2 dell'autore): T, corpo 0,45 m, ombra stimata −20 cm, rilevamento 0,7, M1 + `sd-1` | R90 su «prosegue» < 0,80 a 1 s e a 2 s (C6 non scatta mai: fra corpo tagliato e ombra stimata restano due celle); centro nascosto fuori da R100: 0 passaggi; passaggi con il soggetto nascosto senza traccia pendente ≤ 3 %. Braccio di base (e = 0, rilevamento 0,9): ≥ 0,85 a 1 e 2 s | con −20 cm resta ≥ 0,85 a 1 e 2 s |
| P-av-4a | «Sbircia»: si ferma 5 s con il centro entro ± 0,15 m dal bordo vero (corpo tagliato, in parte visibile), T | cicli «osservato» durante la sosta: 0 %; R90 contiene il centro in meno di 0,60 dei passaggi a 2 s | R90 ≥ 0,85 a 2 s |
| P-av-4b | Fermo in piena vista a 0,33–0,40 m dall'ombra per 10 s, rilevamento 0,9 | mediana ≥ 8 cambi di stato osservato ↔ previsto per passaggio (un segnale sonoro l'uno); il pavimento («ampio») in almeno metà delle false entrate | mediana ≤ 1 |
| P-av-5a | Taratura: «sul percorso» con curva dolce a velocità angolare costante, T | R90 a 2 s: ≥ 0,85 a 3°/s; < 0,85 a 6°/s; < 0,60 a 10°/s | ≥ 0,85 a 10°/s |
| P-av-5b | Libreria di 30 camminate di camminatori «calmi», prova su camminatori «vivaci» (ondulazione 5 cm, velocità ± 10 % al passo), dritti, T | R90 a 2 s ≥ 0,80 (prevedo che tenga); con la libreria dei vivaci ≥ 0,88 | < 0,80 con la libreria dei calmi |
| P-av-6a | Il punto ibrido arretra: «prosegue» con almeno un passo indietro > 5 cm | D ≥ 15 % dei passaggi; T ≤ 8 % | D < 5 % |
| P-av-6b | La croce in «ampio» informa? Errore mediano della croce / errore mediano di un segno fisso al baricentro dell'ombra, nei cicli «ampio», miscela sul percorso | D: rapporto ≥ 0,8 (non informa più di un segno fisso); T: < 0,8 | D < 0,5 |
| P-av-6c | Salto alla ricomparsa: prima misura a più di 0,40 m da R90, sul percorso | ≤ 3 % (regge) | > 10 % |
| P-av-7 | Demo: D, «prosegue» fra 0,8 e 1,5 m/s, corpo 0,45 m | il segno passa ad «ampio» prima della ricomparsa in ≥ 30 % dei transiti; area di R90 / ombra all'ultimo ciclo nascosto, mediana ≥ 0,70 | < 10 % dei transiti |
| P-av-8 | Costo: passo di `sd-1` in Python puro (T), e in C con le pendenti accumulate | Python: ≥ 3 ms per traccia e ciclo (mediana); 3 tracce > 6,7 ms (A-sd-7 smentita); 10 tracce ≥ 30 ms. C: 10 tracce ≤ 2 ms (regge); 60 pendenti ≥ 4 ms al 95º percentile | Python, 10 tracce ≤ 6,7 ms |
| P-av-9 | «A prescindere dal sistema»: maschera stimata ruotata dall'errore d'imbardata, T, corpo, rilevamento 0,9 | tremolio di 2° per ciclo: R90 a 2 s sul percorso < 0,85. Scostamento fisso di 3° (0,21 m a 4 m): centro nascosto su una cella «vista libera oltre la fascia» in ≥ 20 % dei passaggi; fuori da R100: 0 a 3°, ≥ 1 passaggio a 6° | a 2° di tremolio R90 ≥ 0,90 |
| P-av-10 | Due tracciati nella stessa ombra, in versi opposti | per la regola 2 com'è scritta: 2 «identità ambigue» su 2, quattro oggetti a schermo per due persone, 2 pendenti senza chiusura (stesso ramo di P-av-2: lo eseguo dentro la sessione) | un riaggancio con identità |

Semi: libreria e tarature 100000+, prova 200000+ (mai usati da altri file dello sciame). Ogni lancio con `timeout 120`.

## Esiti (aggiunti DOPO le prove; ciò che sta sopra questa riga non è stato toccato)

Aggiunti alle 2026-11-14T17:19:18+01:00. File: `ris/<nome>.txt`. «Prosegue» salvo dove detto; tre numeri = D / T / L.

| # | Esito | Numeri |
|---|---|---|
| P-av-1 | **regge** | riagganciati 102/273, 306/397, 250/332 = 0,37 / 0,77 / 0,75 (`base_*`) |
| P-av-2 | **mista** | prima ambigua al passaggio 1 (D) e 4 (T); poi 0 riagganci su 66 e su 100; pendenti alla fine 87 (D: sotto la mia soglia di 100) e 117 (T) (`sess_*`) |
| P-av-3 | **regge** | R90 0,37 a 1 s e 0,28 a 2 s (`tutto_T`); base con maschera esatta 0,99 e 0,93 (`base_T`); fuori da R100: 0; scoperti 9 su 400 |
| P-av-4a | **mista** | «osservato» mai (per costruzione di C6); R90 a 2 s 0,98, non < 0,60: questa metà è smentita (`sbircia_T`) |
| P-av-4b | **mista** | 9 cambi di stato in mediana, di cui 7 fra osservato e previsto (previsti ≥ 8); pavimento nel 32 % delle false entrate (previsto ≥ 50 %); con rilevamento 0,7: 21 cambi (`fermo_T*`) |
| P-av-5a | **mista** | T a 2 s: 0,90 / 0,87 / 0,73 a 3 / 6 / 10 °/s (previsti < 0,85 a 6 e < 0,60 a 10: smentiti); L a 3 s: 0,84 / 0,68 / 0,43 (`curva_*`) |
| P-av-5b | **smentita** (la tenuta) | 30 calmi su vivaci: 0,73 a 2 s, sotto 0,80; vivaci su vivaci 0,93 (`lib*`) |
| P-av-6a | **mista** | D 29 % (previsto ≥ 15); T 13,5 % (previsto ≤ 8: smentito) |
| P-av-6b | **mista** | D: 0,45 contro 0,41 m (rapporto 1,1); T: 0,67 su «prosegue», ma 1,04–1,13 su rallenta, sosta, torna |
| P-av-6c | **regge** | prima misura oltre 0,40 m da R90: 2/273, 1/397, 1/332 |
| P-av-7 | **regge** | 271/279 transiti con «ampio» prima della ricomparsa; area all'ultimo ciclo nascosto 1,04 dell'ombra (`demo_D`) |
| P-av-8 | **smentita** | Python puro: 0,6 ms per traccia, 1,8 ms con 3, 5,3 ms con 10 (95º: 6,2) (`tempo_py`); C: 0,61 ms con 10 (regge), 2,9 ms con 60 pendenti (previsto ≥ 4) |
| P-av-9 | **mista** | tremolio di 2°: 0,56 a 2 s (regge); scostamento di 3°: centro su «visto libero» in 0 passaggi (smentita); fuori da R100: 0 anche a 6° (smentita) (`imb_*`) |
| P-av-10 | **non eseguita come scritta** | due soggetti insieme non simulati; il ramo della regola è eseguito nella sessione (P-av-2) |

**Notato dopo, non previsto:** chi parte da fermo accanto al pannello (R90 0,11 / 0,16 / 0,26 a 1 / 2 / 3 s in T, `fermo_T`); il corpo in parte visibile nel 21–45 % dei cicli «previsto»; scoperti 130 su 1581 con rilevamento 0,7 e corpo esteso; R90 a 1° di tremolio 0,76 a 2 s. I bracci `dopo_*` (correzioni) sono stati scritti e lanciati dopo aver visto questi esiti.
