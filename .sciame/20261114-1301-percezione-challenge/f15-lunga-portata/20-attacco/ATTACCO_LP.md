# Attacco alla seconda fase (lunga portata): controesempi eseguiti

`sciame-avversario`, f15/20-attacco, 15-11-2026, 01:22–01:33 (orologio della macchina; la consegna dice 14). Previsioni scritte prima, alle **01:23:44**, in `PREVISIONI.md`. **Tutto è conto o simulazione: niente è provato su un sensore fisico, niente è «validato».** Solo osservazione e avviso.
Programmi (miei, in questa cartella, nucleo e simulatore **non modificati**, importati con `-B`): `attacchi.py` → `attacchi_esito.json` (X1–X6, pochi secondi); `limite.py` → `limite_*.json`, `limite.log` (X7, 6 min in tutto, 8 processi); `perdita.py` → `perdita_esito.txt`; `leggi_limite.py`. Interprete: `f10-dati/ambiente/venv/bin/python -I -B`.

## 0. In testa

- **Cambi di stato.** «L'avviso contiene il mezzo nascosto» resta **smentito** anche dopo la correzione degli aerei di 12-traiettorie: lo rompe un drone che parte da fermo (X1). «Il libero non contiene oggetti di classe ammessa» è **smentito** in modo nuovo, senza Doppler e senza cella vicina: sezione radar correlata fra passate (X4) ed edificio non in pianta (X5). La tabella § 4 di MODELLI_E_REGOLE («aeroporto: operatore di sito 1,49 km: sì») è **smentita** con l'inviluppo corretto (X3). La separazione taratura/prova di 12-traiettorie **non è per mezzo** su auto e treni (X10).
- **Regole.** Non ne ho violate, che io sappia. Nessun file cancellato o sovrascritto, niente rete salvo 4 pagine lette (§ 2, X8), niente git. Segnalo, non correggo: 02-sensori § 1 dichiara di aver **cancellato** due file scaricati per errore. Se è avvenuto dopo il divieto del coordinatore, è una violazione.
- **Ingressi E1–E5.** I file 40-eventi ci sono. Non ho attaccato gli eventi con prove nuove (tempo): **non coperti da me**. Restano le smentite di 11-prove § 4 (E1 e E2).

## 1. Attacchi, previsione ed esito

| # | Caso (previsione in PREVISIONI.md) | Esito ottenuto | Stato |
|---|---|---|---|
| X1 | Multirotore **in volo stazionario** (v 0, σ_v 0,3) che scatta a 20–25 m/s² fino a 45 m/s (drone da corsa: **ipotesi**, senza fonte aperta oggi), scenario `aeroporto_e_droni` | **fuori dall'insieme** a τ = 3 s (94,5 m contro 89,8 m di raggio), 5 s (184 contro 147) e 8 s (320 contro 284); dentro da 10 s in poi. Causa: v0 = \|v\| + 3σ_v ≈ 1 m/s e a_max dell'inviluppo = 6,9 m/s² (il massimo fra le classi) | attacco **riuscito** |
| X2 | Aereo in decollo a 160 e 205 m/s, inviluppo attuale 90 m/s | fuori **a ogni τ da 1 a 30 s** (a 10 s: 2050 m contro 972 m). Riproduce K4 di 12-traiettorie su un caso costruito | riuscito (già noto) |
| X3 | d_avv con v_max aereo 210 m/s (kalman-1) | operatore di sito **3410 m** contro **2360 m** di portata del «libero» per il multirotore (radar segnaposto, 5 passate): **non tempestivo**. Pilota in rullaggio 1956 m e pilota remoto 1570 m: ancora sì. Con v_max 210 e celle da 100 m, W_aereo = 0,48 s < 1 s di giro: la cella cumula al più una passata | riuscito |
| X4 | Sezione radar **correlata** fra le passate (aspetto fisso, bersaglio che resta in volo stazionario): Swerling 1 dentro la passata, valore tenuto per 5 passate. Monte Carlo 400 000, `ncx2` di scipy | alla portata del «libero» (2360 m, SNR medio 26,2): P(5 passate tutte mancate) = **0,263** contro **0,010** dichiarato (26 volte); con 3 passate 0,299 contro 0,063. Controllo: la Pd media Monte Carlo 0,6024 coincide con la formula 0,6019 | riuscito: il «libero» al 99 % vale solo con passate indipendenti |
| X5 | Edificio **non in pianta**, mezzo dietro a 600 m, 5 passate senza ritorno | cella **«libera»** (con l'edificio in pianta: «in ombra»). Anche un'auto da 10 m² dietro un edificio ignoto, scenario `strada`, a 800 m: «libera» | riuscito, per costruzione: il «non osservato» dipende dalla mappa |
| X6 | Classe **non ammessa** dallo scenario | `strada` (solo auto, 10 m²): 16 920 celle su 39 240 «libere» hanno Pd cumulata < 0,99 per un pedone da 0,5 m² (oltre 6,25 km, minimo 0,13) e 35 280 per un drone da 0,01 m² (già da **850 m**). `aeroporto`: 2160 su 2880 celle libere non verificate per un drone C0 da 1,6·10⁻⁴ m², da **250 m** | riuscito: «libero» vuol dire «libero per le classi ammesse» |
| X7a | Simulatore al limite, A1 prudente, N = 30 per configurazione, **semi appaiati**: IRIS a 5 falsi ritorni per giro (uccelli, terreno: **ipotesi**), pannello 0,5, sezione vera del drone 0,005 m² contro 0,01 della classe | A1 min fuori avviso **8/797 = 0,010 [0,005; 0,020] → 25/797 = 0,031 [0,021; 0,046]** (× 3,1). Falsi avvisi 4,2 → **217 per ora** (min) e 113 → **2109 per ora** (alta). «Libero» sull'oggetto in A1 alta: 119/2964 = 0,040 [0,034; 0,048] nominale, 126/2964 [0,036; 0,050] al limite; C0 61/456 = 0,13 [0,11; 0,17] | previsione (≥ × 2) **regge** |
| X7b | S1 prudente, N = 30, radar 4D a 1 falso per quadro (il valore del JSON di 02-sensori, non 0,3) | fuori avviso min **100/1697 = 0,059 [0,049; 0,071] → 152/1697 = 0,090 [0,077; 0,104]** (× 1,52); alta 55/1152 → 91/1152 (× 1,65). Falsi avvisi 717 → **2828 per ora** (min), 2160 → **6846** (alta). «Libero» sull'auto 20/1170 → 21/1170 | **non risolta** (fra 1,5 e 2) |
| X10 | Taratura e prova di 12-traiettorie separate per mezzo? (domanda della consegna, senza previsione numerica scritta: **notato dopo**) | La divisione è per **cartella**, e un mezzo è tagliato in più cartelle (`ngsim_us101_v10_0`, `_1`, `_2`). Mezzi con pezzi **in entrambe le metà**: auto **37/59** [0,50; 0,74], treni **29/37** [0,63; 0,89], droni 7/227, aerei 2/189 | la «prova» su auto e treni **non è tenuta da parte** |

**Indipendenza.** X1–X6 condividono con il nucleo il codice (`movi_lp.py`), il radar segnaposto e le classi. Sono controesempi **al modello**, non misure di un sensore. X7 condivide tutto il simulatore e cambia solo tre parametri. Il campione è piccolo (N = 30) e le righe al limite non sono indipendenti da quelle nominali: i semi sono appaiati, ed è voluto.

## 2. Otto valori di scheda riaperti (X8; previsione: almeno uno non coincide)

| Valore nel file | Fonte | Riaperta | Esito |
|---|---|---|---|
| AT128: 210 m al 10 %, 120° × 25,4°, 0,1° × 0,2° | [hesaitech.com/product/at128](https://www.hesaitech.com/product/at128/) | oggi, 01:2x | coincide. La frequenza di 10 Hz non è nella pagina: resta «ipotesi», come dice il JSON |
| Tele-15: 320 m al 10 %, 500 m al 50 %, 14,5° × 16,2°, < 0,03°, falsi < 0,01 % | [livoxtech.com/tele-15/specs](https://www.livoxtech.com/tele-15/specs) | oggi | coincide. 2 cm vale a 20 m (nota 1), e i falsi sono a 100 klx |
| ADS-B: NACp < 0,05 NM, NIC < 0,2 NM, latenza ≤ 2 s, ≥ 1 al s in volo, ogni 5 s da fermo | [14 CFR 91.227](https://www.law.cornell.edu/cfr/text/14/91.227) | oggi | coincide |
| Remote ID: 100 ft al 95 %, quota 150 ft, ≤ 1 s, ≥ 1 al s | [14 CFR 89.310](https://www.law.cornell.edu/cfr/text/14/89.310) | oggi | coincide |
| IRIS: C1 0,9 kg a 3100 m; C0 0,249 kg a 1100 m | copia locale della scheda (`02-sensori/scaricati`, letta con `pdftotext`) | oggi (copia scaricata ieri sera) | coincide. La scheda dice: «indicative … under typical sight, clutter and weather conditions». **Nessuna Pd e nessuna sezione radar**: la Pd 0,5 è un'ipotesi |
| IRIS: errore in distanza 0,6 m; angolo 0,6–0,75°; elevazione 1° | idem | oggi | coincide |
| **IRIS: rivisita 1 s** | idem | oggi | **non coincide alla lettera.** La scheda dice «Rotation / Scan Speed 30 rpm / 1s» e «Back-to-back radars allow for 1 second update». Ora, 30 giri al minuto fanno **2 s per giro**: il secondo sembra richiedere due antenne contrapposte. Da chiarire; se vale 2 s, cambiano W, le passate e la tabella dell'avviso |
| SCANTER 5000: 60 giri al minuto (1 s); radar d'aeroporto ciechi sotto 200–300 m, aggiornamento 4 s | copia locale Terma | oggi | coincide |

**Esito: 7 su 8 coincidono e 1 è dubbio.** La previsione regge, al limite. Le pagine web sono state lette con uno strumento che le riassume: le citazioni non sono ricontrollate sul testo grezzo.

## 3. Le frasi (X9; previsione: almeno una occorrenza nei documenti)

`grep` su `proposta/proposta_sciame.tex`, `allegato_tecnico/capitoli/*.tex` e i `.md` della fase: **0 occorrenze** del lessico d'ingaggio fuori dalle liste «da evitare». Nessuna portata in km nei documenti per la giuria, che oggi non parlano ancora di lunga portata. La previsione è **smentita**. I rischi sono nei materiali di lavoro, che non vanno ripresi tali e quali.

- **Non si può dire:**
  - «rileva i droni a 3 km», «a 7,6 km», «la camera vede un drone a 13 km». Le portate IRIS non hanno né Pd né sezione radar, e valgono «in condizioni tipiche»; i 13 km sono un limite geometrico.
  - «non dichiara mai libero ciò che non ha osservato», senza aggiungere «per le classi ammesse, con la mappa degli ostacoli data e con passate indipendenti» (X4–X6).
  - «l'avviso contiene sempre il mezzo» (X1, X2).
  - «avviso tempestivo per aerei e droni» (X3; A3 0/200).
  - «validato», «in tempo reale», «certificabile», «detect and avoid».
- **Da non citare per nome davanti alla giuria:** la fonte ROBINBLOG («counter-drone technologies to detect and stop drones»), il lessico della scheda IRIS («drone threat»), i nomi «Shahed».
- **La frase che regge:** «In simulazione, con sensori presi dalle schede, MoVi mantiene l'avviso di possibile presenza finché non torna a guardare, e dichiara dove e per quale classe di mezzi non può dire "libero".»

## 4. Correzioni obbligate

1. **Inviluppo.**
   - v_max degli aerei ≥ 210 m/s (kalman-1).
   - a_max dei multirotori sopra 6,9 m/s², oppure una classe «drone veloce». È un'ipotesi da 20–25 m/s², da sostituire con una fonte. Lo chiede X1.
   - Poi va rifatta la tabella § 4: l'**operatore di sito d'aeroporto non è tempestivo** con il radar segnaposto, e l'uscita lo deve dire.
2. **Passate correlate.** Il «libero» al 99 % non può contare 5 passate come indipendenti per un bersaglio che non cambia aspetto. Due correzioni possibili:
   - n effettivo = 1 entro un tempo di decorrelazione dichiarato (ipotesi). La portata del «libero» del multirotore scende da 2,36 km a **0,88 km**;
   - oppure una fonte che misuri la decorrelazione della sezione radar dei multirotori.
3. **Mappa.** La mappa degli ostacoli è un ingresso di sicurezza.
   - Le celle dietro un ritorno statico forte vanno trattate «in ombra»: serve una mappa del disturbo statico (clutter).
   - I documenti devono dire che un ostacolo ignoto apre un «libero» falso (X5).
4. **Classi.**
   - L'uscita dice «libero per ⟨classi⟩».
   - `strada` deve ammettere pedoni e due ruote, oppure dichiararne l'esclusione.
   - `aeroporto` dichiara che il drone C0 è fuori dal «libero» (X6).
5. **Restano obbligate** validazione-1, 2 e 3 di 11-prove. Anche nel modo prudente S1 perde il mezzo fuori avviso nel 5,9 % dei cicli, e il 9,0 % con i falsi del JSON (X7b).
6. **Falsi avvisi.** Con uccelli e terreno anche il solo IRIS dà 217 avvisi falsi all'ora (X7a). Servono un modello di disturbo strutturato e un valore misurato prima di dire qualunque cosa sui falsi allarmi. Il radar d'aeroporto filtra i bersagli lenti (MTI)? Non è modellato: **non verificato**.
7. **12-traiettorie.**
   - Rifare la divisione **per mezzo**, cioè sul nome della cartella senza `_N`, almeno per auto e treni.
   - Le occlusioni virtuali cadono a caso nel tempo, mentre quelle vere cadono vicino agli ostacoli, dove si vira e si frena. In virata la copertura è già 0,71–0,74: le occlusioni virtuali sono più facili delle vere, e la copertura marginale di 0,90 non va detta per le ombre vere.
8. **Rivisita IRIS.** Chiarire se è 1 s o 2 s (§ 2).

## 5. Forma più forte che resta vera, per classe (sempre in simulazione o su moto pubblico con rumore di scheda)

- **Multirotore piccolo (0,01 m²) e radar per droni.**
  - «Libero» per questa classe solo entro **0,88 km** se le passate sono correlate (2,36 km se indipendenti: ipotesi).
  - Avviso tempestivo per un operatore di sito, se il drone non supera 19 m/s e 6,9 m/s².
  - Un drone che scatta da fermo esce dall'avviso a 3–8 s.
- **Drone C0 (< 250 g).** Con il radar segnaposto, il «libero» delle classi ammesse non verifica il C0 già da circa 250 m (X6). Oltre quella distanza va detto «zona non verificata per droni sotto 250 g».
- **Aerei.**
  - Zona dichiarata in almeno 8 casi su 10 fino a 30 s (12-traiettorie, su divisione per mezzo quasi pulita: 2/189).
  - Avviso: **nessuna frase** finché v_max non è corretto.
  - Tempestività per l'operatore di sito: **no** con i valori attuali.
- **Auto e treni.** Copertura della zona: **non risolta**, per la divisione non per mezzo. L'avviso sul treno avvisa, non ferma (02-sensori).

## 6. Che cosa resta aperto

- E1–E5 non attaccati da me.
- La fonte della sezione radar e della sua decorrelazione per i multirotori.
- L'a_max dei droni veloci.
- L'MTI del radar d'aeroporto.
- La rivisita IRIS.
- Il rifacimento di X7 con N ≥ 200 e il rifacimento di 12-traiettorie per mezzo.
- Nessun sensore fisico, in nessuna di queste prove.
