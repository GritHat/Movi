# Previsioni — sciame-avversario, f2 torneo, parte 1 (H-001, 002, 003, 004, 006, 007, 008, 017, K-006)

Scritte alle 2026-11-14T13:39:47+01:00, PRIMA di ogni script, ricerca in rete o rilettura riga per riga. Onestà sull'ordine: prima di
scrivere ho letto contratto, triage, schede, firme e, con `grep`, alcune righe delle consegne di f1; per H-001, H-003
e H-004 avevo già una stima a mente (H-003: il conto «1,9 punti» è già dell'autore; H-004: un `grep` di «riconosc»
sulle regole, fatto per orientarmi, ha già dato 1 occorrenza). Per quelle tre la previsione non è cieca: lo dichiaro.

| # | Misura | Esito atteso | Soglia di smentita |
|---|---|---|---|
| P1 (H-001) | σ_z a 4 m = z²·σ_d/(f·B), con base e focale della scheda del modello più economico (classe base 50 mm), in due varianti: sottopixel tipico (0,08 px) e limite dichiarato dal costruttore («≤ 2 % a 2 m», scalato con z²) | tipico 5–8 cm (regge); al limite dichiarato 14–17 cm (sul filo) | smentita se > 15 cm con il dato del costruttore; se le due varianti stanno ai due lati di 15 cm: non risolta |
| P2 (H-002) | gradino 15 cm a 2 m in pianta, sensore a 1,2 m: distanza fra le due quote in unità di σ_h (σ_h = σ_z·sinθ), con il rumore dichiarato dal costruttore | > 3σ (regge, attese 4–6σ) | smentita se ≤ 3σ |
| P2b (H-002, attacco mio) | camera con campo verticale 58° inclinata in basso: distanza sotto cui un ostacolo a 1,8 m di quota (sporgente, all'altezza della testa) esce dal campo, per inclinazioni 0°–30° | con ≥ 20° di inclinazione un ostacolo alto resta invisibile sotto i 2 m di distanza | smentita dell'attacco se a 20° si vede ancora a 1 m |
| P3 (H-003) | punti per giro su una gamba di 12 cm a 5 m (passo 0,72° e 0,8°); quota di giro coperta dal busto (largo 0,40–0,45 m) con il LiDAR a 5–10 cm dal petto | 1,7–1,9 punti (< 4); busto copre 130°–155°, cioè più di metà del semigiro posteriore | smentita dell'idea se < 4 punti O se manca ≥ metà del retro (soglie del triage) |
| P4 (H-004) | rilettura delle 3 frasi di regole riga per riga: frasi che il «taglio a otto» (senza classi, sensore fermo) non copre | ne trovo almeno una: «riconoscere un oggetto o un soggetto», forse «attività», «orientamento» | smentita del taglio se una frase PRESCRITTIVA («dovrà», «la sfida è») non è coperta; se è solo una premessa: RIFORMULARE |
| P6a (H-006) | 7 categorie (muro, porta, gradino/scala, palo, scatola, carrello/transpallet, cono) fra le 80 classi di coco.yaml, riletto da me dal file grezzo | 0 su 7 (regge) | smentita se ≥ 1 |
| P6b (H-006) | somma della latenza del percorso critico da tempi pubblicati: latenza propria del sensore (esposizione + lettura a 30 fps) + geometria su CPU + uscita audio | la parte di calcolo sta sotto 80 ms, ma con sensore e audio il totale «fotone → suono» supera 80 ms | smentita se il totale dichiarabile supera 80 ms; se i tempi pubblicati non si trovano: non risolta |
| P7 (H-007) | esiste un sensore a tempo di volo con campo orizzontale ≥ 130° e ≥ 4 m al sole? Cerco camere ToF grandangolari e LiDAR dToF | nessuna camera iToF ≥ 130°; ma i LiDAR dToF rotanti (360°) sì: il motivo «nessun ToF» cade se «ToF» include i dToF a scansione | smentita del MOTIVO se ne trovo uno con scheda aperta; l'idea (una RGB-D frontale) non cade per questo |
| P8 (H-008) | regola firmata applicata a 5 casi con uno script mio (un settore, 1D): vetro; rampa a 5°; errore di assetto di 1°–2°; mobile che lascia la cella mentre è fuori campo (occupato ricordato); corridore a 3–5,6 m/s contro la scadenza di 0,5 s; sosta dietro il pannello con la regola dei tre fotogrammi | vetro → «libero» falso; rampa/assetto → «occupato» falso oltre 0,8–4 m; fuori campo → «occupato» fantasma senza limite d'età; corridore → penetra > 0,7 m; sosta → traccia chiusa a ~1 s con la persona nascosta | smentita di «0 libero falsi» se almeno un caso dà «libero» su cella fisicamente occupata con la regola come firmata |
| P17 (H-017) | simulazione logica mia: il battito con «fresco = età della marca temporale» quando a monte si ripete l'ultimo fotogramma con marca nuova | il battito continua senza limite (smentita della frase «si spegne da solo» in quel guasto); con contatore di fotogramma del sensore + prova di contenuto si spegne entro 1 s | smentita se il battito dura > 1 s dopo il blocco |
| PK6 (K-006) | le due regole (H-008: occupato ricordato, libero 0,5 s; H-009: tutto scade per età T) su vetro e su mobile uscito di scena | vetro: «libero» falso con ENTRAMBE; mobile uscito: fantasma senza limite con H-008, «sconosciuto» dopo T con H-009; ma H-009 con T > 0,5 s dà un «libero» ricordato falso | nessuna delle due vince su tutti e due i casi → composizione |

Dichiarazione d'indipendenza generale: tutti i controlli condividono con le idee il modello linguistico e la lettura delle schede fatta dal traduttore; gli script sono miei e non importano codice degli autori.

## Esiti (aggiunti DOPO)

### Previsioni aggiunte alle 2026-11-14T13:42:46+01:00, prima del secondo script (`attacchi2_parte1.py`)
- **P2c (H-002):** stessa camera montata in verticale (87° in verticale, 58° in orizzontale), inclinata 15°: attesa: suolo da < 1 m E ostacolo a 1,8 m visibile da < 1,3 m; smentita della contromisura se una delle due distanze supera 1,5 m.
- **P6c (H-006):** tempo misurato qui, in Python puro, di un percorso critico minimo (quota per pixel da tabelle + stato per cella polare) a 160×120 e 640×480, mediana su 5 giri. Attesa: 160×120 sotto 80 ms; 640×480 sopra 80 ms in Python puro (non è il codice che la squadra scriverà: vale solo come limite superiore grossolano). Smentita dell'idea: nessuna da questa misura (non decide); se anche 160×120 supera 80 ms, il rischio di latenza è reale senza numpy.
- **P8b (K-006, lancio dei raggi contro «suolo visto»):** scala in discesa che comincia a 2 m, sensore a 1,2 m: con la griglia a lancio dei raggi sui soli ostacoli le celle fra 2 e 3 m risultano «libero»; con «suolo visto alla quota attesa» risultano «non osservato». Smentita se anche il lancio dei raggi non dà «libero».

## Esiti (scritti alle 2026-11-14T13:44:48+01:00, dopo le prove; uscite grezze in `esito_attacchi_parte1.txt` e `esito_attacchi2_parte1.txt`)
- **P1: non risolta a 4 m, regge fino a 3 m.** Tipico (0,08–0,1 px): 3,8–7,2 cm. Al limite dichiarato: Gemini 335 12 cm, D455 8 cm, D435i 16 cm (> 15). Le varianti stanno ai due lati della soglia: per la regola scritta prima, non risolta. Nel campo di R2 come lo definisce H-004 (0,5–3 m) il limite dà al più 9 cm.
- **P2: regge.** 5,4σ al limite dichiarato, 15σ col tipico. Notato dopo: a 3 m la soglia di 7 cm vale 1,8σ al limite dichiarato; 1° d'errore d'assetto vale 3,5 cm a 2 m.
- **P2b: l'attacco riesce.** A 15° l'ostacolo a 1,8 m si vede solo oltre 2,41 m; a 20° oltre 3,79 m; a 30° mai. **P2c: la contromisura regge** (montaggio verticale a 15°: suolo da 0,74 m, ostacolo alto da 1,11 m).
- **P3: smentita la variante indossata al petto** su tutte e due le soglie: 1,7–1,9 punti sulla gamba; 70–86 % del semigiro posteriore coperto.
- **P4: nessuna frase prescrittiva scoperta; tre frasi non prescrittive scoperte** → RIFORMULARE (regola scritta prima).
- **P6a: regge** (0 su 7). **P6b: non risolta** (tempi pubblicati trovati solo per il sensore, e incerti; audio non trovato). **P6c: la mia attesa è smentita**: 640×480 in Python puro 20 ms, non oltre 80.
- **P7: come previsto.** Nessuna camera ToF ≥ 130° (massimo 120°); un LiDAR a scansione con 360° e 40 m a 100 klx esiste (Livox Mid-360, pagina aperta).
- **P8: smentito «0 libero falsi» fuori dalla scena dell'autore** (vetro, corridore); gli altri quattro casi come previsti. **P8b: come previsto.**
- **P17: smentita** con «fresco = marca temporale» (battito per tutti i 25 s osservati); 0,07–0,13 s con contatore o contenuto.
- **PK6: come previsto**, nessuna delle due regole vince su tutti i casi.
