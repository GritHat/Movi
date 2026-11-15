# PREVISIONI (sciame-kalman, f15/12-traiettorie)

Scritte il **2026-11-15T01:15:16+01:00** (`date -Is`), prima di scrivere il codice delle prove e prima di ogni cifra.
(La consegna dice «oggi 14 novembre»; l'orologio della macchina dice 15: riporto l'orologio.)

## Metodo fissato prima

- Dati: `01-dati/traiettorie/<classe>/*/verita.csv` (704 scene). Ogni scena = un tratto.
- Divisione per tratto, stratificata per classe, seme 20261115: metà taratura, metà prova. Le cifre si riportano SOLO sulla prova.
- Misure: ai tempi dei campioni della verità, sottocampionati al periodo del sensore; rumore polare dalla scheda (`02-sensori/parametri_lunga_portata.json`); posizione del sensore: ipotesi.
  aerei: radar di superficie/area, σ 7,5 m isotropa, 1 s (valore «ipotesi» nella scheda); droni: radar di sorveglianza IRIS σr 0,6 m, σaz 0,75°, σel 1,0°, 1 s, sensore a 1,5 km dal primo punto (ipotesi); auto: radar 4D σr 0,15 m, σaz 0,3° (ipotesi), 0,1 s, a 100 m; treni: LiDAR Tele-15 σr 0,02 m, σang 0,03°, sensore a 300 m, al passo dei dati (3 s).
- Filtro: `Traccia` di `04-moto/movi_lp.py` (IMM della classe di `regole_lunga_portata.json`), senza associazione (un oggetto per scena: l'associazione NON è provata qui).
- Occlusione: durata D ∈ {2, 5, 10, 20, 30} s; 10 istanti iniziali a caso per tratto e durata (seme 20261115+D), dopo almeno 10 misure; si valuta al primo campione di verità con τ ≥ D (τ reale riportato).
- Zona: sfera centrata su p + v τ (RegionePrevisione), raggio r_D + 3(σp + σv τ); r_D tarato conforme al livello 0,90 sul residuo `errore − 3(σp+σvτ)` della metà di taratura. Q: fattore su q_cv e q_manovra da {0,25; 0,5; 1; 2; 4; 8}, scelto sulla taratura come quello di area media minima (la copertura la garantisce la taratura conforme).
- Tipo di tratto nella finestra occlusa (dalla verità): **arresto** se la velocità scende sotto max(1 m/s; 0,2 v0) o v0 < 1 m/s; altrimenti **virata** se la rotta cambia più di 15°; altrimenti **accelerazione** se |Δv| > max(2 m/s; 0,15 v0); altrimenti **rettilineo**.
- Wilson al 95 % su ogni frequenza.

## Previsioni e soglie di smentita

| # | previsione | misura | smentita se |
|---|---|---|---|
| K1 | Sulla metà di prova la copertura della zona al livello 0,90 è ≥ 0,85 per ogni classe fino a 10 s | quota dentro, Wilson | limite superiore di Wilson < 0,90 in una classe × durata ≤ 10 s, o stima < 0,85 |
| K2 | La copertura scende nei tratti «virata» e «arresto» rispetto al «rettilineo» | quota per tipo | in nessuna classe virata/arresto è sotto il rettilineo di più di 0,05 |
| K3 | L'errore mediano del punto a 10 s ordina le classi: aerei > droni > auto > treni (in metri) | mediana | ordine diverso |
| K4 | L'insieme di possibile presenza (avviso, inviluppo dello scenario) contiene la verità nel 100 % dei casi di prova | quota fuori | ≥ 1 caso fuori in una classe (allora un v_max o a_max dell'inviluppo è smentito dai dati) |
| K5 | L'ala fissa senza pilota ha l'errore a 5 s più grande in rapporto alla velocità (proposta dati-2) | mediana errore/(v τ) | un'altra classe ha il rapporto maggiore |
| K6 | NIS medio sulle misure di prova fra 0,5 e 2 volte i 3 gradi di libertà, per classe | media NIS | fuori da [1,5; 6] |
| K7 | I profili `auto_strada_urbana` e `treno_banchina` sono superati in velocità (già visto da sciame-dati); `drone_ala_fissa` (40 m/s) e `aereo_linea_avvicinamento` (90 m/s) di `regole_lunga_portata.json` sono superati da almeno un tratto | quota di tratti con v massima oltre v_max | aereo_linea: 0 tratti oltre |
| K8 | Le prove durano meno di 10 minuti | tempo a muro | oltre |
