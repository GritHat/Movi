# Previsioni — f14, 20-inclusione (sciame-scene-dinamiche)

Scritte alle 2026-11-14T18:51:13+01:00, prima di scrivere ed eseguire `conti_blocco.py`. Letti prima: contratto f14, addendum 10, PROFILI, USO, CLASSIFICATORE, ATTACCO (per intero), soluzione v3 finale (§0, 1.1, 1.4, 1.6, 1.7, 1.10–1.12, §2, inizio di §3 e §7), fascicolo di geometria r. 225–231. Conosco già le cifre dell'attacco (`esito_attacco.txt`, parte A1–A3): le previsioni sd-P2 e sd-P4 non sono cieche, sono un ricalcolo con codice mio.

Formula unica: d_serve = (v + v_ego)(t_conf + tau + T_r) + v_ego^2/(2 a_fr) + v v_ego/a_fr + C, con t_conf 0,267 s, tau 0,155 s (stimata), T_r 1,0 s (ipotesi), C 0,95 m (fascicolo di geometria r. 231), portata 3 m; velocità da `../01-profili/classi.json` (15 classi).

- **sd-P1.** Stazione fissa: classi con d_serve <= 3 m a v_tip: esattamente 3 su 15 (persona a piedi, veicolo a guida automatica, aereo al traino); a v_max: 0 su 15. Smentita: un conteggio diverso.
- **sd-P2.** Velocità coperta: 1,44 m/s con C 0,95 (tolleranza 0,01: il fascicolo usa 1,425 s, io 1,422); 1,83 con C 0,40; 2,11 con C 0. Smentita: scarto oltre 0,01.
- **sd-P3.** Regola composta del blocco (w_ombra = massimo che non torna indietro, pavimento w_scen; v_obj = max(v osservata + 2 sigma, v_scen, v_max dell'etichetta non smentita); rilascio oltre w_ombra; d del «suolo visto libero» da w_scen): su 20 000 sequenze a caso di etichette (assente, in ritardo, sbagliata, che cambia, smentita, fuori scenario) 0 cicli con fascia più stretta del «senza etichette», 0 cali nel tempo, 0 cicli con v_obj più bassa, 0 rilasci in più, 0 differenze nel d di settore. Controllo negativo (regola «max con la base» e «senza etichetta = inviluppo»): oltre il 50 % delle sequenze con almeno una violazione. Smentita: 1 ciclo nella regola composta, oppure controllo negativo sotto il 50 % (la prova non vedrebbe il difetto).
- **sd-P4.** Avviso dopo il contatto (3 m percorsi in meno di t_conf + tau = 0,422 s, cioè oltre 7,1 m/s): 3 classi a v_tip, 10 su 15 a v_max. Smentita: conteggi diversi.
- **sd-P5.** Con la fascia di scenario accesa, le classi che da sole portano w_scen >= 1,7 m (nessun tratto «suolo visto libero»: d = 3 − w <= 1,3 m) sono 11 su 15. Smentita: conteggio diverso.
- **sd-P6.** Persona non vedente in cammino (v_ego 1,0; T_r 1,5; a_fr 1,0; tutte ipotesi): d_serve supera 3 m già per un ostacolo fermo. Smentita: d_serve(0) <= 3 m.

## Esiti (scritti dopo, alle 2026-11-14T18:55:16+01:00; uscita in `esito_conti.txt`, esecuzione 18:51:14–18:51:17)

- sd-P1 **regge**: 3 su 15 a v_tip (persona a piedi 2,94 m; veicolo a guida automatica 2,37; aereo al traino 2,94), 0 su 15 a v_max.
- sd-P2 **regge**: 1,442 / 1,828 / 2,110 m/s (1,439 col prodotto 1,425 s del fascicolo).
- sd-P3 **regge per la regola composta** (0 sequenze su 20 000 in ognuno dei cinque conteggi; il conteggio sul d di settore è 0 per costruzione, non misura niente) ed è **smentita nel controllo negativo**: 7 068 su 20 000 (0,353), sotto la soglia del 50 % scritta prima. Il difetto si vede, ma meno di quanto previsto: nelle mie sequenze l'etichetta arriva tardi e di rado. La prova dell'attacco (0,791) è più severa della mia.
- sd-P4 **regge**: 3 a v_tip, 10 su 15 a v_max; soglia 7,11 m/s.
- sd-P5 **regge**: 11 su 15.
- sd-P6 **regge**: 3,37 m per l'ostacolo fermo.

Notato dopo, non previsto: con T_r = 1,5 s la persona non vedente FERMA ha una velocità coperta di 1,07 m/s, sotto il passo normale (1,4 m/s).
