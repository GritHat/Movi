# Previsioni del torneo f7 — `sciame-avversario`

Scritte alle **2026-11-14T16:14:21+01:00** (`date -Is`), dopo aver letto contratto, triage, nucleo, addendum, `promptMare.txt`, `prepropostaEsterna.md`, il contratto di f8 e le consegne di nuvole-punti, creativo, requisiti, matematico; **prima di scrivere una riga di codice**. Non ho aperto i sorgenti delle corsie (salvo le righe 1–90 di `f4/H-012/01-avversario/comune_f4.py`, per vedere se il nucleo ha una quota: non ce l'ha).

Simulatore mio (`torneo.c`): camera a 1,2 m inclinata di 15°, 87° × 58°, 320 × 240, profondità valida fino a 6 m, rumore σ = 0,004·z² m, stanza 6 × 4 × 3 m, 15 fotogrammi al secondo. Verità analitica (raggio contro scatole), reticolo di prova a 5 o 10 cm sfalsato dai centri dei voxel.

Sigle delle candidate: **N0** griglia del nucleo, «libero se il suolo è visto in uno degli ultimi 3 fotogrammi» anche se ora la cella è in ombra (lettura lasca); **N1** la stessa, ma occupato e ombra correnti vincono (clausola); **Q1** V-002 su un fotogramma (minimo e massimo 3 × 3, margine 3 cm + 3σ); **Q3** V-002 con finestra di 3 fotogrammi e clausola «non contraddetto ora» (V-013); **Q3c** Q3 più «pixel centrale valido ora»; **P** profilo V-003 da Q1; **S10** tre fasce da Q1 (prudente), **S10p** tre fasce per proiezione con «attraversato = osservato» (alla lettera), **S10i** maschera ingenua (bit a zero = libero); **VO** voxel densi da 10 cm, log-odds di OctoMap, «attraversato = libero»; **VOa** VO più età ≤ 3 fotogrammi, clausola e prudenza sul voxel visto in parte; **VH** blocchi 8³ da 5 cm con tabella hash e tetto; regioni di possibile presenza: **cuneo** (nucleo), **V12** (ombra d'ingresso, V-012), **rec** (mia: Π(t) = dilata(Π(t−1)) ∖ libero-ora sul piano, da V-011).

Falso libero = punto dichiarato libero che in verità è occupato, oppure non è osservabile (nascosto, fuori campo, senza fondale).

## Le dieci prove (più l'undicesima del triage)

| # | Previsione | Smentita se |
|---|---|---|
| A1 (prova 1) | VH con interrogazione a due vie («non occupato ⇒ libero»): migliaia di punti in voxel mai allocati dati per liberi; a tre vie: 0. S10i: ≥ 1 cella «libero» con la barra a 1,7–1,9 m dentro. Q1, N1: 0 | tre vie > 0; due vie = 0 |
| A11 (prova 11) | VO: fra i suoi «libero» il 3–15 % dei punti è falso (scena ferma); VOa ≤ 0,2 %; Q1: 0; braccio Q senza 3 × 3 e senza margine: > 0 | VO < 1 %; Q1 > 0; braccio = 0 (prova cieca) |
| A2 (prova 2) | Sosta di 60 s dietro il pannello. VO con decadimento verso «libero»: > 0 fotogrammi col soggetto in voxel liberi; con decadimento verso il priore: 0; Q1, Q3, N1: 0. Possibile presenza: cuneo, V12, rec 0 fotogrammi fuori regione; braccio col timer di 10 s: circa 750 fotogrammi fuori | un fotogramma fuori per cuneo/V12/rec; braccio a 0 |
| A3 (prova 3) | VH col tetto sotto la domanda ed espulsione del blocco usato meno di recente: i blocchi in ombra (mai toccati dai raggi) escono per primi; voxel di possibile presenza persi > 0 e ≥ 1 fotogramma col soggetto nascosto fuori regione. Con i blocchi bloccati («pin») o con la regione fuori dalla mappa (V12): 0 | 0 persi senza pin |
| A4 (prova 4, K-102) | Adulto (1,7 m) dietro la cassa da 1 m, visibile dalla vita in su: N alla lettera («oltre il primo ritorno = ombra») lo dà «osservato» nello 0 % dei fotogrammi in cui ha > 500 pixel validi; con la lettura «ogni ritorno è occupato» è «osservato» ma il suo gruppo sta tutto nel cuneo (C6 lo esclude dal filtro) nel 100 %. Q1/P: «osservato» nel ≥ 99 %. Soggetto del tutto nascosto: «osservato» 0 fotogrammi per N, Q, P; VO: > 0 fotogrammi con voxel «occupato» fantasma nell'ombra (senza etichetta d'età) | N alla lettera > 10 %; Q1 < 95 %; VO = 0 |
| A5 (prova 5) | (a) Scatola che compare su una zona vista libera per 60 fotogrammi: VO tiene «liberi» punti dentro o dietro la scatola per sempre (> 100 punti dopo 30 fotogrammi); N0 e Q3 senza clausola: > 0 per 2 fotogrammi, poi 0; N1, Q1, Q3, VOa: 0. (b) **Attacco nuovo:** mobile a 1,4 m/s e 30 % di pixel non validi sparsi: Q3 (con la clausola) dichiara liberi punti dentro il corpo in ≥ 10 % dei fotogrammi, perché un pixel non valido non può contraddire; Q1: 0; Q3c: 0 punti a più di 5 cm dentro | VO = 0; Q3 = 0 in (b); Q1 > 0 |
| A6 (prova 6) | Imbardata di 1° non segnalata al fotogramma 30, scena ferma: VO (mappa nel mondo) > 50 falsi liberi persistenti; Q1 nel riferimento vero del sensore 0; Q3 e N1 0; senza clausola (N0) > 0 per 2 fotogrammi | VO = 0; Q1 > 0 |
| A7 (prova 7) | Due occlusori adiacenti, A entra a sinistra e B a destra, si scambiano dietro. Regola «una traccia pendente **per ombra d'ingresso**»: scambio muto nel ≥ 95 % di 200 corse; regola globale del nucleo («una sola traccia pendente»): 0 muti, 100 % «identità ambigua» | per ombra < 50 %; globale > 0 |
| A8 (prova 8) | Lastra di vetro (invisibile alla profondità): tutte le candidate danno «libero» nei punti della lastra (> 0 per N, Q1, P, S10, VO). Nessuna lo risolve | una candidata a 0 |
| A9 (prova 9) | (a) Tutto non valido dal fotogramma 30: Q1 0 liberi subito; Q3, N: liberi per 2 fotogrammi, poi 0; VO: liberi per sempre; VOa: 2 fotogrammi. (b) Coperto con profondità valida a 2 cm: Q1, Q3, N1, VOa 0 subito; VO per sempre. (c) Fotogramma congelato mentre entra un mobile: tutte dichiarano liberi punti dentro il corpo finché non scatta «3 fotogrammi identici» (2 fotogrammi) | Q1 > 0 in (a); VO torna a 0 da sola |
| A10 (prova 10) | Tempo per fotogramma, massimo / mediana nello scenario C: Q1 e Q3 ≤ 1,35; N ≤ 1,35; VO ≤ 1,5; VH > 1,35 (raffica di allocazioni). Tempi indicativi: la macchina ha altri processi | Q > 1,35 con mediana stabile |

## S10 (V-005)

| # | Previsione | Smentita se |
|---|---|---|
| S10-a | Con la fascia alta pertinente (fino a 2 m): 0 celle «libero» entro 3 m (il bordo alto del campo è 1,2 + 0,249·r < 2 m per r < 3,21 m) | ≥ 1 cella |
| S10-b | Fascia alta non pertinente: barra a 1,7–1,9 m di quota a 1,5 m → ≥ 1 cella «libero» con la barra dentro la colonna | 0 celle |
| S10-c | Barra a 1,52–1,58 m a 1,3 m (bordo del campo): S10 prudente non dà «libero» (0 celle sotto la barra); S10p alla lettera ≥ 1. Con basso + medio non c'è «libero» fra 1,24 e 1,61 m | S10 prudente ≥ 1 |
| S10-d | Scatola alta 0,10 m a 2 m: N la dà occupata; S10 (fascia bassa da 0,15 m) dà «libero» ≥ 1 cella sopra la scatola | S10 = 0 celle |

## Possibile presenza, scene dinamiche

| # | Previsione | Smentita se |
|---|---|---|
| PP1 | Sosta 60 s dietro il pannello alto, poi pannello tolto: cuneo, V12, rec: 0 fotogrammi col soggetto nascosto fuori regione; regione sparita entro 3 fotogrammi (+2 di tolleranza) dove il suolo torna visto; braccio «sagoma ristretta di 20 cm» fallisce | fuori > 0; braccio = 0 |
| PP2 | Pedana bassa (0,5 m), carrello da 0,25 m nascosto dietro: l'ombra vera si chiude prima di 3 m; cuneo/ombra vera > 1,5 in area; V12/vera fra 0,8 e 1,6 | V12 fuori dall'intervallo |
| PP3 | **Attacco nuovo — sensore coperto 2 s** mentre il carrello passa dall'ombra chiusa della pedana all'ombra del pannello: cuneo e V12 lo lasciano fuori regione (> 0 fotogrammi) e V12 continua a dire «ombra chiusa»; rec: 0 fuori | cuneo e V12 a 0 |
| PP4 | **Attacco nuovo — occlusore mobile** (scaffale che trasla a 0,5 m/s con il soggetto dietro): cuneo e V12 fuori regione in > 50 % dei fotogrammi di occultamento; rec: 0 | cuneo o V12 < 10 % |

## Scenari degradati (soglie)

- **A, azzeramento dal 100 % allo 0 %, sparso e a chiazze, con un mobile:** falsi liberi «profondi» (punto a più di 5 cm dentro un corpo, o nascosto): Q1 0 a ogni passo; Q3 > 0 col rado da 70 % di validi in giù; N1 0; VO > 0 a ogni passo. Resa di Q1 col 90 % di validi sparsi: 30–45 % (0,9⁹ = 39 %); a chiazze: > 80 %. Q3: 70–85 %. N: > 95 % fino al 30 % di validi.
- **K-106 (calcolo, poi misura):** 5 % di buchi sparsi → Q1 tiene 0,95⁹ = 63 % (< 70 %: no), Q3 ≥ 90 %; chiazze 20 × 20 sul 5 % → Q1 ≥ 85 % (sì).
- **B, tre mobili dietro cassa, pedana, pannello:** soggetto del tutto nascosto con un punto in «libero»: 0 per N1 (lettura «suolo»), Q1, Q3c, P, S10; VO > 0. «Nascosto a torto» (ombra dichiarata ma punto visibile) per N: > 30 % della sua ombra.
- **C, dieci oggetti che compaiono con il 50 % di pixel persi per 1 s:** punti dentro un oggetto dati liberi nei 2 fotogrammi dopo: Q1 0; Q3 > 0 (rado); N0 > 0, N1 0 col rado; VO > 0 per > 10 fotogrammi. Tempo massimo di Q ≤ 1,35 × mediana.

## K-105 e V-011 in forma minima

N1: celle «libero» al fotogramma t occupate entro 3 fotogrammi (0,20 s) da un soggetto che a t non aveva pixel validi (mai tracciato, esce da un'ombra): **> 0** nello scenario B. Con il margine v·h + 5 cm attorno a ogni bordo del non osservato (0,33 m a 1,4 m/s): 0. Libero conservato: 45–75 % a 1,4 m/s, 20–50 % a 2,5 m/s (0,55 m). Smentita: N1 = 0, o margine > 0.

## Q2

- **S11 (T-005):** `SOSTA_IN_OMBRA` scatta dal peso μ2. Soggetto che esce dal lato lontano di un'ombra aperta, oltre la portata, senza fermarsi: la macchina emette comunque «sosta in ombra» (previsto: 100 % delle corse, entro 3 s). Smentita: < 50 %.
- **T-001:** `grep` sulla traccia e sull'apertura proposta: almeno due frasi della traccia coperte solo a parole («oggetti», «ispezione», «aerospaziali», «bassa latenza»). È un'analisi, non una misura.

## Aggiunte dopo i primi tre lanci (statica, s10, a5) — scritte alle 2026-11-14T16:25:38+01:00, prima di lanciare le varianti

Esiti già visti (non sono previsioni): S10-b **smentita** nella posizione scritta (barra a 1,5 m: 0 celle, perché lì la fascia media non è vista tutta); A5b **smentita** col rado (0 falsi), mentre con le chiazze Q3 e VOa cedono (variante già nel codice, senza previsione sua).

| # | Previsione nuova | Smentita se |
|---|---|---|
| S10-b2 | Barra a 1,7–1,9 m di quota a 2,0 m e a 2,5 m di distanza (fascia alta non pertinente): S10(B+M) dà «libero» ≥ 1 cella con la barra nella colonna, in tutti e due i casi; a 2,5 m la barra è in parte **vista** e la cella resta «libero» | 0 celle in uno dei due casi |
| A5c | «Soggetto nero»: i pixel che cadono sul corpo del mobile (1,4 m/s) sono non validi, il resto è valido. N0, N1, Q3, VOa: punti a più di 5 cm dentro il corpo dati liberi in ≥ 50 % dei fotogrammi; Q1, Q3c, S10: 0; VO > 0 | N1 o Q3 a 0; Q1 o Q3c > 0 |

## Aggiunta alle 2026-11-14T16:30:34+01:00 (dopo a6, a8, a9, a2, pp, a3, a4; prima di K-102 dedicata e degli scenari)

Esiti già visti: A4 ha solo 7 fotogrammi utili (N alla lettera 1 su 7): campione troppo piccolo per la soglia del 10 %. Rifaccio K-102 con una prova dedicata (`k102`): cassa da 1 m al centro, adulto a 0,5 m/s sulla corsia dietro, contati solo i fotogrammi in cui tutta l'impronta dell'adulto sta nell'ombra al suolo della cassa e l'adulto ha più di 500 pixel validi. **Previsione (la stessa di A4, soglia invariata):** N alla lettera «osservato» in ≤ 10 % di quei fotogrammi; N «ogni ritorno» occupato ma tutto nel cuneo in ≥ 90 %; Q1 e P «osservato» in ≥ 99 %.

## Aggiunta alle 2026-11-14T16:32:27+01:00 (dopo k102, scenB, scenC, k106, k105; prima di «k106 3c», scenA, a10)

Esiti già visti: col 5 % di buchi sparsi il profilo P (costruito su Q1) tiene lo 0,1 % del libero e S10 lo 0,0 %; il margine di V-011 conserva lo 0,4 % del libero nello scenario B (previsto 45–75 %: **smentita**). **Previsione nuova:** P e S10 costruiti su Q3c (finestra di 3 fotogrammi, clausola, pixel centrale valido ora) tengono col 5 % sparso almeno 25 % (P) e 15 % (S10) del libero vero, con 0 fotogrammi di falso libero profondo anche con le chiazze. Smentita: resa sotto quelle soglie, o un fotogramma con un falso profondo.

## Aggiunta alle 2026-11-14T16:34:51+01:00 (dopo scenA e a10; prima di `prova7.py` e `s11.py`)

Esiti già visti: P su Q3c tiene lo 0,8 % col 5 % sparso (previsto ≥ 25 %: **smentita**); Q3 supera 1,35 nel rapporto massimo/mediana (2,0–2,2: **smentita**, in assoluto 1,3 ms).
- **A7, precisazione:** oltre alla regola «per ombra» provo la stessa regola con una porta cinematica al 99 % sulla posizione prevista (q = 0,2 m²/s³). Previsione: la porta non salva (scambi muti ancora ≥ 50 %), perché dopo 1,5–2,5 s di buio la porta è larga più dell'ombra.
- **S11, terzo caso (c):** transito normale in cui il soggetto rallenta dietro il pannello (fattore 0,6–1,0) e la velocità d'ingresso è stimata con errore di 0,15 m/s. Previsione: «sosta in ombra» emessa a torto prima della ricomparsa in ≥ 10 % dei transiti. Smentita: < 3 %.

## Aggiunta alle 2026-11-14T16:35:41+01:00 (prima del braccio di controllo per «rec»)

**PP5, braccio che deve fallire per la mia regione «rec»:** come PP3, ma il carrello corre a 3 m/s (1,34 m in 0,45 s) e il sensore resta coperto solo 8 fotogrammi; la dilatazione di una cella per fotogramma copre 1,5 m/s. Previsione: «rec» lascia il carrello fuori regione in > 0 fotogrammi dopo la copertura (se resta a 0, la prova PP3 era cieca per «rec»).

## Aggiunta alle 2026-11-14T16:36:14+01:00

Esito di PP5: **smentita** (rec resta a 0 anche a 3 m/s): il braccio era debole, perché fra l'ombra della pedana e quella del pannello ci sono solo 0,16 m e in 8 fotogrammi la regione cresce di 0,8 m. **PP6, braccio più duro:** il carrello fa lo stesso salto durante **un solo** fotogramma coperto (la regione cresce di 0,1 m, meno del varco). Previsione: rec lo perde (> 0 fotogrammi fuori). Se resta a 0, «rec» copre troppo e lo zero di PP3 e PP4 non prova niente.

## Registro delle correzioni al banco (annotato alle 2026-11-14T16:44:26+01:00, a prove finite: non sono previsioni)

1. **A2:** il primo lancio campionava punti al centro del corpo, in voxel mai visti («sconosciuto» in ogni variante); corretto campionando la faccia anteriore, poi rilanciato.
2. **A3:** nel primo lancio il tetto era fissato dopo la scrittura della possibile presenza e non mordeva mai (0 espulsioni); corretto fissandolo prima.
3. **PP1:** il braccio «sagoma ristretta di 20 cm» non falliva (soggetto a 0,16 m dal bordo, celle da 10 cm); soggetto spostato a x = −0,505 m. Il conteggio delle celle residue dopo la rimozione del pannello era falsato dal riaggancio: disattivato in quella sola misura.
4. **A4:** 7 fotogrammi utili; rifatta come `k102` (31 fotogrammi), con la misura di P estesa a tutta l'impronta.
5. **A8:** aggiunta la lastra a 2,0 m, perché a 1,5 m S10 non dichiara mai «libero» e lo zero non voleva dire niente.
6. I file `risultati_*.txt` sono quelli dell'ultimo rifacimento completo (`rifai.sh`, 16:37–16:41): conteggi identici ai lanci precedenti, tempi diversi.
