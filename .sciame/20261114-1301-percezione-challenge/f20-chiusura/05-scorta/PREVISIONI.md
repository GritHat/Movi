# Previsioni F7 «scorta» (sciame-tracciamento, f20-chiusura/05-scorta)

Scritte alle 2026-11-15T05:53:49+01:00 (`date -Is`), PRIMA di scrivere il simulatore e prima di ogni prova.
Tutto simulato dalle schede e da ipotesi dichiarate; nessun sensore fisico; etichette a mano. Solo osservazione e
avviso: «seguire» = mantenere la traccia.

## Celle
- Varianti: `lato` (collisione 30-100 m di lato), `davanti` (30-100 m sul percorso, fra portatore e bersaglio),
  `dietro` (30-100 m dietro), `vira` (geometria `davanti` + bersaglio che vira a 8 m/s² durante la saturazione),
  `F7c` (controllo: quasi collisione a 30-60 m senza urto, riflesso solare che satura la camera 0,5 s nella metà dei
  passaggi).
- Configurazioni: `att` (radar piccolo di bordo + camera, schede/ipotesi) e `sda` (radar a scansione elettronica +
  EO/IR raffreddato; ipotesi).
- Semi: sviluppo `SeedSequence(20261120, …)` indici 0-9; valutazione `SeedSequence(20261121, …)`, 60 passaggi per
  cella (200 per F7c). La valutazione si lancia una volta sola, dopo aver fissato i parametri.

## Definizioni (fissate ora)
- **Continuità del bersaglio** (per passaggio): in ogni ciclo di 0,1 s dalla conferma fino alla fine, il bersaglio
  vero sta in una regione dichiarata dalla traccia del bersaglio (raggio = max(r99 gaussiano, inviluppo
  r0 + δv·τ + a_max·τ²/2)) o in una regione di traccia nuova dichiarata «possibile bersaglio».
- **Identità mantenuta**: la traccia con l'id del bersaglio è viva alla fine del passaggio, la sua stima è entro
  30 m dal vero, e nessun aggiornamento da detrito o falso allarme le è stato dato senza segnarlo «dubbio».
- **Riacquisizione**: primo aggiornamento della traccia del bersaglio da una misura vera del bersaglio dopo la fine
  della saturazione ottica; si misura anche la riacquisizione da camera (fumo).
- **«Libero» sul bersaglio o su un frammento**: un ciclo in cui il punto vero sta in una cella che il sistema dichiara
  libera (osservata, nella portata di rilevamento del frammento più piccolo, fuori da ogni regione).
- **Volume dei detriti**: i campioni (ogni 0,5 s) dei frammenti veri dentro il volume dichiarato.
- **Avviso al portatore**: se il percorso previsto del portatore (5 s) interseca il volume, avviso entro 2 cicli.
- **Falso evento**: un evento «collisione/esplosione» dichiarato in F7c.

## Previsioni e soglie di smentita (Wilson 95 % per passaggio)
| # | Misura | Previsione | Smentita se |
|---|---|---|---|
| P1 | continuità, ogni cella | 60/60 | < 57/60 in una cella |
| P2 | identità mantenuta | ≥ 51/60 (incoraggiante) in lato e dietro; in davanti e vira att forse sotto (45-55) | < 51/60 in lato o dietro |
| P3 | riacquisizione ≤ 2 s dalla fine della saturazione | ≥ 51/60 ovunque (il radar non è accecato) | < 51/60 in una cella |
| P4 | «libero» su bersaglio o frammento | 0 in ogni cella | ≥ 1 |
| P5 | volume dei detriti | contiene 100 % dei campioni (per costruzione nel modello, vento nullo) | < 99 % dei campioni |
| P6 | avviso al portatore se il percorso interseca | 100 % dei casi che intersecano (davanti sempre, lato a volte) | un caso senza avviso |
| P7 | falsi eventi F7c | 0/200 | ≥ 1 |
| P8 | camere dichiarate non affidabili durante saturazione | 100 % dei cicli saturi | un ciclo saturo con camera «affidabile» |

Rischio principale che prevedo: in `davanti` gli echi dei detriti cadono nella stessa direzione del bersaglio; la porta
in distanza e la porta Doppler dovrebbero separarli, ma la `vira` può spostare il bersaglio fuori porta
(continuità dalla regione, identità a rischio).
