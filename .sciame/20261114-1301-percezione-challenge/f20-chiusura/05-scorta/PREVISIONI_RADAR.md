# Previsioni F7r «scorta col radar accecato» (sciame-sensori, f20-chiusura/05-scorta)

Scritte alle 2026-11-15T06:22:16+01:00 (`date -Is`), PRIMA di scrivere `scorta_f7r.py` e prima di ogni prova.
Tutto simulato; nessun sensore fisico. Solo osservazione e avviso.

## Modello aggiunto (ipotesi, da fissare nel codice senza cambiarlo dopo la valutazione)
- **R1 saturazione del ricevitore radar:** nessuna misura radar in [T_EV, T_EV + d_rad), con
  d_rad = 0,2 + 1,8·(100 − d)/70 s, d = distanza portatore-urto in m, limitata in [0,2; 2] (30 m → 2 s, 100 m → 0,2 s).
  Il ricevitore segnala la saturazione (bandierina AGC/ADC): ipotesi ottimista sull'innesco, dichiarata.
- **R2 occultamento nella nube:** Pd del bersaglio × 0,3 quando il segmento portatore-bersaglio passa nella sfera
  della nube densa (centro = baricentro dei frammenti in aria, raggio = 80° percentile delle loro distanze), per 3 s
  dall'urto.
- **R3 perdita totale (cella `totale`):** geometria `davanti` a 30-50 m, radar perso 2 s, camera saturata 2-3 s, fumo.
- Durante la saturazione radar: niente «libero» (il campo è non osservato) e fino a 3 scansioni dopo il ritorno.

## Celle e semi
- `lato`, `davanti`, `vira`, `totale` × `att`, `sda`: 60 passaggi ciascuna; `F7c`: 200 per configurazione.
- Semi nuovi: `SeedSequence(20261122, …)`. Sviluppo (se serve) su `20261123`, indici 0-4. Valutazione una sola volta.

## Previsioni e soglie di smentita (per passaggio, Wilson 95 %)
- **P1 continuità** (bersaglio dentro la regione dichiarata in ogni ciclo): 60/60 in ogni cella. Smentita se < 60/60.
- **P2 riacquisizione** entro 2 s dal ritorno del radar (prima misura del bersaglio vero associata alla sua traccia,
  o riacquisizione presunta da una traccia nata dal bersaglio vero): ≥ 51/60 in ogni cella. Smentita se < 51/60.
- **P3 «libero»** sul bersaglio o su un frammento: 0/60 in ogni cella (0/200 in F7c). Smentita se ≥ 1.
- **P4 associazione spuria non dichiarata** (misura non del bersaglio sulla traccia del bersaglio fuori dal volume, o
  riacquisizione presunta da una traccia non nata dal bersaglio): 0/60. Smentita se ≥ 1.
- **P5 C osservata contro C(τ) di `curva_F7.json`** (perdita totale): la C 2D del filtro durante l'accecamento sta
  entro ±0,10 dalla curva per τ ≤ 2 s. Smentita se lo scarto medio per τ supera 0,10.

## Che cosa mi aspetto (scritto prima, per distinguere dopo)
- P1 regge (l'insieme di presenza cresce con τ).
- **P2 a rischio in `att` nelle celle `davanti`, `vira`, `totale`:** dopo 1 s di perdita il bersaglio si riaggancia solo
  per riacquisizione presunta (≥ 5 colpi a 5 Hz ≈ 1 s) e solo **fuori** dal volume dei detriti, che cresce di circa
  90 m/s; il bersaglio a 150-300 m davanti rischia di starci dentro. Mi aspetto meno di 51/60 lì; in `sda` (20 Hz)
  meglio ma con lo stesso blocco del volume.
- Rischio P3/P4: se l'evento viene dichiarato tardi (radar cieco), il volume nasce tardi e piccolo. Contromisura
  prevista nel codice, dichiarata prima: la saturazione del ricevitore radar vale come indizio d'evento (come la
  saturazione della camera) e fissa t0 del volume all'inizio della saturazione.
