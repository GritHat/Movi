# Previsioni dell'attacco f14 (sciame-avversario) — scritte alle 2026-11-14T18:44:35+01:00, prima di ogni programma e di ogni lettura in rete

Letti prima: contratto f14, addendum 10, PROFILI.md, USO_DELLA_CLASSE.md, CLASSIFICATORE.md, righe 184, 303, 427 della soluzione v3 finale, testa e ordine dei tagli del piano finale. Nessun conto mio ancora eseguito.

- **av-P1 (regola «max con la base», PROFILI esperto-dominio-1 e CLASSIFICATORE C-2).** Con «non classificato = inviluppo del sito» e «etichetta sicura = max(base, v_max della classe)», su sequenze a caso di etichette (assente, in ritardo, sbagliata, che cambia in occlusione) esiste almeno un ciclo in cui la fascia w CON etichetta è più stretta della fascia SENZA etichetta (inviluppo). Misura: quota di sequenze con almeno un ciclo w_con < w_senza, 20 000 sequenze. Smentita: 0 sequenze. Mi aspetto oltre il 30 %.
- **av-P2 (regola di USO §2, massimo che non torna indietro con pavimento w_scen).** Stesse sequenze: 0 cicli con w_con < w_senza. Smentita: almeno 1. Mi aspetto che regga.
- **av-P3 (USO §5, «la classe può solo anticipare»: v_obj <- min(v_max, v + a_max*T_ant)).** Esiste un caso in cui v_obj con l'etichetta è SOTTO la velocità osservata (v + 2 sigma): carrello a 4 m/s etichettato «pedone» (v_max 2,5). Misura: d_serve con etichetta meno d_serve senza. Smentita: differenza >= 0 in tutti i casi provati. Mi aspetto circa -2 m.
- **av-P4 (coerenza cinematica, oggetto fermo).** Un veicolo fermo etichettato «persona» non è mai smentito finché sta fermo (0 scatti su 2 000 tracce di 3 s), e se parte da 2,5 m con 3 m/s^2 lo scatto di c1 arriva DOPO il contatto in più del 90 % delle tracce. Smentita: scatto prima del contatto in più del 10 %.
- **av-P5 (conti di portata).** Rifacendo d_avv di PROFILI con il tempo di conferma (0,267 s, usato in USO e non in PROFILI) le classi fuori dai 3 m a v_tip per la stazione fissa passano da 10 a 11 su 15 (esce il carrello). Smentita: restano 10. Inoltre: nella colonna «non vedente che cammina» PROFILI omette il termine v_classe*v_ego/a_fr, e il pedone a 1,4 m/s chiede oltre 5 m e non 3,7. Smentita: differenza sotto 0,5 m.
- **av-P6 (avviso dopo l'impatto).** Con 3 m, t_conf + tau = 0,422 s: l'avviso stesso esce dopo il contatto sopra 7,1 m/s; fra le 15 classi a v_tip almeno 3 (auto urbana, aereo in rullaggio, treno in banchina). Smentita: meno di 3.
- **av-P7 (valori).** Di sei valori campionati (1,4 m/s F1; 1,27-1,46 e 1,75-2,53 F2; 3,4 m/s^2 F4; 16-19 nodi F6; 1,5 m/s^2 F7; 15,5 km/h F11) almeno 5 tornano alla riapertura della fonte. Smentita: 4 o meno tornano. Almeno un valore usato in un conto «in grassetto» è R o I (non verificato).
- **av-P8 (ore).** Il piano finale non ha nessuna voce per classi, profili o etichette oltre al taglio n. 1 «etichetta persona (non si comincia)»: 0 ore previste contro 2,5-5,5 chieste. Smentita: una voce del piano con ore per l'etichetta.

## Esiti (scritti alle 2026-11-14T18:48:32+01:00, dopo le prove; uscite in esito_attacco.txt, esito_piano.txt, scaricato/)

- av-P1 **regge**: 15 814 su 20 000 (0,791) con almeno un ciclo più stretto del «senza etichetta»; caso a mano 1,60 → 0,89 m.
- av-P2 **regge**: 0 su 20 000 (regola di USO §2). È un massimo: lo zero è una proprietà della regola, non una misura del sistema.
- av-P3 **regge**: −2,42 m (carrello a 4 m/s etichettato «pedone»), −5,26 m (auto a 6 m/s).
- av-P4 **regge**: 0 scatti su 2 000 da fermo; scatto prima del contatto 2 su 2 000 (3,0 m/s²) e 0 su 2 000 (1,5 m/s²).
- av-P5 **regge**: da 10 a 11 classi su 15 fuori dai 3 m con il tempo di conferma (carrello 3,53 m); non vedente in cammino e pedone a 1,4 m/s: 5,07 m contro 3,67.
- av-P6 **regge**: 3 classi a v_tip (auto urbana, aereo in rullaggio, treno in banchina), 10 a v_max.
- av-P7 **regge**: 6 valori su 6 ritrovati nel sorgente delle pagine (più i 160 e 190 ms); valori R o I nei grassetti: carrello (R1), traino (R5), T_r (I).
- av-P8 **regge**: nel piano finale la sola menzione è il taglio n. 1 (riga 90).

**Notato dopo, non previsto:** le tre cifre del dominio (2,25; 2,11 o 1,76; 1,44 m/s nel fascicolo di geometria r. 231); l'invariante tr-I15 sui rilasci; la soglia «w_scen > 1,3 m» della riga fissa; il conflitto sull'età dell'etichetta fra USO e CLASSIFICATORE; il rilancio del modello del piano (0,428 → 0,195 con 2,5 h; 0,053 con 5,5 h); treno e aereo sempre «tagliati» e quindi non etichettabili per RC-6; la v_max della persona è una media. Otto previsioni su otto reggono: cercavo dove mi aspettavo di trovare.
