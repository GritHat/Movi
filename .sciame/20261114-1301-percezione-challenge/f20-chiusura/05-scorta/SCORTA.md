# F7 «scorta»: MoVi a bordo di un drone che mantiene la traccia di un bersaglio veloce mentre accanto due droni collidono

Autore: `sciame-tracciamento`, fase 4 (chiusura), 15-11-2026, dalle 05:51 alle 06:40 (`date -Is`).
**Tutto è simulato dalle schede e da ipotesi dichiarate. Nessun sensore fisico, nessuna prova su hardware, niente è
«validato». Le etichette sono messe a mano.** Il sistema fa solo osservazione, monitoraggio e avviso: «seguire» vuol dire
mantenere la traccia. MoVi non comanda il portatore, non insegue e non intercetta.
**Indipendenza.** Lo scenario, il tracciatore e la misura li ha scritti lo stesso autore con lo stesso simulatore. La
misura scopre gli errori di codice, non quelli della fisica ipotizzata.

## 0. In testa: cambi di stato e regole

- **Previsioni.** Scritte alle 05:53:49, prima del codice, in `PREVISIONI.md`.
  - Parametri congelati alle 06:07:43, dopo lo sviluppo sui semi 20261120, in `CONGELAMENTO.md` (sha256 dello script).
  - Valutazione fatta una sola volta sui semi nuovi 20261121, in `passaggi_valutazione.jsonl` e
    `risultati_valutazione.json`.
  - Esito: P1, P3, P4, P5, P7 e P8 **reggono**. P2 è **smentita in una cella** (vira/att, 43/60). P6 **regge**, ma
    l'avviso non discrimina (§2, A-6).
- **Regole.** Ho scritto solo in `f20-chiusura/05-scorta/` e nei registri `prototipo/uscite/video_volo/registro_F7_*`,
  più `INDICE_F7*.md`. Niente git, niente sudo, niente rete. Al più 8 processi, sempre con `timeout`.
  - **Violazione 1 (lieve).** `scorta_f7.py` è il mio file di lavoro e l'ho riscritto durante lo sviluppo. Ogni stato
    precedente è conservato accanto (`scorta_f7_v0…v5_*.py`).
  - **Violazione 2.** I registri F7 di prima stesura (`registro_F7_<variante>.jsonl`) violano la regola 5 del
    validatore: la parola dell'evento non diceva «non verificata». Restano accanto. Quelli da usare sono `*_v2.jsonl`:
    0 violazioni su 5 × 240 fotogrammi (`esito_convalida_F7_v2.txt`). I numeri sono identici, verificato con `cmp`.
  - **Difetto noto.** In `INDICE_F7_v2.md` l'elenco riporta i nomi senza `_v2`. Vale l'intestazione dell'indice.
- **Riuso.** Le copie di fase 3 sono accanto: `eventi_volo_f7_copia_origine.py` e `prove_volo_v3i_copia_origine.py`.
  I file di fase 3 e il nucleo v4 dell'altro agente non li ho toccati.
  - `frammenti_volo()` (integratore semi-implicito, stabile) è copiato testualmente in `scorta_f7.py`.
  - Il nucleo v3i lavora su griglie polari di sensori **fermi** e non si applica a un sensore in moto. Ne ho ripreso
    **le regole**, non il codice:
    - mai «libero» sul non osservato;
    - insieme di presenza r0 + δv·τ + a·τ²/2;
    - la C non cresce durante la perdita;
    - l'evento non sparisce;
    - un sensore perso non torna «affidabile».
  - **Limite:** il tracciatore F7 è un componente nuovo, non il nucleo v3i.

## 1. Scenario e parametri (I = ipotesi)

**Portatore** (profilo deterministico con lo schema di `f14/01-profili/profili_portatore.json`; valori I):
- volo livellato a 120 m, a 25–35 m/s, in rotta retta;
- a_max 4 m/s², T_r 0,25 s, 6 gradi di libertà, «quasi» olonomo, canale d'avviso «comando», `sensore_in_moto`
  vero;
- la rotta retta è il caso peggiore per il campo visivo: il portatore non segue il bersaglio con la sua guida.

**Navigazione inerziale** (classe tattica con GNSS, I):
- posizione: 0,5 m, deriva 0,02 m/s, passeggiata aleatoria 0,05 m/√s;
- assetto: 0,1°, deriva 0,005°/s.

Il moto proprio è compensato con la posa **stimata**. L'errore di navigazione correlato, che filtrando non si riduce,
entra nella regione come margine: 3(σp + b·t + σrw·√t) + distanza · 3(σatt + ω·t).

**Bersaglio** (drone, RCS 0,02 m²):
- parte 150–300 m avanti, a 35–45 m/s, con uno zig-zag laterale di 3 m/s² e periodo 8 s;
- variante **vira**: virata di 8 m/s² durante l'accecamento e per altri 2 s, cioè circa 45–60° di cambio di rotta;
- la missione lo designa all'avvio come «bersaglio» (etichetta a mano).

**Evento** a t = 6 s. Due droni a 30–40 m/s, con un angolo d'incontro di 60–180°, collidono:
- **dove:**
  - lato: 30–100 m di fianco;
  - davanti: 30–100 m sul percorso, fra il portatore e il bersaglio;
  - dietro: 30–100 m dietro;
- **fiammata:** satura le camere per 0,5–3 s. La saturazione la segnala il sensore stesso (istogramma); nel simulatore
  è la finestra dell'evento, quindi l'innesco è **ottimista**;
- **fumo:** sfera di 5–30 m che deriva, dura 5–20 s e blocca la linea di vista ottica;
- **frammenti:** 30 frammenti più i 2 corpi:
  - velocità = media dei mezzi + u, con |u| ≤ 50 m/s;
  - v_t da 5 a 30 m/s;
  - RCS da 10⁻⁴ a 10⁻² m²;
- **radar:**
  - echi dei frammenti;
  - echi spuri nella nube per 3 s (Poisson 3 per scansione);
  - fondo di 0,5 falsi per scansione;
  - mascheramento CFAR del bersaglio (Pd × 0,3) se un frammento è entro 15 m in distanza e 5 σ in angolo.

**F7c** (controllo):
- quasi collisione con una separazione verticale di 30–60 m e nessun urto;
- in metà dei passaggi un riflesso solare satura la camera per 0,5 s.

**Configurazioni** (classi dichiarate come ipotesi; nessuna scheda aperta in questo lavoro):

| | radar | camera |
|---|---|---|
| att | FMCW piccolo di bordo, 5 Hz, ±60° avanti, 1°, 1,5 m, Doppler 0,3 m/s, Pd 0,5 a 800 m per 0,01 m² | fissa, ±30°, 0,05°, fino a 800 m |
| sda | scansione elettronica a 20 Hz, 4 pannelli (360°), 0,5° (classe EchoShield da `parametri_volo.json`, scheda **non aperta**) | EO/IR raffreddato su brandeggio, 0,02°, 2 km |

- Non è simulata una camera a eventi (non provato).
- Le latenze di elaborazione **non** sono simulate in F7.

**Tracciatore** (`scorta_f7.py`):
- **filtro:** Kalman a velocità costante con Q = 80 m²/s³;
- **associazione:**
  - porta di Mahalanobis χ²₃ al 99,9 %, allargata di 8 per le tracce con almeno 3 colpi;
  - porta Doppler di 3σ + 2 m/s;
  - assegnazione globale con l'algoritmo ungherese;
- **vita delle tracce:**
  - conferma 3 su 5;
  - cancellazione delle tracce non confermate dopo 1 s e delle confermate dopo 3 s; il bersaglio non si cancella mai,
    diventa regione;
  - dopo 1 s di perdita il bersaglio non si aggiorna da una misura sola;
  - riacquisizione «presunta» solo da una traccia confermata, con almeno 5 colpi, velocità coerente e fuori dal volume
    dei detriti (non è mai scattata nella valutazione);
- **evento:** un grappolo di almeno 5 misure nuove entro 40 m in 1 s, **e** in più la saturazione delle camere o due
  tracce che convergono entro 20 m;
- **regione del bersaglio:** max(r al 99,99 % + margine INS, insieme di presenza r_ult + 3σv·τ + 10·τ²/2);
- **volume dei detriti** (dimostrato nel modello: resistenza lungo −v, vento nullo, v_t ≤ 40 m/s dichiarata):
  - è un cono orizzontale {p0 + S(vc + u) : S ∈ [0, τ], |u| ≤ δv}, con δv = 80 m/s + 10 (velocità dei mezzi dalle
    tracce; + 60 se non sono note), più r0 = 15 m + l'estensione del grappolo;
  - le quote vanno da z0 − (δv + |vcz|)τ − gτ²/2 − r0 a z0 + (vcz + δv)τ + r0;
  - il tutto è intersecato con la sfera del cammino massimo L(τ) = (v_t²/g)·ln(cosh(gτ/v_t) + (v0/v_t)·sinh(gτ/v_t)),
    che viene dal confronto con d|v|/dt ≤ g − k|v|²;
- **«libero»:** solo dentro il campo del radar, entro la portata in cui un oggetto di 10⁻⁴ m² è visto con Pd ≥ 0,99 in
  3 scansioni (193 m in att, 339 m in sda), e fuori da ogni regione e dal volume;
- **avviso al portatore:** se il percorso stimato dei prossimi 5 s entra nel volume allo stesso istante futuro.

## 2. Esiti (valutazione, semi 20261121)

60 passaggi per cella, 200 per F7c, Wilson al 95 % **per passaggio**.

Classi:
- **S** = solido: limite inferiore ≥ 0,90, oppure 0/N con limite superiore ≤ 0,06;
- **I** = incoraggiante;
- **L** = limite;
- **NP** = non provato.

Stato di tutte le righe: **sim** (simulato).

| # | Misura | att | sda | Classe |
|---|---|---|---|---|
| A-1 | Continuità del bersaglio (traccia o regione che lo contiene in ogni ciclo) | lato, dietro e vira 60/60 [0,940; 1]; davanti 59/60 [0,911; 0,997] (1 ciclo fuori in 1 passaggio) | 60/60 [0,940; 1] in tutte e 4 | **S** |
| A-2 | Identità mantenuta (traccia viva, entro 30 m alla fine, nessuna associazione spuria non dichiarata) | lato, davanti e dietro 60/60 [0,940; 1]; **vira 43/60 = 0,72 [0,59; 0,82]** | 60/60 [0,940; 1] in tutte e 4 | S, ma **L** in vira/att |
| A-3 | Riacquisizione entro 2 s dalla fine della saturazione | 60/60 [0,940; 1]; ritardo massimo 0,38 s | 60/60 [0,940; 1]; massimo 0,10 s | S (vedi la nota *) |
| A-3c | Riacquisizione **da camera** entro 2 s (fumo) | lato e dietro 60/60; davanti 57/60 [0,863; 0,983]; vira 56/60 [0,841; 0,974]; massimo 3,25 s | uguale | I |
| A-4 | «Libero» sul bersaglio o su un frammento | 0/60 [0; 0,060] in ogni cella | 0/60 [0; 0,060] in ogni cella | **S** (in parte per costruzione, vedi la nota **) |
| A-5 | Associazioni detrito→bersaglio non dichiarate | 0/60 [0; 0,060] in ogni cella | 0/60 | **S** |
| A-5b | Associazioni nel volume dei detriti, **dichiarate** «presunta_dubbia» | davanti 20/60, vira 23/60 | lato 3/60, davanti 20/60, vira 25/60 | dato |
| A-6 | Volume dei detriti: campioni dei frammenti veri dentro | lato 757/757 (evento visto in 1/60 passaggi); davanti 43 681/43 681; vira 42 950/42 950; dietro: evento non visto | 44 051, 43 681, 43 600 e 42 950, tutti dentro: 60/60 passaggi [0,940; 1] in ogni cella | **S** come contenimento |
| A-6b | Avviso al portatore quando un frammento vero gli passa entro 10 m | davanti 56/56; vira 54/54; margine minimo 0,4 s | uguale | I (soglia dei 10 m scelta da me) |
| A-6c | Avviso anche quando nessun frammento passa vicino | lato 1/60; dietro 0/60 (evento non visto) | **lato 60/60, dietro 60/60** | **L**: il volume è prudente e l'avviso non discrimina |
| A-7 | Evento dichiarato | **lato 1/60, dietro 0/60** (fuori dal campo ±60°: «non so», mai «libero»); davanti e vira 60/60 alla prima scansione | 60/60 in tutte e 4, alla prima scansione | S in sda; **L** in att di lato e dietro |
| A-8 | Falsi eventi in F7c | 0/200 [0; 0,019] | 0/200 [0; 0,019] | **S** |
| A-9 | Camera «affidabile» in un ciclo saturo | 0 cicli | 0 cicli | S (innesco ottimista) |

\* Il radar di bordo nel simulatore non è accecato dalla fiammata. La riacquisizione del bersaglio è quindi quasi
immediata **per ipotesi**. Accecamento del radar e disturbo elettromagnetico dell'esplosione sono **non provati**.

\*\* Il bersaglio sta a 150 m o più: quasi sempre oltre la portata del «libero» (193 e 339 m). Lo 0 sul bersaglio
dipende in parte da questo. Lo 0 sui frammenti viene dal contenimento del volume (A-6) e dalle regioni delle tracce.

**Perché vira/att fallisce (causa, non errore d'associazione).** Il bersaglio vira e il portatore resta in rotta
retta: il bersaglio esce dal campo di ±60° del radar avanti (in sviluppo, idx 4: azimut 38° a 12 s e poi oltre 60°).
- La regione lo contiene sempre (A-1 60/60).
- La traccia resta «non vista» con la regione che cresce, e l'errore finale supera i 30 m (da 30 a 83 m).
- Associazioni spurie: 0.
- **Miglioria:** campo di 360° (sda: 60/60), oppure il portatore che orienta il sensore (camera su brandeggio).

## 3. Curva della confidenza del bersaglio (`curva_F7.json`)

**Formula** (verdetto di fase 3, §3, piano 2D; dimostrata nel modello):

    σ²(τ) = σ0² + 2σ0v·τ + σv²·τ² + q·τ³/3,    C(τ) = 1 − exp(−g²/2σ²(τ)),    r_0,9(τ) = 2,146·σ(τ)

I parametri vengono dallo stato stazionario del filtro F7 (Riccati, misura a 250 m), quindi sono calcolati da
ipotesi. g = 30 m. Il caso descritto è la **perdita totale**, radar e ottici, che nel simulato non avviene.

| τ (s) | 0 | 0,5 | 1,0 | 1,5 | 2,0 | 3,0 | 5,0 |
|---|---|---|---|---|---|---|---|
| att: C | 1,00 | 1,00 | 0,98 | 0,84 | 0,62 | 0,31 | 0,09 |
| att: r_0,9 (m) | 6,5 | 13,2 | 22,5 | 33,6 | 46,2 | 75,3 | 146 |
| att: insieme di presenza (m) | 14 | 26 | 40 | 56 | 75 | 121 | 242 |
| sda: C | 1,00 | 1,00 | 1,00 | 0,93 | 0,73 | 0,37 | 0,11 |
| sda: r_0,9 (m) | 2,7 | 8,6 | 17,1 | 27,6 | 39,5 | 67,5 | 137 |

Parametri:
- att: σ0 = 3,05 m, σ0v = 13,6 m²/s, σv = 6,84 m/s, t(C < 0,9) = 1,35 s;
- sda: σ0 = 1,26 m, σv = 5,17 m/s (tabella completa nel JSON).

**Misura durante l'accecamento ottico** (sim, cicli correlati, quindi senza intervallo per ciclo):
- quota di cicli col bersaglio dentro r_0,9 3D: **0,86–0,93 in att**, 0,88–0,92 in sda, nei primi 5 s;
- dentro la regione dichiarata: **tutti i cicli**.
- La C numerica del registro resta 1,00 perché il radar continua a vedere il bersaglio.
- La r_0,9 del filtro in att è **leggermente ottimista** (0,86 contro 0,90): la mostrerei come **L**, non come «90 %».

## 4. Frasi per la giuria

| Italiano | English | Classe |
|---|---|---|
| «A bordo di un drone, durante una collisione a 30–100 m con fiammata, fumo e detriti, MoVi non ha mai perso la regione che contiene il drone seguito: 60 passaggi simulati su 60 per ogni geometria con il radar a 360 gradi.» | "On board a drone, through a collision 30–100 m away with flash, smoke and debris, MoVi never lost the region containing the tracked drone: 60 out of 60 simulated runs for each geometry with the 360-degree radar." | S, sim |
| «Nessun frammento è stato attribuito al drone seguito senza dichiararlo: 0 su 60 in ogni caso; quando una misura cade nel volume dei detriti, l'identità diventa "presunta, dubbia".» | "No fragment was attributed to the tracked drone without saying so: 0 out of 60 in every case; when a measurement falls inside the debris volume, the identity becomes 'presumed, doubtful'." | S, sim |
| «Il volume dei detriti dichiarato ha contenuto tutti i frammenti simulati, e MoVi non ha mai detto "libero" dove c'era un frammento.» | "The declared debris volume contained every simulated fragment, and MoVi never said 'clear' where a fragment was." | S, sim (nel modello) |
| «Camere dichiarate non affidabili in ogni istante di saturazione; nessun falso evento in 200 voli di controllo.» | "Cameras declared unreliable at every saturated instant; no false event in 200 control flights." | S, sim |
| «Se il drone seguito vira fuori dal campo di un radar solo frontale, MoVi lo dichiara: regione che cresce, identità non più garantita (43 su 60).» | "If the tracked drone turns out of a forward-only radar's field, MoVi says so: a growing region, identity no longer guaranteed (43 of 60)." | L, sim |

## 5. Frasi da non dire

- «MoVi segue» o «insegue» il bersaglio, o qualsiasi lessico d'ingaggio. Si dice «mantiene la traccia», solo
  osservazione e avviso.
- «Riacquisisce sempre entro 2 s» senza la frase «il radar non è accecato nel simulato».
- «Confidenza al 90 % tarata» sulla r_0,9 (in att 0,86).
- «Funziona con un radar piccolo di bordo in ogni geometria»: con l'evento di lato o dietro va 1/60 e 0/60.
- «L'avviso di detriti è preciso»: è prudente e scatta anche quando nessun frammento passa vicino (60/60).
- «Testato con la camera a eventi», «validato», «su hardware», «in tempo reale», «detect and avoid».
- «Identità certa»: è «presunta».

## 6. Limiti e migliorie per passare a un sistema attuato

| Limite | Miglioria (che cosa e come) | Prova che la decide |
|---|---|---|
| Radar non accecato e niente disturbo elettromagnetico dell'esplosione: la riacquisizione è facile per ipotesi | modello di blanking del ricevitore e di saturazione dell'AGC; prova con il radar perso per 0,2–2 s | riacquisizione ≤ 2 s ≥ 51/60 con il radar perso |
| Saturazione presa dalla finestra dell'evento (innesco ottimista) | rilevatore sull'istogramma della camera; registrazioni vere di fiammate | ritardo ≤ 1 ciclo in ≥ 0,9 |
| Campo di ±60° (att): evento laterale o posteriore non visto, bersaglio che esce dal campo | radar a 360° o camera su brandeggio puntata dalla traccia | vira/att identità ≥ 51/60; lato/att evento ≥ 57/60 |
| Volume dei detriti troppo largo (cresce di circa 90 m/s), avviso non discriminante | Doppler dei frammenti per stimare δv per frammento; volume per grappoli tracciati invece che dall'inviluppo | avviso falso ≤ 10 % nei casi senza intersezione, con contenimento 100 % |
| r_0,9 del filtro ottimista in att (0,86) | IMM con un regime di manovra; covarianza INS correlata nel filtro (stato aumentato) | quota in r_0,9 nell'intervallo [0,88; 0,92] |
| Stato della camera che oscilla «ripristinata/degradata» nel fumo | isteresi di N cicli | 0 oscillazioni sotto 1 s |
| Nessuna camera a eventi, nessuna latenza, vento nullo, una sola dinamica dei frammenti, tracciatore nuovo (non il nucleo v3i) | simulare la camera a eventi; latenze da `latenza.json`; vento nel volume; integrazione nel nucleo v4 | stesse soglie |
| Margine dell'avviso di 0,4 s nei casi peggiori (evento a 30 m davanti) | è fisica: a 30 m e 30 m/s resta circa 1 s; serve la previsione delle traiettorie dalle tracce prima dell'urto (avviso di prossimità) | margine ≥ T_r = 0,25 s in 60/60 (oggi regge) |
| Tutto simulato | prove su registrazioni vere e sul campo | tutte |

## 7. File

Nella cartella `f20-chiusura/05-scorta/`:
- `PREVISIONI.md`, `CONGELAMENTO.md`;
- `scorta_f7.py` (e le versioni da v0 a v5), `curva_f7.py`, `indice_f7.py` (e `indice_f7_v1.py`);
- `passaggi_sviluppo*.jsonl`, `esito_sviluppo*.txt`;
- `passaggi_valutazione.jsonl`, `risultati_valutazione.json` (copia di `esito_valutazione.txt`), `curva_F7.json`;
- `esito_convalida_F7*.txt`.

Registri: `prototipo/uscite/video_volo/registro_F7_{lato,davanti,dietro,vira,F7c}_v2.jsonl` e `INDICE_F7_v2.md`.

Per rifare tutto:

    python -I -B scorta_f7.py valutazione 8
    F7_REG_SUFFISSO=_v3 python -I -B scorta_f7.py --registro DIR

Le uscite si scrivono in modo `x` e non sovrascrivono mai.
