# La collisione veloce come evento: la regola di contatto v4c (f20-chiusura/01-contatto, `sciame-scene-dinamiche`)

Lavoro del 15-11-2026, dalle 05:37 (`date -Is`). Le previsioni e il protocollo sono in `PREVISIONI.md`, scritti alle 05:38:53,
prima di qualunque passaggio con la regola nuova. Il congelamento della regola è in `congelamento.txt`: sha256 c14e903f…,
alle 05:46:27, prima dell'unica valutazione.

Tutto quel che segue è **simulato** dalle schede: nessun sensore fisico, nessuna prova su hardware, etichette messe a mano.
Il Doppler è **simulato** (ipotesi: σ_vr = 0,5 m/s, nessuna scheda aperta). Il Wilson al 95 % è calcolato **per passaggio**.
Ogni scenario ha una sola geometria nominale.

## 0. In testa: esito, cambi di stato, regole

**Esito su semi nuovi (idx 1000–1059, e 1000–1199 per F6).**

| Configurazione | Esito | Motivo |
|---|---|---|
| att (radar rotante a 1 Hz) | **SMENTITA** | F3 entro 2 s: 34/60 [0,441; 0,684], sotto la soglia di smentita di 45/60 |
| sda (radar a scansione elettronica a 10 Hz) | **NON RISOLTA, da trattare come LIMITE** | F3 entro 2 s: 57/60 [0,863; 0,983], sopra 51/60; F6 0/200 [0; 0,019]; ma la condizione «F1 e F5 0/60» **fallisce** |

Il dettaglio dei falsi eventi in sda:
- F5 (quasi incrocio a 39 m con gli ottici ciechi): **2/60** [0,009; 0,114];
- F3: un evento aperto 6,3 s **prima** dell'urto, 1/60.

Per D1, il caso centrale si presenta con la **collisione veloce come limite dichiarato**. La regola v4c resta una miglioria
in prova e non entra nel sistema.

**Cambi di stato proposti all'arbitro:**
- **V-11** resta L. La frase cambia da «0/60» a «regola in prova: sda 57/60 entro 2 s, ma 2/60 falsi eventi nel quasi
  incrocio F5; att 34/60».
- **D2** è fatta: il nucleo v4 è `prove_volo_v4.py`, cioè v3i più la regola v4c, che si spegne con
  `VOLO_REGOLA=v3i`. Il file `f19-volo/10-prove/prove_volo.py` è intatto.
- **K-709** è risolta sul volume, con un fatto nuovo sul ritardo (§ 5).
  - Con l'integratore stabile E1 dà 48/60 [0,682; 0,882] eventi entro 2 s dopo l'urto, più 3/60 [0,017; 0,137]
    aperti 11 s prima dell'urto. La fase 2c aveva 51/60.
  - I frammenti dentro V passano da 48/60 a 60/60 [0,940; 1].
  - Propongo **V-13 da I a L**.

**Regole.**
- Ho scritto solo in questa cartella. Niente rm, niente sovrascritture, niente git, niente sudo, niente rete.
- Processi: la valutazione girava con 7 lavoratori più il principale. E1 girava con 7 processi; con i 7 involucri
  `timeout` il conto supera 8, che è il limite del mandato. Lo dichiaro come violazione formale.
- Sviluppo: quattro iterazioni sugli idx 0–19 di F3 ed F6. Le versioni intermedie sono tenute accanto
  (`prove_volo_v4_sviluppo1..3.py`).
- **Registri video F3 _v4: NON generati.** Il mandato li chiedeva solo se F3 passava, e F3 non passa.

## 1. La regola (pseudocodice; non legge mai la verità)

La regola usa solo le tracce, le loro covarianze e i ritorni radar, cioè la posizione e la v_r misurata.

    ogni ciclo (0,1 s), se nessun evento è aperto:
      per ogni traccia confermata: conta gli aggiornamenti radar consecutivi con |v_r − v_traccia·los| ≤ max(5, 4·√(σ_vr²+σ_v²))
      per ogni coppia (a, b) di tracce confermate, a ogni aggiornamento comune:
        R_c = ingombro_max + 3(σ_a+σ_b) + cella di risoluzione del radar (2σ_r, 2·r·σ_az, 2·r·σ_el)
        RISOLTA:  d_ab > R_c, con ritorni radar DISTINTI e separati più di R_c, per ≥ 3 aggiornamenti di fila
        MATURE:   età ≥ 3 s, e coerenza Doppler per ≥ 3 aggiornamenti, per tutte e due
        CONVERGENTE: |v_b − v_a| ≥ 10 m/s, punto di massimo avvicinamento (a velocità costante) entro 10 s e sotto R_c
                     → memorizza t_c, p_c, le velocità di prima v_a e v_b
      per ogni coppia convergente, con t_c − 0,5 ≤ t ≤ t_c + 4 s:
        (a) si FONDE (d ≤ R_c dopo t_c − 1) oppure una traccia SPARISCE (non aggiornata da max(3 periodi, 0,5 s))
        (b) ≥ 2 tracce nuove confermate, nate dopo t_c − 1, entro 150 m da p_c
            OPPURE, per 3 aggiornamenti radar consecutivi dopo t_c, una delle due ha v_r incompatibile con
            ENTRAMBE le velocità di prima: |v_r − v_pre·los| > 5 m/s
        se (a) e (b): evento «collisione/frammentazione in volo (dedotto)», con volume e impronta del profilo
        collisione (eventi_v3.apri_evento)

Le soglie (dichiarate in `CONTATTO` dentro `prove_volo_v4.py`):

| Soglia | Valore | Da dove viene |
|---|---|---|
| aggiornamenti con la coppia risolta | 3 | dal verdetto |
| velocità relativa minima | 10 m/s | tabella § 4 del verdetto |
| orizzonte del massimo avvicinamento | 10 s | ipotesi |
| finestra dopo t_c | 4 s | ipotesi |
| aggiornamenti Doppler fuori norma | 3 | dal mandato («sostenuto») |
| scarto Doppler | max(5 m/s; 4σ) | ipotesi |
| tracce nuove | 2 entro 150 m | ipotesi |
| maturità e coerenza Doppler di prima | — | aggiunte in sviluppo, vedi sotto |

Queste soglie sono state fissate, o modificate, **guardando i semi di sviluppo**. Le soglie di decisione del mandato
invece sono state scritte prima.

**Sviluppo** (solo idx 0–19 di F3 ed F6; file `sviluppo_1..4.jsonl`):

| Iterazione | Che cosa è cambiato | Esito |
|---|---|---|
| 1 | regola base | F3 sda: 2 eventi prima dell'urto, su tracce giovani |
| 2 | maturità e coerenza Doppler prima dell'urto | att 0/20, per un errore mio: il ritorno radar si cercava all'istante di un aggiornamento della camera |
| 3 | ritorno radar più recente entro un periodo | F3 sda idx 18: due tracce sullo stesso drone a 120 m formavano una coppia |
| 4 | i ritorni radar della coppia devono essere distinti | F3 entro 2 s: att 14/20, sda 19/20; F6 0/20 e 0/20 |

Dopo l'iterazione 4 la regola è stata congelata. F1, F4 ed F5 **non** sono stati guardati in sviluppo, per protocollo.

**Il radar a scansione elettronica più vicino** ai frammenti (seconda parte della miglioria) **non è stato provato**.
- In sda c'è il radar a scansione elettronica a 10 Hz nella posizione dello scenario, a circa 2,1 km dall'urto.
- Per i frammenti (RCS 2·10⁻⁴ m²) la portata scala come (2·10⁻⁴/0,01)^¼ · 1400 m ≈ 530 m. Il conto è un
  **calcolo dall'ipotesi r_rif**.
- Servirebbe quindi un radar a meno di circa 500 m dall'urto. Metterlo lì sapendo dove avverrà l'urto è ottimista: la
  prova onesta lo mette su una griglia di posizioni fissata prima.

## 2. Esiti della valutazione unica

Valutazione unica: `valutazione_v4c.jsonl`, 880 passaggi, nessun errore. I conteggi sono in `risultati_v4c.json`, fatti
da `conta_v4c.py`.

| Cella | Misura | att | sda | Stato |
|---|---|---|---|---|
| F3, collisione di droni a 40 e 35 m/s | evento entro 1 s | 2/60 [0,009; 0,114] | 22/60 [0,256; 0,493] | sim |
| | **entro 2 s** | **34/60 [0,441; 0,684]** | **57/60 [0,863; 0,983]** | sim |
| | entro 2,5 s (soglia notata dopo) | 48/60 [0,682; 0,882] | 59/60 [0,911; 0,997] | sim |
| | entro 3 s (soglia notata dopo) | 51/60 [0,739; 0,919] | 59/60 | sim |
| | mai | 5/60 [0,036; 0,181] | 0/60 [0; 0,060] | sim |
| | **prima dell'urto** | 1/60 (−0,7 s) | 1/60 (−6,3 s) | sim |
| | ritardo min / mediano / max | −0,7 / 1,8 / 4,2 s | −6,3 / 1,2 / 2,2 s | sim |
| | innesco | tracce nuove 49, Doppler 6 | tracce nuove 48, Doppler 12 | sim |
| F6, controllo | falsi eventi | 0/200 [0; 0,019] | 0/200 [0; 0,019] | sim |
| F1, quasi collisione a 41 m | falsi eventi | **1/60 [0,003; 0,089]** | 0/60 [0; 0,060] | sim |
| F5, ottici ciechi, incrocio a 39 m | falsi eventi | **2/60 [0,009; 0,114]** | **2/60 [0,009; 0,114]** | sim |
| F4, avaria | evento entro 1 s | 60/60 [0,940; 1] | 60/60 [0,940; 1] | sim |
| | margine minimo dell'operatore | 0,3 s | 0,4 s | sim, ip |
| tutte le 10 celle | passaggi con «libero» sul punto vero | 0 (0/60 [0; 0,060]; 0/200 [0; 0,019]) | 0 | sim |

Due note sulla tabella.
- **F4 non peggiora:** 60/60 entro 1 s in tutte e due le configurazioni, «libero» sul vero 0, l'innesco è sempre la
  fiammata. Il margine minimo dell'operatore è 0,3 s in att e 0,4 s in sda, mentre in v3i era 0,25 e 0,45 s: semi
  diversi, nessun confronto da trarne.
- **Previsione mia** (scritta prima): «sda regge, att no». Su att **regge**. Su sda **regge solo a metà**: F3 sì, ma
  non avevo previsto i falsi eventi in F5.

## 3. I falsi eventi e la loro causa

| Passaggio | Innesco | t_c previsto | Evento | Causa probabile (**non verificata** passo per passo) |
|---|---|---|---|---|
| F5/sda 1048 e 1050 | Doppler | 39,4 e 40,2 s | 43,3 s | quasi incrocio a 39 m: i due ritorni cadono nella stessa cella e vengono uniti (`unisci_non_risolti`, v_r del primo oggetto); dopo l'incrocio le tracce si scambiano o si riagganciano. La v_r della traccia «sbagliata» non è compatibile con nessuna delle due v_pre proiettate, perché la los è cambiata nel frattempo |
| F5/att 1038 | Doppler | — | 44,3 s | come sopra |
| F5/att 1033 | 2 tracce nuove dopo l'incrocio | — | 41,6 s | riaggancio delle tracce dopo la cecità degli ottici: ricorrono tracce «nuove» che non sono frammenti |
| F1/att 1050 | Doppler | 81,9 s | 85,0 s | traccia del drone a 1 Hz con riassociazione al passaggio a 41 m dall'aereo |
| F3/sda 1024 | Doppler | 13,2 s | 13,7 s | evento 6,3 s prima dell'urto: una coppia con un massimo avvicinamento previsto sbagliato. Va contato come un falso allarme anche se il passaggio ha l'urto |
| F3/att 1015 | Doppler | 15,8 s | 19,3 s | evento 0,7 s prima dell'urto |

**Un limite di fondo.** In F3 l'innesco più frequente sono «2 tracce nuove vicino al punto»: 48–49 su 60. Nel
simulatore i frammenti (RCS 2·10⁻⁴ m²) **non si vedono** (F-702). Le tracce nuove sono quasi certamente riagganci dei due
droni dopo l'urto, o tracce spurie, e **non frammenti** (non verificato per passaggio).
- La regola quindi riconosce «due tracce risolte convergono, si confondono e la scena si ricompone in modo diverso».
  Non riconosce i detriti.
- Lo stesso segnale compare in un quasi incrocio con riaggancio (F5/att 1033): è la stessa ambiguità della domanda
  «residuo o oggetto».

## 4. Stati proposti

| Enunciato | Stato | Classe | Frase ammessa |
|---|---|---|---|
| C-1: collisione veloce dichiarata come evento entro 2 s, regola v4c, sda | sostenuto dai dati per F3 (57/60 [0,863; 0,983]); **smentito come regola senza falsi** (F5 2/60) | **L** | «Una regola di contatto in prova riconosce la collisione di due droni veloci entro 2 s in 57 passaggi simulati su 60 col radar a scansione elettronica, ma dà ancora 2 falsi eventi su 60 in un quasi incrocio a 39 m: non è adottata» |
| C-2: idem in att | **smentito** (34/60 < 45) | L | «col radar rotante a 1 Hz non basta: 34 su 60» |
| C-3: F6 nessun falso evento con v4c | sostenuto dai dati | S | 0/200 [0; 0,019] per configurazione |
| C-4: F4 invariato con v4c | sostenuto dai dati | come V-2 | 60/60 [0,940; 1] |
| V-1 con v4c | sostenuto dai dati | S | 0 passaggi con «libero» sul vero in tutte le 10 celle |

Restano vietate «MoVi rileva la collisione in volo» e «entro 2 s» senza «in N su 60».

## 5. E1 rifatto con l'integratore stabile (K-709)

**Che cosa ho fatto.** Ho scritto `e1_stabile.py`, che importa `eventi_v3.py` senza modificarlo e sostituisce
`frammenti_vett` con la stessa funzione cambiata in un solo punto: il passo della resistenza è semi-implicito, come in
`eventi_volo.frammenti_volo`. Le estrazioni casuali restano le stesse e nello stesso ordine.
- Scenario: E1 «alta», idx 0–59, gli stessi semi di f15/2c.
- Controllo: con Eulero lo stesso codice riproduce f15 su idx 0–4 (ritardi 1,9 / 1,4 / 1,5 / 1,2 / 1,3 s e
  frammenti_dentro_V identici).
- Dati: `e1_stabile_*.jsonl`, `e1_euler_000.jsonl`, `e1_confronto.json`.

| E1, multirotori a 8 e 6,7 m/s | f15 (Eulero) | integratore stabile | Stato |
|---|---|---|---|
| evento con 0 ≤ ritardo ≤ 2 s | 51/60 [0,739; 0,919] | **48/60 [0,682; 0,882]** | sim |
| ritardo ≤ 2 s, come contava il verdetto | 51/60 | 51/60, di cui 3 negativi | sim |
| evento **prima** dell'urto (t = 3,5–4 s, tipo «separazione», ritardo −11 s) | 0/60 [0; 0,060] | **3/60 [0,017; 0,137]** | sim |
| entro 2,5 s | 60/60 [0,940; 1] | 60/60 [0,940; 1], di cui 3 negativi | sim |
| passaggi con tutti i frammenti conformi dentro V | 48/60 [0,682; 0,882]; campioni 108 495/108 840 | **60/60 [0,940; 1]**; campioni 109 500/109 500 | sim |
| falsi eventi (passaggi senza urto) | — | 0 (E1 ha sempre l'urto) | sim |

Il ritardo cambia in 22 passaggi su 60. La causa che ho trovato: già i ritorni **delle camere prima dell'urto** cambiano.
Su idx 17, 34 dei 55 record prima di 5 s sono diversi, e il primo è a t = 1,68 s, dove droneA manca. Vuol dire che le
traiettorie dei frammenti entrano nella sequenza casuale del simulatore delle camere già dall'inizio. Il «rifacimento»
quindi **non isola l'integratore**: è anche una nuova estrazione del rumore.

**Risposta a K-709.**
- **Risolta sul volume:** con l'integratore stabile i frammenti restano dentro V in 60/60 passaggi, contro 48/60. Lo
  scostamento della fase 2c sul volume era un artefatto di Eulero.
- **Il 51/60 cambia:** diventa 48/60 [0,682; 0,882] contando solo gli eventi dopo l'urto, più 3/60 eventi
  «separazione» aperti a 3,5–4 s, cioè 11 s prima dell'urto.
- Proposta per **V-13**: il limite inferiore scende sotto 0,70, quindi da **I a L** finché non si spiega l'evento
  precoce. Il motivo dei 3 «separazione» precoci (tracce di camera nuove al primo aggancio) è **non verificato**.
- La cifra da non dire diventa «entro 2 s in 51 su 60» senza la nota «con l'integratore stabile: 48 su 60 e 3 eventi
  prima dell'urto».

## 6. Che cosa propongo dopo (migliorie con meccanismo, previsione e prova)

1. **Doppler sulla cella unita.**
   - Meccanismo: non usare la v_r di un ritorno marcato «unito» (due oggetti nella stessa cella). Nel test (b)
     confrontare v_r con v_pre·los calcolata con la los di **prima** dell'incrocio, più lo scarto dovuto alla
     rotazione della los.
   - Previsione: F5 da 2/60 a 0/60, con F3/sda ≥ 54/60.
   - Smentita: un falso evento in F5 o F1 su 60 semi nuovi (idx 2000+), oppure F3/sda < 51/60.
2. **Tracce nuove contate solo se non sono riagganci.**
   - Meccanismo: una traccia nuova la cui posizione e la cui v_r sono compatibili con la previsione di a o di b è un
     riaggancio, non un frammento.
   - Previsione: F5/att 1033 sparisce; F3 perde una parte degli inneschi «tracce nuove», ma li recupera col Doppler.
   - Prova: le stesse celle su semi nuovi.
3. **Eventi prima dell'urto.**
   - Meccanismo: richiedere che il punto previsto p_c sia stato raggiunto, cioè che le due tracce si siano avvicinate
     a meno di 2R_c, prima di accettare (b).
   - Smentita: un evento con ritardo < 0 su 60.
4. **Radar a scansione elettronica vicino**, su una griglia di posizioni fissata prima e non sul punto d'urto, con i
   frammenti a 2·10⁻⁴ m².
   - Previsione: con il radar entro 500 m, ritorni dei frammenti in ≥ 0,8 dei passaggi.
   - È un calcolo da r_rif: ipotesi.
5. **Geometrie variate** (≥ 10 per scenario), perché ogni scenario qui è una sola geometria.

**File** (tutti in questa cartella):
- protocollo e congelamento: `PREVISIONI.md`, `congelamento.txt`;
- codice: `prove_volo_v4.py` (nucleo v4 con v4c) e le copie `_congelato` e `_sviluppo1..3`; `conta_v4c.py`;
  `e1_stabile.py`; `registri_v4.py`, che non è stato eseguito;
- dati: `sviluppo_1..4.jsonl`, `valutazione_v4c.jsonl`, `risultati_v4c.json`, `e1_*.jsonl`.

**Indipendenza.** Condivido con ciò che misuro il simulatore, il tracciatore, le definizioni di evento e di falso evento
e il modello linguistico. Anche il Doppler simulato l'ho scritto io. Il controllo vale solo per i difetti fuori da
questo insieme.
