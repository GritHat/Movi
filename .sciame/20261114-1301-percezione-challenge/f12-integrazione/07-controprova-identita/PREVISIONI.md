# PREVISIONI — f12, 07-controprova-identita (`sciame-avversario`)

Scritte alle **2026-11-14T18:20:17+01:00** (`date -Is`), dopo aver letto IDENTITA_SU_PROFONDITA.md, PREVISIONI.md, DIFFERENZE.md/.diff,
prova.py dell'autore, catalogo.py, genera.py, misura_passaggi.py; **prima di eseguire qualunque corsa mia**.
Tutto è simulazione. Configurazione attaccata: «tutte_p» (la finale dell'autore), confrontata con «prima».
Semi miei: k = 300…309 (mai usati: l'autore ha usato 0–29 su disco, 100–129, e preparato 200–229 senza eseguirli).
Soglie (fissate ora): continuità **regge** se ≥ 8 su 10, **smentita** se ≤ 6 su 10, 7 = non risolta (N = 10 è piccolo:
Wilson 8/10 = [49–94]). Sicurezza: **0** celle·fotogramma «libero» nell'ombra vera in più rispetto a «prima», e **0**
fotogrammi con la persona nascosta (dentro la griglia) fuori dall'avviso; un solo caso = smentita.

## R — rifacimento
- **R1** rilancio `prova.py nuovi424` (conf prima, tutte, tutte_p) e `nuovi848` (tutte_p): cifre identiche a quelle
  dichiarate (semi dal nome → deterministico): tutte_p 29, 29, 30 su 30 a 424; 30, 29, 29 a 848; scatola 100/100.
  Smentita: una cifra diversa.
- **R2** riconto con programma mio (`riconta.py`) dai .jsonl dell'autore: ogni cifra della tabella del §3 coincide.
  Smentita: una differenza ≥ 1.

## A — attacchi alle correzioni (tutte_p, D435i nominale, 424 px, caso a12, 10 semi, salvo diverso avviso)
- **A1** pannello a 2,1 m e persona a 2,8 m (0,7 m dietro). La regola «rifiuta se portata − d ≤ fascia» (3,0 − 2,8 =
  0,2 ≤ 0,4) dovrebbe vietare ogni riaggancio: prevedo **≤ 2 su 10** (smentita della continuità). Regge se ≥ 8.
- **A1b** pannello a 1,5 m e persona a 2,0 m (stessi 0,5 m di distacco, più vicino): prevedo ≥ 8 su 10.
- **A2** 640×360 (risoluzione mai provata) con a12; D455 e Gemini 335 con **a05** (l'autore ha provato solo a12 sugli
  altri profili): prevedo ≥ 8 su 10 in ciascuno (ci credo al 60 %).
- **A3** livello «limite»: ≤ 3 su 10 (l'autore: 0). Buchi ×3,5 sul livello limite (p_buco_materiale, p_buco_bordo,
  p_buco_incidenza ×3,5, tetto 0,95): 0–2 su 10; sicurezza: 0 «libero» in ombra in più (50 %).
- **A4** persona alta 1,2 m: ≥ 8; **bambino 1,0 m: ≤ 6** (la regola del picco contro un pannello di 1,6 m lo scarta);
  persona scura: ≥ 8; **nera: ≤ 6**.
- **A5** 1,6 m/s: ≥ 8 su 10; 0,5 m/s (a05, k = 300…): ≥ 8 su 10.
- **A6** errore di posa ±0,5° (il sensore è a 15,5° o 14,5°, la catena crede 15°): continuità ≥ 8 su 10; 0 tracce
  confermate sul pavimento vuoto; 0 «libero» in ombra in più.
## B — ciò che la correzione può aver rotto
- **B1** scatola 15 cm a 2,0 e 2,8 m, tutte_p: «occupato» entro 15 cm ≥ 9 fotogrammi su 10 (mappa invariata: regge).
  Ma come GRUPPO (un gruppo con centro entro 0,25 m): a 2,8 m **< 9 su 10** (prevedo che la soglia dei pixel attesi
  la tolga dai gruppi: la scatola è nella mappa ma non è più un oggetto inseguibile).
- **B2** cubo di 10 cm a 2,0 m: nella mappa ≥ 9/10, come gruppo < 9/10. Bambino (1,0 m) fermo in campo aperto a 2,5 m:
  gruppo ≥ 9/10. Bambino fermo che tocca il fianco del pannello (x = 0,72, z = 1,95): gruppo proprio (centro entro
  0,3 m, larghezza < 0,8 m) in < 50 % dei fotogrammi con tutte_p (fuso o scartato).
- **B3** persona che ricompare tagliata dal bordo del campo (pannello spostato a x 0,6–1,6; cammina da sinistra a destra
  fino a uscire dal campo): identità non ripresa (≤ 2 su 10 «stessa»); misuro il vuoto = fotogrammi con la persona
  visibile ≥ 50 % dopo l'ombra e nessuna traccia «osservato» su di lei. Prevedo vuoto mediano ≤ 5 fotogrammi (nasce
  un'identità nuova) — se > 10 fotogrammi (0,67 s) è un buco di continuità peggiore di «prima».
- **B4** avviso perpetuo: (i) pannello fermo: dopo il riaggancio l'avviso resta acceso nel 100 % dei fotogrammi
  successivi a ombra vuota; (ii) se dopo il passaggio il pannello viene tolto (sequenza concatenata con il pavimento
  vuoto) l'avviso si spegne entro 5 fotogrammi (0,33 s) in ≥ 9 su 10; smentita se ancora acceso dopo 15.
## E — l'estraneo, rifatto con rumore
- A entra da sinistra e si ferma nascosta dietro il pannello; B, mai visto, era già nascosto e ne esce a destra.
  10 semi, 424 e 848, D435i nominale. Prevedo: l'identità di A passa a B in ≥ 8 su 10 (la geometria non distingue);
  con tutte_p A nascosta fuori dall'avviso: **0** fotogrammi; cella di A mai «libero». Smentita di F-409: ≥ 1.
## S — sicurezza (vale più della continuità)
- Su tutte le corse sopra: «libero» nell'ombra vera (centro di cella) di tutte_p = quello di «prima»; persona nascosta
  in griglia fuori dall'avviso: 0. Al limite con buchi ×3,5 non scommetto (50 %).

## Dopo (aggiunte con l'ora, mai riscrivendo sopra)

### 2026-11-14T18:25:36+01:00 — esiti parziali letti ora, un incidente, e una prova in più scritta PRIMA di eseguirla
- **Incidente (mio):** il rifacimento (`prova_autore.py`, copia di prova.py) alla fine cancella `tmp/`, la stessa cartella
  temporanea del mio `attacco.py`: il blocco «geometria» è morto a metà (FileNotFoundError, `registro_attacchi_1.txt`).
  Spostata la mia cartella temporanea in `tmp_att/` e rilanciato il blocco intero; nessun parametro cambiato.
  Prima ancora, il primo lancio del rifacimento è fallito per un errore di shell (zsh non spezza `$PY`): nessuna corsa.
- Letti finora (blocchi estraneo, persona, e geometria a metà): A1 0/10 (regge la previsione «≤ 2»), A1b 9/10, A4 bambino
  2/10 (previsto ≤ 6), nera 7/10 (previsto ≤ 6: **non risolta**), scura 10/10, alta 1,2 m 9/10; estraneo 9/10 e 10/10.
- **R3 (nuova): replica del criterio su semi mai usati k = 200…229** (blocchi `ultimi424/848` dell'autore, mai eseguiti),
  configurazione tutte_p. Dai tre campioni dell'autore il tasso è 86–88 su 90 per caso: con p ≈ 0,96 una cella da 30
  resta ≥ 28 circa 85–92 volte su 100, sei celle insieme circa una volta su due. **Prevedo (50 %) che almeno una delle sei
  celle (a12, a05, b × 424, 848) scenda sotto 28 su 30.** Il criterio «passa» è smentito in replica se una cella < 28;
  regge se tutte ≥ 28. La linea a 2,1 m (k = 200…209): ≤ 2 su 10 come nell'autore.

### 2026-11-14T18:27:08+01:00 — B3 smentisce la MIA previsione; un caso più stretto, scritto prima di eseguirlo
- **B3 (pannello a x 0,2–1,2, la persona si ferma a x = 2,0):** previsto «identità non ripresa (≤ 2 su 10)»; ottenuto
  **9 su 10 «stessa»**, 0 fotogrammi senza traccia su 546 (`att_geometria.jsonl`). La mia previsione è **smentita**: fra
  il bordo dell'ombra e il bordo del campo restavano circa 0,2 m liberi e il riaggancio è avvenuto lì.
- **B3b (nuovo, blocco `bordo2`):** pannello a x 0,5–1,5; la persona esce dall'ombra GIÀ sul bordo del campo e si ferma
  3 s a x = 2,05 (visibile per circa l'80 %, tagliata sia dall'ombra sia dal bordo). Previsione: continuità ≤ 2 su 10;
  vuoto (visibile ≥ 50 % senza traccia «osservato») mediano ≤ 5 fotogrammi perché nasce un'identità nuova; se il vuoto
  mediano supera 10 fotogrammi (0,67 s) la correzione F-402 ha aperto un buco di continuità che «prima» non aveva
  (confronto con la colonna «prima» sugli stessi semi). Regge (per l'autore) se ≥ 8 su 10 «stessa».

### 2026-11-14T18:32:03+01:00 — esiti finali (tutte le corse sono finite; cifre in `risultati/RICONTO.md` e `risultati/ATTACCHI.md`)
| Previsione | Esito | Cifra (tutte_p) |
|---|---|---|
| R1 rifacimento identico | **regge** | 579 + 193 righe rifatte, 0 diverse nei campi deterministici |
| R2 riconto | **regge** | ogni cifra del §3 dell'autore ritrovata (130 = senza «limite» e senza d; 108 = senza i 2 «mai nascosto») |
| R3 replica k = 200…229: una cella < 28 (50 %) | **avverata: il criterio cade in replica** | 424: 30, 30, 28; 848: 29, 30, **27** (caso b) |
| A1 2,1 m / 2,8 m: ≤ 2 su 10 | **regge** (continuità smentita) | 0/10 |
| A1b 1,5 m / 2,0 m: ≥ 8 | regge | 9/10 |
| A2 640 px; D455 a05; Gemini a05: ≥ 8 | regge | 10/10; 10/10; 9/10 |
| A3 limite ≤ 3; limite + buchi ×3,5 ≤ 2 | regge (continuità smentita) | 0/10; 0/10. **Non previsto:** buchi ×3,5 al nominale 10/10 |
| A3 sicurezza al limite + buchi (50 %) | **smentita la sicurezza, ma già in «prima»** | 4 celle·fot. «libero» in ombra vera su 600, uguali in «prima» |
| A4 1,2 m ≥ 8; bambino ≤ 6; scura ≥ 8; nera ≤ 6 | regge; regge; regge; **non risolta** | 9/10; 2/10; 10/10; 7/10 |
| A5 1,6 m/s e 0,5 m/s ≥ 8 | regge | 10/10; 10/10 |
| A6 posa ±0,5°: ≥ 8, 0 tracce | **smentita a +0,5°** | +0,5°: 6/10 e tracce in 2 sequenze di pavimento su 30; −0,5°: 10/10 e 0 |
| B1 scatola nella mappa ≥ 9/10; gruppo a 2,8 m < 9/10 | regge; regge | mappa 120/120; gruppo a 2,8 m 22/30 e 23/30 (prima 30/30) |
| B2 cubo 10 cm: gruppo < 9/10; bambino aperto ≥ 9/10; al pannello < 50 % | regge tutte | gruppo 0/60; 200/200; 70/200 (prima 33/200) |
| B3 bordo del campo ≤ 2 | **smentita (la mia)** | 9/10 |
| B3b bordo stretto ≤ 2, vuoto ≤ 5 fot. | regge | 0/10 stessa identità, 10/10 identità nuova, vuoto 0/499 |
| B4 (i) avviso 100 % dopo; (ii) spento entro 5 fot. dalla rimozione | (i) regge; **(ii) smentita** | (i) 160/160; (ii) acceso 30 fot. dopo in 10/10 (anche «prima») |
| E estraneo: identità a B ≥ 8/10; A fuori avviso 0 | regge | 9/10 e 10/10; 0/264 |
| S sicurezza: nessun «libero» in più, 0 nascosti fuori avviso | regge | 5 = 5 celle·fot.; 0/2360 fot. |
- **Notato dopo (non previsto):** nei blocchi statici ho scritto `n=30` credendo fossero i fotogrammi: sono 30 SEMI da 10
  fotogrammi (A6_pavimento, A3_pavimento) e 20 semi da 10 (B2_bambino/adulto). Le cifre riportano la numerosità vera.
- **Notato dopo:** in B4 la traccia del pannello sparito diventa «previsto» e apre un suo strato (`diag.py rimozione`):
  l'avviso residuo non è attribuibile al solo strato orfano di F-409. In B3b, k = 302, l'identità vecchia segna un
  riaggancio mentre la persona ha già un'identità nuova: a che cosa, non l'ho guardato.
