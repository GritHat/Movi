Canarino: sciame-canarino-20c82ebff50dded3

# Consegna di sciame-tracciamento — f8 (continuità visiva), f1, corsia A

## 0. Scostamenti e regole violate

- **Quattordici previsioni su ventidue smentite, in tutto o in parte** (`PREVISIONI.md`: T1, T2 di misura, T4, T6, T7, T8, T9, T11; V-b, V-c, V-d, V-f; F-a e F-d in una o due celle). La più pesante: il predittore che avevo proposto io (particelle con «sosta» e «svolta», d2 e poi d3) **non migliora** quello del torneo (d1, solo «sosta»).
- **Modifiche fatte dopo aver visto i primi dati**, tutte marcate in `PREVISIONI.md`: d3, la massa «fuori area», il punto ibrido, la taratura conforme, la misura «entro 0,3 m dalla regione» al posto di «dentro la regione». Le ho poi provate su traiettorie e geometrie nuove (V1, V2, V3), con previsioni scritte prima.
- **Una regola forzata:** i tre lanci dell'ultimo giro stavano in un solo comando, che ha superato i 120 s dello strumento ed è finito in secondo piano; ogni lancio aveva il suo `timeout 120` e sono girati uno alla volta (15:31–15:33).
- **Indipendenza, dichiarata.** Tutto è simulazione mia in C (`prove/cont.c`, 4 versioni conservate; `prove/rifai.sh` rifà tutto). Scena e traiettorie di prosegue, sosta, torna, lontano: `truth()` dell'avversario, copiata senza modifiche. Rallenta, svolta, sosta lunga: generatore **mio**. I tassi di d1 sono dell'avversario. Condiviso con ciò che controllo: modello linguistico, bersaglio puntiforme, ombra esatta, sensore fermo, Pd 0,9, nessun falso allarme, un solo oggetto, celle quadrate di 0,25 m (non la griglia polare del nucleo). **La taratura qui non è quella indipendente che chiede il criterio 3.** Niente è verificato su hardware né in moto.

## 1. Q3 per le parti che mi competono: **non rispettato**

Geometrie: T/V1 = pannello da 1 m a 2 m, soggetto a 4 m; V2 = pannello da 2 m; V3 = demo corretta (pannello da 1 m a 1,9 m, attore a 2,3 m, portata 3 m). 400 traiettorie per comportamento, 7 comportamenti; «miscela» = tutti insieme.

| Parte | Esito | Prova |
|---|---|---|
| Nucleo, regola «meno di metà dell'ombra» più «perso» assorbente (criterio 1) | **non rispettato** | quota dei cicli senza osservazione con una stima emessa: V3 **14–69 %** (prosegue 68,9; torna 62,6; rallenta 46,3; sosta 26,2; sosta lunga 15,7; lontano 13,9; svolta 13,8), V2 21–47 %, V1 25–88 % (`fin_V*.txt`). Dopo «perso» il vuoto dura fino alla ricomparsa: 3,0 s in media per la sosta in V3 |
| Punto mostrato dal nucleo (criterio 4) | **non rispettato** | il punto del filtro sta su una cella vista libera nel 90–94 % dei casi a 2–3 s (V1); ritagliato sul non libero, salta: 0,2–6,6 % dei cicli oltre v_max·dt, passo massimo 2,57 m |
| Regione del nucleo (criterio 3) | **non rispettato** | cerchio al 90 %: miscela 0,64 a 2–3 s (V1) e 0,47 a 2 s (V3); torna 0,46 a 2 s, lontano 0,33 a 3 s; area 4,35 volte l'ombra a 3 s (V1), 24,9 volte in V3 |
| Criteri d'accettazione di R3 | **non rispettato** | misurano solo l'identità al ritorno; «area prevista» è «tolta dalla promessa» (`VERDETTO.md` §3) |
| Identità alla ricomparsa, strato di garanzia | **rispettato** (in simulazione) | 100 %, una traccia pendente (`SOLUZIONE_V2.md` §1); resta così |
| Gruppo tagliato dall'ombra escluso (C6) | **in parte** | porta il buio da 0,60–0,67 a 1,07–1,27 s (`SOLUZIONE_V2.md` §1): l'oggetto è mezzo visibile e il sistema prevede. Non misurato da me |
| Specializzazione e documento per l'utente | **non rispettato** | «per le classi veloci [il previsto] si riduce a un istante» (`SPECIALIZZAZIONE.md` §3.3); «con 24 ore si tagliano […] area prevista» (`proposta_sciame.tex`, riga 184) |

## 2. Critiche, con il confronto (V1, miscela; d1 con 2000 particelle; `fin_V1.txt`)

| Metodo | Errore mediano del punto a 1 / 3 / 5 s (m) | Copertura 90 %, min–max su τ | Comportamento peggio coperto | Area 90 % / ombra a 3 s | Passi oltre v_max·dt | Sosta: errore a 3 s | Torna: cop. a 2 s | Identità più bassa |
|---|---|---|---|---|---|---|---|---|
| (a) Kalman lasciato correre | 0,28 / 2,99 / 5,38 | 0,64–0,94 | lontano 0,33 | 4,35 | 0 % (non si ferma mai) | 2,81 | 0,46 | torna 49,8 % |
| (b) lo stesso, ritagliato | 0,28 / 3,40 / 5,38 | uguale | uguale | 3,23 | 0,2–6,6 % | 3,29 | 0,46 | uguale |
| (c) cinque modelli, pesi aggiornati | 0,25 / 1,67 / 3,18 | 0,65–0,97 | svolta 0,34; sosta 0,41 a 5 s | 0,44 | 0,1–1,9 % | 2,16 | 1,00 | svolta 97,4 % |
| (d0) particelle senza «sosta» | 0,25 / 1,40 / 3,00 | 0,68–0,92 | torna 0,39 | 0,59 | — | 1,35 | 0,39 | torna 38,2 %, sosta 75,2 % (`ris_T1_v1.txt`) |
| (d1) particelle con «sosta» | 0,26 / 0,88 / 1,49 | **0,79–0,96** | svolta 0,42; lontano 0,45 (a 2 s) | **0,43** | 0 % | **0,62** | 0,97 | svolta 93,5 % |
| (e) raggiungibile ∩ ombra | 1,16 / 1,78 / 1,39 (baricentro) | 1,00 | — | 1,00 (0,58 a 0,5 s) | — | 1,38 | 1,00 | 100 %, ma ambigua |
| fermo all'ultima misura | 1,18 / 1,78 / 2,15 | — | — | — | — | 1,15 | — | — |

1. **Che cosa interrompe la continuità nel nucleo.** (i) La regola «meno di metà dell'ombra»: spegne la stima dopo 0,7–1,9 s. (ii) «Perso» assorbente: da lì nessuna posizione fino al riaggancio. (iii) Il punto del filtro esce dall'ombra e non si ferma mai (riga a). (iv) C6 allunga il buio. (v) La chiusura in campo aperto dopo 3 fotogrammi è motivata e va bene; in ombra manca ogni regola di chiusura con un motivo.
2. **Più modelli con pesi (c): no.** I pesi imparano dall'evidenza negativa, le forme no: le gaussiane non si troncano. Regge fino a 3 s sui modi che ha, poi cede: sosta 0,74 a 4 s e 0,41 a 5 s; in V3 miscela 0,38–0,50 da 2 s. Punto a 3,9 m da chi è fermo a 4–5 s.
3. **Il modo «sosta» è necessario** (conferma il torneo): senza, torna 0,39 e identità 38 %.
4. **d1 è il compromesso migliore, con tre limiti misurati.** (i) Vuole almeno 8 particelle per cella d'ombra da 0,25 m: con circa 2 la copertura in V2 scende a 0,73 a 3 s; con 2000 particelle 0,90 (`ris_V2.txt`, `fin_V2.txt`). (ii) Non copre chi fa ciò che il modello non prevede: svolta e lontano 0,42–0,45 a 2 s (± 0,05). (iii) La sua media resta indietro su chi prosegue: salto alla ricomparsa 0,79 m (V1) e 1,72 m (V2), contro 0,26 e 0,46 m del filtro.
5. **Le mie varianti con «svolta» (d2, d3): smentite.** d2 copre «lontano» a 3 s nello 0,09 (attesi ≥ 0,75); d3 in V2 perde chi prosegue (0,63 contro 0,91 a 3 s; identità 66 % contro 99 %, `fin_V2.txt`).
6. **Nessuna regione «probabile» garantisce ogni comportamento.** Anche tarata sul comportamento peggiore copre «lontano» 0,71 e «svolta» 0,74 a 2 s occupando 0,79 dell'ombra (`ris_V1.txt`). La garanzia per comportamento la dà solo il limite esterno (e).
7. **Il punto non vale per sempre.** Errore mediano oltre 1 m da 4 s (1,24–1,55 m; 1,30 m già a 3 s in V2). In V3, a 4 e 5 s, è peggiore di «fermo»: 1,39 contro 1,10 m e 2,01 contro 1,22 m.
8. **«Può aver lasciato l'area: p» non è tarato.** d3: 0,13 dichiarato contro 0,89 vero a 3 s per «lontano»; 0,13–0,23 contro 0 per chi rallenta (`fin_V1.txt`). Va mostrato come etichetta, non come numero.
9. Fino al 4 % (V1) e al 10 % (V3, a 1 s) delle celle della regione di d1 è «libero» nella griglia vera: sono celle di bordo da 0,25 m. Con la griglia del nucleo e la fascia di guardia va rimisurato: così com'è, l'invariante 4 non è provato.

## 3. Stati proposti

| Enunciato | Stato |
|---|---|
| Il nucleo emette una stima a ogni ciclo senza osservazione | **smentito** (14–69 % in V3) |
| Il cerchio del filtro è tarato per comportamento | **smentito** (0,33–0,46) |
| d1, 2000 particelle, livello nominale: copertura al 90 % nella miscela 0,90–0,98 a 0,5–5 s | **sostenuto dai dati** in V2 e V3; **smentito in una cella** in V1 (0,794 ± 0,018 a 2 s) |
| d1 copre ≥ 0,85 prosegue, sosta, sosta lunga, torna, rallenta | **sostenuto dai dati** (≥ 0,865, tre geometrie, n ≥ 100) |
| d1 copre chi svolta o esce dal lato lontano | **smentito** (0,42–0,83) |
| Punto ibrido: nessun passo oltre v_max·dt | per costruzione; 0,00 % misurato nelle tre scene |
| Punto ibrido: salto ≤ 0,30 m su chi prosegue | sostenuto in V1 (0,25) e V3 (0,19); **smentito** in V2 (0,50, dopo 3,3 s) |
| Errore mediano del punto ≤ 1,0 m fino a 5 s | **smentito**; fino a 3 s sostenuto in V1 (0,88) e V3 (0,97), non in V2 |
| La taratura conforme tiene sulla stessa geometria | **sostenuto dai dati**, una geometria: 0,882–0,900 e 0,476–0,503 (n = 1197–2798) |
| I livelli tarati si trasferiscono a un'altra geometria | **smentito** (0,63–0,71 a 3–5 s in V2) |
| Costo: 64–73 µs per ciclo e per traccia (2000 particelle, C; misurato su d3, che fa più conti di d1) | sostenuto dai dati, indicativo |
| Tutto ciò su camera vera, corpo esteso, sensore in moto | **non risolto**: lo decidono 30 passaggi registrati con la posizione vera segnata a terra |

## 4. Proposte per Q4

**`tracciamento-1` — «previsto» continuo a due livelli; «perso» smette di essere uno stato finale.**
- *Enunciato.* Per ogni traccia confermata entrata in un'ombra, a ogni ciclo senza misura escono: **(1) il punto più probabile**, cioè il punto del filtro finché sta su celle non viste libere, poi (dopo 3 cicli su celle libere) la media delle particelle, mai più di v_max·dt per ciclo; **(2) la regione probabile**, le celle a massa più alta di d1 (sosta 0,25/s, ripartenza 0,4/s, evidenza negativa solo oltre la fascia di guardia, almeno 8 particelle per cella); **(3) il limite esterno**, che è lo strato 1 di oggi, invariato. «Perso» diventa **«previsto ampio»**: quando il raggio della regione al 50 % supera una soglia utile dichiarata in metri, il punto si spegne e resta la regione, con un altro segno e la sua età. La soglia non è una quota dell'ombra: nella demo la regione al 90 % supera metà dell'ombra già a 1 s (0,67), e la regola di oggi spegnerebbe tutto di nuovo. La soglia in metri **non è misurata**. La traccia si chiude solo con un motivo scritto: riagganciata; celle viste libere una per una; uscita dalla zona coperta.
- *Quando è onesto smettere.* Il **punto**: quando non batte più «fermo» o supera la soglia d'errore (qui fra 3 e 4 s). La **regione probabile**: finché è più piccola del limite esterno e la copertura misurata tiene (qui fino a 5 s, il massimo provato: 0,43–0,55 dell'ombra da 3 s in poi). Il **limite esterno**: mai, e mai per un timer.
- *Guadagno atteso (prima → dopo).* Cicli con una stima: 14–69 % → 100 %. Copertura al 90 % nella miscela: 0,47–0,87 → 0,90–0,97 (V3). Errore del punto a 3 s: 2,99 → 0,88 m (V1), 3,13 → 0,97 m (V3). Passi oltre v_max·dt: 0,2–6,6 % → 0. Identità: 100 % in V1 e V3 sui cinque comportamenti modellati; 93,9–100 % in V2.
- *Vincoli.* Invarianti 3–7 intatti: la regione è sempre «previsto», mai su celle libere oltre la fascia, e non tocca lo strato 1. Una sola traccia pendente per ombra. L'etichetta è «probabile», mai «certo».
- *Chi la prova.* Validazione e statistico, con un generatore non mio.
- *Falsificatore (≤ 5 min).* `traiettoria()` del rovesciatore o `g1` del torneo, portate nella scena e date a `cont` (d1, 2000 particelle). **Atteso, scritto ora:** copertura della miscela ≥ 0,85 a ogni τ fino a 5 s; chi svolta 0,4–0,8. **Smentita:** miscela < 0,80 a un τ con n ≥ 300, o un ciclo senza stima.

**`tracciamento-2` — il livello della regione si tara per installazione, e R3 prende misure nuove.**
- *Enunciato.* Il livello mostrato non è quello nominale del modello: è il quantile empirico del punteggio «livello al quale la cella del vero entra nella regione», per tempo senza osservazione, su passaggi di quell'installazione diversi da quelli della prova. R3 aggiunge: stima emessa nel 100 % dei cicli; copertura al 90 % fra 0,85 e 0,95 a 0,5, 1, 2, 3, 5 s; copertura per comportamento riportata accanto a quella del limite esterno (che deve essere 100 %); area della regione riportata accanto alla copertura (qui 0,14–0,67 dell'ombra a 1 s); nessun passo oltre v_max·dt; prima misura entro 0,3 m dalla regione in ≥ 95 % dei ritorni (d1: 85–100 %; la svolta è sotto).
- *Guadagno atteso.* Una precisione dichiarata che è una misura: 0,88–0,90 e 0,48–0,50 su dati nuovi, contro 0,64–0,94 del cerchio.
- *Vincoli.* Vale per la popolazione di taratura: altra geometria, altra taratura (smentita V-c). Non garantisce il singolo comportamento.
- *Chi la prova.* Statistico.
- *Falsificatore (≤ 5 min).* Tarare su V3 con un seme e provare su un altro. **Atteso:** tutte le celle fra 0,86 e 0,94. **Smentita:** una cella fuori da 0,85–0,95 con n ≥ 1000. Non eseguito.

## 5. Che cosa propongo dopo

1. Rifare il confronto con un generatore indipendente e con la griglia polare e la fascia del nucleo (`sim_v2.py`): è la prova che manca al criterio 3.
2. Ombra stimata a ± 20 cm e corpo largo 45 cm: nel torneo le particelle morivano nel 23–55 % dei casi con l'ombra stretta. **Non verificato qui.**
3. Gruppo tagliato dall'ombra: usare il bordo libero più la larghezza nota come misura a rumore largo, solo per tracce confermate e mai per l'etichetta «mobile». **Non verificato.**
4. Due tracce pendenti nella stessa ombra, e sensore in moto (previsione in riferimento fisso, ombra che cambia per parallasse): **non verificato**.
5. Togliere dal documento per l'utente la frase che mette l'area prevista fra le cose tagliabili.

File: `PREVISIONI.md`, `stato.md`, `prove/` (sorgenti, risultati, `rifai.sh`, `tabella.py`).
