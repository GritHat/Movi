# Previsioni (sciame-tempo-reale, f19-volo/02-sensori-hw)

Scritte il 2026-11-15T04:36:33+01:00, prima di cercare le fonti e di fare i conti.

- P1. La catena su CPU generica (prototipo, modo interfaccia) sta fra 0,1 e 55 ms di elaborazione per ciclo (misure già esistenti); la latenza dalla cattura all'avviso è dominata dalla rivisita e dall'acquisizione del sensore (decine-centinaia di ms), non dall'elaborazione. Smentita se l'elaborazione su CPU supera il 50 % della latenza totale nel caso radar a rivisita rapida.
- P2. Il fattore di accelerazione prudente dell'hardware dedicato sulla nostra parte di calcolo (filtro, associazione, regione) sta fra 10x e 100x rispetto alla CPU; sull'elaborazione del segnale radar (FFT, CFAR) fra 10x e 50x rispetto alla CPU, 2-5x rispetto alla GPU. Smentita se le fonti aperte indicano fattori sistematicamente < 5x o > 1000x per carichi analoghi.
- P3. Catena intera con hardware dedicato e radar AESA a 20-50 Hz: latenza 30-80 ms (cattura-avviso, caso peggiore inclusa una rivisita). Smentita se il conto dà < 10 ms o > 200 ms.
- P4. Il tempo di reazione umano (0,75-2,5 s) è almeno 10 volte la latenza della catena dedicata: domina l'umano. Smentita se il rapporto è < 5.
- P5. Per un aereo a 250 m/s con avviso a operatore umano (reazione 2,5 s + manovra), la distanza minima di avviso utile supera 1 km; con sistema di bordo automatico (latenza di macchina < 0,1 s) scende di oltre 500 m. Smentita se la differenza è < 300 m.
