# Verdetto finale della fase 4, chiusura (f20-chiusura/20-verdetto, `sciame-arbitro`)

Scritto il 15-11-2026 dalle 06:25:19 (`date -Is`). Le previsioni PA-1…PA-9 sono in `PREVISIONI.md`, scritte alle
06:26:20, **prima** del riconto e delle corse.

Riconti e attacco con codice mio, tutto in questa cartella:
- `riconta_finale.py` → `riconto_finale.txt`: v4c, v3i, E1 stabile, E1 di f15 ed F7, dai jsonl grezzi;
- `attacco_f7.py` → `attacco_f7.jsonl`, contato da `conta_attacco_f7.py` → `conteggi_attacco_f7.txt`. Sono 480
  passaggi su semi nuovi e varianti; `scorta_f7.py` è importato e non modificato.

**Tutto è simulato dalle schede, calcolato, o su traiettorie pubbliche con un sensore simulato.**
- Nessun sensore fisico e nessuna prova su hardware. Niente è «validato».
- Le classi degli oggetti sono etichettate a mano.
- Il sistema fa solo osservazione, monitoraggio e avviso.

**Come leggere le cifre.**
- Il Wilson al 95 % è **per passaggio**. Quando scrivo «casi», i casi sono correlati dentro un mezzo e l'intervallo
  è ottimista.
- Stati: dim = dimostrato nel modello; calc = calcolato; sim = simulato; pub = su dati pubblici con un sensore
  simulato; ip = ipotesi.
- Classi:
  - **S** (solido): limite inferiore ≥ 0,90, oppure 0/N con limite superiore ≤ 0,06;
  - **I** (incoraggiante): stima ≥ 0,80, limite inferiore ≥ 0,70 e una base matematica;
  - **L**: limite dichiarato;
  - **NP**: non provato.

**Indipendenza.** Con gli autori condivido i simulatori, i tracciatori, le definizioni dei campi e il modello
linguistico. I miei controlli coprono gli errori di aggregazione e di conteggio. In F7 coprono anche la robustezza a
semi e geometrie nuovi. Non coprono la fisica ipotizzata né il modello dei sensori.

## 1. In testa: previsioni, regole, cambi di stato

**Previsioni.**

| # | Esito | Prova |
|---|---|---|
| PA-1 F3 v4c | **regge** | att 34/60, sda 57/60, prima dell'urto 1/60 e 1/60 |
| PA-2 F6/F5/F1 v4c | **regge** | F6 0/200 ×2; F5 2/60 ×2; F1/att 1/60 |
| PA-3 F3 v3i | **regge** | 0/60 entro 2 s, att e sda («mai» 60/60) |
| PA-4 E1 stabile | **regge** | 48/60; 3/60 prima dell'urto (−11,5, −11,0, −11,0 s); V 60/60 |
| PA-5 F7, riconto | **regge** | tutte le celle identiche a SCORTA § 2 |
| PA-6 F7, semi nuovi (base 20261199) | **regge** | continuità 20/20 in tutte le celle; «libero» 0; F7c 0/60 ×2 |
| PA-7 F7, urto davanti a 10–30 m | **regge** per continuità e «libero»; **limite nuovo** sul margine (§ 2.2, A-6b) | 20/20 [0,839; 1] |
| PA-8 F7, frammenti a 100 m/s, oltre i 90 dichiarati | **smentita**, a favore del sistema | contenimento 15 019/15 019 e 14 557/14 557, sda |
| PA-9 F7c, quasi collisione a 5–20 m | **smentita** | 0/60 falsi eventi in att e in sda. È un limite della prova (§ 2.2) |

**Regole.**
- Ho scritto solo in `20-verdetto/`. Niente cancellazioni, sovrascritture, git o sudo.
- Rete: non usata.
- Una corsa pesante sola: Pool da 6 più il principale, con `timeout 1500`.

**Cambi di stato.**
- **F-801.** La collisione veloce (F3) resta **L**. La regola di contatto v4c è stata provata (D1) e **non è adottata**:
  - in sda: 57/60 [0,863; 0,983];
  - però F5 dà 2/60 falsi eventi e ci sono eventi prima dell'urto;
  - in att: 34/60 [0,441; 0,684], smentita.
- **F-802.** Il nucleo v4 è `01-contatto/prove_volo_v4.py`. Con `VOLO_REGOLA=v3i` è il nucleo della fase 3 (D2). La v3
  resta intatta.
- **F-803.** K-709 è **risolta sul volume**: E1 con l'integratore stabile dà V 60/60 [0,940; 1], contro 48/60.
  - Il ritardo invece cambia: 48/60 [0,682; 0,882] entro 2 s, più 3/60 eventi prima dell'urto.
  - **V-13 passa da I a L.** Il rifacimento cambia anche il rumore delle camere, quindi non isola l'integratore.
- **F-804.** La taratura della confidenza riporta la fascia 1–2 s degli aerei da 0,71 a **0,89 [0,87; 0,91]**, e diventa
  **I**. Ha due condizioni:
  - l'89,5 % dei casi viene da 4 numeri di volo di una sola rotta;
  - in virata la copertura scende a 0,73 [0,67; 0,78] (**L**).
- **F-805.** F7 «scorta» entra nel caso centrale. È **S** con il radar a 360° (sda) per continuità, «mai libero»,
  contenimento dei detriti e assenza di falsi eventi in F7c. È **L** in quattro punti:
  - identità in vira/att: 43/60 [0,592; 0,815];
  - evento di lato o dietro col radar frontale: 1/60 e 0/60;
  - avviso al portatore non discriminante: 60/60 anche senza frammenti vicini;
  - margine dell'avviso sotto T_r = 0,25 s in 7 casi su 20 con l'urto a 10–30 m davanti (attacco).
- **F-806.** In F7 l'evento è sempre dichiarato **alla prima scansione** (ritardo 0,0 s in tutti i passaggi riconti). È un
  artefatto ottimista del simulatore, con due cause:
  - i 32 frammenti nascono tutti nel punto d'urto e sono visti subito: a 30–100 m anche RCS di 10⁻⁴ m² ritornano;
  - la saturazione delle camere è presa dalla finestra vera dell'evento.

  Quindi il ritardo dell'evento in F7 **non si presenta** come risultato.
- **F-807.** In F7 il tracciatore usa la **velocità vera del portatore** (`W["Vc"]`) in due punti: la porta Doppler e il
  percorso dell'avviso. Usa anche la posizione vera del portatore nel margine INS della regione.
  - Le misure invece usano la posa stimata.
  - È un uso del vero, piccolo ma da dichiarare: a velocità costante l'errore INS di velocità vale circa 0,02 m/s
    (ipotesi).
  - Miglioria: usare la velocità stimata dalla navigazione inerziale.
- **F-808.** Il controllo F7c **non contiene fenomeni che generano grappoli**: niente stormi di uccelli, chaff né
  pioggia. Lo 0/200 controlla solo il fondo di 0,5 falsi per scansione. **K-801:** SCORTA A-8 è classe S ↔ PA-9 mostra
  che la prova è debole. **Risoluzione:** resta S, ma con la frase «nel controllo simulato, senza clutter a grappoli».
- **F-809.** In F7 il radar non è accecato. La variante F7r lo acceca: il rapporto `05-scorta/ACCECAMENTO_RADAR.md` è
  arrivato alle 06:33, e ho ricontato i suoi grezzi (`riconta_f7r.py` → `riconto_f7r.txt`, identici al rapporto). Il
  modello di F7r è pessimista: ricevitore saturo per 0,2–2 s, occultamento × 0,3, cella «totale» con radar e camera
  ciechi insieme.
  - **Reggono:**
    - «libero» 0/60 in ogni cella;
    - continuità 59–60/60;
    - falsi eventi F7c 0/200;
    - contenimento del volume: tutti i campioni dentro.
  - **Crolla l'avviso al portatore** prima di un frammento entro 10 m:
    - davanti: 27/52 [0,387; 0,649] in att e 28/52 [0,405; 0,667] in sda;
    - vira: 19/55 e 21/55;
    - totale: **0/59 [0; 0,061]**.
  - **In att scendono:**
    - riacquisizione ≤ 2 s: davanti 41/60 [0,558; 0,787], vira 43/60 [0,592; 0,815];
    - evento: totale 7/60, vira 33/60.
  - **S-6 diventa condizionata** a «radar non disturbato».
  - Nota di conteggio: in totale/att l'unica riacquisizione spuria del rapporto (1/60) sta nel campo
    `riacq_spurie`, non in `assoc_detriti_non_dich` (0/60).
  - La cartella `05-scorta/correzione_f7r/` è in corso e non è considerata qui.

**Contraddizioni nuove (K#).**

| K# | Fra | Esito |
|---|---|---|
| K-801 | SCORTA A-8 (S) ↔ PA-9 | S con la condizione «senza clutter a grappoli» (F-808) |
| K-802 | TARATURA § 6, frase «da 85 a 89 in ogni fascia, 16 aerei» ↔ ATTACCO § 4 | la fascia 21–30 s è 0,845 [0,806; 0,878]; i mezzi sono 12 aerei (icao) e 4 numeri di volo. **Vale la frase di ATTACCO § 4** |
| K-803 | CONTATTO § 5 «entro 2,5 s 60/60» ↔ riconto | 0 ≤ ritardo ≤ 2,5 s dà **57/60 [0,863; 0,983]**. Il 60/60 conta i 3 negativi (riconto mio identico) |
| K-804 | VERDETTO_VOLO § 4, riga 3, «q × 4» ↔ TARATURA | non confermato: il gonfiamento che serve sta in σ_rif² (20 m per gli aerei), non in q |
| K-805 | VERDETTO_VOLO § 4, riga 10, «per il passo di Kalman il CERN dà l'FPGA più lento della CPU» ↔ FONTI n. 14 | vero **in latenza** (725 contro 250 ns). In portata l'FPGA è 4,5×; nel caso misurato il PCIe e 0,5 ms di latenza iniziale annullano il guadagno |
| K-806 | ARCO/voce v3 «sixteen real aircraft tracks… 92 to 98» ↔ K-802 | la voce va riscritta (§ 7) |

## 2. Tavola FINALE dei risultati presentabili

Riga fissa per tutte: «simulazione da schede · etichette a mano · nessun sensore fisico».

### 2.1 Volo ad alta velocità con eventi (caso centrale)

Fonti:
- nucleo v3i: `f19-volo/10-prove/passaggi_volo_v3i.jsonl`, idx 0–59 (F6 0–199);
- v4c: `01-contatto/valutazione_v4c.jsonl`, idx 1000–1059.

Ogni scenario ha una sola geometria nominale.

| # | IT (frase per la giuria) | EN | Classe | Intervallo · stato | Base matematica |
|---|---|---|---|---|---|
| V-1 | «Nei sei scenari di volo, dall'avaria alla collisione di droni, MoVi non ha mai detto "libero" dove c'era l'oggetto o un frammento.» | "In six flight scenarios, from an in-flight failure to a drone collision, MoVi never said 'clear' where the object or a fragment was." | S | F6 0/200 [0; 0,019]; le altre celle 0/60 [0; 0,060]; ancora 0 col nucleo v4 in tutte le 10 celle · sim | libero solo ciò che è osservato (CR-1); insieme di presenza a 210 m/s |
| V-2 | «Avaria in volo di un aereo a 135 m/s con fiammata: evento dedotto entro 1 s e camere dichiarate non affidabili, in 60 passaggi su 60.» | "In-flight failure of an aircraft at 135 m/s with a flash: event inferred within 1 s and cameras declared unreliable, in 60 of 60 simulated runs." | I (innesco ottimista) | 60/60 [0,940; 1] att e sda, v3i e v4 · sim | separazione di tracce e salute del sensore; la saturazione è presa dalla finestra vera |
| V-3 | «Dopo l'avaria i detriti a bassa energia restano nel volume dichiarato: tutti in 58 passaggi su 60.» | "After the failure, low-energy debris stays inside the declared volume: all of it in 58 of 60 runs." | I | 58/60 [0,886; 0,991] · sim | V(τ) balistico con dv ≤ 100 m/s |
| V-4 | «L'avviso arriva prima del primo frammento a terra, in 60 su 60; il margine minimo per un operatore è di 0,25–0,45 s.» | "The warning comes before the first fragment reaches the ground, in 60 of 60; the minimum margin for an operator is 0.25–0.45 s." | I | 60/60 [0,940; 1] · sim, ip (risposta umana 5,4 s, FAA AC 90-48E) | d = v·(L + t_risp + ritardo del mezzo) |
| V-5 | «Due droni veloci in rotta di collisione: avviso di prossimità almeno 10 s prima, in 60 su 60.» | "Two fast drones on a collision course: proximity warning at least 10 s ahead, in 60 of 60." | I (soglia dei 10 s non scritta prima) | 60/60 [0,940; 1] · sim | massimo avvicinamento a velocità costante |
| V-6 | «Dopo la collisione veloce, il punto vero e i frammenti sono sempre rimasti nella regione dichiarata.» | "After the fast collision, the true position and the fragments always stayed inside the declared region." | S come copertura | 60/60 [0,940; 1]; 939/939 campioni · sim | inviluppo con \|v\| ≤ 210 m/s |
| V-7 | «Quasi collisioni a 40 m e incroci veloci col nucleo: nessun falso evento.» | "Near misses at 40 m and fast crossings with the core: no false event." | S (nucleo v3i, senza v4c) | F6 0/200 [0; 0,019]; F1 e F5 0/60 [0; 0,060] · sim | conferma su più cicli |
| V-8 | «Con un radar a scansione elettronica a 10 Hz la regione non si perde mai.» | "With a 10 Hz electronically scanned radar, the region is never lost." | S in sda | 60/60 e 200/200 [0,981; 1] · sim; il 10 Hz viene da fonte di stampa (FONTI n. 3) | rivisita più breve della crescita dell'inviluppo |
| V-9 | «Col radar rotante a 1 Hz l'aereo veloce perde continuità, e MoVi lo dichiara.» | "With a 1 Hz rotating radar the fast aircraft loses continuity, and MoVi says so." | L | F1/att 39/60 [0,524; 0,758] · sim | — |
| V-10 | «Ottici accecati per 2–4 s: tutte le tracce conservano una regione; l'identità resta "presunta".» | "Optics blinded for 2–4 s: every track keeps a region; identity stays 'presumed'." | S (regione); L (identità, scambio 0,47–0,63) | 60/60 [0,940; 1] · sim | — |
| V-11 | «La collisione veloce non è ancora dichiarata come evento. Una regola di contatto in prova la riconosce entro 2 s in 57 passaggi su 60 col radar a scansione elettronica, ma dà ancora falsi eventi in un quasi incrocio a 39 m: 2 su 60. Non è adottata.» | "A fast collision is not yet declared as an event. A contact rule under test recognises it within 2 s in 57 of 60 simulated runs with the scanning radar, but still gives false events in a near crossing at 39 m (2 of 60): not adopted." | **L** | v3i 0/60 [0; 0,060]; v4c sda 57/60 [0,863; 0,983], F5 2/60 [0,009; 0,114], prima dell'urto 1/60; att 34/60 [0,441; 0,684]; varianti 16–19 su 20 · sim | conferma su tracce risolte e Doppler simulato (ip σ_vr 0,5 m/s) |
| V-12 | Avaria non contenuta (frammenti di disco a 250 m/s) | — | **NP** | V 0/10 [0; 0,278] · sim | — |
| V-13 | «Collisione fra droni lenti (8 m/s), con l'integratore stabile: evento entro 2 s in 48 su 60, con 3 eventi aperti prima dell'urto; i frammenti nel volume in 60 su 60.» | "Slow drone collision (8 m/s), stable integrator: event within 2 s in 48 of 60, with 3 opened before impact; fragments inside the volume in 60 of 60." | **L** per l'evento; **S** per il volume | 48/60 [0,682; 0,882]; 3/60 [0,017; 0,137]; V 60/60 [0,940; 1] · sim | fusione e separazione di tracce |

### 2.2 F7 «scorta»: MoVi a bordo di un drone in moto (caso centrale; addendum 15)

Fonte: `05-scorta/passaggi_valutazione.jsonl` (semi 20261121), riconto mio identico. L'attacco sta in
`attacco_f7.jsonl`: semi 20261199, 20 per cella e 60 per F7c; varianti con i semi 20261198 e 20261197.

| # | IT | EN | Classe | Intervallo · stato | Base matematica |
|---|---|---|---|---|---|
| S-1 | «A bordo di un drone, durante una collisione a 30–100 m con fiammata, fumo e detriti, MoVi non ha mai perso la regione che contiene il drone seguito: 60 passaggi simulati su 60 per ogni geometria, col radar a 360°.» | "On board a drone, through a collision 30–100 m away with flash, smoke and debris, MoVi never lost the region containing the tracked drone: 60 of 60 simulated runs for each geometry, with the 360° radar." | S | sda 60/60 [0,940; 1] ×4 (lato, davanti, dietro, vira); att 59/60 [0,911; 0,997] davanti; attacco 20/20 [0,839; 1] in ogni cella, anche con l'urto a 10–30 m · sim | regione = max(r al 99,99 % + margine INS, insieme di presenza r + 3σv·τ + a·τ²/2) |
| S-2 | «Mai "libero" sul drone seguito né su un frammento.» | "Never 'clear' on the tracked drone or on a fragment." | S (in parte per costruzione: il bersaglio sta spesso oltre la portata del «libero», 193 e 339 m) | 0/60 [0; 0,060] in ogni cella; attacco 0/20 ×16 celle · sim | libero solo se osservato, dentro la portata per 10⁻⁴ m², fuori da regioni e volume |
| S-3 | «Nessun frammento attribuito al drone seguito senza dirlo: le misure nel volume dei detriti rendono l'identità "presunta, dubbia".» | "No fragment attributed to the tracked drone without saying so: measurements inside the debris volume make the identity 'presumed, doubtful'." | S | 0/60 [0; 0,060] in ogni cella; attacco 0/20 · sim | porta di Mahalanobis + Doppler; marcatura nel volume |
| S-4 | «Il volume dei detriti dichiarato ha contenuto tutti i frammenti simulati, anche con frammenti più veloci di quanto dichiarato.» | "The declared debris volume contained every simulated fragment, even with fragments faster than declared." | S nel modello (resistenza lungo −v, vento nullo) | sda 60/60 [0,940; 1] ×4; campioni 44 051, 43 681, 43 600 e 42 950, tutti dentro; dv 100 m/s: 20/20 ×2 · sim, dim nel modello | cono {p0 + S(vc+u)} ∩ sfera del cammino L(τ) con d\|v\|/dt ≤ g − k\|v\|² |
| S-5 | «Camere dichiarate non affidabili in ogni istante di saturazione; nessun falso evento in 200 voli di controllo simulati senza clutter a grappoli.» | "Cameras declared unreliable at every saturated instant; no false event in 200 simulated control flights without clustered clutter." | S (innesco ottimista; controllo debole, F-808) | 0 cicli saturi «affidabili»; F7c 0/200 [0; 0,019] ×2; attacco 0/60 ×2 e quasi collisione a 5–20 m 0/60 ×2 · sim | — |
| S-6 | «Con il radar non disturbato, se il percorso del portatore entra nel volume dei detriti, l'avviso arriva prima: in tutti i casi simulati. Con il radar accecato no.» | "With the radar undisturbed, if the carrier's path enters the debris volume the warning comes first in every simulated case; with the radar blinded, it does not." | I con radar indisturbato; **L** con radar accecato | F7: davanti 56/56, vira 54/54 [0,934; 1], margine minimo 0,4 s; F7r: davanti 27–28/52, vira 19–21/55, totale 0/59 [0; 0,061] · sim | percorso stimato a 5 s ∩ volume allo stesso istante |
| S-6r | «Abbiamo accecato anche il radar fino a 2 s, insieme alle camere: MoVi non ha mai detto "libero" né sul drone seguito né sui frammenti, e il drone è rimasto nella regione in 59–60 passaggi su 60.» | "We also blinded the radar for up to 2 s, together with the cameras: MoVi never said 'clear' on the tracked drone or on any fragment, and the drone stayed inside its region in 59–60 of 60 runs." | S | F7r: libero 0/60 [0; 0,060] in ogni cella; continuità 59/60 [0,911; 0,997] (totale/att), le altre 60/60 · sim, modello di cecità pessimista (ip) | come S-1 e S-2; il radar è dichiarato «non affidabile» in ogni ciclo saturo |
| S-7 | «Il volume è prudente: l'avviso scatta anche quando nessun frammento passa vicino.» | "The volume is conservative: the warning also fires when no fragment passes close." | L | lato/sda 60/60, dietro/sda 60/60 senza intersezione · sim | — |
| S-8 | «Con un radar solo frontale: un urto di lato o dietro non è visto (MoVi dice "non so", mai "libero"); se il drone seguito vira fuori dal campo, l'identità non è più garantita.» | "With a forward-only radar, a collision to the side or behind is not seen (MoVi says 'I don't know', never 'clear'); if the tracked drone turns out of the field, identity is no longer guaranteed." | L | evento lato/att 1/60 [0,003; 0,089], dietro/att 0/60; identità vira/att 43/60 [0,592; 0,815], attacco 15/20 [0,531; 0,888] · sim | — |
| S-9 | Margine dell'avviso con l'urto a 10–30 m davanti | — | **L (nuovo)** | 7 casi su 20 sotto T_r = 0,25 s (minimo 0,1 s), att e sda · sim | fisica: a 10 m e 30 m/s restano circa 0,3 s |
| S-10 | Ritardo della dichiarazione dell'evento in F7 | — | **non presentabile** (F-806) | 0,0 s in tutti i passaggi: artefatto | — |
| S-11 | Radar accecato dalla nube vicina (F7r) | — | provato in simulazione con un modello pessimista: S per «libero» e continuità (S-6r), **L** per l'avviso (S-6) e per la riacquisizione e l'evento in att | vedi F-809 · sim, ip | — |

### 2.3 Sito con rullaggio (sezione breve; verdetti f15, invariati)

| # | IT | EN | Classe | Intervallo · stato |
|---|---|---|---|---|
| LP-1 | «Drone a 15–21 m/s dietro un edificio, annunciato in tempo.» | "A drone at 15–21 m/s behind a building, announced in time." | S | 200/200 [0,981; 1] · sim |
| LP-2 | «Mai "libero" sul drone, con la mappa dichiarata.» | "Never 'clear' on the drone, with the declared map." | S | 0/171 [0; 0,022] · sim |
| LP-3 | «Il drone che rallenta o si ferma resta nell'avviso.» | "A drone that slows or stops stays in the warning." | I | 188/200 [0,898; 0,965] · sim |
| LP-4/5 | «Aereo in rullaggio: con tre sensori fusi l'avviso arriva in tempo; col solo radar no.» | "Taxiing aircraft: with three fused sensors the warning is timely; with radar alone it is not." | S / L | 200/200 [0,981; 1] / 50/200 [0,195; 0,314] · sim |
| LP-6 | «Per gli aerei in volo, l'avviso al sito non è tempestivo.» | "For aircraft in flight, the site warning is not timely." | L | servono 3410 m · calc |
| LP-11 | «L'avviso si spegne solo guardando tutta la zona.» | "The warning clears only after the whole zone is observed." | S | 0/600 [0; 0,006] · sim |

### 2.4 Corto raggio e altri usi (invariati)

- **S:** CR-1 (dimostrazione condizionata); CR-3: 0/23 402 [0; 0,0002]; CR-6: 0/4324 [0; 0,001].
- **I:** CR-4 ≥ 0,92 a 2 s; CR-8 176/180 [0,944; 0,991], dominio stretto.
- **L:** CR-10.
- **NP:** CL-1 (classificatore).
- Persona non vedente: è un aiuto d'avviso, non sostituisce il bastone né il cane guida; nessuna cifra.

## 3. F3 ed E1: che cosa si dice

- **F3 (collisione veloce di droni, 40 e 35 m/s).** È un **limite dichiarato**, non «evento riconosciuto in N su 60».
  - Il nucleo adottato (v4 con `VOLO_REGOLA=v3i`) dà 0/60 [0; 0,060].
  - Si mostra quello che il sistema fa: avviso di prossimità almeno 10 s prima (V-5) e regione mantenuta (V-6).
  - La regola v4c si cita **solo** come miglioria in prova, con la frase di V-11. Comprende:
    - 57/60 [0,863; 0,983] in sda;
    - nelle varianti di geometria 16–19 su 20 (quota 400 m: 16/20 [0,584; 0,919]);
    - falsi eventi F5 2/60 [0,009; 0,114] ed F1/att 1/60;
    - eventi prima dell'urto: 1/60 nominale, fino a 2/20 in sda e 4/20 in att nelle varianti;
    - att 34/60.
- **E1 (droni lenti, 8 e 6,7 m/s, integratore stabile).** Il volume ha contenuto i frammenti in 60/60 [0,940; 1].
  - Evento entro 2 s: 48/60 [0,682; 0,882], con 3/60 [0,017; 0,137] eventi aperti 11 s prima dell'urto.
  - Entro 2,5 s, contando solo i ritardi ≥ 0: 57/60 [0,863; 0,983] (soglia notata dopo).
  - **L** per l'evento. Il «51/60» non si dice più senza «con Eulero; con l'integratore stabile 48 su 60 e 3 prima
    dell'urto».
  - Il motivo dei 3 eventi precoci (tracce di camera al primo aggancio) è non verificato.

## 4. Confidenza nel tempo dopo la taratura

**Formula** (dim nel modello a velocità quasi costante con rumore gaussiano, verificata numericamente):

    σ²(τ) = σ0² + 2σ0v·τ + σv²·τ² + q·τ³/3 + σ_rif²
    C(τ) = 1 − exp(−r²/2σ²(τ)),   r_0,9(τ) = 2,146·σ(τ)
    più regimi: C = Σ μ_j P_j, con i μ_j fissati alla perdita; mostrata come C̃(τ) = min_{s≤τ} C(s)

- C̃ è monotona **per costruzione**: la C grezza ha 45 violazioni su 1440 passi.
- Dopo la formula viene una ricalibrazione isotonica per fascia e per regime dominante alla perdita, fatta sulla metà
  di taratura.
- Fuori modello (urto, avaria) si mostra l'insieme di presenza r0 + v_max·τ, con v_max 210 m/s per gli aerei e 45 m/s
  per i droni. È un contenimento garantito con |v| ≤ v_max (condizionato a |p(0) − p̂0| ≤ r0), non una probabilità.

**Tabella da mostrare** (aerei, metà di prova, regione al 90 %, casi correlati; graffe = bootstrap per mezzo;
pub):

| τ | 1–2 s | 3–5 s | 6–10 s | 11–20 s | 21–30 s | in virata (tutte) | in accelerazione |
|---|---|---|---|---|---|---|---|
| prima (IMM f19) | 0,71 [0,67; 0,74] | 0,92 | 0,95 | 0,98 | 0,96 | 0,905 | 0,841 |
| **dopo la taratura** | **655/733 = 0,89 [0,87; 0,91]** {0,88; 0,92} | 372/416 = 0,89 [0,86; 0,92] | 344/385 = 0,89 [0,86; 0,92] | 334/374 = 0,89 [0,86; 0,92] | 328/388 = **0,85 [0,81; 0,88]** {0,78; 0,89} | **161/221 = 0,73 [0,67; 0,78] L** | **81/107 = 0,76 [0,67; 0,83] L** |
| r_0,9 mediano | 39 m (era 27) | — | 138 m (era 264) | — | 1106 m (era 2065) | — | — |

- Scarto medio dal 90 %: da 0,081 a 0,016.
- Droni ad ala fissa e multirotori: 0,89–0,93, ma da uno o pochi esemplari.
- Senza i due mezzi più pesanti, la fascia 21–30 s vale 0,81 [0,75; 0,86].

**Frase IT (I):** «Dopo la perdita, nella simulazione su traiettorie di volo pubbliche, la regione al 90 % ha
contenuto l'aereo da 85 a 89 volte su 100 fra 1 e 30 s. I casi vengono per nove decimi da quattro voli della stessa
rotta. In virata la copertura scende a 73 su 100: è un limite dichiarato.»
**EN:** "After the track is lost, on public flight trajectories with a simulated sensor, the 90 % region contained the
aircraft 85 to 89 times in 100 from 1 to 30 s; nine tenths of the cases come from four flights on one route, and in
turns coverage drops to 73 in 100: a declared limit."

**F7, bersaglio a perdita totale** (calc da ipotesi; `05-scorta/curva_F7.json`, porta g = 30 m). In att C scende da
1,00 (τ = 0) a 0,62 (2 s) e a 0,09 (5 s); t(C < 0,9) = 1,35 s.
- r_0,9 passa da 6,5 a 46 m a 2 s, e a 146 m a 5 s. L'insieme di presenza è di 75 m a 2 s.
- Durante l'accecamento ottico misurato, la quota di cicli dentro r_0,9 è 0,86–0,93 in att: **L**, non «90 %».
- Dentro la regione dichiarata ci sono tutti i cicli.

**Da non mostrare:**
- la C del nucleo in att (F6: 1/78);
- la zona «al 99 %» della sola covarianza;
- la C numerica dei registri F2, F3 ed F5 (minimo progressivo non applicato ai registri, TARATURA § 6);
- «tarata» senza condizione;
- «16 aerei».

## 5. Da proposta a sistema attuato (aggiornata)

Le latenze sono **stime** da `02-sensori-hw/latenza.json` (non ricontato da me).

| Limite | Miglioria (che cosa e come) | Stato ed esito / prova che la decide |
|---|---|---|
| F3: collisione veloce non dichiarata | regola di contatto v4c (tracce risolte e mature, convergenza ≥ 10 m/s, fusione o sparizione, tracce nuove o Doppler fuori norma) | **miglioria applicata in simulazione, non adottata**: sda 57/60 [0,863; 0,983], ma F5 2/60 e eventi prima dell'urto; att 34/60. Prossimi passi: Doppler sulla cella unita, riagganci esclusi, p_c raggiunto, radar vicino su una griglia fissata prima. Soglia: F3/sda ≥ 54/60 con F5, F1 e F6 a 0 su semi 2000+ e su ≥ 10 geometrie |
| Insieme di presenza a 90 m/s nel nucleo | inviluppo a 210 m/s (v3i → nucleo v4) | **miglioria applicata in simulazione**: F4/att da 13/60 a 60/60; F6/att da 126/200 a 186/200 |
| E1 con Eulero instabile | integratore semi-implicito | **miglioria applicata in simulazione**: V da 48/60 a 60/60 [0,940; 1]; evento 48/60 e 3 precoci (ora L) |
| C(τ) ottimista a 1–2 s | σ_rif² (20 m per gli aerei), regime CAL, pesi fissati, isotonica, minimo progressivo | **miglioria applicata su dati pubblici**: 0,71 → 0,89 [0,87; 0,91]; scarto 0,016. **Peggiora la virata** (0,91 → 0,73) e l'accelerazione resta a 0,76. Prossimo: ricalibrazione condizionata a una manovra rilevata in modo causale (virata ≥ 0,85; smentita se < 0,80); 5 divisioni; divisione per rotta |
| C del nucleo in att mal tarata | minimo progressivo e covarianza gonfiata sui registri F1/F6 | **non fatto**: soglia C ≥ 0,9 con copertura ≥ 0,80 |
| Avaria non contenuta (0/10) | profilo dv ≥ 300 m/s, impronta ≥ 10 km, Doppler sui frammenti | non fatto; 60/60 dentro V |
| Innesco della fiammata ottimista (anche in F7) | saturazione dall'istogramma della camera | non fatto; ritardo ≤ 1 ciclo in ≥ 0,9 su registrazioni vere |
| Identità dopo la cecità (0,47–0,63) | Doppler, RCS, firma termica per riassociare | non fatto; scambio ≤ 0,2 |
| Continuità col radar rotante a 1 Hz | radar a scansione elettronica 10 Hz (EchoShield: 10 Hz da stampa, campo **120×80°** dal produttore; portate per bersaglio **non verificate**, forse dell'EchoGuard) | simulato in sda: 60/60; manca la misura sul sensore |
| **F7: radar frontale ±60°** | radar a 360° (4 pannelli) o camera su brandeggio puntata dalla traccia | **miglioria applicata in simulazione**: con sda identità in vira 60/60, evento di lato e dietro 60/60 (contro 43/60, 1/60, 0/60) |
| **F7: radar non accecato dall'esplosione** | ricevitore saturo per 0,2–2 s e occultamento (variante F7r, modello pessimista) | **miglioria applicata in simulazione**:<br>- «libero» 0/60 e continuità 59–60/60 reggono;<br>- l'avviso prima dei frammenti crolla (totale 0/59);<br>- la riacquisizione in att scende a 41–43/60.<br>Prossimo: avviso immediato «evento vicino non localizzato» alla saturazione congiunta; riacquisizione presunta anche dentro il volume con coerenza Doppler; modello dell'AGC dalla scheda. Soglie: avviso ≥ 0,9 con falsi in F7c ≤ 0,05; riacquisizione davanti/att ≥ 51/60 |
| **F7: volume prudente, avviso non discriminante** (60/60 senza frammenti vicini) | δv per frammento dal Doppler; volume per grappoli tracciati | non fatto; avviso falso ≤ 10 % con contenimento al 100 % |
| **F7: margine dell'avviso < T_r con l'urto a 10–30 m** (7/20) | previsione dell'urto dalle tracce prima del contatto (avviso di prossimità, come V-5) | non fatto; margine ≥ 0,25 s in 20/20 a 10–30 m |
| **F7: velocità vera del portatore nel tracciatore** (F-807) | velocità dalla navigazione inerziale; covarianza INS correlata nello stato | non fatto; stesse soglie di S-1…S-6 |
| **F7: controllo senza clutter a grappoli** | F7c con stormi, pioggia e chaff simulati | non fatto; falsi eventi 0/200 |
| **F7: tracciatore nuovo, non il nucleo** | integrare F7 nel nucleo v4 con sensore in moto | non fatto |
| Una geometria per scenario | ≥ 10 geometrie | in parte: F3 su 5 varianti (16–19/20 in sda); F7 su 3 varianti |
| Tempestività verso l'umano | avviso con la direzione: 5,4 s invece di 12,5 s (FAA AC 90-48E, Tabella 1, **aperta**); 2005 m invece di 3312 m a 250 m/s | calc; prova con operatori |
| Latenza del calcolo | FPGA o ASIC per segnale e CFAR (CFAR su FPGA in 0,6 µs, Sim 2023; range-Doppler 85× su ARM, Choi 2021); calcolo dedicato totale 0,08–1,2 ms (**ip**). Analogia con i chip per modelli linguistici (Taalas HC1 circa 17 000 token/s contro circa 230 su H200, dato aziendale da prove interne; Cerebras 1936), valida solo per i carichi limitati dalla memoria. Passo di Kalman su FPGA: più lento in latenza, 4,5× in portata (CERN) | misura su FPGA reale: ≤ 1,2 ms per aggiornamento |
| Primo avviso verso una macchina | la leva è la rivisita: 10 Hz 0,62 s → 40 Hz 0,17 s (calc da ip) | misura end-to-end |
| Mappa, classificatore, sensore fisico | LiDAR, classificatore per classe, prove sul campo | tutte |

## 6. Fonti: quali frasi cambiano (da FONTI_APERTE)

1. Si cita **AC 90-48E (2022)**, non la 90-48D cancellata. Stessa Tabella 1: 12,5 s compresi i 2,0 s del mezzo; 5,4 s
   con la direzione. Le distanze restano 3312 m e 1058 m.
2. **EchoShield.** Restano: banda Ku, 10 Hz (stampa specializzata 2026).
   - Il campo diventa **120×80°**: il 130×90° si toglie.
   - Le portate 2,5, 1,4 e 1,0 km diventano «non verificate» (forse dell'EchoGuard).
   - Le distanze che ne dipendono sono «ipotesi».
3. **CERN.** Si toglie «FPGA più lento della CPU» detto senza condizione. Al suo posto: «più lento in latenza (725
   contro 250 ns), circa 4,5× in portata; nel caso misurato PCIe e latenza iniziale annullano il guadagno».
4. **Taalas.** «Circa 17 000 token/s per utente, dato dell'azienda; nessuna misura indipendente a febbraio 2026». Si
   toglie «14 357».
5. **CFAR.** Il preprint si toglie. Al suo posto `sim2023` (0,6 µs) e `choi2021` (85×), come analogia.
6. **ADS-B.** ≥ 1 messaggio/s e latenza ≤ 2,0 s (14 CFR 91.227). Il ritmo di «0,5 s» è non verificato.
7. **Restano «scheda non aperta»:** CM202A e il ΔT della SupIR. Per la SupIR, «oltre 25 km» è un dato del produttore su
   un bersaglio grande.
8. **Fonti nuove.** OpenSky (`schafer2014`) per i dati, e `blom1988`, `mazor1998`, `li2003` per l'IMM.
   - Per le ultime tre sono verificati solo i metadati.
   - Le voci per RIFERIMENTI vanno da [394] a [410]. `imhof1961` e `ruben1962` (capitolo) non sono stati aperti da
     nessuno: si tolgono o si segnano «non verificata».

## 7. Frasi da non dire (aggiornate; solo quelle false o non provate)

- «MoVi rileva la collisione in volo», oppure «riconosce la collisione dei droni veloci entro 2 s». La v4c non è
  adottata: 57/60 solo in prova, con falsi eventi.
- «Entro 2 s in 51 su 60» senza la nota sull'integratore: con l'integratore stabile sono 48 su 60, più 3 eventi prima
  dell'urto. Anche «sempre», o «entro N s» senza «in k su n, simulato».
- «Detriti sempre nel volume» per l'avaria non contenuta, e «avaria non contenuta» come nome di F4.
- «Confidenza 99 %», «zona al 99 %», «confidenza tarata» senza condizione, «16 aerei reali», «da 85 a 89 in ogni
  fascia» detto con 16 aerei, «da 92 a 98» (era prima della taratura e va tolto dalla voce v3).
- «Identità confidente al 79 %»; «identità certa» in F7: è «presunta».
- «Il calcolo dedicato porta l'avviso sotto il millisecondo», «in tempo reale», «l'hardware riduce il ritardo
  dell'evento di N volte», «sda più rapido grazie all'FPGA», «l'FPGA è più lento della CPU» senza condizione,
  «14 357 token/s».
- «Umano senza ausilio 3812 m» (sono 3312) o «1237 m» (sono 1058).
- «Validato», «testato su sensori» o su hardware, «certificabile», «detect and avoid», il lessico d'ingaggio.
- In F7, «MoVi segue» o «insegue» o «intercetta»: si dice «mantiene la traccia».
- In F7, «riacquisisce sempre entro 2 s» senza «radar non accecato nel simulato».
- In F7r, «avvisa sempre dei detriti» (totale 0/59) e «il radar vede attraverso l'esplosione»: vale per il fumo e la
  luce, non per la nube vicina.
- In F7, «dichiara l'evento istantaneamente» o «in 0 s» (F-806).
- In F7, «funziona con un radar piccolo di bordo in ogni geometria».
- In F7, «l'avviso di detriti è preciso».
- In F7, «nessun falso evento» senza «nel controllo simulato».
- «Avviso tempestivo al sito per gli aerei in volo» (LP-6).
- «Mai "libero"» per la lunga portata senza «con la mappa dichiarata».
- EchoShield «130×90°» e le portate EchoShield 2,5, 1,4 e 1,0 km come dato verificato.

## 8. Per il video

**Vincolo assoluto dell'utente:** durata totale **non oltre 176,0 s**, da misurare con ffprobe sul file finale;
obiettivo fra 168 e 175 s.
- La bozza v3 (`video/progetto_v3/tempi/scene_v3_en.json`) fa 171,903 s su 10 scene.
- F7 va **subito dopo il volo veloce principale e subito prima del sito e rullaggio**.
- Proposta di bilancio (a carico del montaggio, da rimisurare):
  - ordine: s1 … s7 (confidenza) → **F7 (circa 17 s)** → s9 (sito e corto raggio) → s10 (limiti e titoli);
  - la scena s8 (hardware, 16,2 s) si riduce a una riga di circa 6 s, oppure si fonde nella scala di s10;
  - s5 (F3) scende a circa 15 s;
  - s7 scende a circa 26 s, perché la frase cambia.
  - Somma stimata: circa 172 s. Se si sfora, si taglia: mai accelerare la voce, mai oltre 176,0 s.

**Etichette per scena.** Riga per tutte le scene Simulation: «Simulated · state-of-the-art sensor parameters assumed ·
no physical sensor».

| Scena | Etichetta | Cifre e testi consentiti |
|---|---|---|
| s1 introduzione | Schematic | nessuna cifra |
| s2 tre risposte | Schematic | — |
| s3 F1 (mai libero) | Simulation | `V-1` |
| s4 F4 avaria | Simulation | `V-2`, `V-3`; nome «failure with low-energy debris»; «optimistic trigger» |
| s5 F3 collisione veloce | Simulation | `V-5`, `V-6`; testo «collision not yet declared as an event: region kept»; facoltativo `V-11-PROVA` come riga piccola «contact rule under test: 57/60 [0.86; 0.98] · 2/60 false events · not adopted». Il registro non contiene l'evento: niente «EVENT: COLLISION» |
| s6 F5 ottici ciechi | Simulation | `V-10`; identità «presumed» |
| s7 confidenza | Schematic (curva) + Public trajectories (punti) | `C-TAR-1-2`, `C-TAR-BANDA`, `C-TAR-VIRATA`; formula a schermo; niente «16 aircraft» |
| **F7 scorta** (nuova) | **Simulation** (registri `registro_F7_*_v2.jsonl`, sda, idx 0; **mai** quelli senza `_v2`) | `F7-CONT`, `F7-LIBERO`, `F7-ID`, `F7-VOL`, `F7-CAM`, `F7-LIM-FRONTALE`, `F7R-CIECO`. Righe obbligatorie: «flash trigger optimistic», e una delle due che seguono. Con i registri F7 `_v2` va «radar assumed unaffected in this run; with the radar also blinded up to 2 s: never clear, region kept (sim.)». Con i registri `registro_F7r_*.jsonl` (0 violazioni del validatore) va «radar blinded up to 2 s · pessimistic model». In ogni caso niente avviso dei detriti presentato come affidabile con il radar cieco. Testo d'evento «nearby collision · inferred · debris volume declared, never clear inside». Niente ritardo dell'evento. L'avviso al portatore si mostra come «warning: path enters debris volume», con l'etichetta «conservative». Verbo: «keeps the track» |
| s8 hardware (ridotta) | Schematic · ESTIMATE | `HW-CALC`: «dedicated processing estimated 0.08–1.2 ms (estimate by analogy, not a measurement); the sensor revisit dominates» |
| s9 sito, rullaggio, corto raggio | Simulation (sito), Schematic (persona) | `LP-1`, `LP-4`; persona senza cifre |
| s10 limiti | Schematic | testo dei limiti: tutto simulato; collisione veloce non ancora dichiarata; avviso al sito tardivo per gli aerei in volo; radar accecato non provato |

**Voce EN della scena F7** (proposta, 38 parole, circa 17 s a 135 parole al minuto, da misurare): «Now MoVi rides on a
drone, keeping the track of a fast drone ahead. Nearby, two drones collide: flash, smoke, debris. In sixty of sixty
simulated runs, the tracked drone stayed inside its region, and no fragment was ever called clear.»
**IT:** «Ora MoVi è a bordo di un drone e mantiene la traccia di un drone veloce più avanti. Accanto, due droni si
scontrano: fiammata, fumo, detriti. In sessanta prove simulate su sessanta il drone seguito è rimasto nella sua
regione, e nessun frammento è stato detto libero.»

**Voce s7 (sostituisce «sixteen real aircraft… ninety-two to ninety-eight… seventy-one»):** «On public flight tracks,
with a simulated sensor, the region held the aircraft eighty-five to eighty-nine times in a hundred, from one to thirty
seconds. In turns, seventy-three: a declared limit.»
**Voce s5:** «After the impact, the collision is not yet declared as an event, but the region is kept: the fragments
stayed inside it in every simulated run.» Resta com'è, è già conforme.

**Blocco JSON delle cifre consentite** (le chiavi esistenti di `cifre.json` non elencate qui restano valide solo se
coincidono con § 2):

```json
{
  "V-1": {"valore": "0 runs with 'clear' on the true object or a fragment", "intervallo": "0/200 [0; 0.019] (F6); 0/60 [0; 0.060] other cells", "stato": "simulato", "fonte": "f19-volo/10-prove/passaggi_volo_v3i.jsonl; f20/01-contatto/valutazione_v4c.jsonl; f20/20-verdetto/riconto_finale.txt", "frase_en": "In six flight scenarios, MoVi never said clear where an aircraft, a drone or a fragment was."},
  "V-2": {"valore": "60/60", "intervallo": "[0.940; 1]", "stato": "simulato (innesco ottimista)", "fonte": "VERDETTO_FINALE §2.1 V-2; riconto_finale.txt F4", "frase_en": "MoVi infers the event and declares the cameras unreliable within one second, in sixty of sixty simulated runs."},
  "V-3": {"valore": "58/60", "intervallo": "[0.886; 0.991]", "stato": "simulato", "fonte": "VERDETTO_VOLO §2.1 V-3", "frase_en": "Low-energy debris stays inside the declared volume in fifty-eight of sixty."},
  "V-5": {"valore": "60/60, at least 10 s ahead", "intervallo": "[0.940; 1]", "stato": "simulato", "fonte": "VERDETTO_VOLO §2.1 V-5", "frase_en": "MoVi warns of the close pass at least ten seconds ahead."},
  "V-6": {"valore": "60/60 runs; 939/939 samples", "intervallo": "[0.940; 1]", "stato": "simulato", "fonte": "VERDETTO_VOLO §2.1 V-6", "frase_en": "After the impact the region is kept: the fragments stayed inside it in every simulated run."},
  "V-10": {"valore": "60/60 tracks keep a region", "intervallo": "[0.940; 1]", "stato": "simulato", "fonte": "VERDETTO_VOLO §2.1 V-10", "frase_en": "Radar alone keeps a region for every track; identity is presumed."},
  "V-11-PROVA": {"valore": "57/60 within 2 s (scanning radar), 2/60 false events (F5), not adopted", "intervallo": "[0.863; 0.983]; false [0.009; 0.114]", "stato": "simulato (regola in prova, limite)", "fonte": "f20/01-contatto/CONTATTO.md §2; riconto_finale.txt", "frase_en": "A contact rule under test recognises it in fifty-seven of sixty, but still gives false events: not adopted."},
  "C-TAR-1-2": {"valore": "0.89 (655/733)", "intervallo": "[0.87; 0.91] cases, correlated", "stato": "su dati pubblici, sensore simulato", "fonte": "f20/02-taratura/TARATURA.md §3; f20/10-attacco/riconto_taratura.txt", "frase_en": "At one to two seconds, the region held the aircraft eighty-nine times in a hundred."},
  "C-TAR-BANDA": {"valore": "0.85–0.89 from 1 to 30 s", "intervallo": "21–30 s: 0.85 [0.81; 0.88]", "stato": "su dati pubblici, sensore simulato; 89.5% of cases from 4 flights of one route", "fonte": "f20/10-attacco/ATTACCO_FINALE.md §4", "frase_en": "On public flight tracks the region held the aircraft eighty-five to eighty-nine times in a hundred, from one to thirty seconds."},
  "C-TAR-VIRATA": {"valore": "0.73 (161/221)", "intervallo": "[0.67; 0.78]", "stato": "su dati pubblici; limite", "fonte": "f20/02-taratura/TARATURA.md §3", "frase_en": "In turns, seventy-three: a declared limit."},
  "F7-CONT": {"valore": "60/60 per geometry (360-degree radar)", "intervallo": "[0.940; 1] x4; attack 20/20 [0.839; 1]", "stato": "simulato", "fonte": "f20/05-scorta/passaggi_valutazione.jsonl; f20/20-verdetto/riconto_finale.txt, conteggi_attacco_f7.txt", "frase_en": "In sixty of sixty simulated runs, the tracked drone stayed inside its region."},
  "F7-LIBERO": {"valore": "0 runs with 'clear' on the tracked drone or a fragment", "intervallo": "0/60 [0; 0.060] every cell", "stato": "simulato", "fonte": "riconto_finale.txt F7", "frase_en": "No fragment was ever called clear."},
  "F7-ID": {"valore": "0 fragments attributed to the tracked drone without saying so", "intervallo": "0/60 [0; 0.060] every cell", "stato": "simulato", "fonte": "riconto_finale.txt F7", "frase_en": "Inside the debris volume the identity becomes presumed, doubtful."},
  "F7-VOL": {"valore": "every simulated fragment sample inside the declared volume", "intervallo": "60/60 [0.940; 1] per cell (sda)", "stato": "simulato; dimostrato nel modello (resistenza, vento nullo)", "fonte": "riconto_finale.txt F7; conteggi_attacco_f7.txt dv100", "frase_en": "The declared debris volume contained every simulated fragment."},
  "F7-CAM": {"valore": "0 saturated cycles with cameras 'reliable'; 0/200 false events", "intervallo": "0/200 [0; 0.019]", "stato": "simulato (innesco ottimista; controllo senza clutter a grappoli)", "fonte": "riconto_finale.txt F7c", "frase_en": "Cameras declared unreliable at every saturated instant; no false event in two hundred simulated control flights."},
  "F7-LIM-FRONTALE": {"valore": "forward-only radar: side/behind collision seen 1/60 and 0/60; identity in a turn 43/60", "intervallo": "43/60 [0.592; 0.815]", "stato": "simulato; limite", "fonte": "riconto_finale.txt F7 att", "frase_en": "With a forward-only radar, a collision to the side is not seen: MoVi says I don't know, never clear."},
  "F7R-CIECO": {"valore": "radar blinded up to 2 s with the cameras: 0 runs with 'clear'; region kept 59-60/60", "intervallo": "0/60 [0; 0.060] every cell; continuity 59/60 [0.911; 0.997] worst cell", "stato": "simulato (modello di cecita' pessimista, ipotesi)", "fonte": "f20/05-scorta/ACCECAMENTO_RADAR.md; f20/20-verdetto/riconto_f7r.txt", "frase_en": "Even with the radar blinded for up to two seconds, MoVi never called a fragment clear."},
  "LP-1": {"valore": "200/200", "intervallo": "[0.981; 1]", "stato": "simulato", "fonte": "f15-lunga-portata/60-fase2c/02-verdetto/VERDETTO_2C.md", "frase_en": "A drone behind a building, warned in time in two hundred of two hundred simulated runs."},
  "LP-4": {"valore": "200/200 with three fused sensors", "intervallo": "[0.981; 1]", "stato": "simulato", "fonte": "VERDETTO_2C", "frase_en": "A taxiing aircraft, warned in time with three fused sensors."},
  "HW-CALC": {"valore": "0.08–1.2 ms dedicated processing", "intervallo": "range of estimates, no measurement", "stato": "ipotesi (analogia)", "fonte": "f19-volo/02-sensori-hw/latenza.json; VERDETTO_VOLO K-707", "frase_en": "Dedicated chips suggest processing in 0.08 to 1.2 milliseconds: an estimate by analogy, not a measurement."}
}
```

## 9. Documento tecnico e proposta: che cosa cambia

**Documento tecnico v3** (D6: copia della v2 in `allegato_tecnico/v2/` prima di modificare). I capitoli si prendono da
`04-capitolo/`: `11_volo_alta_velocita.tex` e `12_da_proposta_a_sistema.tex`.
- **Tavola.** Al posto della V-1…V-13 del capitolo va quella del § 2.1 di questo verdetto: V-11 con la frase della v4c
  in prova, V-13 passata a L.
- **Marcatori:**
  - `%% MIGLIORIA-F3` riceve l'esito del § 3, cioè regola provata e non adottata, con la tabella delle varianti di
    ATTACCO § 1;
  - `%% MIGLIORIA-TARATURA` riceve la tabella del § 4, con la virata L e la concentrazione su una rotta;
  - `%% MIGLIORIA-E1` riceve 48/60, i 3 eventi precoci e V 60/60.
- **Sezione nuova «F7: sensore a bordo di un drone in moto».** Comprende:
  - il modello del portatore e della navigazione inerziale (ipotesi);
  - il volume dei detriti con L(τ) (proposizione nel modello);
  - la tavola § 2.2;
  - i limiti F-806, F-807, F-808 e S-9;
  - le righe F7 della tabella § 5.
- **Tabella «da proposta a sistema»:** quella del § 5, per intero.
- **Fonti:** le correzioni del § 6; si tolgono le citazioni `DA_VERIFICARE` non aperte, oppure si segnano «non
  verificata»; si ripulisce la nota interna di `faa-ac-90-48d` e si cita la 90-48E.
- **Dimostrazioni dal capitolo:**
  - t_C = 0 solo con σ0v ≥ 0;
  - il contenimento è condizionato a |p(0) − p̂0| ≤ r0;
  - la C della miscela non è monotona in generale, e il minimo progressivo lo è.
- **Rullaggio e altri usi:** in una sezione breve (§ 2.3 e § 2.4).

**Proposta v3.0** (due pagine):
- caso centrale: volo veloce, con V-1, l'avaria (V-2…V-4) e la confidenza tarata (§ 4, con la virata come limite);
- F7 «scorta» in tre righe: S-1, S-2, S-4 e S-6r (radar accecato), più i limiti del radar frontale e dell'avviso con il radar cieco;
- la collisione veloce come miglioria in prova (V-11);
- il sito e il corto raggio come altri usi;
- la riga «tutto simulato, nessun sensore fisico».

**F7r (radar accecato).** `ACCECAMENTO_RADAR.md` è arrivato alle 06:33 ed è ricontato (F-809). Documenti e video ne
usano gli esiti, come chiede l'addendum 18:
- **S-6r** si presenta;
- **S-6** si presenta solo con la condizione «radar non disturbato»;
- la tabella fisica del rapporto (fumo e luce non degradano il radar; la nube vicina sì) entra nel documento tecnico;
- le fonti F2 ed F3 del rapporto vanno segnate «non verificata».

**Decisioni per l'utente (via coordinatore):** nessuna obbligata. Facoltative:
1. mostrare o no in s5 la riga piccola della regola in prova;
2. in s7, presentare la taratura principale (scelta qui) oppure la variante b, fatta a posteriori.

## 10. Che cosa manca

- Non ricontati da me: `latenza.json`, il bootstrap per mezzo e il contenuto delle fonti (mi affido a FONTI_APERTE).
- F3 con i sensori a circa 570 m in sda: ancora parziale (7/7).
- F5 ed F6 a 40–150 m: non provati.
- La C del nucleo v4 sui registri: non fatta.
- Attacco F7 non fatto:
  - portatore in manovra;
  - vento;
  - clutter a grappoli;
  - più di 20 passaggi per variante.
