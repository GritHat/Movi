# Verdetto della fase 3: volo ad alta velocità con eventi (f19-volo/30-verdetto, `sciame-arbitro`)

15-11-2026, dalle 05:30:44 (`date -Is`). Previsioni V1–V5 scritte **prima** del riconto, alle 05:31:06, in
`PREVISIONI.md`. Riconto con codice mio:
- `riconta_verdetto.py` → `riconto_esito.json`: record per passaggio v3i, v3b e v4, E1 di f15/2c, casi reali per fascia;
- `riconta_manovra.py` → `riconto_manovra.json`: casi reali per tipo di moto.

**Tutto è simulato dalle schede, calcolato, o su traiettorie pubbliche con un sensore simulato.** Nessun sensore
fisico, nessuna prova su hardware, niente è «validato». Le etichette sono messe a mano. Solo osservazione,
monitoraggio e avviso.
**Indipendenza.** Condivido con gli autori i record, i simulatori, le definizioni dei campi e il modello
linguistico. Ricontrollo l'aggregazione, non la fisica né la misura.
Wilson al 95 % è **per passaggio**. Dove scrivo «casi», i casi sono correlati dentro un mezzo e l'intervallo è
ottimista.

## 1. In testa: previsioni, regole, cambi di stato

**Previsioni: reggono tutte e cinque.**
- **V1.** In v3i:
  - F3, evento entro 2 s: 0/60 in att e in sda;
  - F4, evento entro 1 s: 60/60 in tutte e due;
  - F6, falsi eventi: 0/200 per configurazione;
  - «libero» sul punto vero: 0 passaggi in tutte le 12 celle.
- **V2.** I Wilson coincidono entro 0,001.
- **V3.** Continuità: F1/att 39/60, F6/att 186/200.
- **V4.** Margine minimo dell'operatore in F4: 0,25 s in att, 0,45 s in sda.
- **V5.** Aerei reali, IMM, 1–2 s: 518/733 = 0,707.

**Regole.** Ho scritto solo in `30-verdetto/`. Niente cancellazioni, niente git, niente sudo, niente rete. Un
processo alla volta, con `timeout`.
**Non ricontato da me:**
- `latenza.json` (le latenze sono riportate dal file);
- il bootstrap a grappoli di 21-statistica;
- `prove_confidenza.json` (i raggi r_0,9).

**Fatti nuovi (F#).**
- **F-701.** L'insieme di presenza del nucleo v3 usava l'inviluppo delle classi (90 m/s), non i 210 m/s. Correzione
  v3i, con `movi_lp_v3.py` intatto: F4/att da 13/60 a 60/60 senza buchi; F6/att da 126/200 a 186/200.
  - Stato: simulato.
  - Da adottare come nucleo v4, accanto alla v3.
- **F-702.** La collisione **veloce** fra droni (F3, 40 e 35 m/s) **non è dichiarata come evento**: 0/60 [0; 0,060]
  in att e in sda. I ritorni dei frammenti (RCS 2·10⁻⁴ m²) non arrivano.
  - Il 51/60 di E1 (multirotori a 8 m/s) **non si trasferisce** al volo veloce.
- **F-703.** La regola v4 «impulso» dà F3 59/60 [0,911; 0,997], ma anche falsi eventi in F6, 198/200 in att e
  158/200 in sda, con l'evento aperto prima dell'urto. **Respinta.**

**Contraddizioni (K#), con la risoluzione.**

| K# | Fra | Esito |
|---|---|---|
| K-701 | RIVALUTAZIONE EV-7 «nessuno scenario in volo» ↔ 10-prove | superata: F3 è LIMITE (dimostrato dal simulato), F4 è INCORAGGIANTE |
| K-702 | 10-prove: F4 «evento entro 1 s» SOLIDO ↔ attacco | **INCORAGGIANTE con innesco ottimista**: la saturazione è presa dal punto vero |
| K-703 | F4 «avaria non contenuta» ↔ attacco V3 (dischi a 250 m/s: 0/10 [0; 0,278] passaggi dentro V) | F4 si rinomina **«avaria con detriti a bassa energia»**; l'avaria non contenuta è NON PROVATA |
| K-704 | 10-prove: «fasce alte vicine all'osservato» ↔ 21-statistica | **smentita in att**: F6 con C ≥ 0,9 osservata 1/78 campioni, F1 con C 0,99–1 osservata 15/45; vale solo in sda e in F2/F5 att |
| K-705 | SCENARI «P6 regge» (p_scambio 0,21–0,29) ↔ simulato | **smentita**: 28/60 = 0,47 [0,35; 0,59] e 38/60 = 0,63 [0,51; 0,74]; si toglie la «confidenza d'identità 0,79–0,71» |
| K-706 | SENSORI «umano senza ausilio» 3812 e 1237 m ↔ attacco | doppio conto di 2,0 s; ricalcolato da me: **3312 m** (aereo a 250 m/s), **1058 m** (drone a 90 m/s) |
| K-707 | SENSORI «calcolo dedicato sotto il millisecondo» ↔ i suoi numeri | il calcolo dedicato è **0,08–1,2 ms** (ipotesi); «sotto 1 ms» è falso |
| K-708 | 10-prove: «sda più rapido» ↔ attacco | in sda cambiano insieme il sensore (1 → 10 Hz) e il calcolo: il guadagno da 0,3 a 0,1 s **non è attribuibile all'hardware** |
| K-709 | Eulero instabile nei frammenti (04-scenari) ↔ E1 di f15 | **non risolto**. Il frammento più lontano di E1 passa da 130 a 154 m; non è verificato se sposti il 51/60. Prova che lo decide: rifare E1 con `frammenti_volo` (versione nuova accanto) |

**Cambi di classe.**
- LP-7 («circa 9 su 10» sugli aerei) resta INCORAGGIANTE solo con «v_max 90 m/s, non rimisurato a 210».
- LP-8 è «un esemplare».
- La C(τ) del nucleo in att diventa LIMITE e non si mostra.

## 2. Tavola finale dei risultati presentabili

Riga fissa per tutte: «simulazione da schede · etichette a mano · nessun sensore fisico».
Classi:
- **S** = solido: limite inferiore ≥ 0,90, oppure 0 su N con limite superiore ≤ 0,06;
- **I** = incoraggiante: stima ≥ 0,80, limite inferiore ≥ 0,70, base matematica;
- **L** = limite;
- **NP** = non provato.

Stati: sim = simulato, calc = calcolato, pub = su dati pubblici con sensore simulato, ip = ipotesi, dim = dimostrato.

### 2.1 Volo ad alta velocità con eventi (caso centrale; `10-prove/passaggi_volo_v3i.jsonl`)

Ogni scenario è una sola geometria nominale: i passaggi variano solo semi e rumore.

| # | Frase per la giuria | Classe | Intervallo · stato | Base matematica |
|---|---|---|---|---|
| V-1 | «Nei sei scenari di volo, dall'avaria in volo alla collisione di droni, MoVi non ha mai detto "libero" dove c'era l'oggetto o un frammento.» | S | 0/200 [0; 0,019] in F6; 0/60 [0; 0,060] nelle altre 11 celle · sim | per costruzione: si dichiara libero solo ciò che si osserva (CR-1), con l'insieme di presenza a 210 m/s |
| V-2 | «Avaria in volo di un aereo a 135 m/s con fiammata: evento dedotto in 0,1–0,4 s, camere dichiarate non affidabili entro 3 cicli, in 60 passaggi su 60.» | I (innesco ottimista) | 60/60 [0,940; 1], sia att sia sda · sim | separazione di tracce e salute del sensore; la saturazione è presa dal punto vero |
| V-3 | «Dopo l'avaria, i detriti a bassa energia restano nel volume dichiarato: in 58 passaggi su 60 tutti, e in quelli peggiori il 96 % (att) e il 74 % (sda).» | I | 58/60 [0,886; 0,991] · sim | volume balistico V(τ) con dv ≤ 100 m/s; al bordo dei parametri 1000/1000 [0,9962; 1] |
| V-4 | «L'avviso arriva prima del primo frammento a terra: con margine per un sistema di bordo (almeno 5,7 s) e per un operatore (almeno 0,25 s), in 60 su 60.» | I | 60/60 [0,940; 1] · sim, ip (5,4 s di risposta umana) | d = v·(L + t_risp + ritardo del mezzo), da `latenza.json` |
| V-5 | «Due droni veloci in rotta di collisione: avviso di prossimità fra 18 e 20 s prima dell'urto, in 60 passaggi su 60.» | I (soglia di 10 s non scritta prima) | 60/60 [0,940; 1], almeno 10 s · sim | punto di massimo avvicinamento a velocità costante, sotto 150 m |
| V-6 | «Dopo la collisione veloce, il punto vero e i frammenti stanno sempre nella regione dichiarata: 939 campioni su 939.» | S come copertura; NON come evento | 60/60 passaggi [0,940; 1] · sim | inviluppo \|a\| ≤ a_max, v ≤ 210 m/s |
| V-7 | «Quasi collisioni a 40 m e incroci veloci: nessun falso evento.» | S | F6 0/200 [0; 0,019]; F1 e F5 0/60 [0; 0,060] · sim | conferma su più cicli |
| V-8 | «Con un radar a scansione elettronica a 10 Hz, la regione non si perde mai.» | S in sda | 60/60 e 200/200 [0,981; 1] · sim, scheda del sensore non aperta | rivisita più breve della crescita dell'inviluppo |
| V-9 | «Col radar rotante a 1 Hz l'aereo veloce perde continuità, e MoVi lo dichiara.» | L | F1/att 39/60 [0,524; 0,758]; F6/att 186/200 [0,886; 0,958] · sim | — |
| V-10 | «Ottici accecati per 2–4 s: tutte le tracce conservano una regione.» | S (regione); L (identità) | 60/60 [0,940; 1]; scambio 0,47 [0,35; 0,59] e 0,63 [0,51; 0,74] · sim | identità «presunta» |
| V-11 | Collisione **veloce** dichiarata come evento | **L** | 0/60 [0; 0,060] · sim | — |
| V-12 | Avaria non contenuta, con frammenti di disco a 250 m/s | **NP** (V3 0/10 [0; 0,278]) | sim, ip | — |
| V-13 | Collisione fra droni **lenti** (8 e 6,7 m/s): evento in 1,2–2,3 s; entro 2 s in 51 su 60 | I | 51/60 [0,739; 0,919]; entro 2,5 s 60/60 (soglia notata dopo) · sim | fusione e separazione di tracce confermate su più cicli |

### 2.2 Sito con rullaggio (sezione breve; verdetti f15)

| # | Frase | Classe | Intervallo |
|---|---|---|---|
| LP-1 | Drone a 15–21 m/s dietro un edificio annunciato in tempo | S | 200/200 [0,981; 1] ×2; 100/100 [0,963; 1] |
| LP-2 | Mai «libero» sul drone col nucleo v3, con la mappa dichiarata | S | 0/171 [0; 0,022] |
| LP-3 | Il drone che rallenta o si ferma resta nell'avviso | I | 188/200 [0,898; 0,965] |
| LP-4/5 | Rullaggio con tre sensori fusi in tempo; col solo radar no | S / L | 200/200 [0,981; 1] (nucleo v2) / 50/200 [0,195; 0,314] |
| LP-6 | Aerei in volo: l'avviso **al sito** non è tempestivo, e MoVi lo scrive | L, calc | servono 3410 m |
| LP-7 | 43 aerei reali dopo 2–30 s: zona che li contiene | I, pub | circa 0,93–0,95, con v_max 90 m/s; non rimisurato a 210 |
| LP-11 | L'avviso si spegne solo guardando tutta la zona | S | 0/600 [0; 0,006] |

### 2.3 Corto raggio e altri usi (RIVALUTAZIONE § 1, invariata)

| Classe | Risultati |
|---|---|
| S | CR-1 (dimostrazione condizionata); CR-3: 0/23 402 [0; 0,0002]; CR-6: 0/4324 [0; 0,001] |
| I | CR-4: ≥ 0,92 a 2 s; CR-8: 176/180 [0,944; 0,991], dominio stretto |
| L | CR-10 |
| NP | CL-1 (classificatore) |

## 3. Perdita di confidenza nel tempo: la forma da mostrare

**Formula, dimostrata nel modello** (moto a velocità quasi costante, rumore gaussiano). Stato: dimostrato e
verificato numericamente (`03-confidenza`): scarto ≤ 7,6·10⁻⁸ dalla quadratura; Monte Carlo 10⁶ con |z| ≤ 2,11.

    σ²(τ) = σ0² + 2σ0v·τ + σv²·τ² + q·τ³/3
    C(τ)  = 1 − exp(−r² / 2σ²(τ))             (disco di raggio r, 2D)
    r_α(τ) = k_α·σ(τ),   k_0,9 = 2,146         (regione che cresce per tenere il livello α)
    t_C: radice positiva di (q/3)t³ + σv²t² + 2σ0v·t + σ0² − (r/k_α)² = 0

Per più regimi: C(τ) = Σ_j μ_j(τ)·P_j. È esatta per la miscela, approssimata per il moto vero.

**Fuori modello, cioè dopo un urto, un'avaria o una manovra non modellata, si mostra l'insieme di presenza.**
- Raggio: r(τ) = r0 + v_max·τ, con v_max di 210 m/s per gli aerei e 45 m/s per i droni.
- Non dà una probabilità: dà un contenimento garantito con |a| ≤ a_max.
- Nel simulato ha contenuto il vero: dopo l'urto 939/939 campioni (F3, sda); dopo l'avaria 1072/1072 (F4, att).

**Verifica su dati reali**, ricontata da me: regione IMM al 90 %, metà di prova divisa per mezzo, casi (Wilson
ottimista).

| τ | 1–2 s | 3–5 s | 6–10 s | 11–20 s | 21–30 s |
|---|---|---|---|---|---|
| aerei, 16 mezzi | 0,71 [0,67; 0,74] **L** | 0,92 [0,89; 0,94] | 0,95 [0,92; 0,97] | 0,98 [0,96; 0,99] | 0,96 [0,94; 0,98] |
| aerei in virata | — | — | 29/37 = 0,78 [0,63; 0,89] **L** | 68/71 = 0,96 | 96/105 = 0,91 [0,85; 0,95] |
| aerei in accelerazione | 2/6 **L** | 14/17 | 15/18 | 22/25 | 35/38 |
| droni ad ala fissa (un velivolo?) | 0,91 [0,88; 0,93] | 0,92 | 0,96 | 1,00 | 1,00 |
| multirotori (un esemplare?) | 0,95 [0,94; 0,96] | 0,99 | 1,00 | 1,00 | 1,00 |

**Frase da mostrare.** «Quando un aereo veloce non è più visto, la regione che lo contiene nove volte su dieci
cresce con il tempo. Su 16 aerei reali la regione l'ha contenuto da 92 a 98 volte su 100 fra 3 e 30 s.»
- Etichetta: «calcolata nel modello; verificata su traiettorie ADS-B con un sensore simulato».
- Accanto vanno i limiti: 0,71 a 1–2 s (la verità ADS-B è sospetta, non risolto) e 0,78 in virata a 6–10 s.
- Oltre i 10 s l'IMM è prudente: la regione è più larga del necessario.

**Da non mostrare:**
- la C del nucleo in att (F6: 1/78);
- la zona «al 99 %» della sola covarianza (0,003–0,91);
- la C numerica dei registri F2, F3 ed F5 finché non è monotona (76 violazioni).

## 4. Da proposta a sistema attuato

Tutte le latenze sono **stime** prese da `02-sensori-hw/latenza.json` (non ricontato da me). Nessuna è misurata.

| Limite | Miglioria (che cosa e come) | Prova che la decide (soglia) |
|---|---|---|
| F3: collisione veloce non dichiarata (0/60) | regola di contatto su tracce **risolte e non doppioni** (velocità relativa > 10 m/s per ≥ 3 aggiornamenti), più un cambio di velocità sostenuto misurato col Doppler; radar a scansione elettronica più vicino ai frammenti | F3 entro 2 s ≥ 0,85 **con** F6 0/200; smentita da un falso evento in F6 o da F3 < 0,75 |
| C(τ) ottimista a 1–2 s e in manovra | σ_rif² nella σ²; regime di accelerazione longitudinale nell'IMM; ricalibrazione isotonica per tipo di moto | 1–2 s in [0,85; 0,95]; accelerazione ≥ 0,85; scarto < 0,05 (smentita > 0,10) |
| C del nucleo in att mal tarata | covarianza gonfiata dal fattore tarato (q×4); C sulla miscela a pesi fissati durante la perdita (monotona) | F1/F6 att con C ≥ 0,9: osservata ≥ 0,80 per passaggio; 0 violazioni di monotonia |
| Avaria non contenuta (V3 0/10) | profilo con dv ≥ 300 m/s; impronta ≥ 10 km; Doppler sui frammenti per restringerla | 60/60 passaggi dentro V |
| Innesco della fiammata ottimista | saturazione rilevata dal segnale della camera, non dal punto vero | ritardo ≤ 1 s in ≥ 0,9 su registrazioni vere |
| Identità dopo la cecità (0,47–0,63) | attributi per riassociare (Doppler, RCS, firma termica); identità «presunta» senza cifra | scambio ≤ 0,2 |
| Continuità col radar rotante 1 Hz | radar a scansione elettronica 10 Hz (classe EchoShield, scheda **non aperta**); AESA a 40 Hz (ipotesi, nessun esemplare con scheda) | già simulato in sda: 60/60; manca la misura sul sensore |
| Una geometria per scenario; nessun clutter | geometrie variate; registrazioni con uccelli e clutter; inviluppo per classe (FPV oltre 45 m/s) | stesse soglie su ≥ 10 geometrie |
| Tempestività verso l'umano | avviso con la direzione: 5,4 s invece di 12,5 s (AC 90-48D, fonte **non aperta**); distanza minima per un aereo a 250 m/s: 2005 m, invece di 3312 m senza ausilio | prova con operatori |
| Latenza del calcolo | codice compilato: guadagno di circa 80 ms, **non** dovuto all'FPGA. FPGA o ASIC dedicato per segnale e CFAR: elaborazione stimata 0,05–0,5 ms invece di 5–20, calcolo dedicato totale 0,08–1,2 ms. **Ipotesi**, per analogia con i chip per modelli linguistici (Taalas HC1 circa 74× su una H200, dato del produttore; Cerebras 8,4×), che vale solo per i carichi limitati dalla memoria; per il passo di Kalman il CERN dà l'FPGA più lento della CPU. L'ASIC «analogo all'HC1» è un'ipotesi di progetto, non esiste | misura su FPGA reale: massimo per aggiornamento ≤ 1,2 ms |
| Primo avviso verso una macchina | la leva è la **rivisita**: dedicato a 10 Hz 0,62 s → a 40 Hz 0,17 s (calcolato da ipotesi); l'hardware accorcia di circa 80 ms | misura end-to-end sul sensore |
| Mappa, classificatore, sensore fisico | mappa verificata col LiDAR; classificatore per classe; prove sul campo | tutte |

## 5. Frasi da non dire (solo quelle false)

- «MoVi rileva la collisione in volo» o «la collisione dei droni veloci entro 2 s»: F3 dà 0/60. Il 51/60 è dei
  multirotori a 8 m/s.
- «Detriti sempre nel volume» per un'avaria non contenuta (0/10), e «avaria non contenuta» come nome di F4.
- «Confidenza 99 %» o «zona al 99 %»; «la confidenza è tarata» (PIT rifiutato; F6/att 1/78).
- «Identità confidente al 79 %» (osservata 0,37–0,63).
- «Il calcolo dedicato porta l'avviso sotto il millisecondo», «in tempo reale», «l'hardware dedicato riduce il
  ritardo dell'evento di N volte», «sda più rapido grazie all'FPGA».
- «Umano senza ausilio: 3812 m» (è 3312) o «1237 m» (è 1058).
- «Validato», «testato su sensori» o su hardware, «certificabile», «detect and avoid», il lessico d'ingaggio.
- «Avviso tempestivo al sito per gli aerei in volo» (LP-6).
- «Mai "libero" ciò che non ha osservato» per la lunga portata senza «con la mappa dichiarata».
- «Sempre», o «entro 2 s» senza «in 51 su 60».

## 6. Scene del video (`prototipo/uscite/video_volo/INDICE.md`, configurazione sda, passaggio 0)

| Registro | Etichetta | Condizione |
|---|---|---|
| F1: aereo in avvicinamento, drone non cooperante, quasi collisione a 41 m | **Simulation** | «avviso di prossimità 33 s prima»; nessun evento; niente C numerica |
| F2: salita in una cella di pioggia | **Simulation** | portata ridotta dichiarata; regione che cresce; niente C (violazioni di monotonia) |
| F3: collisione fra droni a 40 e 35 m/s | **Simulation** | mostrare **solo** ciò che il registro contiene: avviso di prossimità circa 16 s prima, tracce perse, regioni che crescono, tracce nuove non associate. **Niente** «evento: collisione» e niente volume dei detriti come uscita del sistema (il registro non ha l'evento). Testo: «collisione non ancora riconosciuta come evento: regione mantenuta» |
| F4: avaria di un aereo a 135 m/s | **Simulation** | nome «avaria con detriti a bassa energia»; evento a 0,2 s; camere dichiarate non affidabili; impronta di 6,8 km |
| F5: ottici ciechi per 3 s | **Simulation** | «solo radar»; identità «presunta»; niente C |
| F6: controllo, nessun evento | **Simulation** | «nessun falso evento» |
| Curva C(τ) e r_0,9(τ) sugli aerei reali | **Schematic** (grafico) | «calcolata nel modello, verificata su ADS-B con un sensore simulato» |
| Collisione con detriti riconosciuta come evento in volo veloce | **Schematic** | «obiettivo: non ancora simulato con successo» |
| Catena dedicata e latenze | **Schematic** | «stime per analogia, nessuna misura» |

Riga in sovrimpressione per tutte le scene Simulation: «Simulated · state-of-the-art sensor parameters assumed ·
no physical sensor». Questo è un controllo da fare: il validatore `convalida_volo.py` registra F1, F4 ed F6 senza
violazioni.

## 7. Che cosa cambia

**Documento tecnico** (capitolo nuovo sul volo veloce, accanto a `10_lunga_portata.tex`):
- la tavola § 2.1 con le classi e le frasi «in N su M»;
- la formula § 3 e la tabella di verifica, con i limiti a 1–2 s e in manovra;
- la tabella § 4 per intero, come «da proposta a sistema attuato»;
- K-701…K-709, con la v4 respinta come controesempio e F-701 (inviluppo a 210 m/s nel nucleo);
- la sezione sui sensori e sull'hardware, con le correzioni K-706, K-707 e K-708 e le fonti «non aperta» segnate,
  oppure aperte prima di citarle;
- il rullaggio come sezione breve § 2.2.

**Proposta:**
- caso centrale: volo veloce con «mai libero» (V-1), l'avaria (V-2…V-4) e la regione che cresce (§ 3);
- la collisione veloce come miglioria dichiarata con la sua soglia;
- il rullaggio e il corto raggio come altri usi.

**Video:**
- le etichette del § 6;
- le cifre solo dalla tavola § 2, con intervallo;
- niente cifre sotto un limite inferiore di 0,70, salvo come limite dichiarato.

**Decisioni per l'utente (via coordinatore).**
1. Accettare un caso centrale in cui la collisione veloce **non** è ancora riconosciuta come evento. In alternativa,
   provare prima la regola di contatto (§ 4, riga 1), che costa circa 30 minuti di simulazione.
2. Adottare v3i come nucleo v4.
3. Rifare E1 con l'integratore stabile (K-709).
