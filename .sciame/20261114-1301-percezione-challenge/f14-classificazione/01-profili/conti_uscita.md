## A. Per classe: arresto proprio, tempo sui 3 m, fascia di guardia che servirebbe

Fascia: w_cl = v_max * (eta' 0.133 + latenza 0.155 + tenuta 0.067) = v_max * 0,355 s; w = 0,40 m copre 1,13 m/s.

| classe | v_tip | v_max | frenata v_tip²/(2·dec_tip) (m) | con reazione di chi guida (m) | tempo per 3 m a v_tip (s) | a v_max (s) | w_cl (m) |
|---|---|---|---|---|---|---|---|
| persona_a_piedi | 1,4 | 2,5 | 0,65 | — | 2,14 | 1,20 | 0,89 |
| persona_di_corsa | 3,0 | 8,0 | 2,25 | — | 1,00 | 0,38 | 2,84 |
| bicicletta | 4,3 | 8,3 | 4,62 | 11,07 | 0,70 | 0,36 | 2,95 |
| monopattino | 4,2 | 5,6 | 4,41 | 10,71 | 0,71 | 0,54 | 1,99 |
| carrello_elevatore | 2,2 | 4,5 | 2,69 | 5,99 | 1,36 | 0,67 | 1,60 |
| agv_magazzino | 1,0 | 2,0 | 0,50 | 0,80 | 3,00 | 1,50 | 0,71 |
| auto_area_lavoro | 2,8 | 8,3 | 1,15 | 5,35 | 1,07 | 0,36 | 2,95 |
| auto_strada_urbana | 8,3 | 13,9 | 10,13 | 22,58 | 0,36 | 0,22 | 4,93 |
| mezzo_piazzale | 1,7 | 8,3 | 0,96 | 3,51 | 1,76 | 0,36 | 2,95 |
| aereo_rullaggio | 9,0 | 15,4 | 40,50 | 54,00 | 0,33 | 0,19 | 5,47 |
| aereo_traino | 1,4 | 4,2 | 1,96 | 4,06 | 2,14 | 0,71 | 1,49 |
| treno_banchina | 11,0 | 16,7 | 75,62 | 92,12 | 0,27 | 0,18 | 5,93 |
| tram_fermata | 5,6 | 13,9 | 13,07 | 21,47 | 0,54 | 0,22 | 4,93 |
| treno_manovra | 4,2 | 8,3 | 17,64 | 23,94 | 0,71 | 0,36 | 2,95 |
| multirotore_lento | 3,0 | 19,0 | 2,25 | 3,15 | 1,00 | 0,16 | 6,75 |

## B. Distanza d'avviso d_avv (m) alla velocita' TIPICA della classe, per profilo; in grassetto se <= 3 m

| classe | stazione_fissa | ugv_lento | uav_stazionario | uav_lento | persona_non_vedente_bastone | persona_ferma | operatore_remoto |
|---|---|---|---|---|---|---|---|
| ostacolo_fermo | **0,40** | **1,19** | **0,40** | 3,26 | **2,06** | **0,40** | **2,69** |
| persona_a_piedi | **2,02** | **1,83** | **1,04** | 3,90 | 3,67 | **2,02** | 5,43 |
| persona_di_corsa | 3,86 | **2,55** | **1,76** | 4,63 | 5,52 | 3,86 | 8,55 |
| bicicletta | 5,37 | 3,14 | **2,36** | 5,22 | 7,02 | 5,37 | 11,09 |
| monopattino | 5,25 | 3,10 | **2,31** | 5,18 | 6,91 | 5,25 | 10,90 |
| carrello_elevatore | **2,94** | **2,19** | **1,40** | 4,27 | 4,60 | **2,94** | 6,99 |
| agv_magazzino | **1,56** | **1,64** | **0,85** | 3,72 | 3,21 | **1,56** | 4,64 |
| auto_area_lavoro | 3,63 | **2,46** | **1,67** | 4,54 | 5,29 | 3,63 | 8,16 |
| auto_strada_urbana | 9,99 | 4,96 | 4,18 | 7,04 | 11,64 | 9,99 | 18,91 |
| mezzo_piazzale | **2,36** | **1,96** | **1,17** | 4,04 | 4,02 | **2,36** | 6,01 |
| aereo_rullaggio | 10,79 | 5,28 | 4,50 | 7,36 | 12,45 | 10,79 | 20,28 |
| aereo_traino | **2,02** | **1,83** | **1,04** | 3,90 | 3,67 | **2,02** | 5,43 |
| treno_banchina | 13,11 | 6,19 | 5,41 | 8,27 | 14,76 | 13,11 | 24,19 |
| tram_fermata | 6,87 | 3,74 | **2,95** | 5,81 | 8,52 | 6,87 | 13,64 |
| treno_manovra | 5,25 | 3,10 | **2,31** | 5,18 | 6,91 | 5,25 | 10,90 |
| multirotore_lento | 3,86 | **2,55** | **1,76** | 4,63 | 5,52 | 3,86 | 8,55 |

## C. Per profilo: spazio d'arresto, velocita' di classe massima coperta dai 3 m, inviluppo del non classificato

| profilo | v_ego | T_r | a_fr | arresto proprio v_ego·(τ+T_r)+v²/2a (m) | v di classe massima coperta da 3 m (m/s) | classi ammesse: v_max d'inviluppo (m/s) | d_avv del non classificato (m) | portata che servirebbe alla v_max di persona_a_piedi (m) |
|---|---|---|---|---|---|---|---|---|
| stazione_fissa | 0,0 | 1,0 | — | 0,00 | 2,25 | 2,5 | 3,29 | 3,29 |
| ugv_lento | 1,0 | 0,3 | 1,5 | 0,79 | 3,98 | 4,5 | 3,24 | 2,33 |
| uav_stazionario | 0,0 | 0,3 | 3,0 | 0,00 | 5,71 | 19,0 | 9,04 | 1,54 |
| uav_lento | 3,0 | 0,3 | 3,0 | 2,86 | -0,58 | 19,0 | 11,91 | 4,40 |
| persona_non_vedente_bastone | 1,0 | 1,0 | 1,0 | 1,66 | 0,82 | 8,3 | 11,64 | 4,94 |
| persona_ferma | 0,0 | 1,0 | — | 0,00 | 2,25 | 8,3 | 9,99 | 3,29 |
| operatore_remoto | 1,0 | 1,8 | 1,5 | 2,29 | 0,16 | 4,5 | 11,49 | 7,58 |

## D. Etichetta sbagliata: di quanto si accorcerebbe l'avviso se la distanza dipendesse SOLO dall'etichetta

Stazione fissa, v_max di classe. «Vero» = classe reale; «detto» = etichetta. Deficit = d_avv(vero) − d_avv(detto).

| vero | detto | d_avv vero (m) | d_avv detto (m) | deficit (m) | con la regola max(base, classe) e inviluppo per l'incerto |
|---|---|---|---|---|---|
| auto_area_lavoro | persona_a_piedi | 9,99 | 3,29 | 6,70 | un'etichetta sicura ma sbagliata NON e' coperta dalla regola: resta il deficit; l'etichetta incerta prende l'inviluppo (9,99 m con persona_a_piedi, carrello_elevatore, auto_area_lavoro) |
| carrello_elevatore | persona_a_piedi | 5,60 | 3,29 | 2,31 | un'etichetta sicura ma sbagliata NON e' coperta dalla regola: resta il deficit; l'etichetta incerta prende l'inviluppo (9,99 m con persona_a_piedi, carrello_elevatore, auto_area_lavoro) |
| carrello_elevatore | agv_magazzino | 5,60 | 2,71 | 2,89 | un'etichetta sicura ma sbagliata NON e' coperta dalla regola: resta il deficit; l'etichetta incerta prende l'inviluppo (9,99 m con persona_a_piedi, carrello_elevatore, auto_area_lavoro) |
| persona_di_corsa | persona_a_piedi | 9,64 | 3,29 | 6,35 | un'etichetta sicura ma sbagliata NON e' coperta dalla regola: resta il deficit; l'etichetta incerta prende l'inviluppo (9,99 m con persona_a_piedi, carrello_elevatore, auto_area_lavoro) |

## E. Esiti delle previsioni (soglie scritte prima, in PREVISIONI.md)

| # | misura | esito |
|---|---|---|
| E1 | d_avv = 2,02 m | regge |
| E2 | d_avv a 8 m/s = 9,64 m | regge |
| E3 | 10 classi su 15 oltre 3 m | regge |
| E4 | ostacolo fermo 2,06 m; pedone incontro 3,67 m | regge |
| E5 | pedone 1,83 m; veicolo a 5 m/s 3,46 m | regge |
| E6 | treno in banchina 13,11 m; aereo in rullaggio 10,79 m | smentita |
| E7 | velocita' con fonte aperta oggi: 9 su 30; lette solo in un risultato di ricerca: 6; ipotesi o memoria: 15 | smentita |
