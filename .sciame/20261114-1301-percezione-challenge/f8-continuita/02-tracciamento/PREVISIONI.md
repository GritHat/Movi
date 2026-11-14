# Previsioni di sciame-tracciamento — f8 (continuità visiva), corsia A

Scritte alle 2026-11-14T15:17:23+01:00 (`date -Is`), PRIMA di scrivere il codice della prova e di ogni lancio. Ho già letto: contratto f8,
SOLUZIONE_V2, VERDETTO, TORNEO parti 2 e 3, `scena_parte3.py`, `risultati_main1_parte3.txt` (i numeri lì dentro li conosco: le previsioni
che li ripetono valgono come controllo di riproduzione, non come previsioni nuove; le marco [rip.]).

## Scena e metodi fissati prima

Scena dell'avversario (`scena_parte3.py`, copiato in `prove/`): sensore fermo in (0,0), campo ±43,5°, portata 6 m, pannello a 2 m largo 1 m
(ombra 7,8 m²) o 2 m, pedone puntiforme a 4 m, 1,0–1,5 m/s, 15 Hz, σ = 5 cm, Pd 0,9. Traiettorie: `truth()` dell'avversario per
prosegue, sosta (2–4 s), torna, lontano (NON è mio); generatore MIO, dichiarato, per rallenta (a 0,2–0,5 m/s in un punto a caso dell'ombra),
svolta (±45–90° verso il sensore o via, in un punto a caso dell'ombra) e sosta lunga (6–10 s). τ = tempo dall'ingresso in ombra; misure a
τ = 0,5, 1, 2, 3, 4, 5 s solo se il soggetto è ancora non visibile.

Parametri dei predittori fissati QUI, a priori, non tarati sulla prova:
- (a) Kalman a velocità quasi costante, q = 0,2, lasciato correre; regioni = cerchi a χ²(2) 50 % (1,386) e 90 % (4,605).
- (b) lo stesso, regione ∩ celle non viste libere; punto proiettato sulla cella non libera più vicina. Regola del nucleo: mostrato finché il
  cerchio al 95 % ritagliato copre < metà dell'ombra, poi «perso» assorbente.
- (c) IMM a 5 modi sullo stesso stato [x,y,vx,vy]: prosegue (+v), fermo (0), torna (−v), svolta (±90°); probabilità iniziali
  0,90/0,04/0,02/0,02/0,02; tassi: prosegue→fermo 0,25/s, prosegue→torna 0,05/s, prosegue→svolta 0,05/s per lato, fermo→prosegue 0,2/s,
  fermo→torna 0,2/s, svolta→prosegue-nel-nuovo-verso: nessuna (resta), torna→fermo 0,1/s; q = 0,2 nei modi in moto, 0,02 nel modo fermo.
  I pesi dei modi si aggiornano con l'evidenza negativa: peso × (1 − Pd·massa del modo su celle viste libere). Le gaussiane non si troncano.
  Punto = media della miscela. Regione = celle di 0,25 m a densità più alta, fuori dalle celle viste libere, fino a massa p.
- (d0) particelle (500), solo moto a velocità quasi costante q = 0,2, evidenza negativa (peso × 0,1 su celle viste libere).
- (d1) + modo «sosta» con i tassi dell'avversario (0,25/s e 0,4/s).
- (d2) + modo «sosta» + «svolta»: una particella in moto cambia direzione a 0,15/s (40 % inversione, 60 % ±45–90°); alla ripartenza dalla sosta
  (0,3/s): 60 % stessa direzione, 25 % inversione, 15 % svolta; velocità limitata a 2,5 m/s. Punto = media pesata (proiettata se cade su libero).
  Regione = celle di 0,25 m a massa più alta fino a p.
- (e) raggiungibile: disco di raggio v_max·(t − t_ultima misura) + 3σ, v_max = 2,5 m/s, ∩ celle non viste libere.
- Linee di base del punto: «fermo all'ultima misura»; (a).
- Punteggio complessivo: −log della massa assegnata alla cella di 0,25 m che contiene il vero, con pavimento 1e-4 (uguale per tutti).
- Soglia utile dell'errore del punto, dichiarata ora (ombra larga 2 m alla distanza del soggetto): mediana ≤ 0,5 m fino a 1 s, ≤ 1,0 m fino a 5 s.

## Previsioni (misura · attesa · che cosa la smentisce)

- **T1 (continuità del nucleo).** Quota dei cicli senza osservazione in cui la regola «meno di metà dell'ombra» emette una stima: < 60 % per
  «prosegue» e < 35 % per «sosta» (pannello 1 m). Smentita: ≥ 90 % in uno dei due. Tutti gli altri metodi: 100 % per costruzione.
- **T2 (a, efficacia).** Errore mediano del punto di (a): «prosegue» < 0,3 m a 1 s; «sosta» > 1,0 m a 2 s e > 2,0 m a 3 s; «torna» > 2 m a 2 s.
  Punto di (a) su cella vista libera in > 50 % dei casi a 2 s per «sosta» [rip.: 92,9 %]. Smentita: sosta < 0,7 m a 2 s.
- **T3 (a, taratura).** Copertura del cerchio al 90 %: «prosegue» ≥ 0,90; «sosta» 0,70–0,90; «torna» < 0,70 a 2 s; «lontano» < 0,6 a 3 s.
  Area del cerchio al 90 % > area dell'ombra a 3 s. Smentita: torna ≥ 0,85 a 2 s.
- **T4 (c, IMM).** Errore mediano a 3 s su «sosta» inferiore di almeno il 40 % a quello di (a); copertura al 90 % ≥ 0,85 per prosegue, rallenta,
  sosta; < 0,85 per «lontano» a 3 s; media della miscela su cella libera < 5 % dei cicli. Smentita: guadagno < 20 % o sosta < 0,75.
- **T5 (d1).** Copertura 90 %: ≥ 0,85 per prosegue, sosta, torna; «lontano» a 3 s < 0,50 [rip. sul 95 %: 22–41 %].
- **T6 (d2, la mia proposta).** Copertura 90 %: «lontano» a 3 s ≥ 0,75; ogni altro comportamento a ogni τ ≥ 0,85 (≥ 0,80 se n < 100).
  Copertura 50 % fra 0,40 e 0,65 in aggregato. Area della regione al 90 % ≤ 0,80 dell'ombra a 3 s (pannello 1 m) e ≤ 0,45 a 1 s.
  Smentita: «lontano» < 0,60; un comportamento (n ≥ 100) < 0,75; area ≥ 0,95 dell'ombra a 2 s.
- **T7 (efficacia di d2).** Errore mediano del punto di d2, miscela uniforme dei comportamenti: ≤ 0,5 m a 0,5 e 1 s; ≤ 1,0 m a 2–5 s; a τ ≥ 2 s
  non peggiore della migliore fra le due linee di base (fermo, velocità costante). Per il solo «prosegue» d2 è PEGGIORE di (a) (la media è
  tirata indietro dal modo sosta): errore mediano 0,2–0,6 m a 1,5 s contro < 0,3 m. Smentita: mediana > 1,0 m a qualche τ, o d2 peggiore di
  «fermo» a τ ≥ 2 s.
- **T8 (regolarità).** Passo per ciclo del punto mostrato oltre v_max·dt = 0,167 m: 0 % dei cicli per (a) e (c); < 1 % per d2. Passi all'indietro
  (contro il passo precedente) oltre 3 cm: < 5 % dei cicli per d2 con 500 particelle; < 1 % con un lisciamento esponenziale (α = 0,3) del punto.
  (a) non si ferma mai: su «sosta» il punto mostrato esce dall'ombra. Smentita: d2 ≥ 10 % di passi all'indietro.
- **T9 (ricomparsa e identità).** Salto fra punto e prima misura: (a) su «prosegue» mediana < 0,3 m; d2 0,3–0,8 m. Prima misura dentro la regione
  al 90 % di d2: ≥ 0,85 in aggregato. Cancello d'identità (≥ 1 % della massa entro 0,5 m): d2 ≥ 0,97 con il pannello da 1 m e ≥ 0,90 con 2 m,
  per ogni comportamento (d1 su sosta con 2 m: 76 % [rip.]). Smentita: un comportamento < 0,85 (1 m) o < 0,75 (2 m).
- **T10 (costo).** d2 con 500 particelle: < 1 ms per ciclo e per traccia in C su questa macchina (bilancio 66,7 ms). Smentita: > 5 ms.
- **T11 (punteggio).** Punteggio medio (−log, più basso è meglio) a τ ≥ 2 s: d2 < d1 < (a) nella miscela uniforme. Smentita: (a) migliore di d2.

Esiti e note «viste dopo»: in fondo a questo file, aggiunti dopo le prove, senza toccare le righe sopra.

---

## Esiti del primo lancio (prove/ris_T1_v1.txt, 15:21; codice prove/cont_v1.c; scritti alle 2026-11-14T15:27:58+01:00)

| # | Esito | Numeri (T-1 m, 400 traiettorie per comportamento) |
|---|---|---|
| T1 | **smentita** | il nucleo emette nell'88,6 % dei cicli nascosti per «prosegue» (attesi < 60 %) e nel 39,8 % per «sosta» (attesi < 35 %); lontano 24,6 %, sosta lunga 25,2 %, svolta 32,4 %, rallenta 54,6 %, torna 79,1 %. In questa geometria la regola dura 1,3–1,9 s, non 0,5 s |
| T2 | regge, salvo «torna» di misura | (a) prosegue 0,17 m a 1 s; sosta 1,55 m a 2 s e 2,73 m a 3 s; torna 1,99 m a 2 s (attesi > 2); punto su cella libera 91 % |
| T3 | regge | cop. 90 %: prosegue 1,00; sosta 0,68–0,87; torna 0,45 a 2 s; lontano 0,31 a 3 s; area 4,35 volte l'ombra a 3 s |
| T4 | **smentita in due parti su quattro** | guadagno su sosta a 3 s: 25 % (attesi ≥ 40 %); «lontano» coperto a 0,99 (attesi < 0,85: i modi a ±90° lo prendono); copertura ≥ 0,85 su prosegue, rallenta, sosta: regge; punto: 3,9 m d'errore a 4–5 s di sosta e 0,2–1,8 % di passi oltre v_max·dt |
| T5 | regge | d1: sosta 0,91–0,99, torna 0,93–1,00; lontano a 3 s 0,035 |
| T6 | **smentita** | d2: lontano a 3 s 0,087 (attesi ≥ 0,75), svolta 0,22–0,38; le aree reggono (0,26 a 1 s, 0,63 a 3 s) |
| T7 | regge fino a 3 s, **smentita a 4–5 s** | d2 miscela: 0,12 / 0,28 / 0,77 / 0,93 / 1,17 / 1,44 m; fermo 1,62–2,08 m e (a) 1,63–5,32 m a τ ≥ 2 s |
| T8 | regge per (a) e d2, **smentita per (c)** | d2: 0,00 % di passi oltre v_max·dt, 0,06–0,26 % all'indietro; (c) 0,17–1,84 % di passi oltre v_max·dt; (b) fino a 6,7 %, passo massimo 2,57 m |
| T9 | mista | salto di (a) su prosegue 0,25 m: regge; d2 0,88 m (attesi 0,3–0,8): smentita; prima misura nella regione al 90 %: 25–72 %: smentita, ma la misura era sbagliata (vedi sotto); identità d2 100 % salvo svolta 93,3 % (n = 149): sotto 0,97, sopra la soglia di smentita |
| T10 | regge | 19,3 µs per ciclo e per traccia |
| T11 | regge solo «(a) è il peggiore» | τ ≥ 2 s: d2 5,04–6,37, d1 5,06–6,31, (a) 6,38–8,38, (c) 4,73–6,42 |

**Notato dopo (non era previsto).** (1) La «prima misura dentro la regione» è una misura sbagliata per ogni regione che usa l'evidenza negativa: chi riemerge sta per
costruzione sul bordo della regione; la sostituisco con «entro 0,3 m dalla regione». (2) La regione delle particelle supera l'ombra dopo 4–5 s perché la massa esce oltre
la portata, dove lo spazio non osservato non ha limite: la regione mostrata va limitata alla zona coperta e la massa fuori va dichiarata con un numero («può aver lasciato
l'area: p»). (3) Nessun tasso di svolta copre «lontano» e «svolta» a 2 s al livello nominale (0,35–0,40 con tassi 0,3–1,0/s, lanci di taratura `tar_T1_LT*.txt`): il difetto è del
livello nominale, non del tasso. (4) La media delle particelle resta indietro su «prosegue»: salto di 0,9–1,0 m alla ricomparsa contro 0,25 m del Kalman.

## Modifiche fatte DOPO aver visto T-1 m (tutte dichiarate, codice prove/cont.c)

- **d3** = particelle con sosta (0,25/s), ripartenza (0,3/s, metà con direzione nuova uniforme) e cambio di direzione uniforme a 0,5/s; 5 % di massa uniforme sulle celle
  d'ombra raggiungibili; massa fuori da campo e portata dichiarata come «fuori area» e sempre parte della regione dichiarata.
- **Punto ibrido**: il punto del Kalman finché sta su celle non viste libere; dopo 3 cicli su celle viste libere passa alla media delle particelle; il punto mostrato non
  si sposta mai più di v_max·dt per ciclo.
- **Taratura conforme**: il livello interno della regione è il quantile empirico del punteggio (livello al quale la cella del vero entra nella regione) sul lancio di taratura
  `tar_T1_cal.txt` (traiettorie seme 8100, simulazione seme 81). Due tarature: sulla popolazione (miscela uniforme dei 7 comportamenti) e sul comportamento peggiore
  (n ≥ 100). Livelli fissati: L50 = 0.209 0.302 0.507 0.348 0.337 0.274; L90 = 0.672 0.744 0.983 0.866 0.841 0.870;
  W50 = 0.314 0.473 0.885 0.558 0.541 0.625; W90 = 0.734 0.905 0.986 0.987 0.985 0.984 (per τ = 0,5, 1, 2, 3, 4, 5 s).

## Previsioni della convalida (scritte alle 2026-11-14T15:27:58+01:00, prima dei lanci su dati nuovi)

Dati nuovi: V1 = stessa geometria, semi nuovi (traiettorie 9200, simulazione 92); V2 = pannello da 2 m (9300, 93); V3 = geometria della demo corretta
(pannello da 1 m a 1,9 m, attore a 2,3 m, portata 3 m; 9400, 94). I livelli restano quelli tarati su T-1 m.

- **V-a.** V1, «d3 ibr. tar.» (taratura sulla popolazione): copertura nella miscela fra 0,87 e 0,93 al 90 % e fra 0,45 e 0,55 al 50 %, a ogni τ. Smentita: una cella fuori.
- **V-b.** V1, «d3 ibr. peg.» (taratura sul peggiore): ogni comportamento con n ≥ 100 coperto ≥ 0,85 al 90 % a ogni τ; area al 90 % ≥ 0,75 dell'ombra a 2–5 s (cioè la
  garanzia per comportamento costa quasi tutta l'ombra). Area di «tar.» ≤ 0,55 a 3 s. Smentita: un comportamento < 0,80, oppure area di «peg.» < 0,6.
- **V-c.** V2 e V3 (livelli di un'altra geometria): la copertura della miscela al 90 % resta fra 0,80 e 0,97, ma almeno una cella τ esce da 0,85–0,95: i livelli vanno
  ritarati per geometria. Smentita del «vanno ritarati»: tutte le celle in 0,85–0,95.
- **V-d.** V3: il nucleo emette in < 60 % dei cicli nascosti per «prosegue» e < 20 % per «sosta». Punto ibrido su «prosegue»: salto mediano alla ricomparsa ≤ 0,30 m nelle
  tre scene (media delle particelle: ≥ 0,6 m in V1 e V2).
- **V-e.** Errore mediano del punto ibrido nella miscela, V1: ≤ 0,5 m fino a 1 s, ≤ 1,0 m a 2–3 s, **oltre 1,0 m a 4–5 s** (1,2–1,5 m): la soglia utile non regge oltre 3 s.
- **V-f.** Identità (≥ 1 % della massa entro 0,5 m dalla prima misura) di d3: ≥ 0,97 per prosegue, sosta, torna, rallenta nelle tre scene; svolta ≥ 0,85.
- **V-g.** Punto ibrido: 0 passi oltre v_max·dt (per costruzione); passi all'indietro oltre 3 cm < 3 % dei cicli.

## Esiti della convalida (prove/ris_V1.txt, ris_V2.txt, ris_V3.txt, 15:28; scritti alle 2026-11-14T15:31:18+01:00)

| # | Esito | Numeri |
|---|---|---|
| V-a | **regge** | V1, miscela: 90 % → 0,896 / 0,900 / 0,883 / 0,882 / 0,892 / 0,899; 50 % → 0,503 / 0,494 / 0,481 / 0,476 / 0,491 / 0,502 (n = 1197–2798) |
| V-b | **smentita sulla copertura**, regge sull'area | taratura sul peggiore: «lontano» 0,838 a 1 s e 0,705 a 2 s, «svolta» 0,735 a 2 s (soglia 0,80); area 0,79 / 0,79 / 0,75 / 0,73 dell'ombra a 2–5 s; area di «tar.» 0,45 a 3 s |
| V-c | **smentita la tenuta, confermato «vanno ritarati»** | V2: 0,939 / 0,953 / 0,920 / **0,629 / 0,669 / 0,713**; V3: 0,859 / 0,829 / 0,998 / 0,927 / 0,891 / 0,915 |
| V-d … V-g | vedi CONSEGNA (lette dopo questa riga) | |

**Notato dopo.** Con 500 particelle l'ombra da 14,75 m² ha circa 2 particelle per cella di 0,25 m: la regione «a massa più alta» sbaglia per difetto di campionamento. Lancio
esplorativo `espl_V2_np2000.txt` (15:29, 2000 particelle): d1 nominale nella miscela 0,979 / 0,961 / 0,939 / 0,896 / 0,895 / 0,914 contro 0,975 / 0,957 / 0,878 / 0,726 /
0,761 / 0,778; d3 (mio, con svolte a 0,5/s) resta peggiore di d1 su «prosegue» a 3 s (0,625 contro 0,905). **Il mio d3 non migliora d1**: la modifica del tasso di svolta
era adattata alla sola geometria di taratura.

## Previsione dell'ultimo giro (scritta alle 2026-11-14T15:31:18+01:00, prima dei lanci `fin_V1`, `fin_V3`; `fin_V2` ripete l'esplorativo con il punto ibrido su d1)

2000 particelle, d1 (sosta 0,25/s, ripartenza 0,4/s: i tassi dell'avversario, mai toccati da me), livello NOMINALE, massa «fuori area» dichiarata; punto ibrido = Kalman
finché sta su celle non libere, poi media di d1.
- **F-a.** Copertura al 90 % di d1 nella miscela fra 0,87 e 0,99 a ogni τ, in V1 e V3. Smentita: una cella sotto 0,85.
- **F-b.** Per comportamento (n ≥ 100): prosegue, sosta, sosta lunga, torna, rallenta ≥ 0,85 a ogni τ in V1, V2, V3; «lontano» e «svolta» sotto 0,85 in almeno un τ per scena
  (i comportamenti fuori modello restano coperti solo dal limite esterno). Smentita: uno dei cinque sotto 0,80 con n ≥ 100.
- **F-c.** Area al 90 % di d1 ≤ 0,65 dell'ombra a ogni τ in V1 e V2.
- **F-d.** Punto ibrido su d1, miscela: errore mediano ≤ 0,5 m fino a 1 s in ogni scena; salto mediano alla ricomparsa su «prosegue» ≤ 0,30 m in ogni scena.

## Esiti rimasti della convalida e dell'ultimo giro (scritti alle 2026-11-14T15:36:05+01:00)

| # | Esito | Numeri |
|---|---|---|
| V-d | **smentita sul nucleo**, mista sul salto | V3: il nucleo emette nel 68,9 % dei cicli per «prosegue» (attesi < 60 %) e nel 26,2 % per «sosta» (attesi < 20 %). Salto del punto ibrido su «prosegue»: 0,25 m (V1), **0,49 m (V2)**, 0,19 m (V3); media delle particelle 1,01 e 2,46 m |
| V-e | regge | V1: 0,12 / 0,27 / 0,85 / 0,98 / 1,24 / 1,45 m |
| V-f | **smentita** | identità di d3 (500 particelle) in V2: prosegue 58,8 %, sosta 36,9 %, rallenta 50,8 %; in V1 e V3 ≥ 99,2 % (svolta 91,5 %) |
| V-g | regge | 0 passi oltre v_max·dt; passi all'indietro 0,5–2,8 % |
| F-a | **smentita in una cella** | d1, 2000 particelle: V1 0,956 / 0,912 / **0,794** / 0,922 / 0,949 / 0,936; V3 0,935 / 0,900 / 0,973 / 0,959 / 0,947 / 0,925 (V2: 0,979 / 0,961 / 0,939 / 0,896 / 0,895 / 0,914) |
| F-b | regge | i cinque comportamenti modellati ≥ 0,865 con n ≥ 100 nelle tre scene; «lontano» 0,45 (V1, 2 s), 0,79 (V2), 0,65 (V3, 1 s); «svolta» 0,42, 0,68, 0,83 |
| F-c | regge | area al 90 %: V1 0,08–0,44; V2 0,04–0,55 dell'ombra |
| F-d | **smentita in due celle** | errore mediano a 1 s: 0,28 (V1), 0,20 (V2), **0,54 m (V3)**; salto su «prosegue»: 0,25, **0,50**, 0,19 m |

**Notato dopo.** Nella geometria della demo, a 4 e 5 s, il punto (ibrido o media) è peggiore di «fermo all'ultima misura»: 1,39 contro 1,10 m e 2,01 contro 1,22 m
(`fin_V3.txt`, miscela): lì resta nascosto soprattutto chi è uscito oltre la portata o è fermo. L'identità di d1 con 2000 particelle in V2: prosegue 99,0 %, sosta 93,9 %,
torna 100 %, rallenta 97,2 %, svolta 81,8 % (n = 99).
