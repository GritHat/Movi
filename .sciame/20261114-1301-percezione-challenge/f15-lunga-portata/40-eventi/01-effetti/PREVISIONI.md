# Previsioni scritte prima dei conti (sciame-sensori, 40-eventi/01-effetti)

Ora: 2026-11-15T00:12:09+01:00 (orologio della macchina). Scritte prima di eseguire `conti.py`.

- **sens-ev-P1.** Il conto ITU-R P.838-3 (coefficienti letti dalla pagina itu-rpy) a 10 GHz, polarizzazione
  orizzontale, riproduce k = 0,01217 e alfa = 1,2571 (valori della tabella riportati da un riassunto di ricerca).
  Smentita: scarto > 2 % su k o > 0,01 su alfa.
- **sens-ev-P2.** Lo stesso conto a 77 GHz e 25 mm/h dà fra 8 e 13 dB/km (la rassegna arXiv:2112.08936 dice
  «al livello di 10 dB/km»). Smentita: fuori da 8-13.
- **sens-ev-P3.** La legge di Kim a 905 nm con visibilità 0,5 km dà 34 +- 2 dB/km (la rassegna dice «circa 35»).
  Smentita: fuori da 32-36.
- **sens-ev-P4.** Una sfera metallica di 2 cm ha sezione radar ottica pi*r^2 = -35 dBsm +- 1 (valore riportato da
  un riassunto di ricerca su uno studio FOD). Smentita: fuori da -36..-34.
- **sens-ev-P5.** In nebbia con visibilità 200 m il LiDAR tele (320 m in aria limpida) scende sotto 200 m, mentre il
  radar in banda X perde meno del 5 % di portata. Smentita: LiDAR >= 200 m o radar X sotto il 95 %.
- **sens-ev-P6.** Con pioggia a 25 mm/h il ritorno di volume della pioggia in una cella di un radar in banda X a
  1 km supera la sezione radar di un multirotore piccolo (0,01 m2) se non si filtra in Doppler. Smentita: ritorno
  della pioggia < 0,01 m2.
- **sens-ev-P7.** Un frammento di 5 cm è rilevabile dal radar per droni oltre 1 km (se metallico) ma dal LiDAR tele
  solo sotto 200 m. Smentita: radar < 1 km o LiDAR >= 200 m.
