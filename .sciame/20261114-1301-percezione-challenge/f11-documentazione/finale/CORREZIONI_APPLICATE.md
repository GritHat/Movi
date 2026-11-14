# Correzioni applicate e non applicate a `STATO_PROGETTO.md` — versione 2 (finale di f11)

`sciame-redattore`, fase f11, 14 novembre 2026, dalle 17:21 alle 17:40 (`date -Is`). I percorsi sono relativi a `.sciame/20261114-1301-percezione-challenge/`. «Versione 1» è `f11-documentazione/unione/STATO_PROGETTO.md` (17:05, 1609 righe); «versione 2» è `f11-documentazione/finale/STATO_PROGETTO.md`. I paragrafi indicati («§») sono quelli del documento.

## 0. In testa

**Esito.** Applicate tutte le correzioni chieste dalle tre verifiche delle cifre e le correzioni S1–S6 della verifica dei riferimenti, salvo le dodici del §2, che non si potevano applicare da questa cartella o che spettano all'arbitro. Nessun contenuto tolto: dove una cifra cambia, la riga dice che cosa scriveva la versione 1. **Niente è provato sull'hardware:** le correzioni riguardano trascrizioni, stati e rimandi di un testo su simulazioni, conti e schede, a sensore fermo.

**Cambi di stato scritti nel documento** (li decide l'arbitro; il testo è già indebolito).
1. «Lato della zona dei sensori a tempo di volo a 2 m: 13 e 10 cm»: **smentito** da un conto (26 e 20 cm), nel modello geometrico della zona quadrata.
2. «Nascono F-301…F-311, K-301…K-309»: **smentito** dal file (F-301…F-309, K-301…K-308).
3. Limiti geometrici di B1: da «dimostrato» a **conto** (camera ideale, altezza di 1,2 m ipotizzata).
4. «0 passaggi falliti su 14 400»: da «sostenuto in simulazione» a **misura su 4800 passaggi (ombra a −20 cm), per costruzione sugli altri 9600**.
5. «Area prevista ancora mostrata: in tutti i casi sotto il 20 %»: **smentito** dai file (28–72 % con il pannello da 0,5 m).
6. «La traccia della challenge ha sei righe»: **smentito** (5, di cui una vuota).
7. «In due studi l'aptico costa più dell'audio»: scritta ora come «studi discordi»; lo stato «smentita come scritta» resta proposto all'arbitro.
8. «Tre pratiche consolidate usano il principio del nucleo»: indebolita in «tre pratiche del dominio usano un principio analogo; fonti non vagliate».
9. Cifre del cap. 3 prese da f10 e f9: da senza marca a **[prel.]**; cifre di f6 nei cap. 1–3 e 8: con «non vagliato dall'arbitro (f6)».

**Previsioni** (scritte alle 17:23 in `f11-documentazione/finale/stato.md`, prima di applicare). F1 (almeno 16 cifre contestate su 18 coincidono con il file riaperto): **regge**, 18 su 18. F2 (nessun numero perso non dichiarato): **regge**, tre numeri con un'occorrenza in meno, dichiarati. F3 (percorsi): **regge**. F4 (chiavi con riga e numero): **regge**, 85 su 85. F5 (marche di f6 e [prel.]): **regge**. Dettaglio nell'appendice C del documento.

**Regole e scostamenti.** Scritto solo in `f11-documentazione/finale/` (`STATO_PROGETTO.md`, questo file, `stato.md`). Niente git. Rete non usata: nessuna fonte riaperta da me. Nessuna simulazione rieseguita; un lancio in sola stampa di `f10-dati/02-sensori/controlla_parametri.py`, di cui non ho letto l'uscita. Lunghezza oltre le due pagine: la consegna chiede l'elenco di ogni correzione. Regole violate: nessuna che io sappia.

**Indipendenza.** Condivido con il documento l'autore (un'altra istanza dello stesso ruolo), il modello linguistico e i file dello sciame; con i verificatori il modello linguistico. Ho riaperto i file per le cifre contestate, non ho rifatto le verifiche.

**Come leggere la colonna «Prova».** «Riaperto» = ho ritrovato io la cifra o la frase nel file indicato. «Dalla verifica» = accolta sulla parola del verificatore, che cita il file; nel documento porta «secondo la verifica-…».

## 1. Correzioni applicate

### 1.1 Verifica 1 (`f11-documentazione/verifica-1/VERIFICA.md`, righe 1–536 della versione 1)

| Sigla | Dove | Che cosa è cambiato | Prova |
|---|---|---|---|
| a1, d1 | §3.2, tabella dei sensori a tempo di volo; §3.8, punto 12 | lato della zona a 2 m da 13 e 10 cm a **26 e 20 cm**, con la nota sull'errore del file d'origine | riaperto `f10-dati/02-sensori/controlla_parametri.py`, riga 84 (`200*tan(passo/2)`); conto rifatto: 0,262 e 0,196 m |
| a2 | riquadro in testa; legenda delle sigle; §9.2 | F-301…F-309, K-301…K-308 | riaperto `f9-preproposta/13-verdetto/VERDETTO_PREPROPOSTA.md`, riga 5 |
| a3, d3 | §2.2, B8 | le voci della latenza sono quattro (mancava «evento → inizio esposizione, 0–33 ms»); le tre scritte sommavano 138,3 ms | riaperto `f3/H-012/02-validazione/VERIFICA.md`, righe 67–68 e 74; la media di 16,7 ms è un conto della verifica |
| a4 | §1.4, punto 4; §6.1 | k* da 0,33 a 0,38 vale «in 24 ore»; aggiunti i valori a 36 e 48 ore | riaperto `f9-preproposta/11-pianificatore/CONSEGNA.md`, riga 57 |
| b1, d2 | §2.2, B1 | «[DIM]» diventa «[CONTO] geometrico», con le ipotesi | dalla verifica (cita `f4/H-012/09-arbitro/VERDETTO.md`, §3, e `CONTROPROVE.md`, in testa) |
| b2 | cap. 3 | frase in testa al §3.2 e marca [prel.] nelle 33 righe che citano f10 o f9 senza averla | controllo meccanico mio: 0 righe senza marca dopo la correzione |
| b3 | §1.4 punto 6; §2.2 B3, B5, B7, B9; §3.4; §3.5; §3.6 | aggiunta «non vagliato dall'arbitro (f6)» | lettura del documento |
| b4 | §3.2, camere stereo | «l'unica terna» diventa «l'unica terna trovata dal ruolo» | riaperto `f1/985ccd9bca46/CONSEGNA.md`, riga 47 |
| b5 | §3.2, sensori a tempo di volo | «solo I2C» vale per L7CX e L8CX; L5CX non verificato | riaperto `f10-dati/04-embedded/PREVISIONI.md`, riga 51 |
| b6 | sintesi; §1.5; §4.2, riga 3 | «due calcoli indipendenti» diventa «due ruoli dello stesso modello; il valore a 10 Hz poggia su un'ipotesi» | riaperto `f1/985ccd9bca46/CONSEGNA.md`, righe 28–29 |
| b7 | legenda; sintesi; §1.3; §2.2 B5; §4.1.6; §4.2 | «al 95 % di confidenza» accanto ai limiti; 13 su 4800 = 0,27 %, limite 0,43 % | riaperto `f4/H-012/03-validazione/MISURE_V2_bis.md`, riga 17; 0,27 % è un conto |
| b8 | sintesi; §5.2 | «tre aggiunte leggere» diventa «tre aggiunte fra le nove voci della fascia 14 ore» | riaperto `f7-estensione/10-triage/TRIAGE.md`, righe 19–42 |
| c1 | §3.4, cono cieco in alto | 1,95 m: uscita non salvata dello script; file che la portano | riaperti `f6-specializzazione/03-avversario/risultati_spec.txt`, riga 40, e il triage di f7, F-108 |
| c2 | §3.4, anello cieco | 1,04 m a 20°: file giusto | riaperto `f2/04-torneo/esito_attacchi_parte1.txt`, riga 31 |
| c3 | §3.2, camere a tempo di volo | Arducam: file giusto | riaperto `f1/dfac83300259/CONSEGNA.md`, righe 18–19 |
| c4 | §3.2, LiDAR | campo e portata del Livox: tabella della consegna, non la previsione P9 | dalla verifica |
| c5 | §1.2 | «7 frasi»: file giusto; righe corrette (vedi verifica 3, a1) | riaperto `regole_challenge.md` con `wc -l` (5) |
| c6 | §2.2, B1 | «58° in orizzontale»: viene dalla versione 1 della soluzione | riaperto `f3/H-012/01-scene-dinamiche/SOLUZIONE.md`, riga 52 |
| d4 | §2.2, B4; §4.1.2; §4.2, riga 6; §4.4, punto 12 | 0,902 è la fascia 1,5–2,5 s (n = 1616); 0,890 sull'intero | riaperto `f2/04-torneo/risultati_A_parte2.txt`, righe 34 e 37 |
| d5 | §3.2, tabella delle camere; §3.8, punto 10 | Gemini 335: 0,26–3 m (pagina) contro 0,3–3 m (scheda); errore dichiarato di natura diversa; origine del limite di scheda | riaperti `f3/fonti/FONTI_VERIFICATE.md`, riga 29, `parametri_sensori.json`, riga 256, `MODELLO_SENSORE.md`, riga 12 |
| e1 | sintesi; §1.3, R7; §2.2, B8; §3.4 | il confronto 155 ms (media) contro 150 ms (95° percentile) non è alla pari; la misura di R7 copre solo il terzo tratto | riaperto `f3/H-012/02-validazione/VERIFICA.md`, righe 68 e 74 |
| e2 | sintesi; §1.3, R1; §2.2, B3 | 100 / 85,9 / 26,6 % vale in avvicinamento; di traverso 100 % | riaperto `f4/H-012/03-validazione/v2_MOB.txt`, righe 3, 5, 7 |
| e3 | §2.2, B5; §2.3, invariante 4 | il 28,2 % è misurato con il pannello da 0,5 m a 1,5 m | riaperto `f4/H-012/01-avversario/risultati_a05.txt`, intestazione |
| e4 | §1.3, capoverso nuovo | quanto prova ogni soglia (9 su 10, 5 su 5, 300 occlusioni) | riaperto `f3/H-012/02-validazione/VERIFICA.md`, righe 54, 55, 61 |
| e5 | §2.2, B5 | nota dell'arbitro sui bracci; 2 riagganci sbagliati su 1200 nella scena T | riaperti `VERDETTO.md`, riga 5, e `MISURE_V2.md`, riga 31 |
| e6 | §1.3, R2; §2.2, B1 e B2 | 85 % delle celle con un pixel sopra 0,07 m; R2 cade con la profondità allineata al colore | riaperto `f5/02-audit/AUDIT.md`, riga 27 |
| e7 | riquadro in testa; §2.2, B5; §5.2; §5.3 | controllo rifatto alle 17:24; nominati i file nuovi; «ciclo di vita del nucleo (B5): smentito» del torneo di f8 | riaperto `f8-continuita/12-torneo/TORNEO.md`, riga 9; teste dei file nuovi |
| e8 | §2.2, B1; §3.8, punto 11 | f = 424 px corrisponde a 90°, non a 87° | riaperto `VERIFICA.md`, riga 80; la stampa dello script e il «5 %» sono dalla verifica |

### 1.2 Verifica 2 (`f11-documentazione/verifica-2/VERIFICA.md`, righe 537–1073)

| Sigla | Dove | Che cosa è cambiato | Prova |
|---|---|---|---|
| a1, d1 | §4.1.2, H-006 | 4,7 ms diventa 5,1 ms | riaperto `f2/04-torneo/esito_attacchi2_parte1.txt`, riga 21 |
| a2 | §6.2, rischio 8 | «392–393 su 400» diventa «392 su 392, in 392 passaggi su 400» | riaperto `f9-preproposta/05-tracciamento/CONSEGNA.md`, righe 18 e 49 |
| a3 | §4.2, riga 6 | N per ciascuno dei tre valori | come d4 della verifica 1 |
| a4 | §4.1.1, creativo | «0,1 %» diventa «1,6 % a 2 s, 0,1 % a 3 s» | riaperto `f1/e30f9e2dd4d7/esito_sim.txt`, righe 4–5 |
| a5, d2 | §4.1.5, A3 bis e A4 | D con pannello da 0,5 m: 28–72 % (d1), 0–7 % (d2); lo 0–1,5 % è un'altra misura | riaperti `MISURE.md`, riga 29, e `out_A_D_w05.txt`, riga 4 |
| a6 | §4.1.2, H-013 | la soglia di smentita vera | riaperto `f2/04-torneo/PREVISIONI_parte2.md`, riga 15 |
| a7 | §3.6, Q1; §4.2, riga 55 | 0,873–0,876° sulla finestra di 0,867 s | riaperto `f6-specializzazione/02-slam/risultati.txt`, righe 6–12 |
| a8, c3 | §4.2, riga 13 | i 12 cm sono dell'avversario, ridati dal metrologo | riaperti `TORNEO_parte1.md`, riga 9, e `conti_metrologo.txt`, riga 47 |
| b1 | §4.1.6, P1; §4.2, riga 30; §4.3, K-013; sintesi; §1.3; §2.2, B5 | misura su 4800, per costruzione su 9600 | riaperto `f4/H-012/03-validazione/MISURE_V2.md`, righe 13 e 28 |
| b2 | §4.4, punto 3 | «in tutti i casi sotto il 20 %» riscritta | riaperti `v2_C6.txt`, righe 2 e 5, `risultati_a02.txt`, righe 4–11 (lì l'estremo alto è 75,4 %, non 67,6 %) |
| b3 | §4.1.1, tracciamento | la forma a particelle e la forma semplice | riaperto `f1/992c41c8860e/PREVISIONI.md` per il 91 %; lo 0 % in sosta è dalla verifica |
| b4 | §4.1.1, visione | P3: valore atteso sbagliato | riaperto `f1/c85dbcc51ea6/PREVISIONI.md`, riga 49 |
| b5 | §4.1.5, A3 | 82,8–84,8 % con la curva pessimista | riaperto `MISURE.md`, riga 27 |
| b6 | §5.4, S11 | la prima macchina «corretta» mancava 60 avvicinamenti | riaperto `f9-preproposta/05-tracciamento/CONSEGNA.md`, riga 18 |
| b7 | §6.1, candidati al taglio | «vale il secondo» diventa «vale il quarto addendum» | lettura |
| minori | §4.2, righe 2, 10, 56 | [rias.]; [COSTR] per lo zero; [SIM] nel modello | riaperto `FONTI_VERIFICATE.md`, riga 15, per la riga 2 |
| c1 | §3.8, punto 7 | file giusto per 5,7 cm e 446,8 px | riaperto `esito_attacchi_parte1.txt`, riga 2 |
| c2 | §3.8, punto 3 | file giusti per 90°×65° | riaperti `geometria_sensori.py`, riga 16, e `INVENTARIO_E_DECISIONE.md`, riga 19 |
| c4 | §4.1.1, visione | σ ≈ 66 m/s²: conto a mano nella consegna | riaperto `f1/c85dbcc51ea6/CONSEGNA.md`, riga 14 |
| c5 | §6.1, bilancio | fonte delle 54 ore | riaperto `SOLUZIONE_V2.md`, riga 134 |
| ore non verificabili | testa del cap. 5; §5.1; §5.5 | «ora dichiarata dalla sezione» | lettura |
| d3 | §2.4; §6.1 | il 59,5 parte da un nucleo di 48 ore; la somma 80,5–87,5 parte da 54 | riaperto `11-pianificatore/CONSEGNA.md`, righe 25–31 |
| d4, d5 | testa del cap. 5; §5.1; §5.4; §1.4; §6.1 | integrato il verdetto di f9: colonna dell'arbitro, piano a 14 ore, criterio 3,1 / 4,1 / 5,2 | verdetto letto per intero |
| d6 | §5.5 | 4,04 GB comprendono i 2,8 di Friburgo, non scaricato | conto mio: 1,24 GB |
| d7 | §4.1.8; §4.4, punto 14 | 14:42:21 contro 14:41:49 | riaperti i due file di `f6-specializzazione/02-slam/` |
| e1 | §4.1.5, A2 | A2 (b) «smentita alla lettera» | riaperto `MISURE.md`, riga 25 |
| e2 | §4.1.5, A3 bis e A4 | con Pd 0,9 le misure A3–A4 non valgono | riaperto `MISURE.md`, riga 14 |
| e3 | §4.1.5, `validazione-1` | costo: falsi sul muro al 5,7–14,9 % | riaperto `MISURE.md`, riga 53 |
| e4 | §4.1.8 | aggiunte le righe S4 e S6a; S1b e S6c completate | riaperto `ATTACCO_SPECIALIZZAZIONE.md`, righe 23, 25, 27 |
| e5 | §3.6 | costo di allargare la soglia; drone al 7 % a 10–30 m | riaperto `MOTO_PROPRIO.md`, righe 48 e 70 |
| e6 | §4.1.6 | regola violata: lancio oltre i 120 s | riaperto `MISURE_V2_bis.md`, riga 39 |
| dopo la fotografia | riquadro in testa; §5.2; §5.3; §5.5; §4.5 | nominati e riassunti in testa i file nuovi di f7, f8, f10, marcati non vagliati | teste dei file (prime righe) |

### 1.3 Verifica 3 (`f11-documentazione/verifica-3/VERIFICA.md`, righe 1073–1609)

| Sigla | Dove | Che cosa è cambiato | Prova |
|---|---|---|---|
| a1, d5 | §1.2; §8.1 | 5 righe, non 6 | `wc -l` su `regole_challenge.md`; `CONTRATTO.md`, riga 27 |
| a2, d4 | §10.2, punto 1; §2.2, B5 | estremo alto «1–1,6 s»; aggiunto «da 0,8 a 5,8 s» | riaperti `QUADRO_DOMINIO.md`, riga 47, e `SOLUZIONE_V2.md`, riga 92 |
| a3, a4, d6 | appendice B | link di `codice-strada-reg-art162` e di `lupu2020` | riaperti `09-interfacce/CONSEGNA.md`, riga 80, e la voce 57 dell'elenco |
| a5 | appendice B, «Che cosa manca» | prezzo dell'Unitree L2; le voci della OAK-D Pro W e dell'Arducam esistono | riaperto il §8.3 dell'elenco |
| a6 | §8.9 | «tramite CTMAVIO» nel §1, «la controllata» in testa | riaperto `QUADRO_DOMINIO.md`, righe 7 e 18 |
| b1 | §8.3, prima frase | «pratiche consolidate» indebolita | dalla verifica |
| b2 | §10.1, riquadro 2; §3.4 | `sensori-P13` è in simulazione | riaperto `f10-dati/02-sensori/PREVISIONI.md`, riga 43 |
| b3 | §8.2 | 0,13 s «nel solo simulatore dell'avversario» | riaperto `VERDETTO.md`, riga 22 |
| b4 | §4.1.8; §8.5, C3; §10.1, riquadro 3 | 12 su 18 con la possibile presenza spenta, 18 su 18 accesa | riaperto `risultati_spec2.txt`, righe 1–2 |
| b5 | §4.1.8; §8.5, C7 | 40,5 % con il 99 % | riaperto `ATTACCO_SPECIALIZZAZIONE.md`, riga 27 |
| b6 | §8.5, C8 | fra virgolette il testo intero del file | riaperta la riga 39 |
| b7 | §8.1 | «dimostrato» diventa «conto, con il criterio scelto dal ruolo; [prel.]» | riaperto `f7-estensione/05-esperto-dominio/CONSEGNA.md`, riga 37 |
| b8 | §8.3 | [balch2019]: in f11 solo i dati bibliografici | riaperto `sez-e/PREVISIONI.md`, penultimo capoverso |
| b9 | §9.1 | «Audit (f5), verdetto (f4), cancelli» | lettura |
| b10 | §8.2; §10.1, riquadro 6, a | «studi discordi» (è anche S5 della verifica dei riferimenti) | riassunti riletti dal curatore, non da me |
| c1 | §8.2 | file per 1,95 e 1,00 m | riaperto `risultati_spec.txt`, riga 40 |
| c2 | §8.8, tappa 4 | marcata «proposta di [dom.]» | ricerca di «indossa» nel file: non c'è |
| c3 | §8.3 | «funzione solo orizzontale»: file indicato | dalla verifica (la mia ricerca nel file non l'ha ritrovata alla lettera) |
| c4, c5, c6 | §8.3 | file indicati per «avviso», I062/290 e I062/500, la frase sui radar navali | riaperti `QUADRO_DOMINIO.md`, riga 55, e `f8-continuita/07-ricercatore/FONTI.md`, righe 76 e 84 |
| c7 | §8.3, precisazione | la premessa (2,0 m/s) è non verificata; i conti tornano | riaperto `sez-e/PREVISIONI.md`, ultimo capoverso |
| c8 | §9.2 | «tre commit»: non verificato; quarto commit dal riepilogo della sessione | nessun comando git |
| c9 | §5.4 | i 161 ms hanno ora la riga del file | riaperto `f9-preproposta/02-tempo-reale/CONSEGNA.md`, riga 82: la cifra c'è |
| c10 | §8.6 | origine di «entro 24 mesi» e «diritto di salire» | riaperto `QUADRO_DOMINIO.md`, riga 20 |
| d1, e1 | testa del cap. 8; §8.2; §8.5; §8.8 | marca di f6 | controllo meccanico mio |
| d2, e2 | §8.9, punto nuovo; §8.2 | regole comuni 3-6-7-9 contro 2-3-5-9; il rilascio «mai» vale a sensore fermo | riaperti `AUDIT.md`, righe 31 e 36, e `VERDETTO.md`, riga 71 |
| d3 | §8.4; §8.6 | «nessuna passata dal curatore» precisata | conteggio della verifica |
| e3 | §8.7 | limiti mancanti nella frase «Un limite» | riaperto `proposta/proposta_sciame.tex`, riga 190 |
| e4, e5 | §8.5, C2, C3, C4, C6 | parti omesse delle correzioni; velocità di classe non verificate | riaperto `ATTACCO_SPECIALIZZAZIONE.md`, righe 33–37 |
| e6 | §2.2, B9; §10.1, riquadro 3; §6.2, rischio 7 | il v0.6 scrive già «almeno 1,5 m … a 1,7–1,9 m»; conto 1,62 e 1,67 m; decisione di f7 | riaperti la riga 160 del sorgente e la testa di `f7-estensione/13-soluzione/DECISIONE.md`; i conti sono della verifica |
| e7 | §9.1 | cancello di f3 riapprovato alle 15:05:21; f4 senza `PREVISIONI.md`; cartelle con il solo `TASK.md` | riaperti i due file `GATE_*.json` e le due cartelle |
| e8 | §8.3 | 1,68 m esito di una previsione mancata; 0,27 s di conferma | riaperto `06-esperto-dominio/CONSEGNA.md`, riga 7; i 0,27 s sono dalla verifica |
| e9 | §8.8, tappa 6 | perde il 21,4 % del libero | riaperto il triage di f7, riga 20 |
| e10 | testa del cap. 8 | che cosa il verdetto di f9 conferma e che cosa no | `grep` mio: 0 occorrenze di 2,80 e 1,68 nel verdetto |

### 1.4 Verifica dei riferimenti (`f11-documentazione/verifica-rif/VERIFICA_RIFERIMENTI.md`, §4.3)

| Sigla | Dove | Che cosa è cambiato |
|---|---|---|
| S1 | appendice B, `koschi2021` | link sostituito con il DOI |
| S2 | appendice B, `ue-2019-945`, `ue-2019-947` | link della voce per il primo, «manca» per il secondo; la pagina dell'EASA è la voce 168 |
| S4 | §10.1, riquadro 6; appendice B | «non ancora verificato» diventa «verificato alle 17:20» |
| S5 | §8.2 | frase «studi discordi» (indebolimento; lo stato resta all'arbitro) |
| S6 | registro delle modifiche | riga 2 |
| chiavi | tutto il testo | ogni chiave porta il numero della voce: 133 citazioni di 85 chiavi; nessuna chiave senza voce, quindi nessuna marca «riferimento da aggiungere» |

Le correzioni R1–R23 e B1–B12 riguardano l'elenco e il file BibTeX: le ha applicate il curatore in `f11-documentazione/finale/RIFERIMENTI.md` (291 voci, 17:36). Ho controllato con un programma che per le 85 chiavi del documento numero e stato non cambiano.

### 1.5 Aggiunte oltre le verifiche

- **Verdetto dell'arbitro su f9**, letto per intero: colonna nuova e sei capoversi nel §5.4; tabella del piano a 14 ore e criterio nel §6.1; decisioni 10 e 11 nel cap. 7; due righe nel §9.2; sintesi e legenda.
- **Rimando alla versione finale dell'elenco** (testata, appendice B).
- **Appendice C:** che cosa ha fatto la versione 2, con i controlli.

## 2. Correzioni non applicate, con il motivo

1. **Correggere `controlla_parametri.py` (riga 84) e `MODELLO_SENSORE.md` di f10** (proposta `validazione-f11-1` della verifica 1). Non applicata: sono file fuori dalla mia cartella. Il documento porta il valore giusto e segnala l'errore. Nel `MODELLO_SENSORE.md` una ricerca di «13 cm» non trova la cifra: lì l'errore resta **non verificato da me**.
2. **Una seconda marca («misura / per costruzione») per tutte le 56 righe del §4.2** (proposta della verifica 2). Applicata solo alle righe 10 e 30, le due indicate: per le altre servirebbe rileggere ogni prova.
3. **Controllo automatico riga per riga del §4.2 con `grep` sulla cifra** (proposta della verifica 2). Non fatto: è uno strumento per gli aggiornamenti, non una correzione.
4. **Riordinare le righe del §9.2** (verifica 3, d7). Non spostate: aggiunta una nota nelle due righe.
5. **Togliere la proposta di [dom.] dalla tappa 4 del §8.8** (verifica 3, c2: «marcata o tolta»). Marcata, non tolta: la consegna vieta di togliere contenuto.
6. **Le correzioni (b)–(o) dell'elenco dei riferimenti alle frasi** (§10.1, riquadro 6). Non applicate: cambiano affermazioni e spettano all'arbitro; restano segnate in riga.
7. **I cambi di stato formali** del §0: scritti come proposte; li decide l'arbitro.
8. **Integrare nei capitoli i file di f7, f8 e f10 comparsi dopo la fotografia.** Non fatto: non sono vagliati, e ne ho letto solo la testa. Sono nominati e riassunti nel riquadro in testa e nei §5.2, §5.3, §5.5, marcati.
9. **Verificare il numero dei commit** (verifica 3, c8). Non fatto: git è vietato dalla consegna.
10. **Ricontrollare sulle fonti in rete le frasi fra «» del cap. 8** e la premessa dei 2,0 m/s. Non fatto: non ho usato la rete; restano «non verificato».
11. **Verificare gli orari d'arrivo degli addendum** (§1.4). Non verificabili: nessun file li porta; restano «dedotti».
12. **Portare il punto sul pannello a chi tiene il PDF** (verifica 3, e6). Non è nella mia consegna: è scritto nel §10.1, riquadro 3, per l'arbitro e per chi tiene il PDF.

**Cifre accolte «dalla verifica», che non ho ritrovato io nel file:** la stampa di `controlla_parametri.py` sul campo dagli intrinseci e i valori in 4×4; il «5 % più basso» con 87°; lo 0 % in sosta della forma semplice (f1, tracciamento); «funzione solo orizzontale» in f7; i 0,27 s di conferma nei 1,44 m/s; le regole violate di f6; il conteggio «otto verificate e sei in parte» del §8.4; i conti 1,62 e 1,67 m del pannello.

## 3. Stati che propongo

- «La versione 2 riporta le correzioni delle quattro verifiche»: **verificato** sull'insieme elencato nel §1 (ogni sigla delle verifiche ha una riga qui o nel §2).
- «Le cifre contestate hanno ora il valore del file»: **verificato** per le 18 delle sezioni «(a)».
- «Il resto del documento è giusto»: **non verificato** da me: vale ciò che dichiarano i verificatori (98–99 % delle cifre tornava, su circa 2030 controllate).
- Tutto il contenuto resta simulazione, conto o scheda, a sensore fermo: **niente è provato sull'hardware**; ciò che viene da f7, f8, f10 e da f6 non è vagliato dall'arbitro.

## 4. Che cosa propongo dopo

1. All'arbitro: i nove cambi di stato del §0, le correzioni (b)–(o) dell'elenco, la discordanza sulle regole comuni (§8.9) e il punto sul pannello (§10.1, riquadro 3), che tocca la condizione 3 del verdetto e una frase del PDF v0.6.
2. All'autore di f10: la riga 84 dello script (proposta `redattore-f11-1`: dopo la correzione lo script stampa 26 e 20 cm in 8×8; la smentisce una scheda del costruttore con un'altra larghezza di zona).
3. Al prossimo aggiornamento (riga 3 del registro): i verdetti di f8, f7 e f10, partendo dai file elencati nel riquadro in testa.
