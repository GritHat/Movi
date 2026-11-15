# Attacco alla fase 3 (volo veloce): confidenza, hardware, scenari, riclassificazione

`sciame-avversario` (scheda 34), f19-volo/20-attacco, 15-11-2026, dalle 05:26 alle 05:45 circa (`date -Is`). Le previsioni
PA1–PA8 sono state scritte **prima** dei conti, alle 05:28:03, in `PREVISIONI.md`. Il codice è mio:
- `attacco_adsb.py` → `attacco_adsb.json`: rilegge i casi di prova di 03-confidenza;
- `attacco_frammenti.py` → `attacco_frammenti.json`: importa `eventi_volo` e `frammenti.py` senza toccarli, 10
  passaggi per variante, seme 20261134.

Tutto è **simulato** o **su dati pubblici con rumore di sensore simulato**. Nessun hardware. Solo osservazione e avviso.

**Indipendenza.** Condivido con gli autori i casi di prova (gli stessi u e gli stessi tipi di moto), il volume
`frammenti.py` e la fisica dei frammenti. Il mio attacco trova i difetti di copertura e di parametri, non quelli del
modello fisico comune.

## 0. In testa: cambi di stato, regole

- **Reggono** (l'attacco è riuscito): **PA1, PA2, PA3, PA4, PA5, PA7**. **Smentite** (l'attacco è fallito): **PA6**
  (F3 al bordo resta dentro) e **PA8** (un errore di 8 m/s sulla vc dichiarata non fa uscire i frammenti).
- **Regole.** Nessun file cancellato. Niente git, niente sudo, nessuna rete: le fonti dell'hardware **non** le ho
  riaperte, e le cito come le cita 02-sensori-hw. Un processo alla volta. Ho scritto solo in questa cartella.
- **Limite del mio conto ADS-B.** I casi non portano l'identificativo della sequenza: ci sono 8 istanti per sequenza
  e 31 aeromobili. Il Wilson **per caso** è quindi **ottimista**, perché i casi sono correlati. Non ho potuto
  calcolarlo per aeromobile, come chiederebbe la regola «Wilson per passaggio».

## 1. Critiche, con la prova

**1. La formula di C(τ) è esatta nel suo modello, ma promette troppo fuori dal modello, sui dati ADS-B (PA1, PA2,
PA3 reggono).** La derivazione (σ² = σ0² + 2σ0v·τ + σv²·τ² + q·τ³/3, chi-quadro, cubica di t_C) è corretta: non
trovo errori. Il problema è dove la si applica. Le cifre seguono, tutte su dati pubblici con rumore simulato, Wilson
per caso, quindi ottimista:
- **IMM, aerei in virata, τ 6–10 s:** la regione al 90 % contiene il vero in 29/37 casi, cioè 0,784 [0,628; 0,886].
  Anche il limite superiore resta sotto 0,90.
- **IMM, aerei in accelerazione, τ 1–2 s:** 2/6, cioè 0,333 [0,097; 0,700].
- **IMM, droni ad ala fissa in virata, τ 1–2 s:** 0,834 [0,771; 0,883].
- **CV in virata, aerei:**
  - 6–10 s: 0,243 [0,134; 0,401];
  - 11–20 s: 0,31 [0,21; 0,43];
  - 21–30 s: 0,41 [0,32; 0,51].
- **Livello 50 %, aerei, τ 1–2 s:** il CV contiene il vero in 0,393 [0,358; 0,429] dei casi, l'IMM in 0,363
  [0,329; 0,398]. La curva sbaglia la **forma**, non solo un livello: è ottimista nei primi secondi e troppo
  prudente oltre i 10 s (l'IMM al 50 % arriva a 0,88). Al livello del 90 % i due errori si compensano in parte, e la
  tabella di 03-confidenza lo nasconde.
- **Caso reale singolo in cui la curva promette più di quanto si osserva** (`attacco_adsb.json`, chiave
  `peggiori_imm_manovra`). È un aereo in accelerazione con v0 = 25,4 m/s, quindi probabilmente in corsa di decollo,
  dentro una sequenza classificata come «veloce» perché la sua velocità **mediana** supera 60 m/s.
  - A τ = 10 s l'IMM dichiara r_90 = 144 m.
  - L'errore vero è di **801 m**, 5,6 volte il raggio, e u = 1,000.
  - Un altro caso, a 63 m/s: a τ = 2 s dichiara r_90 = 37 m, e l'errore è di 167 m.
  - Il filtro non contiene un regime d'accelerazione **longitudinale forte e sostenuta**, cioè la corsa di decollo e
    la rotazione.
- **Conseguenza.** La curva C(τ) è presentabile solo con l'etichetta «calcolata nel modello». Accanto va la
  copertura osservata **per tipo di moto**. Nel volo in manovra non si può dire «il 90 % è il 90 %».

**2. La confidenza dopo un evento impulsivo e quella sull'identità sono troppo alte (già nei dati di 10-prove;
nessun documento ne tira la conclusione).**
- **F3, sda, dopo l'urto:** C prevista 0,976, osservata 14/24 per passaggio, cioè 0,583 [0,388; 0,755].
- **F2, att, nelle fasce medie:** C prevista 0,697, osservata 20/53, cioè 0,377 [0,259; 0,512]. A 3–5 s la C è
  0,76 contro un'osservata di 0,28.
- **Identità in F5.** La formula p_scambio = Φ(−d/(√2·s)) è dimostrata per errori gaussiani indipendenti e
  isotropi. Prevede 0,21–0,29, ma il simulato dà 28/60, cioè 0,47 [0,35; 0,59], e 38/60, cioè 0,63 [0,51; 0,74].
  La previsione è quindi **smentita**, mentre SCENARI_VOLO §2 la dà come «P6 regge» e PERDITA_DI_CONFIDENZA dichiara
  una confidenza d'identità di 0,79–0,71.
- **Il registro del video non è monotono.** 76 violazioni di «C non cresce durante la perdita», in F2, F3 ed F5.
- **Correzione.** Dopo un evento, o fuori dal modello, la C della covarianza non va mostrata. Si mostra «fuori
  modello: vale l'insieme di presenza», che nel simulato ha contenuto il vero 939/939 [0,996; 1]. L'identità resta
  «presunta» senza cifra, oppure con il valore osservato 0,37–0,53 e non con quello della formula.

**3. Hardware dedicato: due errori di conto e un'attribuzione impropria (PA4 e PA5 reggono).**
- **La colonna «umano senza ausilio» conta due volte i 2,0 s del mezzo.** Il totale di 12,5 s dell'AC 90-48D
  comprende già il ritardo dell'aereo, eppure la formula aggiunge altri 2,0 s. Lo scarto è esattamente v·2,0 in
  tutte le righe dell'aereo: 140, 240, 360 e 500 m.
  - **Valori corretti (calcolati):** 928, 1590, 2385 e **3312 m** (non 3812).
  - **Droni** (togliendo i 2,0 s dell'aereo e mettendo gli 0,5 s del drone): 235, 529, 822 e **1058 m** (non 1237).
  - Le colonne «con direzione» sono invece coerenti: 5,4 s **senza** il ritardo del mezzo.
- **«Il calcolo dedicato garantisce un caso peggiore sotto il millisecondo» è falso sui numeri del documento.** La
  somma degli stadi di calcolo dedicato di `latenza.json` va da **0,081 a 1,21 ms**. Inoltre non esiste nessuna
  misura. Va corretta in «stimato 0,08–1,2 ms (ipotesi, nessuna misura)».
- **L'attribuzione «CPU contro dedicato» mescola due cose.** La colonna CPU contiene il **Python** misurato (55 ms di
  p95), mentre la colonna dedicata contiene codice compilato **ipotizzato**. Per ammissione del documento stesso, gli
  ~80 ms guadagnati vengono dal passaggio a codice compilato, che darebbe anche una CPU generica. Il CERN, nella fonte
  aperta, dà un FPGA più lento della CPU sul passo di Kalman.
- **Stessa confusione in 10-prove.** Lì «sda» cambia insieme il **sensore** (da 1 a 10 Hz) e il calcolo (da 80 a
  1,2 ms). Il ritardo di F4, sceso da 0,3 a 0,1 s, non è attribuibile all'hardware.
- **L'analogia con i chip per i modelli linguistici** (74 volte secondo il produttore, 8,4 volte per Cerebras) è
  usata con prudenza: vale per i carichi limitati dalla memoria, e lo si dichiara. Ma la frase «Un ASIC fatto
  apposta per tutta la catena, analogo all'HC1» va marcata come **ipotesi di progetto: non esiste, non è stato
  provato**. Sei fonti restano «NON APERTA».

**4. Gli scenari F3 ed F4 sono comodi in un punto e realistici in un altro (PA7 regge; PA6 e PA8 smentite).**
- **Dove sono comodi.** I frammenti veri di F3 hanno dv = 40 contro i 120 dichiarati; quelli di F4 hanno 60 contro
  100. C'è un margine di 3 e di 1,7 volte.
- **Rifatti al limite** (simulato, 10 passaggi per variante):
  - **V1, F3 con |u| = 120 sul bordo e vento a 15 m/s:** 600/600 frammenti sempre dentro, [0,9936; 1]. Il volume
    regge dentro le sue ipotesi, e PA6 è smentita.
  - **V2, come V1 più una vc dichiarata sbagliata di 8 m/s:** 600/600. Regge, perché i frammenti partono dalla
    velocità media, che sta fra i due segmenti dichiarati.
  - **V4, F4 con l'aereo a 210 m/s, dv 100 sul bordo e vento a 15 m/s:** 1000/1000 [0,9962; 1]. L'impronta sale a
    **8,65 km**.
  - **V3, F4 come avaria *non contenuta* vera,** cioè con il 5 % dei frammenti come pezzi di disco a 250 m/s e v_t
    80 m/s. Il dato è un'**ipotesi**: «centinaia di m/s», già dichiarati fuori dall'inviluppo in FRAM.
    - Frammenti sempre dentro V: 965/1000, cioè 0,965 [0,952; 0,975].
    - Pezzi di disco sempre dentro: **15/50**.
    - Passaggi con tutti i frammenti dentro: **0/10** [0; 0,278].
    - A terra nessuno cade fuori dall'impronta di 6,8 km, ma in aria V non li contiene.
- **Lettura.** F4 è chiamato «avaria non contenuta», ma il profilo scelto (`avaria_motore_a_terra`, dv 100) esclude
  per costruzione proprio i frammenti tipici di quell'avaria. Va rinominato «avaria con detriti a bassa energia»,
  oppure serve un profilo con dv di almeno 300 m/s (ipotesi), che allarga ancora il volume.
- **F4 «evento entro 1 s» classificato «solido».** L'innesco della fiammata prende la saturazione dal punto vero:
  RIVALUTAZIONE, EV-4, lo dice «ottimista». Il 60/60 è quindi in gran parte per costruzione, e la classe giusta è
  **incoraggiante con innesco ottimista**, non «solido».

**5. Riclassificazione: risultati «incoraggianti» lontani dal sicuro o senza base sufficiente.**
- **EV-1 (51/60 [0,739; 0,919]).** È ammissibile per l'addendum, ma riguarda multirotori a **8 m/s**. Per la
  collisione **veloce** (F3, 35–40 m/s) il risultato è **0/60 [0; 0,060]**, in att e in sda. Nel video, il cui caso
  centrale è il volo veloce, la cifra 51/60 senza «droni lenti, 8 m/s» fa credere che regga anche lì. È il rischio
  più grave per la giuria.
- **LP-8 «almeno 9 volte su 10 fino a 10 s».** Viene da **un solo esemplare** di multirotore, e la base effettiva è
  un mezzo. Sui multirotori, nella fascia 6–10 s, 03-confidenza dà per il CV 0,89 [0,87; 0,91]: il limite inferiore
  sta sotto 0,9, quindi «almeno» non è sostenuto (metrica diversa: non ho riletto f15, non verificato).
- **LP-7 «circa 9 su 10» sugli aerei.** Con v_max 210 m/s **non è stato rimisurato**. Gli intervalli sono bootstrap
  per mezzo, non Wilson per passaggio. Nel volo in manovra le regioni gaussiane contengono il vero in 0,24–0,78 dei
  casi (critica 1).
- **Le cifre «incoraggianti» di kalman-3.** Sono riportate come copertura in [0,82; 0,87] sugli aerei, ma per caso,
  con correlazione, e sulla media di tutti i tipi di moto. In manovra la copertura è lontana dal sicuro.
- **RIVALUTAZIONE, EV-7 «NON PROVATO» e «nessuno scenario».** Sono superati da 10-prove: F3 ed F4 sono ora simulati,
  con F3 come LIMITE e F4 come incoraggiante. Le 15 frasi vanno aggiornate.

**6. Frasi per la giuria.** Il testo del video non contiene ancora frasi sul volo (`testi.js` controllato). Per le
frasi che arriveranno, è vietato dire:
- «C(τ) esatta» senza «nel modello»;
- «confidenza 99 %» (P3 è smentita: 0,003–0,91);
- «l'hardware dedicato porta l'avviso sotto il millisecondo» o «a tempo reale»;
- «MoVi rileva la collisione in volo» (F3 0/60);
- «detriti sempre nel volume» per un'avaria non contenuta (V3 0/10);
- «identità confidente al 79 %».

## 2. Stati proposti

| enunciato | stato |
|---|---|
| C(τ), t_C e la miscela: formule | **dimostrato** nel modello CV o miscela gaussiana (confermo; nessun controesempio) |
| C(τ) sugli aerei in manovra | **smentito** come calibrato: 0,24–0,78 contro 0,90 (su dati pubblici, rumore simulato) |
| p_scambio da formula in F5 | **smentito** dal simulato (0,47–0,63 contro 0,21–0,29) |
| «caso peggiore dedicato < 1 ms» | **smentito** dai propri numeri (fino a 1,21 ms); comunque **ipotesi** |
| d_min «umano senza ausilio» | **calcolato, con errore**: corretto a 3312 m (aereo a 250 m/s) e 1058 m (drone a 90 m/s) |
| V(τ) per F3 al bordo dei parametri | **simulato**: regge, 600/600 [0,9936; 1] |
| V(τ) per un'avaria non contenuta con frammenti di disco | **smentito** (simulato, ipotesi sulla velocità): 0/10 passaggi [0; 0,278] |
| F4 evento entro 1 s | **incoraggiante con innesco ottimista**, non «solido» |

## 3. Proposte nuove

- **avversario-1: regime di accelerazione longitudinale nell'IMM** (CA con varianza tarata sulla corsa di decollo).
  - Previsione: la copertura al 90 % sui casi «accelerazione» sale ad almeno 0,85.
  - Smentita se resta sotto 0,75.
- **avversario-2: la confidenza mostrata è quella osservata per tipo di moto,** stimata con una tabella della metà di
  taratura, al posto della C del modello (ricalibrazione isotonica della PIT).
  - Previsione: lo scarto |C − osservata| è minore di 0,05 alle fasce 50 % e 90 %.
  - Smentita se supera 0,10.
- **avversario-3: un profilo «avaria non contenuta»** con dv di almeno 300 m/s (ipotesi) e un sottoinsieme di
  frammenti ad alta energia.
  - Previsione: V3 dentro in 10/10 passaggi, con un'impronta di almeno 10 km.
  - Smentita se qualche passaggio esce.

## 4. Correzioni obbligate (prima del documento tecnico e del video)

1. **EV-1 e la collisione veloce.** Accanto a ogni 51/60 va «multirotori a 8 m/s». Per la collisione veloce va
   scritto **0/60 [0; 0,060] (F3)**, con la miglioria della regola di contatto e del Doppler (10-prove §5.2).
2. **La C(τ) è «calcolata nel modello».** Accanto si mettono le coperture osservate in manovra: IMM in virata
   0,78 [0,63; 0,89], CV in virata 0,24–0,41, livello 50 % a 1–2 s 0,36–0,39. Dopo un evento o fuori modello la C si
   sostituisce con «fuori modello: insieme di presenza».
3. **p_scambio.** In SCENARI_VOLO, «P6 regge» va corretto in «smentita dal simulato (0,47–0,63)», e va tolta la
   confidenza d'identità 0,79–0,71.
4. **SENSORI_E_HARDWARE, colonna dell'umano senza ausilio.** Va tolto il doppio conteggio dei 2,0 s: 3312 m e
   1058 m. Va ricontata la lettura «domina l'umano: 3,1 km», che diventa circa 2,6 km.
5. **«Sotto il millisecondo» va sostituito** da «stimato 0,08–1,2 ms, ipotesi, nessuna misura». Il guadagno di
   circa 80 ms va attribuito al codice compilato, non all'FPGA o all'ASIC. L'ASIC «analogo all'HC1» va dichiarato come
   ipotesi di progetto, non esistente. Le fonti «NON APERTA» vanno aperte o tolte.
6. **10-prove: l'effetto di «sda» non è dell'hardware.** Lì cambiano insieme sensore e calcolo, quindi il ritardo di
   F4 (da 0,3 a 0,1 s) non va attribuito all'hardware.
7. **F4.** Va rinominato, oppure va aggiunto il profilo non contenuto; la classe dell'evento entro 1 s è
   «incoraggiante con innesco ottimista».
8. **RIVALUTAZIONE va aggiornata con 10-prove:** EV-7, la frase 7 con «8 m/s», LP-7 «non rimisurato a 210 m/s» e
   LP-8 «un esemplare».

## 5. Che cosa propongo dopo

- Rifare le coperture ADS-B **per aeromobile**, con il Wilson per mezzo: serve l'identificativo della sequenza nei
  casi.
- Provare avversario-1 e avversario-2 sulla stessa divisione per mezzo.
- Provare avversario-3 con 60 passaggi.
