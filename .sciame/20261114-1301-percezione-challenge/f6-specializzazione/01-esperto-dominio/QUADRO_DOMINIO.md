# Quadro di dominio — sistemi uncrewed, lato percezione (`sciame-esperto-dominio`, f6)

**Campo in cui parlo:** percezione per sistemi senza equipaggio (aerei UAS, terrestri UGV, di superficie USV) in aerospazio e difesa. Ricerche in rete del 14 novembre 2026, fra le 14:06 e le 14:12.

**In testa.**

- **Cambio di stato proposto:** «Mare Group ha avuto un contratto per veicoli uncrewed a ottobre 2026» passa da *riferito dall'utente* a **sostenuto dai dati, con due precisazioni**: è un *ordine* da 1,7 milioni per «sistemi uncrewed», preso tramite la controllata CTMAVIO; nessuna fonte dice il tipo di piattaforma, il cliente o l'uso.
- **Regole violate:** regola 3 (nessuna previsione scritta prima delle ricerche). Lo strumento di lettura ha salvato da solo un PDF dell'EASA fuori dalla cartella di consegna: l'ho solo convertito in testo nella cartella temporanea.
- **Indipendenza:** le notizie sulla società derivano tutte dai suoi comunicati: più testate non sono più prove. Le pagine le riassume un modello ausiliario: le frasi fra «» vanno ricontrollate dal curatore delle fonti.
- **Sigle:** **[A]** pagina aperta; **[R]** trovata dal motore di ricerca, non aperta; **NV** non verificato; **[inf.]** inferenza mia, non fatto del dominio. L'elenco dei link (S1–S38) è in fondo.
- **Scostamento sulla lunghezza:** il corpo ha circa 2.450 parole. Misurato dopo la consegna (pandoc e xelatex, A4, corpo 10, margini 1,8 cm): quattro pagine e mezza e non le tre chieste, più mezza pagina di link. Non ho tagliato oltre per non togliere le fonti ai sei punti della consegna.

## 1. La società: che cosa risulta

| Affermazione | Esito | Fonte |
|---|---|---|
| Società di «ingegneria ad alta tecnologia per progettare, sviluppare e produrre sistemi complessi», quotata su Euronext Growth Milan; settori Aerospace & Defence, Industry & Transportation, Infrastructure & Building; fra le linee: Intelligenza Artificiale, XR & Simulation, Digital Twin, Testing | sostenuto | [A] S1 |
| **21-10-2026:** «Primo ordine da cliente estero da 1,7 milioni di euro per sistemi uncrewed», tramite CTMAVIO, da eseguire per lo più nel 2026. La stampa lo lega a componenti e strutture per usi aeronautici, motoristici e UAV | sostenuto; cliente, piattaforma e uso **NV** | [A] S2–S5 |
| 05-06-2026: prime commesse (circa 1,05 milioni): ingegneria di sistema e sottosistemi di bordo «critici per la sicurezza» di un velivolo a pilotaggio remoto medio-grande | sostenuto | [A] S6 |
| 09-06-2026: 20 % di NIDO, con opzione per il 51 %. Piattaforma NIDO: drone H815, stazione di ricovero e ricarica, calcolo a bordo, voli oltre la linea di vista con supervisione umana remota. Usi: ispezione di strade, infrastrutture, condotte e reti; sorveglianza perimetrale; duplice uso | sostenuto | [A] S7 |
| 10-07-2026: Task Force X (NATO, Torre Veneri) con NIDO, GMSPAZIO e CTM Avio: sorveglianza continua e protezione delle infrastrutture critiche | sostenuto | [A] S8 |
| 24-07-2026: accordo per comprare CTMAVIO (9 milioni); 15-09-2026: via libera Golden Power | sostenuto; chiusura **NV** | [A] S9, S10 |
| 28-07-2026: accordo quadro da 8,3 milioni, oltre 6.000 kit motore per velivoli senza pilota | sostenuto dalla stampa | [R] S11 |
| Linee terrestri o navali; prodotti di percezione o visione artificiale; notizie pubbliche sull'hackathon | **non trovate** | S10 |

**Lettura [inf.].** Il profilo pubblico è aereo, e con NIDO è un drone da ispezione con autonomia a bordo e supervisione remota. La demo più vicina a ciò che la società mostra è **ispezione e sorveglianza da drone con operatore remoto**, non il traffico aereo.

## 2. Che cosa cambia rispetto al nucleo a sensore fermo

**(a) Il moto proprio arriva dall'autopilota.** Su un UAS lo stimatore di stato fonde IMU (in predizione, almeno 100 Hz), magnetometro, GNSS con controlli di qualità, barometro, telemetro e visione esterna, e dà assetto, velocità e posizione ([A] S12): la percezione *riceve* una posa con la marca temporale. Una camera indossata non ha nulla di simile. Su UGV: ruote, giroscopio, GNSS; su USV: GNSS e bussola (NV). Qualità in numeri: **NV** (confronto di riferimento: [R] S13, non letto). **[inf.]** Al nucleo serve l'errore *relativo* sull'orizzonte della previsione, soprattutto d'assetto: 1° di imbardata a 10 m vale 17 cm. Un drone in volo stazionario non è fermo: oscilla e si inclina contro il vento. In un hangar il GNSS manca: serve odometria visuale o LiDAR.

**(b) I sensori realistici.**

| Sensore | Dato | Limite | Fonte |
|---|---|---|---|
| Stereo attiva (D455) | campo ideale 0,6–6 m; errore < 2 % a 4 m, crescente con z² | all'aperto con luce forte un preprint del 2025 trova prestazioni imprevedibili | [R] S14 |
| LiDAR a stato solido (Livox Mid-360) | 40 m al 10 % di riflettività, 70 m all'80 %, a 100 klx; 360° × 59°; 10 Hz; 265 g; 6,5 W | zona cieca 0,1 m; vetro e pioggia NV | [A] S15 |
| Radar a 77 GHz | vede nel buio e nel fumo, misura la velocità radiale; su un quadrirotore: tracciatore su Raspberry Pi 4B, 75 ms fino al comando, avvicinamenti fino a 14,6 m/s | errori laterali fino a 0,9 m; è un preprint | [A] S16 |
| Termico (Boson 640) | nucleo da 7,5 g, circa 0,6–1 W | direzione, non distanza | [R] S17 |
| Telemetri a fascio | ingressi tipici della prevenzione delle collisioni dell'autopilota | settori stretti (esempio: 35°) | [A] S18 |

**[inf.]** Sotto il chilo: camere e telemetri. Da due chili: LiDAR leggero o radar. I rover portano tutto.

**(c) Le scale.** Dal dominio: 19 m/s è il tetto delle classi C0 e C1 della categoria aperta, 3 m/s il modo lento della C2 ([R] S19); la prevenzione delle collisioni di PX4 è provata a 4 m/s, con messaggi a 10 Hz e ritardi di 0,1–0,5 s ([A] S18). Il «restare ben distanti» dal traffico con equipaggio ragiona su 35 s e oltre un chilometro ([R] S20; cifre dal riassunto del motore): **un'altra scala, fuori dalla portata di una camera di profondità**.
**[inf.]** Il tempo utile è (portata − spazio d'arresto) / velocità di avvicinamento: circa 1 s con 3 m e 2,5 m/s; 4 s con 40 m e 10 m/s. Quindi:

- l'orizzonte del «previsto» (1–1,6 s nel nucleo, per pedoni a 3 m) si ricalcola per classe; la regola «finché copre meno di metà dell'ombra» non dipende dalla scala e si conserva;
- **v_max diventa un parametro di classe**: persona 2,5 m/s (il nucleo); mezzo di piazzale 5–8 m/s (NV); piccolo drone fino a 19 m/s ([R] S19). A 19 m/s l'area raggiungibile dopo 2 s ha 38 m di raggio: il «previsto» non informa più e resta «perso, zona non osservata». È il comportamento onesto del nucleo, ma va detto;
- per bersagli in volo il piano del suolo non basta: serve la quota.

**(d) Le occlusioni che contano [inf., dal campo].** In ordine di frequenza: (1) **uscita dal campo per il moto proprio** (la piattaforma ruota): nel nucleo è già «perso, fuori campo»; (2) strutture ferme, e nell'ispezione l'oggetto stesso: ala, fusoliera, carrello, attrezzature di terra, tubazioni; (3) altri veicoli: l'ombra si sposta, e la maschera per fotogramma la segue; (4) **il veicolo stesso** (eliche, bracci, pattini): maschera fissa dichiarata «non osservato»; (5) vegetazione: ritorni misti; (6) polvere, fumo, controluce: i «buchi» del nucleo. I lavori sul tracciamento da drone nominano insieme occlusione e moto irregolare della camera ([R] S21, S22).

**(e) A chi va il feedback.**

- **All'autopilota.** L'interfaccia di fatto è il messaggio per settori OBSTACLE_DISTANCE: `UINT16_MAX` vuol dire sconosciuto, `max_distance + 1` nessun ostacolo ([R] S23). PX4: «If there is no sensor data in a particular direction, velocity in that direction is restricted to 0»; oltre 0,5 s senza dati azzera i comandi orizzontali, dopo 5 s passa in attesa; la regione di un sensore guasto è «treated as uncovered» ([A] S18). **È il principio degli invarianti 1, 2 e 8: «sconosciuto» non è «libero».** [inf.] La griglia polare del nucleo si traduce in questo messaggio quasi senza lavoro.
- **All'operatore remoto.** Mappa o video con i tre stati e l'età del dato. [inf.] L'invariante 8 si estende al collegamento: senza un messaggio fresco, alla stazione compare «affidabilità persa».
- **Agli altri veicoli.** Tracce con stato, età e accuratezza (punto 3).

«Segnalare la perdita di affidabilità», nel dominio, è dichiararla **e** legarla a un comportamento: rallentare, attesa, rientro, richiesta all'operatore. L'EASA chiede di individuare i modi di deterioramento dei sistemi esterni («complete loss of GNSS… latency issues») e i mezzi per rilevarli ([A] S24); la perdita del collegamento ha un'azione configurata ([R] S25). Il prototipo dichiara soltanto, e può mostrare quale comportamento chiederebbe.

**(f) Calcolo, peso, collegamento.** Una Jetson Orin Nano lavora a 7, 15 o 25 W ([R] S26); una catena radar con tracciatore gira su un Raspberry Pi 4B ([A] S16). [inf.] Il percorso geometrico del nucleo ci sta; la rete di B6 resta asincrona. La percezione che protegge il veicolo sta a bordo, perché il collegamento può mancare. Latenze tipiche di un collegamento: **NV**.

## 3. I riferimenti che danno credito

**Consolidato.**

- **Definizione.** Detect and avoid: «The capability to see, sense or detect conflicting traffic or other hazards and take the appropriate action to comply with the acceptable rules of flight»; funzioni: «detect, decide, command, execute and feedback loop» ([A] S24).
- **Norme tecniche.** RTCA DO-365 e EUROCAE ED-275 ([R] S20); ASTM F3442-25 per velivoli piccoli, che esclude uccelli e incontri fra droni ([R] S27). L'EASA rinvia a «RTCA SC-228 and/or EUROCAE WG-105» ([A] S24).
- **Quadro europeo.** Droni: regolamenti (UE) 2019/947 e 2019/945, U-space 2021/664 ([R] S28); valutazione del rischio SORA 2.5 nella decisione 2025/018/R ([R] S28; testo [A] S24). Terra: nessuna norma dedicata; regolamento macchine (UE) 2023/1230 dal 20 gennaio 2027, il primo a nominare le macchine mobili autonome, e ISO 3691-4:2023 ([R] S29). Mare: codice MASS dell'IMO, non obbligatorio, dal 1° luglio 2026, solo navi da carico ([R] S30).
- **La traccia non più osservata.** Nei dati di sorveglianza (ASTERIX, categoria 062) lo stato di traccia ha il bit CST, «Age of the last received track update is higher than system dependent threshold (coasting)», il bit CNF fra «Confirmed track» e «Tentative track», le età degli aggiornamenti e le accuratezze stimate ([A] S31, trascrizione non ufficiale). **Osservato, in coasting, con età e accuratezza: è il vocabolario del nucleo.**

**Non consolidato (ricerca).**

- **Lo strato 1** non è nelle norme di sorveglianza. Viene dalla guida automatica: ostacoli nascosti ai bordi del campo visivo, con stati sovrastimati per intervalli ([A] S32); oggetti fantasma fuori dall'area osservata ([R] S33). Griglie dinamiche: [A] S34.
- **Tracciamento attraverso le occlusioni da piattaforma in moto:** compensazione del moto della camera nel filtro ([A] S35); tracciatori per drone ([R] S21, S22); radar a bordo ([A] S16). [inf.] Si misurano sull'identità nel piano dell'immagine. Non ho trovato una metrica per «mai libero dove non è osservato»: è il tratto distintivo del nucleo, e nessuna fonte lo certifica.

**Cautela.** Il nucleo è prevenzione delle collisioni a corto raggio, non un «detect and avoid» nel senso delle norme. Dire «ispirato a», mai «conforme a».

## 4. Tre scenari di demo

| Scenario | Che cosa mostra | In più rispetto al nucleo | Rischio principale |
|---|---|---|---|
| **1. Sentinella ferma.** Rover fermo, o drone in volo stazionario simulato dal treppiede, su un varco o un oggetto in ispezione | R1–R8 come nel nucleo | il racconto; lo schermo dell'operatore al posto della voce; l'uscita per settori a tre valori. Qualche ora | la giuria vede un treppiede: mostrare l'uscita che un autopilota leggerebbe, e dire che un drone vero non sta fermo |
| **2. Piattaforma che avanza piano.** Carrello o rover a 0,3–0,5 m/s, posa da ruote e giroscopio o da odometria visuale | continuità con il sensore in moto; uscita dal campo come «perso» | tracce e memoria della griglia nel riferimento del mondo; sincronia fra posa e profondità; regola «mobile» compensata. **Nessuna soglia del nucleo è provata qui** | ogni muro diventa «mobile» (F-008). Ripiego: scenario 1 |
| **3. Riproduzione o simulatore.** La stessa catena su registrazioni con posa, o su un autopilota simulato | velocità e distanze irraggiungibili in sala; il veicolo che si ferma verso i settori sconosciuti | integrazione e scelta dei dati; fattibilità nei tempi **NV** | profondità simulata troppo pulita: non prova niente sul sensore vero |

**Consiglio [inf.]:** lo scenario 1 è la demo; un filmato breve del 2 o del 3 mostra la direzione.

## 5. Gli innesti per gli sviluppi futuri [inf.]

- **Altri sensori:** entrano nella griglia (B2) e nelle misure del filtro (B4), ciascuno con il suo rumore e la sua nozione di «buco». «Libero osservato» solo da un sensore capace di vedere il vuoto. Il radar porta la velocità radiale; il termico entra da B6.
- **Più veicoli:** scambio di tracce (stato, età, covarianza) e di zone non osservate; con correlazioni ignote, intersezione delle covarianze ([R] S36). Un «libero» altrui vale solo se fresco e in un riferimento comune.
- **Piattaforme diverse:** diventano parametri il montaggio, la maschera del veicolo, il modello del suolo, v_max e orizzonte per classe. In mare la superficie non è un pavimento (NV).
- **Ritorno all'assistivo:** stesso nucleo, moto proprio da sensori indossati, feedback vocale (soluzione, tabella 5).

## 6. I limiti da dichiarare

- **Ambito:** osservazione, ispezione, navigazione sicura. Niente ingaggio, puntamento o indicazione di bersagli. [inf.] La «gravità» di B7 va chiamata *priorità di rischio di collisione*, perché non si legga come graduatoria di minacce.
- **Natura:** prototipo dimostrativo, non certificato.
- **Volare:** le regole europee valgono per chi vola davvero ([R] S28); all'hackathon conviene non volare. Voli al chiuso: NV.
- **Esportazione e duplice uso:** regolamento (UE) 2021/821 e legge 185/1990 con l'autorità UAMA ([R] S37); voci per droni e camere termiche NV. Il Golden Power su CTMAVIO ([A] S10) dice che il settore è vigilato. Per un prototipo di componenti commerciali lo valuta la società.
- **Regolamento sull'intelligenza artificiale:** esclude i sistemi «exclusively for military, defence or national security purposes»; il duplice uso resta dentro ([R] S38).
- **Riprese di persone:** all'analista normativo (NV). Questo quadro non è un parere legale.

## Stati proposti e passi successivi

- **Sostenuto dai dati:** l'ordine del 21-10-2026; il profilo aereo e da ispezione della società; «sconosciuto non è libero» nella pratica degli autopiloti; il coasting nei dati di sorveglianza.
- **Non risolto:** il tipo di piattaforma dell'ordine (lo decide il comunicato integrale o la società); la qualità del moto proprio (una misura sulla piattaforma scelta).
- **Proposte, con la smentita:**
  - `esperto-dominio-1`, uscita per settori a tre valori: smentita se un settore non osservato esce una volta come distanza valida.
  - `esperto-dominio-2`, v_max e orizzonte per classe: smentita se il «previsto» resta acceso con l'area raggiungibile più grande dell'ombra.
  - `esperto-dominio-3`, maschera del veicolo: smentita se una parte del veicolo genera tracce.
- **Dopo:** al curatore delle fonti le citazioni [R] e la trascrizione ASTERIX; all'esperto di odometria l'errore di posa su 2 s; all'analista normativo il punto 6.

## Fonti

S1 https://www.maregroup.it/ · S2 https://www.maregroup.it/news/primo-ordine-estero-sistemi-uncrewed · S3 https://www.borsaitaliana.it/borsa/notizie/teleborsa/finanza/mare-group-primo-ordine-da-un-cliente-estero-per-sistemi-uncrewed-da-17-milioni-di-euro-21_2026-10-21_TLB.html?lang=it · S4 https://www.soldionline.it/notizie/azioni-italia/mare-group-primo-ordine-estero-sistemi-uncrewed · S5 https://www.websim.it/azioni/small-mid-cap/notizie/mare-group-nuovo-ordine-da-1-7-milioni-di-euro/ · S6 https://www.teleborsa.it/News/2026/06/05/mare-group-prima-commessa-per-velivoli-a-pilotaggio-remoto-valore-superiore-a-1-milione-di-euro-53.html · S7 https://www.teleborsa.it/News/2026/06/09/mare-group-entra-nel-capitale-di-nido-al-20percent-con-opzione-per-il-controllo-entro-24-mesi-5.html · S8 https://www.websim.it/azioni/small-mid-cap/notizie/mare-group-scelta-dalla-nato-per-la-task-force-x/ · S9 https://www.teleborsa.it/News/2026/07/24/mare-group-acquisisce-ctmavio-e-rafforza-la-filiera-dei-droni-per-aerospazio-e-difesa-17.html · S10 https://www.maregroup.it/news/ · S11 https://www.teleborsa.it/News/2026/07/28/mare-group-contratto-da-8-3-milioni-di-euro-per-unita-di-propulsione-uav-13.html · S12 https://docs.px4.io/main/en/advanced_config/tuning_the_ecl_ekf · S13 https://rpg.ifi.uzh.ch/docs/ICRA18_Delmerico.pdf · S14 https://www.preprints.org/manuscript/202511.0498 e https://forums.intel.com/cipcp26785/attachments/cipcp26785/feeditem_no_topic/6364/1/BKMs_Tuning_RealSense_D4xx_Cam.pdf · S15 https://www.livoxtech.com/mid-360/specs · S16 https://arxiv.org/abs/2608.01855 · S17 https://www.oem.flir.com/products/boson/ · S18 https://docs.px4.io/main/en/computer_vision/collision_prevention · S19 https://www.easa.europa.eu/en/the-agency/faqs/open-category (cifre lette in guide secondarie) · S20 https://standards.globalspec.com/std/14562761/do-365c e https://standards.globalspec.com/std/14356966/eurocae-ed-275 · S21 https://mlanthology.org/cvpr/2022/liu2022cvpr-multiobject · S22 https://mdpi.com/2504-446X/8/9/480 (403 all'apertura) · S23 https://docs.px4.io/main/en/msg_docs/ObstacleDistance · S24 https://www.easa.europa.eu/sites/default/files/dfu/annex_to_ed_decision_2025-018-r_1_2.pdf · S25 https://docs.px4.io/main/en/config/safety · S26 https://www.kiwi-electronics.com/en/single-board-computers-390/nvidia-jetson-orin-nano-super-developer-kit-11461 · S27 https://store.astm.org/f3442-25.html · S28 https://www.easa.europa.eu/domains/drones-air-mobility/rules-standards e https://eur-lex.europa.eu/eli/reg_impl/2021/664/2026-02-22/eng/pdf · S29 https://eur-lex.europa.eu/eli/reg/2023/1230/corrigendum/2023-07-04/oj/eng e https://genorma.com/en/standards/en-iso-3691-4-2023 · S30 https://www.dnv.com/news/2026/imo-mcs-111-new-mass-code-adopted/ · S31 https://zoranbosnjak.github.io/asterix-specs/specs/cat062/cats/cat1.18/definition.html · S32 https://arxiv.org/abs/1807.01262 · S33 https://mediatum.ub.tum.de/doc/1575368/1575368.pdf · S34 https://arxiv.org/abs/1605.02406 · S35 https://arxiv.org/abs/2206.14651 · S36 https://arxiv.org/pdf/2203.16964 · S37 https://www.esteri.it/it/ministero/struttura/uama/ e https://eur-lex.europa.eu/EN/legal-content/summary/dual-use-export-controls.html · S38 https://verfassungsblog.de/the-ai-act-national-security-exception/
