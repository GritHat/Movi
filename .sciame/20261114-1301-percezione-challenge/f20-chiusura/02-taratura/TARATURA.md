# Taratura della perdita di confidenza nel tempo (f20-chiusura/02-taratura, `sciame-kalman`)

15-11-2026, dalle 05:37:09 (`date -Is`). Previsioni P-T1…P-T5 scritte **prima** di ogni calcolo, alle 05:37:50,
in `PREVISIONI.md`. Consegnato alle 05:46, prima della scadenza delle 06:30.

**Tutto è calcolato nel modello o su traiettorie pubbliche (ADS-B, ALFA, CMU) con un sensore simulato dalle schede.**
Nessun sensore fisico e nessuna prova su hardware. Niente è «validato» e la confidenza non è «tarata» in generale.
Solo osservazione, monitoraggio e avviso.
**Indipendenza.** Con f19/03-confidenza condivido i dati, la divisione per mezzo (seme 20261115), il simulatore del
sensore, gli istanti delle occlusioni, `stima_v4.py` (importato e non modificato), l'autore e il modello. Il codice
nuovo (`stima_v5.py`, `prove_v5.py`) è dello stesso autore: un difetto comune a tutti e due non lo vedo.

## 1. In testa: esiti delle previsioni, regole

| Previsione (soglia scritta prima) | Esito sulla metà di prova, aerei (16 mezzi, 2296 casi) |
|---|---|
| P-T1: 1–2 s, copertura al 90 % in [0,85; 0,95] | **regge**: 0,894 [0,869; 0,914], bootstrap per mezzo [0,875; 0,917] (era 0,707) |
| P-T2: accelerazione ≥ 0,85 | **smentita**: 81/107 = 0,757 [0,668; 0,828], bootstrap [0,722; 0,792] (era 0,841) |
| P-T3: scarto medio < 0,05 (smentita > 0,10) | **regge**: 0,016 (era 0,081) |
| P-T4: 0 violazioni di monotonia | C **grezza**: **smentita**, 45 violazioni su 24 traiettorie × 60 passi (aerei). La mia previsione «regge per il teorema di Anderson» era sbagliata: le medie dei regimi si separano. Col minimo progressivo: 0, **per costruzione** |
| P-T5: area a 6–10 s ≤ 1,5 × IMM attuale | **regge**: 0,28 × (r_0,9 mediano da 264 a 138 m) |

**Limite nuovo, notato dopo e non previsto.** La taratura sulla copertura complessiva **peggiora la copertura in
virata**: da 0,905 [0,859; 0,937] a 0,729 [0,666; 0,783] (aerei, tutte le fasce, 221 casi). È un limite da scrivere: un
valore giusto in media nasconde gli errori nella condizione che conta.

**Regole.**
- Ho scritto solo in questa cartella. Non ho cancellato niente. Prima di rifare `curva_video.json` ne ho copiato le
  due versioni precedenti (`curva_video_v0_*.json`, `curva_video_v1_*.json`, con gli script `_v0`, `_v1`).
- Niente git, niente sudo, niente rete. Un processo pesante alla volta (Pool da 8), sempre con `timeout`.
- **A posteriori, dichiarato:** la variante b (pesi che evolvono, `prove_v5b.py`) l'ho provata **dopo** aver visto i
  risultati della principale. Il fattore di q scelto per gli aerei, 0,25, sta sul bordo della griglia, come già in f19.

## 2. Che cosa ho cambiato (`stima_v5.py`; stato: calcolato)

1. **σ_rif²** sommata al blocco di posizione di ogni regime:
   σ²(τ) = σ0² + 2σ0v·τ + σv²·τ² + q·τ³/3 + **σ_rif²**.
   Il valore viene da una griglia {0, 10, 20, 40, 80 m} × q × {0,25; 1; 4}, scelta **solo sulla taratura**:
   - aerei: σ_rif = 20 m, q × 0,25;
   - ala fissa: 10 m, q × 4;
   - multirotori: 0 m, q × 0,25.

   Il «q × 4» proposto nel verdetto § 4 non è confermato per gli aerei. Il gonfiamento che serve sta nel termine
   costante σ_rif², non in q: questo è coerente con la verità ADS-B rumorosa e campionata in modo irregolare, che
   resta un'ipotesi non verificata.
2. **Quarto regime IMM, l'accelerazione longitudinale (CAL).** Lo strappo è bianco e anisotropo:
   Q = J(dt) ⊗ D, con D = q_long·uuᵀ + q_perp·(I − uuᵀ) e u = v/|v|.
3. **Pesi fissati durante la perdita.** I μ_j restano quelli dell'istante della perdita e ogni regime si propaga da
   solo.
4. **Ricalibrazione isotonica.** a*(α = 0,9) è il quantile 0,9 del PIT sulla taratura, per fascia di τ e per regime
   dominante alla perdita (scelta causale: il tipo di moto *futuro* non è noto al sistema). La mappa è un ECDF,
   quindi monotona.
5. **C monotona.** C̃(τ) = min_{s≤τ} C(s); il raggio della regione è il massimo progressivo. Tutte e due le correzioni
   possono solo rendere la stima più prudente.

## 3. Tabella prima/dopo (metà di prova, copertura della regione al 90 %; Wilson per caso, ottimista perché i casi sono correlati dentro un mezzo; tra graffe il bootstrap a grappoli per mezzo, 2000 ricampionamenti)

| mezzo, versione | 1–2 s | 3–5 s | 6–10 s | 11–20 s | 21–30 s | scarto |
|---|---|---|---|---|---|---|
| aerei, prima (IMM f19) | 0,71 [0,67; 0,74] {0,67; 0,74} | 0,92 [0,89; 0,94] | 0,95 [0,92; 0,97] | 0,98 [0,96; 0,99] | 0,96 [0,94; 0,98] | 0,081 |
| aerei, dopo (σ_rif + CAL + pesi fissati) | 0,93 [0,91; 0,95] | 0,87 [0,83; 0,90] | 0,84 [0,80; 0,88] | 0,89 [0,86; 0,92] | 0,87 [0,83; 0,90] | 0,031 |
| aerei, dopo + isotonica | **0,89 [0,87; 0,91] {0,88; 0,92}** | 0,89 [0,86; 0,92] {0,86; 0,95} | 0,89 [0,86; 0,92] {0,88; 0,93} | 0,89 [0,86; 0,92] {0,87; 0,94} | 0,85 [0,81; 0,88] {0,79; 0,89} | **0,016** |
| aerei, variante b (pesi che evolvono), senza isotonica | 0,93 [0,91; 0,95] | 0,88 [0,85; 0,91] | 0,87 [0,83; 0,90] | 0,95 [0,92; 0,97] | 0,93 [0,90; 0,95] | 0,032 |
| aerei, variante b + isotonica | 0,89 [0,87; 0,91] | 0,90 [0,86; 0,92] | 0,90 [0,87; 0,93] | 0,91 [0,87; 0,93] | 0,88 [0,85; 0,91] | 0,007 |
| ala fissa, prima / dopo + isotonica | 0,91 / 0,93 [0,90; 0,95] | 0,93 / 0,93 | 0,96 / 0,93 | 1,00 / 0,91 [0,85; 0,94] | 1,00 / 0,92 [0,86; 0,95] | 0,058 / 0,023 |
| multirotori, prima / dopo + isotonica | 0,95 / 0,91 [0,89; 0,92] | 0,99 / 0,91 | 1,00 / 0,89 | 1,00 / 0,90 | 1,00 / 0,91 [0,89; 0,93] | 0,089 / 0,007 |

**Aerei per tipo di moto** (il tipo è letto dalla verità *dopo* la perdita, quindi serve solo alla prova):

| tipo | prima | dopo + isotonica | variante b senza isotonica |
|---|---|---|---|
| virata, tutte le fasce (n 221) | 0,905 [0,859; 0,937] | 0,729 [0,666; 0,783] **L** | 0,824 [0,768; 0,868] |
| accelerazione, tutte le fasce (n 107) | 0,841 [0,760; 0,898] | 0,757 [0,668; 0,828] **L** | 0,841 [0,760; 0,898] |

**Area della regione al 90 %, aerei** (r_0,9 mediano, dopo + isotonica rispetto a prima):
- 1–2 s: 39 m contro 27 m (2,2 volte l'area). È il prezzo della copertura giusta.
- 6–10 s: 138 m contro 264 m (0,28 volte).
- 21–30 s: 1106 m contro 2065 m (0,29 volte).

Stati: tutte le cifre sono **su dati pubblici con un sensore simulato**. La formula vale **nel modello**.

## 4. Curva per il video (`curva_video.json`)

Il file contiene C(τ) e r_0,9(τ) da 0 a 30 s, a passi di 0,5 s, per due casi:
- un aereo a 210 m/s, regione sferica r0 = 150 m;
- un drone a 45 m/s, con i parametri dell'ala fissa, r0 = 80 m.

Contiene anche la formula esatta, la C grezza e le violazioni, e la **banda osservata** per fascia (copertura
[Wilson] {bootstrap per mezzo} e il r_0,9 mediano reale).

Le traiettorie sono **sintetiche e rettilinee**, con 60 s di inseguimento a 1 Hz.
- Aereo: r_0,9 va da 35 m a 0 s a 177 m a 30 s; C con r0 = 150 m va da 1,00 a 0,71.
- Drone: r_0,9 va da 40 a 1257 m; C passa sotto 0,5 fra 8 e 10 s.

**Avvertenza da mettere accanto alla curva.** Per l'aereo il caso rettilineo è il più favorevole: il r_0,9 mediano
sui casi reali a 21–30 s è di 1106 m, non di 177. Nel video si mostri la banda reale accanto alla curva, con
l'etichetta «Schematic: calcolata nel modello, verificata su traiettorie ADS-B con un sensore simulato».

## 5. Stati proposti

| enunciato | stato |
|---|---|
| kalman-6: con σ_rif = 20 m la fascia 1–2 s degli aerei passa da 0,71 a 0,93; con l'isotonica a 0,89 [0,87; 0,91] | su dati pubblici, sensore simulato; **I** (stima ≥ 0,80, limite inferiore ≥ 0,70) |
| kalman-7: scarto medio a 0,9 da 0,081 a 0,016 (0,007 nella variante b, a posteriori) | su dati pubblici; I |
| kalman-8: la copertura complessiva giusta peggiora la virata (0,73) e l'accelerazione (0,76); il regime CAL non basta | **L**, su dati pubblici |
| kalman-9: la C grezza della miscela non è monotona; il minimo progressivo lo è | dimostrato per costruzione; 45 violazioni grezze su 1440 passi (calcolato) |
| kalman-10: la causa a 1–2 s è il rumore della verità ADS-B | **non risolto**: σ_rif lo assorbe, ma non lo distingue da una latenza. Lo deciderebbe una verità più pulita (registrazioni di bordo) |

## 6. Che cosa manca, e che cosa propongo

**Non fatto in 40 minuti:**
- la C del nucleo v4 sui registri F1/F6 att (soglia del verdetto: con C ≥ 0,9, copertura osservata ≥ 0,80);
- la verifica dei 76 casi di violazione nei registri F2, F3 ed F5.

Lì la regola del minimo progressivo è pronta (`stima_v5.minimo_progressivo`) ma **non applicata né provata**.

**Proposte, ciascuna con la prova che la smentirebbe:**
1. **Presentare la variante b senza isotonica** come compromesso (1–2 s 0,93; virata 0,82; accelerazione 0,84;
   scarto 0,032). È smentita se su una seconda divisione dei mezzi lo scarto supera 0,05.
2. **Ricalibrazione condizionata a una manovra rilevata in modo causale** (varianza dell'innovazione negli ultimi
   10 s), invece che al solo regime dominante. Prevede la virata ≥ 0,85 con lo scarto < 0,05; è smentita se la virata
   resta sotto 0,80.
3. **Ripetere con 5 divisioni per mezzo e semi diversi**, prima di parlare di cifre stabili: una sola divisione non
   basta per dire «tarato».

**Frase per la giuria (I).** «Dopo la perdita, la regione al 90 % ha contenuto un aereo reale da 85 a 89 volte su
100 in ogni fascia da 1 a 30 s (16 aerei, sensore simulato). In virata, 73 su 100: è un limite dichiarato.»
