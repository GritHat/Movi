# Schede di traduzione — percezione-challenge, f2/01 (`sciame-logico`)

**In testa.** Nessun cambio di stato e nessuna prova miei: gli stati sono quelli dichiarati dagli autori. Letti il contratto, le nove `CONSEGNA.md` e, per gli esiti, le `PREVISIONI.md` (creativo e rovesciatore per intero, le altre per righe d'esito). Venti schede, nessuna fusione, nessuna correzione. **Limite violato, la lunghezza:** 4 900 parole circa (30 800 caratteri, misurati con `wc`), cioè quattro pagine solo a corpo piccolo e cinque a corpo normale; la coda (650 parole) supera la mezza pagina. Ho preferito non togliere numeri e condizioni che gli autori devono firmare.
**Legenda.** Origine = `f1/<cartella>/CONSEGNA.md`. [aut.] = il controllo condivide con l'idea autore, modello linguistico e modello simulato. n.e. = non eseguito. [trad.] = controesempio non scritto dall'autore, ricavato dal traduttore dai vincoli dell'idea. **Non riportati:** i ripieghi «se l'ipotesi di fattibilità è falsa» (salvo dove sono citati) e le fonti con i link: restano nelle consegne d'origine.

### `visione-1` · sciame-visione, `c85dbcc51ea6` · oggetto: sensori, scena, ordine della catena · tipo: soluzione
- **Enunciato.** Una camera RGB-D frontale (tipo D455: 87°×58°, otturatore globale, IMU). Percorso critico per fotogramma: profondità → piano del suolo → punti sopra il suolo → griglia a tre stati (libero osservato, occupato osservato, sconosciuto = mai visto o senza ritorno) → misure 3D. Percorso asincrono: rilevatore «nano» con maschere + tracciatore (BoT-SORT o ByteTrack) per i mobili; classe e identità si attaccano alle tracce. Ordine: rete → associazione → Kalman → decisione. Dominio: interni o ombra, 0,6–6 m.
- **Rischi.** Vetro e nero restano «sconosciuto»; fuori dagli 87° «non osservato»; AGPL-3.0 (alternativa RF-DETR); moto proprio; sfocatura se sulla testa.
- **Ipotesi critica → controesempio.** La profondità copre R2 senza classi e il percorso critico regge su CPU → vetro, oggetti bassi; portatile oltre 80 ms.
- **Verifica, esito.** P1 (0 su 7 categorie d'ostacolo fra le 80 classi COCO): regge [fonte riassunta, aut.]. P5 (latenza; smentita oltre 80 ms): non risolta, n.e. Cinque oggetti fuori da COCO (5/5 dalla profondità, ≤ 1/5 dal rilevatore): n.e.
- **Vicina a** `ricercatore-1`, `lidar-1`, `nuvole-punti-2`, `requisiti-1`; differisce per: due percorsi (critico geometrico, asincrono con rete) e ordine della catena.

### `visione-2` · sciame-visione, `c85dbcc51ea6` · oggetto: ciclo di vita delle tracce, regione prevista · tipo: regola di decisione
- **Enunciato.** Ogni traccia esce OSSERVATO, PREVISTO o SCONOSCIUTO. Senza rilevamento si legge la profondità lungo il raggio verso la posizione prevista: più vicina della previsione (meno un margine) → occlusore → PREVISTO (sola predizione, ellisse che cresce); uguale o più lontana → traccia chiusa; non valida → SCONOSCIUTO. PREVISTO scade quando il raggio al 95 % supera 1 m (1,0–1,4 s per un pedone); poi la zona dietro l'occlusore è «possibile presenza», mai libera. Ritorno: cancello di Mahalanobis + aspetto (ReID). Nessuna rete amodale o generativa.
- **Rischi.** Profondità allineata all'RGB; occlusori trasparenti o sottili; camera ferma o moto proprio compensato; chi si ferma dietro il pannello scade a SCONOSCIUTO (voluto).
- **Ipotesi critica → controesempio.** Il raggio verso il punto previsto distingue «nascosto» da «assente» → due persone che si incrociano dietro il pannello.
- **Verifica, esito.** P3 (raggio al 95 %, σ_a 0,5–1,0 m/s²): regge, soglie non toccate; valore atteso dell'autore corretto da 1,5–3 s a 1,0–1,4 s [modello di moto assunto, aut.]. P6 (20 passaggi; smentita a ≤ 15 stati giusti): non risolta, n.e.
- **Vicina a** `tracciamento-2`, `nuvole-punti-1`, `kalman-2`, `ricercatore-2`; differisce per: prova sul solo raggio verso il punto, chiusura immediata, soglia 1 m.

### `lidar-1` · sciame-lidar, `985ccd9bca46` · oggetto: sensori · tipo: decisione
- **Enunciato.** Un solo sensore frontale: camera stereo attiva con IMU (D455, D435i, Gemini 335, o quella già posseduta), circa 87°×58°, 30 fps. Fuori campo è «sconosciuto» per costruzione; i 360° si dichiarano come limite. 42–56 pixel su una persona a 4 m contro 1,3 zone di un ToF 8×8; un cavo USB, nessuna interferenza, nessuna calibrazione estrinseca.
- **Rischi.** Niente retro; portata utile 3–6 m; col vetro una griglia a lancio di raggi segna «libero» una porta; nero a portata dimezzata; sole pieno non verificato; 330–417 $.
- **Ipotesi critica → controesempio.** I pixel validi bastano a 4 m e c'è il budget → persona con pantaloni scuri sotto il 50 % di pixel validi; budget zero senza camera (la proposta cade, resta `lidar-2`).
- **Verifica, esito.** P6 (schede: portata e pixel): regge sulla soglia; prezzo e sole non risolti [dichiarazioni dei costruttori, in parte da riassunto]. P10 (≥ 70 % di pixel validi): non risolta, n.e.
- **Vicina a** `visione-1`, `nuvole-punti-2`, `ricercatore-1`, `requisiti-1`; differisce per: parla del solo sensore.

### `lidar-2` · sciame-lidar, `985ccd9bca46` · oggetto: sensori (estensione a 360°) · tipo: decisione condizionale
- **Enunciato.** Se i 360° servono davvero: un LiDAR 2D rotante (RPLIDAR C1 o LD19, 70–80 $; 360° a 10 Hz, 5000 punti/s, 12 m, 6 m sul nero) più la camera di `lidar-1`. Il lancio di raggi dà per direzione «occupato», «libero fin qui», «sconosciuto oltre»; avvisa di ciò che arriva da dietro senza classificarlo. Con 420 $ in più: Unitree L2, 3D a 360°, 5,55 Hz.
- **Rischi.** Un solo piano (niente gradini, tavoli, ostacoli bassi o sospesi); 8 punti su una persona a 5 m, 2 su una gamba; vetro invisibile; giro di 100 ms: a 90°/s la scansione a 5 m si deforma di 0,8 m; addosso il corpo copre circa metà giro (non verificato). Rende meglio fermo su un palo.
- **Ipotesi critica → controesempio.** Un piano basta per i mobili attorno → ostacolo basso o sospeso; portatore che ruota senza correzione IMU.
- **Verifica, esito.** P7 (schede) e P8 (conto dei punti): reggono [schede dei costruttori, aut.]. P11 (≥ 4 punti nel 90 % dei giri a 5 m): non risolta, n.e.
- **Vicina a** `nuvole-punti-2` (LD19 come aggiunta); differisce per: qui il LiDAR è l'oggetto della proposta, con i limiti da indossato.

### `nuvole-punti-1` · sciame-nuvole-punti, `dfac83300259` · oggetto: scena, legame cella–traccia · tipo: rappresentazione e regola
- **Enunciato.** A ogni fotogramma ogni cella di una griglia polare egocentrica (settori di 1°, 0,1 m, fino alla portata utile) riceve uno di quattro stati: *libero osservato* (suolo visto alla quota attesa), *occupato osservato* (primo ritorno fra 0,07 e 2 m di quota), *in ombra* (oltre il primo ritorno), *non osservato* (fuori campo, nessun ritorno, suolo mancante). Memoria = ultimo stato con l'età: «libero» scade dopo 0,7 m / 1,4 m/s = 0,5 s; «occupato» resta *ricordato* finché non è smentito. Traccia con posizione prevista in ombra o fuori campo → *prevista* (oltre soglia di covarianza *persa*, segnalata); in *libero osservato* per tre fotogrammi → chiusa. Log-odds facoltativa, solo come filtro sull'occupato. Niente odometria; 2 ms a fotogramma.
- **Rischi.** Servono gravità (IMU) e altezza del sensore; rampe (il suolo in salita diventa ostacolo); testa che ruota (memoria da compensare o scade); soglia di 7 cm fino a circa 3 m (calcolo).
- **Ipotesi critica → controesempio.** Suolo riconoscibile alla quota attesa, ombra geometrica corretta → vetro, rampa, oggetto che esce dall'ombra dal lato opposto.
- **Verifica, esito.** P-np1a (regola della bozza: 173 «libero» falsi in ombra su 552, più 92 da visibile; regola proposta: 0) e P-np1b (2,0 ms): reggono [simulazione 2D senza rumore, aut.]. Registrazione vera (smentita con ≥ 1 fotogramma «libero» sulla cella nascosta): non risolta, n.e.
- **Vicina a** `rovesciatore-2`, `visione-1`, `visione-2`; differisce per: quattro stati, «libero» = suolo visto, memorie diverse per libero e occupato, regola dei tre fotogrammi.

### `nuvole-punti-2` · sciame-nuvole-punti, `dfac83300259` · oggetto: sensori · tipo: decisione
- **Enunciato.** Una sola camera di profondità densa (almeno 240×180; meglio RGB-D stereo 640×480, classe D435, 87°×58°) inclinata verso il basso, con IMU; fuori dal suo campo tutto è «non osservato»; il 360° non si promette. Se la demo lo vuole, lo aggiunge un LiDAR 2D (LD19: 0,8°, 5–13 Hz, 12 m), che vede i mobili su un piano (8,9 fasci su un pedone a 4 m), non il terreno. Terreno risolto fino a 3 m (impronta 1,8 cm contro 87 cm del ToF 8×8); 7 756 pixel sul pedone a 4 m contro 5,4 zone.
- **Rischi.** Lati e retro ignoti; stereo su pareti uniformi e al sole (non verificato). Con tre *camere* ToF già possedute: una avanti per il terreno, due ai lati per i soli ostacoli.
- **Ipotesi critica → controesempio.** La camera densa separa suolo e ostacoli bassi → gradino da 15 cm a 2 m le cui quote non si separano.
- **Verifica, esito.** P-np2 (calcolo sulle schede): regge [aut.; alcune fonti da riassunto]. Gradino a 2 m (due mode distanti più di 3 deviazioni standard): n.e.
- **Vicina a** `lidar-1`, `visione-1`, `ricercatore-1`, `requisiti-1`; differisce per: camera inclinata verso il basso, risoluzione minima dichiarata.

### `tracciamento-1` · sciame-tracciamento, `992c41c8860e` · oggetto: ciclo di vita delle tracce · tipo: regola di decisione
- **Enunciato.** Quattro stati, in uscita con la posizione: **tentativa** (rilevamento non associato; nessuna indicazione propria, l'ostacolo resta nella mappa di occupazione); **confermata** (3 rilevamenti su 5: «osservato»); **in volo cieco** (nessuna misura: velocità costante, q circa 0,5 m²/s³, «previsto», raggio al 95 % che cresce); **persa** (raggio oltre 1,5 m o tetto di tempo: solo «zona incerta», mai «libero»). Riaggancio: porta di Mahalanobis al 99 % e ungherese; con più candidati decidono classe, dimensione e aspetto; se non decidono, identità nuova, dichiarata.
- **Rischi.** Serve un riferimento fisso; q e tetti da ritarare su camminate vere; a 3 s la porta ha raggio circa 7,3 m: con più oggetti la geometria non identifica.
- **Ipotesi critica → controesempio.** q = 0,5 calibra la porta anche su pedoni veri → due persone che si incrociano dietro il pannello (prova 5c, non risolta).
- **Verifica, esito.** `simA.py` (smentita se copertura < 90 % a T ≤ 3 s): minimo 98,6 %, regge. Smentite le attese dell'autore su orizzonte (1,5–3 s → circa 1,2 s) ed errore a 1 s (0,53 m contro ≤ 0,5) [un solo oggetto, nessun sensore, aut.].
- **Vicina a** `kalman-2`, `visione-2`, `ricercatore-2`; differisce per: stato «tentativa» (3 su 5), q = 0,5, regola di riaggancio con più candidati.

### `tracciamento-2` · sciame-tracciamento, `992c41c8860e` · oggetto: chiusura delle tracce · tipo: regola di decisione
- **Enunciato.** Per ogni traccia non osservata la mappa di profondità dice la causa: (a) superficie più vicina davanti alla posizione prevista → **nascosto**, l'esistenza non cala; (b) fuori campo o portata → **fuori campo**; (c) profondità non valida → **sensore cieco**, segnalato (R6); (d) il sensore vede attraverso e non c'è niente → evidenza negativa. Il conto si fa sulla massa d'incertezza (filtro di Bernoulli, circa 200 particelle per traccia in volo cieco), non sul punto medio. Tetto di 10 s, poi «zona incerta».
- **Rischi.** L'ombra reale viene da una profondità rumorosa; il modo «sosta» va giustificato.
- **Ipotesi critica → controesempio.** L'ombra calcolata è giusta → ombra sbagliata di 20 cm; due oggetti.
- **Verifica, esito.** `simB.py` (smentita se identità tenuta < 80 % con sosta, o se il punto medio da solo supera l'80 %): 100 % e 0 %, regge; fantasma in zona visibile 0,06–0,07 s contro 2,0 s [aut.; indipendenza debole: il modello ha un modo «sosta» come lo scenario].
- **Vicina a** `creativo-2`, `visione-2`, `nuvole-punti-1`, `rovesciatore-2`; differisce per: quattro cause nominate, Bernoulli, tetto di 10 s.

### `kalman-1` · sciame-kalman, `21d3813ca7e1` · oggetto: stimatore, catena, decisione «mobile» · tipo: soluzione
- **Enunciato.** Un Kalman lineare a velocità costante per traccia, stato [x, y, vx, vy] sul piano del suolo, in un riferimento stabilizzato in rotazione dal giroscopio (e in traslazione, se c'è odometria), a valle di rilevamento e associazione e a monte della decisione. Niente massa né accelerazione. «Mobile» = prova sulla covarianza (v'·Pv⁻¹·v > 9,21, chi quadrato al 99 %), non soglia fissa. Gravità = classe di taglia × velocità di avvicinamento. A 15 Hz e 5 cm: velocità a 0,2 m/s; pedone a 1,2 m/s mobile in 0,20 s; ostacolo fermo mobile nello 0,0 % del tempo (500 prove); sotto circa 0,62 m/s la prova non scatta.
- **Rischi.** IMU con marche temporali allineate; senza traslazione ogni muro è «mobile» il 100 % del tempo; centroide spostato in occlusione parziale (non simulato). Se il tempo è poco: sensore fisso o portatore fermo, senza compensazione.
- **Ipotesi critica → controesempio.** Rumore gaussiano isotropo di 5 cm (ipotesi dell'autore) → muro ripreso ruotando la testa che risulta «mobile».
- **Verifica, esito.** Simulazione (errore > 1 m senza compensazione, < 0,3 m col giroscopio): 1,49 e 0,25 m, regge [aut., nessun errore di associazione]. Muro per 30 s (smentita se «mobile» oltre il 10 % del tempo): n.e. Massa: non osservabile, dimostrato nel modello del punto materiale con forza ignota.
- **Vicina a** `tracciamento-1`, `requisiti-1`; differisce per: stato e riferimento fissati, prova «mobile» sulla covarianza.

### `kalman-2` · sciame-kalman, `21d3813ca7e1` · oggetto: regione prevista, accettazione · tipo: regola e criterio di accettazione
- **Enunciato.** Tre stati per traccia: «osservato» (aggiornata in questo ciclo, innovazione in porta); «previsto» (sola predizione; si comunica l'area al 95 %, non un punto); «perso» quando il raggio al 95 % supera r_max (proposta: 1,5 m, circa 1,6 s) o l'innovazione alla ricomparsa è fuori porta: la zona torna «non osservata», mai «libera». Q si tara sul NIS (q = 0,2 m²/s³ in simulazione) e si accetta solo se, su 30 occlusioni registrate di 1–2 s, la misura alla ricomparsa cade nel cerchio al 95 % almeno 26 volte.
- **Rischi.** Un'ora di registrazioni; il NIS a un passo non garantisce la copertura a più secondi (0,90–0,94 sotto il 95 % nominale); q a occhio (0,01) copre il 42 % a 2 s.
- **Ipotesi critica → controesempio.** Il 26/30 separa le tarature (passa nel 91 % dei casi con copertura 0,92, nel 10 % con 0,75) → pedone vero che sosta o svolta; scambio d'identità alla ricomparsa.
- **Verifica, esito.** Simulazione (copertura in [0,88; 0,99], smentita sotto 0,85): 0,90–0,94, regge [un solo modello di pedone, aut.]. Le 30 occlusioni: n.e.
- **Vicina a** `visione-2`, `tracciamento-1`, `ricercatore-2`; differisce per: criterio 26/30 senza verità di riferimento, q = 0,2.

### `requisiti-1` · sciame-requisiti, `b8262bfed263` · oggetto: ambito (MVP), catena · tipo: decisione d'ambito
- **Enunciato.** «Taglio a otto»: un solo sensore di profondità frontale e fermo copre R1–R8, senza 360°, massa, accelerazione, gerarchia, MLE/MAP e mappa del terreno. Catena: rilevamento geometrico sulla profondità → Kalman a velocità costante → tre stati per traccia e per settore → audio (direzione, distanza, stato) e schermo a tre colori → contatore della latenza. Fuori campo «non osservato», mai «libero». Soglie proposte (ipotesi): R1 ≥ 9/10 entro 1 s; R2 5/5 entro 15 cm; R3 ≥ 8/10; R4 0 fotogrammi «osservato» a soggetto nascosto; R5 ≤ 300 ms; R6 entro 1 s; R7 p95 ≤ 150 ms, ≥ 15 fotogrammi/s senza GPU; R8 0 «libero» su settore non osservato, più l'invariante nel codice.
- **Rischi.** Campo 87–120°; soglie non verificate; ambiguità D1–D7 aperte (hardware, giuria, dal vivo o video, dislivelli).
- **Ipotesi critica → controesempio.** Le regole non chiedono ciò che è tagliato (0 occorrenze nelle 6 righe: verificato) → una frase delle regole non coperta; «ostacolo» include i dislivelli.
- **Verifica, esito.** P1 (7 sensori: nessun campo orizzontale ≥ 130°; caso limite Femto Bolt, 120° esatti): regge [schede in parte da riassunto; il falsificatore dichiarato misura il campo dei sensori].
- **Vicina a** `visione-1`, `ricercatore-1`, `rovesciatore-1`, `rovesciatore-2`; differisce per: sensore fermo, rilevamento senza rete, soglie R1–R8.

### `requisiti-2` · sciame-requisiti, `b8262bfed263` · oggetto: demo · tipo: procedura
- **Enunciato.** Una scena di circa 3 minuti in cinque atti: (1) campo mezzo coperto → «non osservato» (R8); (2) ostacolo fermo (R2, R5); (3) persona che attraversa, latenza a schermo (R1, R5, R7); (4) passa dietro un pannello di circa 1 m → «previsto» → stessa traccia (R3, R4); (5) si ferma dietro il pannello, o si copre il sensore → «affidabilità persa» (R6, R8).
- **Rischi.** Larghezza del pannello da tarare sul modello del moto; 1,3 m/s non verificato.
- **Ipotesi critica → controesempio.** Il transito dietro 1 m dura meno della finestra del «previsto» → pedone lento o q diverso [trad.].
- **Verifica, esito.** P2 (2σ supera 1 m dopo 1,30 / 1,07 / 0,87 s per q = 0,25 / 0,5 / 1,0 m²/s³; forma chiusa e Monte Carlo entro l'1,1 %): regge [stesso modello e parametri dell'enunciato: vale per l'algebra, non per un pedone vero].
- **Vicina a** `creativo-3`, `rovesciatore-2` (cinque momenti); differisce per: atti legati uno a uno a R1–R8, pannello di 1 m.

### `ricercatore-1` · sciame-ricercatore, `3fff79e9c3ea` · oggetto: sensori, scena, grandezze · tipo: soluzione
- **Enunciato.** Una camera RGB-D frontale con IMU al posto di tre ToF; ostacoli dalla profondità in una griglia a tre stati libero/occupato/sconosciuto; mobili da un rilevatore leggero più associazione tipo ByteTrack/OC-SORT. Fianchi e spalle «sconosciuto», mai liberi. La massa si toglie: restano ingombro misurato e classe, con il peso tipico della classe dichiarato come ipotesi a priori.
- **Rischi.** Campo frontale; sole non risolto (Luxonis «<2% outdoors», Orbbec «Indoor»); licenza del rilevatore; circa metà delle fonti non aperta.
- **Ipotesi critica → controesempio.** Nessun ToF rende valida l'idea dei tre sensori → un ToF con campo orizzontale ≥ 130° e ≥ 4 m al sole.
- **Verifica, esito.** P1 (schede): non risolta (campo: nessuno trovato; sole: disaccordo) [fonti esterne, ricerca non esaustiva]. Senza camera di profondità: demo a camera fissa.
- **Vicina a** `visione-1` (quasi coincidente), `lidar-1`, `nuvole-punti-2`; differisce per: peso tipico per classe come a priori, nessun percorso asincrono nominato.

### `ricercatore-2` · sciame-ricercatore, `3fff79e9c3ea` · oggetto: stimatore in occlusione, modelli appresi · tipo: soluzione
- **Enunciato.** Kalman a velocità costante; tre stati per traccia: «osservato» finché c'è la misura; «previsto» in occlusione, con regione che cresce; «sconosciuto» quando la regione supera una soglia o dopo un tempo massimo, e parte il segnale R6. Soglia e tempo non fissati: da misurare. SAM 2 e trasformatori di visione solo in asincrono (classe, riaggancio), mai a decidere un allarme. Confidenze calibrate a posteriori su una registrazione propria.
- **Rischi.** Prova da camere fisse dall'alto (ETH/UCY, 2020); con camera indossata si somma il moto proprio.
- **Ipotesi critica → controesempio.** Velocità costante adeguata per occlusioni brevi → svolta dietro l'ostacolo (nessun modello confrontato la prevede).
- **Verifica, esito.** P2(a) (a 4,8 s, errore medio/finale: 0,39/0,83 m contro 0,44/0,91 del miglior appreso deterministico; 0,32/0,60 un generativo): regge. P2(b) (nessuna misura dei modelli video su Jetson o CPU): regge solo come assenza di prova contraria [letteratura esterna, non esaustiva].
- **Vicina a** `visione-2`, `kalman-2`, `tracciamento-1`; differisce per: soglie non fissate, calibrazione a posteriori, divieto d'allarme ai modelli appresi.

### `creativo-1` · sciame-creativo, `e30f9e2dd4d7` · oggetto: feedback · tipo: soluzione
- **Enunciato.** «Il libero costa energia». Entra lo stato per settore (libero osservato, occupato a distanza d, previsto con σ, sconosciuto) con l'età dell'ultimo fotogramma. Esce un canale audio o aptico: battito sommesso ogni 0,5 s solo se il settore davanti è osservato libero e il fotogramma è fresco; occupato = clic nitidi, ritmo ∝ 1/d; previsto = stesso ritmo, suono sfocato, durata ∝ σ; sconosciuto = battito sospeso più ronzio grave. Il battito viene da un processo separato che si spegne da solo senza dati freschi.
- **Rischi.** Il suono continuo copre l'udito ambientale (ripiego: vibrazione al polso); assuefazione.
- **Ipotesi critica → controesempio.** I timbri si distinguono e il battito muore col guasto → riconoscimento sotto l'80 %; battito che continua a percezione sospesa.
- **Verifica, esito.** P-creativo-1 (3 persone bendate, ≥ 54/60, smentita < 48/60; percezione sospesa: battito muto entro 1 s): non risolta, n.e.

### `creativo-2` · sciame-creativo, `e30f9e2dd4d7` · oggetto: stimatore in occlusione, regione prevista · tipo: soluzione
- **Enunciato.** «Il sottomarino perduto»: la traccia nascosta diventa 300–1000 particelle (posizione, velocità, modo fermo o in moto); a ogni fotogramma, nelle celle che la profondità vede libere, le particelle pesano (1−Pd). Escono P(ancora nell'ombra) e la regione dove può essere. Regola: il «previsto» non si disegna mai dove si osserva libero. 1000 particelle a 15 Hz sotto l'1 % di un core (stima).
- **Rischi.** In 2D serve la visibilità per raggio; due bersagli che si scambiano nell'ombra.
- **Ipotesi critica → controesempio.** Le celle viste libere sono libere → falso «libero» (superficie scura o lucida) che uccide l'ipotesi giusta.
- **Verifica, esito.** P-creativo-2a (sosta dietro un occlusore di 2 m; massa in celle osservate libere a 3 s; smentita se Kalman < 50 % o particelle > 25 %): Kalman 100 %, particelle 0,11 %; senza evidenza negativa 90,1 % (notato dopo): regge [simulazione 1D, aut., nessun dato reale].
- **Vicina a** `tracciamento-2`, `rovesciatore-2`; differisce per: 300–1000 particelle con peso (1−Pd), uscita P(ancora nell'ombra).

### `creativo-3` · sciame-creativo, `e30f9e2dd4d7` · oggetto: demo, finestra di riemersione · tipo: procedura
- **Enunciato.** «La buca dichiarata e la moviola»: all'ingresso nell'ombra il sistema sigilla e mostra una scommessa («riemerge a destra fra 1,6 e 2,9 s»); una seconda camera oltre il pannello mostra alla giuria la verità, e il sistema non la usa; un tabellone conta scommesse vinte e perse. Poi: sosta → a finestra scaduta «ancora dietro, non lo vedo»; mano sul sensore → il battito tace. Quattro passaggi in tre minuti (stima). Finestra = quantili 5–95 % del rapporto tempo vero / tempo nominale su circa 100 passaggi di prova generale.
- **Ipotesi critica → controesempio.** Le prove generali somigliano alla demo → un giurato che cammina in modo diverso (il tabellone lo mostra).
- **Verifica, esito.** P-creativo-2b/3 (400 passaggi, intervallo al 90 %): Kalman 69,3 % (0,40 s); particelle 100 %, largo 6,27 s: attesa 75–97 % smentita in alto. P-creativo-3bis (scritta dopo quell'esito; 85–95 %, ≤ 2,5 s): 91,7 %, 1,24 s, regge [taratura e prova dalla stessa distribuzione simulata, aut.].
- **Vicina a** `requisiti-2`, `kalman-2`; differisce per: scommessa sul tempo esposta prima, seconda camera, finestra da quantili empirici.

### `creativo-4` · sciame-creativo, `e30f9e2dd4d7` · oggetto: risorse (a chi va il calcolo) · tipo: procedura
- **Enunciato.** «Il ronzio terminale»: a ogni ciclo un solo «sguardo costoso» (classificatore su un ritaglio, o modo rapido del sensore) va alla traccia con varianza / tempo al contatto massimo, con un'età massima di guardia per le altre. Entra la lista delle tracce, esce l'indice da guardare. Venti righe.
- **Rischi.** Errore sugli altri bersagli +158 % (da 0,059 a 0,151 m); guardia non provata; modo 4×4 a 60 Hz del VL53L5CX non verificato sul testo.
- **Ipotesi critica → controesempio.** La minaccia è già fra le tracce guardate → minaccia nuova fra le tracce affamate.
- **Verifica, esito.** P-creativo-4 (6 bersagli 1D, una misura per passo, 300 scene; smentita sotto il 10 %): −48,4 % sul più minaccioso (da 0,060 a 0,031 m), regge [aut.].

### `rovesciatore-1` · sciame-rovesciatore, `8f275a60e807` · oggetto: ambito, posa del sensore, ordine delle fasi · tipo: decisione
- **Enunciato.** Prima il sensore fermo, poi indossato. Lo stesso nucleo su un sensore fisso su treppiede, nell'applicazione industriale: sfondo di profondità = mediana di N fotogrammi, mobili per differenza (R1), ostacoli e ombre dallo sfondo (R2), nastro a terra come verità di riferimento. L'indossato viene dopo, con utente fermo e sola rotazione compensata; l'odometria si compra, non si scrive.
- **Rischi.** Perde il racconto assistivo e il senso dei 360°; gradimento della giuria non verificato; «mobile» sulla velocità istantanea: 21,6 % di falsi anche da fisso (soglia 0,3 m/s), serve una finestra di spostamento non misurata.
- **Ipotesi critica → controesempio.** Il moto proprio è la parte fragile dell'indossato → IMU allineata entro 10 ms (domina il rumore del filtro).
- **Verifica, esito.** P-rovesciatore-1 (punto fermo a 3 m; smentita se RMS < 0,10 m/s a δt = 30 ms): non risolta. Indossato 0,275 m/s a 10 ms, 0,469 a 30 ms, 2,50 senza compensazione; smentite le attese sul fisso (0,241 m/s contro ≤ 0,05). Traslazione non simulata. Per l'autore la proposta resta per la verità di riferimento, non per il rumore [aut.].
- **Vicina a** `requisiti-1` (sensore fermo); differisce per: applicazione industriale, sfondo a mediana, ordine delle fasi.

### `rovesciatore-2` · sciame-rovesciatore, `8f275a60e807` · oggetto: scena, regione prevista, ambito · tipo: soluzione
- **Enunciato.** Il prodotto è la mappa di ciò che non si sa. Griglia in pianta a celle di 10 cm, lancio dei raggi a ogni fotogramma; ogni cella ha stato ed età: osservata ora (libera o occupata), prevista, sconosciuta; una cella non rivista torna sconosciuta per età, non per log-odds. Per una traccia persa «previsto» = disco v_max·τ attorno all'ultima osservazione, intersecato con le celle non osservate; quando il disco riempie l'ombra → «sconosciuto» (segnale R6, senza soglie tarate). Il Kalman resta per la velocità sul visibile e nel primo secondo. Decisione = tabella di regole sui tre stati. Fuori campo = occlusione permanente dichiarata. Fuori dal percorso critico: classificazione, massa, accelerazione, vision transformer, decisione appresa, 360°, Rolling Grid.
- **Rischi.** R5 più prudente (dopo circa 1 s «sconosciuto» anche per chi prosegue); niente classi da mostrare; costo su CPU non misurato.
- **Ipotesi critica → controesempio.** v ≤ v_max (2,5 m/s) → bersaglio più veloce; due bersagli che si incrociano nell'ombra; ombra che tocca il bordo del campo.
- **Verifica, esito.** P-rovesciatore-2 (2000 traiettorie, manovre 60/25/15 ipotizzate, q = 0,1): fuori dall'ellisse al 95 % del Kalman 14,3 % (smentita < 5 %, attesa > 20 %): non risolta; traccia cancellata dopo 1 s 73,5 %, insieme raggiungibile 0,00 % (per costruzione), τ* = 1,2 s: reggono [aut.].
- **Vicina a** `nuvole-punti-1`, `creativo-2`, `tracciamento-2`; differisce per: regione prevista come insieme raggiungibile, ogni cella scade per età, nessuna soglia.

## In coda, senza giudizi

Sigle: v = visione, l = lidar, np = nuvole-punti, t = tracciamento, k = kalman, rq = requisiti, rc = ricercatore, c = creativo, rv = rovesciatore; il numero è quello dell'idea (v2 = `visione-2`); la sigla senza numero indica la diagnosi di quel ruolo.

**(a) Affermato da più idee.**
1. Un solo sensore di profondità frontale, fuori campo mai «libero»: v1, l1, np2, rq1, rc1, rv2.
2. Massa fuori dall'uscita o dal percorso critico: k1, rq1, rc1, rv2.
3. Ordine rilevamento → associazione → Kalman → decisione: v1, k1, rq1. Modelli pesanti asincroni o fuori: v1, rc2, rv2.
4. Kalman a velocità costante senza stato d'accelerazione: k1, t1, rq1, rc2.
5. Stati distinti, «previsto» a scadenza, zona mai restituita «libera»: v2, t1, k2, rc2, rq1, np1, rv2. Orizzonte fra 0,9 e 1,6 s: v2, t1, k2, rq2, rv2.
6. Causa della misura mancata letta dalla profondità: v2, np1, t2, c2, rv2.
7. La bozza (scadenza fissa, log-odds, Kalman che prosegue alla cieca) non regge R8: t2, np1, rv2, c2.
8. Demo col pannello e passaggi contati: rq2, c3, rv2, k2. Il sensore fermo toglie il moto proprio: rq1, rv1, k1, l2.
9. Casi aperti: vetro e superfici scure (v1, l1, np1, c2); due bersagli che si incrociano nell'ombra (v2, t1, c2, rv2).

**(b) Contraddizioni candidate a K#.**
1. **Nascosto o assente.** Prova sul punto previsto (v2: un raggio; np1: tre fotogrammi in libero) contro prova sulla massa d'incertezza (t2: il punto medio tiene l'identità nel 91 % dei transiti e nello 0 % delle soste; c2).
2. **Regione prevista.** Ellisse di covarianza (v2; k2: copertura 0,90–0,94; t1: 98,6–99,9 % alla porta al 99 %) contro disco v_max·τ ∩ non osservato (rv2: ellisse al 95 % fuori nel 14,3 %) contro particelle (c2: 300–1000; t2: circa 200).
3. **q in m²/s³.** 0,5 (t1) contro 0,2 (k2) contro 0,1 (rv2).
4. **Fine del «previsto».** Raggio 1 m (v2) contro 1,5 m (t1, k2) contro disco che riempie l'ombra, senza soglia (rv2) contro soglia da misurare (rc2) contro tetto di 10 s (t2).
5. **Sosta dietro il pannello.** La traccia scade (v2, k2, rq2) contro identità tenuta dopo 2–4 s di sosta (t2).
6. **Celle.** «Occupato» ricordato finché non smentito, «libero» che scade in 0,5 s (np1) contro ogni cella scade per età (rv2). Tre stati (v1, rc1, rq1) contro quattro (np1). «Libero» = suolo visto alla quota attesa (np1) contro libero dal lancio dei raggi (l2: «libero fin qui»; rv2).
7. **«Mobile» (R1).** Rilevatore a classi (v1, rc1) contro rilevamento geometrico (rq1) contro differenza dallo sfondo (rv1). Prova sulla covarianza con 0,0 % di falsi (k1) contro 21,6 % di falsi da sensore fisso alla soglia 0,3 m/s (rv1).
8. **Moto proprio e applicazione.** Rischio maggiore dell'indossato (v, t, rc; k1: 1,49 m senza giroscopio, 0,25 m con) contro «solo senza IMU o con δt ≥ 30 ms» (rv1). Assistiva con utente fermo (rq1) contro industriale su treppiede (rv1).
9. **I 360°.** Nessun requisito li chiede (rq1) contro LiDAR 2D se servono (l2, np2). «3 ToF = 360°»: smentito (v, l, rq, rc) contro non risolto (np per un ToF qualsiasi; c anche per i multizona).
10. **Feedback.** Battito continuo sul libero osservato (c1) contro messaggi direzione + distanza + stato (rq1).
11. **Accettazione.** Occlusione: ≥ 8/10 (rq1), ≥ 18/20 (t, §5), ≥ 26/30 nel cerchio (k2), ≥ 16/20 stati giusti (v2). Pannello 1 m (rq2) contro 2 m (t, §5). Latenza 80 ms (v1) contro p95 ≤ 150 ms (rq1).
12. **Numeri.** Femto Bolt 0,25–2,88 m (v, l, rq, rc) contro 0,25–2,21 m (np). VL53L7CX 2,0 m (l) contro 3,5 m (rc). Persona a 4 m su ToF 8×8: 1,3 zone (l) contro 5,4 (np). Velocità costante: errore medio/finale 0,39/0,83 m a 4,8 s (rc2) contro raggio al 95 % di 2 m a 2 s (k); metriche diverse. Accelerazione: «smentito che aiuti» (k) contro «non risolto» (l).
