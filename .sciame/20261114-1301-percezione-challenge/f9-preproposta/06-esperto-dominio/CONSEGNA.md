# Consegna — `sciame-esperto-dominio`, f9: S6, S7, S8 (preproposta §3)

**Campo in cui parlo:** sicurezza del volo e degli aeroporti (anticollisione di bordo, luci di stato della pista, radar per volatili) e sicurezza delle macchine (sorveglianza di velocità e separazione). Non sostituisce un professionista della certificazione; prove del 14-11-2026.

## 1. Scostamenti e regole violate

- **Previsione smentita (esp9-P1):** avevo scritto che «ABAR» non esiste; esiste come sigla di un costruttore (critica 1). **Mancata (esp9-P6, seconda metà):** 1,68 m contro «< 1,5 m». Le altre otto reggono (`PREVISIONI.md`).
- **Regola 5:** lo strumento di lettura ha salvato da solo due PDF fuori dalla mia cartella; li ho solo convertiti in testo nella cartella temporanea.
- **Indipendenza:** le prove usano codice mio sui numeri del nucleo: valgono per errori di conto, non per il sensore vero. Le pagine web le riassume un modello ausiliario; i due PDF (F1, F3) li ho letti come testo, e le loro citazioni sono dirette. Sigle: [A] aperta; [R] solo trovata dal motore di ricerca; NV non verificato.

## 2. Verdetti proposti

| Strategia | Verdetto proposto | Prova |
|---|---|---|
| **S6** massimo avvicinamento e volume protetto probabilistico | **approvata con correzioni**: le formule sì, la probabilità d'intrusione **non** come criterio di «nominale»; soglie **da provare sull'hardware** | su rotta di collisione esatta la probabilità a 2 s è 0,16–0,18, e **cala** se il dato peggiora (0,12 con rumore di 0,20 m) |
| **S7** indice di rotta convergente | **respinta come indice a sé**; resta un'etichetta derivata da S6 | è la stessa grandezza di S6 (scarto 3,0e-16 su 10 000 stati); controesempio: oggetto dritto su un varco a 1 m di lato dal sensore, 6,9–21,2 °/s visti dal sensore |
| **S8** logica a livelli | **approvata con correzioni**: nomi, avaria separata, corridoio ridefinito | alla lettera l'attesa è permanente (73,2 % del corridoio 0–3 m non è osservabile) o intermittente (44,8 ingressi al minuto a scena vuota) |

Per rifare: `cd prove && timeout 120 python3 p7_corridoio.py`; `timeout 120 python3 p8_p9_p10.py` (semi 20261114); uscite in `prove/risultati_*.txt`.

## 3. Critiche numerate

**1. «Sistemi aeroportuali ABAR/ACAS».** «ABAR» è la sigla di un solo costruttore: «MERLIN Aircraft-Birdstrike Avoidance Radar (ABAR)» di DeTect [A, F1]. Quel radar dà un **rischio per zona** in tre colori («Green = LOW, Yellow = MODERATE, Red = SEVERE») a controllori, gestori e addetti alla fauna, calcolato da «location, size, mass & number»: nessun massimo avvicinamento, nessun TA o RA, e usa la massa, che la preproposta esclude. La FAA parla di «avian radar», a supporto della gestione della fauna [A secondaria, F2]. L'ACAS non è aeroportuale ma di bordo: «ACAS Xu does not support operations on the ground» [A, F3 §13.6]. Il titolo «Anti-Bird Strike» promette ciò che una camera a 3 m non fa: va tolto.

**2. TA e RA sono due atti diversi, non due gradi.** Guida ACAS di EUROCONTROL [A, F3]: il TA serve «to aid visual acquisition … No manoeuvres are permitted in response to a TA» (§6.1); con un RA «pilots shall respond immediately … following the RA» (§9.2.1), «even if the RAs are contrary to ATC clearances», e i due velivoli coordinano le manovre. Un RA è una **manovra prescritta ed eseguita subito**: il prototipo dichiara e chiede, quindi «RA» promette ciò che non fa. In più ACAS «does not detect non-transponder equipped aircraft» (§2.7); il prototipo misura senza cooperazione.

**3. Le scale non si trasferiscono.** TCAS II: entro 14 NM, fino a 1200 kt, TA a 20–48 s e RA a 15–35 s dal massimo avvicinamento, volume protetto di 0,20–1,10 NM e 600–800 ft [A, F3 §8.6.2, tab. 16]. Prototipo: 3 m, 2,5 m/s, orizzonte utile circa 1,2 s. Rapporti: circa 8600 in distanza, 250 in velocità, 12–29 in tempo. Passa il principio (il tempo al massimo avvicinamento), non le soglie.

**4. «RA / FAIL-SAFE» fonde ciò che la traccia chiede distinto.** L'avaria è l'assenza di giudizio, non il pericolo più alto; nel TCAS ha annunci propri («TCAS/ACAS has failed», §5.7). «Fail-safe» vale per chi comanda uno stato sicuro: il prototipo non comanda.

**5. La probabilità d'intrusione soffre di diluizione.** Con q = 0,2 m²/s³ (nucleo, B4) l'incertezza prevista è 0,34 / 0,58 / 0,85 m a 1 / 1,5 / 2 s; su rotta di collisione **esatta** contro un volume di raggio 0,5 m la probabilità è 0,65 / 0,31 / 0,16 e supera 0,5 solo sotto 1,19 s. Con un dato più rumoroso **scende** (a 1 s da 0,75 a 0,45): «P circa 0, quindi nominale» premia il dato peggiore, contro «l'incerto non è libero». È noto nelle congiunzioni fra satelliti: «lower quality data paradoxically appear to reduce the risk of collision»; gli ellissoidi d'incertezza ne sono immuni [A, F4]. Il TCAS stesso non usa probabilità: «assumes the worst-case scenario (i.e., the aircraft are on a collision course)» (§11.2.2).

**6. S7 è S6 riscritta, e riferita al punto sbagliato.** Velocità angolare del rilevamento = d·|v|/r², con d la distanza della retta di moto dall'osservatore. Una soglia fissa (5 °/s a 1,2 m/s) vale un raggio protetto di 0,65 m a 3 m e di 0,16 m a 1,5 m: si stringe mentre l'oggetto si avvicina. Il rilevamento va preso dal **punto protetto**, che coincide con il sensore solo se il sensore è sul corpo da proteggere (veicolo, persona), non nella stazione fissa. La regola viene dal mare (COLREG 7(d)(i): rischio «if the compass bearing of an approaching vessel does not appreciably change») e avverte essa stessa che il rischio può esistere «even when an appreciable bearing change is evident … at close range» [A, F5]: a 3 m «rilevamento che cambia, bassa criticità» non vale. «On-Boresight» e «indice di minaccia» sono lessico di puntamento, fuori ambito: si dice «avvicinamento diretto».

**7. La regola d'attesa rimette un difetto già corretto.** La correzione C3 del nucleo aveva tolto il «non osservato sempre primo», che faceva dire «mobile in avvicinamento» nello 0 % dei casi (`SOLUZIONE_V2.md` §4). Con «una cella non osservata, quindi attesa»: un corridoio dal sensore a 3 m è sempre in attesa; uno largo 2 m fra 1,3 e 2,9 m lo è per 2 celle d'angolo oltre portata; uno tutto osservabile (1,3–2,9 m, largo 1 m, 454 celle) entra in attesa nel 5,72 % dei cicli a scena vuota con suolo valido 0,95 e nel 97,5 % con 0,80.

**8. L'analogia con la pista è rovesciata.** Le luci di stato si accendono per **traffico osservato** («Two aircraft, or a surface vehicle and an aircraft, are required»), non per ciò che non si vede. La parte citabile è un'altra: «When the THLs extinguish, this is not clearance»; il sistema «does not substitute for or convey an ATC clearance» [A su riproduzione di terzi, F6]. «Runway Hold» non è un sistema; la scala «TA / HOLD / RA» mescola bordo e terra e non compare nelle fonti lette (un campione).

## 4. Dove la preproposta ha letto male il v0.5 o il nucleo

- **«NOMINAL (Go)»** contraddice il v0.5 §4 («mai "via libera"») e la condizione 9 del verdetto.
- **Zone non osservate strutturali:** il nucleo (B7) le dichiara all'avvio e le toglie dal messaggio per fotogramma; S8 le rimette nel corridoio.
- **«Sotto 1,1 m»** nel v0.5 è una **distanza dal sensore** («fra 1,1 e 3 m»; B1: «invisibile sotto 1,09 m»), non una quota come la legge la preproposta (§1.2, §4).
- **«Volume protetto dell'utente»:** un volume attorno al sensore fermo cade nell'anello cieco (suolo visto da 1,24 m).
- **Probabilità sulle tracce «previste»:** oggi il «previsto» dura circa 0,5 s; il resto dipende da S3 e S4.

## 5. Le versioni corrette

**S6 (`esperto-dominio-9a`).** Per ogni traccia osservata: tempo e distanza al massimo avvicinamento **rispetto al punto protetto dichiarato**, con la covarianza **portata a quell'istante**. Prova prudente: «l'ellisse al 95 % (2,45 σ) tocca la zona di rispetto», solo entro un orizzonte T_h dichiarato (1,0–1,2 s con il q attuale; a 1,5 s un passaggio a 1,5 m di lato dà già falso allarme). La probabilità si può mostrare, mai usare per dire «nominale». Tracce non osservate: decide la «possibile presenza». **Smentita se** su 30 avvicinamenti diretti registrati l'avviso arriva a meno di 0,5 s dal contatto, o su 30 passaggi a 1,5 m di lato scatta più di 3 volte.

**S7.** Nessun indice: l'etichetta «avvicinamento diretto / attraversamento» si ricava dalla distanza al massimo avvicinamento.

**S8 (`esperto-dominio-9b`): quattro livelli ordinati per ciò che chiedono, più un indicatore.**

| Preproposta | Nome onesto | Che cosa chiede |
|---|---|---|
| NOMINAL (Go) | «Nessun ostacolo osservato nel corridoio fino a d m» | niente; non è un'autorizzazione |
| TA | «Attenzione: oggetto in avvicinamento» (osservato o previsto) | guardare |
| HOLD | «Attesa prudente richiesta: corridoio non confermato» | attendere; finisce solo guardando |
| RA | «Allarme di prossimità: arresto richiesto» | fermarsi (richiesta, non comando) |
| FAIL-SAFE | a parte: «Affidabilità persa» | non è un livello di rischio |

Corridoio: dichiarato all'avvio, **tutto dentro la zona di valutazione**, con una cella di margine (regge: 1,3–2,9 m, largo 1 m). Attesa se: una cella «possibile presenza»; un ostacolo o la sua ombra nel corridoio; buchi su almeno il 2 % delle celle per 3 cicli (0,00 % di falsi a 0,95 e a 0,80). Più prudente, NV: «buchi contigui più larghi dell'oggetto minimo». Il primo livello dice la quota di corridoio non vista.

**Citabili come «ispirato a»:** il tempo al massimo avvicinamento (ACAS); l'avviso che non autorizza manovre, per il secondo livello; «spento non è autorizzato» (luci di pista); il rischio per zona (radar per volatili). **Da non usare:** RA e TA come nomi di stati, ACAS, ABAR, «fail-safe», «Go», «On-Boresight», «minaccia», «conforme a».

## 6. Il riferimento più vicino alla traccia: la distanza protettiva

Per aree condivise fra persone e mezzi il concetto consolidato è la **sorveglianza di velocità e separazione** (ISO/TS 15066, confluita in ISO 10218-2:2025 [R]). Forma lineare [A, F7]: **S = v_H·T_R + v_H·T_S + v_R·T_R + B + C + Z_S + Z_R**: T_R «the time for the robot system to respond to the operator's presence», T_S tempo d'arresto, C margine d'intrusione, Z_S «operator position (sensor) uncertainty»; v_H = 1,6 m/s (da ISO 13855). **Latenza e incertezza di misura ci sono già.** Sotto S quel sistema avvia un arresto: comanda, quindi anche questo è «ispirato a». Con i numeri del nucleo (latenza 0,155 s, Z_S = 0,10 m, C = 0,85 m [R]): **2,80 m** se si chiede a una persona (reazione 1 s), **1,68 m** con arresto automatico in 0,3 s; con 3 m di portata e 0,27 s di conferma la velocità coperta è 1,44 m/s. È più vicino alla traccia («ambienti industriali») dell'ACAS, e i suoi termini si misurano alla prima ora. Zone di rispetto dei piazzali aeroportuali: NV.

## 7. Il giurato di una società aerospaziale

**Apprezza:** «non visto non è libero», come nelle luci di pista; latenza e incertezza in una formula; la diluizione nominata; livelli definiti da ciò che chiedono; l'avaria separata. **Contesta:** «RA» senza manovra prescritta; l'ACAS detto aeroportuale; «bird strike» nel titolo; soglie senza taratura; parole di puntamento. I velivoli senza equipaggio hanno una scala propria (avvisi preventivo, correttivo, d'allarme [A, F8]): «un'altra scala», come in f6.

## 8. Costo

| Voce | Ore-persona | Calcolo per ciclo |
|---|---|---|
| S6 corretta | 4 (2 codice, 1 prova, 1 taratura di T_h e q) | 0,42 µs per traccia, sola formula, Python puro (misurato) |
| S7 come etichetta | 0,5 | compreso |
| S8 corretta | 3, di cui circa 2 già in B7 | conteggio su 454–900 celle: NV |

Netto circa 6 ore-persona. **A 24 ore entra solo S8 corretta**; S6 va nel taglio a 38 ore (S12 la mette a 24) al posto dell'etichetta della rete (B6, 4 ore).

## 9. Non verificato, e dopo

Testi ISO (a pagamento: letti tramite F7 e riassunti [R]); C = 0,85 m e il termine d'incertezza di ISO 13855:2024 [R]; AIM su faa.gov (403) e SKYbrary (bloccata); tempi DO-365 [R]; q, incertezza della velocità e T_h sul sensore vero; S6 sulle tracce previste; il 2 % con buchi correlati (simulati indipendenti). **Dopo:** al curatore le citazioni [R]; a f8 T_h con il q tarato; all'arbitro l'ordine fra «attesa» e «attenzione» rispetto alla graduatoria di B7.

**Fonti.** F1 https://birdstrike.org/wp-content/uploads/2024/04/TS5-P19-J.Lewis_.pdf · F2 https://www.accipiterradar.com/faa-advisory-circular-1505220-25-airport-avian-radar · F3 https://www.eurocontrol.int/sites/default/files/2025-09/eurocontrol-safety-acas-guide-5-0.pdf · F4 https://arxiv.org/abs/1706.08565 · F5 https://ialacolreg.com/en/colreg/rule-7 · F6 https://www.angleofattack.com/aim/chapter-2/2-1-6/ · F7 https://pmc.ncbi.nlm.nih.gov/articles/PMC5117641 · F8 https://nasa.github.io/WellClear
