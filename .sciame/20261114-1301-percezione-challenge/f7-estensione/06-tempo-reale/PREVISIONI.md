# Previsioni — `sciame-tempo-reale`, estensione f7, corsia A

Scritte alle **2026-11-14T15:09:27+01:00** (`date -Is`), **prima** di scrivere e lanciare il micro-banco `banco.c`.
A quest'ora ho letto: il contratto dell'estensione, la traccia, `promptMare.txt`, `SOLUZIONE_V2.md`, gli addendum,
e a pezzi (con `grep`) `MOTO_PROPRIO.md`, `AUDIT.md`, `f3/H-012/02-validazione/VERIFICA.md` §3c. Nessuna misura fatta.

## Che cosa misuro e dove

- Macchina: AMD Ryzen AI 9 HX 370 (12 core, 24 fili; 8 fili a 5,16 GHz massimi e 16 a 3,29 GHz: `cpuinfo_max_freq`),
  governor `performance`, gcc 16.2.1, `-O2`, un filo, legato a un core con `taskset`. **Non è la macchina di
  destinazione** (che non è dichiarata): ogni tempo vale qui e basta.
- Ingresso sintetico: profondità 640×480, campo 87°×58° (foro stenopeico: fx = 337,2, fy = 433,0), sensore a 1,2 m
  inclinato di 15° in basso (blocco B1 del nucleo), rumore σ(z) = 0,00375·z² m (curva nominale del nucleo: 1,5 / 3,4 /
  6,0 cm a 2 / 3 / 4 m). Regione: 6 × 4 × 3 m davanti al sensore. Voxel da 5 e da 10 cm. 8 byte per voxel.
- Scene: «vuota» (solo pavimento, pareti oltre la regione: i raggi più lunghi), «tipica» (parete di fondo a 5,5 m, sei
  scatole mobili, un palo di 2 cm), «perturbazione» (tipica; al fotogramma 60 compaiono 40 scatole e il 5 % dei pixel
  diventa non valido). 120 fotogrammi riprodotti due volte: 240 campioni per configurazione. Seme fisso.
- Metodi: (G) griglia polare del nucleo, 1° × 0,1 m fino a 3 m; (D) lancio dei raggi con DDA su matrice densa;
  (H) lo stesso su blocchi 8×8×8 con tabella hash a indirizzamento aperto e serbatoio preallocato; (P) proiezione
  dei voxel sull'immagine con piramide dei minimi (la mia proposta). Sottocampionamento k = 1, 2, 4, 8.

## Conti a mano fatti prima (non sono previsioni: sono aritmetica)

- Voxel teorici nella regione: 120×80×60 = 576 000 a 5 cm (4,6 MB a 8 byte); 60×40×30 = 72 000 a 10 cm (0,58 MB).
- Raggi: 307 200 (k = 1); 76 800 (k = 2); 19 200 (k = 4); 4 800 (k = 8).
- Passo fra due raggi vicini a distanza Z: Z/fx. A 6 m: 17,8 mm in orizzontale, 13,9 mm in verticale. Perché il
  passo fra i raggi resti sotto il lato del voxel alla portata massima: k ≤ s·fx/Z = 2,8 (5 cm) e 5,6 (10 cm).
- Voxel attraversati da un raggio lungo L: L·(|dx|+|dy|+|dz|)/s, fra L/s e √3·L/s: su 6 m, 120–208 a 5 cm e 60–104 a
  10 cm.
- Inversione di un voxel saturo con i parametri consueti di OctoMap (colpo +0,85, mancato −0,4, saturazione −2,0 e
  +3,5: da verificare sulla fonte): da «libero» saturo a positivo servono ⌈2,0/0,85⌉ = 3 colpi (0,2 s a 15 Hz); senza
  saturazione, dopo 10 s di «libero» (150 × 0,4 = 60) ne servono 71 (4,7 s). Da «occupato» saturo a negativo:
  ⌈3,5/0,4⌉ = 9 mancati (0,6 s).

## Previsioni (misura, attesa, soglia di smentita)

| # | Misura | Attesa | Smentita se |
|---|---|---|---|
| P1 | voxel attraversati per raggio, media, scena «vuota», ritagliati alla regione | 40–90 a 5 cm; 20–45 a 10 cm | fuori dall'intervallo |
| P2 | (D) 5 cm, k = 1, scena «vuota», core veloce: tempo per fotogramma | media 40–150 ms: **non sta** in metà del periodo (33 ms) | p95 < 20 ms |
| P3 | (D) 5 cm, colpi a piena risoluzione + liberi con k = 4 (minimo del blocco) | p95 < 20 ms | p95 ≥ 33 ms |
| P4 | (D) 10 cm: k = 1 e k = 4 | k = 1: p95 fra 15 e 80 ms; k = 4: p95 < 8 ms | fuori |
| P5 | (H) contro (D), stessi raggi, 5 cm, k = 1: rapporto delle medie | 1,3–3 volte più lento | < 1,15 o > 5 |
| P6 | (G) griglia polare in C | p95 < 2 ms; (D) 5 cm k = 1 costa ≥ 30 volte (G) | (G) ≥ 5 ms, o rapporto < 10 |
| P7 | falsi «libero» in un fotogramma (voxel con un punto di superficie a piena risoluzione, etichettati liberi), scena «tipica», 5 cm | (a) somma dei log-odds senza priorità: > 0 (centinaia); (b) k = 1 con priorità al colpo: 0 per costruzione; (c) decimazione k = 4: > 0; (d) minimo del blocco k = 4 con colpo sul raggio centrale: > 0; (e) colpi a piena risoluzione + liberi a blocchi + priorità: 0 per costruzione | (a) o (c) = 0 (la prova sarebbe cieca); (b) o (e) > 0 (errore nel codice o nel ragionamento) |
| P8 | prova 10: fotogramma della perturbazione (60) contro la mediana dei 30 precedenti | (D): non cresce (≤ +10 %); (H): il massimo sta al primo fotogramma (allocazione a freddo), non alla perturbazione | (D) > 1,5 volte la mediana |
| P9 | blocchi allocati su blocchi della regione, scena «vuota», dopo 120 fotogrammi | ≥ 40 %: lo spazio visto libero va allocato, quindi lo sparso risparmia meno di 2,5 volte | < 25 % |
| P10 | (P) proiezione dei voxel, 5 cm | p95 < 15 ms; fra le tre scene la media cambia meno del 30 %; falsi «libero» come in P7: 0 | p95 > 33 ms, o scene che differiscono di oltre 2 volte, o falsi > 0 |
| P11 | interferenza: (G) a 15 Hz su un core mentre (D) 5 cm k = 1 gira senza sosta su un altro | p95 di (G) ≤ 2 volte quello da sola, e < 5 ms | p95 > 5 ms |
| P12 | tetto di memoria: (H) con il serbatoio al 50 % dei blocchi che servirebbero, scena «tipica» | falsi «libero» 0; tempo ≤ +20 %; voxel liberi in calo | falsi > 0, o tempo > 1,5 volte |
| P13 | margine di scavo: falsi «libero» rispetto alla superficie **vera** (profondità senza rumore), k = 1 con priorità, 5 cm, scena «tipica» | senza margine: > 0 (da decine a migliaia); fermando lo scavo a Z − 3σ(Z): meno di un decimo | senza margine = 0 (prova cieca), o con margine > metà |
| P14 | core lento (3,29 GHz) contro core veloce, (D) 5 cm k = 1 | 1,4–2,2 volte più lento | < 1,2 o > 3 |

Indipendenza, dichiarata prima: banco, scene, generatore del rumore e conteggio dei falsi sono dello stesso autore e
dello stesso file. P7(b), P7(e) e lo «0» di P10 sono controlli di coerenza, non dati: il riferimento («punto di
superficie a piena risoluzione») è costruito con le stesse proiezioni del metodo. Solo P13 usa un riferimento diverso
(la profondità senza rumore), ma viene dalla stessa scena e dallo stesso autore.

## Aggiunte (ogni riga con la sua ora, sempre prima della prova a cui si riferisce)

- **2026-11-14T15:21:50+01:00 — dopo la parte «tempo», prima di scrivere il metodo Q e prima di «lento», «sicurezza»,
  «interf», «tetto».** Notato DOPO (non previsto): nella scena «perturbazione» la proiezione rigida (P) lascia 2 voxel
  liberi a 5 cm e 0 a 10 cm all'ultimo fotogramma, perché con il 5 % di pixel non validi sparsi a caso quasi ogni
  impronta di voxel contiene un pixel non valido. Aggiungo il metodo **Q = proiezione «lasca»** (piramide dei minimi dei
  soli pixel validi; serve almeno un pixel valido nell'impronta). **P15:** scena «perturbazione», 5 cm, ultimo
  fotogramma: liberi(Q) ≥ 60 % dei liberi di (D) k = 1 (133 984), cioè ≥ 80 000; p95 < 10 ms; falsi sul riferimento 1
  = 0 (per costruzione: i colpi vanno prima). **Smentita se:** liberi < 50 % di (D), o p95 > 15 ms, o falsi > 0.
- **2026-11-14T15:24:56+01:00 — dopo «lasca», «lento», «sicurezza» (primo lancio), prima di «interf», «tetto» e del
  contatore senza pavimento.** Notato DOPO: (1) i due core girano entrambi a 3,30 GHz (`scaling_cur_freq` letto durante
  il lancio; `scaling_max_freq` = 3 289 474 su tutti e due): P14 non confronta due frequenze, e **tutti i tempi sono a
  3,3 GHz**; (2) nel conteggio dei falsi sul riferimento 2 (superficie vera) entrano i voxel del pavimento, colpiti di
  striscio: non sono un pericolo e gonfiano il numero. Aggiungo un terzo conteggio che esclude i voxel con il centro
  sotto 0,10 m. **P16:** scena «tipica», 5 cm, esclusi i voxel bassi: (a) somma senza priorità > 0 e almeno 10 volte
  (b3); (c) decimazione k = 4 > 0 e almeno 10 volte (e3); (p) e (q3) = 0. **Smentita se:** (a) < 10 × (b3), o
  (c) < 10 × (e3), o (p) > 0. Se (b3) o (e3) valgono 0 il rapporto si legge come «infinito» e la previsione regge.
- **2026-11-14T15:30:20+01:00 — dopo «interf» e «tetto», prima di scrivere il modo «vecchi» (prove 2 e 5: dati vecchi contro
  occlusione nuova; ramo lento).** Scena «perturbazione», 5 cm; mappa integrata fino al fotogramma 59, poi al 60
  compaiono 40 scatole. Falso «libero» = voxel etichettato libero il cui **centro sta dentro una scatola** (verità della
  scena, non del sensore). Tre letture: **L** = libero se il log-odds è negativo (la storia decide); **M3** = libero se
  visto libero in uno degli ultimi 3 fotogrammi e non colpito ora (invariante 1 del nucleo); **M1** = libero solo se
  visto libero nel fotogramma corrente. Due casi: mappa che continua a integrare; mappa ferma dal fotogramma 60 (ramo
  lento in ritardo). **P17 (mappa che integra, fotogramma 74):** L > 1000 e non scende a zero (gli interni delle
  scatole non sono mai colpiti); M3 > 0 ma meno del 10 % di L; M1 = 0 con la proiezione. **P18 (mappa ferma):** L > 1000
  a ogni fotogramma da 60 a 74; M3 > 0 a 60 e 61, poi 0 da 62; M1 = 0 da 60. **Smentita se:** L = 0 (prova cieca),
  M1 > 0, M3 ≥ L al fotogramma 74, o M3 > 0 dal fotogramma 62 a mappa ferma.
- **2026-11-14T15:31:05+01:00 — dopo il primo lancio di «vecchi», prima di aggiungere la lettura M3c.** Notato DOPO: la lettura M3
  (finestra di 3 fotogrammi) dà 1045 falsi liberi al fotogramma 60 e 934 al 61 anche con la mappa che integra, perché
  la finestra non guarda se il fotogramma corrente **contraddice** il vecchio «libero». Aggiungo **M3c** = M3, ma un
  voxel che nel fotogramma corrente ha davanti una profondità valida più vicina del suo lato lontano (cioè è occupato o
  in ombra adesso) non è libero. **P19:** con la proiezione lasca (Q), 5 cm, mappa che integra: M3c = 0 ai fotogrammi
  60–64 e 74. **Smentita se:** M3c > 0 in uno di quei fotogrammi. (A mappa ferma M3c coincide con M3: nessun
  fotogramma corrente.)

## Esiti (scritti alle 2026-11-14T15:32:56+01:00, dopo tutte le prove; file: `risultati_*.txt`)

| # | Esito | Numero |
|---|---|---|
| P1 | **smentita** | 108,4 voxel per raggio a 5 cm e 53,7 a 10 cm (attesi 40–90 e 20–45) |
| P2 | regge | 88,9 / 90,2 / 91,1 ms (media / p95 / massimo) |
| P3 | regge | p95 8,7 ms («vuota»), 7,6 ms («tipica») |
| P4 | regge | k = 1: p95 50,9 ms; k = 4: p95 5,6 ms |
| P5 | regge | 1,52 («vuota»), 1,46 («tipica») |
| P6 | regge | (G) p95 0,50 ms; rapporto 180 |
| P7 | regge (ordine di grandezza sbagliato: migliaia, non centinaia) | per fotogramma, sul riferimento 1: (a) 13 818; (c) 8 901; (d) 1 571; (b) 0; (e) 0 |
| P8 | (D) regge; (H) **smentita** | (D) 70,0 ms contro mediana 82,6; (H): primo fotogramma 111,8 ms, massimo 123,9 altrove: l'allocazione a freddo non si vede |
| P9 | regge | 736 su 1200 blocchi (61,3 %) a 5 cm; 116 su 160 (72,5 %) a 10 cm |
| P10 | regge | p95 5,7–6,0 ms; medie 5,51–5,71 ms nelle tre scene; falsi 0 |
| P11 | regge | p95 0,84 ms da sola; 0,88 con (D) su un altro core; 1,03 sul filo gemello |
| P12 | tempo e liberi: regge; falsi: **non misurato** (vale per costruzione) | tempo −4 %; liberi 89 427 contro 175 570. Notato dopo: occupati persi 0,24 % («tipica») e 8,6 % («perturbazione») |
| P13 | regge sulla soglia; attesa numerica mancata | sul riferimento 2: 5 579 → 931 (0,17: non «meno di un decimo»); sopra 0,10 m: 4 283 → 280 (0,065) |
| P14 | **smentita** | rapporto 1,00: i due core giravano entrambi a 3,30 GHz |
| P15 | **smentita** | liberi(Q) 59 672 su 130 958 = 45,6 % (soglia 50 %); p95 6,0 ms; falsi 0 |
| P16 | regge | (a) 44 482 contro (b3) 280: 159 volte; (c) 25 151 contro (e3) 118: 213 volte; (p), (q3): 0 |
| P17 | regge sulle soglie; attesa «M3 > 0 al fotogramma 74» mancata | L = 5 553; M3 = 0 (1 045 al fotogramma 60, 934 al 61, 90 al 62); M1 = 0. Con (D): M1 = 54 |
| P18 | regge | L da 6 960 a 8 783; M3 = 1 773 e 1 474 ai fotogrammi 60 e 61, poi 0; M1 = 0 |
| P19 | regge | M3c = 0 in tutti i fotogrammi controllati, a 5 e a 10 cm |

Riproduzione: «sicurezza» e «vecchi» lanciati due volte danno gli stessi conteggi (`diff` sui file `*_primo_lancio.txt`).

Rilancio di controllo (2026-11-14T15:40:42+01:00): «tempo» e «lasca» rifatti con il binario finale (`risultati_*_binario_finale.txt`);
sul p95 lo scarto mediano è 0,8 %, il massimo 18,6 % (raggi 8×8 a 5 cm, scena «vuota»: 4,62 → 3,76 ms). Nessun esito cambia.
