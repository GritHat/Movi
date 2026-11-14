# PREVISIONI — sciame-sensori, f15-lunga-portata/02-sensori

Scritte alle 2026-11-15T00:01:05+01:00 (`date -Is`), PRIMA di aprire le schede tecniche e di fare i conti.
Tutto è conto da scheda: nessuna prova su sensore fisico.

Misura: portata di rilevamento scalata con l'equazione del radar, R(σ) = R_ref · (σ/σ_ref)^(1/4), e portata
ottica dal criterio dei pixel sul bersaglio, R = d · f / (n_px · passo).

- **sens-P1.** Un radar di sorveglianza per droni di classe commerciale (scheda pubblica) scalato a 0,01 m² dà una
  portata fra 0,5 e 5 km. *Smentita:* fuori da [0,5; 5] km.
- **sens-P2.** Lo stesso radar scalato a 100 m² dà una portata «da equazione» oltre la portata strumentata
  dichiarata: la portata utile per l'aereo di linea è quindi limitata dallo strumento, non dalla sensibilità.
  *Smentita:* R(100 m²) < portata strumentata.
- **sens-P3.** Una camera EO con ottica lunga (campo stretto, ≤ 2°) rileva (≥ 2 pixel, criterio di Johnson
  «rilevamento» ~1 ciclo) un drone di 0,3 m entro 1–5 km; il riconoscimento (≥ 6–8 pixel) sotto 1,5 km.
  *Smentita:* rilevamento fuori da [1; 5] km.
- **sens-P4.** LiDAR automobilistico: nessuna scheda pubblica dichiara più di 300 m al 10 % di riflettività.
  *Smentita:* una scheda aperta oggi con > 300 m @ 10 %.
- **sens-P5.** Radar 4D automobilistico: portata massima dichiarata ≥ 250 m, risoluzione azimutale ≤ 2°.
  *Smentita:* una delle due non rispettata nella scheda presa a riferimento.
- **sens-P6.** ADS-B: aggiornamento di posizione ~2 volte al secondo; accuratezza dichiarata (NACp ≥ 8) < 93 m.
  *Smentita:* fonte normativa con valori diversi.
- **sens-P7.** Con rivisita ≥ 1 s e bersaglio a 70 m/s (aereo in avvicinamento), lo spostamento fra due rivisite è
  ≥ 70 m: maggiore dell'accuratezza del sensore, quindi «fra due rivisite» è la voce dominante del non osservato.
  *Smentita:* rivisita dichiarata < 0,2 s per i radar di sorveglianza scelti.

Esiti: in fondo a SENSORI_LUNGA_PORTATA.md.
