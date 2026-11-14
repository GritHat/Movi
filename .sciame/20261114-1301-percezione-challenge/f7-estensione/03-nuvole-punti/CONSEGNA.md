Canarino: sciame-canarino-55f6adcfa718b00e

# Consegna di `sciame-nuvole-punti` — f7, corsia A (geometria e visione)

File: `PREVISIONI.md` (15:09:32, prima di ogni codice), `sim3d.c`, `risultati_scene.txt`, `risultati_sweep.txt`, `risultati_rumore.txt`, `risultati_scene_zona.txt`, `rifai.sh` (rifà tutto in meno di 40 s). Tutto è **simulazione, un fotogramma, sensore fermo**: nessuna riga è verificata su una camera vera.

## 0. Scostamenti, regole violate, esiti delle previsioni

- **Previsioni:** reggono np-P1, P3, P4, P6, P7, P8. **np-P2 smentita per N-G** (la mia variante «suolo visto vince»: 2,85 % del corpo di un soggetto del tutto nascosto in celle «libero»); regge per le altre. **np-P5 a metà**: la cella è «in ombra» come previsto, ma la quota vista dell'ombra dichiarata è 75,1 %, fra le mie due soglie (80 e 60): soglie mal poste. **np-P9 smentita**: con il rumore nominale lo scavo fino al punto misurato non mette «libero» nei solidi più di quanto faccia senza rumore (0,55 % identico): il troncamento a 3σ non è mostrato necessario in un fotogramma.
- **Dopo le previsioni** ho aggiunto la variante «zona» (marcare la fascia morta attorno al punto misurato): l'ipotesi che spiegasse lo 0,12 % di V5-C è **smentita** (stesso 0,3 litri). La causa resta un'ipotesi (schegge più sottili del passo fra i raggi): non verificato.
- **Lettura mia, dichiarata:** lo stato di una cella del nucleo l'ho fatto valere per la colonna 0–2 m (la fascia di quote che il nucleo usa per «occupato»). Se «libero» si legge «suolo visto e basta», la critica 1 diventa una critica alla frase d'uscita, non alla cella.
- Ho elencato con un `ls` i nomi delle sottocartelle di `f7-estensione`, senza aprirne nessuna. Rete: cinque pagine per le fonti; il link di Amanatides e Woo ha dato 403 (**non verificato**).
- **Indipendenza:** verità e rappresentazioni condividono l'autore, il modello della camera e i solidi; non il codice di visibilità (analitico contro immagine di profondità). Profondità ideale ai bordi: niente pixel misti, niente buchi, niente vetro.

## 1. La misura (cinque scene; volume giudicato 13,66 m³: settore di 87° fino a 3 m, quote 0–2 m)

S1 cassa alta 1 m con dietro un adulto (a) o un accovacciato (b); S2a trave a 1,7–1,9 m di quota sopra il campo; S2b la stessa trave vista, adulto dietro; S3 pedana da 0,4 m. Litri; fra parentesi il caso peggiore.

| Rappresentazione (numeri in memoria) | Libero a torto | Nascosto a torto | Visto reso «libero» | Nascosto in «libero» (max su 17 + 6 posizioni) | Trave non vista in «libero» |
|---|---|---|---|---|---|
| N-L nucleo alla lettera, cuneo fino al bordo (2 640) | 1 099–1 659 | 0–3 610 | 51–88 % | 0,00 % | **100 %** |
| N-G nucleo, «suolo visto vince» (2 640) | 1 247–1 659 | 0–1 375 | 69–88 % | **2,85 %** | **100 %** |
| B8 otto fasce di quota per cella (21 120) | 0 | 0–202 | 84–88 % | 0,00 % | 0 % |
| V5-O voxel 5 cm, «attraversato = libero» (576 000) | **310–449** | 0 | 99–100 % | **1,27 %** (10 cm: 7,28 %) | 0 % |
| V5-C voxel 5 cm, regola prudente (576 000) | 0–0,3 | 0–142 | 93–96 % | 0,00 % | 0 % |
| Q interrogazione nell'immagine, senza memoria (0) | 0 | 0 | 98 % | 0,00 % | 0 % |
| P profilo: due quote per cella, da Q (5 280) | 0 | 114–375 | 91–96 % | 0,00 % | 0 % |

Costo su un filo (Ryzen AI 9 HX 370, C `-O2`): DDA a piena risoluzione 43,9 milioni di passi e **307 ms** (5 cm), 155 ms (10 cm); aggiornamento proiettivo dei 576 000 centri **2,2 ms**; profilo P **3,9 ms**; griglia del nucleo 5 ms.

## 2. Critiche, ciascuna con la prova

1. **[nucleo] «Libero» non porta la quota, e in quota non è osservato.** Il bordo alto del campo sta a 1,2 + 0,249·r: 1,51 m a 1,24 m, 1,95 m a 3 m (conto a mano). Entro la griglia la colonna 0–2 m non è mai vista tutta. Misura: 1,10–1,66 m³ dichiarati liberi e mai osservati, il 15–19 % di ciò che il nucleo dà per libero; la trave non vista sta al 100 % in colonne «libero» (S2a).
2. **[nucleo] Il cuneo «oltre il primo ritorno» nasconde ciò che si vede.** Dell'ombra dichiarata è in realtà visto il 32,6–42,3 % (S1), il 75,1 % (S2b), l'81,5 % (S3). L'adulto dietro la cassa ha 13 730 pixel di ritorno, quello dietro la trave 21 550: in N-L il loro corpo è al 100 % «in ombra» e allo 0 % «occupato». Con la regola C6 (un gruppo tagliato da un'ombra non aggiorna il filtro) una persona in piena vista dalla vita in su andrebbe a «perso». **Non verificato su un'implementazione:** i simulatori del nucleo sono in pianta (`comune_f4.py`, righe 44–58: l'ombra è un intervallo angolare, senza quota). Quindi **nessuna prova del nucleo copre un occlusore più basso del sensore**.
3. **[consegna] «L'ombra dell'ostacolo basso non arriva al bordo» va precisata.** Al suolo l'ombra finisce a d·h_s/(h_s − h_o): per la cassa da 1 m sono 11,4 m (arriva al bordo: il difetto è in quota, sopra la linea di vista); per la pedana da 0,4 m sono 2,55 m.
4. **[promptMare §9] Il modello di costo è quello sbagliato per una camera di profondità.** Il lancio dei raggi pixel per pixel costa 307 ms per fotogramma, oltre i 66 ms dei 15 Hz; il confronto proiettivo (ogni voxel proiettato nell'immagine) 2,2 ms. È lo schema della fusione volumetrica da camere di profondità (Nießner e altri, 2013, https://niessnerlab.org/projects/niessner2013hashing.html; lì su GPU). Il sottocampionamento dei raggi non l'ho misurato.
5. **[promptMare §3, §14] La sparsità promette poco.** Un fotogramma tocca il 37,9 % dei voxel della regione 6 × 4 × 3 m e il 40,8–43,8 % dei blocchi 8³: scavare lo spazio libero alloca tutto il cono. Il risparmio sulla densa è al più 2,3–2,5 volte, prima del costo della tabella hash. «Meno memoria della densa equivalente» confronta il voxel con sé stesso: la linea di base è la griglia da 2 640 celle.
6. **[promptMare §10] Manca la prova che conta: il voxel visto in parte.** Con la regola corrente delle mappe a octree (libero esplicito, sconosciuto implicito: https://octomap.github.io/) un voxel attraversato da un raggio è libero tutto. Misura: 310–449 litri di falso libero a 5 cm, 548–813 a 10 cm (8,9–18,4 % del non visto), e la prova 1 del contratto passa lo stesso. Serve una prova 11: «un voxel osservato in parte è dichiarato libero?».
7. **[promptMare §5] I voxel in ombra non vanno memorizzati.** L'interrogazione Q (un punto è nascosto se si proietta più lontano della profondità misurata, con minimo e massimo 3 × 3 e margine) dà le classi con 0 litri d'errore nei due versi e resa 96,6–98,5 %, senza stato. Memorizzarli costa da 1 992 (S3) a 31 632 (S1a) voxel in più per fotogramma e crea ciò che le prove 2, 3 e 5 devono poi difendere.
8. **[limiti che nessuna rappresentazione chiude]** Fuori campo: 3 000–3 080 litri su 13 663 (22 %) in ogni riga della tabella. Vetro: non provato; per costruzione sbaglia la profondità, quindi ogni riga. Oggetti più sottili del passo fra i raggi (6–7 mm a 3 m): 0,3 litri di solido in «libero» anche in V5-C. Pixel misti ai bordi: non simulati, vanno all'esperto hardware.
9. **[promptMare §4] Storia contro garanzia corrente: non provata da me.** Il mio banco ha un fotogramma: log-odds, τ e decadimento restano al matematico. Deduzione: a sensore fermo la garanzia corrente è Q sugli ultimi 3 fotogrammi; la storia serve solo a «occupato ricordato».

## 3. `promptMare.txt` per il mio campo

- **Utile:** §5 (cinque classi; «non allocate un voxel per ogni punto sconosciuto»; memorizzare o interrogare: la risposta è interrogare); il problema del §4; §7 (i tre riferimenti e l'arresto dell'integrazione se la posa non è affidabile: 1° d'errore a 3 m sposta i raggi di 5,2 cm, un voxel intero; conto a mano); §10 prove 1–4, 6, 8–10; §11; del §14 la voce «ostacoli a quote diverse», l'unico beneficio che trovo dimostrato.
- **Inutile al primo prototipo:** §3 (hash, octree, CSR/COO: a sensore fermo il cono è fisso), §6 (stato a sei dimensioni), la formula di memoria del §9.
- **Sbagliato o da correggere:** §9 (costo per raggi); §14 «meno memoria della densa»; §10 senza la prova 11; la domanda finale che lega il beneficio alle «applicazioni UAV», che la traccia non nomina.

## 4. Stati proposti

| Enunciato | Stato |
|---|---|
| Il nucleo dichiara «libero» volume mai osservato in quota (1,1–1,7 m³) | sostenuto dai dati (simulazione; lettura «colonna 0–2 m» mia) |
| Il cuneo dichiara nascosto a torto il 33–82 % della sua ombra | sostenuto dai dati |
| Col cuneo alla lettera il soggetto del tutto nascosto non finisce mai in «libero» | verificato su 23 posizioni dichiarate; non universale |
| Il voxel 3D prudente chiude «quota della testa» (come dichiarazione, non come vista), ombra bassa, quote diverse | sostenuto dai dati |
| Fasce, profilo e interrogazione nell'immagine chiudono gli stessi buchi | sostenuto dai dati (np-P8 regge) |
| Il voxel «attraversato = libero» introduce falsi «libero» | sostenuto dai dati |
| A sensore fermo la mappa voxel è necessaria | **smentito** (in simulazione) |
| Il voxel serve in moto | non risolto: lo decide una riproduzione con errore di posa |
| Vetro, anello cieco, campo visivo chiusi dal 3D | no: deduzione; vetro non provato |
| Bersagli in volo | non risolto; il profilo P li esclude (assume soggetti poggiati al suolo) |

**Per Q1, dalla mia corsia: NO per il primo prototipo; SÌ CONDIZIONATO solo come stadio successivo per la piattaforma in moto** (posa con errore sotto un voxel alla portata, aggiornamento proiettivo, regola prudente, prova 11).

## 5. Proposte

**nuvole-punti-1 — profilo di quota per cella, ricavato nello spazio dell'immagine.** Accanto alla griglia polare, per ogni cella due quote: sotto quale non si vede (h_ombra) e fino a quale si vede (z_vista). «Libero» esce come «libero fino a z_vista»; «in ombra» come «possibile presenza sotto h_ombra»; un gruppo visto sopra h_ombra aggiorna il filtro. *Guadagno (misurato in simulazione):* libero a torto da 1 100–1 660 litri a 0; nascosto a torto da 1 100–3 610 a 114–375 (590–606 con rumore e margine 3σ); 5 280 numeri, 3,9 ms. *Vincoli:* sensore fermo, pavimento piano, soggetti poggiati al suolo. *Chi la prova:* la validazione, portando la quota nei simulatori del nucleo; poi chi ha la camera. *Falsificatore (meno di 5 minuti):* 200 scene a caso con rumore (occlusore alto 0,2–1,1 m, soggetto 0,2–1,7 m). **Atteso, scritto ora:** 0 scene con più dell'1 % di un soggetto nascosto in «libero». La smentisce una sola scena. Braccio che deve fallire: margine a zero senza minimo 3 × 3.

**nuvole-punti-2 — possibile presenza come «ombra d'ingresso» fuori dalla mappa.** La regione è la sagoma dell'occlusore nell'immagine (al più 480 righe di tre numeri: due colonne e una profondità), più la fascia di 0,40 m e l'età; un punto vi appartiene se si proietta nella sagoma, sta oltre quella profondità e sotto h_ombra. Vive nello strato delle tracce. **Si libera solo** per riaggancio, o cella per cella quando la profondità valida corrente supera il punto oltre il margine per almeno 3 fotogrammi nella fascia bassa (suolo visto). **Mai** per timer, decadimento, covarianza, rimozione di blocchi, raggi senza ritorno, salto di posa; vedere libera solo la parte alta cambia l'etichetta («sotto h_ombra»), non libera. *Guadagno:* le prove 2, 3 e 5 chiuse per costruzione; circa 3 kB contro 11 200 voxel da 5 cm per 1,4 m³ (conto a mano). *Vincoli:* sagoma ancorata ai pixel, quindi sensore fermo; in moto va riproiettata con la posa. *Chi la prova:* scene dinamiche e avversario. *Falsificatore:* sosta di 60 s dietro la cassa, poi la cassa viene tolta. **Atteso:** 0 fotogrammi col centro del soggetto fuori da regione, «occupato» e «non osservato»; regione sparita entro 3 fotogrammi dove il suolo torna visto. Braccio che deve fallire: sagoma ristretta di 20 cm.

## 6. Che cosa propongo dopo

1. Nel documento: «libero fino a quota z», con la tabella z(r). Il montaggio verticale già nella tabella delle decisioni del nucleo vede 1,8 m di quota da 1,11 m e il suolo da 0,74 m, al prezzo di 58° in orizzontale (conto a mano): chiude più buchi di qualunque mappa.
2. Per Q2: negli ambienti aerospaziali e industriali gli occlusori bassi e le sporgenze (carrelli, casse, ali, scaffali) sono la norma. S1, S2b e S3 sono la scena tipo, ed è lì che il cuneo sbaglia di più.
3. La validazione rifaccia R3 e R8 con un occlusore più basso del sensore.
4. All'esperto hardware: pixel misti e buchi ai bordi dell'occlusore, che cadono proprio dove vive la possibile presenza.
