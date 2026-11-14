# Previsioni di sciame-creativo (f7, corsia B) — scritte prima delle prove

Ora di scrittura: 2026-11-14T15:10:20+01:00 (`date -Is`, lanciato subito prima di scrivere questo file). Nessuna prova era stata eseguita.

Prova unica: `prova_ombra.c` (C, un solo processo, seme fisso 1). Scena sintetica: sensore a (0, 0, 1,2 m), inclinato di 15° verso il basso, campo 87° × 58°, immagine di profondità 320 × 240; pavimento piano; una scatola bassa (0,3 m), un pannello 1 × 2 m a 2 m, una barra alla quota della testa (1,70–1,85 m) a 1,5 m, una «persona» nascosta dietro il pannello. Regione d'interesse 6 × 4 × 3 m, voxel da 5 e da 10 cm. Due varianti: senza rumore; con rumore σ = 0,00375·z² m e 5 % di pixel non validi.

Metodi a confronto, sullo stesso fotogramma:
- **A** = griglia voxel densa con lancio dei raggi (riferimento di ciò che chiede `promptMare.txt`), «occupato» vince su «libero», libero solo fino a D − ε.
- **B** = idea creativo-1: nessuna mappa; interrogazione del buffer di profondità (minimo e massimo su 3 × 3 pixel) per ogni punto.
- **Verità** = visibilità analitica del centro del voxel (dentro una scatola; fuori campo; nascosto; visibile e vuoto).

| # | Idea | Misura | Previsto | Smentita se |
|---|---|---|---|---|
| P1 | creativo-1 | centri che B chiama «libero» mentre la verità è occupato, nascosto o fuori campo | 0, a 5 e a 10 cm, con e senza rumore | ≥ 1 |
| P1b | creativo-1 | costo di prudenza di B: quota dei centri davvero visibili e vuoti che B NON chiama «libero» | ≤ 10 % senza rumore, ≤ 20 % con rumore | > 25 % |
| P2 | critica alla griglia voxel | centri che A chiama «libero» mentre la verità è occupato o nascosto (effetto del bordo del voxel) | più di 0 e meno del 5 % dei «libero» di A, a 5 cm | 0 oppure ≥ 5 % |
| P3 | critica alla sparsità | blocchi 8³ toccati da A (libero od occupato) sul totale dei blocchi della regione, a 5 cm | fra il 30 % e il 55 % (la sparsità risparmia meno di 3,3 volte, prima dell'indice) | < 30 % o > 55 % |
| P4 | creativo-1 | tempo per fotogramma di B per ciò che serve (minimo/massimo 3 × 3, sagoma su tutte le celle della zona, ombra al suolo) contro l'aggiornamento di A a 5 cm | B ≤ 1/5 di A | B > 1/5 di A |
| P4b | creativo-1 | tempo di B per interrogare TUTTI i 576 000 centri contro l'aggiornamento di A | fra 0,5 e 2 volte A (nessun vantaggio se si chiede tutto) | fuori dall'intervallo |
| P5 | creativo-1 | celle polari (1° × 0,1 m, fino a 3 m) «in ombra» dietro la scatola bassa: B contro il cuneo del nucleo | B fra il 35 % e il 65 % del cuneo; verità entro ± 15 % di B | fuori dall'intervallo |
| P6a | creativo-2 | montaggio orizzontale: celle da 10 cm della zona 1,24–3 m che la regola del nucleo dà «libero» mentre nella colonna 0,07–1,9 m c'è la barra | ≥ 5 celle | < 5 |
| P6b | creativo-2 | celle che la sagoma dà «verificata libera per intero» mentre la colonna contiene un oggetto | 0 (orizzontale e verticale) | ≥ 1 |
| P6c | creativo-2 | quota delle celle della zona in cui la sagoma di 1,9 m è verificabile per intero | orizzontale: 3–7 %; verticale (87° in altezza): ≥ 90 % | fuori dall'intervallo |
| P7 | creativo-1 | punti della «persona» nascosta dietro il pannello: stato secondo B | 100 % «in ombra», 0 «libero», 0 «fuori campo» | altro |
| P7-controllo | braccio che deve fallire | stessa misura senza il pannello | meno del 50 % «in ombra» (se resta 100 %, la prova è cieca) | ≥ 50 % |

Conti a mano che la prova deve ritrovare (scritti prima): ostacolo a 1,8 m visibile solo oltre 0,6 / tan 14° = 2,41 m; sagoma di 1,9 m verificabile solo oltre 0,7 / tan 14° = 2,81 m; ombra al suolo di un ostacolo alto h a distanza d con sensore a quota H: finisce a d·H / (H − h); scatola di 0,3 m a 1,7 m: 2,27 m.

Idea creativo-3 (Q2, giuria): la prova chiede persone esterne alla squadra, non la posso eseguire. Previsione scritta ora per chi la farà: tre persone senza contesto, dopo il video di tre minuti senza spiegazioni, rispondono giusto ad almeno 3 domande su 4 (che cosa sorveglia; che cosa vuol dire il tratteggio; è provato su un veicolo in moto; funziona oggi per una persona non vedente) in almeno 2 casi su 3. Smentita: meno di 2 su 3.

Indipendenza: A, B, verità e scena sono dello stesso autore, nello stesso file; la verità usa un'intersezione raggio–scatola diversa dal confronto di profondità di B, ma condivide scena, modello di camera e modello di rumore. La prova vale per i difetti della rappresentazione, non per quelli del sensore vero.

---

## Esiti del primo giro (lancio delle 2026-11-14T15:12:07+01:00, file `risultati_ombra_giro1.txt`, sorgente `prova_ombra_giro1.c`)

**Errore mio nel lancio:** il ciclo di shell passava i tre argomenti come una stringa sola (zsh non la spezza), quindi hanno girato solo «senza rumore» e «con rumore», sempre con montaggio orizzontale e con il pannello. Le righe ripetute del file sono lanci identici, non conferme. Il montaggio verticale e il braccio senza pannello NON sono stati provati nel primo giro.

| # | Esito | Numero |
|---|---|---|
| P1 | **regge** | 0 falsi liberi di B su 576 000 e su 72 000 centri, con e senza rumore |
| P1b | **smentita** | visibili non detti liberi: 60,9 % senza rumore, 78,1 % con rumore (previsto ≤ 10 % e ≤ 20 %) |
| P2 | **regge** a 5 cm (di poco) | 4,47 % dei «libero» di A ha il centro nascosto o fuori campo (684 + 2403 su 69 074); a 10 cm 9,32 % |
| P3 | **smentita** | blocchi toccati 20,8 % a 5 cm (previsto 30–55 %); 29,4 % a 10 cm |
| P4 | **regge** | B 0,43 ms contro A 30,4 ms (mediana) a 5 cm |
| P4b | **smentita** | B su tutti i centri 3,1 ms contro 30,4 ms: rapporto 0,10, fuori da 0,5–2 (B più rapido del previsto) |
| P5 | **regge** senza rumore, **smentita** con rumore | 143 celle su 283 (50,5 %), verità 164; con rumore 82 su 285 (28,8 %); in tutti e due i casi 164 celle nascoste su 164 non sono dette «libero» |
| P6a | **regge** | 16 celle «libero» sotto la barra (19 con un oggetto nella colonna) |
| P6b | regge **a vuoto** | 0 falsi, ma su 0 celle verificate: non prova niente |
| P6c | **smentita** (orizzontale); verticale non provato | 0,0 % (previsto 3–7 %) |
| P7 | **regge** senza rumore, **smentita** con rumore | 100 % in ombra; con rumore 59,2 % in ombra e 40,8 % «buco», 0 «libero» |
| P7-controllo | non eseguito | errore del lancio |

**Notato dopo (non era previsto).**
1. La scena non aveva pareti né soffitto: il 32,2 % dei raggi non incontra niente entro 6 m e non dà profondità. Lungo quei raggi né A né B possono dire «libero» (evidenza negativa solo dove la profondità è valida): è la causa di P1b, P3 e P6c. È un fatto del sensore, non della rappresentazione: «libero» si prova solo dove il raggio finisce su un fondale.
2. Con il 5 % di pixel non validi la regola prudente «tutti e nove i pixel validi» scarta 1 − 0,95⁹ = 37 % delle interrogazioni: è la causa delle smentite con rumore di P5 e P7. Il costo è in «buco», mai in «libero».
3. Il braccio di controllo di P7 era mal progettato: senza pannello i punti interni della persona stanno comunque dietro la sua faccia visibile, quindi restano «in ombra». **Lo ritiro prima di lanciarlo.**

## Previsioni del secondo giro — scritte alle 2026-11-14T15:13:40+01:00 (`date -Is` del comando che ha aggiunto questo blocco), prima di scrivere e di lanciare la variante

Varianti aggiunte al sorgente dopo il primo giro: stanza chiusa (parete di fondo a 4 m, pareti laterali a ± 3 m, soffitto a 3 m); fusione di 3 fotogrammi per B (un pixel vale se è valido in almeno uno; minimo e massimo sui validi); braccio «B ingenuo» (un solo pixel, ε = 0, pixel non valido = libero fino alla portata).

| # | Misura | Previsto | Smentita se |
|---|---|---|---|
| S1 | stanza, senza rumore, 5 cm: falsi liberi di B; visibili non detti liberi da B | 0; ≤ 10 % | ≥ 1; > 15 % |
| S2 | stanza, senza rumore, 5 cm: blocchi 8³ toccati da A; falsi liberi di A | 30–55 %; fra 2 e 6 % dei suoi «libero» | fuori dagli intervalli |
| S3 | stanza, rumore, fusione di 3 fotogrammi, 5 cm: falsi liberi di B; visibili non detti liberi; persona nascosta | 0; ≤ 20 %; ≥ 95 % «in ombra» e 0 «libero» | ≥ 1; > 25 %; < 95 % o ≥ 1 libero |
| S4 | stanza, senza rumore: ombra al suolo dietro la scatola bassa, B sul cuneo | 35–65 % | fuori |
| S5 | stanza, senza rumore, orizzontale: celle con sagoma di 1,9 m verificata per intero | 1–3 % della zona (conto rifatto: circa 10 celle su 570) | fuori |
| S6 | stanza, senza rumore, verticale: celle con sagoma verificata per intero; di queste, con un oggetto nella colonna | ≥ 90 % delle colonne senza oggetti; 0 | < 90 %; ≥ 1 |
| S7 | stanza, verticale: celle «libero» del nucleo sotto la barra | 0 (la barra entra nel campo: 1,2 + 1,5·tan 28,5° = 2,01 m) | ≥ 1 |
| S8 | braccio che deve fallire: B ingenuo, stanza, rumore, un fotogramma, 5 cm | falsi liberi ≥ 1000; persona nascosta con ≥ 1 % di punti «libero» | meno: allora il contatore dei falsi liberi è cieco |

## Terzo giro — previsioni scritte alle 2026-11-14T15:15:18+01:00, prima di scrivere e lanciare le due prove

| # | Misura | Previsto | Smentita se |
|---|---|---|---|
| S9 | stanza VUOTA (senza scatola, pannello, barra, persona), senza rumore: celle della zona con sagoma di 1,9 m verificata per intero | verticale: 70–90 %; orizzontale: 1–3 % | fuori |
| S10 | `prova_logodds.py`: un raggio, voxel da 5 cm, 15 Hz, parametri predefiniti di OctoMap (colpo 0,7, mancato 0,4, limiti 0,1192 e 0,971), spazio prima visto libero fino a saturazione; un corpo spesso 0,30 m si avvicina a v m/s. Misura: quota dei fotogrammi in cui il voxel che contiene la faccia del corpo ha probabilità > 0,5 | v = 1,0 m/s: 0 %; v = 0,5 m/s: 0 %; v = 0,2 m/s: > 50 %; a 10 cm e 1,0 m/s: 0 % | a 1,0 m/s e 5 cm più del 10 % |
| S10b | stessa prova: voxel dentro il corpo (occupati davvero, non più visibili) che la mappa tiene con probabilità < 0,5 | a 1,0 m/s: tutti (6 su 6 a 5 cm) | meno della metà |

---

## Esiti del secondo giro (lancio delle 2026-11-14T15:14:04+01:00, file `risultati_ombra_giro2.txt`)

| # | Esito | Numero |
|---|---|---|
| S1 | **regge** | 0 falsi liberi di B; visibili non detti liberi 4,6 % |
| S2 | **regge** | blocchi toccati 39,1 % (469 su 1200); falsi liberi di A 4,83 % dei suoi «libero» (10,13 % a 10 cm) |
| S3 | falsi liberi e persona: **regge**; prudenza: **non risolta** | 0 falsi liberi; 21,4 % (previsto ≤ 20 %, soglia di smentita 25 %); persona 100 % in ombra (verticale: 99,9 %, 2 punti «buco»), 0 «libero» |
| S4 | **regge** | 143 celle su 283 (50,5 %); verità 164 |
| S5 | **regge** | 7 celle su 570 (1,2 %) |
| S6 | quota: **smentita**; falsi: **regge** | 112 celle su 376 (29,8 % della zona; 35 % delle 317 colonne senza oggetti; previsto ≥ 90 %); 0 con un oggetto nella colonna |
| S7 | **regge** | 0 celle «libero» sotto la barra con il montaggio verticale |
| S8 | **regge** (il braccio fallisce, come deve) | B ingenuo: 2561 falsi liberi a 5 cm (190 su occupato, 2371 su nascosto); persona nascosta 107 punti «libero» su 1782 (6,0 %) |

Lanciato per errore anche il braccio di controllo di P7 che avevo ritirato (senza pannello): persona 98,4 % «in ombra», come scritto nel ritiro: quel braccio era cieco.

## Esiti del terzo giro (lancio delle 2026-11-14T15:15:18+01:00, file `risultati_giro3.txt`)

| # | Esito | Numero |
|---|---|---|
| S9 | **regge** | stanza vuota: verticale 300 celle su 376 (79,8 %); orizzontale 10 su 570 (1,8 %) |
| S10 | 1,0 e 0,5 m/s: **regge**; 0,2 m/s: **non regge** (46 %, previsto > 50 %; la soglia di smentita era scritta solo per 1,0 m/s) | faccia «occupata» nello 0 % dei fotogrammi a 0,5, 1,0 e 1,5 m/s (5 cm) e a 1,0 e 1,5 m/s (10 cm); a 10 cm e 0,5 m/s: 33 % |
| S10b | **regge** | voxel dentro il corpo tenuti «liberi»: 265 su 265 a 1,0 m/s (5 cm), 130 su 130 (10 cm) |

**Notato dopo il secondo e il terzo giro (non previsto).** La smentita di S6 ha una causa che S9 separa in parte: nella stanza vuota la sagoma è verificabile sul 79,8 % della zona (il resto è il bordo del campo); con gli oggetti scende al 29,8 %, perché le colonne dietro barra, pannello e scatola sono in parte nell'ombra. Non ho scomposto oltre.
