# Sezione E — Ambiti d'uso, profili e dominio

*Bozza per `STATO_PROGETTO.md` · `sciame-esperto-dominio`, fase f11 · 14 novembre 2026, dalle 16:16 (`date -Is`).*

**Campo in cui parlo:** monitoraggio e ispezione in ambienti aerospaziali e industriali, sistemi uncrewed (senza equipaggio), ausili per persone non vedenti, dal lato della percezione. Non è un parere legale, regolatorio, medico o di sicurezza funzionale: per quelle decisioni serve un professionista.

**In testa.**

- **Cambi di stato proposti.** (1) «L'ordine del 21 ottobre 2026 è della controllata CTMAVIO»: sostenuto **dalla stampa**; la pagina della società, riaperta oggi, non nomina la controllata (§E.6). (2) Il messaggio per settori degli autopiloti aperti, in f6 solo un risultato di ricerca, è ora **pagina aperta** (§E.3). (3) La distanza protettiva di 2,80 e 1,68 m (f9) vale per una persona a 1,6 m/s; la fonte raccomanda 2,0 m/s: **non risolto** quale usare (§E.3).
- **Scostamenti.** Ho scritto anche `PREVISIONI.md` in questa cartella (dodici previsioni sulle fonti, con gli esiti; un'ora approssimata in un titolo, corretta e dichiarata lì). Due pagine consultate senza previsione, per i soli dati bibliografici. Nessuna simulazione rifatta: ho ricontato solo parole nella traccia e nel sorgente della proposta. Le pagine in rete le riassume uno strumento ausiliario: le frasi fra «» vanno ricontrollate dal curatore sul testo grezzo. Non ho letto tutta la convocazione (elenco in coda). **Lunghezza:** il corpo sta nel limite di sei pagine sul metro a parole dello sciame, ma composto ne occupa dieci per via delle tabelle (misure in coda).
- **Niente è provato sull'hardware.** Il nucleo è «adottabile come progetto di prototipo, non come sistema validato» (VER §4): simulazione, sensore fermo, scala di una stanza.

**Come leggere.** Stati: *dimostrato* (in un modello nominato); *verificato* (controllo esaustivo su un insieme dichiarato); *sostenuto dai dati* (in simulazione); *smentito*; *non risolto*; *non verificato fino all'hardware*; *preliminare* (dalle estensioni f7–f10: **non ancora vagliato dall'arbitro**); *progetto, mai simulato*. Fonti: **[C]** verificata dal curatore (`f3/fonti/FONTI_VERIFICATE.md`); **[A]** aperta dal ruolo che la cita; **[A11]** riaperta oggi da me; **[R]** vista solo in un risultato o riassunto di ricerca; **NV** non verificata.

**Rimandi** (percorsi relativi alla cartella della convocazione). V2 = `f4/H-012/05-correzioni/SOLUZIONE_V2.md`, il *nucleo* approvato; VER = `f4/H-012/09-arbitro/VERDETTO.md`; AUD = `f5/02-audit/AUDIT.md`; Q, SP = `f6-specializzazione/01-esperto-dominio/QUADRO_DOMINIO.md` e `SPECIALIZZAZIONE.md`; MP = `f6-specializzazione/02-slam/MOTO_PROPRIO.md`; ATT = `f6-specializzazione/03-avversario/ATTACCO_SPECIALIZZAZIONE.md` (cifre in `risultati_spec.txt`, `risultati_spec2.txt`); R7, D7 = `f7-estensione/04-requisiti/CONSEGNA.md` e `05-esperto-dominio/CONSEGNA.md`; TR7 = `f7-estensione/10-triage/TRIAGE.md`; D9 = `f9-preproposta/06-esperto-dominio/CONSEGNA.md`.

**Sigle interne.** R1–R8: i requisiti ricavati dalla traccia. B1–B9: i blocchi del sistema. K-…: contraddizioni fra ruoli; F-…: fatti stabiliti. C1–C8: qui, le correzioni obbligate dell'attacco alla specializzazione (non le C1–C11 del nucleo); «ATT, S1…S7»: i sette attacchi di quel file. V-…, T-…: ipotesi e proposte del triage di f7. *Fascia*: il margine di 0,40 m attorno a una zona nascosta. *Vuoto vicino* (o anello cieco): il suolo a meno di 1,24 m, che la camera non vede.

## E.1 L'ambito, con le parole della traccia

La traccia (`regole_challenge.md`, sei righe) ammette due applicazioni: l'«orientamento assistito di persone con disabilità visiva» oppure il «monitoraggio di attività e oggetti in ambienti aerospaziali e industriali»; in premessa nomina «sistemi per l'accessibilità e soluzioni di osservazione e ispezione nei settori Aerospace & Industry».

- **Verificato** (ricerca testuale su tutta la traccia): `uncrewed`, `drone`, `UAV`, `veicol`, `volo`, `3D`, `voxel` compaiono 0 volte (R7 §2 e §4; TR7, F-113; ricontato oggi, anche `autopilot`, `unmanned`, `pilot`: 0). R7 dice «dieci radici», TR7 «sette»: cambia l'elenco, non l'esito.
- **La storia.** Il contratto lasciava aperta la scelta fra le due applicazioni; la selezione l'ha rimessa all'utente (K-008, `f2/05-selezione/SELEZIONE.md` §6: «solo il sensore fermo ha prove»). Il primo addendum chiede la specializzazione uncrewed; il secondo fissa due ambiti; il terzo chiede le parole della traccia: **il veicolo uncrewed è un modo di portare il sensore, non l'ambito** (`ADDENDUM_UTENTE.md`).
- **Formulazione in uso** (proposta dalla v0.4: `proposta/VERSIONI.md`, nella radice del progetto): caso principale «monitoraggio di attività e oggetti in ambienti aerospaziali e industriali»; secondo profilo «avviso per una persona non vedente». Nel sorgente v0.6 `uncrewed` compare una volta, accanto a «ferma»; «volo stazionario» mai (ricontato oggi).
- **Tre assi** (T-001, *preliminare*): l'**applicazione** (le due della traccia), il **portatore del sensore** (supporto fisso o piattaforma uncrewed ferma), l'**uscita** (schermo e registro, oppure suoni). Regola di redazione: ogni frase con «uncrewed» contiene «ferma» o «non provato» (R7 §5).

**Nel campo, «monitoraggio di attività e oggetti»** vuol dire sapere chi e che cosa si muove in un'area di lavoro dichiarata, dov'è, e quando non lo si sa più (D7 §4, *preliminare*). Tre casi documentati: (1) l'area attorno a un velivolo, dove velivolo e mezzi nascondono le persone: il danno a terra potrebbe arrivare a «nearly $10 billion by 2035», nastri, caricatori, scale e pontili causano il «40% of total incidents», mezzi con anticollisione ridurrebbero il costo atteso del 42 % (stima dell'associazione) [iata-gse2022] https://www.iata.org/en/pressroom/2022-releases/2022-12-06-04/ **[A11]**; (2) l'area condivisa fra persone e robot o mezzi (§E.3); (3) l'ispezione visiva con drone in hangar [aviationweek-ispezioni] https://aviationweek.com/mro/emerging-technologies/aircraft-inspections-drones-accelerate-toward-next-evolution **[A]**.

**Che cosa il prototipo non fa in questo ambito.**

| Limite | Numero | File e stato |
|---------------------|---------------------|------------------------------|
| Il «monitoraggio di attività» non è coperto dal nucleo; l'«ispezione» non è una sua funzione | — | V2 §7; R7, critica 8. Lo coprirebbe un registro di eventi (T-002, *preliminare*): 0 violazioni su 600 scene, ma un evento mancato in 103 scene su 200 e «scomparse» spurie nel 12,5 % |
| Non rileva oggetti estranei al suolo | gli oggetti di riferimento delle piste (sfera di 4,3 cm, cilindro di 3 × 3,8 cm) stanno sotto i 7 cm di quota minima; con 5 pixel di lato: 3,4 cm a 3 m | D7, C6, `risultati_osservabilita.txt`: *dimostrato* nella geometria della camera (848 × 480, 87°); [flightsafety-fod] **[A]**, secondaria |
| Senza una superficie di fondo non c'è «libero» | stanza vuota di 6 m: 44,2 % dei raggi senza ritorno | D7, C4 (scena sintetica); F-112: *sostenuto dai dati*, *preliminare* |
| Con un ostacolo basso (cassa, bancale: il caso comune in industria) il cuneo d'ombra è sbagliato | l'ombra finisce a d·H/(H − h): cuneo 283 celle, vere 164 | F-109: *dimostrato* (geometria); l'effetto sulla continuità è K-102, **aperta** (TR7) |
| Scala e luogo | fino a 3 m, camera a 1,2 m, al chiuso | V2, B1; ATT, C8 |

Link della tabella: [flightsafety-fod] https://flightsafety.org/asw-article/clean-sweep/

## E.2 I profili d'uso

Due profili, entrambi a **sensore fermo**: **monitoraggio** da stazione fissa o da piattaforma uncrewed ferma; **avviso per una persona non vedente ferma** (in attesa a un varco, a una fermata). Fonti: SP §1 corretta da ATT; AUD, ipotesi 12; VER §4.

| Voce (e natura) | Monitoraggio (principale) | Avviso, persona ferma | Stato |
|--------------------|----------------|-------------|--------------------|
| Contratto d'uscita: tre stati (osservato, previsto, perso); il non osservato non diventa mai «libero»; la «possibile presenza» finisce solo guardando — *comune* | identico | identico | «mai libero»: dimostrazione condizionata, per costruzione (VER §1). Possibile presenza: *sostenuta in simulazione* (0 su 14 400 passaggi), con controesempio (13 su 4800) |
| Nove regole fisse — *comune e parametro* | 4 identiche; 5 prendono un termine del profilo | idem | lettura dei testi (ATT, S2) |
| Metodo: soglie prima, bracci che devono fallire — *comune* | identico | identico | — |
| Sensore e montaggio — *parametro, oggi uguale* | camera di profondità stereo su supporto a 1,2 m, inclinata di 15°; o piattaforma ferma alla stessa quota | la stessa, accanto alla persona | altra quota *non provata*: a 0,25 m il suolo si vede da 0,26 m (non 1,24) e a 3 m fino a 1,00 m di quota (non 1,95) (ATT, S7: conto) |
| Moto proprio — *parametro, oggi uguale* | nessuno | nessuno | in moto nessuna soglia vale (VER, condizione 4) |
| Classe e margine — *parametro, oggi uguale* | persona; fascia 0,40 m | idem | onesto fino a circa 1,4 m/s (1,39: conto con 0,288 s fra età del dato e latenza; ATT, S3) |
| Zona di valutazione — *parametro, oggi uguale* | da 1,24 a 3 m, al chiuso | idem; il vuoto vicino lo copre il bastone | conto; *non verificato fino all'hardware* |
| Canale d'uscita — *parametro, diverso* | schermo dell'operatore (tre stati, età del dato, ritardo); registro di eventi (*preliminare*); valore per settore verso un autopilota (*progetto, mai simulato*) | un segnale sonoro di 0,3 s per stato | segnali: una durata ipotizzata, senza persone (ATT, S4) |
| Alla perdita di affidabilità — *parametro, diverso* | la dichiara e *chiede* attesa o verifica dell'operatore | segnale dedicato; si torna a bastone o cane guida | 0,13 s in simulazione (V2 §4, correzione C10 del nucleo); «collegamento caduto»: *non provato* |
| **Da provare** | moto, volo, sole, oltre 3 m, classi veloci, altra quota, valore per settore | persona che cammina, sensore indossato, segnali con persone | *non verificato* |

- **Il conto dell'attacco** (ATT, S2): dei sei parametri, allo stato provato **ne differiscono due** (uscita e reazione alla perdita). Regole identiche 4 su 9 (nessun «osservato» senza misura; assenza dedotta solo dove la profondità è valida; la possibile presenza finisce solo guardando; niente grandezze non osservabili). «Adattabile» si dice quindi come in C5 (§E.5).
- **Il profilo assistivo non ha elementi provati oltre il nucleo comune** (ATT, S4). Camminando, senza una stima del moto, ogni oggetto fermo risulta «in movimento» nel 100 % dei casi (MP §2d: modello con errori ipotizzati).
- **Ciò che è comune davvero** (AUD, ipotesi 12): contratto d'uscita e metodo. Fascia, zona, portata, criterio del sensore inerziale, «libero = suolo visto», parametri del pedone (corpo di 40 cm, conferma 3 su 5) sono del profilo «fermo, pedone, sala»: a 10 m/s 0,288 s valgono 2,9 m, tutta la portata.
- **Cautele assistive.** Prototipo dimostrativo: non è un dispositivo medico né di sicurezza, non sostituisce bastone o cane guida (`CONTRATTO.md`; secondo addendum). Due avvisi *preliminari*: un battito regolare è già un codice per una persona non vedente in Italia (semafori acustici: 60 impulsi al minuto via libera, 120 sgombero; [dpr-495-1992] art. 162, letto su un sito divulgativo, **NV**: `f9-preproposta/09-interfacce/CONSEGNA.md`, critica 11); e non risultano studi su come dire l'incertezza di una previsione a una persona non vedente: l'ausilio più vicino estrapola a 5 s, con sei partecipanti, senza incertezza [kayukawa2019] https://wotipati.github.io/projects/BBeep/paper/CHI'19_BBeep_preprint.pdf **[A]** (`f8-continuita/07-ricercatore/CONSEGNA.md`). Suono o vibrazione: in due studi l'aptico costa più dell'audio ([martinez2014] https://doi.org/10.1007/978-3-319-08599-9_20 **[C]**; [lupu2020] **[C]**, in riassunto); non decide (K-010, aperta).

## E.3 Che cosa del dominio dà credito al nucleo

Tre pratiche consolidate usano il principio del nucleo. Danno credito **all'idea**, non al prototipo: nessuna fonte lo certifica, e non risulta una metrica pubblica per «mai libero dove non è osservato» (Q §3).

| Principio | Nel dominio | Fonte e stato | Dove il paragone finisce |
|-----------|----------------------|------------------|------------------|
| **«Sconosciuto» non è «libero»** | Autopiloti aperti: senza dati in una direzione «velocity in that direction is restricted to 0»; oltre 0,5 s un avviso e nessun movimento, dopo 5 s l'attesa; la regione di un sensore guasto è «treated as uncovered». Nel messaggio per settori `UINT16_MAX` è sconosciuto, `max_distance + 1` nessun ostacolo | [px4-collisionprevention] **[A, A11]**; [px4-obstacledistance] **[A11]** | L'autopilota **comanda**, il prototipo dichiara. Il valore per settore non è mai stato generato. Funzione solo orizzontale, provata a 4 m/s con messaggi a 10 Hz |
| **La traccia non più osservata resta, con età e accuratezza** | Sorveglianza del traffico aereo: bit CST, «Age of the last received track update is higher than system dependent threshold (coasting)»; bit CNF (confermata o provvisoria); età (I062/290) e accuratezze stimate (I062/500). Radar navali: la traccia persa si segnala e «the target's last position should be clearly indicated» | [eurocontrol-asterix062] **[A, A11]**: copia strutturata, **non** il documento ufficiale; [imo-msc192] **[A]**, da f8 (*preliminare*) | È il vocabolario, a un'altra scala. La «possibile presenza» sull'ombra **non** è in queste norme |
| **Latenza e incertezza stanno nella distanza protettiva** | Sorveglianza di velocità e separazione, forma lineare: S = v_H·T_R + v_H·T_S + v_R·T_R + B + C + Z_S + Z_R (T_R reazione del sistema, T_S arresto, C margine d'intrusione, Z_S incertezza del sensore). Un sistema commerciale classifica i volumi in vuoto, occupato, sconosciuto; lo sconosciuto è «treated as occupied» | [marvel2017] **[A, A11]**; [vu2020] **[A, A11]**, autrice del costruttore; norme ISO a pagamento, **non lette** | Quel sistema avvia un arresto. Con i numeri del nucleo (latenza 0,155 s, Z_S 0,10 m, C 0,85 m **[R]**): **2,80 m** se si chiede a una persona, **1,68 m** con arresto in 0,3 s; velocità coperta con 3 m di portata: 1,44 m/s (D9, `prove/risultati_p8_p9_p10.txt`, P6: conto, *preliminare*) |

Link della tabella: [px4-collisionprevention] https://docs.px4.io/main/en/computer_vision/collision_prevention · [px4-obstacledistance] https://docs.px4.io/main/en/msg_docs/ObstacleDistance · [eurocontrol-asterix062] https://zoranbosnjak.github.io/asterix-specs/specs/cat062/cats/cat1.18/definition.html · [imo-msc192] https://law.resource.org/pub/us/cfr/ibr/inc/imo/imo.msc.192.2004.pdf · [marvel2017] https://pmc.ncbi.nlm.nih.gov/articles/PMC5117641 · [vu2020] https://www.therobotreport.com/advanced-vision-future-robot-safety-manufacturing/

**Precisazione di oggi.** La fonte usa v_H = 1,6 m/s ma, letta attraverso lo strumento che riassume, nota che la norma dà 2,0 m/s come massimo e lo raccomanda. Con 2,0 le distanze diventano 3,26 e 1,86 m (conto mio, notato dopo, non vagliato): la prima supera la portata. **Non risolto.**

**Altri agganci, da f9 (*preliminari*).** Il tempo al massimo avvicinamento dell'anticollisione di bordo [eurocontrol-acasguide] https://www.eurocontrol.int/sites/default/files/2025-09/eurocontrol-safety-acas-guide-5-0.pdf **[A]**: passa il principio, **non le soglie** (rapporti di circa 8600 in distanza, 250 in velocità, 12–29 in tempo: D9, critica 3). Le luci di stato della pista: lo spegnimento «is not clearance», il sistema «does not substitute for or convey an ATC clearance» [faa-aim-rwsl] https://www.angleofattack.com/aim/chapter-2/2-1-6/ **[A11]**, sito di terzi. Il rilevamento costante in mare, che a distanza ravvicinata non basta [imo-colreg7] https://ialacolreg.com/en/colreg/rule-7 **[A11]**.

**Non consolidato.** La «possibile presenza» viene dalla ricerca sulla guida automatica: ostacoli nascosti ai bordi del campo visivo, sovrastimati per intervalli [orzechowski2018] https://arxiv.org/abs/1807.01262 **[C]**; oggetti possibili fuori dall'area osservata [koschi2021] https://mediatum.ub.tum.de/doc/1575368/1575368.pdf **[C]** per i soli dati bibliografici; griglie dinamiche [nuss2018] https://arxiv.org/abs/1605.02406 **[C]**. Una probabilità d'intrusione non si usa per dire «nominale»: dati peggiori sembrano ridurre il rischio [balch2019] https://arxiv.org/abs/1706.08565 **[A, A11]**; su rotta di collisione esatta vale 0,16–0,18 a 2 s e 0,12 con rumore di 0,20 m (D9, ivi, P9).

## E.4 Norme e quadri regolatori: «ispirato a», mai «conforme a»

**Nessuna norma è stata applicata.** Il nucleo è prevenzione delle collisioni a corto raggio, non un «detect and avoid» nel senso delle norme (Q §3). Le norme si nominano solo per dire da dove viene un'idea. Nessuna di queste fonti è passata dal curatore.

| Quadro | Che cosa se ne prende | Fonte e stato |
|-------------------------|-------------------------|-------------------------|
| Rilevare ed evitare per velivoli senza equipaggio: valutazione del rischio europea (SORA 2.5, decisione 2025/018/R); RTCA DO-365, EUROCAE ED-275, ASTM F3442-25 | la definizione («detect, decide, command, execute and feedback loop») e la richiesta di individuare i modi di deterioramento. Ragiona su 35 s e oltre un chilometro (da un riassunto di ricerca): **un'altra scala** | [easa-sora25] **[A]**; [rtca-do365], [eurocae-ed275], [astm-f3442] **[R]** |
| Droni in Europa: regolamenti (UE) 2019/947, 2019/945, 2021/664 | 19 m/s come tetto di alcune classi (da guide secondarie). Valgono per chi vola: **all'hackathon conviene non volare** | [ue-2019-947], [ue-2019-945], [ue-2021-664], [easa-categoria-aperta] **[R]** |
| Macchine mobili autonome: regolamento (UE) 2023/1230 (dal 20 gennaio 2027), ISO 3691-4:2023. Navi: codice MASS dell'IMO | contesto; nessuna regola usata | [ue-2023-1230], [iso-3691-4], [imo-mass] **[R]** |
| Sicurezza delle macchine: ISO/TS 15066, confluita in ISO 10218-2:2025; ISO 13855 | la formula della distanza protettiva | tramite [marvel2017]; [iso-ts-15066], [iso-10218-2], [iso-13855] non letti; «confluita» **[R]** |
| Anticollisione di bordo; luci di stato della pista | tempo al massimo avvicinamento; «spento non è autorizzato» | [eurocontrol-acasguide] **[A]**; [faa-aim-rwsl] **[A11]** |
| Dispositivi medici: regolamento (UE) 2017/745, art. 2, punto 1 | è dispositivo medico ciò che il fabbricante destina, fra l'altro, a «compensation for, an injury or disability». **Se un ausilio all'orientamento vi rientri è non verificato** | [ue-2017-745] **[A, A11]**, copia non ufficiale |
| Duplice uso: regolamento (UE) 2021/821, legge 185/1990; regolamento sull'intelligenza artificiale | per un prototipo lo valuta la società | [ue-2021-821], [legge-185-1990], [verfassungsblog-aiact] **[R]** |

Link della tabella: [easa-sora25] https://www.easa.europa.eu/sites/default/files/dfu/annex_to_ed_decision_2025-018-r_1_2.pdf · [ue-2017-745] https://www.legislation.gov.uk/eur/2017/745/article/2/2020-01-31

**Ambito, sempre:** osservazione, monitoraggio, ispezione, navigazione sicura, avviso a una persona non vedente. **Nessuna funzione d'ingaggio o di puntamento**; il prototipo dichiara e chiede, non comanda (`ADDENDUM_UTENTE.md`; contratti di f9 e f10).

## E.5 Che cosa è stato corretto dopo l'attacco alla specializzazione

La specializzazione «un nucleo, due profili» (SP) è stata attaccata con conti sulla geometria (ATT): condividono con i testi attaccati camera, griglia, fascia e latenza, e non valgono per il sensore vero. Ne escono otto **correzioni obbligate** prima di ogni documento per la giuria; **nessuna è stata riprovata** (ATT §3). L'ultima colonna è un mio controllo testuale di oggi su `proposta/proposta_sciame.tex` (v0.6).

| # | Che cosa cadeva | Numero | Correzione | Nel v0.6 |
|---|------------|--------------------|---------------|-------|
| C1 | la frase «una prova» («ogni volta»; «dodici tentativi») | «ogni volta» vale con una persona e rilevamento certo (27 configurazioni da 400 passaggi); con un mancato su dieci 99,7–100 %; con un secondo soggetto dalla stessa ombra 2400 scambi su 2400; nessuno script ha calcolato un «libero» da una profondità | frasi riscritte (§E.7) | sì (righe 91–92) |
| C2 | «mai "nessun ostacolo" a soggetto nascosto» | chi è alto fino a 0,72 / 0,62 / 0,43 / 0,23 m a 0,5 / 0,6 / 0,8 / 1,0 m non è visto: il settore direbbe «nessun ostacolo» | una traccia finita a meno di 0,40 m dal vuoto vicino lascia «sconosciuto» finché non è rivista | solo il limite (riga 190), non la regola |
| C3 | «nell'occlusione i settori tengono la distanza» | pannello a 1,15 m: 18 settori su 18 «sconosciuto»; a 1,50 m 16 su 18; a 1,70–1,90 m 2 «sconosciuto», 12 con distanza, 4 «nessun ostacolo» | pannello a non meno di 1,7 m, attore a 2,3 m | sì (riga 160) |
| C4 | la fascia per classe contava solo l'età del dato | con la latenza: persona 0,72 m, mezzo 2,31 m, piccolo drone 5,48 m (non 0,40 / 1,2 / 2,5) | fascia ≥ 0,20 m + mezza larghezza + velocità massima × (età + latenza misurata); intanto «fino a 1,4 m/s, di corsa no» | sì (righe 97, 184) |
| C5 | «non cambia mai… le nove regole»; «in moto riusa tutto il nucleo» | regole identiche 4 su 9; blocchi cambiati 6 su 9; in moto cambiano 9 righe su 9 | restano identici contratto d'uscita e quattro regole; in moto si riusano solo contratto e griglia del fotogramma | sì (riga 136), senza «quattro su nove» |
| C6 | profilo assistivo detto «orientamento» | zero elementi provati oltre il nucleo | «avviso di presenza per una persona non vedente ferma» | sì (righe 141–143) |
| C7 | piano del suolo ristimato con porta di ±2° | con 2° d'errore una scatola di 15 cm è letta 8,0 / 6,3 / 4,5 cm a 2 / 2,5 / 3 m (soglia 7 cm); oltre 0,37 m/s «nessun ostacolo» a torto nell'1,0 % dei fotogrammi | porta riferita alla taratura da fermo, 1° a 3 m; velocità propria ≤ 0,37 m/s | riguarda il moto, dato per non provato |
| C8 | limiti incompleti | a 0,25 m di quota i numeri cambiano; varco e piazzale sono all'aperto, il sensore no | «al chiuso, fino a 3 m, camera a 1,2 m; il valore per l'autopilota è progetto» | in parte (righe 190, 144) |

Reggono senza riserve nuove: la regola del valore per settore alla lettera, la proposta «nessuna uscita è un comando», l'elenco «da non dire» (ATT §3).

## E.6 La società che propone la sfida: che cosa risulta in pubblico

La società è Mare Group, come riferisce l'utente nel primo addendum. Le notizie derivano tutte dai suoi comunicati: **più testate non sono più prove** (Q, in testa). Nessuna è passata dal curatore. Nel sorgente v0.6 la società non è nominata (0 occorrenze, ricontato oggi).

| Affermazione | Stato | Fonte |
|------------------------------|------------------|--------------------|
| 21-10-2026: «Primo ordine da cliente estero da 1,7 milioni di euro per sistemi uncrewed» | *sostenuto* | [maregroup-ordine2026] **[A, A11]** |
| L'ordine è della controllata CTMAVIO | *sostenuto dalla stampa*; sulla pagina della società «CTMAVIO» e «controllata» **non compaiono** | [soldionline-ordine2026] **[A, A11]** |
| Cliente, piattaforma, uso | **non risolto**: nessuna fonte li dice | ivi |
| 05-06-2026: prime commesse (circa 1,05 milioni), sottosistemi di bordo di un velivolo a pilotaggio remoto | *sostenuto* | [teleborsa-commesse2026] **[A]** |
| 09-06-2026: 20 % di NIDO, con diritto di salire al 51 % entro 24 mesi. Piattaforma: drone, stazione di ricovero e ricarica, calcolo a bordo, voli oltre la linea di vista con supervisione remota. Usi: ispezione di strade e infrastrutture, condotte e reti, sorveglianza perimetrale | *sostenuto* | [teleborsa-nido2026] **[A, A11]** |
| 10-07-2026: Task Force X (iniziativa NATO, Torre Veneri) con NIDO, GMSPAZIO e CTM Avio: «la sorveglianza continua e la protezione delle infrastrutture critiche» | *sostenuto* | [websim-taskforcex2026] **[A, A11]** |
| 24-07-2026: accordo per acquisire CTMAVIO (9 milioni); 15-09-2026: via libera Golden Power | *sostenuto*; chiusura **NV** | [teleborsa-ctmavio2026]; [maregroup-news] **[A]** |
| 28-07-2026: accordo quadro da 8,3 milioni, oltre 6000 kit motore per velivoli senza pilota | *sostenuto dalla stampa* | [teleborsa-kitmotore2026] **[R]** |
| Linee terrestri o navali; prodotti di percezione; notizie sull'hackathon | **non trovate** | [maregroup-news] |

Link della tabella: [maregroup-ordine2026] https://www.maregroup.it/news/primo-ordine-estero-sistemi-uncrewed · [soldionline-ordine2026] https://www.soldionline.it/notizie/azioni-italia/mare-group-primo-ordine-estero-sistemi-uncrewed · [teleborsa-commesse2026] https://www.teleborsa.it/News/2026/06/05/mare-group-prima-commessa-per-velivoli-a-pilotaggio-remoto-valore-superiore-a-1-milione-di-euro-53.html · [teleborsa-nido2026] https://www.teleborsa.it/News/2026/06/09/mare-group-entra-nel-capitale-di-nido-al-20percent-con-opzione-per-il-controllo-entro-24-mesi-5.html · [websim-taskforcex2026] https://www.websim.it/azioni/small-mid-cap/notizie/mare-group-scelta-dalla-nato-per-la-task-force-x/ · [teleborsa-ctmavio2026] https://www.teleborsa.it/News/2026/07/24/mare-group-acquisisce-ctmavio-e-rafforza-la-filiera-dei-droni-per-aerospazio-e-difesa-17.html · [maregroup-news] https://www.maregroup.it/news/ · [teleborsa-kitmotore2026] https://www.teleborsa.it/News/2026/07/28/mare-group-contratto-da-8-3-milioni-di-euro-per-unita-di-propulsione-uav-13.html

**Lettura (inferenza, non fatto).** Il profilo pubblico è aereo, da ispezione con supervisione remota: la demo più vicina è l'osservazione con un operatore remoto, non il traffico aereo. Ciò che l'utente ha riferito si dice così: «un ordine da circa 1,7 milioni per sistemi uncrewed, annunciato il 21 ottobre 2026».

## E.7 Che cosa dire a una giuria mista, e che cosa no

Frasi di SP §6, riscritte dove l'attacco le ha smentite (C1, C5, C6, C8). **Non rilette da un lettore esterno**: la prova di T-001 (un esterno, dopo 30 secondi, dice che cosa fa il sistema) non è stata eseguita.

**A chi non ha il contesto.**

- *Il problema.* «Chi osserva con una macchina perde di vista le cose: una persona passa dietro un ostacolo, e il rischio è che il sistema si comporti come se non ci fosse più.»
- *Il principio.* «È progettato per dire, di ogni oggetto che ha seguito, se lo vede, se non lo vede ma sa dove può essere, o se non lo sa; e per non dare per libero uno spazio che non ha visto negli ultimi istanti.»
- *Una prova.* «Al computer, con una persona sola e rilevamento senza errori, in 400 passaggi dietro l'ostacolo per ciascuna di 27 configurazioni il sistema l'ha ritrovata con la stessa identità ogni volta. Sappiamo dove cede: se dalla stessa ombra esce un'altra persona mai vista, la scambia sempre; e con un rilevamento mancato su dieci e l'ombra stimata stretta di 20 cm, in 13 passaggi su 4800 la persona nascosta è finita in uno spazio dato per libero.» E: «La regola "mai libero senza aver visto" ha retto a dodici attacchi alla sua logica; nessuna prova l'ha ancora esercitata su immagini vere.»
- *Un limite.* «Finora è provato solo in simulazione, con il sensore fermo, al chiuso, fino a 3 m, con la camera a 1,2 m; non vede il vetro; non è un dispositivo di sicurezza né un dispositivo medico.»

**Al giurato della società.**

- «Una stazione ferma, o una piattaforma uncrewed ferma, monitora un varco per un operatore remoto. Con un'altra uscita, lo stesso contratto dà un avviso a una persona non vedente ferma: lì, oltre il nucleo comune, non è provato niente.»
- «L'operatore vede tre stati con l'età del dato, come le tracce "in coasting" dei dati di sorveglianza. In progetto, per un autopilota: un valore per settore in cui "sconosciuto" non è "libero", il principio con cui gli autopiloti aperti azzerano la velocità verso i settori senza dati.» Sempre «ispirato a».
- «La strada: sensore in moto, altri sensori, più punti di vista, ciascuno con la prova che lo sblocca.»

**Da non dire.**

| Non dire | Perché | Al suo posto |
|----------------------|---------------------------|----------------------|
| «conforme a», «compatibile con» una norma | nessuna è stata applicata | «ispirato a» |
| «detect and avoid» | nelle norme è il traffico con equipaggio, a chilometri | «percezione per la navigazione sicura a corto raggio» |
| «validato», «R8 garantito», «bassa latenza», «funziona in movimento» | VER §4; latenza nota circa 155 ms contro la soglia di 150 | «provato solo in simulazione, a sensore fermo» |
| «via libera», «Go», «libero» da solo | il sistema non autorizza; «libero» è «suolo visto libero» (`f7-estensione/07-rovesciatore/CONSEGNA.md`, *preliminare*) | «nessun ostacolo osservato fino a d metri» |
| «orientamento» per il secondo profilo; «dispositivo medico»; «sostituisce il bastone» | C6; secondo addendum | «avviso di presenza per una persona non vedente ferma»; a voce: «per chi cammina non è provato niente» |
| «drone in volo stazionario simulato dal treppiede» | un drone in volo trasla: bastano 3,4 cm/s non compensati per i falsi a 2 m (MP §2a: conto) | «su una piattaforma ferma è lo stesso caso; in moto non è provato» |
| «UAV» o «drone» come ambito; «rileva detriti od oggetti estranei» | la traccia non li nomina; sotto 7 cm di quota non vede | le parole della traccia; «non osservabili» |
| «RA», «TA», «ACAS», «ABAR», «anti-bird strike», «fail-safe»; «minaccia», «bersaglio», «On-Boresight» | il prototipo non prescrive manovre e non comanda; lessico di puntamento, fuori ambito (D9, *preliminare*) | livelli nominati da ciò che chiedono; «avvicinamento diretto»; «priorità di rischio di collisione» |

## E.8 La strada degli sviluppi, con la prova che sblocca ogni tappa

Ogni tappa è «non verificata» finché la sua prova non passa. Le soglie sono quelle dei file.

| Tappa | Aggiunge | Prova che la sblocca | File |
|--------------|-----------------|------------------------------|-----------|
| 0. Sensore vero, fermo | filtri della camera spenti, autoverifica all'avvio | pannello sul suolo segnato col nastro, 150 fotogrammi: **0 celle «libero» dentro l'ombra vera**; poi le misure sull'hardware (circa un'ora e quaranta in due) | VER §3, §6 |
| 1. Avviso sonoro con persone | la prova con persone | tre persone bendate **ferme**, soglia «≥ 54 su 60» (che cosa si conta va fissato prima) | V2 §6; rinviata oltre le 14 ore (`f8-continuita/01-requisiti/CONSEGNA.md`, *preliminare*) |
| 2. Sensore che ruota da fermo | giroscopio tarato all'avvio; sincronia | dieci rotazioni di 30° in circa 1 s: muro o persona ferma «in movimento» in **non più del 10 %** (oggi, dopo 10°, 96–100 %: V2 §6). Il conto: regge fino a 20 ms di ritardo, 15 % a 33 ms, 83 % a 67 ms | MP §4 |
| 3. Piattaforma che avanza piano | posa da ruote e giroscopio o da odometria visuale; piano del suolo come in C7 | 2 m a 0,3–0,5 m/s lungo un muro: falsi ≤ 10 %, distanza entro il 6 %; con ±2° d'inclinazione una scatola di 15 cm a 2 m resta «occupato» 5 volte su 5; nessun «libero» falso | MP §4; ATT, C5, C7 |
| 4. Sensore indossato | odometria visuale-inerziale; **al petto, non sulla testa** (sincronia richiesta 27 ms contro 5,6 ms: conto) | le prove 2 e 3 indossando il sensore, poi la 1 in cammino | MP §2d, §3 |
| 5. Altri sensori, 10–40 m | LiDAR per la portata (40 m al 10 % di riflettività: [livox-mid360] **[A]**), radar per la velocità, termico come etichetta | rumore misurato a 10–30 m; elementi mobili e occlusioni rimisurati a quella scala con la fascia di C4 | SP §5; Q §2b |
| 6. Quota (ostacoli sospesi: ala, carico) | stato di un punto letto nell'immagine di profondità corrente; «libero fino a quota h» | in corso in f7 (*preliminare*): 0 falsi liberi su 576 000 punti, scena ferma; mancano le prove dinamiche e con buchi a chiazze | TR7, V-002, V-003, K-106 |
| 7. Più punti di vista o veicoli | riferimento e orologio comuni; fusione prudente | due sensori fermi con viste incrociate: la zona nascosta a uno e vista dall'altro **si libera cella per cella, senza un «libero» falso** | SP §5 |
| 8. Valore per settore verso un autopilota | il messaggio; la causa «collegamento» | su registrazioni: **mai** un settore non osservato con una distanza valida, mai un valore oltre la prima cella non libera | Q, `esperto-dominio-1`; SP §3.1 |
| 9. Avviso di avvicinamento | tempo e distanza al massimo avvicinamento rispetto a un punto protetto dichiarato | su 30 avvicinamenti diretti l'avviso mai a meno di 0,5 s dal contatto; su 30 passaggi a 1,5 m di lato al più 3 scatti | D9 §5 (*preliminare*) |
| 10. Prodotto | qualificazione regolatoria | parere di un professionista: fuori dallo sciame | §E.4 |

Link della tabella: [livox-mid360] https://www.livoxtech.com/mid-360/specs

**Non promettere, a nessuna tappa** (MP §4): una mappa, una precisione di localizzazione, oltre 0,5 m/s, il volo, il sensore sulla testa, una soglia del nucleo valida in moto.

## E.9 Dove i file dicono cose diverse

- **Volo stazionario.** Q §4 lo dà per simulabile dal treppiede; SP §2 lo esclude, MP §2a lo smentisce, e R7 (critica 7) trova falsa la frase nel PDF v0.3. Vale l'esclusione.
- **Controllata dell'ordine.** Q §1 scrive «tramite la controllata CTMAVIO»; la pagina della società, riaperta oggi, non la nomina; la stampa sì. In §E.6 sono due righe distinte.
- **Durata del «previsto».** 0,6–0,7 s (V2 §1); «1–1,6 s» (Q §2c, scritto prima di V2); 0,40–0,53 s (VER, K-004); «circa mezzo secondo» (VER §5). Le riporto tutte: f8 sta rivedendo il punto.
- **Stati in uscita.** «Tre stati» (V2; VER §5); ma le uscite per traccia sono cinque, con «non confermato» e «identità ambigua» (ATT, S5). Alla giuria tre condizioni; nel dettaglio cinque.
- **Righe che cambiano in moto.** «Almeno 7 su 9» in testa ad ATT, «9 su 9» nella sua tabella (S6a).
- **Lo sconosciuto nella sicurezza industriale.** D7 (C3) cita «treated as occupied for SSM purposes»; oggi lo strumento restituisce «classified as unknown and treated as occupied until the system can determine it to be otherwise». Stesso senso; da ricontrollare sul testo grezzo.
- **Radar su quadrirotore.** Q §2b scrive «errori laterali fino a 0,9 m»; il riassunto, oggi, dà errori medi fino a 0,15 / 0,93 / 0,87 m sui tre assi [mandaokar2026] https://arxiv.org/abs/2608.01855 **[A, A11]**, preprint.
- **Cuneo d'ombra con ostacoli bassi.** «Sbaglia dal lato prudente» (D7, C7) contro «nasconde ciò che si vede» (ruolo delle nuvole di punti, f7): è la contraddizione K-102, aperta.

---

## File letti

**Per intero:** `ADDENDUM_UTENTE.md`; `CONTRATTO.md`; V2; VER; `f3/fonti/FONTI_VERIFICATE.md`; Q; SP; MP; ATT con `risultati_spec.txt` e `risultati_spec2.txt`; R7; D7 con `risultati_griglia_densa.txt`; TR7; D9 con `prove/risultati_p7.txt` e `prove/risultati_p8_p9_p10.txt`. Nella radice del progetto: `regole_challenge.md`; `proposta/VERSIONI.md`.

**In parte:** AUD (ipotesi 10–12, §2, §3); `f2/05-selezione/SELEZIONE.md` (§2, §6); `f2/03-triage/TRIAGE.md` (K-008); `f7-estensione/05-esperto-dominio/risultati_osservabilita.txt`; `f8-continuita/07-ricercatore/CONSEGNA.md` (punti 5–6) e `FONTI.md` (§4–§5); `f8-continuita/01-requisiti/CONSEGNA.md` (riga dei tagli); `f9-preproposta/09-interfacce/CONSEGNA.md` (critiche 2–12); `f9-preproposta/11-pianificatore/CONSEGNA.md` (tagli); `f10-dati/CONTRATTO_DATI.md` (ambito); `proposta/proposta_sciame.tex` (righe 48, 90–97, 136–195, conteggi); `promptMare.txt` (solo conteggio).

**Non letti:** misure e controprove di f4 (le cifre vengono da V2 e VER), f1, il torneo di f2, f3 salvo le fonti, gli altri ruoli di f7–f10, `prepropostaEsterna.md`, i PDF.

**Lunghezza, misurata.** Corpo (fino a §E.9): circa 4670 parole, cioè 6,0 pagine sul metro di 775 parole a pagina usato dallo sciame. Composto con pandoc e xelatex (A4, corpo 10, margini 1,8 cm) fa **10 pagine**: le otto tabelle, con celle lunghe, occupano molto più del testo. Scostamento dichiarato; se serve tagliare, le prime candidate sono §E.9 e la tabella di §E.4.

## Chiavi di riferimento usate

Chiavi provvisorie. Dove gli autori non stanno nei file dello sciame né sulla pagina letta, la chiave porta l'ente o il sito.

- **Società** (link in §E.6): [maregroup-ordine2026], [soldionline-ordine2026], [teleborsa-commesse2026], [teleborsa-nido2026], [websim-taskforcex2026], [teleborsa-ctmavio2026], [teleborsa-kitmotore2026], [maregroup-news].
- **Autopiloti e sorveglianza** (link in §E.3): [px4-collisionprevention], [px4-obstacledistance], [eurocontrol-asterix062] (pagina ufficiale, non aperta: https://www.eurocontrol.int/publication/cat062-eurocontrol-specification-surveillance-data-exchange-asterix-part-9-category-062), [imo-msc192].
- **Sicurezza industriale:** [marvel2017] = Marvel e Norcross, «Implementing Speed and Separation Monitoring in Collaborative Robot Workcells», Robotics and Computer-Integrated Manufacturing 44, 144–155, DOI 10.1016/j.rcim.2016.08.001 (in linea 2016, fascicolo 2017); [vu2020] = Clara Vu, «Advanced vision and the future of robot safety in manufacturing», The Robot Report, 1° luglio 2020; [iso-ts-15066], [iso-10218-2], [iso-13855] (non letti; nessun link nei file: **manca**).
- **Aviazione e mare:** [eurocontrol-acasguide], [faa-aim-rwsl], [imo-colreg7] (link in §E.3); [easa-sora25] (link in §E.4); [rtca-do365] https://standards.globalspec.com/std/14562761/do-365c; [eurocae-ed275] https://standards.globalspec.com/std/14356966/eurocae-ed-275; [astm-f3442] https://store.astm.org/f3442-25.html.
- **Regole europee e italiane:** [ue-2019-947], [ue-2019-945] (pagina d'ingresso: https://www.easa.europa.eu/domains/drones-air-mobility/rules-standards); [easa-categoria-aperta] https://www.easa.europa.eu/en/the-agency/faqs/open-category; [ue-2021-664] https://eur-lex.europa.eu/eli/reg_impl/2021/664/2026-02-22/eng/pdf; [ue-2023-1230] https://eur-lex.europa.eu/eli/reg/2023/1230/corrigendum/2023-07-04/oj/eng; [iso-3691-4] https://genorma.com/en/standards/en-iso-3691-4-2023; [imo-mass] https://www.dnv.com/news/2026/imo-mcs-111-new-mass-code-adopted/; [ue-2017-745] (link in §E.4); [ue-2021-821] https://eur-lex.europa.eu/EN/legal-content/summary/dual-use-export-controls.html; [legge-185-1990] https://www.esteri.it/it/ministero/struttura/uama/; [verfassungsblog-aiact] https://verfassungsblog.de/the-ai-act-national-security-exception/; [dpr-495-1992] (art. 162, comma 5; nessun link nel file che lo cita: **manca**).
- **Ambito aerospaziale e industriale** (link in §E.1): [iata-gse2022], [aviationweek-ispezioni], [flightsafety-fod].
- **Ricerca:** [orzechowski2018], [nuss2018] (link in §E.3); [koschi2021] = Koschi e Althoff, IEEE T-IV 6(2), 249–265, 2021, DOI 10.1109/TIV.2020.3017385 (da `FONTI_VERIFICATE.md`); [balch2019] = Balch, Martin, Ferson, «Satellite conjunction analysis and the false confidence theorem», Proc. R. Soc. A 475, 20180565 (2019); [mandaokar2026] = Mandaokar e Rinner, «RADAR Perception for Dynamic Obstacle Avoidance onboard small-scale Quadrotor UAVs», arXiv 2608.01855 (preprint).
- **Ausili per persone non vedenti:** [kayukawa2019] = Kayukawa e altri, «BBeep», CHI 2019 (link in §E.2); [martinez2014] = Martinez e altri, ICCHP 2014, LNCS, pp. 128–135; [lupu2020] = Lupu e altri, Sensors 20(20):5821, 2020 (link non riportato in `FONTI_VERIFICATE.md`: **manca**).
- **Sensori:** [livox-mid360] (link in §E.8).
