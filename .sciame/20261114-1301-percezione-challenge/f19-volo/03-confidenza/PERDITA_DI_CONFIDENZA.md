# Perdita di confidenza nel tempo dopo la perdita di continuità, e stima IMM per aerei e droni veloci

Ruolo: sciame-kalman (scheda 42), fase 3, f19-volo/03-confidenza. Data: 15-11-2026. Previsioni scritte prima, alle 04:38:08+01:00, in `PREVISIONI.md`.
Tutto è **calcolato** (formule, quadratura) o **su dati pubblici con rumore di sensore simulato** (traiettorie ADS-B e di droni; sensori dalle schede f15). Nessuna prova su hardware. Solo osservazione, monitoraggio e avviso.

## 0. Cambi di stato e regole

- **P1 regge** (integrale esatto), **P2 regge** (t_C dalla cubica). **P3 regge** per il CV (aerei veloci 4 fasce su 5 in [0,80; 0,97]; droni ad ala fissa 3 su 5). **P4 smentita**: l'IMM non riduce l'errore del punto né l'area sugli aerei a τ 11–30 s; migliora invece la copertura in virata (da 0,31–0,42 a 0,92–0,96). **P5 smentita per gli aerei**: lo scarto più grande è nella fascia corta (1–2 s), non in quelle lunghe.
- Regole: nessun file cancellato, niente git. Una cosa fatta dopo aver visto i dati: una seconda taratura con la griglia allargata (`griglia_estesa/`), perché il fattore scelto per il CV stava sul bordo della griglia. La segno come **a posteriori**; i risultati principali sono quelli della prima griglia.

## 1. Derivazioni (stato: dimostrato nel modello dichiarato)

**Modello.** L'oggetto non è più osservato da t0. Per ciascun asse il moto è a velocità quasi costante (accelerazione bianca di densità spettrale q). All'ultimo aggiornamento la covarianza di posizione e velocità è [[σ0², σ0v],[σ0v, σv²]]. Senza misure la previsione è lineare e gaussiana: Φ(τ) = [[1, τ],[0, 1]] e Q(τ) = q·[[τ³/3, τ²/2],[τ²/2, τ]]. Ne segue la varianza di posizione

  σ²(τ) = σ0² + 2σ0v·τ + σv²·τ² + q·τ³/3.

Lo stesso vale in forma matriciale: P(τ) = Φ P0 Φᵀ + Q(τ), e la posizione x(τ) ~ N(m(τ), Σ(τ)).

**Regione isotropa centrata sulla previsione.** Se Σ = σ²I, allora |x − m|²/σ² segue un chi-quadro a d gradi.
- 2D, disco di raggio r: **C(τ) = 1 − exp(−r² / 2σ²(τ))**.
- 3D, sfera di raggio r: **C(τ) = erf(k/√2) − √(2/π)·k·e^{−k²/2}**, con k = r/σ(τ).

**Tempo di soglia.** Sia k_α la radice del chi-quadro: k_α = √(−2 ln(1−α)) in 2D (2,146 per α = 0,9; 1,177 per α = 0,5); in 3D si trova per bisezione (2,500 per α = 0,9). C(τ) ≥ α equivale a σ²(τ) ≤ (r/k_α)². Il tempo di soglia t_C è quindi la più piccola radice reale positiva della cubica

  (q/3)·t³ + σv²·t² + 2σ0v·t + σ0² − (r/k_α)² = 0

(t_C = 0 se σ0 ≥ r/k_α). Il raggio che tiene il livello α (la regione che cresce) è **r_α(τ) = k_α·σ(τ)**; per τ grande cresce come τ^{3/2}·√(q/3)·k_α.

**Caso anisotropo, regione ellissoidale qualunque.** La regione è E = {x : (x − c)ᵀA⁻¹(x − c) ≤ 1}. Si pone A = LLᵀ e z = L⁻¹(x − c), che porta E nella palla unitaria. Poi si diagonalizza L⁻¹ΣL⁻ᵀ = U diag(λ) Uᵀ, con μ = UᵀL⁻¹(m − c). Ne segue C = P(Σ λ_i (y_i + μ_i/√λ_i)² ≤ 1), con y_i normali standard indipendenti: un chi-quadro generalizzato non centrato. La riduzione esatta:
- 2D: C = ∫ φ_1(z1) [Φ((h − μ2)/s2) − Φ((−h − μ2)/s2)] dz1, con h = √(1 − z1²);
- 3D: lo stesso integrale annidato, con la corda interna h2 = √(h1² − z2²).

Con z = sin θ la funzione integranda diventa liscia (sparisce la singolarità della radice agli estremi), e la si integra con Gauss–Legendre a 64 nodi sull'intervallo tagliato a ±9 deviazioni standard. Il risultato è esatto a meno della quadratura e di erfc, che ha errore relativo < 1,2·10⁻⁷. Questo copre la regione fissa nel mondo (c fisso, per esempio la zona dichiarata al momento della perdita) e quella che segue la previsione (c = m(τ)). Un'alternativa è la serie di Ruben o l'integrale di Imhof, non usati qui. Un'approssimazione rapida, non usata, è il «σ equivalente» √(λ1λ2): sbaglia quando λ1/λ2 è grande, cioè proprio per gli aerei, lunghi lungo la rotta e stretti di traverso.

**Più regimi.** Con i regimi j (rettilineo, virata coordinata, accelerazione) di peso μ_j(τ) e gaussiane N(m_j, Σ_j):

  **C(τ) = Σ_j μ_j(τ) · P_j(x ∈ E)**.

È esatta *per la miscela*. La miscela, però, è un'approssimazione della vera densità a regimi che si alternano: c'è la fusione dei momenti nell'interazione IMM e la linearizzazione (EKF) della virata. Durante la perdita i pesi evolvono con la catena di Markov, μ(τ+h) = Π(h)ᵀμ(τ), con Π_jj = e^{−h/T}. Per τ ≫ T i pesi tendono a 1/3 ciascuno: la regione si allarga per effetto dei regimi più dispersi. È la causa dell'eccesso di prudenza misurato al §3.

**Verifica numerica** (`prove_confidenza.py`, `prove_confidenza.json`; stato: calcolato):
- contro le forme chiuse, scarto massimo 1,4·10⁻⁸ in 2D e 7,6·10⁻⁸ in 3D, su 20 coppie (σ, r) per dimensione;
- contro Monte Carlo (10⁶ campioni, seme 20261115) su 20 casi anisotropi e fuori centro: tutti nell'intervallo al 99,9 %, |z| massimo 2,11;
- t_C dalla cubica contro la bisezione: scarto massimo 1·10⁻¹⁴ s;
- jacobiana della virata, analitica contro differenze finite: scarto massimo 8·10⁻⁴. Lo scarto si ha al passaggio della soglia |w| = 10⁻⁶ fra le due espressioni; altrove è più piccolo (non misurato caso per caso).

## 2. Stima migliorata: IMM a tre regimi (`stima_v4.py`, solo numpy)

Lo stato comune ha 10 componenti, x = [p(3), v(3), a(3), w], dove w è il tasso di virata.
- **CV:** p ← p + v·dt; a ← 0, con varianza a priori a_prior² (serve all'interazione); w si conserva. Q a blocchi q_cv·[[dt³/3, dt²/2],[dt²/2, dt]].
- **CT (virata coordinata con tasso stimato):**
  - px ← px + (vx sin wdt − vy(1 − cos wdt))/w;
  - py ← py + (vx(1 − cos wdt) + vy sin wdt)/w;
  - (vx, vy) ruotato di w·dt; quota a velocità costante; w a passeggiata aleatoria (q_w).
  - Si usa la jacobiana analitica (EKF), con il limite w → 0 in serie.
- **CA:** accelerazione di Wiener (strappo bianco q_ca), blocco 3×3 [[dt⁵/20, dt⁴/8, dt³/6], …].
- **Interazione IMM** classica: c_j = Σ_i Π_ij μ_i, μ_{i|j} = Π_ij μ_i / c_j, e la miscela dei momenti.
- **Aggiornamento** in forma di Joseph; verosimiglianza gaussiana dell'innovazione.

La sorveglianza cooperativa (ADS-B, Remote ID) entra come misura di posizione e velocità, con H = [I₃ 0; 0 I₃ 0 …], R da NACp/NACv. Il codice la accetta (argomento `H`), ma **non è provata** qui: la verità è essa stessa ADS-B, quindi la prova sarebbe circolare.

L'uscita per il registro del prototipo è `curva_confidenza(filtro, regione, taus)`, che produce un JSON con:
- τ e C(τ);
- r_0,9(τ) e r_0,5(τ);
- t_C ai livelli;
- i pesi dei regimi;
- lo stato «calcolato nel modello».

`riga_registro()` scrive la riga. Esempio calcolato: aereo a 80 m/s in virata (w = 0,03 rad/s), radar con σ 7,5 m, zona dichiarata alla perdita come disco fisso di 300 m. C resta 1,00 fino a 2 s ed è ≈ 0 a 5 s, quindi t_C(0,9) cade fra 2 e 5 s: l'oggetto *esce* dalla zona dichiarata. La regione che cresce al 90 % ha questi raggi:

| filtro | r_0,9 a 1 s | 5 s | 10 s | 20 s | 30 s |
|---|---|---|---|---|---|
| IMM | 16 m | 56 m | 153 m | 503 m | 1039 m |
| CV | 13 m | 31 m | 61 m | 141 m | 239 m |

(`prove_confidenza.json`; il CV è più stretto perché ignora la virata.)

## 3. Verifica su traiettorie reali (stato: su dati pubblici, rumore di sensore simulato)

**Dati e metodo.**
- Mezzi:
  - aerei con velocità mediana > 60 m/s (avvicinamento, decollo, sorvolo): 104 sequenze, 31 aeromobili;
  - droni ad ala fissa ALFA: 47 sequenze, 31 voli;
  - multirotori CMU: 196 voli.
- Taratura e prova sono divise **per mezzo**, con la stessa funzione `mezzo()` di f15/21-statistica e il seme 20261115.
- Sensori simulati:
  - aerei: σ 7,5 m isotropa, 1 Hz;
  - droni: radar a 1,5 km con σ_r 0,6 m, σ_az 0,75° e σ_el 1° (scheda IRIS f15; la posizione del radar è un'ipotesi).
- Occlusioni virtuali di 1, 2, 5, 10, 20 e 30 s: 8 istanti a caso per sequenza e per durata.
- La prova è il **PIT**: u = C(sfera centrata sulla previsione, con raggio pari alla distanza osservata). La verità sta nella regione al livello α se e solo se u ≤ α, quindi un solo integrale per caso dà la curva di affidabilità a ogni livello.
- Il fattore di scala di q si sceglie sulla metà di taratura (griglia 0,25, 1, 4, 16): CV 16 / IMM 4 per aerei e ala fissa, CV 4 / IMM 0,25 per i multirotori.
- Codice in `prove_reali.py`; risultati in `risultati_reali.json` e `casi_prova_*.json`; registro in `prove_reali.log` (119 s, 8 processi).

**Copertura al 90 % sulla metà di prova** (osservato [Wilson 95 %]; n casi per fascia):

| mezzo, filtro | 1–2 s | 3–5 s | 6–10 s | 11–20 s | 21–30 s |
|---|---|---|---|---|---|
| aerei, CV | 0,72 [0,69; 0,75] n733 | 0,85 [0,82; 0,88] | 0,87 [0,84; 0,90] | 0,85 [0,81; 0,88] | 0,82 [0,78; 0,86] n388 |
| aerei, IMM | 0,71 [0,67; 0,74] | 0,92 [0,89; 0,94] | 0,95 [0,92; 0,97] | 0,98 [0,96; 0,99] | 0,96 [0,94; 0,98] |
| ala fissa, CV | 0,83 [0,79; 0,86] n435 | 0,75 [0,69; 0,81] | 0,71 [0,64; 0,77] | 0,81 [0,75; 0,87] | 0,91 [0,85; 0,95] n130 |
| ala fissa, IMM | 0,91 [0,88; 0,93] | 0,92 [0,88; 0,95] | 0,96 [0,92; 0,98] | 1,00 [0,98; 1] | 1,00 [0,97; 1] |
| multirotori, CV | 0,90 [0,88; 0,91] n1555 | 0,90 [0,87; 0,92] | 0,89 [0,87; 0,91] | 0,86 [0,83; 0,88] | 0,91 [0,88; 0,93] n643 |
| multirotori, IMM | 0,95 [0,94; 0,96] | 0,99 | 1,00 | 1,00 | 1,00 |

**Aerei in virata** (copertura al 90 %; il tratto è una virata se la rotta cambia di più di 15°):

| fascia | n | CV | IMM |
|---|---|---|---|
| 6–10 s | 37 | 0,24 | 0,78 |
| 11–20 s | 71 | 0,31 | 0,96 |
| 21–30 s | 111 | 0,42 | 0,92 |

Il CV dichiara una regione più piccola dell'errore vero proprio dove l'aereo manovra: secondo la missione è un difetto, anche se l'errore mediano del CV è minore.

**Errore del punto e regione al 90 %, aerei, mediane:**

| fascia | errore CV | errore IMM | r_90 CV | r_90 IMM |
|---|---|---|---|---|
| 11–20 s | 187 m | 211 m | 577 m | 918 m |
| 21–30 s | 326 m | 412 m | 1022 m | 2065 m |

L'area della regione al 90 % (π r_90²) dell'IMM è quindi circa 2,5–4 volte quella del CV: è il prezzo della copertura. La previsione P4 (−10 %) è smentita.

**Dove la formula è esatta, dove approssima, quanto sbaglia sui dati reali.**
1. È **esatta** (a meno di 10⁻⁷) se il moto e il sensore sono gaussiani lineari come dichiarato: CV con q noto.
2. È un'**approssimazione** per l'IMM (miscela a momenti fusi, virata linearizzata), e ogni volta che q non è quello vero.
3. Sui dati reali lo scarto |osservato − 0,9|:
   - per il **CV**: aerei fino a 0,18 a 1–2 s e 0,03–0,08 oltre; multirotori ≤ 0,04 in tutte le fasce; ala fissa fino a 0,19;
   - per l'**IMM**: troppo prudente oltre 10 s (osservato 0,96–1,00 contro 0,90).

   Alla fascia **1–2 s degli aerei** entrambi i filtri sono ottimisti (0,71–0,72). **Non risolto.** Causa probabile: la verità ADS-B ha un suo rumore e una sua latenza (posizioni con età variabile, campionamento irregolare 1–4 s), che la formula non contiene. La prova che lo deciderebbe: aggiungere σ_rif² a σ²(τ) e stimarlo sulla taratura dai residui a τ ≈ 0; oppure usare una verità più pulita (registrazioni di bordo).
4. **Griglia allargata, a posteriori** (`griglia_estesa/`): il CV con fattore 64 copre gli aerei per 0,83–0,99, ma con r_90 più larghi (1111 m a 11–20 s). Nessun fattore unico di q va bene a tutte le τ: la forma τ³ del modello non è quella dei dati reali.

## 4. Stati proposti

| enunciato | stato |
|---|---|
| kalman-1: C(τ) chiusa per disco/sfera isotropa; t_C dalla cubica; r_α(τ) = k_α σ(τ) | dimostrato (modello CV gaussiano); verificato numericamente |
| kalman-2: integrale esatto su ellisse/ellissoide anisotropo, fuori centro, e miscela pesata | dimostrato per la gaussiana e per la miscela; calcolato (quadratura, errore ≤ 10⁻⁷ misurato) |
| kalman-3: sui dati reali, CV tarato per mezzo, copertura al 90 % per τ 3–30 s fra 0,82 e 0,87 (aerei) e fra 0,86 e 0,91 (multirotori) | su dati pubblici, rumore simulato; **incoraggiante** (vicino a 0,9, con intervallo), non «tarato» in generale |
| kalman-4: l'IMM rende coerente la regione in virata (0,78–0,96 contro 0,24–0,42) ma è troppo prudente a τ > 10 s | su dati pubblici, rumore simulato |
| kalman-5: a 1–2 s sugli aerei entrambi i filtri sono ottimisti (0,71–0,72) | non risolto (la verità ADS-B è il sospetto) |

Indipendenza: il simulatore del sensore, i dati e la divisione sono gli stessi di f15; il codice del filtro è nuovo (non riusa `movi_lp`). Sono condivisi l'autore e le ipotesi sui sensori.

## 5. Che cosa propongo dopo (ciascuna con la prova che la smentirebbe)

1. **σ_rif nella formula:** C con σ²(τ) + σ_rif², e σ_rif stimato sulla taratura. Prevede la fascia 1–2 s degli aerei in [0,85; 0,95]. È smentita se resta sotto 0,80.
2. **Taratura a due parametri** (q del CV per le τ lunghe, R o σ_rif per quelle corte) al posto di un fattore unico. È smentita se lo scarto medio a 0,9 non scende sotto 0,04.
3. **IMM meno prudente:** T_soggiorno più lungo durante la perdita, oppure i pesi congelati all'istante t0 (miscela a regimi fissi). Prevede la copertura a 11–30 s in [0,88; 0,95] con un r_90 almeno del 30 % più piccolo. È smentita se la copertura in virata scende sotto 0,85.
4. **Per il video:** mostrare la curva C(τ) e la regione che cresce, r_0,9(τ), dell'IMM, con le cifre come «calcolate su traiettorie reali con sensore simulato». Non vanno dette «misurate su hardware».
5. **Il problema non è tutto di filtraggio.** Dopo eventi impulsivi (collisione, detriti) il rischio principale è l'associazione: i frammenti nascono come tracce nuove. La perdita di confidenza qui derivata vale per l'oggetto seguito, non per la nube di detriti: per quella si usa l'insieme di possibile presenza dell'inviluppo (f15).
