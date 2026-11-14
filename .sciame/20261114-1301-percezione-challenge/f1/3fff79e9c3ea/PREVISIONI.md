# PREVISIONI — sciame-ricercatore, f1, corsia A

Scritte PRIMA delle prove che le decidono. Ora di scrittura: 2026-11-14T13:10:29+01:00 (da `date -Is`).
Che cosa avevo già visto a quest'ora: TASK.md, CONTRATTO.md, regole_challenge.md, l'indice dei titoli della bozza
(righe 1998-3800), e i riassunti di quattro ricerche in rete (GuideTouch; EdgeTAM a circa 16 FPS su iPhone 15 Pro Max;
image2mass e seguiti; occhiali Ally Solos). NON avevo ancora aperto: schede tecniche di sensori ToF, l'articolo di
Schöller et al. sul modello a velocità costante, i numeri di SAM 2 / SAMURAI, i numeri di image2mass.
Indipendenza: le previsioni poggiano sulla mia memoria (modello con conoscenza fino a metà 2026); le prove sono
fonti primarie in rete (schede tecniche e articoli), quindi indipendenti da me salvo l'errore di lettura.

## P1 (falsificatore di ricercatore-1: «un solo sensore di profondità frontale stereo + IMU, non 3 ToF a 360°»)
- Misura: dalle schede tecniche dei costruttori, (a) campo visivo orizzontale (HFOV) della profondità e (b) portata
  massima dichiarata e uso in luce solare, per le camere ToF commerciali sotto ~450 EUR l'una (Orbbec Femto Bolt /
  Femto Mega, Azure Kinect, Arducam ToF, Luxonis OAK ToF) e per i ToF multizona economici (ST VL53L5CX / VL53L7CX /
  VL53L8CX).
- Previsione: nessuna camera ToF di questa fascia ha HFOV > 120°; quella a 120° (modalità WFOV di Femto Bolt / Azure
  Kinect) ha portata dichiarata < 3 m ed è data per uso interno; i multizona ST hanno FoV <= 90° in diagonale e
  portata <= 4 m al buio, minore in luce ambiente. Quindi 3 ToF non danno 360° con sovrapposizione.
- Soglia di smentita: trovo una camera ToF <= 450 EUR con HFOV >= 130° (3 x 130 = 390°, sovrapposizione minima per
  calibrare) E portata dichiarata >= 4 m in esterno alla luce solare. Se la trovo: smentita, e 3 ToF a 360° tornano
  un'opzione. Se trovo solo l'HFOV o solo la portata: non risolta.

## P2 (falsificatore di ricercatore-2: «Kalman a velocità costante nel percorso critico, modelli appresi fuori»)
- Misura (a): in Schöller, Aravantinos, Lay, Knoll, «What the Constant Velocity Model Can Teach Us About Pedestrian
  Motion Prediction» (RA-L 2020), l'errore ADE/FDE medio su ETH/UCY del modello a velocità costante rispetto ai
  predittori appresi (Social-LSTM, Social-GAN, SoPhie...), orizzonte 4,8 s.
- Previsione (a): il modello a velocità costante ha ADE circa 0,5 m e FDE circa 1,0-1,1 m, pari o migliore dei
  modelli appresi confrontati nell'articolo.
- Soglia di smentita (a): se nell'articolo il modello a velocità costante è peggiore di oltre il 30% (ADE medio)
  rispetto al miglior modello appreso confrontato, la proposta è smentita per le occlusioni lunghe.
- Misura (b): la velocità dichiarata dei modelli video promptabili con memoria (SAM 2 e derivati) su hardware
  modesto (telefono, Jetson Orin Nano, CPU).
- Previsione (b): nessuna fonte primaria dichiara >= 30 FPS per SAM 2 o derivati su hardware di classe Jetson Orin
  Nano / CPU portatile; i 30-44 FPS di SAM 2 sono su GPU da datacenter (A100).
- Soglia di smentita (b): una fonte primaria con >= 30 FPS misurati su Jetson Orin Nano o CPU portatile, più oggetti.

## P3 (enunciato di contorno: «la massa non è osservabile dalla visione con l'affidabilità che serve»)
- Misura: l'errore dichiarato dai lavori di stima della massa da immagini (image2mass 2017 e seguiti 2025-2026).
- Previsione: gli errori tipici sono dell'ordine di un fattore 1,5-2 (o MAPE >= 40%) su oggetti piccoli da catalogo
  (dataset di prodotti), e nessun lavoro stima la massa di pedoni/veicoli/carrelli in scena da un sensore indossato.
- Soglia di smentita: un lavoro con errore relativo mediano <= 15% su oggetti di scena reali non di catalogo.

## Esiti (compilati DOPO le prove, vedi CONSEGNA.md)

Compilati alle 2026-11-14T13:13:46+01:00, dopo le prove. Il testo sopra questa riga non è stato modificato.

- **P1: NON RISOLTA** (per la regola scritta prima: trovata solo una metà).
  - Metà HFOV: regge sui sensori aperti. Orbbec Femto Bolt: profondità «H 120° V 120° (WFOV)», portata WFOV
    0,25-2,88 m, ambiente «Indoor» (pagina del costruttore, aperta). ST VL53L7CX: 60° x 60° (90° in diagonale), 8x8
    zone, 350 cm (pagina ST: timeout; dato letto solo nel riassunto della ricerca). Nessun ToF con HFOV >= 130°
    trovato; la ricerca NON è esaustiva (due famiglie di sensori). HFOV di Luxonis ToF: non dichiarato nella pagina.
  - Metà portata/sole: le fonti sono in disaccordo. Luxonis dichiara ToF 20 cm-5 m e accuratezza «<1% indoors, <2%
    outdoors» (pagina del costruttore, aperta); Orbbec dichiara «Indoor»; una rassegna ISPRS 2023 (solo riassunto,
    non aperta) dice che l'uso esterno resta limitato dal sole. Decide una prova di 5 minuti al sole col sensore vero.
- **P2(a): REGGE**, con uno scarto numerico. Tabella I di Schöller et al. (PDF aperto, testo estratto): media ETH/UCY
  a 4,8 s, ADE/FDE: velocità costante 0,39/0,83 m; SR-LSTM 0,45/0,94; LSTM 0,99/2,08; SoPhie 0,54/1,15; S-GAN
  (migliore di 20 campioni) 0,32/0,60; velocità costante con campionamento 0,28/0,56. Avevo previsto 0,5/1,0-1,1: la
  direzione regge, i valori sono più bassi del 20% circa. La soglia di smentita (peggiore di oltre il 30%) non è
  toccata: il caso meno favorevole è S-GAN a 20 campioni contro la versione deterministica, +22%.
- **P2(b): REGGE sulle fonti trovate** (assenza di prova su ricerca non esaustiva, non prova di assenza). EdgeTAM: «16
  FPS on iPhone 15 Pro Max», 150,9 FPS su A100 (README, aperto). SAMURAI: «The existing code doesn't support
  live/streaming video» (README, aperto). Nessuna misura su Jetson Orin Nano o CPU trovata: non verificato.
- **P3: REGGE.** Lee et al., IJCAI 2026 (arXiv 2601.20303, HTML aperto): su image2mass APE 1,066 (image2mass) e 0,665
  (loro metodo), ALDE 0,655 e 0,519 (cioè un fattore medio e^0,519 = 1,68); su ABO-500 APE 0,976 e 0,980. Oggetti da
  catalogo Amazon. Nessun lavoro trovato sulla massa di pedoni o carrelli in scena (ricerca non esaustiva).
- Notato DOPO (non era nelle previsioni): la pagina Luxonis contraddice la mia attesa che il ToF ceda al sole; il
  codice di SAMURAI non accetta flussi dal vivo; la bozza (righe 2091-2118) propone già una sola camera RGB-D, non 3 ToF.
- Correzione delle 2026-11-14T13:15:26+01:00 (aggiunta, non sostituzione): nella Tabella I di Schöller et al. c'è anche RED, 0,44/0,91,
  che è il miglior modello appreso deterministico confrontato (non SR-LSTM, come lasciava intendere l'elenco sopra,
  che lo ometteva). L'esito di P2(a) non cambia: la velocità costante (0,39/0,83) resta migliore.
