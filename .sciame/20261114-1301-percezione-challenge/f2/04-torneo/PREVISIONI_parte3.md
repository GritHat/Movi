# Previsioni — avversario, f2 torneo, parte 3 (H-009, H-014, H-015, H-016; K-001, K-002, K-005)

Scritte alle 2026-11-14T13:41:09+01:00, PRIMA di scrivere e di eseguire `scena_parte3.py`. Non ho aperto gli script degli autori (solo schede, firme, triage).
Scena mia, simulata (2D in pianta): sensore in (0,0) che guarda +y, campo ±43,5°, portata 6 m; pannello a y = 2 m, largo 1 m o 2 m, centrato;
pedone puntiforme a y = 4 m (ombra larga 2 m o 4 m a quella distanza), 1,0–1,5 m/s; 15 Hz; rumore 5 cm isotropo; Pd = 0,9 se visibile; nessun falso allarme.
Comportamenti: prosegue; sosta 2–4 s nell'ombra; torna indietro; esce dal lato lontano (radiale, oltre la portata).
Famiglie: (a) Kalman a velocità quasi costante, q = 0,2, cerchio al 95 %, senza e con la prova del raggio di H-014 (chiusa dopo M = 1 o 3 fotogrammi «più lontano», scade a 1 m);
(b) disco 2,5 m/s·τ ∩ non osservato; (c) 250 particelle, evidenza negativa (1−Pd), esistenza di Bernoulli r0 = 0,99, morta sotto 0,05, senza e con modo «sosta».
Misure a 0,5/1/2/3 s dall'ingresso in ombra, solo se il soggetto è ancora non visibile.

| ID | Misura | Esito atteso | Soglia di smentita (della mia previsione) |
|---|---|---|---|
| P3-1 (K-002a) | Sosta, pannello 1 m, 3 s: quota della regione in celle viste libere e contenimento | cerchio Kalman: ≥ 50 % in libere; particelle con sosta: ≤ 5 % in libere e contiene ≥ 80 %; disco: 0 % in libere, contiene ≥ 95 %, ma copre ≥ 90 % dell'ombra | cerchio < 50 %; particelle > 25 % o contenimento < 80 %; disco contenimento < 95 % |
| P3-2 (K-002b, H-009) | A 1 s, quota dell'ombra coperta dalla regione | disco ≥ 50 % sul pannello da 1 m (non informa più); cerchio e particelle < 50 % | disco < 50 % a 1 s (pannello 1 m) |
| P3-3 (K-001, H-014) | Sosta: traccia chiusa dalla prova del raggio mentre il soggetto è nascosto | a 4 m (ombra 2 m): < 20 % dei casi, perché scade prima a 1 m di raggio (≈ 1,2 s) che uscire dall'ombra (≈ 1,5 s); pedone a 3 m (ombra 1,5 m): > 50 % | ≥ 20 % a 4 m, oppure ≤ 50 % a 3 m |
| P3-4 (H-015, K-005) | Sosta 2–4 s, pannello 1 m: identità tenuta alla riemersione (r ≥ 0,05 e misura nel cancello) | particelle SENZA modo sosta: < 80 % (il falsificatore del triage scatta); CON modo sosta ≥ 80 %; Kalman con raggio 0 % (scaduta o chiusa) | senza sosta ≥ 80 %; con sosta < 80 % |
| P3-5 (ombra −20 cm) | Ombra stimata più stretta di 20 cm (a 4 m), pannello 1 m | raggio M = 1: chiusa all'ingresso in ≥ 90 %; M = 3: < 30 %; particelle: r < 0,5 poco dopo l'ingresso in ≥ 30 % dei casi; con sosta: identità tenuta < 85 % (le soste nella banda muoiono) | M = 1 < 90 %; particelle r < 0,5 in < 30 %; identità con sosta ≥ 85 % |
| P3-6 (falso libero, H-016/H-015) | Bersaglio visibile non rilevato per k fotogrammi, celle date per libere | campo aperto: r < 5 % a k = 4 (Pd 0,9), 5 (0,8), 7 (0,7); all'uscita dall'ombra: massa entro 0,5 m dal vero < 5 % entro 3 fotogrammi (Pd 0,9) e P(in ombra) > 90 % a soggetto in vista; raggio M = 1 chiude al 1º fotogramma; il disco esclude il vero dal 1º fotogramma | massa giusta ≥ 5 % dopo 10 fotogrammi |
| P3-7 (v > v_max, H-009) | Prosegue a v = 2,0…3,5 m/s, pannello 2 m: il disco contiene il vero a 0,5 s | ≥ 95 % per v ≤ 2,4; ≤ 20 % per v ≥ 3,0; Kalman e particelle ≥ 80 % | disco ≥ 50 % a v = 3,0 |
| P3-8 (due bersagli) | Entrano insieme da lati opposti; tornano entrambi indietro nell'ombra: scambio d'identità alla prima riemersione | Kalman (Mahalanobis) ≥ 80 % di scambi; particelle ≥ 50 %; disco: ambiguo nel 100 % (nessuna identità); se proseguono entrambi: scambi ≤ 10 % | scambi < 50 % nel caso «tornano» per il Kalman |

## Esiti (compilati DOPO l'esecuzione)

### Previsione aggiunta alle 2026-11-14T13:47:47+01:00 (dopo aver visto main1 con 250 particelle, prima di eseguire con 1000)
| P3-9 (numero di particelle, H-016 contro H-015) | pannello 1 m, 1000 particelle invece di 250 (`NP3=1000`) | il contenimento a 3 s per chi esce dal lato lontano resta < 50 % (è un errore di modello, non di campionamento); l'identità sulla sosta SENZA modo sosta resta < 80 % | lontano ≥ 80 % oppure senza sosta ≥ 80 % |

## Esiti (scritti alle 2026-11-14T13:49:55+01:00, dopo l'esecuzione; file `risultati_*_parte3.txt`)

| ID | Esito | Numeri ottenuti |
|---|---|---|
| P3-1 | **mista** | cerchio Kalman a 3 s: 22,9 % dell'area (37,1 % della massa gaussiana) in celle viste libere, sotto il 50 % previsto → la mia previsione sul cerchio è SMENTITA a 3 s (a 2 s: 51,3 % area, 64,1 % massa: il cerchio a 3 s ha raggio 3,77 m ed esce in gran parte dal campo). Particelle con sosta: 0,2 % e contenimento 100 %: regge. Disco: 0 %, 100 %, copre il 100 % dell'ombra: regge |
| P3-2 | **regge** | a 1 s il disco copre il 97,8 % dell'ombra (pannello 1 m) e il 59,8 % (2 m); cerchio 31,0 % / 18,1 %; particelle 32–35 % / 20 %. A 0,5 s il disco copre 44,5 % / 23,6 % |
| P3-3 | **mista** | a 4 m: M = 3 → 0 % (regge); M = 1 → 16,0 % (n = 100) e 20,3 % (n = 300), alla soglia: smentita alla lettera, ma per un meccanismo che non avevo previsto (il punto previsto resta 0–5 cm fuori dall'ombra al momento dell'ingresso: chiusa a 0,04 s). A 3 m: M = 1 56,3 % (regge), M = 3 14,0 % (smentita). A 2,5 m: 86,3 % e 53,0 %. Scadenza a SCONOSCIUTO a 1,12 s |
| P3-4 | **regge** (pannello 1 m) | identità sulla sosta: senza modo sosta 71 % (1 m), 28 % (2 m); con modo sosta 100 % (1 m) ma 76,3 % (2 m, non coperto dalla previsione); Kalman con raggio 0 % |
| P3-5 | **mista** | M = 1: chiusa all'ingresso 100 % (regge); M = 3: 45–50 % (previsto < 30 %: SMENTITA, è peggio); r < 0,5 nei primi 6 fotogrammi: 50–59 % (regge); identità con sosta 68 % (regge), morte a 3 s 23 % (con sosta) e 55 % (senza) |
| P3-6 | **regge** sulla soglia | campo aperto: massa giusta < 5 % a k = 4 / 5 / 7 (Pd 0,9 / 0,8 / 0,7), come previsto; all'uscita dall'ombra: < 5 % a k = 5 per i tre Pd (avevo scritto ≤ 3: sbagliato), parte da 0,17; P(in ombra) 0,95–0,99 a soggetto in vista; raggio in campo aperto chiude al 1º (M = 1) o 3º (M = 3) fotogramma nel 100 %; il disco esclude il vero dal 1º fotogramma nel 100 % |
| P3-7 | **regge** (con una smentita di contorno) | disco a 0,5 s: 100 / 90 / 10 / 0 / 0 % per v = 2,0 / 2,4 / 2,6 / 3,0 / 3,5 m/s (avevo scritto ≥ 95 % a 2,4: è 90 %, per il rumore dell'ultima misura); Kalman 100 %, particelle 99–100 % |
| P3-8 | **mista** | «tornano entrambi»: Kalman 74 % (1 m) e 61 % (2 m) di scambi (attesi ≥ 80 %; sopra la soglia di smentita del 50 %), di cui senza segnale d'ambiguità 44 % e 10 %; particelle 48 % e 10 % (attese ≥ 50 %: smentita sul pannello da 2 m). «Proseguono»: Kalman 0 % (regge); particelle 4 % (1 m) ma 79 % (2 m): SMENTITA la mia attesa ≤ 10 %. Disco: ambiguo 100 % (proseguono), 71 % e 60 % (tornano; il resto assegnato giusto per esclusione), mai uno scambio |
| P3-9 | **non risolta** | 1000 particelle: uscita dal lato lontano, contenimento a 3 s 29 % con modo sosta (regge: < 50 %); identità sulla sosta senza modo sosta 81 % contro 71 % a 250 particelle (soglia 80 %, n = 100, intervallo di circa ± 8 punti) |

## Notato DOPO (non previsto prima: vale come osservazione, non come prova registrata)
- L'ombra di un pannello largo 1 m a 2 m dal sensore, alla distanza del pedone (4 m), è larga 2 m, non 1 m: il transito normale dura in media 1,70 s, oltre la scadenza a 1 m di raggio (1,12 s). Identità tenuta dalla regola di H-014 su chi PROSEGUE: 0 %; con r_max = 1,5 m: 30 %.
- Chi esce dal lato lontano: le particelle tengono il 99,8 % della massa fuori dalle celle viste libere e la loro regione al 95 % contiene il vero nel 22 % (1 m) e 41 % (2 m) dei casi a 3 s.
- Ombra stimata più LARGA di 20 cm: il disco ha il 14,4 % della regione in celle davvero viste libere a 0,5 s; le particelle l'11–23 % della massa a 2–3 s.
- Il cerchio al 95 % del Kalman (q = 0,2) contiene il vero a 1 s nel 77–88 % dei casi con manovre (sosta 88 %, torna 81 %, lontano 77 %; 2 m: 92 / 96 / 86 %).
